"""Cleans HTML out of scraped text.

The Hacker News API returns HTML in `text`, so scraped descriptions arrived
containing entities like `&#x27;` and `<p>` tags. Those reached PROBLEM.md and
polluted extracted keywords (e.g. the keyword "x27").
"""

import html
import re

_TAG = re.compile(r"<[^>]+>")
_WHITESPACE = re.compile(r"\s+")


def clean_text(raw: str) -> str:
    """Unescape entities, strip tags and collapse whitespace."""
    if not raw:
        return ""
    text = _TAG.sub(" ", raw)
    text = html.unescape(text)
    return _WHITESPACE.sub(" ", text).strip()
