"""Tests for problem-to-template routing."""

import pytest

from scripts.smart_solver import SolutionGenerator, generate_solution


@pytest.fixture
def generator():
    return SolutionGenerator()


def problem(title, description="", keywords=()):
    return {"title": title, "description": description, "keywords": list(keywords)}


def test_returns_none_when_no_template_fits(generator):
    """A problem the library cannot serve must not silently get a JSON formatter."""
    assert generator.analyze_problem(
        problem(
            "Running 104GB Qwen3 on 48GB Mac at ~12 tok/s",
            "expert-offloading and ssd-streaming on a low-memory mac using MLX and Swift",
        )
    ) is None


def test_does_not_route_on_substring_false_positive(generator):
    """'context' contains 'text' but is not a text-summariser problem."""
    assert generator.analyze_problem(
        problem("AI that knows your company", "an agent that knows every context about our company")
    ) != "text_summarizer"


def test_routes_a_clear_match(generator):
    assert generator.analyze_problem(
        problem("Need to format and validate JSON", "my json file is unreadable, need to lint it")
    ) == "json_formatter"


def test_routes_by_strongest_fit_not_declaration_order(generator):
    assert generator.analyze_problem(
        problem("Track my budget", "log expenses, income and spending by category to a budget")
    ) == "budget_tracker"


def test_only_implemented_templates_are_registered(generator):
    """Stub types aliasing another template made metadata.json record a lie."""
    for name in generator.TEMPLATE_KEYWORDS:
        assert name in generator.solution_templates
    assert "git_helper" not in generator.solution_templates
    assert "pdf_converter" not in generator.solution_templates


def test_generate_solution_returns_none_when_nothing_fits():
    assert generate_solution(problem("Qwen3 on a Mac", "ssd streaming MLX Swift")) is None
