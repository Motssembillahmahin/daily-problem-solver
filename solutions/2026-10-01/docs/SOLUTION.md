# Solution Notes

Generated on 2026-10-01 by the Daily Problem Solver pipeline.

## Problem

**Sharepoint 2013 Add large files with rest api**

I am working on a project to copy files from one document library to another in Sharepoint 2013 via jquery and the rest api. My solution is based off of this http://techmikael.blogspot.com/2013/07/how-to-copy-files-between-sites-using.html The following code works for smaller file sizes (64mb or less). However I am getting an error when attempting to copy larger files (128Mb and up). The addFileBinary function returns to the error callback with "Not enough storage is available to complete this o

| | |
|---|---|
| Source | Stack Overflow |
| Category | webdev |
| Original URL | https://stackoverflow.com/questions/24438818/sharepoint-2013-add-large-files-with-rest-api |
| Selected because | Trending problem in webdev category |

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
