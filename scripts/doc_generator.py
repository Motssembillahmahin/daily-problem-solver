"""Auto-generates documentation for a generated solution.

Everything written here must be true of the files that were actually generated.
Solution templates ship their own README.md with real usage instructions; this
module never overwrites one, and only writes a README when the template omitted it.
"""

from pathlib import Path
from typing import Dict, List

from scripts.dates import today_str

DOC_FILENAME = "SOLUTION.md"

# Files that describe the solution rather than implement it.
_NON_CODE = {"README.md", "PROBLEM.md", "metadata.json", "requirements.txt"}


def generate_documentation(problem_dir: Path, problem: Dict, solution: Dict) -> None:
    """Write docs/SOLUTION.md, plus a README.md if the solution shipped none."""
    docs_dir = problem_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    files = solution.get("files", {})
    generate_solution_doc(docs_dir, problem, solution, files)

    readme = problem_dir / "README.md"
    if not readme.exists():
        generate_readme(readme, problem, solution, files)


def _entry_points(files: Dict[str, str]) -> List[str]:
    """The runnable scripts in the generated file set."""
    return sorted(name for name in files if name.endswith(".py") and name not in _NON_CODE)


def _has_dependencies(files: Dict[str, str]) -> bool:
    """True when requirements.txt lists at least one real package."""
    requirements = files.get("requirements.txt", "")
    return any(
        line.strip() and not line.strip().startswith("#")
        for line in requirements.splitlines()
    )


def _usage_block(files: Dict[str, str]) -> str:
    """Install/run instructions derived from the files that were generated."""
    entries = _entry_points(files)
    if not entries:
        return "No runnable script was generated for this problem.\n"

    lines = ["```bash"]
    if _has_dependencies(files):
        lines.append("pip install -r requirements.txt")
    for entry in entries:
        lines.append(f"python {entry}")
    lines.append("```")
    lines.append("")
    lines.append("Run a script with no arguments to see its available commands.")
    return "\n".join(lines) + "\n"


def _file_table(files: Dict[str, str]) -> str:
    rows = ["| File | Lines | Role |", "|------|-------|------|"]
    for name in sorted(files):
        line_count = len(files[name].splitlines())
        if name == "requirements.txt":
            role = "Python dependencies"
        elif name.endswith(".md"):
            role = "Usage documentation"
        elif name.endswith(".py"):
            role = "Solution source"
        else:
            role = "Supporting file"
        rows.append(f"| `{name}` | {line_count} | {role} |")
    return "\n".join(rows) + "\n"


def generate_solution_doc(
    docs_dir: Path, problem: Dict, solution: Dict, files: Dict[str, str]
) -> None:
    """Write docs/SOLUTION.md describing the problem and the generated code."""
    solution_type = solution.get("type", "unknown")

    content = f"""# Solution Notes

Generated on {today_str()} by the Daily Problem Solver pipeline.

## Problem

**{problem['title']}**

{problem.get('description', 'No description was captured.')}

| | |
|---|---|
| Source | {problem.get('source', 'N/A')} |
| Category | {problem.get('category', 'N/A')} |
| Original URL | {problem.get('url', 'N/A')} |
| Selected because | {problem.get('reason', 'N/A')} |

## What Was Generated

The pipeline classified this problem as **`{solution_type}`** and generated the
following files:

{_file_table(files)}
## Running It

{_usage_block(files)}
## How This Was Produced

1. **Scrape** - trending posts were collected from Reddit, Hacker News,
   Google Trends and a Twitter mirror.
2. **Extract** - posts containing problem indicators were scored by engagement
   and source weight.
3. **Deduplicate** - the problem was compared against `data/solved_problems.json`
   by title similarity and keyword overlap.
4. **Generate** - keywords in the problem were matched to the `{solution_type}`
   solution template, which produced the files listed above.

The generated code comes from a curated template selected by keyword matching,
not from a language model, so it addresses the problem's *category* rather than
its specific details. Review it before relying on it.
"""

    (docs_dir / DOC_FILENAME).write_text(content, encoding="utf-8")


def generate_readme(
    readme_path: Path, problem: Dict, solution: Dict, files: Dict[str, str]
) -> None:
    """Write a minimal accurate README for solutions whose template omitted one."""
    entries = _entry_points(files)
    summary = ", ".join(f"`{name}`" for name in entries) if entries else "no runnable script"

    content = f"""# {problem['title']}

> Auto-generated solution - {today_str()}

## Problem

{problem.get('description', 'No description was captured.')}

Source: {problem.get('source', 'N/A')}

## Contents

This solution ships {summary}.

{_file_table(files)}
## Usage

{_usage_block(files)}
See [`docs/{DOC_FILENAME}`](docs/{DOC_FILENAME}) for how this problem was selected
and how the code was produced.
"""

    readme_path.write_text(content, encoding="utf-8")
