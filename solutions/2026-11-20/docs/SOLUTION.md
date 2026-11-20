# Solution Notes

Generated on 2026-11-20 by the Daily Problem Solver pipeline.

## Problem

**In Django REST Framework, why does raising serializers.ValidationError return errors in different format in validate() and create() methods?**

I am working on a DRF project and have a serializer like: class SomeSerializer(serializers.Serializer): number_field = serializers.IntegerField(required=False, min_value=25, max_value=100) In my settings.py, I have REST_FRAMEWORK = { other settings.... 'EXCEPTION_HANDLER': 'apps.utils.exceptions.custom_exception_handler', } In the custom exception handler, I handle ValidationError as follows: def custom_exception_handler(exc, context): # Call REST framework's default exception handler first resp

| | |
|---|---|
| Source | Stack Overflow |
| Category | general |
| Original URL | https://stackoverflow.com/questions/79271787/in-django-rest-framework-why-does-raising-serializers-validationerror-return-er |
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
