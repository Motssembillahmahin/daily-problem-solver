# Solution Notes

Generated on 2026-10-25 by the Daily Problem Solver pipeline.

## Problem

**Deleting all files in a folder older than X days**

I'm trying to write a Python script to delete all files in a folder older than X days. This is what I have so far: import os, time, sys path = r"c:\users\%myusername%\downloads" now = time.time() for f in os.listdir(path): if os.stat(f).st_mtime < now - 7 * 86400: if os.path.isfile(f): os.remove(os.path.join(path, f)) When I run the script, I get: Error2 - system cannot find the file specified , and it gives the filename. What am I doing wrong?

| | |
|---|---|
| Source | Stack Overflow |
| Category | productivity |
| Original URL | https://stackoverflow.com/questions/12485666/deleting-all-files-in-a-folder-older-than-x-days |
| Selected because | Trending problem in productivity category |

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
