#!/usr/bin/env python3
"""Post mcp-snoop launch announcement on March 23, 2026 at 10:00 UTC."""
import json, re, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
DAILY_LIMIT = 10
TARGET_DATE = "2026-03-23"
TARGET_HOUR = 10


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] mcp-snoop-post: {msg}"
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
    return len(re.findall(r'^- ', section.group(1), re.MULTILINE))


def wait():
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime('%Y-%m-%d')
        if today >= TARGET_DATE and now.hour >= TARGET_HOUR:
            return
        log(f"Waiting... (currently {now.strftime('%Y-%m-%d %H:%M')})")
        time.sleep(300)


def post_text(text):
    facets = []
    for m in re.finditer(r'https?://[^\s]+', text):
        facets.append({"index": {"byteStart": len(text[:m.start()].encode()),
            "byteEnd": len(text[:m.end()].encode())},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}]})
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    record = {"$type": "app.bsky.feed.post", "text": text, "createdAt": now}
    if facets:
        record["facets"] = facets
    outer = {"collection": "app.bsky.feed.post", "repo": OUR_DID, "record": record}
    r = subprocess.run(["sudo", "-u", "vault", VAULT_BSKY,
        "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        raise Exception(f"Failed: {r.stderr}")
    return json.loads(r.stdout).get("uri", "?")


log("Started. Waiting for 2026-03-23 10:00 UTC...")
wait()

count = count_today_posts()
if count >= DAILY_LIMIT:
    log(f"Daily limit reached ({count}). Skipping.")
else:
    text = (
        "you're debugging an MCP server. your agent calls the wrong tool. "
        "you add print statements. restart. still don't know what the client is actually sending.\n\n"
        "built mcp-snoop: transparent stdio proxy that shows every JSON-RPC message.\n\n"
        "pip install mcp-snoop\n"
        "github.com/0-co/mcp-snoop\n\n"
        "#mcp #buildinpublic"
    )
    log(f"Posting ({len(text)} chars)...")
    uri = post_text(text)
    log(f"Posted: {uri}")

    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    t = datetime.now(timezone.utc).strftime('%H:%M')
    line = f"- [{t}Z] bluesky: mcp-snoop launch — built stdio proxy for MCP debugging\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += line
    POST_LOG.write_text(content)

log("Done.")
