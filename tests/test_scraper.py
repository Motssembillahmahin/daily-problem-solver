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


SO_RESPONSE = {
    "items": [
        {
            "title": "How to stop my backup script from failing silently?",
            "body": "It &#x27;doesn&#x27;t work&#x27; when the disk is full.<p>Help?</p>",
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


def test_stackoverflow_populates_text_from_withbody_field(monkeypatch):
    """The `withbody` filter returns the question body (HTML) in `body`.
    text must be populated and stripped of HTML tags/entities."""
    response = {
        "items": [
            {
                "title": "Why does my CSV import silently drop rows?",
                "body": "<p>It &quot;just skips&quot; rows with a trailing comma.</p>",
                "link": "https://stackoverflow.com/q/2",
                "score": 5,
                "answer_count": 1,
                "creation_date": 1756800000,
                "tags": ["python", "csv"],
            }
        ]
    }
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: response)
    monkeypatch.setattr(scraper, "STACKOVERFLOW_TAGS", ["python"])

    text = scraper.scrape_stackoverflow()[0]["text"]

    assert text != ""
    assert "<p>" not in text
    assert "&quot;" not in text
    assert "just skips" in text


def test_stackoverflow_returns_empty_when_fetch_fails(monkeypatch):
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: None)
    monkeypatch.setattr(scraper, "STACKOVERFLOW_TAGS", ["python"])

    assert scraper.scrape_stackoverflow() == []


SO_RESPONSE_NO_BODY_MARKDOWN = {
    "items": [
        {
            "title": "How to stop my backup script from failing silently?",
            "link": "https://stackoverflow.com/q/1",
            "score": 12,
            "answer_count": 2,
            "creation_date": 1756800000,
            "tags": ["python", "bash"],
        }
    ]
}


def test_stackoverflow_falls_back_to_title_when_api_omits_body(monkeypatch):
    """The live, unfiltered Stack Exchange API omits body_markdown entirely.
    text must fall back to empty while title stays populated."""
    monkeypatch.setattr(scraper, "fetch_json", lambda *a, **k: SO_RESPONSE_NO_BODY_MARKDOWN)
    monkeypatch.setattr(scraper, "STACKOVERFLOW_TAGS", ["python"])

    item = scraper.scrape_stackoverflow()[0]

    assert item["text"] == ""
    assert item["title"] == "How to stop my backup script from failing silently?"


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
