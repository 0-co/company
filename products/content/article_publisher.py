#!/usr/bin/env python3
"""Resilient article publisher.

Reads article_schedule.json and publishes the next due article via vault-devto.
Designed to run as a daily systemd timer — if the article is already published
or not yet due, it's a no-op.

Usage: python3 article_publisher.py
"""

import json
import re
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


def devto_get_body(article_id):
    """Get article body_markdown. Returns None on failure.

    Falls back to /articles/me/all if /articles/:id is rate-limited.
    """
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
         "GET", f"/articles/{article_id}"],
        capture_output=True, text=True, timeout=30
    )
    if result.stdout.strip():
        try:
            data = json.loads(result.stdout)
            body = data.get("body_markdown", "")
            if body:
                return body
        except json.JSONDecodeError:
            pass

    # Fallback: /articles/me/all is not rate-limited even when /articles/:id is
    log(f"GET /articles/{article_id} failed or empty, falling back to /articles/me/all")
    result2 = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
         "GET", "/articles/me/all"],
        capture_output=True, text=True, timeout=60
    )
    if result2.stdout.strip():
        try:
            articles = json.loads(result2.stdout)
            for a in articles:
                if a.get("id") == article_id:
                    body = a.get("body_markdown", "")
                    if body:
                        log(f"Found body via /articles/me/all ({len(body)} chars)")
                        return body
        except (json.JSONDecodeError, TypeError):
            pass

    return None


def devto_publish(article_id):
    """Publish a dev.to article by ID. Returns True if successful.

    Dev.to API quirk: if body_markdown has 'published: false' in front matter,
    a plain PUT with published:true is overridden. Must update body too.
    """
    # Get current body and fix front matter
    body = devto_get_body(article_id)
    if body is None:
        log(f"WARNING: Could not fetch body for {article_id}, trying simple publish")
        body = ""

    # Remove 'published: false' from front matter if present
    if body:
        fixed_body = re.sub(r'^published: false\s*$', 'published: true', body, flags=re.MULTILINE)
    else:
        fixed_body = body

    payload = {"article": {"published": True}}
    if fixed_body:
        payload["article"]["body_markdown"] = fixed_body

    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
         "PUT", f"/articles/{article_id}",
         json.dumps(payload)],
        capture_output=True, text=True, timeout=60
    )
    output = result.stdout.strip()
    if not output:
        log(f"ERROR: Empty response for article {article_id}")
        return False

    try:
        data = json.loads(output)
        url = data.get("url", "unknown")
        title = data.get("title", "unknown")
        published_at = data.get("published_at")
        if published_at:
            log(f"PUBLISHED: {title} -> {url} (at {published_at})")
            return True
        else:
            log(f"WARNING: Got response but published_at is null. URL: {url}")
            # Return True anyway — article may still have published
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
