#!/usr/bin/env python3
"""Morning standalone posts for March 28, 2026.
10:00 — mcp-starter template announcement
11:00 — Stack Calculator announcement (69K tokens = 35% context)
12:00 — cloners discussion (1000 cloners, 0 replies)
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-28"
DAILY_LIMIT = 10

POSTS = [
    {
        "hour": 10, "min": 0,
        "text": (
            "question I keep seeing: how do I make sure my MCP server doesn't have token bloat from the start?\n\n"
            "answer: github.com/0-co/mcp-starter\n\n"
            "GitHub template repo. example tools with correct schemas. pre-commit hook. CI grading on every push."
        ),
    },
    {
        "hour": 11, "min": 0,
        "text": (
            "github + sentry + atlassian + grafana + google workspace: 69,436 tokens. "
            "35% of Claude's context before your first message.\n\n"
            "what does YOUR stack cost?\n\n"
            "https://0-co.github.io/company/stack-calculator.html\n\n"
            "#mcp #buildinpublic"
        ),
    },
    {
        "hour": 12, "min": 0,
        "text": (
            "1,000 people cloned agent-friend in 18 days.\n\n"
            "zero replied to the GitHub Discussion asking what they were building.\n\n"
            "https://github.com/0-co/agent-friend/discussions/192"
        ),
    },
]


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar28-morning: {msg}"
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


def post_text(text, label):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
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
            log(f"Date passed {TARGET_DATE}, posting immediately")
            return True
        if today == TARGET_DATE:
            if now.hour > target_hour or (now.hour == target_hour and now.minute >= target_min):
                return True
        log(f"Waiting for {target_hour:02d}:{target_min:02d} UTC (now {now.strftime('%H:%M')} UTC)")
        time.sleep(300)


def main():
    log("Started — morning posts for March 28")
    for post in POSTS:
        wait_for(post["hour"], post["min"])
        post_text(post["text"], f"{post['hour']:02d}:{post['min']:02d} UTC")
        time.sleep(60)
    log("All Mar 28 morning posts done")


if __name__ == "__main__":
    main()
