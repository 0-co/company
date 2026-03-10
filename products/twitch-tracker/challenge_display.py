#!/usr/bin/env python3
"""
Live display: "Follower #1 before midnight" challenge status.
Shows countdown, attempt tracking, and live follower count.
Run in terminal for visual stream content.
"""

import subprocess
import json
import time
import sys
from datetime import datetime, timezone

BROADCASTER_ID = "1455485722"

ATTEMPTS = [
    ("@nakibjahan.com", "reply: repeatable systems post", "no response yet"),
    ("@bagelblog.bsky.social", "follow train reply", "no response yet"),
    ("cmgriffing Bluesky", "yak shaving post", "no response yet"),
    ("@sabine.sh", "reply: agents/SaaS building post", "no response yet"),
    ("@jenny-ouyang.bsky.social", "reply: AI agent admin access post", "no response yet"),
    ("@nonzerosumjames.bsky.social", "reply: AI authenticity thread", "no response yet"),
]

def get_followers():
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/channels/followers?broadcaster_id={BROADCASTER_ID}"],
        capture_output=True, text=True, timeout=15
    )
    try:
        return json.loads(result.stdout).get("total", 0)
    except Exception:
        return 0

def get_viewers():
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/streams?user_id={BROADCASTER_ID}"],
        capture_output=True, text=True, timeout=15
    )
    try:
        data = json.loads(result.stdout).get("data", [])
        return data[0].get("viewer_count", 0) if data else 0
    except Exception:
        return 0

def display():
    midnight = datetime(2026, 3, 10, 23, 59, 59, tzinfo=timezone.utc)
    
    iteration = 0
    while True:
        now = datetime.now(timezone.utc)
        time_left = midnight - now
        
        if time_left.total_seconds() < 0:
            print("\n=== MIDNIGHT ===")
            print("Challenge ended. Final state captured.")
            break
        
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        seconds = int(time_left.total_seconds() % 60)
        
        # Refresh followers every 30 iterations (30 seconds)
        if iteration % 30 == 0:
            followers = get_followers()
            viewers = get_viewers()
        
        # Clear screen
        print("\033[H\033[J", end="")
        
        print("=" * 60)
        print("  DAY 3 CHALLENGE: FOLLOWER #1 BEFORE MIDNIGHT UTC")
        print("=" * 60)
        print()
        print(f"  TIME REMAINING:  {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"  FOLLOWERS:       {followers}/50")
        print(f"  LIVE VIEWERS:    {viewers}")
        print(f"  PROGRESS:        {'[' + '█' * followers + '░' * (50-followers) + ']'[:22]}")
        print()
        print("  OUTREACH ATTEMPTS TODAY:")
        for i, (target, method, status) in enumerate(ATTEMPTS, 1):
            status_icon = "✓" if "followed" in status else "→" if "responded" in status else "○"
            print(f"  {i}. {status_icon} {target}")
            print(f"       {method}")
            print(f"       {status}")
        print()
        print(f"  [updated {now.strftime('%H:%M:%S')} UTC]")
        print("=" * 60)
        
        sys.stdout.flush()
        time.sleep(1)
        iteration += 1

if __name__ == "__main__":
    display()
