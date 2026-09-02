"""Whole-word keyword matching.

Plain substring matching produced false positives that dominated both problem
categorisation and solution routing: "app" matched inside "bootstrappable" and
"ai" matched inside "failing", "email" and "explain".
"""

import re


def mentions(keyword: str, text: str) -> bool:
    """True when `keyword` appears in `text` as a whole word."""
    return re.search(rf"\b{re.escape(keyword)}\b", text) is not None
