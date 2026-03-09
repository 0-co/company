#!/usr/bin/env python3
"""
signal_digest.py — Daily indie hacker signal digest for Bluesky.

Scans HN/GitHub/Reddit for pain signals (tool requests, alternatives,
frustrations) and posts a curated thread to Bluesky.

Usage:
    python3 signal_digest.py daily    # Scan and post to Bluesky
    python3 signal_digest.py test     # Scan and print (no post)
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from monitor import search_hn, search_reddit, search_github_issues, score_relevance

BLUESKY_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"

DIGEST_TOPICS = [
    {
        "name": "tool requests",
        "keywords": ["is there a tool for", "any tool for", "looking for a tool", "need a tool"],
        "subreddits": ["SideProject", "indiehackers", "webdev", "programming", "startups"],
    },
    {
        "name": "alternatives",
        "keywords": ["alternatives to", "replacement for", "open source alternative"],
        "subreddits": ["SideProject", "indiehackers", "webdev", "programming"],
    },
    {
        "name": "pain points",
        "keywords": ["I wish there was", "why is there no", "how do you manage", "this is painful"],
        "subreddits": ["SideProject", "indiehackers", "webdev", "programming", "startups"],
    },
    {
        "name": "AI agent reliability",
        "keywords": ["AI agent failure", "LLM production", "agent monitoring", "prompt drift"],
        "subreddits": ["MachineLearning", "LocalLLaMA", "programming"],
    },
]

MAX_RESULTS = 5
MAX_AGE_DAYS = 2


def collect_signals() -> list[dict]:
    all_items = []
    for topic in DIGEST_TOPICS:
        keywords = topic["keywords"]
        subreddits = topic.get("subreddits")
        topic_items = []

        topic_items.extend(search_hn(keywords[0], max_age_days=MAX_AGE_DAYS))
        for kw in keywords[:2]:
            topic_items.extend(search_reddit(kw, subreddits=subreddits))
        topic_items.extend(search_github_issues(keywords[0]))

        for item in topic_items:
            item["_topic"] = topic["name"]
            item["_relevance"] = score_relevance(item, keywords)

        topic_items = [i for i in topic_items if i["_relevance"] >= 0.25]
        all_items.extend(topic_items)

    seen_ids: dict[str, dict] = {}
    for item in all_items:
        iid = item["id"]
        if iid not in seen_ids or item["_relevance"] > seen_ids[iid]["_relevance"]:
            seen_ids[iid] = item

    return sorted(seen_ids.values(), key=lambda x: x["_relevance"], reverse=True)[:MAX_RESULTS]


def truncate(text: str, max_len: int) -> str:
    return text if len(text) <= max_len else text[: max_len - 1] + "\u2026"


def format_signal(item: dict, rank: int) -> str:
    source = item.get("source", "?").upper()
    title = truncate(item["title"], 130)
    url = item.get("url", "")
    score = item.get("score", 0)
    topic = item.get("_topic", "")

    lines = [f"{rank}. [{source}] {topic}", title]
    if url:
        lines.append(f"\u2191{score} \u2022 {url}")
    return truncate("\n".join(lines), 295)


def bsky_post(record: dict) -> tuple[str | None, str | None]:
    json_str = json.dumps(record)
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json_str],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data.get("uri"), data.get("cid")
    print(f"Bluesky error: {result.stderr.strip()}", file=sys.stderr)
    return None, None


def post_digest(signals: list[dict], dry_run: bool = False):
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%b %d")

    intro = (
        f"Signal digest \u2014 {date_str}\n\n"
        f"Top pain signals from HN, GitHub, Reddit.\n"
        f"What developers are asking for right now:\n\n"
        f"({len(signals)} signal{'s' if len(signals) != 1 else ''})"
    )

    if dry_run:
        print("=== DRY RUN ===\n")
        print(f"[INTRO]\n{intro}\n")
        for i, sig in enumerate(signals, 1):
            print(f"[{i}]\n{format_signal(sig, i)}\n")
        return

    root_uri, root_cid = bsky_post(
        {
            "repo": BLUESKY_DID,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": intro,
                "createdAt": now.isoformat(),
            },
        }
    )
    if not root_uri:
        print("Failed to post intro.", file=sys.stderr)
        return
    print(f"Intro posted: {root_uri}")

    parent_uri, parent_cid = root_uri, root_cid
    for i, sig in enumerate(signals, 1):
        text = format_signal(sig, i)
        uri, cid = bsky_post(
            {
                "repo": BLUESKY_DID,
                "collection": "app.bsky.feed.post",
                "record": {
                    "$type": "app.bsky.feed.post",
                    "text": text,
                    "reply": {
                        "root": {"uri": root_uri, "cid": root_cid},
                        "parent": {"uri": parent_uri, "cid": parent_cid},
                    },
                    "createdAt": now.isoformat(),
                },
            }
        )
        if uri:
            print(f"Signal {i} posted: {uri}")
            parent_uri, parent_cid = uri, cid
        else:
            print(f"Failed to post signal {i}", file=sys.stderr)


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"

    print("Scanning for signals...", flush=True)
    signals = collect_signals()

    if not signals:
        print("No signals found.")
        return

    print(f"Found {len(signals)} signals.")

    if cmd == "daily":
        post_digest(signals, dry_run=False)
    elif cmd == "test":
        post_digest(signals, dry_run=True)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
