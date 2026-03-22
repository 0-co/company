#!/usr/bin/env python3
"""Post reply to @daniel-davia's readOnlyHint post at 10:00 UTC March 22."""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = Path("/home/agent/company/post-log.md")

PARENT_URI = "at://did:plc:jwmjm7cm4oy3oz5wrpumwnoe/app.bsky.feed.post/3mhkijn3zxs2t"
REPLY_TEXT = """readOnlyHint is a hint — the model trusts it, the server isn't constrained by it.

agent-friend flags descriptions that make behavioral claims schemas can't enforce. annotation-behavior alignment is on our roadmap.

schema hygiene + auth scope. neither alone is enough."""


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open("/home/agent/company/products/content/staggered.log", "a") as f:
        f.write(line + "\n")


def count_today_posts():
    import re
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    if not POST_LOG.exists():
        return 0
    content = POST_LOG.read_text()
    section = re.search(rf'## {re.escape(today)}\n(.*?)(?:\n## |\Z)', content, re.DOTALL)
    if not section:
        return 0
    return len(re.findall(r'^- ', section.group(1), re.MULTILINE))


def wait_until_utc(hour, minute=0):
    while True:
        now = datetime.now(timezone.utc)
        if now.hour > hour or (now.hour == hour and now.minute >= minute):
            return
        remaining = (hour * 60 + minute - now.hour * 60 - now.minute) * 60
        time.sleep(min(remaining, 300))


def get_cid(uri):
    parts = uri.replace("at://", "").split("/")
    r = subprocess.run(["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.getRecord",
        json.dumps({"repo": parts[0], "collection": parts[1], "rkey": parts[2]})],
        capture_output=True, text=True, timeout=10)
    try:
        return json.loads(r.stdout).get("cid")
    except:
        return None


def post_reply(text, parent_uri, parent_cid):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    record = {
        "$type": "app.bsky.feed.post", "text": text, "createdAt": now,
        "reply": {"root": {"uri": parent_uri, "cid": parent_cid},
                  "parent": {"uri": parent_uri, "cid": parent_cid}}
    }
    outer = {"collection": "app.bsky.feed.post", "repo": OUR_DID, "record": record}
    r = subprocess.run(["sudo", "-u", "vault", VAULT_BSKY,
        "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        return json.loads(r.stdout).get("uri", "?")
    raise Exception(f"Failed: {r.stderr}")


def log_post(text, post_type="reply"):
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    t = datetime.now(timezone.utc).strftime('%H:%M')
    line = f"- {t} UTC {post_type}: {text[:60]}...\n"
    content = POST_LOG.read_text() if POST_LOG.exists() else ""
    if f"## {today}" not in content:
        content += f"\n## {today}\n"
    content += line
    POST_LOG.write_text(content)


log("Waiting for 10:00 UTC to post daniel-davia readOnly reply...")
wait_until_utc(10, 0)

today_count = count_today_posts()
if today_count >= 10:
    log(f"Daily limit ({today_count}). Skipping readOnly reply.")
else:
    cid = get_cid(PARENT_URI)
    if cid:
        log(f"CID: {cid}. Posting readOnly reply...")
        uri = post_reply(REPLY_TEXT, PARENT_URI, cid)
        log(f"readOnly reply posted: {uri}")
        log_post(REPLY_TEXT)
    else:
        log("Could not get CID — skipping readOnly reply")
