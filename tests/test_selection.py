"""Tests for choosing a problem the template library can actually serve."""

from main import select_solvable_problem

UNSOLVABLE = {
    "title": "Running 104GB Qwen3 on 48GB Mac",
    "description": "ssd streaming with MLX and Swift",
    "keywords": [],
}
SOLVABLE = {
    "title": "My JSON file is unreadable",
    "description": "need to format and validate this json",
    "keywords": ["json", "format"],
}


def test_skips_problems_no_template_fits():
    problem, solution = select_solvable_problem([UNSOLVABLE, SOLVABLE])

    assert problem["title"] == SOLVABLE["title"]
    assert solution["type"] == "json_formatter"


def test_returns_none_when_nothing_is_solvable():
    problem, solution = select_solvable_problem([UNSOLVABLE])

    assert problem is None
    assert solution is None


def test_returns_none_for_an_empty_list():
    assert select_solvable_problem([]) == (None, None)


def test_prefers_the_earliest_solvable_problem():
    """Problems arrive ranked by priority, so the first fit wins."""
    other = {"title": "Track my budget", "description": "log expenses and income",
             "keywords": ["budget"]}
    problem, _ = select_solvable_problem([other, SOLVABLE])

    assert problem["title"] == other["title"]
