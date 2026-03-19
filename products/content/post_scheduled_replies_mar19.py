#!/usr/bin/env python3
"""
Scheduled Bluesky reply poster for March 19, 2026.

Posts 4 replies at scheduled times:
  10:00 UTC — @daniel-davia_2 (safe-mcp.com thread)
  13:00 UTC — @ai-nerd (Colab MCP)
  17:00 UTC — @joozio (context drift)
  19:00 UTC — @aroussi.com (token budget)

Checks daily reply limit (max 4/day) before each post.
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
POST_LOG = "/home/agent/company/post-log.md"
MAX_REPLIES_PER_DAY = 4

# Schedule: (hour, minute, draft_file)
SCHEDULE = [
    (10, 0, "/home/agent/company/drafts/bsky_reply_mar19_daniel_davia_2.md"),
    (13, 0, "/home/agent/company/drafts/bsky_reply_mar19_ainerd_colab.md"),
    (17, 0, "/home/agent/company/drafts/bsky_reply_mar19_joozio.md"),
    (19, 0, "/home/agent/company/drafts/bsky_reply_mar19_aroussi.md"),
]


def parse_draft(filepath: str) -> dict:
    """Parse a reply draft file to extract URIs, CIDs, and text."""
    with open(filepath) as f:
        content = f.read()

    result = {}

    # Extract Reply to URI
    m = re.search(r'- Reply to URI:\s*(at://\S+)', content)
    result['parent_uri'] = m.group(1) if m else None

    # Extract Reply to CID
    m = re.search(r'- Reply to CID:\s*(\S+)', content)
    result['parent_cid'] = m.group(1) if m else None

    # Extract Root URI
    m = re.search(r'- Root URI(?:\s*\(same[^)]*\))?:\s*(at://\S+)', content)
    result['root_uri'] = m.group(1) if m else result.get('parent_uri')

    # Extract Root CID
    m = re.search(r'- Root CID(?:\s*\(same[^)]*\))?:\s*(\S+)', content)
    result['root_cid'] = m.group(1) if m else result.get('parent_cid')

    # Extract draft text (after "## Draft Reply" or "## Draft reply" section)
    m = re.search(r'## Draft [Rr]eply.*?\n(.*?)(?:\n##|\Z)', content, re.DOTALL)
    if m:
        text = m.group(1).strip()
        # Remove any trailing "## Notes" etc
        text = re.split(r'\n##\s+', text)[0].strip()
        result['text'] = text
    else:
        result['text'] = None

    return result


def count_today_replies() -> int:
    """Count today's reply posts from post-log.md."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    try:
        with open(POST_LOG) as f:
            content = f.read()
    except FileNotFoundError:
        return 0

    # Find today's section
    m = re.search(rf'## {re.escape(today)}\n(.*?)(?:\n## |\Z)', content, re.DOTALL)
    if not m:
        return 0

    today_section = m.group(1)
    replies = re.findall(r'bluesky reply:', today_section)
    return len(replies)


def log_post(target: str, text_preview: str):
    """Append to post-log.md."""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    now = datetime.now(timezone.utc).strftime('%H:%MZ')

    try:
        with open(POST_LOG) as f:
            content = f.read()
    except FileNotFoundError:
        content = ""

    entry = f'- [{now}] bluesky reply: {target} — "{text_preview[:60]}"\n'

    if f'## {today}' in content:
        content = content.replace(f'## {today}\n', f'## {today}\n{entry}')
    else:
        content = f'## {today}\n{entry}\n' + content

    with open(POST_LOG, 'w') as f:
        f.write(content)


def build_facets(text: str) -> list:
    """Build Bluesky facets for @mentions and URLs in text."""
    facets = []
    text_bytes = text.encode("utf-8")

    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        handle = m.group(1)
        byte_start = len(text[:m.start()].encode('utf-8'))
        byte_end = len(text[:m.end()].encode('utf-8'))
        result = subprocess.run(
            ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.identity.resolveHandle",
             json.dumps({"handle": handle})],
            capture_output=True, text=True, timeout=10
        )
        try:
            d = json.loads(result.stdout)
            did = d.get("did")
            if did:
                facets.append({"index": {"byteStart": byte_start, "byteEnd": byte_end},
                               "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]})
        except (json.JSONDecodeError, KeyError):
            pass

    for m in re.finditer(r'https?://[^\s)]+', text):
        byte_start = len(text[:m.start()].encode('utf-8'))
        byte_end = len(text[:m.end()].encode('utf-8'))
        facets.append({"index": {"byteStart": byte_start, "byteEnd": byte_end},
                       "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group(0)}]})

    return facets


def post_reply(text: str, parent_uri: str, parent_cid: str,
               root_uri: str, root_cid: str) -> bool:
    """Post a reply to Bluesky."""
    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
        "reply": {
            "root": {"uri": root_uri, "cid": root_cid},
            "parent": {"uri": parent_uri, "cid": parent_cid},
        }
    }
    facets = build_facets(text)
    if facets:
        rec["facets"] = facets

    outer = {"repo": OUR_DID, "collection": "app.bsky.feed.post", "record": rec}
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr.strip()[:200]}", flush=True)
        return False
    try:
        d = json.loads(result.stdout)
        uri = d.get("uri", "no-uri")
        print(f"  Posted: {uri}", flush=True)
        return True
    except json.JSONDecodeError:
        print(f"  Response: {result.stdout[:200]}", flush=True)
        return True


def main():
    today = datetime.now(timezone.utc)
    target_date = "2026-03-19"
    today_str = today.strftime('%Y-%m-%d')

    if today_str != target_date:
        print(f"Script is for {target_date}, but today is {today_str}. Exiting.")
        sys.exit(1)

    print(f"Scheduled reply poster starting. Today: {today_str}", flush=True)
    print(f"Schedule: {len(SCHEDULE)} replies planned", flush=True)

    for sched_hour, sched_min, draft_file in SCHEDULE:
        now_utc = datetime.now(timezone.utc)
        target = now_utc.replace(hour=sched_hour, minute=sched_min, second=0, microsecond=0)

        # If target already passed, skip (or post immediately if within 30min window)
        elapsed = (now_utc - target).total_seconds()
        if elapsed > 1800:  # more than 30min past scheduled time
            print(f"Skipping {sched_hour:02d}:{sched_min:02d} UTC (already {elapsed/60:.0f} min past)", flush=True)
            continue

        # Wait until target time
        wait_secs = max(0, (target - now_utc).total_seconds())
        if wait_secs > 0:
            print(f"Waiting {wait_secs/3600:.1f}h for {sched_hour:02d}:{sched_min:02d} UTC reply...", flush=True)
            time.sleep(wait_secs)

        # Check daily reply limit
        reply_count = count_today_replies()
        if reply_count >= MAX_REPLIES_PER_DAY:
            print(f"Daily reply limit reached ({reply_count}/{MAX_REPLIES_PER_DAY}). Stopping.", flush=True)
            break

        # Parse draft
        draft = parse_draft(draft_file)
        if not all([draft.get('text'), draft.get('parent_uri'), draft.get('parent_cid'),
                    draft.get('root_uri'), draft.get('root_cid')]):
            print(f"Invalid draft at {draft_file}: {draft}", flush=True)
            continue

        text = draft['text']
        char_count = len(text)
        if char_count > 300:
            print(f"WARNING: Text is {char_count} chars (>300). Truncating.", flush=True)
            text = text[:297] + "..."

        print(f"\n[{datetime.now(timezone.utc).strftime('%H:%MZ')}] Posting reply {reply_count+1}/{MAX_REPLIES_PER_DAY}", flush=True)
        print(f"  Draft: {draft_file.split('/')[-1]}", flush=True)
        print(f"  Text ({char_count} chars): {text[:80]}...", flush=True)

        success = post_reply(text, draft['parent_uri'], draft['parent_cid'],
                             draft['root_uri'], draft['root_cid'])

        if success:
            # Extract target handle from filename
            handle = draft_file.split('bsky_reply_mar19_')[-1].replace('.md', '').replace('_', '.')
            log_post(f"@{handle}", text)
            print(f"  Logged. Reply count now: {reply_count+1}", flush=True)
        else:
            print(f"  Failed to post. Continuing.", flush=True)

    print("\nScheduled reply poster complete.", flush=True)


if __name__ == '__main__':
    main()
