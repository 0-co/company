#!/usr/bin/env python3
"""
Post a single standalone Bluesky post from a draft file.

Draft format: any text file where the actual post text comes after "TEXT:"

Usage:
  python3 post_standalone.py <draft_file>          # post live
  python3 post_standalone.py <draft_file> --dry-run # preview only
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"


def parse_text(filepath: str) -> str:
    """Extract text after 'TEXT:' line in draft file."""
    with open(filepath) as f:
        content = f.read()
    if "TEXT:" in content:
        text = content.split("TEXT:", 1)[1].strip()
    else:
        text = content.strip()
    return text


def build_facets(text: str) -> list:
    """Build Bluesky facets for @mentions and URLs in text."""
    facets = []
    handle_cache: dict[str, str] = {}

    def resolve_handle(handle: str) -> str | None:
        if handle in handle_cache:
            return handle_cache[handle]
        result = subprocess.run(
            ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.identity.resolveHandle",
             json.dumps({"handle": handle})],
            capture_output=True, text=True, timeout=10
        )
        try:
            did = json.loads(result.stdout).get("did")
            if did:
                handle_cache[handle] = did
            return did
        except Exception:
            return None

    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        handle = m.group(1)
        did = resolve_handle(handle)
        if not did:
            continue
        byte_start = len(text[:m.start()].encode("utf-8"))
        byte_end = len(text[:m.end()].encode("utf-8"))
        facets.append({
            "index": {"byteStart": byte_start, "byteEnd": byte_end},
            "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]
        })

    for m in re.finditer(r'https?://[^\s]+', text):
        url = m.group()
        byte_start = len(text[:m.start()].encode("utf-8"))
        byte_end = len(text[:m.end()].encode("utf-8"))
        facets.append({
            "index": {"byteStart": byte_start, "byteEnd": byte_end},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]
        })

    return facets


def main():
    if len(sys.argv) < 2:
        print("Usage: post_standalone.py <draft_file> [--dry-run]")
        sys.exit(1)

    filepath = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    text = parse_text(filepath)
    print(f"Text ({len(text)} chars):\n{text}\n")

    if dry_run:
        print("[DRY RUN] Not posting.")
        return

    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
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
        print(f"FAILED: {result.stderr.strip()[:200]}")
        sys.exit(1)
    try:
        d = json.loads(result.stdout)
        print(f"Posted: {d.get('uri')}")
    except json.JSONDecodeError:
        print(f"Posted (raw): {result.stdout[:100]}")


if __name__ == "__main__":
    main()
