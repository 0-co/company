#!/usr/bin/env python3
"""
Signal Intelligence Demo
Watches HN and GitHub for relevant threads in real time.
Usage: python demo.py "topic to watch"

Live demo — shows what Signal does.
"""

import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone


def fetch_json(url: str) -> dict | list | None:
    """Fetch JSON from a URL."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Signal-Demo/1.0 (0coCEO; market intelligence tool)",
                "Accept": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"  [fetch error: {e}]", file=sys.stderr)
        return None


def search_hn(query: str, limit: int = 10) -> list[dict]:
    """Search Hacker News via Algolia API."""
    encoded = urllib.parse.quote(query)
    # Search last 30 days
    cutoff = int(time.time()) - 86400 * 30
    url = (
        f"https://hn.algolia.com/api/v1/search?query={encoded}"
        f"&hitsPerPage={limit}&tags=(story,ask_hn,show_hn)"
        f"&numericFilters=created_at_i>{cutoff}"
    )
    data = fetch_json(url)
    if not data or "hits" not in data:
        return []
    results = []
    for hit in data["hits"]:
        results.append({
            "source": "HN",
            "title": hit.get("title", ""),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "score": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "author": hit.get("author", ""),
            "created_at_i": hit.get("created_at_i", 0),
            "selftext": "",
        })
    return results


def search_github_issues(query: str, limit: int = 5) -> list[dict]:
    """Search GitHub Issues for relevant discussions."""
    encoded = urllib.parse.quote(f"{query} type:issue state:open sort:reactions-desc")
    url = f"https://api.github.com/search/issues?q={encoded}&per_page={limit}"
    data = fetch_json(url)
    if not data or "items" not in data:
        return []
    results = []
    for item in data.get("items", []):
        repo = item.get("repository_url", "").replace("https://api.github.com/repos/", "")
        results.append({
            "source": f"GitHub ({repo})",
            "title": item.get("title", ""),
            "url": item.get("html_url", ""),
            "score": item.get("reactions", {}).get("+1", 0) + item.get("reactions", {}).get("total_count", 0),
            "comments": item.get("comments", 0),
            "author": item.get("user", {}).get("login", ""),
            "created_at_i": 0,
            "selftext": (item.get("body") or "")[:200],
        })
    return results


def search_hn_comments(query: str, limit: int = 5) -> list[dict]:
    """Search HN comments for relevant discussions."""
    encoded = urllib.parse.quote(query)
    cutoff = int(time.time()) - 86400 * 14
    url = (
        f"https://hn.algolia.com/api/v1/search?query={encoded}"
        f"&hitsPerPage={limit}&tags=comment"
        f"&numericFilters=created_at_i>{cutoff}"
    )
    data = fetch_json(url)
    if not data or "hits" not in data:
        return []
    results = []
    for hit in data["hits"]:
        story_id = hit.get("story_id") or hit.get("objectID")
        results.append({
            "source": "HN (comment)",
            "title": hit.get("story_title", hit.get("comment_text", "")[:80] + "..."),
            "url": f"https://news.ycombinator.com/item?id={story_id}",
            "score": hit.get("points", 0),
            "comments": 0,
            "author": hit.get("author", ""),
            "created_at_i": hit.get("created_at_i", 0),
            "selftext": (hit.get("comment_text") or "")[:200],
        })
    return results


def score_relevance(item: dict, keywords: list[str]) -> float:
    """Relevance score based on keyword overlap + recency + engagement."""
    text = (item.get("title", "") + " " + item.get("selftext", "")).lower()
    hits = sum(1 for kw in keywords if kw.lower() in text)

    # Recency boost (within last 48h)
    recency_boost = 0.0
    ts = item.get("created_at_i", 0)
    if ts:
        age_hours = (time.time() - ts) / 3600
        if age_hours < 48:
            recency_boost = 0.25
        elif age_hours < 168:  # 1 week
            recency_boost = 0.1

    # Engagement boost
    engagement = min(0.3, (item.get("score", 0) + item.get("comments", 0)) / 200)

    # Keyword match ratio
    kw_score = hits / max(len(keywords), 1)

    return kw_score + recency_boost + engagement


def relative_time(ts: float) -> str:
    """Human-readable relative time."""
    if not ts:
        return "recently"
    age = time.time() - ts
    if age < 3600:
        return f"{int(age/60)}m ago"
    elif age < 86400:
        return f"{int(age/3600)}h ago"
    else:
        return f"{int(age/86400)}d ago"


def format_result(item: dict, relevance: float) -> str:
    """Format a result for terminal display."""
    source = item["source"]
    title = item["title"][:90]
    url = item["url"]
    score = item.get("score", 0)
    comments = item.get("comments", 0)
    age = relative_time(item.get("created_at_i", 0))
    rel_score = min(1.0, relevance)  # cap at 100%
    rel_pct = int(rel_score * 100)
    rel_bar = "█" * int(rel_score * 8) + "░" * (8 - int(rel_score * 8))
    return (
        f"\n  \033[36m[{source}]\033[0m {title}\n"
        f"  \033[90m{url}\033[0m\n"
        f"  \033[90m{age} · ↑{score} · {comments} comments · relevance {rel_bar} {rel_pct}%\033[0m"
    )


def run_demo(query: str, limit: int = 8):
    """Run a demo search and display results."""
    keywords = [w for w in query.lower().split() if len(w) > 3]
    if not keywords:
        keywords = query.lower().split()

    print(f"\n\033[1m{'='*60}\033[0m")
    print(f"  \033[1mSignal Intelligence Demo\033[0m")
    print(f"  Watching: \033[33m'{query}'\033[0m")
    print(f"  Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"\033[1m{'='*60}\033[0m")

    all_results = []

    print(f"\n\033[90m[1/3] Searching Hacker News stories...\033[0m")
    hn_results = search_hn(query, limit=limit)
    print(f"  Found {len(hn_results)} results")
    all_results.extend(hn_results)

    print(f"\n\033[90m[2/3] Searching HN comments...\033[0m")
    hn_comment_results = search_hn_comments(query, limit=5)
    print(f"  Found {len(hn_comment_results)} results")
    all_results.extend(hn_comment_results)

    print(f"\n\033[90m[3/3] Searching GitHub Issues...\033[0m")
    gh_results = search_github_issues(query, limit=5)
    print(f"  Found {len(gh_results)} results")
    all_results.extend(gh_results)

    # Score and sort
    for item in all_results:
        item["_relevance"] = score_relevance(item, keywords)
    all_results.sort(key=lambda x: x["_relevance"], reverse=True)

    # Display top results
    print(f"\n\033[1mTop signals (ranked by relevance):\033[0m")
    shown = 0
    for item in all_results:
        if item["_relevance"] > 0.02:
            print(format_result(item, item["_relevance"]))
            shown += 1
            if shown >= 5:
                break

    if shown == 0:
        print("  No highly relevant results found. Try broader keywords.")

    print(f"\n\033[1m{'='*60}\033[0m")
    print(f"  Searched: HN stories + HN comments + GitHub Issues")
    print(f"  Signal Pro would also watch: Reddit, Discord servers, Twitter/X")
    print(f"  \033[36mSign up at: 0-co.github.io/signal\033[0m")
    print(f"\033[1m{'='*60}\033[0m\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python demo.py \"topic to watch\"")
        print("Example: python demo.py \"dependency management automation\"")
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    run_demo(query)
