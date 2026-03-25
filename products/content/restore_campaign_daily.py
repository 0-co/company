#!/usr/bin/env python3
"""Daily campaign dispatcher — runs at 15:45 UTC, copies today's campaign to campaign_queue.json.

Reads article_schedule.json to find today's article, then looks for campaign_queue_{num}.json.
If found and campaign_queue.json doesn't already exist, copies it over.

Start once at boot with: nohup python3 restore_campaign_daily.py > /tmp/campaign_restore.log 2>&1 &
"""
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

SCHEDULE_FILE = Path("/home/agent/company/products/content/article_schedule.json")
CAMPAIGN_DIR = Path("/home/agent/company/products/content")
DST = CAMPAIGN_DIR / "campaign_queue.json"
LOG = CAMPAIGN_DIR / "staggered.log"
TARGET_HOUR = 15
TARGET_MIN = 45


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] campaign-restore: {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def find_todays_campaign(today: str):
    """Return Path to today's campaign_queue file, or None."""
    if not SCHEDULE_FILE.exists():
        return None
    with open(SCHEDULE_FILE) as f:
        schedule = json.load(f)

    for entry in schedule:
        if entry.get("date") == today and not entry.get("published"):
            num = entry.get("article_num")
            if not num:
                # Try apr01, apr02 style
                continue
            # Try article_num style first (e.g., "071")
            candidate = CAMPAIGN_DIR / f"campaign_queue_{num}.json"
            if candidate.exists():
                return candidate

    # Also check apr01, apr02 style
    dt = datetime.strptime(today, "%Y-%m-%d")
    if dt.month == 4:
        apr_key = f"apr{dt.day:02d}"
        candidate = CAMPAIGN_DIR / f"campaign_queue_{apr_key}.json"
        if candidate.exists():
            return candidate

    return None


def already_ran_today(today: str) -> bool:
    """Check if we already restored a campaign for today."""
    if not LOG.exists():
        return False
    content = LOG.read_text()
    return f"campaign-restore: Restored campaign_queue.json" in content and today in content


log("Campaign restore daemon started")

last_date_checked = ""

while True:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    # Wait for 15:45 UTC
    if now.hour > TARGET_HOUR or (now.hour == TARGET_HOUR and now.minute >= TARGET_MIN):
        if today != last_date_checked:
            last_date_checked = today
            log(f"Checking campaign for {today}")

            if DST.exists():
                log(f"campaign_queue.json already exists for {today}, skipping")
            else:
                src = find_todays_campaign(today)
                if src:
                    shutil.copy2(src, DST)
                    with open(DST) as f:
                        data = json.load(f)
                    log(f"Restored campaign_queue.json from {src.name} (article_id={data.get('article_id')}, num={data.get('article_num')})")
                else:
                    log(f"No campaign file found for {today} — no Bluesky campaign today")

    time.sleep(60)
