"""Tests for cleaning HTML out of scraped text."""

from scripts.textclean import clean_text


def test_unescapes_html_entities():
    assert clean_text("I&#x27;m building this") == "I'm building this"
    assert clean_text("memory&#x2F;RAM") == "memory/RAM"


def test_strips_html_tags():
    assert clean_text("first<p>second</p>") == "first second"


def test_collapses_whitespace():
    assert clean_text("too   many\n\n spaces") == "too many spaces"


def test_handles_empty_input():
    assert clean_text("") == ""
    assert clean_text(None) == ""
