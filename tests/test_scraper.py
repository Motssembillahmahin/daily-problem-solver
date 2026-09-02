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
