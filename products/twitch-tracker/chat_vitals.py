#!/usr/bin/env python3
"""
Twitch Chat Vitals Poster
Posts a company metrics summary to Twitch chat.
Designed to run every 30 minutes via systemd timer.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

BROADCASTER_ID = "1455485722"
STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"
VAULT_TWITCH = "sudo -u vault /home/vault/bin/vault-twitch"

AFFILIATE_FOLLOWERS = 50
AFFILIATE_BROADCAST_MINUTES = 500
DEADLINE = datetime(2026, 4, 30, tzinfo=timezone.utc)


def run_cmd(cmd: str) -> tuple[bool, str]:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
    return result.returncode == 0, result.stdout.strip()


def load_state() -> dict:
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {"total_broadcast_minutes": 0, "last_follower_count": 0}


def fetch_stream() -> dict | None:
    ok, out = run_cmd(f"{VAULT_TWITCH} GET '/streams?user_id={BROADCASTER_ID}'")
    if not ok or not out:
        return None
    try:
        data = json.loads(out).get("data", [])
        return data[0] if data else None
    except (json.JSONDecodeError, IndexError):
        return None


def fetch_followers() -> int:
    ok, out = run_cmd(f"{VAULT_TWITCH} GET '/channels/followers?broadcaster_id={BROADCASTER_ID}'")
    if not ok or not out:
        return -1
    try:
        return json.loads(out).get("total", 0)
    except (json.JSONDecodeError, KeyError):
        return -1


def post_chat(message: str) -> bool:
    payload = json.dumps({
        "broadcaster_id": BROADCASTER_ID,
        "sender_id": BROADCASTER_ID,
        "message": message,
    })
    ok, _ = run_cmd(f"{VAULT_TWITCH} POST '/chat/messages' '{payload}'")
    return ok


def main() -> None:
    state = load_state()
    stream = fetch_stream()

    if not stream:
        print("Stream is offline, skipping chat post", file=sys.stderr)
        return

    followers = fetch_followers()
    if followers < 0:
        followers = state.get("last_follower_count", 0)

    broadcast_min = state.get("total_broadcast_minutes", 0)
    # Add live minutes for current stream
    started_at_str = stream.get("started_at", "")
    if started_at_str:
        started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
        live_min = int((datetime.now(timezone.utc) - started_at).total_seconds() / 60)
        base_min = state.get("broadcast_minutes_before_stream", broadcast_min)
        broadcast_min = base_min + live_min

    viewer_count = stream.get("viewer_count", 0)
    days_left = max(0, (DEADLINE - datetime.now(timezone.utc)).days)
    now_utc = datetime.now(timezone.utc).strftime("%H:%M UTC")

    message = (
        f"📊 {now_utc} | "
        f"Followers: {followers}/{AFFILIATE_FOLLOWERS} | "
        f"Broadcast: {broadcast_min}/{AFFILIATE_BROADCAST_MINUTES}min | "
        f"Viewers: {viewer_count}/3 | "
        f"Revenue: $0 | "
        f"{days_left}d to deadline"
    )

    ok = post_chat(message)
    if ok:
        print(f"Posted vitals: {message}")
    else:
        print("Failed to post to chat", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
