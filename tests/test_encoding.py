"""Tests that every file the pipeline writes uses an explicit UTF-8 encoding.

Scraped Reddit/HN titles routinely contain non-ASCII text. Relying on the
platform default encoding crashes with UnicodeEncodeError on runners whose
locale is not UTF-8, after files have been partially written.

`PYTHONWARNDEFAULTENCODING=1` makes CPython emit an EncodingWarning for any
open()/read_text()/write_text() call that omits `encoding`; promoting that
warning to an error turns the latent bug into a test failure.
"""

import subprocess
import sys
import textwrap

PROBLEM = {
    "title": "Cómo organizar archivos — 日本語 emoji 🎯",
    "description": "Los usuarios necesitan организовать their files ✨",
    "source": "r/programación",
    "category": "productivity",
    "url": "https://reddit.com/r/x",
    "reason": "Trending problem in productivity category",
}

SOLUTION = {
    "type": "file_organizer",
    "files": {"solution.py": "# ¡Hola! 🎉\nprint('café')\n", "requirements.txt": "requests>=2.31.0\n"},
}

EXERCISE = textwrap.dedent(
    """
    import json, pathlib, sys
    sys.path.insert(0, {repo!r})

    import main
    from scripts.doc_generator import generate_documentation

    problem = json.loads({problem!r})
    solution = json.loads({solution!r})
    out = pathlib.Path(sys.argv[1])

    main.HISTORY_FILE = out / "history.json"
    main.DATA_DIR = out
    main.save_history({{"problems": [{{"title": problem["title"]}}]}})
    assert main.load_history()["problems"][0]["title"] == problem["title"]

    solution_dir = out / "solution"
    solution_dir.mkdir(parents=True)
    main.write_solution_files(solution_dir, "2026-09-03", problem, solution)
    generate_documentation(solution_dir, problem, solution)

    for path in sorted(solution_dir.rglob("*")):
        if path.is_file():
            path.read_text(encoding="utf-8")
    print("OK")
    """
)


def _run_under_encoding_warnings(tmp_path, repo_root):
    script = EXERCISE.format(
        repo=str(repo_root),
        problem=__import__("json").dumps(PROBLEM),
        solution=__import__("json").dumps(SOLUTION),
    )
    return subprocess.run(
        [sys.executable, "-W", "error::EncodingWarning", "-c", script, str(tmp_path)],
        capture_output=True,
        text=True,
        env={"PYTHONWARNDEFAULTENCODING": "1", "PATH": "/usr/bin:/bin"},
        cwd=repo_root,
    )


def test_pipeline_writes_declare_utf8(tmp_path, pytestconfig):
    result = _run_under_encoding_warnings(tmp_path, pytestconfig.rootpath)

    assert "EncodingWarning" not in result.stderr, result.stderr
    assert result.returncode == 0, result.stderr


def test_non_ascii_problem_text_round_trips(tmp_path, pytestconfig):
    result = _run_under_encoding_warnings(tmp_path, pytestconfig.rootpath)

    assert result.returncode == 0, result.stderr
    problem_md = (tmp_path / "solution" / "PROBLEM.md").read_text(encoding="utf-8")
    assert "日本語" in problem_md
    assert "🎯" in problem_md
