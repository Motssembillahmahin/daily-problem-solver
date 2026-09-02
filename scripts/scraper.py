"""
Scrapes real-world problems from multiple free sources.
"""

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


def scrape_reddit() -> List[Dict]:
    """Scrape trending problems from Reddit (no API key needed)."""
    subreddits = [
        "technology", "programming", "webdev", "MachineLearning",
        "artificial", "datascience", "startups", "SideProject"
    ]

    all_posts = []

    for subreddit in subreddits:
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=10"
            headers = {"User-Agent": "DailyProblemSolver/1.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", {}).get("children", [])

                for post in posts:
                    post_data = post.get("data", {})
                    all_posts.append({
                        "title": post_data.get("title", ""),
                        "text": clean_text(post_data.get("selftext", ""))[:500],
                        "source": f"r/{subreddit}",
                        "url": f"https://reddit.com{post_data.get('permalink', '')}",
                        "score": post_data.get("score", 0),
                        "num_comments": post_data.get("num_comments", 0),
                        "created_at": datetime.fromtimestamp(
                            post_data.get("created_utc", 0)
                        ).isoformat()
                    })
        except Exception as e:
            print(f"   Warning: Failed to scrape r/{subreddit}: {e}")
            continue

    return all_posts


def scrape_hackernews() -> List[Dict]:
    """Scrape top stories from Hacker News (free API)."""
    all_posts = []

    try:
        # Get top story IDs
        response = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10
        )
        story_ids = response.json()[:30]  # Top 30

        for story_id in story_ids:
            try:
                story_response = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json",
                    timeout=5
                )
                story = story_response.json()

                if story and story.get("type") == "story":
                    all_posts.append({
                        "title": story.get("title", ""),
                        "text": clean_text(story.get("text", ""))[:500],
                        "source": "Hacker News",
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                        "score": story.get("score", 0),
                        "num_comments": story.get("descendants", 0),
                        "created_at": datetime.fromtimestamp(
                            story.get("time", 0)
                        ).isoformat()
                    })
            except Exception:
                continue

    except Exception as e:
        print(f"   Warning: Failed to scrape Hacker News: {e}")

    return all_posts


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


SOURCE_SCRAPERS: Dict[str, Callable[[], List[Dict]]] = {
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
