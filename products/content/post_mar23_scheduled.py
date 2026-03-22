#!/usr/bin/env python3
"""Scheduled standalone posts for March 23, 2026.

Posts:
  11:00 UTC — bsky_mar23_fetch_override.md (prompt injection in fetch server)
  14:00 UTC — bsky_mar23_schema_lint_take.md (schema lint irony)
"""
import json, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
DAILY_LIMIT = 10
CONTENT_DIR = Path("/home/agent/company/products/content")
TARGET_DATE = "2026-03-23"


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] {msg}"
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


def wait_until_date(target):
    while True:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        if today >= target:
            return
        log(f"Waiting for date {target} (currently {today})...")
        time.sleep(300)


def wait_until_utc(hour, minute=0):
    while True:
        now = datetime.now(timezone.utc)
        if now.hour > hour or (now.hour == hour and now.minute >= minute):
            return
        remaining = (hour * 60 + minute - now.hour * 60 - now.minute) * 60
        if remaining > 300:
            time.sleep(300)
        else:
            time.sleep(30)


def extract_post_text(filepath):
    """Extract text from a bsky post file (strip frontmatter and metadata lines)."""
    content = Path(filepath).read_text()
    lines = content.split('\n')
    # Strip YAML frontmatter
    if lines[0].strip() == '---':
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == '---'), None)
        if end:
            lines = lines[end+1:]
    # Strip trailing metadata lines (Graphemes: N, Note: ...)
    text_lines = []
    for line in lines:
        if re.match(r'^(Graphemes:|Note:)', line.strip()):
            break
        text_lines.append(line)
    return '\n'.join(text_lines).strip()


def build_facets(text):
    facets = []
    cache = {}
    def resolve(h):
        if h in cache: return cache[h]
        r = subprocess.run(["sudo", "-u", "vault", VAULT_BSKY,
            "com.atproto.identity.resolveHandle", json.dumps({"handle": h})],
            capture_output=True, text=True, timeout=10)
        try:
            d = json.loads(r.stdout).get("did")
            if d: cache[h] = d
            return d
        except: return None
    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        did = resolve(m.group(1))
        if did:
            facets.append({"index": {"byteStart": len(text[:m.start()].encode()),
                "byteEnd": len(text[:m.end()].encode())},
                "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]})
    for m in re.finditer(r'https?://[^\s]+', text):
        facets.append({"index": {"byteStart": len(text[:m.start()].encode()),
            "byteEnd": len(text[:m.end()].encode())},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}]})
    return facets


def post_standalone(text):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    facets = build_facets(text)
    record = {"$type": "app.bsky.feed.post", "text": text, "createdAt": now}
    if facets:
        record["facets"] = facets
    outer = {"collection": "app.bsky.feed.post", "repo": OUR_DID, "record": record}
    r = subprocess.run(["sudo", "-u", "vault", VAULT_BSKY,
        "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        return json.loads(r.stdout).get("uri", "?")
    raise Exception(f"Failed: {r.stderr}")


def log_post(text):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    t = datetime.now(timezone.utc).strftime('%H:%M')
    line = f"- {t} UTC bluesky: {text[:60]}...\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += line
    POST_LOG.write_text(content)


# Wait until March 23
log("post_mar23_scheduled.py started. Waiting for March 23...")
wait_until_date(TARGET_DATE)
log("March 23 reached.")

# === 11:00 UTC — bsky_mar23_fetch_override.md ===
log("Waiting for 11:00 UTC...")
wait_until_utc(11, 0)

today_count = count_today_posts()
if today_count >= DAILY_LIMIT:
    log(f"Daily limit ({today_count}). Skipping fetch_override post.")
else:
    fetch_file = CONTENT_DIR / "bsky_mar23_fetch_override.md"
    if fetch_file.exists():
        text = extract_post_text(fetch_file)
        log(f"Posting fetch_override ({len(text)} chars): {text[:60]}...")
        uri = post_standalone(text)
        log(f"fetch_override posted: {uri}")
        log_post(text)
    else:
        log(f"File not found: {fetch_file}")

# === 14:00 UTC — bsky_mar23_schema_lint_take.md ===
log("Waiting for 14:00 UTC...")
wait_until_utc(14, 0)

today_count = count_today_posts()
if today_count >= DAILY_LIMIT:
    log(f"Daily limit ({today_count}). Skipping schema_lint_take post.")
else:
    lint_file = CONTENT_DIR / "bsky_mar23_schema_lint_take.md"
    if lint_file.exists():
        text = extract_post_text(lint_file)
        log(f"Posting schema_lint_take ({len(text)} chars): {text[:60]}...")
        uri = post_standalone(text)
        log(f"schema_lint_take posted: {uri}")
        log_post(text)
    else:
        log(f"File not found: {lint_file}")

log("post_mar23_scheduled.py completed.")
