"""
Deduplication module - checks if problem was already solved.
Uses local AI (Ollama) + text similarity.
"""

import json
from typing import List, Dict
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using TF-IDF."""
    if not text1 or not text2:
        return 0.0

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return float(similarity[0][0])
    except Exception:
        # Fallback to simple matching
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def check_keyword_overlap(keywords1: List[str], keywords2: List[str]) -> float:
    """Check keyword overlap between two problem sets."""
    if not keywords1 or not keywords2:
        return 0.0

    set1 = set(k.lower() for k in keywords1)
    set2 = set(k.lower() for k in keywords2)

    intersection = set1.intersection(set2)
    union = set1.union(set2)

    return len(intersection) / len(union) if union else 0.0


def check_with_ollama(problem: Dict, history: List[Dict]) -> bool:
    """Use Ollama to check if problem is unique (runs locally, no API needed)."""
    try:
        import ollama

        history_titles = [p["title"] for p in history[-20:]]  # Last 20 problems

        prompt = f"""Analyze if this problem is unique compared to previously solved problems.

NEW PROBLEM: {problem['title']}
DESCRIPTION: {problem.get('description', '')[:300]}

PREVIOUSLY SOLVED:
{chr(10).join(f'- {t}' for t in history_titles)}

Is this a UNIQUE problem that hasn't been solved before? Reply with only "YES" or "NO"."""

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response["message"]["content"].strip().upper()
        return "YES" in answer

    except Exception as e:
        print(f"   Ollama unavailable: {e}")
        # Fallback: assume unique if Ollama not available
        return True


def is_duplicate(problem: Dict, history: List[Dict]) -> bool:
    """Check if a problem is duplicate of any previously solved problem."""
    if not history:
        return False

    for prev_problem in history:
        # Check title similarity
        title_sim = calculate_text_similarity(
            problem["title"],
            prev_problem["title"]
        )
        if title_sim > 0.7:
            return True

        # Check keyword overlap
        kw_overlap = check_keyword_overlap(
            problem.get("keywords", []),
            prev_problem.get("keywords", [])
        )
        if kw_overlap > 0.5:
            return True

    return False


def check_uniqueness(problems: List[Dict], history_data: Dict) -> List[Dict]:
    """Filter out duplicate problems."""
    previous_problems = history_data.get("problems", [])

    unique_problems = []

    for problem in problems:
        # First do quick text similarity check
        if is_duplicate(problem, previous_problems):
            print(f"   Skipping (duplicate): {problem['title'][:50]}...")
            continue

        # Then use Ollama for deeper check (if available)
        is_unique = check_with_ollama(problem, previous_problems)

        if is_unique:
            unique_problems.append(problem)
            print(f"   Unique: {problem['title'][:50]}...")
        else:
            print(f"   Skipping (similar to past): {problem['title'][:50]}...")

    return unique_problems
