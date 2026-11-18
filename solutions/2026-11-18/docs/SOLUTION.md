# Solution Notes

Generated on 2026-11-18 by the Daily Problem Solver pipeline.

## Problem

**How to solve `npm i package` and Vscode Default Formatter conflict**

When I run npm i a-package package.json contains a new line at the end, but when I format that file with Json Language Feature the default json formatter of vscode, that line is removed. This causes unnecessary conflicts within our environment because we also formatOnSave config. If the last developer saved the package.json, the line gets removed, if they installed a package, the line comes back. There is an issue related to it: https://github.com/npm/npm/issues/18545 but it isn't solved and npm

| | |
|---|---|
| Source | Stack Overflow |
| Category | general |
| Original URL | https://stackoverflow.com/questions/79975142/how-to-solve-npm-i-package-and-vscode-default-formatter-conflict |
| Selected because | Trending problem in general category |

## What Was Generated

The pipeline classified this problem as **`json_formatter`** and generated the
following files:

| File | Lines | Role |
|------|-------|------|
| `README.md` | 19 | Usage documentation |
| `format_json.py` | 64 | Solution source |
| `requirements.txt` | 1 | Python dependencies |

## Running It

```bash
python format_json.py
```

Run a script with no arguments to see its usage instructions.

## How This Was Produced

1. **Scrape** - problems and trending posts were collected from Stack Overflow,
   Ask HN, GitHub issues, Hacker News, Reddit and Google Trends.
2. **Extract** - posts containing problem indicators were scored by engagement
   and source weight.
3. **Deduplicate** - the problem was compared against `data/solved_problems.json`
   by title similarity and keyword overlap.
4. **Generate** - keywords in the problem were matched to the `json_formatter`
   solution template, which produced the files listed above.

The generated code comes from a curated template selected by keyword matching,
not from a language model, so it addresses the problem's *category* rather than
its specific details. Review it before relying on it.
