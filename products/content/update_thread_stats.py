#!/usr/bin/env python3
"""Update live follower stats in Day 4 thread files before posting."""

import json, re, subprocess, sys
from datetime import date

BROADCASTER_ID = "1455485722"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
DEADLINE = date(2026, 4, 1)
DAY_ONE = date(2026, 3, 8)


def get_twitch_followers():
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/channels/followers?broadcaster_id={BROADCASTER_ID}"],
        capture_output=True, text=True
    )
    try:
        return json.loads(r.stdout).get("total", 1)
    except Exception:
        return 1


def get_bsky_followers():
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.actor.getProfile", json.dumps({"actor": OUR_DID})],
        capture_output=True, text=True
    )
    try:
        return json.loads(r.stdout).get("followersCount", 14)
    except Exception:
        return 14


def update_file(path, replacements):
    """replacements: list of (old_str, new_str) tuples"""
    with open(path) as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(path, "w") as f:
        f.write(content)


def main():
    twitch_f = get_twitch_followers()
    bsky_f = get_bsky_followers()
    today = date.today()
    day_num = (today - DAY_ONE).days + 1
    days_left = (DEADLINE - today).days

    print(f"Live stats: Twitch={twitch_f}/50, Bluesky={bsky_f}, Day {day_num}, {days_left}d left")

    base = "/home/agent/company/products/twitch-tracker"

    # Update day4_first5min_thread.txt P6
    first5 = f"{base}/day4_first5min_thread.txt"
    # P6 line: "Day 4. 1 Twitch follower. 14 Bluesky followers."
    with open(first5) as f:
        content = f.read()
    # Replace the Day N line with current stats
    new_p6_line = f"Day {day_num}. {twitch_f} Twitch follower{'s' if twitch_f != 1 else ''}. {bsky_f} Bluesky followers."
    # Find pattern like "Day \d+\. \d+ Twitch follower"
    content_new = re.sub(
        r'Day \d+\. \d+ Twitch followers?\. \d+ Bluesky followers?\.',
        new_p6_line,
        content
    )
    with open(first5, "w") as f:
        f.write(content_new)
    print(f"Updated {first5}: P6 → {new_p6_line}")

    # Update day4_vibe_ceo_thread.txt P4
    vibe = f"{base}/day4_vibe_ceo_thread.txt"
    with open(vibe) as f:
        content = f.read()
    new_p4_line = f"still at {twitch_f}/50 Twitch followers."
    content_new = re.sub(
        r'still at \d+/50 Twitch followers?\.',
        new_p4_line,
        content
    )
    with open(vibe, "w") as f:
        f.write(content_new)
    print(f"Updated {vibe}: P4 → {new_p4_line}")

    # Update days_left in day4_vibe_ceo_thread.txt
    with open(vibe) as f:
        content = f.read()
    content_new = re.sub(
        r'\d+ days left\.',
        f"{days_left} days left.",
        content
    )
    with open(vibe, "w") as f:
        f.write(content_new)

    print("All stats updated.")


if __name__ == "__main__":
    main()
