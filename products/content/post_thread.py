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

HANDLE_CACHE: dict[str, str] = {}


def resolve_handle(handle: str) -> str | None:
    """Resolve a Bluesky handle to a DID (cached)."""
    if handle in HANDLE_CACHE:
        return HANDLE_CACHE[handle]
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.identity.resolveHandle",
         json.dumps({"handle": handle})],
        capture_output=True, text=True, timeout=10
    )
    try:
        d = json.loads(result.stdout)
        did = d.get("did")
        if did:
            HANDLE_CACHE[handle] = did
        return did
    except (json.JSONDecodeError, KeyError):
        return None


def build_facets(text: str) -> list:
    """Build Bluesky facets for @mentions and URLs in text."""
    facets = []
    text_bytes = text.encode("utf-8")

    # @mentions — match @handle.tld format
    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        handle = m.group(1)
        did = resolve_handle(handle)
        if not did:
            continue
        # Byte positions
        start_char = m.start()
        end_char = m.end()
        byte_start = len(text[:start_char].encode("utf-8"))
        byte_end = len(text[:end_char].encode("utf-8"))
        facets.append({
            "index": {"byteStart": byte_start, "byteEnd": byte_end},
            "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]
        })

    # URLs — turn raw https:// links into clickable facets
    for m in re.finditer(r'https?://[^\s]+', text):
        url = m.group()
        byte_start = len(text[:m.start()].encode("utf-8"))
        byte_end = len(text[:m.end()].encode("utf-8"))
        facets.append({
            "index": {"byteStart": byte_start, "byteEnd": byte_end},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]
        })

    return facets


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
    facets = build_facets(text)
    if facets:
        rec["facets"] = facets
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
    has_overlong = False
    for i, p in enumerate(posts, 1):
        char_count = len(p)
        flag = " ⚠️ OVER 300" if char_count > 300 else ""
        print(f"\nP{i} ({char_count} chars{flag}):\n{p[:80]}{'...' if len(p) > 80 else ''}")
        if char_count > 300:
            has_overlong = True
    if has_overlong:
        print("\n⚠️  WARNING: posts over 300 chars will fail — shorten before posting")
        if not dry_run:
            print("Aborting. Use --force to post anyway.")
            if "--force" not in sys.argv:
                sys.exit(1)

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
