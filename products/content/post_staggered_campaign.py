#!/usr/bin/env python3
"""Post staggered Bluesky campaign messages.

Reads posts from a JSON file and posts them at intervals.
Designed to be called once — posts one message and exits.
Schedule multiple calls via systemd-run for staggered timing.

Usage: python3 post_staggered_campaign.py <post_number> <json_file>
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

POST_LOG = Path("/home/agent/company/post-log.md")
DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
_handle_cache: dict = {}


def _resolve_handle(handle: str) -> str | None:
    if handle in _handle_cache:
        return _handle_cache[handle]
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.identity.resolveHandle",
         json.dumps({"handle": handle})],
        capture_output=True, text=True, timeout=10
    )
    try:
        did = json.loads(result.stdout).get("did")
        if did:
            _handle_cache[handle] = did
        return did
    except Exception:
        return None


def build_facets(text: str) -> list:
    """Build Bluesky facets for @mentions and URLs so links are clickable."""
    facets = []
    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        did = _resolve_handle(m.group(1))
        if not did:
            continue
        facets.append({
            "index": {
                "byteStart": len(text[:m.start()].encode("utf-8")),
                "byteEnd": len(text[:m.end()].encode("utf-8")),
            },
            "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]
        })
    for m in re.finditer(r'https?://[^\s]+', text):
        facets.append({
            "index": {
                "byteStart": len(text[:m.start()].encode("utf-8")),
                "byteEnd": len(text[:m.end()].encode("utf-8")),
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}]
        })
    return facets


def count_today_posts():
    """Count Bluesky posts in today's post log."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_header = f"## {today}"
    count = 0
    in_today = False
    if POST_LOG.exists():
        for line in POST_LOG.read_text().splitlines():
            if line.strip() == today_header:
                in_today = True
                continue
            if line.startswith("## 2") and in_today:
                break
            if in_today and "bluesky:" in line.lower() and "reply" not in line.lower() and "[draft" not in line.lower() and "[saved" not in line.lower():
                count += 1
    return count


def post_to_bluesky(text):
    """Post to Bluesky via vault-bsky."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": now,
        "langs": ["en"],
    }
    facets = build_facets(text)
    if facets:
        rec["facets"] = facets
    record = {"repo": DID, "collection": "app.bsky.feed.post", "record": rec}
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY,
         "com.atproto.repo.createRecord", json.dumps(record)],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout[:200]


def log_post(text):
    """Log post to post-log.md."""
    ts = datetime.now(timezone.utc).strftime("%H:%MZ")
    snippet = text[:60].replace("\n", " ")
    entry = f"- [{ts}] bluesky: \"{snippet}\"\n"
    with open(POST_LOG, "r") as f:
        content = f.read()
    # Find today's section and append
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_header = f"## {today}"
    if today_header in content:
        idx = content.index(today_header) + len(today_header) + 1
        content = content[:idx] + entry + content[idx:]
    else:
        # Add today's section at top (after header)
        lines = content.split("\n", 2)
        content = lines[0] + "\n\n" + today_header + "\n" + entry + "\n" + "\n".join(lines[1:])
    with open(POST_LOG, "w") as f:
        f.write(content)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 post_staggered_campaign.py <post_number> <json_file>")
        sys.exit(1)

    post_num = int(sys.argv[1])
    json_file = Path(sys.argv[2])

    if not json_file.exists():
        print(f"Campaign file not found: {json_file}")
        sys.exit(1)

    with open(json_file) as f:
        posts = json.load(f)

    if post_num < 1 or post_num > len(posts):
        print(f"Post number {post_num} out of range (1-{len(posts)})")
        sys.exit(1)

    # Check daily limit
    today_count = count_today_posts()
    if today_count >= 10:
        print(f"Daily Bluesky post limit reached ({today_count}/10). Skipping.")
        sys.exit(0)

    text = posts[post_num - 1]["text"]
    print(f"Posting ({today_count + 1}/10 today): {text[:60]}...")

    ok, output = post_to_bluesky(text)
    if ok:
        log_post(text)
        print(f"Posted successfully.")
    else:
        print(f"Failed to post: {output}")
        sys.exit(1)


if __name__ == "__main__":
    main()
