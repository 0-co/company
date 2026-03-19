#!/usr/bin/env python3
"""
Waits for art 073 to publish on March 22, then updates staggered_posts_mar22.json
with the real URL. Run as background process starting from ~15:55 UTC March 22.
Exits once URL is updated or if it's past 16:30 UTC (timeout).
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone

ARTICLE_ID = 3368335
STAGGERED_FILE = "/home/agent/company/products/content/staggered_posts_mar22.json"
PLACEHOLDER = "TEMPURL"
TARGET_DATE = "2026-03-22"
TIMEOUT_HOUR = 16
TIMEOUT_MINUTE = 35  # give up after 16:35 UTC

def get_article_url():
    """Try to get the published URL for art 073."""
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-devto", "GET", f"/articles/{ARTICLE_ID}"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        # Check if published
        if data.get("published_at") and data.get("url"):
            return data["url"]
        return None
    except Exception as e:
        print(f"Error fetching article: {e}", flush=True)
        return None

def get_url_from_published_list():
    """Fallback: search published articles list for art 073."""
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-devto", "GET", "/articles/me/published"],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return None
        articles = json.loads(result.stdout)
        for a in articles:
            if a.get("id") == ARTICLE_ID:
                return a.get("url") or a.get("canonical_url")
        return None
    except Exception:
        return None

def update_staggered(url):
    """Replace TEMPURL with the real URL in staggered_posts_mar22.json."""
    with open(STAGGERED_FILE) as f:
        posts = json.load(f)

    updated = False
    for post in posts:
        if PLACEHOLDER in post.get("text", ""):
            post["text"] = post["text"].replace(PLACEHOLDER, url)
            updated = True

    if updated:
        with open(STAGGERED_FILE, "w") as f:
            json.dump(posts, f, indent=2)
        print(f"Updated staggered_posts_mar22.json with URL: {url}", flush=True)
    else:
        print(f"No TEMPURL placeholder found — already updated?", flush=True)
    return updated

def main():
    print(f"Starting art 073 URL watcher at {datetime.now(timezone.utc).isoformat()}", flush=True)

    # Wait until target date
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime("%Y-%m-%d")

        if today < TARGET_DATE:
            # Sleep until midnight
            print(f"Not March 22 yet ({today}). Sleeping 3600s.", flush=True)
            time.sleep(3600)
            continue

        if today > TARGET_DATE:
            print(f"Past March 22 ({today}). Checking anyway...", flush=True)

        # Check timeout
        if today == TARGET_DATE and now.hour > TIMEOUT_HOUR:
            print(f"Timeout reached ({now.hour}:{now.minute} UTC). Giving up.", flush=True)
            sys.exit(1)
        if today == TARGET_DATE and now.hour == TIMEOUT_HOUR and now.minute >= TIMEOUT_MINUTE:
            print(f"Timeout reached. Giving up.", flush=True)
            sys.exit(1)

        # Try to get URL
        url = get_article_url()
        if not url:
            url = get_url_from_published_list()

        if url:
            print(f"Art 073 published! URL: {url}", flush=True)
            if update_staggered(url):
                print("Done. Staggered post updated.", flush=True)
                sys.exit(0)
            else:
                print("TEMPURL not found in staggered posts — nothing to update.", flush=True)
                sys.exit(0)

        print(f"{now.strftime('%H:%M UTC')} — Not published yet. Checking again in 60s.", flush=True)
        time.sleep(60)

if __name__ == "__main__":
    main()
