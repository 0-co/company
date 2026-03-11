#!/usr/bin/env python3
"""
Bluesky follower attribution tracker.

Records when new followers arrive and correlates them with recent posts
to understand which content drives follows.

Usage:
    python follower_tracker.py
    python follower_tracker.py run
"""

import json
import logging
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY_CMD = "/home/vault/bin/vault-bsky"
VAULT_USER = "vault"
STATE_FILE = Path("/home/agent/company/products/audience-finder/follower_attribution.json")
ATTRIBUTION_WINDOW_HOURS = 48

# ---------------------------------------------------------------------------
# Logging — structured to stderr, clean summary to stdout
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def call_vault_bsky(method: str, body: dict[str, Any]) -> dict[str, Any] | None:
    """Call vault-bsky subprocess and return parsed JSON, or None on failure."""
    cmd = ["sudo", "-u", VAULT_USER, VAULT_BSKY_CMD, method, json.dumps(body)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        logger.warning("vault-bsky timed out for %s", method)
        return None
    except OSError as exc:
        logger.warning("vault-bsky subprocess error: %s", exc)
        return None

    if result.returncode != 0:
        logger.warning(
            "vault-bsky non-zero (%d) for %s: %s",
            result.returncode,
            method,
            result.stderr.strip(),
        )
        return None

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        logger.warning("JSON parse failure for %s: %s", method, exc)
        return None


def fetch_followers() -> dict[str, str]:
    """Return {did: handle} for all current followers (up to 100)."""
    response = call_vault_bsky(
        "app.bsky.graph.getFollowers",
        {"actor": OUR_DID, "limit": 100},
    )
    if response is None:
        return {}

    followers: dict[str, str] = {}
    for follower in response.get("followers", []):
        did = follower.get("did", "")
        handle = follower.get("handle", "")
        if did and handle:
            followers[did] = handle

    return followers


def fetch_recent_posts(hours: int = ATTRIBUTION_WINDOW_HOURS) -> list[dict[str, Any]]:
    """Return our posts from the last N hours with text, created_at, likeCount."""
    response = call_vault_bsky(
        "app.bsky.feed.getAuthorFeed",
        {"actor": OUR_DID, "limit": 20},
    )
    if response is None:
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    recent: list[dict[str, Any]] = []

    for item in response.get("feed", []):
        post = item.get("post", {})
        record = post.get("record", {})
        created_at_raw = record.get("createdAt", "")
        if not created_at_raw:
            continue

        try:
            created_at = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
        except ValueError:
            continue

        if created_at < cutoff:
            continue

        text = record.get("text", "")
        like_count = int(post.get("likeCount", 0))

        recent.append({
            "text": text,
            "created_at": created_at_raw,
            "likes": like_count,
        })

    return recent


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state() -> dict[str, Any]:
    """Load state from JSON file, returning empty structure if missing."""
    if not STATE_FILE.exists():
        return {"known_followers": {}, "events": []}

    try:
        with STATE_FILE.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read state file: %s", exc)
        return {"known_followers": {}, "events": []}


def save_state(state: dict[str, Any]) -> None:
    """Persist state to JSON file atomically."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = STATE_FILE.with_suffix(".json.tmp")
    try:
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(state, file, indent=2)
        tmp_path.replace(STATE_FILE)
    except OSError as exc:
        logger.warning("Could not write state file: %s", exc)


# ---------------------------------------------------------------------------
# Attribution formatting
# ---------------------------------------------------------------------------

def format_post_snippet(post: dict[str, Any]) -> str:
    """Format a single post as a compact attribution label."""
    text = post.get("text", "").replace("\n", " ").strip()
    created_at_raw = post.get("created_at", "")
    try:
        created_at = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
        time_label = created_at.strftime("%H:%M")
    except ValueError:
        time_label = "??"

    snippet = text[:40] + "..." if len(text) > 40 else text
    return f'"{snippet}" at {time_label}'


def format_new_follower_line(handle: str, recent_posts: list[dict[str, Any]]) -> str:
    """Format a single new follower with their attributed posts."""
    if not recent_posts:
        return f"@{handle} (no recent posts in window)"

    post_labels = [format_post_snippet(p) for p in recent_posts[:3]]
    posts_str = ", ".join(post_labels)
    return f"@{handle} (+posts: {posts_str})"


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def find_new_followers(
    current: dict[str, str],
    known: dict[str, str],
) -> dict[str, str]:
    """Return {did: handle} for followers not in known set."""
    return {did: handle for did, handle in current.items() if did not in known}


def build_follower_event(
    handle: str,
    did: str,
    recent_posts: list[dict[str, Any]],
) -> dict[str, Any]:
    """Construct an attribution event record."""
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "handle": handle,
        "did": did,
        "recent_posts": recent_posts,
    }


def run() -> None:
    """Main execution: check followers, detect new ones, record attribution."""
    state = load_state()
    known_followers: dict[str, str] = state.get("known_followers", {})
    events: list[dict[str, Any]] = state.get("events", [])

    current_followers = fetch_followers()
    if not current_followers:
        now_str = datetime.now(timezone.utc).strftime("%H:%M UTC")
        print(f"[{now_str}] Could not fetch followers. Skipping run.")
        return

    total = len(current_followers)
    new_followers = find_new_followers(current_followers, known_followers)
    new_count = len(new_followers)

    now_str = datetime.now(timezone.utc).strftime("%H:%M UTC")

    # First run: establish baseline, no events recorded
    if not known_followers:
        state["known_followers"] = current_followers
        state["events"] = events
        save_state(state)
        print(f"[{now_str}] First run. Baseline established: {total} followers. No events recorded.")
        return

    new_follower_lines: list[str] = []

    if new_count > 0:
        recent_posts = fetch_recent_posts(hours=ATTRIBUTION_WINDOW_HOURS)

        for did, handle in new_followers.items():
            event = build_follower_event(handle, did, recent_posts)
            events.append(event)
            new_follower_lines.append(format_new_follower_line(handle, recent_posts))

    # Update known followers to include new ones (never remove — tracks arrivals only)
    state["known_followers"] = {**known_followers, **new_followers}
    state["events"] = events
    save_state(state)

    if new_count == 0:
        print(f"[{now_str}] Followers: {total}. New: 0.")
    else:
        follower_details = " | ".join(new_follower_lines)
        print(f"[{now_str}] Followers: {total}. New: {new_count}. {follower_details}")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = sys.argv[1:]
    if args and args[0] not in ("run",):
        print(f"Usage: {sys.argv[0]} [run]", file=sys.stderr)
        sys.exit(1)
    run()


if __name__ == "__main__":
    main()
