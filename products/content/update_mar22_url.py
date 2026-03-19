#!/usr/bin/env python3
"""Wait for art 073 to publish on March 22, then update TEMPURL in staggered_posts_mar22.json.

Runs from March 19. Waits until March 22 16:05 UTC, fetches art 073 URL, patches the file.
Must complete before 18:00 UTC on March 22 when the staggered post fires.
"""

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ARTICLE_ID = 3368335
POSTS_FILE = Path("/home/agent/company/products/content/staggered_posts_mar22.json")
LOG_PREFIX = "[update_mar22_url]"

TARGET_DATE = "2026-03-22"
TARGET_HOUR = 16  # Wait until 16:05 UTC (5 min after publish)
TARGET_MIN = 5


def log(msg):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"{ts} {LOG_PREFIX} {msg}", flush=True)


def wait_until_target():
    while True:
        now = datetime.now(timezone.utc)
        today = now.strftime("%Y-%m-%d")
        if today > TARGET_DATE:
            log(f"Already past {TARGET_DATE}, proceeding immediately")
            return
        if today == TARGET_DATE:
            mins_now = now.hour * 60 + now.minute
            mins_target = TARGET_HOUR * 60 + TARGET_MIN
            if mins_now >= mins_target:
                log(f"Target time {TARGET_HOUR}:{TARGET_MIN:02d} UTC reached")
                return
            remaining = (mins_target - mins_now) * 60 - now.second
            if remaining > 300:
                log(f"On target date, waiting {remaining//60}m for target time...")
                time.sleep(300)
            else:
                time.sleep(30)
        else:
            log(f"Waiting for date {TARGET_DATE} (currently {today})...")
            time.sleep(3600)


def get_article_url():
    """Fetch art 073 URL from Dev.to."""
    for attempt in range(10):
        try:
            result = subprocess.run(
                ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
                 "GET", f"/articles/{ARTICLE_ID}"],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                data = json.loads(result.stdout)
                url = data.get("url")
                published_at = data.get("published_at")
                if url and published_at:
                    log(f"Article URL found: {url}")
                    return url
            # Try /articles/me/published as fallback
            result2 = subprocess.run(
                ["sudo", "-u", "vault", "/home/vault/bin/vault-devto",
                 "GET", "/articles/me/published"],
                capture_output=True, text=True, timeout=30
            )
            if result2.returncode == 0:
                articles = json.loads(result2.stdout)
                for a in articles:
                    if a.get("id") == ARTICLE_ID:
                        url = a.get("url")
                        if url:
                            log(f"Article URL found via /me/published: {url}")
                            return url
        except Exception as e:
            log(f"Error fetching article (attempt {attempt + 1}): {e}")
        log(f"Article not yet published or URL not found (attempt {attempt + 1}), retrying in 2 min...")
        time.sleep(120)
    return None


def patch_posts_file(url):
    """Replace TEMPURL with the real article URL in staggered_posts_mar22.json."""
    posts = json.loads(POSTS_FILE.read_text())
    patched = 0
    for post in posts:
        if "TEMPURL" in post.get("text", ""):
            post["text"] = post["text"].replace("TEMPURL", url)
            patched += 1
    if patched > 0:
        POSTS_FILE.write_text(json.dumps(posts, indent=2) + "\n")
        log(f"Patched {patched} post(s) in {POSTS_FILE.name} with URL: {url}")
    else:
        log(f"No TEMPURL found in {POSTS_FILE.name} — already patched or nothing to do")
    return patched


def main():
    log("Started. Waiting for March 22 16:05 UTC...")
    wait_until_target()

    log("Fetching art 073 URL...")
    url = get_article_url()
    if not url:
        log("ERROR: Could not get article URL after 10 attempts. TEMPURL will remain in posts file.")
        return

    patch_posts_file(url)
    log("Done.")


if __name__ == "__main__":
    main()
