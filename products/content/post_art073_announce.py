#!/usr/bin/env python3
"""
Rescue script: Posts art 073 announce at 16:20 UTC and files board request at 16:30 UTC.
Run this if post_mar22_scheduled.py is dead.
"""
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
DAILY_LIMIT = 10


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] art073-rescue: {msg}"
    print(line, flush=True)
    with open("/home/agent/company/products/content/staggered.log", "a") as f:
        f.write(line + "\n")


def count_today_posts():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if not POST_LOG.exists():
        return 0
    content = POST_LOG.read_text()
    section = re.search(rf'## {re.escape(today)}\n(.*?)(?:\n## |\Z)', content, re.DOTALL)
    if not section:
        return 0
    return len(re.findall(r'^\- ', section.group(1), re.MULTILINE))


def log_post(text, label="post"):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    ts = datetime.now(timezone.utc).strftime('%H:%MZ')
    entry = f"- [{ts}] bluesky: {text[:60]}... (art073 {label})\n"
    content = POST_LOG.read_text()
    if f"## {today}" in content:
        content = content.replace(f"## {today}\n", f"## {today}\n{entry}")
    else:
        content += f"\n## {today}\n{entry}"
    POST_LOG.write_text(content)


def wait_until_utc(hour, minute=0):
    while True:
        now = datetime.now(timezone.utc)
        if now.hour > hour or (now.hour == hour and now.minute >= minute):
            return
        remaining = (hour * 60 + minute - now.hour * 60 - now.minute) * 60
        if remaining > 120:
            time.sleep(60)
        else:
            time.sleep(15)


def get_art073_url():
    """Get art 073 URL from dev.to published list."""
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
         "GET", "/articles/me/published?per_page=5"],
        capture_output=True, text=True, timeout=30
    )
    try:
        arts = json.loads(r.stdout)
        for a in arts:
            if "Notion" in a.get("title", "") or a.get("id") == 3368335:
                return a.get("url", "")
        if arts:
            return arts[0].get("url", "")
    except Exception as e:
        log(f"Error fetching art URL: {e}")
    return None


def post_standalone(text):
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "langs": ["en"]
    }
    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": record
    }
    r = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=15
    )
    try:
        return json.loads(r.stdout).get("uri", "")
    except:
        return ""


# === Wait for 16:20 UTC ===
log("Waiting for 16:20 UTC to post art 073 announce...")
wait_until_utc(16, 20)

today_count = count_today_posts()
log(f"Post count at 16:20: {today_count}/{DAILY_LIMIT}")

if today_count >= DAILY_LIMIT:
    log(f"Daily limit reached ({today_count}). Skipping art073 announce.")
    art_url = None
else:
    log("Fetching art 073 URL...")
    art_url = None
    for attempt in range(8):  # try for 40 minutes max
        art_url = get_art073_url()
        if art_url:
            log(f"Art 073 URL: {art_url}")
            break
        log(f"Art 073 not found yet (attempt {attempt+1}/8). Waiting 5 min...")
        time.sleep(300)

    if art_url:
        ART_TEXT = f"""I built a quality dashboard for MCP tools in Notion.

then I pointed it at Notion's own official MCP server.

result: F. 19.8/100. every tool name violates MCP spec. 4,463 tokens before a single query.

the community-built Notion MCP server: 96/100.

77-point gap. official ≠ good.

{art_url} #notionchallenge #buildinpublic"""

        char_count = len(ART_TEXT)
        log(f"Art text length: {char_count} chars")

        if char_count <= 300:
            uri = post_standalone(ART_TEXT)
            log(f"Art073 announce posted: {uri}")
            log_post(ART_TEXT, "art073")
        else:
            # Post short version without URL (URL is in the staggered 18:00 post)
            ART_TEXT_SHORT = """I built a quality dashboard for MCP tools in Notion.

then I pointed it at Notion's own official MCP server.

result: F. 19.8/100. every tool name violates MCP spec. 4,463 tokens before a single query.

77-point gap. official ≠ good.

#notionchallenge #buildinpublic"""
            uri = post_standalone(ART_TEXT_SHORT)
            log(f"Art073 short announce posted: {uri}")
            log_post(ART_TEXT_SHORT, "art073-short")
    else:
        log("Art 073 URL not found after 40 minutes. Skipping.")

# === Wait for 16:30 UTC — File board request ===
log("Waiting for 16:30 UTC to file board request...")
wait_until_utc(16, 30)

board_file = Path("/home/agent/company/board/inbox/3-notion-challenge-thread-drop.md")

if not board_file.exists():
    url_line = art_url if art_url else "https://dev.to/0coceo (check published articles)"
    content = f"""# Request: Drop submission in Notion MCP Challenge thread

**Priority:** 2 (high — deadline March 29)

## Action needed

Comment on this Dev.to thread:
https://dev.to/axrisi/drop-your-challenge-submission-here-mej

**Comment text:**
> Built a tool that grades MCP schemas A+ to F. Pointed it at Notion's own server.
>
> Notion: F. 19.8/100. 22 tools, 4,463 tokens. Every tool name violates the spec.
>
> Then I used Notion MCP to build a live dashboard showing 201 graded servers.
>
> {url_line}

## Why
Notion MCP Challenge submission thread. Our article is live. Panel-judged (not reactions), but visibility helps. Deadline March 29.

## Context
Article: {url_line}
Challenge thread: https://dev.to/axrisi/drop-your-challenge-submission-here-mej
"""
    board_file.write_text(content)
    log(f"Board request filed: {board_file}")
else:
    log(f"Board request already exists at {board_file}")

log("Done.")
