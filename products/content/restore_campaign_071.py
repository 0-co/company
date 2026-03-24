#!/usr/bin/env python3
"""Restore campaign_queue.json for art 071 on 2026-03-25.
Waits until 15:45 UTC on March 25 (before 16:00 article publish + 16:00 campaign timer),
then copies campaign_queue_071.json to campaign_queue.json.
Exits immediately if the file already exists (safety guard).
"""
import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path

TARGET_DATE = "2026-03-25"
TARGET_HOUR = 15
TARGET_MIN = 45

SRC = Path("/home/agent/company/products/content/campaign_queue_071.json")
DST = Path("/home/agent/company/products/content/campaign_queue.json")
LOG = Path("/home/agent/company/products/content/staggered.log")


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] restore-campaign-071: {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")


log("restore-campaign-071 started, waiting for 2026-03-25 15:45 UTC")

while True:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")

    if today > TARGET_DATE:
        log("target date passed, exiting without action")
        break

    if today == TARGET_DATE and now.hour > TARGET_HOUR:
        log("target time passed, exiting without action")
        break

    if today == TARGET_DATE and now.hour == TARGET_HOUR and now.minute >= TARGET_MIN:
        if DST.exists():
            log(f"campaign_queue.json already exists, skipping restore")
        else:
            shutil.copy2(SRC, DST)
            log(f"Restored campaign_queue.json from campaign_queue_071.json")
            with open(DST) as f:
                data = json.load(f)
            log(f"  article_id={data.get('article_id')}, article_num={data.get('article_num')}")
        break

    time.sleep(60)
