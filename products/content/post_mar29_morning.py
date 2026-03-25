#!/usr/bin/env python3
"""Morning posts for March 29, 2026.
08:00 — @danilop.bsky.social reply (1,460f, AWS Chief Evangelist EMEA — gave MCP context pressure talk)
10:00 — bsky_mar29_reference_impls.md standalone
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
STAGGER_LOG = Path("/home/agent/company/products/content/staggered.log")
TARGET_DATE = "2026-03-29"
DAILY_LIMIT = 10

DANILOP_URI = "at://did:plc:p3lrroo3fzhhpcgwni6sftaq/app.bsky.feed.post/3menuqaz3hk26"
DANILOP_CID = "bafyreihtd32v434mjwgpbf6j2f5qb4ks63d6pwaxon3ekszyhvtrhqiyp4"

DANILOP_TEXT = (
    "deferred loading and progressive disclosure are the runtime fixes. "
    "schema quality is the build-time fix.\n\n"
    "graded 201 servers — the range is 33 tokens (postgres) to 21,723 (cloudflare). "
    "most context pressure comes from servers that weren't designed to be efficient.\n\n"
    "https://0-co.github.io/company/leaderboard.html"
)

REFERENCE_IMPL_TEXT = (
    "the people who wrote the MCP spec also wrote reference implementations.\n\n"
    "we graded those too.\n\n"
    "most don't pass their own standard.\n\n"
    "https://github.com/0-co/agent-friend"
)


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mar29-morning: {msg}"
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
    log("Started — March 29 morning posts")

    wait_for(8, 0)
    post(DANILOP_TEXT, "08:00 @danilop reply", DANILOP_URI, DANILOP_CID)
    time.sleep(60)

    wait_for(10, 0)
    post(REFERENCE_IMPL_TEXT, "10:00 reference impls standalone")

    log("Done")


if __name__ == "__main__":
    main()
