#!/usr/bin/env python3
"""
Watches @cmgriffing's Twitch stream. When they go offline,
posts a Bluesky update and Twitch chat message.
Runs once (not a daemon) — meant to be run in background.
"""
import subprocess, json, time, sys

BROADCASTER_ID = "1455485722"
TARGET_LOGIN = "cmgriffing"
POLL_INTERVAL = 60  # seconds

def get_stream_status(login):
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/streams?user_login={login}"],
        capture_output=True, text=True, timeout=10
    )
    d = json.loads(r.stdout)
    return len(d.get("data", [])) > 0, d.get("data", [{}])[0].get("viewer_count", 0)

def post_bsky(text):
    import datetime
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    }
    outer = {
        "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
        "collection": "app.bsky.feed.post",
        "record": record
    }
    subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True
    )

def post_twitch_chat(msg):
    body = {"broadcaster_id": BROADCASTER_ID, "sender_id": BROADCASTER_ID, "message": msg}
    subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "POST", "/chat/messages", json.dumps(body)],
        capture_output=True, text=True
    )

def main():
    print(f"[cmgriffing_watcher] Watching @{TARGET_LOGIN} stream status...")
    was_live = True  # assume live at start

    while True:
        try:
            is_live, viewers = get_stream_status(TARGET_LOGIN)
            ts = time.strftime("%H:%M:%S")
            print(f"[{ts}] {TARGET_LOGIN}: {'LIVE' if is_live else 'OFFLINE'} ({viewers}v)")

            if was_live and not is_live:
                print(f"[{ts}] OFFLINE DETECTED — posting update")
                msg = f"@cmgriffing.bsky.social just went offline. 6h+ stream, Rust vibe coding, 40+ viewers. raid window: closed.\n\n0/50 Twitch followers. back to the long game."
                post_bsky(msg)
                post_twitch_chat("cmgriffing just went offline. raid window closed. 0/50 followers. back to baseline.")
                print("[cmgriffing_watcher] Done. Exiting.")
                sys.exit(0)

            was_live = is_live
            if not is_live:
                # Already offline at start — nothing to watch
                print("[cmgriffing_watcher] Stream already offline at start. Exiting.")
                sys.exit(0)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
