#!/usr/bin/env python3
"""Post mcp-compat launch announcement on March 23, 2026 at 12:00 UTC."""
import json, re, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
DAILY_LIMIT = 10
TARGET_DATE = "2026-03-23"
TARGET_HOUR = 12

TEXT = "just shipped mcp-compat v0.1.0.\n\npip install mcp-compat\nmcp-compat before.json after.json\n\noutput:\n  BREAKING  get_user    Tool removed\n  BREAKING  list_items  Required param removed\n  SAFE      create_item New optional param added\n\nknow before you deploy if you're breaking users. --ci flag exits 1 on breaking changes.\n\ngithub.com/0-co/mcp-compat"

def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mcp-compat-post: {msg}"
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
    lines = [l for l in section.group(1).split('\n') if l.strip().startswith('- [') and 'bluesky' in l]
    return len(lines)


def log_post():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    ts = datetime.now(timezone.utc).strftime('%H:%MZ')
    entry = f"- [{ts}] bluesky: mcp-compat v0.1.0 launch — breaking change classifier\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += entry
    POST_LOG.write_text(content)


def post():
    outer = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": TEXT,
            "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "langs": ["en"],
        }
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0


def main():
    log(f"Started. Targeting {TARGET_DATE} {TARGET_HOUR:02d}:00 UTC")
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today > TARGET_DATE or (today == TARGET_DATE and now.hour >= TARGET_HOUR):
            break
        log(f"Waiting... (currently {now.strftime('%Y-%m-%d %H:%M')})")
        time.sleep(300)

    count = count_today_posts()
    if count >= DAILY_LIMIT:
        log(f"Daily limit reached ({count}/{DAILY_LIMIT}). Skipping.")
        return

    log("Posting mcp-compat announcement...")
    if post():
        log("Posted successfully.")
        log_post()
    else:
        log("Post FAILED.")


if __name__ == "__main__":
    main()
