"""Tests for generated solution documentation.

The generated docs must describe the code that was actually shipped. They
previously claimed every solution was a Next.js + FastAPI + HuggingFace app,
and overwrote the accurate README that the solution template itself provided.
"""

import pytest

from scripts.doc_generator import generate_documentation

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
