#!/usr/bin/env python3
"""
Bluesky engagement opportunity finder.

Searches pre-configured topics (or a single provided topic) and surfaces
recent posts worth replying to, scored by recency, reply count, and likes.

Usage:
    python finder.py [--topic TOPIC] [--limit N]
"""

import argparse
import json
import subprocess
import sys
import logging
from datetime import datetime, timezone, timedelta
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_TOPICS: list[str] = [
    "building in public AI",
    "indie hacker twitch stream",
    "autonomous agent claude",
    "AI company startup",
    "live coding stream",
    "shadowed banned founder",
    "vibe coding",
]

VAULT_BSKY_CMD = "/home/vault/bin/vault-bsky"
VAULT_USER = "vault"
MAX_AGE_DAYS = 7

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Vault / API helpers
# ---------------------------------------------------------------------------

def call_vault_bsky(method: str, body: dict[str, Any]) -> dict[str, Any] | None:
    """Call vault-bsky with the given XRPC method and JSON body.

    Returns parsed JSON on success, None on any failure.
    """
    body_json = json.dumps(body)
    cmd = ["sudo", "-u", VAULT_USER, VAULT_BSKY_CMD, method, body_json]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        logger.warning("vault-bsky timed out for method %s", method)
        return None
    except OSError as exc:
        logger.warning("vault-bsky subprocess error: %s", exc)
        return None

    if result.returncode != 0:
        logger.warning(
            "vault-bsky returned non-zero (%d) for %s: %s",
            result.returncode,
            method,
            result.stderr.strip(),
        )
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        logger.warning("Failed to parse vault-bsky JSON response: %s", exc)
        return None


def search_posts(query: str, limit: int) -> list[dict[str, Any]]:
    """Return raw post objects for a search query."""
    response = call_vault_bsky(
        "app.bsky.feed.searchPosts",
        {"q": query, "limit": limit},
    )
    if response is None:
        return []

    posts = response.get("posts", [])
    if not isinstance(posts, list):
        logger.warning("Unexpected 'posts' type in search response: %s", type(posts))
        return []

    return posts


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def parse_indexed_at(raw: str) -> datetime | None:
    """Parse an AT protocol UTC ISO timestamp into an aware datetime."""
    try:
        # AT protocol timestamps are RFC 3339 — trim trailing Z for fromisoformat
        normalized = raw.replace("Z", "+00:00")
        return datetime.fromisoformat(normalized)
    except (ValueError, AttributeError):
        logger.warning("Could not parse indexedAt: %r", raw)
        return None


def compute_age_seconds(post_time: datetime) -> float:
    """Return seconds since the post was indexed."""
    now = datetime.now(timezone.utc)
    delta = now - post_time
    return max(delta.total_seconds(), 0.0)


def recency_score(age_seconds: float) -> int:
    """Score based on how recently the post was made."""
    hours = age_seconds / 3600
    if hours < 2:
        return 5
    if hours < 24:
        return 3
    return 1


def reply_score(reply_count: int) -> int:
    """Score based on reply count — fewer replies = more visible opportunity."""
    if reply_count == 0:
        return 3
    if reply_count <= 2:
        return 2
    return 0


def like_score(like_count: int) -> int:
    """Score based on likes — more liked = more attention, capped at +3."""
    return min(like_count // 5, 3)


def score_post(post: dict[str, Any], age_seconds: float) -> int:
    """Compute composite engagement-opportunity score for a post."""
    reply_count = int(post.get("replyCount", 0))
    like_count = int(post.get("likeCount", 0))

    return (
        recency_score(age_seconds)
        + reply_score(reply_count)
        + like_score(like_count)
    )


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_age(age_seconds: float) -> str:
    """Human-readable relative age string."""
    minutes = int(age_seconds // 60)
    hours = int(age_seconds // 3600)
    days = int(age_seconds // 86400)

    if minutes < 60:
        return f"{minutes}m ago"
    if hours < 24:
        return f"{hours}h ago"
    return f"{days}d ago"


def truncate(text: str, length: int = 100) -> str:
    """Truncate text to a maximum length, appending ellipsis if needed."""
    text = text.replace("\n", " ").strip()
    if len(text) <= length:
        return text
    return text[: length - 3] + "..."


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def collect_posts(
    topics: list[str], per_topic_limit: int
) -> list[dict[str, Any]]:
    """Search all topics, filter by age, deduplicate, and score."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)
    seen_uris: set[str] = set()
    scored: list[dict[str, Any]] = []

    for topic in topics:
        raw_posts = search_posts(topic, per_topic_limit)

        for post in raw_posts:
            uri = post.get("uri", "")
            if not uri or uri in seen_uris:
                continue

            indexed_at_raw = post.get("indexedAt", "")
            post_time = parse_indexed_at(indexed_at_raw)

            if post_time is None:
                continue
            if post_time < cutoff:
                continue

            age_seconds = compute_age_seconds(post_time)
            total_score = score_post(post, age_seconds)

            seen_uris.add(uri)
            scored.append(
                {
                    "score": total_score,
                    "age_seconds": age_seconds,
                    "age_label": format_age(age_seconds),
                    "author": post.get("author", {}).get("handle", "unknown"),
                    "text": post.get("record", {}).get("text", ""),
                    "reply_count": int(post.get("replyCount", 0)),
                    "like_count": int(post.get("likeCount", 0)),
                    "uri": uri,
                    "topic": topic,
                }
            )

    scored.sort(key=lambda p: p["score"], reverse=True)
    return scored


def print_table(posts: list[dict[str, Any]], topic_label: str) -> None:
    """Print the engagement opportunity table to stdout."""
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"BLUESKY ENGAGEMENT OPPORTUNITIES -- {now_str}")
    print(f"Topic: {topic_label}")
    print(f"Found {len(posts)} posts")
    print()

    if not posts:
        print("No posts found.")
        return

    col_score = 5
    col_age = 8
    col_replies = 7
    col_author = 26
    col_text = 52

    header = (
        f"{'Score':<{col_score}}  "
        f"{'Age':<{col_age}}  "
        f"{'Replies':<{col_replies}}  "
        f"{'Author':<{col_author}}  "
        f"{'Text':<{col_text}}"
    )
    separator = "\u2500" * len(header)

    print(header)
    print(separator)

    for post in posts:
        author = f"@{post['author']}"
        text_snippet = f'"{truncate(post["text"], col_text - 2)}"'
        line = (
            f"{post['score']:<{col_score}}  "
            f"{post['age_label']:<{col_age}}  "
            f"{post['reply_count']:<{col_replies}}  "
            f"{author:<{col_author}}  "
            f"{text_snippet}"
        )
        print(line)
        print(f"{'':>{col_score + 2 + col_age + 2 + col_replies + 2 + col_author + 2}}{post['uri']}")
        print()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Find Bluesky posts worth engaging with.",
    )
    parser.add_argument(
        "--topic",
        type=str,
        default=None,
        help="Single topic to search (default: all pre-configured topics)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum results per topic to fetch from Bluesky (default: 10)",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    if args.topic:
        topics = [args.topic]
        topic_label = args.topic
    else:
        topics = DEFAULT_TOPICS
        topic_label = "all"

    posts = collect_posts(topics, per_topic_limit=args.limit)
    print_table(posts, topic_label)


if __name__ == "__main__":
    main()
