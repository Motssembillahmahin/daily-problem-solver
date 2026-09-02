# Relevant Solutions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the daily pipeline ship a solution that is actually related to a real problem, or honestly ship nothing, by fixing problem selection, template routing, and source quality.

**Architecture:** Keep the existing free/deterministic template library (no LLM). Three changes in sequence: (1) feed the pipeline genuine problem statements from sources whose items *are* problems (Stack Overflow, Ask HN, GitHub issues) instead of HN front-page announcements and fabricated filler; (2) route a problem to a template by a *scored fit* that can return "no fit" rather than a silent `json_formatter` default; (3) select the highest-priority problem that has a fitting template, instead of the highest-priority problem full stop.

**Tech Stack:** Python 3.10+, `requests`, `beautifulsoup4`, `scikit-learn`, `pytest`. No new dependencies.

**Spec:** This document, section "Background" below. Derived from the root-cause investigation in the 2026-09-02 session and two product decisions by the repo owner: keep templates (no LLM), and widen sources until a real problem is found.

## Background (the spec)

Investigation of `solutions/2026-08-31` and `solutions/2026-09-01` established a four-link causal chain for "the solution has no code / just restates the problem":

1. **The input is not problems.** 28 of 29 HN top-stories are link-only; the HN API returns `text` only for self-posts. `is_problem` needs 2 keyword hits, which short link-only titles rarely reach, so the only items that pass are HN self-posts (Show HN / Launch HN product *announcements*) and the fabricated fallback items in `scrape_google_trends` / `scrape_twitter_nitter`, which are hardcoded to contain "problem" and "tool" and therefore always score exactly 2.
2. **Routing fires on substring false positives.** `SolutionGenerator.analyze_problem` matches keywords with bare `in`. "Launch HN: Almanac" routed to `text_summarizer` because its description contains "con**text**" (verified whole-word = NO).
3. **A silent catch-all hides failure.** `smart_solver.py:104` returns `json_formatter` whenever nothing matches, and 9 of 25 registered types are stubs that alias `_json_formatter`/`_csv_analyzer`, so `metadata.json` records a type that was never generated.
4. **Templates ignore the problem.** `json_formatter` output is byte-identical for "Running Qwen on a Mac" and "about gardening"; the problem text appears nowhere in the generated code.

Link 4 is accepted as a known limitation of the template approach: a template addresses a problem *category*, not the specific problem. This plan makes the category match honest and the input real, so a shipped template is at least genuinely relevant — and ships nothing rather than something irrelevant.

Verified source probes (2026-09-02, unauthenticated, HTTP 200):

| Source | Endpoint | Why |
|---|---|---|
| Stack Overflow | `api.stackexchange.com/2.3/questions` | Items *are* problem statements; pre-tagged; has score/answer counts |
| Ask HN | `hn.algolia.com/api/v1/search?tags=ask_hn` | Real questions with self-text |
| GitHub issues | `api.github.com/search/issues?q=label:bug` | Real reported defects; `GITHUB_TOKEN` already in CI |
| Reddit | `www.reddit.com/*.json` | Times out locally and 403s from CI — must be non-fatal, never fabricated |

## Global Constraints

- Python 3.10+ (`X | None` union syntax is already used in `scripts/dates.py`).
- No new third-party dependencies. `requirements.txt` must continue to match real imports.
- No LLM/API-key dependency on the critical path.
- No fabricated, synthetic, or placeholder problem data anywhere in `scripts/scraper.py`. A source that fails returns `[]` and logs why.
- All file writes pass `encoding="utf-8"`.
- Every task ends green: `python -m pytest -q` from the repo root.
- Network is never contacted from tests. HTTP is injected or monkeypatched.

---

### Task 1: Shared whole-word keyword matching

`scripts/extractor.py` already has a private `_mentions`. `smart_solver` needs the same
logic, so it moves to its own module rather than being duplicated.

**Files:**
- Create: `scripts/matching.py`
- Modify: `scripts/extractor.py` (delete `_mentions`, import it instead)
- Test: `tests/test_matching.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `mentions(keyword: str, text: str) -> bool` — True when `keyword` occurs in
  `text` as a whole word. Caller lowercases `text` first. Handles multi-word keywords
  ("machine learning") and punctuation ("ci/cd").

- [ ] **Step 1: Write the failing test**

```python
# tests/test_matching.py
"""Tests for whole-word keyword matching."""

from scripts.matching import mentions


def test_matches_a_whole_word():
    assert mentions("app", "i need an app for this") is True


def test_does_not_match_inside_a_longer_word():
    assert mentions("app", "bootstrappable builds") is False
    assert mentions("ai", "the deploy keeps failing") is False


def test_matches_multi_word_keyword():
    assert mentions("machine learning", "a machine learning model") is True


def test_matches_keyword_containing_punctuation():
    assert mentions("ci/cd", "our ci/cd setup broke") is True


def test_does_not_match_absent_keyword():
    assert mentions("weather", "a budget tracker") is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_matching.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.matching'`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/matching.py
"""Whole-word keyword matching.

Plain substring matching produced false positives that dominated both problem
categorisation and solution routing: "app" matched inside "bootstrappable" and
"ai" matched inside "failing", "email" and "explain".
"""

import re


def mentions(keyword: str, text: str) -> bool:
    """True when `keyword` appears in `text` as a whole word."""
    return re.search(rf"\b{re.escape(keyword)}\b", text) is not None
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_matching.py -q`
Expected: PASS (5 passed)

- [ ] **Step 5: Point extractor at the shared helper**

In `scripts/extractor.py`, delete the `_mentions` function and add
`from scripts.matching import mentions` at the top, then replace the call inside
`categorize_problem`:

```python
    scores = {
        category: sum(1 for kw in keywords if mentions(kw, combined))
        for category, keywords in CATEGORIES.items()
    }
```

- [ ] **Step 6: Run the full suite**

Run: `python -m pytest -q`
Expected: PASS — the existing `tests/test_extractor.py` still passes unchanged.

- [ ] **Step 7: Commit**

```bash
git add scripts/matching.py scripts/extractor.py tests/test_matching.py
git commit -m "refactor: extract whole-word keyword matching into scripts/matching"
```

---

### Task 2: Clean HTML out of scraped text

The HN API returns HTML: production data contains `I&#x27;m`, `memory&#x2F;RAM` and
`<p>` tags. This leaks into `PROBLEM.md`, into the generated docs, and into keywords
(`x27` is a recorded keyword in `data/solved_problems.json`).

**Files:**
- Create: `scripts/textclean.py`
- Test: `tests/test_textclean.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `clean_text(raw: str) -> str` — unescapes HTML entities, strips tags,
  collapses whitespace. Returns `""` for falsy input.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_textclean.py
"""Tests for cleaning HTML out of scraped text."""

from scripts.textclean import clean_text


def test_unescapes_html_entities():
    assert clean_text("I&#x27;m building this") == "I'm building this"
    assert clean_text("memory&#x2F;RAM") == "memory/RAM"


def test_strips_html_tags():
    assert clean_text("first<p>second</p>") == "first second"


def test_collapses_whitespace():
    assert clean_text("too   many\n\n spaces") == "too many spaces"


def test_handles_empty_input():
    assert clean_text("") == ""
    assert clean_text(None) == ""
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_textclean.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'scripts.textclean'`

- [ ] **Step 3: Write minimal implementation**

```python
# scripts/textclean.py
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_textclean.py -q`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/textclean.py tests/test_textclean.py
git commit -m "feat: add clean_text for HTML in scraped content"
```

---

### Task 3: Reject announcements in `is_problem`

`is_problem` currently accepts anything with 2 hits from a list where "tool", "app",
"build", "create" and "idea" are indicators, so product announcements pass. It must
require at least one *strong* signal of someone having trouble, and explicitly reject
announcement phrasing.

**Files:**
- Modify: `scripts/extractor.py` (replace `PROBLEM_INDICATORS` and `is_problem`)
- Test: `tests/test_extractor.py` (add cases)

**Interfaces:**
- Consumes: `mentions()` from Task 1.
- Produces: `is_problem(title: str, text: str) -> bool` — unchanged signature.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_extractor.py`:

```python
from scripts.extractor import is_problem


def test_rejects_show_hn_announcements():
    assert is_problem(
        "Show HN: Running 104GB Qwen3 on 48GB Mac at ~12 tok/s",
        "I built slotstream, a way to run a 125B parameter model on a low-memory mac.",
    ) is False


def test_rejects_launch_hn_announcements():
    assert is_problem(
        "Launch HN: Almanac (YC S26) - AI that knows your company",
        "Hi HN, I'm one of three founders of Almanac. We started our journey building an agent.",
    ) is False


def test_rejects_product_launch_phrasing():
    assert is_problem("Introducing Widget 2.0", "We built a faster tool for teams") is False


def test_accepts_someone_describing_trouble():
    assert is_problem(
        "How do I stop my backup script from silently failing?",
        "It doesn't work when the disk is full and I can't figure out why.",
    ) is True


def test_requires_a_strong_signal_not_just_generic_nouns():
    """'tool' and 'app' alone are not evidence of a problem."""
    assert is_problem("A new tool for developers", "This app is for building things") is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_extractor.py -q`
Expected: FAIL — the three `is False` announcement cases return `True`.

- [ ] **Step 3: Write minimal implementation**

Replace `PROBLEM_INDICATORS` and `is_problem` in `scripts/extractor.py`:

```python
# Phrases that indicate someone is actually stuck or frustrated. At least one
# of these must be present for content to count as a problem.
STRONG_INDICATORS = [
    "how do i", "how to", "how can i", "problem", "issue", "struggle",
    "struggling", "difficulty", "need help", "looking for", "error", "fails",
    "failing", "failed", "can't", "cannot", "doesn't work", "not working",
    "broken", "frustrated", "annoying", "pain", "stuck", "confused",
    "any advice", "any suggestions", "what's the best way", "is there a way",
    "unable to", "keeps crashing", "why does", "why is",
]

# Supporting signals. These corroborate a strong indicator but never stand alone.
WEAK_INDICATORS = [
    "improve", "automate", "simplify", "better", "alternative", "recommend",
    "suggestion", "advice", "tool", "app", "software", "workaround", "fix",
    "solution", "challenge",
]

# Product-announcement phrasing. Announcements describe something that was
# built, not a problem to solve, so they are rejected outright.
ANNOUNCEMENT_MARKERS = [
    "show hn", "launch hn", "introducing", "announcing", "we built",
    "i built", "we've built", "i've built", "we made", "i made",
    "we launched", "just launched", "now available", "release notes",
    "changelog", "yc s2", "yc w2",
]


def is_announcement(title: str, text: str) -> bool:
    """True when content announces a product rather than describing a problem."""
    combined = (title + " " + text).lower()
    return any(marker in combined for marker in ANNOUNCEMENT_MARKERS)


def is_problem(title: str, text: str) -> bool:
    """Check if content describes a problem someone is actually having."""
    if is_announcement(title, text):
        return False

    combined = (title + " " + text).lower()
    if not any(indicator in combined for indicator in STRONG_INDICATORS):
        return False

    weak_hits = sum(1 for indicator in WEAK_INDICATORS if mentions(indicator, combined))
    strong_hits = sum(1 for indicator in STRONG_INDICATORS if indicator in combined)
    return strong_hits + weak_hits >= 2
```

Note: `STRONG_INDICATORS` and `ANNOUNCEMENT_MARKERS` are matched with plain `in`
because they are multi-word phrases where substring collision is not a risk.
`WEAK_INDICATORS` are single words and use `mentions()`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_extractor.py -q`
Expected: PASS

- [ ] **Step 5: Check against recorded production data**

Run:

```bash
python -c "
import json
from scripts.extractor import is_problem
h = json.load(open('data/solved_problems.json', encoding='utf-8'))
for p in h['problems']:
    print(f'{is_problem(p[\"title\"], \"\")!s:<6} {p[\"title\"][:60]}')
"
```

Expected: the two `Show HN` / `Trending:` style titles now report `False`.

- [ ] **Step 6: Run the full suite and commit**

```bash
python -m pytest -q
git add scripts/extractor.py tests/test_extractor.py
git commit -m "fix: reject product announcements and require a strong problem signal"
```

---

### Task 4: Score template fit and allow "no fit"

Replaces the 25-branch ordering-dependent `if any(...)` cascade and its silent
`json_formatter` default with a scored table that can return `None`. The 9 stub types
are removed from the registry so a type that was never implemented can no longer be
recorded in `metadata.json`.

**Files:**
- Modify: `scripts/smart_solver.py` (`SolutionGenerator.__init__`, `analyze_problem`,
  `generate_solution`; delete the 9 stub methods at lines ~1157-1188)
- Test: `tests/test_smart_solver.py`

**Interfaces:**
- Consumes: `mentions()` from Task 1.
- Produces:
  - `SolutionGenerator.TEMPLATE_KEYWORDS: dict[str, list[str]]`
  - `SolutionGenerator.analyze_problem(problem: Dict) -> str | None` — returns a
    template name, or `None` when no template scores at or above `MIN_FIT`.
  - `SolutionGenerator.generate_solution(problem: Dict) -> Dict | None` — returns
    `None` when `analyze_problem` returns `None`.
  - `generate_solution(problem: Dict) -> Dict | None` (module-level entry point).
  - `SolutionGenerator.MIN_FIT: int = 2`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_smart_solver.py
"""Tests for problem-to-template routing."""

import pytest

from scripts.smart_solver import SolutionGenerator, generate_solution


@pytest.fixture
def generator():
    return SolutionGenerator()


def problem(title, description="", keywords=()):
    return {"title": title, "description": description, "keywords": list(keywords)}


def test_returns_none_when_no_template_fits(generator):
    """A problem the library cannot serve must not silently get a JSON formatter."""
    assert generator.analyze_problem(
        problem(
            "Running 104GB Qwen3 on 48GB Mac at ~12 tok/s",
            "expert-offloading and ssd-streaming on a low-memory mac using MLX and Swift",
        )
    ) is None


def test_does_not_route_on_substring_false_positive(generator):
    """'context' contains 'text' but is not a text-summariser problem."""
    assert generator.analyze_problem(
        problem("AI that knows your company", "an agent that knows every context about our company")
    ) != "text_summarizer"


def test_routes_a_clear_match(generator):
    assert generator.analyze_problem(
        problem("Need to format and validate JSON", "my json file is unreadable, need to lint it")
    ) == "json_formatter"


def test_routes_by_strongest_fit_not_declaration_order(generator):
    assert generator.analyze_problem(
        problem("Track my budget", "log expenses, income and spending by category to a budget")
    ) == "budget_tracker"


def test_only_implemented_templates_are_registered(generator):
    """Stub types aliasing another template made metadata.json record a lie."""
    for name in generator.TEMPLATE_KEYWORDS:
        assert name in generator.solution_templates
    assert "git_helper" not in generator.solution_templates
    assert "pdf_converter" not in generator.solution_templates


def test_generate_solution_returns_none_when_nothing_fits():
    assert generate_solution(problem("Qwen3 on a Mac", "ssd streaming MLX Swift")) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_smart_solver.py -q`
Expected: FAIL — `analyze_problem` returns `"json_formatter"` instead of `None`, and
`TEMPLATE_KEYWORDS` does not exist.

- [ ] **Step 3: Write minimal implementation**

In `scripts/smart_solver.py`, add the import and replace `__init__`'s registry,
`analyze_problem`, and `generate_solution`:

```python
from scripts.matching import mentions


class SolutionGenerator:
    """Generates working solutions from a library of templates."""

    # A problem must score at least this many keyword hits for a template to be
    # considered a fit. Below it, the library has nothing relevant and the
    # pipeline should move on rather than ship an unrelated tool.
    MIN_FIT = 2

    # Only templates that are actually implemented appear here.
    TEMPLATE_KEYWORDS = {
        "health_tracker": ["health", "fitness", "workout", "exercise", "calorie",
                            "steps", "sleep", "weight", "medical", "wellness"],
        "file_organizer": ["file", "files", "organize", "organise", "sort",
                            "folder", "directory", "rename", "duplicate"],
        "url_shortener": ["url", "shorten", "shortener", "link", "redirect", "slug"],
        "todo_api": ["todo", "task", "tasks", "checklist", "kanban", "backlog"],
        "weather_app": ["weather", "forecast", "temperature", "rain", "climate"],
        "json_formatter": ["json", "format", "beautify", "pretty print", "lint",
                            "minify", "validate", "unreadable"],
        "csv_analyzer": ["csv", "spreadsheet", "excel", "column", "rows",
                          "tabular", "dataset"],
        "password_generator": ["password", "passphrase", "credential", "random",
                                "secure", "generator"],
        "note_taker": ["note", "notes", "journal", "diary", "scratchpad"],
        "pomodoro_timer": ["pomodoro", "timer", "focus", "concentrate",
                            "distraction", "break"],
        "budget_tracker": ["budget", "expense", "expenses", "spending", "money",
                            "income", "finance", "cost"],
        "bookmark_manager": ["bookmark", "bookmarks", "read later", "saved links",
                              "tabs", "favourites", "favorites"],
        "text_summarizer": ["summarize", "summarise", "summary", "tldr",
                             "article", "long text", "condense"],
        "log_analyzer": ["log", "logs", "logfile", "stacktrace", "traceback",
                          "error rate", "monitor"],
        "backup_tool": ["backup", "backups", "restore", "snapshot", "archive",
                         "sync"],
        "email_validator": ["email", "e-mail", "mailbox", "smtp", "bounce",
                             "verify address"],
    }

    def __init__(self):
        self.solution_templates = {
            "file_organizer": self._file_organizer,
            "url_shortener": self._url_shortener,
            "todo_api": self._todo_api,
            "weather_app": self._weather_app,
            "json_formatter": self._json_formatter,
            "csv_analyzer": self._csv_analyzer,
            "password_generator": self._password_generator,
            "health_tracker": self._health_tracker,
            "note_taker": self._note_taker,
            "pomodoro_timer": self._pomodoro_timer,
            "budget_tracker": self._budget_tracker,
            "bookmark_manager": self._bookmark_manager,
            "text_summarizer": self._text_summarizer,
            "log_analyzer": self._log_analyzer,
            "backup_tool": self._backup_tool,
            "email_validator": self._email_validator,
        }

    def score_templates(self, problem: Dict) -> Dict[str, int]:
        """Score every template by how many of its keywords the problem mentions."""
        combined = " ".join([
            problem.get("title", ""),
            problem.get("description", ""),
            " ".join(problem.get("keywords", [])),
        ]).lower()

        return {
            name: sum(1 for kw in keywords if mentions(kw, combined))
            for name, keywords in self.TEMPLATE_KEYWORDS.items()
        }

    def analyze_problem(self, problem: Dict) -> str | None:
        """Return the best-fitting template, or None when the library has none."""
        scores = self.score_templates(problem)
        best = max(scores, key=scores.get)
        return best if scores[best] >= self.MIN_FIT else None

    def generate_solution(self, problem: Dict) -> Dict[str, Any] | None:
        """Generate a solution, or None when no template fits the problem."""
        solution_type = self.analyze_problem(problem)
        if solution_type is None:
            print(f"   No template fits: {problem.get('title', '')[:60]}")
            return None

        print(f"   Analyzed as: {solution_type}")
        files = self.solution_templates[solution_type](problem)

        return {
            "type": solution_type,
            "files": files,
            "description": f"Working solution for: {problem['title']}",
        }
```

Then delete these 9 now-unregistered stub methods from `scripts/smart_solver.py`
(around lines 1157-1188): `_pdf_converter`, `_markdown_editor`, `_regex_helper`,
`_git_helper`, `_api_tester`, `_image_compressor`, `_json_to_csv`, `_code_formatter`,
`_env_manager`.

Finally update the module-level entry point at the bottom of the file:

```python
def generate_solution(problem: Dict) -> Dict[str, Any] | None:
    """Main entry point. Returns None when no template fits."""
    generator = SolutionGenerator()
    return generator.generate_solution(problem)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_smart_solver.py -q`
Expected: PASS (6 passed)

- [ ] **Step 5: Verify against the two production failures**

Run:

```bash
python -c "
import json
from scripts.smart_solver import SolutionGenerator
g = SolutionGenerator()
for d in ['solutions/2026-08-31', 'solutions/2026-09-01']:
    p = json.load(open(f'{d}/metadata.json', encoding='utf-8'))['problem']
    print(f'{d} -> {g.analyze_problem(p)}')
"
```

Expected: both print `None` (previously `text_summarizer` and `json_formatter`).

- [ ] **Step 6: Run the full suite and commit**

```bash
python -m pytest -q
git add scripts/smart_solver.py tests/test_smart_solver.py
git commit -m "fix: score template fit and return None when nothing matches"
```

---

### Task 5: Select the best problem that has a fitting template

`main.py` takes `unique_problems[0]` and generates unconditionally. With Task 4 it must
walk the ranked list and pick the first problem the library can actually serve.

**Files:**
- Modify: `main.py` (add `select_solvable_problem`, rewrite the selection block of `run`)
- Test: `tests/test_selection.py`

**Interfaces:**
- Consumes: `generate_solution()` from Task 4 (returns `Dict | None`).
- Produces: `select_solvable_problem(problems: List[Dict]) -> tuple[Dict, Dict] | tuple[None, None]`
  — returns `(problem, solution)` for the first problem with a fitting template,
  or `(None, None)`.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_selection.py
"""Tests for choosing a problem the template library can actually serve."""

from main import select_solvable_problem

UNSOLVABLE = {
    "title": "Running 104GB Qwen3 on 48GB Mac",
    "description": "ssd streaming with MLX and Swift",
    "keywords": [],
}
SOLVABLE = {
    "title": "My JSON file is unreadable",
    "description": "need to format and validate this json",
    "keywords": ["json", "format"],
}


def test_skips_problems_no_template_fits():
    problem, solution = select_solvable_problem([UNSOLVABLE, SOLVABLE])

    assert problem["title"] == SOLVABLE["title"]
    assert solution["type"] == "json_formatter"


def test_returns_none_when_nothing_is_solvable():
    problem, solution = select_solvable_problem([UNSOLVABLE])

    assert problem is None
    assert solution is None


def test_returns_none_for_an_empty_list():
    assert select_solvable_problem([]) == (None, None)


def test_prefers_the_earliest_solvable_problem():
    """Problems arrive ranked by priority, so the first fit wins."""
    other = {"title": "Track my budget", "description": "log expenses and income",
             "keywords": ["budget"]}
    problem, _ = select_solvable_problem([other, SOLVABLE])

    assert problem["title"] == other["title"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_selection.py -q`
Expected: FAIL — `ImportError: cannot import name 'select_solvable_problem' from 'main'`

- [ ] **Step 3: Write minimal implementation**

Add to `main.py`:

```python
def select_solvable_problem(problems):
    """Return the first (problem, solution) the template library can serve."""
    for problem in problems:
        solution = generate_solution(problem)
        if solution is not None:
            return problem, solution
    return None, None
```

Then replace the selection and generation block in `run()`:

```python
    # Step 4: Pick the best problem the template library can actually solve
    print("\n[4/5] Generating solution...")
    selected_problem, solution = select_solvable_problem(unique_problems)

    if solution is None:
        print(f"\nNo template fits any of today's {len(unique_problems)} problems. Skipping.")
        return False

    print(f"   Selected: {selected_problem['title']}")
    print(f"   Solution type: {solution['type']}")
```

Delete the now-dead lines that set `selected_problem = unique_problems[0]`, print
`Selected:`, and call `generate_solution(selected_problem)`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_selection.py -q`
Expected: PASS (4 passed)

- [ ] **Step 5: Run the full suite and commit**

```bash
python -m pytest -q
git add main.py tests/test_selection.py
git commit -m "feat: select the highest-priority problem a template can serve"
```

---

### Task 6: Shared HTTP helper, and delete the fabricated fallbacks

`scrape_google_trends` and `scrape_twitter_nitter` invent problems when they fail, and
those synthetic items are hardcoded to pass `is_problem`. They must return `[]`. This
task also centralises HTTP so the new sources in Tasks 7-9 get retries and a shared
session, and so tests can inject a fake fetcher instead of touching the network.

**Files:**
- Modify: `scripts/scraper.py` (add `fetch_json`, delete both fallback blocks,
  add `scrape_all_sources` per-source reporting)
- Test: `tests/test_scraper.py`

**Interfaces:**
- Consumes: `clean_text()` from Task 2.
- Produces:
  - `fetch_json(url: str, headers: Dict | None = None, timeout: int = 15) -> Any | None`
    — returns parsed JSON, or `None` on any failure (logged, never raised).
  - `SOURCE_SCRAPERS: dict[str, Callable[[], List[Dict]]]` — name to scraper, used by
    `scrape_all_sources` so each source's yield is reported.

- [ ] **Step 1: Write the failing test**

```python
# tests/test_scraper.py
"""Tests for source scraping. No test in this file contacts the network."""

import scripts.scraper as scraper


def test_fetch_json_returns_none_on_error(monkeypatch):
    def boom(*args, **kwargs):
        raise scraper.requests.Timeout("read timed out")

    monkeypatch.setattr(scraper._SESSION, "get", boom)

    assert scraper.fetch_json("https://example.com/x") is None


def test_google_trends_returns_empty_when_unavailable(monkeypatch):
    """A failing source must yield nothing, never fabricated problems."""
    monkeypatch.setattr(scraper, "_trending_searches", lambda: (_ for _ in ()).throw(RuntimeError("no")))

    assert scraper.scrape_google_trends() == []


def test_no_fabricated_problem_text_remains_in_the_module():
    source = open(scraper.__file__, encoding="utf-8").read()
    for invented in ["Commonly discussed tech problem",
                     "AI replacing jobs concern",
                     "cybersecurity threats 2026",
                     "fallback"]:
        assert invented not in source, f"scraper still fabricates: {invented!r}"


def test_scrape_all_sources_survives_one_source_failing(monkeypatch):
    monkeypatch.setattr(scraper, "SOURCE_SCRAPERS", {
        "good": lambda: [{"title": "a real problem", "text": "", "source": "good",
                          "url": "", "score": 1, "num_comments": 0, "created_at": ""}],
        "bad": lambda: (_ for _ in ()).throw(RuntimeError("down")),
    })

    items = scraper.scrape_all_sources()

    assert len(items) == 1
    assert items[0]["source"] == "good"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: FAIL — `_SESSION`, `fetch_json`, `_trending_searches` and `SOURCE_SCRAPERS`
do not exist, and the fabricated strings are still in the module.

- [ ] **Step 3: Write minimal implementation**

At the top of `scripts/scraper.py`:

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List

from scripts.textclean import clean_text

USER_AGENT = "DailyProblemSolver/1.0 (github.com/Motssembillahmahin/daily-problem-solver)"

_SESSION = requests.Session()
_SESSION.mount("https://", HTTPAdapter(max_retries=Retry(
    total=2, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504)
)))


def fetch_json(url: str, headers: Dict | None = None, timeout: int = 15) -> Any | None:
    """GET `url` and parse JSON. Returns None on any failure, and says why."""
    merged = {"User-Agent": USER_AGENT}
    merged.update(headers or {})
    try:
        response = _SESSION.get(url, headers=merged, timeout=timeout)
        if response.status_code != 200:
            print(f"   Warning: {url} returned HTTP {response.status_code}")
            return None
        return response.json()
    except Exception as e:
        print(f"   Warning: {url} failed: {type(e).__name__}: {e}")
        return None
```

Extract the pytrends call so it can be monkeypatched, and delete the fabricated
fallback list from `scrape_google_trends`:

```python
def _trending_searches() -> List[str]:
    """Fetch Google Trends trending searches. Raises on failure."""
    from pytrends.request import TrendReq

    pytrends = TrendReq(hl="en-US", tz=360)
    trending = pytrends.trending_searches(pn="united_states")
    return trending[0].tolist()[:10] if not trending.empty else []


def scrape_google_trends() -> List[Dict]:
    """Trending topics from Google Trends. Returns [] when unavailable."""
    try:
        trends = _trending_searches()
    except Exception as e:
        print(f"   Warning: Google Trends unavailable: {type(e).__name__}: {e}")
        return []

    return [{
        "title": f"Trending: {trend}",
        "text": "",
        "source": "Google Trends",
        "url": f"https://www.google.com/search?q={trend.replace(' ', '+')}",
        "score": 100,
        "num_comments": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    } for trend in trends]
```

Delete `scrape_twitter_nitter` entirely — it has three dead instances, a 21-request
worst case, and its only reliable output was the fabricated fallback.

Rewrite `scrape_all_sources` to iterate a registry and report each source:

```python
SOURCE_SCRAPERS: Dict[str, Callable[[], List[Dict]]] = {
    "Stack Overflow": scrape_stackoverflow,
    "Ask HN": scrape_ask_hn,
    "GitHub issues": scrape_github_issues,
    "Hacker News": scrape_hackernews,
    "Reddit": scrape_reddit,
    "Google Trends": scrape_google_trends,
}


def scrape_all_sources() -> List[Dict]:
    """Scrape every source. A failing source yields nothing and does not stop the run."""
    all_content = []
    for name, scrape in SOURCE_SCRAPERS.items():
        try:
            items = scrape()
        except Exception as e:
            print(f"   {name}: FAILED {type(e).__name__}: {e}")
            continue
        print(f"   {name}: {len(items)} items")
        all_content.extend(items)

    if not all_content:
        print("   Warning: every source returned nothing - check network and source APIs")
    return all_content
```

Note: `SOURCE_SCRAPERS` references the three functions added in Tasks 7-9. Define it
*after* those functions exist; until then include only the existing scrapers and add
each new one in its own task.

Also apply `clean_text` to HN and Reddit text in their existing scrapers:

```python
                        "text": clean_text(post_data.get("selftext", ""))[:500],
```

```python
                        "text": clean_text(story.get("text", ""))[:500],
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: PASS (4 passed)

- [ ] **Step 5: Run the full suite and commit**

```bash
python -m pytest -q
git add scripts/scraper.py tests/test_scraper.py
git commit -m "fix: remove fabricated fallback problems, add shared HTTP with retries"
```

---

### Task 7: Add Stack Overflow as a source

Verified 2026-09-02: `HTTP 200`, no API key, and every item is a literal problem
statement ("How to get unix-specific python modules working easily on Windows?").
This is the highest-value source for this pipeline.

**Files:**
- Modify: `scripts/scraper.py` (add `scrape_stackoverflow`, register in `SOURCE_SCRAPERS`)
- Test: `tests/test_scraper.py` (add cases)

**Interfaces:**
- Consumes: `fetch_json()` from Task 6, `clean_text()` from Task 2.
- Produces: `scrape_stackoverflow() -> List[Dict]` with the standard item shape:
  `title`, `text`, `source`, `url`, `score`, `num_comments`, `created_at`.
- Produces: `STACKOVERFLOW_TAGS: List[str]`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_scraper.py`:

```python
SO_RESPONSE = {
    "items": [
        {
            "title": "How to stop my backup script from failing silently?",
            "body_markdown": "It &#x27;doesn&#x27;t work&#x27; when the disk is full.<p>Help?</p>",
            "link": "https://stackoverflow.com/q/1",
            "score": 12,
            "answer_count": 2,
            "creation_date": 1756800000,
            "tags": ["python", "bash"],
        }
    ]
}


def test_stackoverflow_maps_questions_to_problems(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: SO_RESPONSE)
    monkeypatch.setattr(scraper, "STACKOVERFLOW_TAGS", ["python"])

    items = scraper.scrape_stackoverflow()

    assert len(items) == 1
    item = items[0]
    assert item["title"] == "How to stop my backup script from failing silently?"
    assert item["source"] == "Stack Overflow"
    assert item["url"] == "https://stackoverflow.com/q/1"
    assert item["score"] == 12
    assert item["num_comments"] == 2


def test_stackoverflow_cleans_html_from_body(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: SO_RESPONSE)
    monkeypatch.setattr(scraper, "STACKOVERFLOW_TAGS", ["python"])

    text = scraper.scrape_stackoverflow()[0]["text"]

    assert "&#x27;" not in text
    assert "<p>" not in text
    assert "doesn't work" in text


def test_stackoverflow_returns_empty_when_fetch_fails(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: None)
    monkeypatch.setattr(scraper, "STACKOVERFLOW_TAGS", ["python"])

    assert scraper.scrape_stackoverflow() == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: FAIL — `AttributeError: module 'scripts.scraper' has no attribute 'scrape_stackoverflow'`

- [ ] **Step 3: Write minimal implementation**

```python
# Tags chosen to overlap the template library (files, csv, json, logs, email).
STACKOVERFLOW_TAGS = ["python", "json", "csv", "logging", "file", "automation"]

STACKOVERFLOW_URL = (
    "https://api.stackexchange.com/2.3/questions"
    "?order=desc&sort=activity&pagesize=20&site=stackoverflow"
    "&filter=!nNPvSNVZBv&tagged={tag}"
)


def scrape_stackoverflow() -> List[Dict]:
    """Scrape recent Stack Overflow questions. Every question is a stated problem."""
    all_posts = []

    for tag in STACKOVERFLOW_TAGS:
        data = fetch_json(STACKOVERFLOW_URL.format(tag=tag))
        if not data:
            continue

        for item in data.get("items", []):
            all_posts.append({
                "title": clean_text(item.get("title", "")),
                "text": clean_text(item.get("body_markdown", ""))[:500],
                "source": "Stack Overflow",
                "url": item.get("link", ""),
                "score": item.get("score", 0),
                "num_comments": item.get("answer_count", 0),
                "created_at": datetime.fromtimestamp(
                    item.get("creation_date", 0), timezone.utc
                ).isoformat(),
            })

    return all_posts
```

The `filter=!nNPvSNVZBv` parameter asks the Stack Exchange API to include
`body_markdown`, which the default filter omits.

Register it in `SOURCE_SCRAPERS` (defined in Task 6) as `"Stack Overflow": scrape_stackoverflow`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: PASS

- [ ] **Step 5: Verify against the live API once**

Run:

```bash
python -c "
from scripts.scraper import scrape_stackoverflow
from scripts.extractor import extract_problems
items = scrape_stackoverflow()
problems = extract_problems(items)
print(f'scraped {len(items)} -> {len(problems)} passed is_problem')
for p in problems[:5]: print('  ', p['title'][:70])
"
```

Expected: a non-zero count of real problems. If the `filter` parameter returns no
`body_markdown`, drop `&filter=!nNPvSNVZBv` and rely on `title` alone.

- [ ] **Step 6: Run the full suite and commit**

```bash
python -m pytest -q
git add scripts/scraper.py tests/test_scraper.py
git commit -m "feat: scrape Stack Overflow questions as problem sources"
```

---

### Task 8: Add Ask HN as a source

Verified 2026-09-02: `HTTP 200` from the HN Algolia search API, no key. Ask HN posts
carry self-text and are genuine questions, unlike HN front-page link posts.

**Files:**
- Modify: `scripts/scraper.py` (add `scrape_ask_hn`, register in `SOURCE_SCRAPERS`)
- Test: `tests/test_scraper.py` (add cases)

**Interfaces:**
- Consumes: `fetch_json()` from Task 6, `clean_text()` from Task 2.
- Produces: `scrape_ask_hn() -> List[Dict]` with the standard item shape.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_scraper.py`:

```python
ASK_HN_RESPONSE = {
    "hits": [
        {
            "objectID": "42",
            "title": "Ask HN: How do I stop my deploys from failing at random?",
            "story_text": "We&#x27;ve tried everything and it&#x27;s still broken.",
            "points": 88,
            "num_comments": 31,
            "created_at_i": 1756800000,
        }
    ]
}


def test_ask_hn_maps_hits_to_problems(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: ASK_HN_RESPONSE)

    items = scraper.scrape_ask_hn()

    assert len(items) == 1
    item = items[0]
    assert item["title"].startswith("Ask HN: How do I stop my deploys")
    assert item["source"] == "Ask HN"
    assert item["url"] == "https://news.ycombinator.com/item?id=42"
    assert item["score"] == 88
    assert item["num_comments"] == 31
    assert "&#x27;" not in item["text"]


def test_ask_hn_returns_empty_when_fetch_fails(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: None)

    assert scraper.scrape_ask_hn() == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: FAIL — no attribute `scrape_ask_hn`

- [ ] **Step 3: Write minimal implementation**

```python
ASK_HN_URL = "https://hn.algolia.com/api/v1/search?tags=ask_hn&hitsPerPage=30"


def scrape_ask_hn() -> List[Dict]:
    """Scrape Ask HN posts, which are questions rather than announcements."""
    data = fetch_json(ASK_HN_URL)
    if not data:
        return []

    all_posts = []
    for hit in data.get("hits", []):
        all_posts.append({
            "title": clean_text(hit.get("title", "")),
            "text": clean_text(hit.get("story_text", ""))[:500],
            "source": "Ask HN",
            "url": f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}",
            "score": hit.get("points") or 0,
            "num_comments": hit.get("num_comments") or 0,
            "created_at": datetime.fromtimestamp(
                hit.get("created_at_i", 0), timezone.utc
            ).isoformat(),
        })

    return all_posts
```

Register it in `SOURCE_SCRAPERS` as `"Ask HN": scrape_ask_hn`.

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: PASS

- [ ] **Step 5: Run the full suite and commit**

```bash
python -m pytest -q
git add scripts/scraper.py tests/test_scraper.py
git commit -m "feat: scrape Ask HN as a problem source"
```

---

### Task 9: Add GitHub issues as a source

Verified 2026-09-02: `HTTP 200` unauthenticated. Issues labelled `bug` are reported
defects — real problems. `GITHUB_TOKEN` is already available in CI and raises the
search rate limit, so it is used when present.

**Files:**
- Modify: `scripts/scraper.py` (add `scrape_github_issues`, register in `SOURCE_SCRAPERS`)
- Modify: `.github/workflows/daily.yml` (pass `GITHUB_TOKEN` to the solver step)
- Test: `tests/test_scraper.py` (add cases)

**Interfaces:**
- Consumes: `fetch_json()` from Task 6, `clean_text()` from Task 2.
- Produces: `scrape_github_issues() -> List[Dict]` with the standard item shape.

- [ ] **Step 1: Write the failing test**

Append to `tests/test_scraper.py`:

```python
GITHUB_RESPONSE = {
    "items": [
        {
            "title": "Config file has no effect when installed via package manager",
            "body": "It doesn&#x27;t work and I can&#x27;t figure out why.<p>Steps:</p>",
            "html_url": "https://github.com/o/r/issues/7",
            "comments": 4,
            "reactions": {"total_count": 9},
            "created_at": "2026-08-30T10:00:00Z",
        }
    ]
}


def test_github_issues_map_to_problems(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: GITHUB_RESPONSE)

    items = scraper.scrape_github_issues()

    assert len(items) == 1
    item = items[0]
    assert item["source"] == "GitHub Issues"
    assert item["url"] == "https://github.com/o/r/issues/7"
    assert item["num_comments"] == 4
    assert item["score"] == 9
    assert "&#x27;" not in item["text"]


def test_github_issues_send_token_when_available(monkeypatch):
    seen = {}

    def fake_fetch(url, headers=None, **kwargs):
        seen["headers"] = headers or {}
        return {"items": []}

    monkeypatch.setattr(scraper, "fetch_json", fake_fetch)
    monkeypatch.setenv("GITHUB_TOKEN", "secret-token")

    scraper.scrape_github_issues()

    assert seen["headers"].get("Authorization") == "Bearer secret-token"


def test_github_issues_work_without_a_token(monkeypatch):
    seen = {}

    def fake_fetch(url, headers=None, **kwargs):
        seen["headers"] = headers or {}
        return {"items": []}

    monkeypatch.setattr(scraper, "fetch_json", fake_fetch)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)

    scraper.scrape_github_issues()

    assert "Authorization" not in seen["headers"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: FAIL — no attribute `scrape_github_issues`

- [ ] **Step 3: Write minimal implementation**

Add `import os` to the imports, then:

```python
GITHUB_ISSUES_URL = (
    "https://api.github.com/search/issues"
    "?q=label:bug+state:open+is:issue+comments:%3E2&sort=created&order=desc&per_page=30"
)


def scrape_github_issues() -> List[Dict]:
    """Scrape recently reported bugs. Issues labelled `bug` are stated problems."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    data = fetch_json(GITHUB_ISSUES_URL, headers=headers)
    if not data:
        return []

    all_posts = []
    for item in data.get("items", []):
        all_posts.append({
            "title": clean_text(item.get("title", "")),
            "text": clean_text(item.get("body", "") or "")[:500],
            "source": "GitHub Issues",
            "url": item.get("html_url", ""),
            "score": (item.get("reactions") or {}).get("total_count", 0),
            "num_comments": item.get("comments", 0),
            "created_at": item.get("created_at", ""),
        })

    return all_posts
```

Register it in `SOURCE_SCRAPERS` as `"GitHub issues": scrape_github_issues`.

In `.github/workflows/daily.yml`, add the token to the solver step's existing `env`
block so the search API gets the higher rate limit:

```yaml
      - name: Run Daily Solver
        env:
          PYTHONPATH: ${{ github.workspace }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: python main.py
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_scraper.py -q`
Expected: PASS

- [ ] **Step 5: Add the new source weights to prioritisation**

In `scripts/extractor.py`, `calculate_priority` weights sources by name. Add the new
ones so real problem sources outrank trend noise:

```python
    source_weights = {
        "Stack Overflow": 20,
        "Ask HN": 18,
        "GitHub Issues": 16,
        "Hacker News": 12,
        "r/technology": 10,
        "r/programming": 10,
        "r/MachineLearning": 10,
        "Google Trends": 5,
    }
```

- [ ] **Step 6: Run the full suite and commit**

```bash
python -m pytest -q
git add scripts/scraper.py scripts/extractor.py .github/workflows/daily.yml tests/test_scraper.py
git commit -m "feat: scrape GitHub bug reports as a problem source"
```

---

### Task 10: End-to-end verification against live sources

No new code. This task proves the pipeline now selects a real problem and ships a
relevant template, using the real network once.

**Files:**
- Modify: `README.md` (correct the source list and the "no solution" behaviour)

- [ ] **Step 1: Run the real pipeline end to end**

Run: `python main.py`

Expected output: per-source item counts, a non-zero `passed is_problem` count driven by
Stack Overflow / Ask HN / GitHub, a selected problem that reads like an actual problem,
and a solution type whose keywords visibly relate to it. Or a clean
"No template fits any of today's N problems. Skipping." with exit code 0.

- [ ] **Step 2: Inspect what was produced**

Run:

```bash
DATE=$(TZ='Asia/Dhaka' date +%F)
cat "solutions/$DATE/PROBLEM.md"
cat "solutions/$DATE/docs/SOLUTION.md"
ls "solutions/$DATE"
```

Expected: `PROBLEM.md` describes a real problem with no HTML entities; the shipped
`.py` file is topically related to it.

- [ ] **Step 3: Confirm the announcement filter holds on live data**

Run:

```bash
python -c "
from scripts.scraper import scrape_ask_hn
from scripts.extractor import is_problem, is_announcement
items = scrape_ask_hn()
rejected = [i for i in items if is_announcement(i['title'], i['text'])]
accepted = [i for i in items if is_problem(i['title'], i['text'])]
print(f'{len(items)} Ask HN items: {len(accepted)} accepted, {len(rejected)} announcements rejected')
for i in accepted[:5]: print('  OK  ', i['title'][:66])
for i in rejected[:5]: print('  REJ ', i['title'][:66])
"
```

Expected: accepted items read as problems; rejected items read as announcements.

- [ ] **Step 4: Update the README**

In `README.md`, replace the `Scraping Sources` table with the real set and note the
skip behaviour:

```markdown
### Scraping Sources

| Source | What It Captures |
|--------|------------------|
| Stack Overflow | Tagged questions - every item is a stated problem |
| Ask HN | Questions from HN with self-text |
| GitHub Issues | Reported bugs with discussion |
| Hacker News | Top stories (link posts rarely qualify as problems) |
| Reddit | Subreddit discussions (unreliable from CI; non-fatal) |
| Google Trends | Trending searches (low weight) |

Product announcements ("Show HN", "Launch HN", "Introducing") are rejected: they
describe something that was built, not a problem to solve. If no scraped problem
matches any template in the library, the run ships nothing rather than an unrelated
tool.
```

- [ ] **Step 5: Commit**

```bash
git add README.md
git commit -m "docs: document real sources and the no-fit skip behaviour"
```

---

## Self-Review

**Spec coverage:**

| Spec item | Task |
|---|---|
| Link 1 - input is not problems (announcements pass) | Task 3 |
| Link 1 - fabricated fallbacks always pass | Task 6 |
| Link 1 - widen sources until something qualifies | Tasks 7, 8, 9 |
| Link 2 - substring false positives in routing | Tasks 1, 4 |
| Link 3 - silent `json_formatter` default | Tasks 4, 5 |
| Link 3 - 9 stub types make metadata lie | Task 4 |
| Link 4 - templates ignore the problem | Accepted limitation; documented in Task 10 |
| HTML entities in scraped text | Tasks 2, 6, 7, 8, 9 |
| Reddit unreliable, must be non-fatal | Task 6 |

**Placeholder scan:** No TBD/TODO. Every code step carries the actual code. Task 10
is verification-only and its steps are exact commands with stated expected output.

**Type consistency:** `mentions()` (Task 1) is used in Tasks 3 and 4.
`clean_text()` (Task 2) is used in Tasks 6-9. `fetch_json()` (Task 6) is used in
Tasks 7-9. `analyze_problem` returns `str | None` (Task 4) and `select_solvable_problem`
(Task 5) depends on `generate_solution` returning `Dict | None` — consistent.
`SOURCE_SCRAPERS` is introduced in Task 6 and appended to in Tasks 7-9; Task 6 notes
it must initially contain only existing scrapers.

**Known ordering constraint:** Tasks 1-2 have no dependencies. Task 3 needs Task 1.
Task 4 needs Task 1. Task 5 needs Task 4. Task 6 needs Task 2. Tasks 7-9 need Task 6.
Task 10 needs everything.
