#!/usr/bin/env python3
"""
Session Activity Reporter
Posts a Bluesky summary of what was built this session, based on git commits.
Run after each session: python3 session_reporter.py [--hours N] [--dry-run]
"""
import re
import subprocess
import json
import sys
from datetime import datetime, timezone

_handle_cache: dict = {}


def _resolve_handle(handle: str) -> str | None:
    if handle in _handle_cache:
        return _handle_cache[handle]
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.identity.resolveHandle", json.dumps({"handle": handle})],
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

COMPANY_REPO = "/home/agent/company"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
STREAM_URL = "https://twitch.tv/0coceo"
COMPANY_START = datetime(2026, 3, 8, tzinfo=timezone.utc)
STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"
BROADCASTER_ID = "1455485722"


def get_followers() -> int:
    try:
        r = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/channels/followers?broadcaster_id={BROADCASTER_ID}"],
            capture_output=True, text=True, timeout=10
        )
        return json.loads(r.stdout).get("total", 0)
    except Exception:
        return 0


def get_broadcast_min() -> int:
    try:
        return json.loads(open(STATE_FILE).read()).get("total_broadcast_minutes", 0)
    except Exception:
        return 0


def get_recent_commits(hours: int = 12) -> list[str]:
    """Get feature/fix commit messages from the last N hours."""
    result = subprocess.run(
        ["git", "-C", COMPANY_REPO, "log",
         f"--since={hours} hours ago",
         "--format=%s",
         "--no-merges"],
        capture_output=True, text=True
    )
    if not result.stdout.strip():
        return []
    commits = result.stdout.strip().split('\n')
    # Include feat: and fix: commits, skip chore: and plain status updates
    meaningful = [c for c in commits if c.startswith(('feat:', 'fix:'))]
    return meaningful


def format_commit(msg: str) -> str:
    """Strip prefix and clean up commit message for display."""
    for prefix in ('feat: ', 'fix: ', 'feat:', 'fix:'):
        if msg.startswith(prefix):
            msg = msg[len(prefix):].strip()
            break
    # Trim to 60 chars
    if len(msg) > 60:
        msg = msg[:57] + '...'
    return msg


def generate_post(features: list[str], day_num: int) -> str:
    """Generate a Bluesky-appropriate post (max 300 chars)."""
    if not features:
        return (
            f"Day {day_num} session. Monitoring, engagement, strategy.\n\n"
            f"No new tools shipped. Stream continues.\n\n"
            f"{STREAM_URL}"
        )

    items = [f"→ {format_commit(f)}" for f in features[:4]]
    body = '\n'.join(items)

    text = f"Day {day_num} — built this session:\n\n{body}\n\n{STREAM_URL}"

    # Truncate if over limit
    if len(text) > 295:
        items = [f"→ {format_commit(f)}" for f in features[:2]]
        body = '\n'.join(items) + '\n→ ...'
        text = f"Day {day_num} — built:\n\n{body}\n\n{STREAM_URL}"

    return text


def post_bluesky(text: str, reply_root=None, reply_parent=None) -> tuple[str, str] | tuple[None, None]:
    """Post to Bluesky, optionally as a reply. Returns (uri, cid) or (None, None)."""
    record_body = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
    }
    facets = build_facets(text)
    if facets:
        record_body["facets"] = facets
    if reply_root and reply_parent:
        record_body["reply"] = {
            "root": reply_root,
            "parent": reply_parent,
        }
    record = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": record_body,
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(record)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        uri, cid = data.get("uri"), data.get("cid")
        print(f"Posted: {uri}")
        return uri, cid
    print(f"Failed: {result.stderr[:100]}", file=sys.stderr)
    return None, None


def post_thread(posts: list[str]) -> bool:
    """Post a series of posts as a thread."""
    root_uri = root_cid = parent_uri = parent_cid = None
    for i, text in enumerate(posts):
        import time
        if i > 0:
            time.sleep(1)
        if root_uri is None:
            uri, cid = post_bluesky(text)
            root_uri, root_cid = uri, cid
        else:
            uri, cid = post_bluesky(
                text,
                reply_root={"uri": root_uri, "cid": root_cid},
                reply_parent={"uri": parent_uri, "cid": parent_cid},
            )
        if uri is None:
            return False
        parent_uri, parent_cid = uri, cid
    return True


def build_thread(features: list[str], day_num: int, followers: int, broadcast_min: int) -> list[str]:
    """Build a 2-3 post thread for the session report."""
    posts = []

    # P1: What was built
    if features:
        items = [f"→ {format_commit(f)}" for f in features[:4]]
        body = '\n'.join(items)
        p1 = f"Day {day_num} — built this session:\n\n{body}"
        if len(p1) > 295:
            items = [f"→ {format_commit(f)}" for f in features[:2]]
            body = '\n'.join(items) + '\n→ ...'
            p1 = f"Day {day_num} — built:\n\n{body}"
    else:
        p1 = f"Day {day_num} — quiet session. Monitoring, engagement, strategy. No new tools."
    posts.append(p1)

    # P2: Current status
    p2 = (
        f"Status update:\n"
        f"Followers: {followers}/50\n"
        f"Broadcast min: {broadcast_min}/500\n"
        f"Revenue: $0\n\n"
        f"Deadline: April 1. The follower gate is the real problem."
    )
    posts.append(p2)

    # P3: CTA
    p3 = f"Watch it all happen live. An AI building a company from a terminal.\n\n{STREAM_URL}"
    posts.append(p3)

    return posts


def main():
    hours = 12
    dry_run = "--dry-run" in sys.argv
    use_thread = "--thread" in sys.argv or True  # default to thread
    for arg in sys.argv[1:]:
        if arg.startswith("--hours="):
            hours = int(arg.split("=")[1])
        elif arg.isdigit():
            hours = int(arg)

    now = datetime.now(timezone.utc)
    day_num = (now - COMPANY_START).days + 1
    followers = get_followers()
    broadcast_min = get_broadcast_min()

    features = get_recent_commits(hours)
    print(f"Day {day_num} | Last {hours}h | {len(features)} feature commits | {followers}/50 followers")

    if features:
        print("Commits:")
        for f in features:
            print(f"  {f}")

    thread = build_thread(features, day_num, followers, broadcast_min)

    print(f"\nThread preview ({len(thread)} posts):")
    for i, p in enumerate(thread, 1):
        print(f"\n── Post {i} ({len(p)} chars) ──")
        print(p)

    if dry_run:
        print("\n(dry run — not posting)")
        return

    if features or "--force" in sys.argv:
        print("\nPosting thread...")
        post_thread(thread)
    else:
        print("\nNo new features — skipping post (use --force to post anyway)")


if __name__ == "__main__":
    main()
