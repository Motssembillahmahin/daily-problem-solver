"""Tests for generated solution documentation.

The generated docs must describe the code that was actually shipped. They
previously claimed every solution was a Next.js + FastAPI + HuggingFace app,
and overwrote the accurate README that the solution template itself provided.
"""

import pytest

from scripts.doc_generator import generate_documentation
from scripts.smart_solver import SolutionGenerator

PROBLEM = {
    "title": "Track daily health metrics",
    "description": "People struggle to log water, steps and sleep in one place.",
    "source": "r/health",
    "category": "health",
    "url": "https://reddit.com/r/health/x",
    "reason": "Trending problem in health category",
}

SOLUTION = {
    "type": "health_tracker",
    "files": {
        "health_tracker.py": "print('hi')\n",
        "requirements.txt": "# No external dependencies",
        "README.md": "# Health Tracker\n\nReal usage docs from the template.\n",
    },
}

FICTION = ["Next.js", "FastAPI", "HuggingFace", "Mistral", "localhost:3000", "npm install"]

# The two templates that legitimately ship a FastAPI server. FICTION above is
# safe to apply verbatim against the single synthetic health_tracker fixture
# used elsewhere in this file (it never mentions FastAPI), but a test that
# walks every real template must not flag these two for the "FastAPI" entry -
# they really do ship it. Every other FICTION entry stays universally banned.
_FASTAPI_TEMPLATES = {"todo_api", "url_shortener"}


@pytest.fixture
def solution_dir(tmp_path):
    """A solution directory as main.py leaves it: template files already written."""
    for name, content in SOLUTION["files"].items():
        (tmp_path / name).write_text(content, encoding="utf-8")
    return tmp_path


def test_keeps_the_readme_the_solution_shipped(solution_dir):
    generate_documentation(solution_dir, PROBLEM, SOLUTION)

    assert (solution_dir / "README.md").read_text(encoding="utf-8") == SOLUTION["files"]["README.md"]


def test_writes_a_readme_when_the_solution_shipped_none(tmp_path):
    (tmp_path / "health_tracker.py").write_text("print('hi')\n", encoding="utf-8")
    solution = {**SOLUTION, "files": {"health_tracker.py": "print('hi')\n"}}

    generate_documentation(tmp_path, PROBLEM, solution)

    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "health_tracker.py" in readme
    assert PROBLEM["title"] in readme


def test_no_generated_doc_describes_a_stack_that_was_not_shipped(solution_dir):
    generate_documentation(solution_dir, PROBLEM, SOLUTION)

    for path in solution_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for claim in FICTION:
            assert claim not in text, f"{path.name} claims {claim!r}, which was never generated"


def test_solution_doc_lists_the_files_that_were_generated(solution_dir):
    generate_documentation(solution_dir, PROBLEM, SOLUTION)

    docs = list((solution_dir / "docs").glob("*.md"))
    assert docs, "expected at least one generated doc under docs/"
    combined = "\n".join(p.read_text(encoding="utf-8") for p in docs)
    assert "health_tracker.py" in combined
    assert "health_tracker" in combined


# How running each real template's entry point actually behaves, verified by
# reading scripts/smart_solver.py directly (see FIX 2 investigation notes):
# - "server": the entry point calls uvicorn.run(...) and blocks serving HTTP
#   on port 8000. There is no command list.
# - "usage_on_no_args": the entry point exits printing a usage/available-
#   commands message when required arguments are missing.
# - "runs_immediately": the entry point takes no required arguments and
#   performs its default action (or starts a blocking loop) immediately.
# This mapping is independent of scripts/doc_generator.py's own inference
# logic, so the test catches drift in either the templates or the generator.
EXPECTED_ENTRY_POINT_SHAPE = {
    "file_organizer": "usage_on_no_args",
    "url_shortener": "server",
    "todo_api": "server",
    "weather_app": "usage_on_no_args",
    "json_formatter": "usage_on_no_args",
    "csv_analyzer": "usage_on_no_args",
    "password_generator": "runs_immediately",
    "health_tracker": "usage_on_no_args",
    "note_taker": "usage_on_no_args",
    "pomodoro_timer": "runs_immediately",
    "budget_tracker": "usage_on_no_args",
    "bookmark_manager": "usage_on_no_args",
    "text_summarizer": "usage_on_no_args",
    "log_analyzer": "usage_on_no_args",
    "backup_tool": "usage_on_no_args",
    "email_validator": "usage_on_no_args",
}


def test_all_real_templates_get_truthful_docs(tmp_path):
    """Generate docs for every real template and check they describe reality.

    Covers the full 16-template library, not just the synthetic
    health_tracker payload used above, so it would have caught the FastAPI
    server templates being falsely told to print usage instructions.
    """
    generator = SolutionGenerator()
    assert set(generator.solution_templates) == set(EXPECTED_ENTRY_POINT_SHAPE), (
        "a template was added or removed without updating this test's shape mapping"
    )

    problem = {**PROBLEM}

    for name, make_files in generator.solution_templates.items():
        files = make_files(problem)
        solution = {"type": name, "files": files}

        solution_dir = tmp_path / name
        solution_dir.mkdir()
        for filename, content in files.items():
            (solution_dir / filename).write_text(content, encoding="utf-8")

        generate_documentation(solution_dir, problem, solution)

        docs = list(solution_dir.rglob("*.md"))
        assert docs, f"{name}: expected at least one generated doc"
        combined = "\n".join(p.read_text(encoding="utf-8") for p in docs)

        for claim in FICTION:
            if claim == "FastAPI" and name in _FASTAPI_TEMPLATES:
                continue  # these two templates genuinely ship FastAPI
            assert claim not in combined, f"{name}: doc claims {claim!r}, which this template never ships"

        if name not in _FASTAPI_TEMPLATES:
            assert "FastAPI" not in combined, f"{name}: doc claims FastAPI, but this template doesn't ship it"

        shape = EXPECTED_ENTRY_POINT_SHAPE[name]
        lowered = combined.lower()
        if shape == "server":
            assert "web server" in lowered, f"{name}: server template's doc never mentions a server"
            assert "usage instructions" not in lowered, (
                f"{name}: doc claims a command list for a blocking web server"
            )
        elif shape == "usage_on_no_args":
            assert "usage instructions" in lowered, (
                f"{name}: doc doesn't tell the reader how to see this template's commands"
            )
        else:  # runs_immediately
            assert "usage instructions" not in lowered, (
                f"{name}: doc falsely claims a command list; this template just runs"
            )
            assert "web server" not in lowered, f"{name}: doc falsely claims a web server"
