#!/usr/bin/env python3
"""Update Twitch title when art 073 publishes (March 22 ~16:05 UTC)."""
import subprocess, time, json
from datetime import datetime, timezone
from pathlib import Path

LOG = Path("/home/agent/company/products/content/staggered.log")
BROADCASTER_ID = "1455485722"
NEW_TITLE = "Notion MCP challenge submission live! Notion got an F."
TARGET_DATE = "2026-03-22"
TARGET_HOUR = 16  # Fire after 16:00 UTC

def log(msg):
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    line = f"[{ts}] twitch_title: {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def wait_until_date(target):
    while True:
        today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        if today >= target:
            return
        log(f"Waiting for date {target} (currently {today})...")
        time.sleep(300)

def wait_until_utc(hour, minute=5):
    while True:
        now = datetime.now(timezone.utc)
        if now.hour > hour or (now.hour == hour and now.minute >= minute):
            return
        total_mins = hour * 60 + minute
        current_mins = now.hour * 60 + now.minute
        remaining = (total_mins - current_mins) * 60
        log(f"Waiting for {hour:02d}:{minute:02d} UTC (currently {now.strftime('%H:%M')})...")
        time.sleep(min(remaining, 300))

def update_title():
    payload = json.dumps({"title": NEW_TITLE})
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "PATCH", f"/channels?broadcaster_id={BROADCASTER_ID}",
         payload],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        log(f"Twitch title updated: {NEW_TITLE}")
        return True
    else:
        log(f"Failed to update title: {result.stderr[:200]}")
        return False

log("update_twitch_title_mar22.py started.")
wait_until_date(TARGET_DATE)
wait_until_utc(16, 5)  # 16:05 UTC — 5 minutes after art publishes

update_title()
log("Done.")
