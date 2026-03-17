#!/usr/bin/env python3
"""Resilient article publisher.

Reads article_schedule.json and publishes the next due article via vault-devto.
Designed to run as a daily systemd timer — if the article is already published
or not yet due, it's a no-op.

Usage: python3 article_publisher.py
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCHEDULE_FILE = Path(__file__).parent / "article_schedule.json"
LOG_FILE = Path(__file__).parent / "publisher.log"


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def devto_publish(article_id):
    """Publish a dev.to article by ID. Returns True if successful."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
         "PUT", f"/articles/{article_id}",
         '{"article":{"published":true}}'],
        capture_output=True, text=True, timeout=30
    )
    output = result.stdout.strip()
    if not output:
        log(f"ERROR: Empty response for article {article_id}")
        return False

    try:
        data = json.loads(output)
        url = data.get("url", "unknown")
        title = data.get("title", "unknown")
        log(f"PUBLISHED: {title} -> {url}")
        return True
    except json.JSONDecodeError:
        log(f"ERROR: Bad JSON response: {output[:200]}")
        return False


def main():
    if not SCHEDULE_FILE.exists():
        log(f"No schedule file at {SCHEDULE_FILE}")
        sys.exit(1)

    with open(SCHEDULE_FILE) as f:
        schedule = json.load(f)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    log(f"Checking schedule for {today}")

    published_any = False
    for entry in schedule:
        if entry.get("published"):
            continue
        if entry["date"] > today:
            continue
        if entry["date"] <= today:
            article_id = entry["article_id"]
            article_num = entry.get("article_num", "?")
            log(f"Publishing article {article_num} (ID: {article_id}, scheduled: {entry['date']})")

            if devto_publish(article_id):
                entry["published"] = True
                entry["published_at"] = today
                published_any = True
            else:
                log(f"Failed to publish article {article_num}")
                break  # Don't try more if one fails

    if published_any:
        with open(SCHEDULE_FILE, "w") as f:
            json.dump(schedule, f, indent=2)
        log("Schedule updated")
    else:
        log("Nothing to publish today")


if __name__ == "__main__":
    main()
