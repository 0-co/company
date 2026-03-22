#!/usr/bin/env python3
"""Watch Bluesky followers. When we hit 50, auto-file newsletter pitch board request.
Runs until triggered, then exits.
"""
import json, subprocess, time
from datetime import datetime, timezone
from pathlib import Path

OUR_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
VAULT_BSKY = "/home/vault/bin/vault-bsky"
THRESHOLD = 50
BOARD_INBOX = Path("/home/agent/company/board/inbox")
LOG_FILE = Path("/home/agent/company/products/content/staggered.log")
TEMPLATE = Path("/home/agent/company/board/inbox_templates/newsletter_pitch_ready.md")


def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] newsletter-watcher: {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def get_followers():
    r = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "app.bsky.actor.getProfile",
         json.dumps({"actor": OUR_DID})],
        capture_output=True, text=True, timeout=30
    )
    if r.returncode != 0:
        return None
    data = json.loads(r.stdout)
    return data.get("followersCount")


def file_board_request(count):
    template = TEMPLATE.read_text() if TEMPLATE.exists() else ""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    content = f"""# Newsletter Pitch — 50 Followers Threshold Met (auto-filed)

**Auto-filed at**: {ts}
**Bluesky followers**: {count}

{template}
"""
    outfile = BOARD_INBOX / "2-newsletter-pitch-50-followers.md"
    outfile.write_text(content)
    log(f"Board request filed: {outfile}")


def main():
    log(f"Started. Waiting for {THRESHOLD} Bluesky followers...")
    while True:
        count = get_followers()
        if count is not None:
            log(f"Current followers: {count}")
            if count >= THRESHOLD:
                log(f"Threshold reached! {count} followers. Filing board request...")
                file_board_request(count)
                log("Done.")
                return
        else:
            log("Failed to get follower count.")
        time.sleep(300)  # check every 5 minutes


if __name__ == "__main__":
    main()
