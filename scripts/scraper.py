"""
Scrapes real-world problems from multiple free sources.
"""

import requests
import json
from datetime import datetime
from typing import List, Dict


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
                        "text": post_data.get("selftext", "")[:500],
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
                        "text": story.get("text", "")[:500] if story.get("text") else "",
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


def scrape_google_trends() -> List[Dict]:
    """Scrape trending topics from Google Trends."""
    all_posts = []

    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="en-US", tz=360)

        # Get trending searches
        trending = pytrends.trending_searches(pn="united_states")
        trends = trending[0].tolist()[:10] if not trending.empty else []

        for trend in trends:
            all_posts.append({
                "title": f"Trending: {trend}",
                "text": f"Currently trending topic on Google: {trend}",
                "source": "Google Trends",
                "url": f"https://www.google.com/search?q={trend.replace(' ', '+')}",
                "score": 100,
                "num_comments": 0,
                "created_at": datetime.now().isoformat()
            })

    except Exception as e:
        print(f"   Warning: Google Trends unavailable: {e}")
        # Fallback: use trending IT topics
        fallback_trends = [
            "AI automation tools",
            "remote work productivity",
            "cybersecurity threats 2026",
            "sustainable tech solutions",
            "digital health apps"
        ]
        for trend in fallback_trends:
            all_posts.append({
                "title": f"Trending: {trend}",
                "text": f"Commonly discussed tech problem: {trend}",
                "source": "Google Trends (fallback)",
                "url": f"https://www.google.com/search?q={trend.replace(' ', '+')}",
                "score": 80,
                "num_comments": 0,
                "created_at": datetime.now().isoformat()
            })

    return all_posts


def scrape_twitter_nitter() -> List[Dict]:
    """Scrape trending topics from Nitter (Twitter mirror, no API needed)."""
    all_posts = []

    nitter_instances = [
        "https://nitter.privacydev.net",
        "https://nitter.poast.org",
        "https://nitter.woodland.cafe"
    ]

    # Tech-related hashtags/topics to monitor
    topics = [
        "programming", "webdev", "AI", "startup",
        "coding", "tech", "developer"
    ]

    for instance in nitter_instances:
        try:
            for topic in topics:
                url = f"{instance}/search?f=tweets&q={topic}"
                headers = {"User-Agent": "DailyProblemSolver/1.0"}
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(response.text, "html.parser")

                    tweets = soup.find_all("div", class_="timeline-item")[:5]

                    for tweet in tweets:
                        content_el = tweet.find("div", class_="tweet-content")
                        if content_el:
                            all_posts.append({
                                "title": content_el.text[:100],
                                "text": content_el.text[:500],
                                "source": f"Twitter/{topic}",
                                "url": f"{instance}/{topic}",
                                "score": 50,
                                "num_comments": 0,
                                "created_at": datetime.now().isoformat()
                            })
                    break  # If instance works, don't try others
        except Exception:
            continue

    # If all fail, provide fallback
    if not all_posts:
        fallback = [
            {"title": "AI replacing jobs concern", "text": "People worried about AI automation"},
            {"title": "Data privacy issues", "text": "New privacy regulations needed"},
            {"title": "Remote work challenges", "text": "Team collaboration difficulties"}
        ]
        for item in fallback:
            all_posts.append({
                **item,
                "source": "Twitter (fallback)",
                "url": "N/A",
                "score": 50,
                "num_comments": 0,
                "created_at": datetime.now().isoformat()
            })

    return all_posts


def scrape_all_sources() -> List[Dict]:
    """Scrape all sources and combine results."""
    print("   Scraping Reddit...")
    reddit = scrape_reddit()
    print(f"      Found {len(reddit)} posts")

    print("   Scraping Hacker News...")
    hn = scrape_hackernews()
    print(f"      Found {len(hn)} posts")

    print("   Scraping Google Trends...")
    trends = scrape_google_trends()
    print(f"      Found {len(trends)} trends")

    print("   Scraping Twitter (Nitter)...")
    twitter = scrape_twitter_nitter()
    print(f"      Found {len(twitter)} posts")

    all_content = reddit + hn + trends + twitter
    return all_content
