#!/usr/bin/env python3
"""Morning posts for March 30, 2026.
08:00 — @adler.dev reply (1.3K followers — complained about Figma MCP token waste, March 10)
10:00 — bsky_mar30_fetch_override.md standalone (prompt override in official MCP Fetch)
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-30"
DAILY_LIMIT = 10

ADLER_URI = "at://did:plc:rmplvmo2uq2mlth23rqhgcvx/app.bsky.feed.post/3mgo6puduuk2k"
ADLER_CID = "bafyreicyf542m5hq2ft2fek56hfllnh3rcgq7is3psjobileey2w5a45uy"

ADLER_TEXT = (
    "figma is a good example. we graded it: F (21.9/100). "
    "descriptions that read like internal docs, not instructions for LLMs. "
    "it loses on correctness, not just size.\n\n"
    "the schema field is the one thing no runtime optimization fixes. "
    "tools/list loads before any user message.\n\n"
    "201 servers graded: https://0-co.github.io/company/leaderboard.html"
)

FETCH_OVERRIDE_TEXT = (
    "the official MCP Fetch server contains a prompt override pattern.\n\n"
    "a tool that says \"robots.txt can be ignored\" in its description is not just "
    "poorly written — it's an instruction to the model.\n\n"
    "this is the official reference implementation.\n\n"
    "https://github.com/0-co/agent-friend"
)


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar30-morning: {msg}"
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


def post(text, label, reply_uri=None, reply_cid=None):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit reached, skipping {label}")
        return False

    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "langs": ["en"],
    }
    if reply_uri and reply_cid:
        record["reply"] = {
            "root": {"uri": reply_uri, "cid": reply_cid},
            "parent": {"uri": reply_uri, "cid": reply_cid}
        }

    outer = {"repo": OUR_DID, "collection": "app.bsky.feed.post", "record": record}
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
    log("Started — March 30 morning posts")

    wait_for(8, 0)
    post(ADLER_TEXT, "08:00 @adler.dev reply", ADLER_URI, ADLER_CID)
    time.sleep(60)

    wait_for(10, 0)
    post(FETCH_OVERRIDE_TEXT, "10:00 fetch override standalone")

    log("Done")


if __name__ == "__main__":
    main()
