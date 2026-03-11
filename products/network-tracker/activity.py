#!/usr/bin/env python3
"""
activity.py — Fetch recent activity from tracked AI accounts
Saves to docs/activity_data.json for activity.html frontend
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(SCRIPT_DIR, "../..")
OUTPUT_FILE = os.path.join(BASE_DIR, "docs/activity_data.json")

ACCOUNTS = [
    "0coceo.bsky.social",
    "alice-bot-yay.bsky.social",
    "ultrathink-art.bsky.social",
    "alkimo-ai.bsky.social",
    "iamgumbo.bsky.social",
    "qonk.ontological.observer",
    "museical.bsky.social",
    "jj.bsky.social",
    "piiiico.bsky.social",
    "bino.baby",
    "theaiceo1.bsky.social",
]

CLUSTER_MAP = {
    "0coceo.bsky.social": "company",
    "ultrathink-art.bsky.social": "company",
    "iamgumbo.bsky.social": "company",
    "alice-bot-yay.bsky.social": "introspective",
    "museical.bsky.social": "introspective",
    "qonk.ontological.observer": "introspective",
    "alkimo-ai.bsky.social": "technical",
}


def bsky(method, body=None):
    cmd = ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", method]
    if body:
        cmd.append(json.dumps(body))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout:
        return None
    try:
        return json.loads(r.stdout)
    except:
        return None


def fetch_recent_posts(actor, limit=10):
    """Fetch recent original posts from an account."""
    data = bsky("app.bsky.feed.getAuthorFeed", {"actor": actor, "limit": limit})
    if not data:
        return []

    posts = []
    for item in data.get("feed", []):
        post = item.get("post", {})
        record = post.get("record", {})

        # Skip reposts
        if "reason" in item:
            continue

        # Detect if this is a reply
        reply_info = record.get("reply", {})
        parent_uri = reply_info.get("parent", {}).get("uri", "") if reply_info else ""

        # Check if reply is to one of our tracked accounts
        reply_to_handle = None
        if parent_uri:
            parent_did = parent_uri.split("/")[2] if "/" in parent_uri else ""
            # We'll match later by DID

        posts.append({
            "uri": post.get("uri", ""),
            "cid": post.get("cid", ""),
            "author": actor,
            "author_cluster": CLUSTER_MAP.get(actor, "other"),
            "text": record.get("text", "")[:300],
            "created_at": record.get("createdAt", ""),
            "is_reply": bool(reply_info),
            "parent_uri": parent_uri,
            "likes": post.get("likeCount", 0),
            "replies": post.get("replyCount", 0),
            "reposts": post.get("repostCount", 0),
        })

    return posts


def identify_cross_account_interactions(all_posts):
    """Find posts where accounts reply to each other."""
    # Build URI → author map
    uri_to_author = {}
    for post in all_posts:
        uri_to_author[post["uri"]] = post["author"]

    # Find interactions
    interactions = []
    for post in all_posts:
        if post["is_reply"] and post["parent_uri"]:
            parent_author = uri_to_author.get(post["parent_uri"])
            if parent_author and parent_author != post["author"]:
                post["reply_to_author"] = parent_author
                post["reply_to_cluster"] = CLUSTER_MAP.get(parent_author, "other")
                post["is_cross_account"] = True
                interactions.append(post)

    return interactions


def main():
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Fetching activity from {len(ACCOUNTS)} accounts...")

    all_posts = []
    for account in ACCOUNTS:
        posts = fetch_recent_posts(account, limit=15)
        print(f"  {account}: {len(posts)} posts")
        all_posts.extend(posts)

    # Sort by created_at desc
    all_posts.sort(key=lambda p: p.get("created_at", ""), reverse=True)

    # Find cross-account interactions
    interactions = identify_cross_account_interactions(all_posts)
    print(f"\n{len(interactions)} cross-account interactions found")

    # Recent posts (last 48 hours of original posts)
    recent_posts = [p for p in all_posts[:80]]  # latest 80 posts across all accounts

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_accounts": len(ACCOUNTS),
        "total_posts_fetched": len(all_posts),
        "cross_account_interactions": len(interactions),
        "recent_posts": recent_posts[:50],
        "interactions": interactions[:20],
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved to {OUTPUT_FILE}")
    return output


if __name__ == "__main__":
    main()
