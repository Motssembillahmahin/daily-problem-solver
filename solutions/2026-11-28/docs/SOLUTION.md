# Solution Notes

Generated on 2026-11-28 by the Daily Problem Solver pipeline.

## Problem

**Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.String,java.lang.String>` from Array or what would be a correct type of my field**

I try to pass a json object to an api on a Spring boot. Before I was passing values using postman all worked fine. The format was as follows: { "shortname": "test2", "fullname": "testing2", "address": "addrtest2", "telephone": "380979379993", "website": "www.site2.com", "sociallinks": { "facebook": "fb2.com" }, "foundationyear": "1992" } Now in my Angular app I am passing json as follows: {"shortname":"test","fullname":"Bogdan Onyshenko","address":"Пр. Победы 72в","telephone":"0669829242","websi

| | |
|---|---|
| Source | Stack Overflow |
| Category | webdev |
| Original URL | https://stackoverflow.com/questions/70781588/cannot-deserialize-value-of-type-java-util-linkedhashmapjava-lang-string-java |
| Selected because | Trending problem in webdev category |

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
