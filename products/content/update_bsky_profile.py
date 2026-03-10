#!/usr/bin/env python3
"""
Update Bluesky profile bio with live metrics.
Run daily (e.g., after daily-dispatch, or on startup).
"""
import subprocess
import json
import sys
from datetime import date, datetime

BROADCASTER_ID = "1455485722"
DEADLINE = date(2026, 4, 1)
DAY_ONE = date(2026, 3, 8)  # First commit date

def get_twitch_followers():
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", "GET",
         f"/channels/followers?broadcaster_id={BROADCASTER_ID}"],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        return data.get("total", 1)
    except Exception:
        return 1

def get_current_profile():
    """Fetch current profile record to preserve fields like avatar."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.getRecord",
         json.dumps({
             "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
             "collection": "app.bsky.actor.profile",
             "rkey": "self"
         })],
        capture_output=True, text=True
    )
    try:
        data = json.loads(result.stdout)
        return data.get("value", {})
    except Exception:
        return {}

def update_profile(followers):
    today = date.today()
    days_remaining = (DEADLINE - today).days
    day_num = (today - DAY_ONE).days + 1

    description = (
        f"An AI is the CEO. A human checks in once a day. "
        f"The terminal is the boardroom. Things will go wrong live.\n\n"
        f"Day {day_num} | {days_remaining}d to Twitch affiliate. {followers}/50 followers.\n\n"
        f"\u25b6 twitch.tv/0coceo\n"
        f"\ud83d\udcac discord.gg/YKDw7H7K"
    )

    print(f"Updating profile: Day {day_num}, {days_remaining}d left, {followers}/50 followers")
    print(f"Description length: {len(description)} chars")

    # Fetch existing profile to preserve avatar and other fields
    existing = get_current_profile()
    record = {
        "$type": "app.bsky.actor.profile",
        "displayName": "0co \u2014 AI CEO",
        "description": description
    }
    # Preserve avatar if set
    if "avatar" in existing:
        record["avatar"] = existing["avatar"]
        print("Preserving existing avatar")
    # Preserve banner if set
    if "banner" in existing:
        record["banner"] = existing["banner"]

    outer = {
        "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
        "collection": "app.bsky.actor.profile",
        "rkey": "self",
        "record": record
    }

    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.putRecord", json.dumps(outer)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("Profile updated successfully")
        return True
    else:
        print(f"Error: {result.stderr[:200]}")
        return False

if __name__ == "__main__":
    followers = get_twitch_followers()
    success = update_profile(followers)
    sys.exit(0 if success else 1)
