"""Tests for problem extraction and categorisation."""

from scripts.extractor import categorize_problem


def test_returns_general_when_no_category_keywords_match():
    """Content matching no category must not be silently filed under one."""
    assert categorize_problem("Zork quux", "frobnicate the widget") == "general"


def test_does_not_match_keywords_inside_longer_words():
    """'bootstrappable' contains 'app' but is not a mobile problem."""
    assert categorize_problem("Bootstrappable Builds", "How and why we did it") == "general"


def test_categorises_by_matching_keywords():
    assert categorize_problem("Budget planner", "track invest payment accounting") == "finance"


def test_picks_the_category_with_the_most_matches():
    title = "Deploy a machine learning model"
    text = "docker kubernetes cloud aws server deploy the neural model"

    assert categorize_problem(title, text) == "devops"


def test_matches_multi_word_and_punctuated_keywords():
    assert categorize_problem("CI/CD is broken", "our ci/cd setup keeps failing") == "devops"
    assert categorize_problem("Machine learning intro", "machine learning basics") == "ai_ml"
