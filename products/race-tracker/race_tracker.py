#!/usr/bin/env python3
"""
AI Company Race Tracker
Tracks Bluesky follower/post stats for peer AI companies.
Posts daily update to Bluesky.
Run: python3 products/race-tracker/race_tracker.py
"""

import subprocess
import json
import os
import sys
from datetime import datetime, timezone

COMPANIES = [
    {"name": "0coceo (us)", "did": "did:plc:ak33o45ans6qtlhxxulcd4ko", "handle": "0coceo.bsky.social"},
    {"name": "ultrathink-art", "did": "did:plc:rkmhvhrql3etake2ubbo6tjb", "handle": "ultrathink-art.bsky.social"},
    {"name": "iamgumbo", "did": "did:plc:xyur564kq3dlutyqjr2fmest", "handle": "iamgumbo.bsky.social"},
    {"name": "idapixl", "did": "did:plc:zjlxcmf26pwejgdnlagnngff", "handle": "idapixl.bsky.social"},
    {"name": "wolfpacksolution", "did": "did:plc:unudjn5ws5ele6kffzb3pcl5", "handle": "wolfpacksolution.bsky.social"},
]

def get_profile(did):
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.actor.getProfile", json.dumps({"actor": did})],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except Exception:
        return None

def post_to_bluesky(text):
    outer = {
        "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return data.get("uri", "")
    return None

def run():
    print(f"AI Company Race Tracker — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")

    stats = []
    for company in COMPANIES:
        profile = get_profile(company["did"])
        if profile:
            stats.append({
                "name": company["name"],
                "handle": company["handle"],
                "followers": profile.get("followersCount", 0),
                "posts": profile.get("postsCount", 0),
                "follows": profile.get("followsCount", 0),
            })
            print(f"  @{company['handle']}: {profile.get('followersCount',0)} followers, {profile.get('postsCount',0)} posts")
        else:
            print(f"  @{company['handle']}: ERROR")

    if not stats:
        print("No stats retrieved, aborting")
        return

    # Sort by followers descending
    stats.sort(key=lambda x: x["followers"], reverse=True)

    # Build post (300 char limit)
    today = datetime.now(timezone.utc).strftime("%b %d")

    lines = [f"AI company race — {today}"]
    lines.append("")
    for i, s in enumerate(stats):
        medal = ["🥇", "🥈", "🥉", "4.", "5."][min(i, 4)]
        line = f"{medal} @{s['handle']}: {s['followers']}f / {s['posts']}p"
        lines.append(line)

    text = "\n".join(lines)

    if len(text) > 300:
        # Trim handles
        lines = [f"AI company race — {today}", ""]
        for i, s in enumerate(stats):
            medal = ["1.", "2.", "3.", "4.", "5."][min(i, 4)]
            name = s['handle'].replace('.bsky.social', '')[:12]
            line = f"{medal} @{name}: {s['followers']}f/{s['posts']}p"
            lines.append(line)
        text = "\n".join(lines)

    print(f"\nPost ({len(text)} chars):")
    print(text)

    # Save race data to JSON for dashboard /race page
    race_data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "companies": stats,
    }
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "race_data.json")
    with open(data_path, "w") as f:
        json.dump(race_data, f, indent=2)
    print(f"Saved race data to {data_path}")

    if "--dry-run" in sys.argv:
        print("\n[DRY RUN — not posting]")
        return

    uri = post_to_bluesky(text)
    if uri:
        print(f"\nPosted: {uri}")
    else:
        print("\nFailed to post")

if __name__ == "__main__":
    run()
