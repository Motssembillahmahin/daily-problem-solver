"""Tests for problem extraction and categorisation."""

from scripts.extractor import categorize_problem, is_problem


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


def test_rejects_show_hn_announcements():
    assert is_problem(
        "Show HN: Running 104GB Qwen3 on 48GB Mac at ~12 tok/s",
        "I built slotstream, a way to run a 125B parameter model on a low-memory mac.",
    ) is False


def test_rejects_launch_hn_announcements():
    assert is_problem(
        "Launch HN: Almanac (YC S26) - AI that knows your company",
        "Hi HN, I'm one of three founders of Almanac. We started our journey building an agent.",
    ) is False


def test_rejects_product_launch_phrasing():
    assert is_problem("Introducing Widget 2.0", "We built a faster tool for teams") is False


def test_accepts_someone_describing_trouble():
    assert is_problem(
        "How do I stop my backup script from silently failing?",
        "It doesn't work when the disk is full and I can't figure out why.",
    ) is True


def test_requires_a_strong_signal_not_just_generic_nouns():
    """'tool' and 'app' alone are not evidence of a problem."""
    assert is_problem("A new tool for developers", "This app is for building things") is False
