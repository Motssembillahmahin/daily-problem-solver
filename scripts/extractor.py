"""
Extracts problems from scraped content using keyword analysis.
"""

import re
from typing import List, Dict
from collections import Counter

from scripts.matching import mentions


# Phrases that indicate someone is actually stuck or frustrated. At least one
# of these must be present for content to count as a problem.
STRONG_INDICATORS = [
    "how do i", "how to", "how can i", "problem", "issue", "struggle",
    "struggling", "difficulty", "need help", "looking for", "error", "fails",
    "failing", "failed", "can't", "cannot", "doesn't work", "not working",
    "broken", "frustrated", "annoying", "pain", "stuck", "confused",
    "any advice", "any suggestions", "what's the best way", "is there a way",
    "unable to", "keeps crashing", "why does", "why is",
]

# Supporting signals. These corroborate a strong indicator but never stand alone.
WEAK_INDICATORS = [
    "improve", "automate", "simplify", "better", "alternative", "recommend",
    "suggestion", "advice", "tool", "app", "software", "workaround", "fix",
    "solution", "challenge",
]

# Product-announcement phrasing. Announcements describe something that was
# built, not a problem to solve, so they are rejected outright.
ANNOUNCEMENT_MARKERS = [
    "show hn", "launch hn", "introducing", "announcing", "we built",
    "i built", "we've built", "i've built", "we made", "i made",
    "we launched", "just launched", "now available", "release notes",
    "changelog", "yc s2", "yc w2",
]

# Tech categories
CATEGORIES = {
    "productivity": ["productivity", "organize", "task", "schedule", "time", "workflow"],
    "ai_ml": ["ai", "machine learning", "deep learning", "neural", "model", "gpt", "llm"],
    "webdev": ["website", "web app", "frontend", "backend", "api", "react", "nextjs"],
    "automation": ["automate", "automation", "script", "bot", "cron", "pipeline"],
    "security": ["security", "privacy", "encrypt", "authentication", "hack", "vulnerability"],
    "data": ["data", "database", "analytics", "visualization", "dashboard", "csv"],
    "mobile": ["mobile", "app", "android", "ios", "flutter", "react native"],
    "devops": ["deploy", "docker", "kubernetes", "ci/cd", "cloud", "aws", "server"],
    "health": ["health", "fitness", "mental", "wellness", "track", "monitor"],
    "finance": ["finance", "budget", "invest", "crypto", "payment", "accounting"]
}


def extract_keywords(text: str) -> List[str]:
    """Extract relevant keywords from text."""
    words = re.findall(r'\b\w+\b', text.lower())
    # Filter out common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
        'his', 'her', 'its', 'our', 'their', 'what', 'which', 'who', 'whom',
        'where', 'when', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'own', 'same', 'so', 'than', 'too', 'very', 'just', 'about', 'also'
    }
    return [w for w in words if w not in stop_words and len(w) > 2]


def categorize_problem(title: str, text: str) -> str:
    """Categorize a problem based on its content, or "general" if nothing matches."""
    combined = (title + " " + text).lower()

    scores = {
        category: sum(1 for kw in keywords if mentions(kw, combined))
        for category, keywords in CATEGORIES.items()
    }

    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "general"


def is_announcement(title: str, text: str) -> bool:
    """True when content announces a product rather than describing a problem."""
    combined = (title + " " + text).lower()
    return any(marker in combined for marker in ANNOUNCEMENT_MARKERS)


def is_problem(title: str, text: str) -> bool:
    """Check if content describes a problem someone is actually having."""
    if is_announcement(title, text):
        return False

    combined = (title + " " + text).lower()
    if not any(indicator in combined for indicator in STRONG_INDICATORS):
        return False

    weak_hits = sum(1 for indicator in WEAK_INDICATORS if mentions(indicator, combined))
    strong_hits = sum(1 for indicator in STRONG_INDICATORS if indicator in combined)
    return strong_hits + weak_hits >= 2


def calculate_priority(item: Dict) -> int:
    """Calculate problem priority score."""
    score = 0

    # Engagement signals
    score += min(item.get("score", 0) / 10, 20)
    score += min(item.get("num_comments", 0) / 5, 15)

    # Source weight
    source_weights = {
        "Stack Overflow": 20,
        "Ask HN": 18,
        "GitHub Issues": 16,
        "Hacker News": 12,
        "r/technology": 10,
        "r/programming": 10,
        "r/MachineLearning": 10,
        "Google Trends": 5,
    }
    for source, weight in source_weights.items():
        if source in item.get("source", ""):
            score += weight
            break

    return int(score)


def extract_problems(raw_content: List[Dict]) -> List[Dict]:
    """Extract problems from raw scraped content."""
    problems = []

    for item in raw_content:
        title = item.get("title", "")
        text = item.get("text", "")

        if not title:
            continue

        # Check if it's a problem
        if is_problem(title, text):
            keywords = extract_keywords(title + " " + text)
            category = categorize_problem(title, text)
            priority = calculate_priority(item)

            problems.append({
                "title": title,
                "description": text if text else title,
                "source": item.get("source", "unknown"),
                "url": item.get("url", ""),
                "category": category,
                "keywords": keywords[:10],
                "priority": priority,
                "created_at": item.get("created_at", ""),
                "reason": f"Trending problem in {category} category"
            })

    # Sort by priority
    problems.sort(key=lambda x: x["priority"], reverse=True)

    return problems
