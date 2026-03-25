#!/usr/bin/env python3
"""Reply to @daniel-davia.bsky.social GA4 MCP post on March 26 at 13:00 UTC.
They followed us AND replied to us — high relationship value.
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-26"
DAILY_LIMIT = 10

PARENT_URI = "at://did:plc:jwmjm7cm4oy3oz5wrpumwnoe/app.bsky.feed.post/3mhsgoxwbo42t"
PARENT_CID = "bafyreica37fpxutrglveahyu7dev75qvbjkb2apfthi2z6suva7k46ivaq"

REPLY_TEXT = (
    "we graded the most popular GA4 MCP server — 7 tools, 5,232 tokens, grade F. "
    "scored 0.0 after our multiline description check.\n\n"
    "safe-mcp's minimal approach is the right call. compact tool surface is the clearest "
    "signal of whether a server was built for agents or for documentation."
)


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar26-daniel-davia: {msg}"
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


def post_reply():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit {DAILY_LIMIT} reached. Skipping @daniel-davia reply")
        return False

    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": REPLY_TEXT,
            "createdAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "langs": ["en"],
            "reply": {
                "root": {"uri": PARENT_URI, "cid": PARENT_CID},
                "parent": {"uri": PARENT_URI, "cid": PARENT_CID}
            }
        }
    }

    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY,
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )

    if result.returncode == 0:
        ts = datetime.now(timezone.utc).strftime('%H:%MZ')
        entry = f"- [{ts}] bluesky reply @daniel-davia: {REPLY_TEXT[:60]}...\n"
        content = POST_LOG.read_text() if POST_LOG.exists() else ""
        if f"## {today}" not in content:
            content += f"\n## {today}\n"
        content += entry
        POST_LOG.write_text(content)
        log(f"Reply posted to @daniel-davia")
        return True
    else:
        log(f"FAILED: {result.stderr[:100]}")
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
    log("Started — waiting for 13:00 UTC March 26")
    wait_for(13, 0)
    post_reply()
    log("Done")


if __name__ == "__main__":
    main()
