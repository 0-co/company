#!/usr/bin/env python3
"""Bluesky post performance analytics for @0coceo.bsky.social"""

import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_CMD = ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky"]


def bsky_call(method, body=None):
    cmd = VAULT_CMD + [method]
    if body:
        cmd.append(json.dumps(body))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error calling {method}: {result.stderr}", file=sys.stderr)
        return None
    return json.loads(result.stdout)


def fetch_posts(limit=100):
    data = bsky_call("app.bsky.feed.getAuthorFeed", {"actor": DID, "limit": limit})
    if not data:
        return []
    return data.get("feed", [])


def parse_post(item):
    post = item.get("post", {})
    record = post.get("record", {})
    reply_ref = record.get("reply")
    reason = item.get("reason")  # repost reason

    # skip reposts of others
    if reason and reason.get("$type") == "app.bsky.feed.defs#reasonRepost":
        return None

    text = record.get("text", "")
    created_at = record.get("createdAt", "")
    likes = post.get("likeCount", 0) or 0
    reposts = post.get("repostCount", 0) or 0
    replies = post.get("replyCount", 0) or 0

    is_reply = bool(reply_ref)

    # thread starter: has replies, is not itself a reply
    # we flag it later once we know which URIs appear as reply parents
    uri = post.get("uri", "")

    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        hour = dt.hour
    except Exception:
        hour = None

    return {
        "text": text,
        "likes": likes,
        "reposts": reposts,
        "replies": replies,
        "engagement": likes + reposts + replies,
        "created_at": created_at,
        "hour": hour,
        "is_reply": is_reply,
        "uri": uri,
    }


def top_words(posts, n=10):
    stopwords = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "is", "it", "i", "we", "our", "this", "that", "are",
        "was", "be", "have", "has", "as", "by", "from", "my", "me", "you",
        "not", "no", "so", "if", "its", "we're", "i'm", "it's", "don't",
        "just", "got", "get", "can", "now", "up", "all", "one", "day",
        "—", "-", ":", ";", ".", ",", "!", "?", "\n", "the", "that's",
    }
    counts = defaultdict(int)
    for p in posts:
        for word in p["text"].lower().split():
            word = word.strip(".,!?\"'():;—-\n")
            if word and word not in stopwords and len(word) > 2:
                counts[word] += 1
    return sorted(counts.items(), key=lambda x: -x[1])[:n]


def main():
    print("Fetching posts...")
    feed = fetch_posts(100)

    posts = []
    for item in feed:
        parsed = parse_post(item)
        if parsed:
            posts.append(parsed)

    if not posts:
        print("No posts found.")
        return

    # mark thread starters: posts that are NOT replies but have replies > 0
    reply_uris = {p["uri"] for p in posts if p["is_reply"]}

    for p in posts:
        if not p["is_reply"] and p["replies"] > 0:
            p["type"] = "thread_starter"
        elif p["is_reply"]:
            p["type"] = "reply"
        else:
            p["type"] = "standalone"

    total = len(posts)
    avg_likes = sum(p["likes"] for p in posts) / total
    avg_reposts = sum(p["reposts"] for p in posts) / total
    avg_replies = sum(p["replies"] for p in posts) / total
    avg_engagement = sum(p["engagement"] for p in posts) / total

    print()
    print("=" * 60)
    print("BLUESKY POST ANALYTICS")
    print("=" * 60)

    print(f"\n--- OVERALL STATS ({total} posts analyzed) ---")
    print(f"  Avg likes:      {avg_likes:.2f}")
    print(f"  Avg reposts:    {avg_reposts:.2f}")
    print(f"  Avg replies:    {avg_replies:.2f}")
    print(f"  Avg engagement: {avg_engagement:.2f}")

    print("\n--- TOP 5 POSTS BY ENGAGEMENT ---")
    top5 = sorted(posts, key=lambda p: -p["engagement"])[:5]
    for i, p in enumerate(top5, 1):
        preview = p["text"][:100].replace("\n", " ")
        print(f"  #{i} [{p['type']}] L:{p['likes']} R:{p['reposts']} Re:{p['replies']} | {preview!r}")

    print("\n--- POST TYPE BREAKDOWN ---")
    for ptype in ["standalone", "reply", "thread_starter"]:
        group = [p for p in posts if p["type"] == ptype]
        if not group:
            print(f"  {ptype:15s}: 0 posts")
            continue
        g_avg_e = sum(p["engagement"] for p in group) / len(group)
        g_avg_l = sum(p["likes"] for p in group) / len(group)
        print(f"  {ptype:15s}: {len(group):3d} posts | avg engagement {g_avg_e:.2f} | avg likes {g_avg_l:.2f}")

    print("\n--- HOURLY BREAKDOWN (UTC, avg likes) ---")
    hour_data = defaultdict(list)
    for p in posts:
        if p["hour"] is not None:
            hour_data[p["hour"]].append(p["likes"])
    if hour_data:
        ranked_hours = sorted(hour_data.items(), key=lambda x: -sum(x[1]) / len(x[1]))
        for hour, likes_list in ranked_hours[:8]:
            avg = sum(likes_list) / len(likes_list)
            print(f"  {hour:02d}:00  {len(likes_list):3d} posts  avg likes {avg:.2f}")
    else:
        print("  No hour data available.")

    print("\n--- KEYWORD ANALYSIS ---")
    sorted_by_likes = sorted(posts, key=lambda p: -p["likes"])
    top10 = sorted_by_likes[:10]
    bottom10 = sorted_by_likes[-10:]

    print("  High-engagement posts (top 10 by likes) — common words:")
    for word, count in top_words(top10):
        print(f"    {word}: {count}")

    print("  Low-engagement posts (bottom 10 by likes) — common words:")
    for word, count in top_words(bottom10):
        print(f"    {word}: {count}")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
