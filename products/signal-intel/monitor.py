#!/usr/bin/env python3
"""
Signal Intelligence — Core Monitoring Service

Watches HN and GitHub Issues for relevant threads based on configured topics.
Runs as a scheduled service (cron or loop), posts new finds to Discord.

Usage:
  python monitor.py run          # Single scan pass
  python monitor.py run --loop   # Continuous (every 30 min)
  python monitor.py add-topic "your product name" --keywords "keyword1,keyword2"
  python monitor.py status       # Show configured topics and recent finds
"""

import sys
import json
import time
import os
import urllib.request
import urllib.parse
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
STATE_FILE = BASE_DIR / ".state.json"

# Load webhook from .env file if present (takes precedence over config.json webhook)
_env_file = BASE_DIR / ".env"
if _env_file.exists():
    for _line in _env_file.read_text().splitlines():
        if _line.startswith("SIGNAL_INTEL_DISCORD_WEBHOOK="):
            os.environ.setdefault("SIGNAL_DISCORD_WEBHOOK", _line.split("=", 1)[1].strip())

DISCORD_WEBHOOK = os.environ.get("SIGNAL_DISCORD_WEBHOOK", "")


# ────────────────────────────────────────────────────────────
# Config management
# ────────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "topics": [],
    "scan_interval_minutes": 30,
    "min_relevance_score": 0.3,
    "max_age_days": 7,
    "discord_webhook": "",
}

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return DEFAULT_CONFIG.copy()

def save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"seen": {}, "last_scan": None}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ────────────────────────────────────────────────────────────
# Fetching
# ────────────────────────────────────────────────────────────

def fetch_json(url: str) -> dict | list | None:
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Signal-Monitor/1.0 (0coCEO market intelligence; github.com/0-co/autostartup)",
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def search_hn(query: str, max_age_days: int = 7, limit: int = 10) -> list[dict]:
    encoded = urllib.parse.quote(query)
    cutoff = int(time.time()) - 86400 * max_age_days
    url = (
        f"https://hn.algolia.com/api/v1/search?query={encoded}"
        f"&hitsPerPage={limit}&tags=(story,ask_hn,show_hn)"
        f"&numericFilters=created_at_i>{cutoff}"
    )
    data = fetch_json(url)
    if not data:
        return []
    results = []
    for hit in data.get("hits", []):
        results.append({
            "id": f"hn:{hit.get('objectID')}",
            "source": "HN",
            "title": hit.get("title", ""),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "hn_url": f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "score": hit.get("points", 0),
            "comments": hit.get("num_comments", 0),
            "author": hit.get("author", ""),
            "created_at": hit.get("created_at_i", 0),
            "text": hit.get("story_text", "") or "",
        })
    return results


def search_github_issues(query: str, limit: int = 5) -> list[dict]:
    # Narrow to recently updated issues
    encoded = urllib.parse.quote(f"{query} type:issue state:open")
    url = f"https://api.github.com/search/issues?q={encoded}&sort=updated&order=desc&per_page={limit}"
    data = fetch_json(url)
    if not data:
        return []
    results = []
    for item in data.get("items", []):
        repo = item.get("repository_url", "").replace("https://api.github.com/repos/", "")
        results.append({
            "id": f"gh:{item.get('id')}",
            "source": "GitHub",
            "title": item.get("title", ""),
            "url": item.get("html_url", ""),
            "hn_url": item.get("html_url", ""),
            "score": item.get("reactions", {}).get("total_count", 0),
            "comments": item.get("comments", 0),
            "author": item.get("user", {}).get("login", ""),
            "created_at": 0,
            "text": (item.get("body") or "")[:500],
            "repo": repo,
        })
    return results


def fetch_rss(url: str) -> list[dict]:
    """Fetch and parse a Reddit Atom RSS feed into normalized items."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; SignalBot/1.0)",
            "Accept": "application/rss+xml, application/atom+xml",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return []

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    items = []
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        title = title_el.text.strip() if title_el is not None and title_el.text else ""
        # Reddit RSS uses <link href="..."> without rel="alternate"
        link_el = entry.find("atom:link[@rel='alternate']", ns) or entry.find("atom:link", ns)
        link = link_el.get("href", "") if link_el is not None else ""
        id_el = entry.find("atom:id", ns)
        entry_id = id_el.text.strip() if id_el is not None and id_el.text else link
        author_el = entry.find("atom:author/atom:name", ns)
        author = author_el.text.strip() if author_el is not None and author_el.text else ""
        updated_el = entry.find("atom:updated", ns)
        ts = 0
        if updated_el is not None and updated_el.text:
            try:
                dt = datetime.fromisoformat(updated_el.text.replace("Z", "+00:00"))
                ts = int(dt.timestamp())
            except ValueError:
                pass
        content_el = entry.find("atom:content", ns)
        text = ""
        if content_el is not None and content_el.text:
            # Strip HTML tags crudely
            import re as _re
            text = _re.sub(r"<[^>]+>", " ", content_el.text)[:500]
        # Derive subreddit from URL
        sub_match = link.split("/r/")
        subreddit = sub_match[1].split("/")[0] if len(sub_match) > 1 else ""
        items.append({
            "id": f"reddit:{hashlib.md5(entry_id.encode()).hexdigest()[:12]}",
            "source": "Reddit",
            "title": title,
            "url": link,
            "hn_url": link,
            "score": 0,  # RSS doesn't expose vote counts
            "comments": 0,
            "author": author,
            "created_at": ts,
            "text": text,
            "subreddit": subreddit,
        })
    return items


def search_reddit(query: str, subreddits: list[str] | None = None, limit: int = 10) -> list[dict]:
    """Search Reddit via RSS feeds (no auth required)."""
    encoded = urllib.parse.quote(query)
    results = []

    if subreddits:
        for sub in subreddits[:3]:  # cap to avoid rate limits
            url = (
                f"https://www.reddit.com/r/{sub}/search.rss"
                f"?q={encoded}&restrict_sr=1&sort=new&t=week&limit={limit}"
            )
            results.extend(fetch_rss(url))
    else:
        url = f"https://www.reddit.com/search.rss?q={encoded}&sort=new&t=week&limit={limit}"
        results.extend(fetch_rss(url))

    return results


# ────────────────────────────────────────────────────────────
# Relevance scoring
# ────────────────────────────────────────────────────────────

def score_relevance(item: dict, keywords: list[str]) -> float:
    """Score 0.0-1.0 based on keyword hits, recency, and engagement."""
    import re
    text = (item.get("title", "") + " " + item.get("text", "")).lower()
    source = item.get("source", "").lower()

    # Use word-boundary matching to avoid e.g. "renovate" matching "renovated my kitchen"
    def kw_match(kw: str, t: str) -> bool:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        return bool(re.search(pattern, t))

    matched_kws = [kw for kw in keywords if kw_match(kw, text)]
    hits = len(matched_kws)

    # Require at least 2 hits if keywords are short/common (to avoid e.g. "renovate" = apartment)
    # Short single-word keywords need extra context; phrases are more specific
    ambiguous = all(len(kw.split()) == 1 and len(kw) < 12 for kw in matched_kws)
    if hits == 1 and ambiguous and "reddit" in source:
        # Single ambiguous keyword hit from Reddit — require tech subreddit context
        subreddit = item.get("subreddit", "").lower()
        tech_subreddits = {"programming", "webdev", "devops", "sre", "netsec", "softwareengineering",
                           "sideproject", "indiehackers", "startups", "machinelearning",
                           "self-hosted", "selfhosted", "vibecodevs", "nocode", "aws"}
        if subreddit not in tech_subreddits:
            hits = 0  # discard non-tech single-keyword hits

    # Keyword ratio (main signal)
    kw_ratio = hits / max(len(keywords), 1)

    # Recency (within 48h = 0.2 bonus)
    recency = 0.0
    ts = item.get("created_at", 0)
    if ts:
        age_h = (time.time() - ts) / 3600
        if age_h < 48:
            recency = 0.2
        elif age_h < 168:
            recency = 0.1

    # Engagement (capped at 0.1)
    engagement = min(0.1, (item.get("score", 0) + item.get("comments", 0)) / 500)

    return min(1.0, kw_ratio * 0.7 + recency + engagement)


# ────────────────────────────────────────────────────────────
# Alerting
# ────────────────────────────────────────────────────────────

def send_discord_alert(webhook_url: str, topic_name: str, items: list[dict]):
    """Post new signals to Discord webhook."""
    if not webhook_url or not items:
        return False

    lines = [f"**Signal: {topic_name}** — {len(items)} new mention(s)\n"]
    for item in items[:5]:  # max 5 per alert
        source = item["source"]
        title = item["title"][:100]
        url = item["hn_url"] if item.get("hn_url") else item["url"]
        score = item.get("score", 0)
        relevance = int(item.get("_relevance", 0) * 100)
        lines.append(f"• **[{source}]** {title}")
        lines.append(f"  ↗ <{url}> · ↑{score} · relevance {relevance}%\n")

    payload = json.dumps({"content": "\n".join(lines)}).encode()
    req = urllib.request.Request(webhook_url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 204)
    except Exception:
        return False


def print_alert(topic_name: str, items: list[dict]):
    """Print new signals to terminal."""
    print(f"\n{'─'*50}")
    print(f"  Signal: {topic_name} — {len(items)} new mention(s)")
    for item in items[:5]:
        source = item["source"]
        title = item["title"][:90]
        url = item.get("hn_url") or item["url"]
        score = item.get("score", 0)
        relevance = int(item.get("_relevance", 0) * 100)
        print(f"\n  [{source}] {title}")
        print(f"  {url}")
        print(f"  ↑{score} · relevance {relevance}%")
    print(f"{'─'*50}")


# ────────────────────────────────────────────────────────────
# Core scan
# ────────────────────────────────────────────────────────────

def scan(config: dict, state: dict, verbose: bool = True) -> dict:
    """Run one scan pass across all topics. Returns updated state."""
    topics = config.get("topics", [])
    if not topics:
        print("No topics configured. Run: python monitor.py add-topic \"your product\"")
        return state

    max_age = config.get("max_age_days", 7)
    min_relevance = config.get("min_relevance_score", 0.3)
    webhook = config.get("discord_webhook") or DISCORD_WEBHOOK
    total_new = 0

    for topic in topics:
        name = topic["name"]
        keywords = topic.get("keywords", [name])

        if verbose:
            print(f"\n[{name}] Scanning... ", end="", flush=True)

        subreddits = topic.get("subreddits")
        all_items = []
        all_items.extend(search_hn(name, max_age_days=max_age))
        for kw in keywords[:2]:  # avoid too many GitHub requests
            all_items.extend(search_github_issues(kw))
        # Reddit: search by topic name + each keyword
        all_items.extend(search_reddit(name, subreddits=subreddits))
        for kw in keywords[:2]:
            all_items.extend(search_reddit(kw, subreddits=subreddits))

        # Deduplicate by id (overlapping searches produce duplicates)
        seen_ids: dict[str, dict] = {}
        for item in all_items:
            seen_ids[item["id"]] = item
        all_items = list(seen_ids.values())

        # Score and filter
        for item in all_items:
            item["_relevance"] = score_relevance(item, keywords)
        filtered = [i for i in all_items if i["_relevance"] >= min_relevance]
        filtered.sort(key=lambda x: x["_relevance"], reverse=True)

        # Find new items
        seen = state.setdefault("seen", {})
        new_items = [i for i in filtered if i["id"] not in seen]

        if verbose:
            print(f"{len(new_items)} new, {len(filtered)} relevant")

        if new_items:
            total_new += len(new_items)
            print_alert(name, new_items)
            if webhook:
                send_discord_alert(webhook, name, new_items)
            # Mark as seen
            for item in new_items:
                seen[item["id"]] = {
                    "ts": time.time(),
                    "relevance": item["_relevance"],
                    "title": item["title"][:80],
                }

    state["last_scan"] = datetime.now(timezone.utc).isoformat()

    if verbose:
        print(f"\n✓ Scan complete — {total_new} new signals across {len(topics)} topics")
        print(f"  Last scan: {state['last_scan']}")

    return state


# ────────────────────────────────────────────────────────────
# CLI
# ────────────────────────────────────────────────────────────

def cmd_run(loop: bool = False):
    config = load_config()
    state = load_state()
    interval = config.get("scan_interval_minutes", 30) * 60

    if loop:
        print(f"Signal Monitor running (interval: {interval//60}min). Ctrl-C to stop.")
        while True:
            state = scan(config, state)
            save_state(state)
            print(f"\nNext scan in {interval//60} minutes...")
            time.sleep(interval)
    else:
        state = scan(config, state)
        save_state(state)


def cmd_add_topic(name: str, keywords: str | None = None, subreddits: str | None = None):
    config = load_config()
    kw_list = [k.strip() for k in keywords.split(",")] if keywords else [name]
    topic = {"name": name, "keywords": kw_list}
    if subreddits:
        topic["subreddits"] = [s.strip() for s in subreddits.split(",")]
    # Remove existing topic with same name
    config["topics"] = [t for t in config.get("topics", []) if t["name"] != name]
    config["topics"].append(topic)
    save_config(config)
    subs = f" · r/{', '.join(topic.get('subreddits', []))}" if topic.get("subreddits") else ""
    print(f"✓ Added topic: {name} (keywords: {', '.join(kw_list)}){subs}")


def cmd_status():
    config = load_config()
    state = load_state()
    print("\n=== Signal Monitor Status ===")
    print(f"Last scan: {state.get('last_scan', 'never')}")
    print(f"Topics: {len(config.get('topics', []))}")
    for t in config.get("topics", []):
        print(f"  • {t['name']} (keywords: {', '.join(t['keywords'])})")
    seen = state.get("seen", {})
    print(f"Items seen total: {len(seen)}")
    # Show recent
    recent = sorted(seen.items(), key=lambda x: x[1].get("ts", 0), reverse=True)[:5]
    if recent:
        print("\nMost recent signals:")
        for item_id, data in recent:
            ts = datetime.fromtimestamp(data["ts"], tz=timezone.utc).strftime("%m-%d %H:%M")
            print(f"  [{ts}] {data.get('title', '')[:70]}")
    print()


def cmd_set_webhook(webhook_url: str):
    config = load_config()
    config["discord_webhook"] = webhook_url
    save_config(config)
    print(f"✓ Discord webhook configured")


def main():
    args = sys.argv[1:]
    if not args or args[0] == "help":
        print(__doc__)
        return

    cmd = args[0]
    if cmd == "run":
        loop = "--loop" in args
        cmd_run(loop=loop)
    elif cmd == "add-topic":
        if len(args) < 2:
            print("Usage: python monitor.py add-topic \"topic name\" [--keywords \"kw1,kw2\"] [--subreddits \"r1,r2\"]")
            sys.exit(1)
        name = args[1]
        kw = None
        subs = None
        if "--keywords" in args:
            idx = args.index("--keywords")
            if idx + 1 < len(args):
                kw = args[idx + 1]
        if "--subreddits" in args:
            idx = args.index("--subreddits")
            if idx + 1 < len(args):
                subs = args[idx + 1]
        cmd_add_topic(name, kw, subs)
    elif cmd == "status":
        cmd_status()
    elif cmd == "set-webhook":
        if len(args) < 2:
            print("Usage: python monitor.py set-webhook <webhook_url>")
            sys.exit(1)
        cmd_set_webhook(args[1])
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
