"""Tests for whole-word keyword matching."""

from scripts.matching import mentions


def test_matches_a_whole_word():
    assert mentions("app", "i need an app for this") is True


def test_does_not_match_inside_a_longer_word():
    assert mentions("app", "bootstrappable builds") is False
    assert mentions("ai", "the deploy keeps failing") is False


def test_matches_multi_word_keyword():
    assert mentions("machine learning", "a machine learning model") is True


def test_matches_keyword_containing_punctuation():
    assert mentions("ci/cd", "our ci/cd setup broke") is True


def test_does_not_match_absent_keyword():
    assert mentions("weather", "a budget tracker") is False
