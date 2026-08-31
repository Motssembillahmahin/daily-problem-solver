#!/usr/bin/env python3
"""
Text Summarizer - Summarize text using extractive method
Usage: python summarize.py <file.txt> [--sentences 3]
"""

import re
import sys
from collections import Counter

def split_sentences(text: str) -> list:
    """Split text into sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if len(s) > 10]

def score_sentences(sentences: list, word_frequencies: dict) -> list:
    """Score sentences based on word frequency."""
    scores = []
    for sentence in sentences:
        words = re.findall(r'\w+', sentence.lower())
        score = sum(word_frequencies.get(word, 0) for word in words)
        scores.append((score, sentence))
    return scores

def summarize(text: str, num_sentences: int = 3) -> str:
    """Summarize text using extractive method."""
    sentences = split_sentences(text)
    
    if len(sentences) <= num_sentences:
        return text
    
    # Calculate word frequencies
    words = re.findall(r'\w+', text.lower())
    word_freq = Counter(words)
    
    # Normalize frequencies
    max_freq = max(word_freq.values())
    for word in word_freq:
        word_freq[word] /= max_freq
    
    # Score and rank sentences
    scored = score_sentences(sentences, word_freq)
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Get top sentences
    top_sentences = [s[1] for s in scored[:num_sentences]]
    
    # Maintain original order
    ordered = []
    for sentence in sentences:
        if sentence in top_sentences:
            ordered.append(sentence)
    
    return " ".join(ordered)

def summarize_file(file_path: str, num_sentences: int = 3):
    """Summarize a text file."""
    try:
        with open(file_path) as f:
            text = f.read()
        
        summary = summarize(text, num_sentences)
        
        print(f"\nOriginal: {len(text)} characters, {len(split_sentences(text))} sentences")
        print(f"Summary: {len(summary)} characters, {len(split_sentences(summary))} sentences")
        print(f"\nSummary:\n{'='*50}\n{summary}\n{'='*50}")
    
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python summarize.py <file.txt> [--sentences N]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    num_sentences = 3
    
    if "--sentences" in sys.argv:
        idx = sys.argv.index("--sentences")
        num_sentences = int(sys.argv[idx + 1])
    
    summarize_file(file_path, num_sentences)
