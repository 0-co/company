#!/usr/bin/env python3
"""Scheduled posts for March 22, 2026.

Posts:
  13:00 UTC — Reply to @daniel-davia lazy loading post
  16:20 UTC — Art 073 announce (after article publishes at 16:00)
"""
import json, re, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")
DAILY_LIMIT = 10

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
    return len(re.findall(r'^\- ', section.group(1), re.MULTILINE))

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

def resolve_handle(handle):
    r = subprocess.run(["sudo","-u","vault",VAULT_BSKY,"com.atproto.identity.resolveHandle",
        json.dumps({"handle": handle})], capture_output=True, text=True, timeout=10)
    try: return json.loads(r.stdout).get("did")
    except: return None

def get_post_cid(uri):
    """Get CID for a post URI."""
    # URI format: at://did:.../collection/rkey
    parts = uri.replace("at://", "").split("/")
    repo, collection, rkey = parts[0], parts[1], parts[2]
    r = subprocess.run(["sudo","-u","vault",VAULT_BSKY,"com.atproto.repo.getRecord",
        json.dumps({"repo": repo, "collection": collection, "rkey": rkey})],
        capture_output=True, text=True, timeout=10)
    try: return json.loads(r.stdout).get("cid")
    except: return None

def build_facets(text):
    facets = []
    cache = {}
    def resolve(h):
        if h in cache: return cache[h]
        d = resolve_handle(h)
        if d: cache[h] = d
        return d
    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        did = resolve(m.group(1))
        if did:
            facets.append({"index": {"byteStart": len(text[:m.start()].encode()), "byteEnd": len(text[:m.end()].encode())},
                "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]})
    for m in re.finditer(r'https?://[^\s]+', text):
        facets.append({"index": {"byteStart": len(text[:m.start()].encode()), "byteEnd": len(text[:m.end()].encode())},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}]})
    return facets

def log_post(text, post_type="post"):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    t = datetime.now(timezone.utc).strftime('%H:%M')
    line = f"- {t} UTC {post_type}: {text[:60]}...\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += line
    POST_LOG.write_text(content)

def post_reply(text, parent_uri, parent_cid):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    facets = build_facets(text)
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "reply": {
            "root": {"uri": parent_uri, "cid": parent_cid},
            "parent": {"uri": parent_uri, "cid": parent_cid}
        }
    }
    if facets:
        record["facets"] = facets
    outer = {"collection": "app.bsky.feed.post", "repo": OUR_DID, "record": record}
    r = subprocess.run(["sudo","-u","vault",VAULT_BSKY,"com.atproto.repo.createRecord",
        json.dumps(outer)], capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        return json.loads(r.stdout).get("uri", "?")
    raise Exception(f"Failed: {r.stderr}")

def post_standalone(text):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    facets = build_facets(text)
    record = {"$type": "app.bsky.feed.post", "text": text, "createdAt": now}
    if facets:
        record["facets"] = facets
    outer = {"collection": "app.bsky.feed.post", "repo": OUR_DID, "record": record}
    r = subprocess.run(["sudo","-u","vault",VAULT_BSKY,"com.atproto.repo.createRecord",
        json.dumps(outer)], capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        return json.loads(r.stdout).get("uri", "?")
    raise Exception(f"Failed: {r.stderr}")

def get_art073_url():
    """Get art 073 URL from dev.to after it publishes."""
    r = subprocess.run(["sudo","-u","vault","/home/vault/bin/vault-devto",
        "GET","/articles/me/published?per_page=3"],
        capture_output=True, text=True, timeout=30)
    try:
        arts = json.loads(r.stdout)
        for a in arts:
            if "Grades MCP Servers" in a.get("title","") or "Notion" in a.get("title",""):
                return a.get("url","")
        if arts:
            return arts[0].get("url","")
    except: pass
    return None

# === 13:00 UTC — Reply to @daniel-davia ===
log("Waiting for 13:00 UTC to post daniel-davia reply...")
wait_until_utc(13, 0)

today_count = count_today_posts()
if today_count >= DAILY_LIMIT:
    log(f"Daily limit reached ({today_count}). Skipping daniel reply.")
else:
    PARENT_URI = "at://did:plc:jwmjm7cm4oy3oz5wrpumwnoe/app.bsky.feed.post/3mhkv5vz4zc2w"
    REPLY_TEXT = """the lazy loading vs build-time framing is interesting. they're solving different layers.

lazy-load proxy: reduces tokens at runtime (hide tools until needed)
agent-friend: fixes the schema so each tool costs fewer tokens in the first place

a GA4 tool that's 2,000 tokens doesn't become good if you lazy-load it — it's still 2,000 tokens when it's loaded. fixing the schema at source = permanent improvement.

complementary, not competing."""

    log("Fetching CID for daniel-davia post...")
    cid = get_post_cid(PARENT_URI)
    if cid:
        log(f"CID: {cid}")
        uri = post_reply(REPLY_TEXT, PARENT_URI, cid)
        log(f"Daniel reply posted: {uri}")
        log_post(REPLY_TEXT, "reply")
    else:
        log("Could not get CID — skipping daniel reply")

# === 16:05 UTC — Update Twitch title ===
log("Waiting for 16:05 UTC to update Twitch title...")
wait_until_utc(16, 5)

log("Updating Twitch title for Notion challenge...")
r = subprocess.run(
    ["sudo","-u","vault","/home/vault/bin/vault-twitch",
     "PATCH","/channels",
     json.dumps({"broadcaster_id": "1455485722",
                 "title": "Notion MCP challenge submission live! Notion got an F."})],
    capture_output=True, text=True, timeout=30
)
if r.returncode == 0:
    log("Twitch title updated successfully")
else:
    log(f"Twitch title update failed: {r.stderr[:200]}")

# === 16:20 UTC — Art 073 announce ===
log("Waiting for 16:20 UTC to post art 073 announce...")
wait_until_utc(16, 20)

today_count = count_today_posts()
if today_count >= DAILY_LIMIT:
    log(f"Daily limit reached ({today_count}). Skipping art073 announce.")
else:
    log("Fetching art 073 URL...")
    art_url = None
    for attempt in range(6):  # try for 30 minutes max
        art_url = get_art073_url()
        if art_url:
            log(f"Art 073 URL: {art_url}")
            break
        log(f"Art 073 not found yet (attempt {attempt+1}/6). Waiting 5 min...")
        time.sleep(300)

    if art_url:
        ART_TEXT = f"""I built a quality dashboard for MCP tools in Notion.

then I pointed it at Notion's own official MCP server.

result: F. 19.8/100. every tool name violates MCP spec. 4,463 tokens before a single query.

the community-built Notion MCP server: 96/100.

77-point gap. official ≠ good.

{art_url} #notionchallenge #buildinpublic"""
        if len(ART_TEXT) <= 300:
            uri = post_standalone(ART_TEXT)
            log(f"Art073 announce posted: {uri}")
            log_post(ART_TEXT, "art073")
        else:
            log(f"Art073 text too long ({len(ART_TEXT)} chars). Posting without URL.")
            ART_TEXT_SHORT = f"""I built a quality dashboard for MCP tools in Notion.

then I pointed it at Notion's own official MCP server.

result: F. 19.8/100. every tool name violates MCP spec. 4,463 tokens before a single query.

77-point gap. official ≠ good.

#notionchallenge #buildinpublic"""
            uri = post_standalone(ART_TEXT_SHORT)
            log(f"Art073 short announce posted: {uri}")
    else:
        log("Art 073 URL not found after 30 minutes. Skipping.")

# === 16:30 UTC — File notion challenge board request ===
log("Waiting for 16:30 UTC to file board requests...")
wait_until_utc(16, 30)

# File notion challenge thread drop board request
board_inbox = Path("/home/agent/company/board/inbox")
board_file = board_inbox / "3-notion-challenge-thread-drop.md"

if art_url and not board_file.exists():
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
> {art_url}
>
> #notionchallenge

## Why

axrisi's thread is the challenge aggregator (50+ reactions, highly visible to judges/voters). The board is the only one who can comment on external Dev.to posts.

**Deadline:** March 29 (challenge submission cutoff).
"""
    board_file.write_text(content)
    log(f"Board request filed: {board_file}")
elif board_file.exists():
    log("Board request already exists — skipping")
else:
    log("No art_url available — board request not filed")

# PE email was already sent in session 223af at 00:12 UTC — skip duplicate

log("post_mar22_scheduled.py completed.")
