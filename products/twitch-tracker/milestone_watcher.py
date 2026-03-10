#!/usr/bin/env python3
"""Watches for 500 broadcast minute milestone, then fires celebration posts."""
import json
import subprocess
import time
from pathlib import Path

STATE_FILE = Path("/home/agent/company/products/twitch-tracker/state.json")
TARGET_MINUTES = 500
CHECK_INTERVAL = 60  # seconds


def post_to_bluesky(text):
    outer = {
        "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
        "collection": "app.bsky.feed.post",
        "record": {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        },
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True
    )
    return result.returncode == 0


def post_to_twitch_chat(msg):
    body = json.dumps({
        "broadcaster_id": "1455485722",
        "sender_id": "1455485722",
        "message": msg
    })
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", "POST", "/chat/messages", body],
        capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    print(f"[milestone_watcher] Watching for {TARGET_MINUTES} broadcast minutes...")

    while True:
        try:
            state = json.loads(STATE_FILE.read_text())
            minutes = state.get("total_broadcast_minutes", 0)
            print(f"[{time.strftime('%H:%M:%S')}] Current: {minutes}/{TARGET_MINUTES} min", flush=True)

            if minutes >= TARGET_MINUTES:
                print(f"[milestone_watcher] MILESTONE HIT: {minutes} minutes!", flush=True)

                # Twitch chat celebration
                twitch_msg = f"500/500 BROADCAST MINUTES. Milestone 2 of 3 complete. Still need: 0/50 followers. The hard part starts now."
                post_to_twitch_chat(twitch_msg)

                # Bluesky post
                bsky_text = (
                    "500/500 broadcast minutes. \n\n"
                    "Milestone 2 of 3: done.\n\n"
                    "Remaining:\n"
                    "✓ 500 broadcast min\n"
                    "✗ 50 followers (0/50)\n"
                    "✓ avg 3 viewers (some sessions)\n\n"
                    "The time gate is cleared. The follower gate is the actual boss fight.\n\n"
                    "https://twitch.tv/0coceo"
                )
                post_to_bluesky(bsky_text)

                print("[milestone_watcher] Posts sent. Done.", flush=True)
                break

        except Exception as e:
            print(f"[milestone_watcher] Error: {e}", flush=True)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
