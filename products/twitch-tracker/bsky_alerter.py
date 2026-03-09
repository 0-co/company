#!/usr/bin/env python3
"""
Bluesky notification alerter — runs every 5 minutes via NixOS timer.
Checks for new replies/mentions from accounts with 500+ followers.
Posts to Twitch chat when found.
"""

import json
import subprocess
import sys
import os
from datetime import datetime, timezone

STATE_FILE = "/home/agent/company/products/twitch-tracker/bsky_alert_state.json"
MIN_FOLLOWER_COUNT = 200  # alert on replies from accounts with this many+ followers
TWITCH_BROADCASTER_ID = "1455485722"

# High-priority accounts — alert on any interaction regardless of follower count
PRIORITY_HANDLES = {
    "cmgriffing.bsky.social",
    "sabine.sh",
    "jotson.bsky.social",
    "irishjohngames.bsky.social",
    "frengible.bsky.social",
    "nonzerosumjames.bsky.social",
    "joanwestenberg.com",
    "zoesamuel.bsky.social",
}

ALERT_REASONS = {"reply", "mention", "quote"}


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {"last_seen_at": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def get_notifications():
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.notification.listNotifications", '{"limit": 30}'],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        print(f"Error fetching notifications: {result.stderr[:100]}", file=sys.stderr)
        return []
    d = json.loads(result.stdout)
    return d.get("notifications", [])


def post_to_twitch_chat(message):
    body = json.dumps({
        "broadcaster_id": TWITCH_BROADCASTER_ID,
        "sender_id": TWITCH_BROADCASTER_ID,
        "message": message[:500]
    })
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "POST", "/chat/messages", body],
        capture_output=True, text=True, timeout=10
    )
    return result.returncode == 0


def main():
    state = load_state()
    last_seen_at = state.get("last_seen_at")

    notifications = get_notifications()
    if not notifications:
        return

    # Find newest notification timestamp to save
    newest_at = notifications[0].get("indexedAt", "") if notifications else ""

    alerts = []
    for notif in notifications:
        indexed_at = notif.get("indexedAt", "")

        # Skip if we've already seen this
        if last_seen_at and indexed_at <= last_seen_at:
            continue

        reason = notif.get("reason", "")
        if reason not in ALERT_REASONS:
            continue

        author = notif.get("author", {})
        handle = author.get("handle", "")
        followers = author.get("followersCount", 0)

        # Alert if: priority handle OR high follower count
        if handle not in PRIORITY_HANDLES and followers < MIN_FOLLOWER_COUNT:
            continue

        record = notif.get("record", {})
        text = record.get("text", "")[:100]

        alerts.append({
            "handle": handle,
            "followers": followers,
            "reason": reason,
            "text": text,
            "is_priority": handle in PRIORITY_HANDLES
        })

    if alerts:
        for alert in alerts[:3]:  # cap at 3 alerts per run
            priority_tag = " [PRIORITY]" if alert["is_priority"] else ""
            msg = (
                f"BSKY ALERT{priority_tag}: @{alert['handle']} "
                f"({alert['followers']}f) {alert['reason']}: {alert['text']}"
            )
            post_to_twitch_chat(msg)
            print(f"Alert sent: {msg[:100]}")

    # Save newest timestamp
    if newest_at:
        state["last_seen_at"] = newest_at
        save_state(state)


if __name__ == "__main__":
    main()
