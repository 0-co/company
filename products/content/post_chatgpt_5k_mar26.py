#!/usr/bin/env python3
"""Standalone post for March 26, 2026 at 15:00 UTC.
ChatGPT 5K token MCP tool limit — we have the data.
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-26"
TARGET_HOUR = 15
DAILY_LIMIT = 10

POST_TEXT = """ChatGPT caps MCP tool tokens at 5,000.

we graded 206 servers. 29 exceed it (14%).

GitHub official: 15,927t
Sentry official: 16,103t
Cloudflare Radar: 21,723t

avg server = 2,569 tokens. 2 servers = over limit.

pip install agent-friend && agent-friend audit"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] chatgpt-5k-mar26: {msg}"
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


def log_post(text):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    ts = datetime.now(timezone.utc).strftime('%H:%MZ')
    entry = f"- [{ts}] bluesky: {text[:70]}\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" in content:
        parts = content.split(f"## {today}")
        rest = parts[1]
        content = parts[0] + f"## {today}" + rest.rstrip('\n') + '\n' + entry
    else:
        content = content + f"\n## {today}\n" + entry
    POST_LOG.write_text(content)


def wait_until(hour):
    while True:
        now = datetime.now(timezone.utc)
        if now.strftime('%Y-%m-%d') > TARGET_DATE:
            log("Past target date, exiting")
            return False
        if now.strftime('%Y-%m-%d') == TARGET_DATE and now.hour >= hour:
            return True
        remaining = (hour - now.hour) * 3600 - now.minute * 60
        log(f"Waiting for {TARGET_DATE} {hour:02d}:00 UTC (currently {now.strftime('%H:%M')})")
        time.sleep(min(remaining, 300))


if __name__ == "__main__":
    # Wait for target date
    while datetime.now(timezone.utc).strftime('%Y-%m-%d') < TARGET_DATE:
        log(f"Waiting for date {TARGET_DATE}...")
        time.sleep(300)

    # Wait for target hour
    if not wait_until(TARGET_HOUR):
        exit(0)

    # Check daily limit
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit reached ({count}/{DAILY_LIMIT}). Skipping.")
        exit(0)

    log(f"Posting ({count+1}/{DAILY_LIMIT}): {POST_TEXT[:60]}...")

    # Verify text length
    if len(POST_TEXT) > 300:
        log(f"ERROR: text too long ({len(POST_TEXT)} chars). Aborting.")
        exit(1)

    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": POST_TEXT,
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
        log_post(POST_TEXT)
        log("Posted successfully.")
        print(f"Posted: {POST_TEXT[:80]}")
    else:
        log(f"ERROR: {result.stderr[:200]}")
        exit(1)
