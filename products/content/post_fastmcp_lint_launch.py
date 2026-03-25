#!/usr/bin/env python3
"""Post fastmcp-lint launch announcement on March 27 at 12:00 UTC.
Announces the new static analysis tool for FastMCP servers.
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-27"
TARGET_HOUR = 12
VAULT_BSKY = "/home/vault/bin/vault-bsky"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
DAILY_LIMIT = 10

POST_TEXT = """shipped: fastmcp-lint

4/4 FastMCP servers grade F. same root cause: no docstrings → empty descriptions → agents can't select them.

FastMCP handles transport. descriptions are your job.

static AST linter. catches this before deploy.

pip install fastmcp-lint
github.com/0-co/fastmcp-lint"""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] fastmcp-lint-launch: {msg}"
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


def wait_for_target():
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE:
            log(f"Date passed {TARGET_DATE}, posting immediately")
            return
        if today == TARGET_DATE:
            if now.hour >= TARGET_HOUR:
                return
        log(f"Waiting for {TARGET_DATE} {TARGET_HOUR:02d}:00 UTC (now {now.strftime('%Y-%m-%d %H:%M')} UTC)")
        time.sleep(300)


def post():
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit {DAILY_LIMIT} reached. Skipping fastmcp-lint launch post.")
        return False

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
        ts = datetime.now(timezone.utc).strftime('%H:%MZ')
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        entry = f"- [{ts}] bluesky: {POST_TEXT[:60]}...\n"
        content = POST_LOG.read_text() if POST_LOG.exists() else ""
        if f"## {today}" not in content:
            content += f"\n## {today}\n"
        content += entry
        POST_LOG.write_text(content)
        log(f"Posted fastmcp-lint launch announcement")
        return True
    else:
        log(f"FAILED: {result.stderr[:200]}")
        return False


def main():
    log("Started. Waiting for launch time.")
    wait_for_target()
    post()


if __name__ == "__main__":
    main()
