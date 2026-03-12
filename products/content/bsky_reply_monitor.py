#!/usr/bin/env python3
"""
Monitor Bluesky notifications for replies/mentions.
Posts to Discord when someone replies to us.
Run periodically (e.g., every 15 min via systemd timer).
State stored in /var/lib/bsky-monitor/seen.json
"""

import json, os, subprocess, sys
from datetime import datetime

STATE_DIR = "/home/agent/company/products/content"
STATE_FILE = f"{STATE_DIR}/bsky_monitor_state.json"
OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
DISCORD_CHANNEL = "1479926517965258875"  # #general

VAULT_BSKY = ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky"]
VAULT_DISCORD = ["sudo", "-u", "vault", "/home/vault/bin/vault-discord",
                 "-s", "-X", "POST",
                 f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL}/messages",
                 "-H", "Content-Type: application/json"]


def bsky(method, body=None):
    cmd = VAULT_BSKY + [method]
    if body:
        cmd.append(json.dumps(body))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        return None


def discord_post(msg):
    payload = json.dumps({"content": msg})
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-discord",
         "-s", "-X", "POST",
         f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL}/messages",
         "-H", "Content-Type: application/json",
         "-d", payload],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f"Discord post failed: {r.stderr[:100]}", file=sys.stderr)


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"seen_uris": [], "last_run": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def main():
    state = load_state()
    seen = set(state.get("seen_uris", []))

    data = bsky("app.bsky.notification.listNotifications", {"limit": 30})
    if not data:
        print("Failed to fetch notifications", file=sys.stderr)
        return

    notifs = data.get("notifications", [])
    new_replies = []

    for n in notifs:
        uri = n.get("uri", "")
        if uri in seen:
            continue
        reason = n.get("reason", "")
        if reason not in ("reply", "mention", "quote"):
            seen.add(uri)
            continue
        author = n["author"]["handle"]
        author_followers = n["author"].get("followersCount", 0)
        text = n.get("record", {}).get("text", "")
        indexed_at = n.get("indexedAt", "")[:16]
        new_replies.append({
            "uri": uri,
            "reason": reason,
            "author": author,
            "followers": author_followers,
            "text": text,
            "indexed_at": indexed_at,
        })
        seen.add(uri)

    if new_replies:
        # Sort by author followers (highest first)
        new_replies.sort(key=lambda x: x["followers"], reverse=True)

        # Log to local file only — Discord is for community, not notification dumps
        for r in new_replies:
            fcount = f"{r['followers']}f" if r['followers'] else "?f"
            print(f"  [{r['reason']}] @{r['author']} ({fcount}): {r['text'][:80]}")
        print(f"Tracked {len(new_replies)} new replies")
    else:
        print("No new replies")

    # Mark all as seen
    bsky("app.bsky.notification.updateSeen",
         {"seenAt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")})

    state["seen_uris"] = list(seen)[-500:]  # keep last 500
    state["last_run"] = datetime.utcnow().isoformat()
    save_state(state)


if __name__ == "__main__":
    main()
