#!/usr/bin/env python3
"""Morning posts for March 31, 2026.
10:00 — arxiv taxonomy angle (Polytechnique Montreal 419 MCP faults, no detection tools)
11:00 — accuracy degradation angle (43% → 14% tool selection with bloated schemas)
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-31"
DAILY_LIMIT = 10

ARXIV_TEXT = (
    "researchers just classified 419 real MCP faults across 470 repos.\n\n"
    "largest category: tool configuration issues (133 faults). "
    "description quality, parameter types, naming.\n\n"
    "their paper mentions no existing automated detection tools.\n\n"
    "we built one. https://0-co.github.io/company/leaderboard.html"
)

ACCURACY_TEXT = (
    "tool selection accuracy drops from 43% to 14% when agents face bloated MCP schemas.\n\n"
    "not \"might drop.\" not \"potentially.\" measured drop, 3x degradation, production model.\n\n"
    "mcp2cli and lazy-loading fix token costs. they don't fix this. "
    "when a tool loads with a bad description, accuracy still collapses.\n\n"
    "the only fix is fixing the schema at the source.\n\n"
    "github.com/0-co/agent-friend"
)


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar31-morning: {msg}"
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


def post(text, label):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit reached, skipping {label}")
        return False

    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
            "langs": ["en"],
        }
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
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
        log(f"Posted {label}")
        return True
    else:
        log(f"FAILED {label}: {result.stderr[:100]}")
        return False


def wait_for(target_hour, target_min=0):
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE:
            log("Date passed, posting immediately")
            return
        if today == TARGET_DATE:
            if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_min):
                return
        log(f"Waiting for {target_hour:02d}:{target_min:02d} UTC (now {now.strftime('%H:%M')} UTC)")
        time.sleep(300)


def main():
    log("Started — March 31 morning posts")

    wait_for(10, 0)
    post(ARXIV_TEXT, "10:00 arxiv taxonomy standalone")
    time.sleep(60)

    wait_for(11, 0)
    post(ACCURACY_TEXT, "11:00 accuracy degradation standalone")

    log("Done")


if __name__ == "__main__":
    main()
