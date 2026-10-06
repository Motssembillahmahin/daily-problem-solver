# Solution Notes

Generated on 2026-10-07 by the Daily Problem Solver pipeline.

## Problem

**PyCharm option Jupyter: Notebook File Root (Set the root directory for Jupyter Notebooks) missing**

I'm looking for the PyCharm equivalent of this option in VS Code: Jupyter: Notebook File Root Set the root directory for Jupyter Notebooks I usually set it to ${workspaceFolder} instead of the folder in which the .ipynb is. I can't find how to do it in PyCharm. I am not allowed to use os.chdir() or %cd blabla

| | |
|---|---|
| Source | Stack Overflow |
| Category | general |
| Original URL | https://stackoverflow.com/questions/80007464/pycharm-option-jupyter-notebook-file-root-set-the-root-directory-for-jupyter-n |
| Selected because | Trending problem in general category |

## What Was Generated

The pipeline classified this problem as **`file_organizer`** and generated the
following files:

| File | Lines | Role |
|------|-------|------|
| `README.md` | 23 | Usage documentation |
| `requirements.txt` | 1 | Python dependencies |
| `solution.py` | 79 | Solution source |

## Running It

```bash
python solution.py
```

Run a script with no arguments to see its usage instructions.

## How This Was Produced

1. **Scrape** - problems and trending posts were collected from Stack Overflow,
   Ask HN, GitHub issues, Hacker News, Reddit and Google Trends.
2. **Extract** - posts containing problem indicators were scored by engagement
   and source weight.
3. **Deduplicate** - the problem was compared against `data/solved_problems.json`
   by title similarity and keyword overlap.
4. **Generate** - keywords in the problem were matched to the `file_organizer`
   solution template, which produced the files listed above.

The generated code comes from a curated template selected by keyword matching,
not from a language model, so it addresses the problem's *category* rather than
its specific details. Review it before relying on it.
