# Solution Notes

Generated on 2026-09-12 by the Daily Problem Solver pipeline.

## Problem

**Why does my Py-Shiny web app download an empty file?**

I'm working on a web app that searches a database and returns the relevant information as CSV files in a Zip archive (company security policy prevents me from returning the information as tabs in an XLSX file). When I run the get_data() function on its own, I get a CSV file with the expected information in it. But when I use the app, I get a CSV file that is empty except for the header row. from shiny import render, ui, reactive from shiny.express import input from pandas import DataFrame import

| | |
|---|---|
| Source | Stack Overflow |
| Category | data |
| Original URL | https://stackoverflow.com/questions/80002466/why-does-my-py-shiny-web-app-download-an-empty-file |
| Selected because | Trending problem in data category |

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
