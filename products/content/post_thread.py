#!/usr/bin/env python3
"""
Thread poster — reads a draft file and posts each P-block as a Bluesky thread.

Draft format:
  P1:
  [post text]

  P2:
  [reply text]

  ...

Usage:
  python3 post_thread.py <draft_file>          # post live
  python3 post_thread.py <draft_file> --dry-run # preview only
"""

import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"


def parse_posts(filepath: str) -> list[str]:
    """Extract P1, P2, ... blocks from a thread draft file."""
    with open(filepath) as f:
        content = f.read()

    # Find all Pn: blocks
    parts = re.split(r'\nP\d+:\n', content)
    # Filter out header/metadata (first element before P1)
    posts = []
    for part in parts[1:]:
        text = part.strip()
        if text:
            posts.append(text)
    return posts


def post_bluesky(text: str, root_uri: str = None, root_cid: str = None,
                 parent_uri: str = None, parent_cid: str = None) -> tuple[str, str] | tuple[None, None]:
    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
    }
    if parent_uri and parent_cid:
        rec["reply"] = {
            "root": {"uri": root_uri, "cid": root_cid},
            "parent": {"uri": parent_uri, "cid": parent_cid},
        }

    outer = {"repo": OUR_DID, "collection": "app.bsky.feed.post", "record": rec}
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"  FAILED: {result.stderr.strip()[:100]}", file=sys.stderr)
        return None, None
    try:
        d = json.loads(result.stdout)
        return d.get("uri"), d.get("cid")
    except json.JSONDecodeError:
        return None, None


def main():
    if len(sys.argv) < 2:
        print("Usage: post_thread.py <draft_file> [--dry-run]")
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    posts = parse_posts(filepath)
    if not posts:
        print("No posts found in draft file.")
        sys.exit(1)

    print(f"Found {len(posts)} posts in {filepath}")
    for i, p in enumerate(posts, 1):
        print(f"\nP{i} ({len(p)} chars):\n{p[:80]}{'...' if len(p) > 80 else ''}")

    if dry_run:
        print("\n[DRY RUN] Not posting.")
        return

    print("\nPosting...")
    root_uri = root_cid = None
    prev_uri = prev_cid = None

    for i, text in enumerate(posts, 1):
        uri, cid = post_bluesky(text, root_uri, root_cid, prev_uri, prev_cid)
        if not uri:
            print(f"P{i}: FAILED — stopping")
            sys.exit(1)
        print(f"P{i}: {uri}")
        if i == 1:
            root_uri, root_cid = uri, cid
        prev_uri, prev_cid = uri, cid
        if i < len(posts):
            time.sleep(1)

    print(f"\nThread posted: {root_uri}")


if __name__ == "__main__":
    main()
