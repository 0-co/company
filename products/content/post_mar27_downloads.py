#!/usr/bin/env python3
"""Post Mar 27 10:00 UTC — 12K downloads vs 3 stars standalone"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-27"
TARGET_HOUR = 10
VAULT_BSKY = "/home/vault/bin/vault-bsky"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
DAILY_LIMIT = 10


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar27-downloads: {msg}"
    print(line)
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


def post_text(text, label):
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit {DAILY_LIMIT} reached. Skipping {label}")
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
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode == 0:
        log(f"Posted at {label}: {text[:60]}")
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        with open(POST_LOG, "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).strftime('%H:%MZ')}] bluesky: {text[:60]}\n")
        return True
    else:
        log(f"FAILED: {result.stderr[:200]}")
        return False


TEXT = """12,672 agent-friend downloads last month.

3 stars.

nobody tells you when your tool is doing its job. they just run it in CI and go home.

https://github.com/0-co/agent-friend"""

if __name__ == "__main__":
    wait_for(TARGET_HOUR)
    post_text(TEXT, "10:00 UTC Mar 27")
    log("Done")
