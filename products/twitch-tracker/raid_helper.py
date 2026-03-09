#!/usr/bin/env python3
"""
raid_helper.py — finds the best raid target when ending a stream session

Queries "Software and Game Development" category, scores streams by:
- Viewer count (prefer 20-150 range: small enough to notice, big enough to matter)
- Stream duration (prefer 30+ minutes: settled audience)
- Title relevance (prefer coding/AI/building-in-public themes)
- Language (prefer English unless we specifically want cross-community)

Usage:
  python3 products/twitch-tracker/raid_helper.py        # show top 5 candidates
  python3 products/twitch-tracker/raid_helper.py --raid  # execute raid on top pick
  python3 products/twitch-tracker/raid_helper.py --raid <user_id>  # raid specific channel
"""

import sys
import json
import subprocess
from datetime import datetime, timezone

GAME_ID = "1469308723"  # Software and Game Development
MY_BROADCASTER_ID = "1455485722"

# Title keywords that suggest similar content (builds rapport for raid-back)
AFFINITY_KEYWORDS = [
    "ai", "agent", "autonomous", "building in public", "build", "startup",
    "claude", "gpt", "llm", "python", "typescript", "rust", "solo dev",
    "indie", "saas", "open source", "automation"
]


def twitch_get(endpoint):
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", "GET", endpoint],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def score_stream(stream):
    """Score a stream 0-100 as a raid target."""
    score = 0

    # Viewer count sweet spot: 20-150
    vc = stream.get("viewer_count", 0)
    if 20 <= vc <= 150:
        score += 30
    elif 10 <= vc < 20:
        score += 15
    elif 150 < vc <= 300:
        score += 10
    # Under 10 or over 300: 0 points (too small to matter, too big to notice)

    # Stream duration (longer = more settled audience)
    started = stream.get("started_at", "")
    if started:
        try:
            start_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
            duration_min = (datetime.now(timezone.utc) - start_dt).total_seconds() / 60
            if duration_min >= 60:
                score += 25
            elif duration_min >= 30:
                score += 15
            elif duration_min >= 15:
                score += 5
        except (ValueError, TypeError):
            pass

    # Title keyword affinity
    title = stream.get("title", "").lower()
    matches = sum(1 for kw in AFFINITY_KEYWORDS if kw in title)
    score += min(matches * 10, 30)

    # Language: bonus for English
    if stream.get("language", "") == "en":
        score += 15

    # Skip ourselves
    if stream.get("user_id") == MY_BROADCASTER_ID:
        return -1

    return score


def get_streams():
    data = twitch_get(f"/streams?game_id={GAME_ID}&first=100")
    return data.get("data", [])


def format_duration(started_at):
    try:
        start_dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        minutes = int((datetime.now(timezone.utc) - start_dt).total_seconds() / 60)
        if minutes >= 60:
            return f"{minutes//60}h{minutes%60:02d}m"
        return f"{minutes}m"
    except (ValueError, TypeError):
        return "?"


def execute_raid(to_broadcaster_id, username):
    print(f"\nRaiding @{username} (ID: {to_broadcaster_id})...")
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", "POST", "/raids",
         json.dumps({"from_broadcaster_id": MY_BROADCASTER_ID, "to_broadcaster_id": to_broadcaster_id})],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"Raid initiated! Go watch @{username}")
        # Post to Twitch chat
        msg = f"Raiding @{username} — similar energy, check them out!"
        subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", "POST", "/chat/messages",
             json.dumps({"broadcaster_id": MY_BROADCASTER_ID, "sender_id": MY_BROADCASTER_ID, "message": msg})],
            capture_output=True
        )
    else:
        print(f"Raid failed: {result.stderr[:100]}")


def main():
    raid_flag = "--raid" in sys.argv
    specific_id = None
    if raid_flag and len(sys.argv) > 2:
        specific_id = sys.argv[2]

    streams = get_streams()
    if not streams:
        print("No streams found in category.")
        return

    # Score all streams
    scored = []
    for s in streams:
        if s.get("user_id") == MY_BROADCASTER_ID:
            continue
        score = score_stream(s)
        scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:5]

    print(f"Top raid candidates in 'Software and Game Development' ({len(streams)} live streams):\n")
    print(f"{'Score':>5}  {'Viewers':>7}  {'Duration':>8}  {'Lang':>4}  Channel + Title")
    print("-" * 80)

    for score, s in top:
        vc = s.get("viewer_count", 0)
        user = s.get("user_name", "?")
        title = s.get("title", "")[:45]
        lang = s.get("language", "?")
        dur = format_duration(s.get("started_at", ""))
        uid = s.get("user_id", "")
        print(f"{score:>5}  {vc:>7}  {dur:>8}  {lang:>4}  @{user}: {title}")

    if top:
        best_score, best = top[0]
        print(f"\nBest pick: @{best['user_name']} ({best['viewer_count']} viewers, score {best_score})")
        print(f"Title: {best['title']}")

        if raid_flag:
            target_id = specific_id or best["user_id"]
            target_user = best["user_name"] if not specific_id else target_id
            execute_raid(target_id, target_user)
        else:
            print(f"\nTo raid: python3 products/twitch-tracker/raid_helper.py --raid")
            print(f"Or: python3 products/twitch-tracker/raid_helper.py --raid {best['user_id']}")


if __name__ == "__main__":
    main()
