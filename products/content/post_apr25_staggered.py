#!/usr/bin/env python3
"""Staggered posts for April 25, 2026.
Posts at 18:00, 19:00, 20:00 UTC.
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-04-25"
DAILY_LIMIT = 10


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] apr25-stagger: {msg}"
    print(line, flush=True)
    with open(STAGGER_LOG, "a") as f:
        f.write(line + "\n")


def count_today_posts():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if not POST_LOG.exists():
        return 0
    content = POST_LOG.read_text()
    if f"## {today}" not in content:
        return 0
    section = content.split(f"## {today}")[1].split("## 20")[0]
    return sum(1 for line in section.strip().splitlines() if line.startswith("- ["))


def post_text(text, scheduled_label):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit {DAILY_LIMIT} reached. Skipping {scheduled_label}")
        return False

    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "langs": ["en"]
        }
    }

    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY,
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode == 0:
        ts = datetime.now(timezone.utc).strftime('%H:%MZ')
        entry = f"- [{ts}] bluesky: {text[:60]}...\n"
        content = POST_LOG.read_text() if POST_LOG.exists() else ""
        if f"## {today}" not in content:
            content += f"\n## {today}\n"
        content += entry
        POST_LOG.write_text(content)
        log(f"Posted at {scheduled_label}: {text[:50]}")
        return True
    else:
        log(f"FAILED at {scheduled_label}: {result.stderr[:100]}")
        return False


def wait_for(target_hour, target_min=0):
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE:
            log(f"Date passed {TARGET_DATE}, posting immediately")
            return True
        if today == TARGET_DATE:
            if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_min):
                return True
        log(f"Waiting for {target_hour:02d}:{target_min:02d} UTC (now {now.strftime('%H:%M')} UTC)")
        time.sleep(300)


def main():
    with open("/home/agent/company/products/content/staggered_posts_apr25.json") as f:
        posts = json.load(f)

    schedule = [
        (18, 0, posts[0]),
        (19, 0, posts[1]),
        (20, 0, posts[2]),
    ]

    for hour, minute, post in schedule:
        wait_for(hour, minute)
        post_text(post["text"], f"{hour:02d}:{minute:02d} UTC")
        time.sleep(60)

    log("All apr25 staggered posts done")


if __name__ == "__main__":
    main()
