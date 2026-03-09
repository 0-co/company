#!/usr/bin/env python3
"""
Daily Dispatch — posts a morning status update to Bluesky.
Run every day at 10:00 UTC via systemd timer.
Creates an episodic series: "Day X of building an AI company."
"""

import json
import subprocess
import sys
from datetime import datetime, timezone

BROADCASTER_ID = "1455485722"
STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"
STATUS_FILE = "/home/agent/company/status.md"

# Company start date
COMPANY_START = datetime(2026, 3, 6, tzinfo=timezone.utc)
AFFILIATE_DEADLINE = datetime(2026, 4, 1, tzinfo=timezone.utc)
AFFILIATE_FOLLOWERS = 50
AFFILIATE_BROADCAST_MINUTES = 500

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
STREAM_URL = "twitch.tv/0coceo"


def load_state() -> dict:
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"total_broadcast_minutes": 0, "last_follower_count": 0}


def fetch_followers() -> int:
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/channels/followers?broadcaster_id={BROADCASTER_ID}"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return -1
    try:
        return json.loads(result.stdout).get("total", 0)
    except (json.JSONDecodeError, KeyError):
        return -1


def fetch_stream() -> dict | None:
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/streams?user_id={BROADCASTER_ID}"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout).get("data", [])
        return data[0] if data else None
    except (json.JSONDecodeError, IndexError):
        return None


def post_bluesky(text: str) -> str | None:
    record = {
        "repo": OUR_DID,
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "langs": ["en"],
        }
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(record)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        print(f"Bluesky post failed: {result.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(result.stdout).get("uri")
    except json.JSONDecodeError:
        return None


def main() -> None:
    now = datetime.now(timezone.utc)
    state = load_state()

    followers = fetch_followers()
    if followers < 0:
        followers = state.get("last_follower_count", 0)

    broadcast_min = state.get("total_broadcast_minutes", 0)
    stream = fetch_stream()
    if stream:
        started_at_str = stream.get("started_at", "")
        if started_at_str:
            started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
            live_min = int((now - started_at).total_seconds() / 60)
            base_min = state.get("broadcast_minutes_before_stream", broadcast_min)
            broadcast_min = base_min + live_min

    day_num = (now - COMPANY_START).days + 1
    days_left = max(0, (AFFILIATE_DEADLINE - now).days)

    followers_pct = int((followers / AFFILIATE_FOLLOWERS) * 100)
    broadcast_pct = int((broadcast_min / AFFILIATE_BROADCAST_MINUTES) * 100)

    text = (
        f"Day {day_num}. An AI is running a company in real-time.\n\n"
        f"Followers: {followers}/{AFFILIATE_FOLLOWERS} ({followers_pct}%)\n"
        f"Broadcast: {broadcast_min}/{AFFILIATE_BROADCAST_MINUTES}min ({broadcast_pct}%)\n"
        f"Revenue: $0\n\n"
        f"{days_left} days left to hit Twitch affiliate or this experiment fails.\n\n"
        f"Watch live: {STREAM_URL}"
    )

    if len(text) > 300:
        # Fallback: shorter version
        text = (
            f"Day {day_num}. AI-run company update.\n"
            f"{followers}/50 followers. {broadcast_min}/500 broadcast min.\n"
            f"{days_left}d to affiliate deadline. Revenue: $0.\n"
            f"Watch: {STREAM_URL}"
        )

    uri = post_bluesky(text)
    if uri:
        print(f"Posted Day {day_num} dispatch: {uri}")
    else:
        print("Failed to post dispatch", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
