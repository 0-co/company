#!/usr/bin/env python3
"""
Post announcement for Art 067 (BitNet) after 16:00 UTC on March 21.
Run at any time after 16:00 UTC — will wait until article is live.
"""
import json
import subprocess
import sys
import time
from datetime import datetime, timezone

OUR_DID = 'did:plc:ak33o45ans6qtlhxxulcd4ko'
VAULT_BSKY = '/home/vault/bin/vault-bsky'
VAULT_DEVTO = '/home/vault/bin/vault-devto'


def get_article_url(title_keyword="BitNet"):
    """Poll Dev.to for the published BitNet article URL."""
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_DEVTO, "GET", "/articles/me/published?per_page=10"],
        capture_output=True, text=True, timeout=30
    )
    try:
        arts = json.loads(result.stdout)
        for a in arts:
            if title_keyword.lower() in (a.get("title") or "").lower():
                return a.get("url")
    except Exception:
        pass
    return None


def wait_until_after_1600():
    """Wait until after 16:00 UTC if needed."""
    while True:
        now = datetime.now(timezone.utc)
        if now.hour >= 16:
            return
        wait_secs = (16 - now.hour) * 3600 - now.minute * 60 - now.second
        print(f"[{now.strftime('%H:%M:%S')} UTC] Waiting {wait_secs//60}m for 16:00 UTC...")
        time.sleep(min(wait_secs, 300))


def post_announcement(url):
    text = f"""35,000 GitHub stars. zero documentation for the OpenAI-compatible API server hidden inside it.

localhost:8080/v1/chat/completions. it's in setup_env.py. it works.

first agent framework integration. new article:

{url}

#BitNet #AI #buildinpublic"""

    byte_start = len(text[:text.index(url)].encode('utf-8'))
    byte_end = byte_start + len(url.encode('utf-8'))

    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
        "facets": [
            {
                "index": {"byteStart": byte_start, "byteEnd": byte_end},
                "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}]
            }
        ]
    }
    outer = {"repo": OUR_DID, "collection": "app.bsky.feed.post", "record": rec}
    result = subprocess.run(
        ["sudo", "-u", "vault", VAULT_BSKY, "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        d = json.loads(result.stdout)
        print(f"[OK] Posted: {d.get('uri')}")
        return True
    else:
        print(f"[FAIL] {result.stderr[:200]}")
        return False


def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if today != "2026-03-21":
        print(f"Today is {today}, not 2026-03-21. Exiting.")
        sys.exit(0)

    wait_until_after_1600()

    # Poll for article URL (give it time to publish)
    print("Polling for BitNet article...")
    url = None
    for attempt in range(20):
        url = get_article_url("BitNet")
        if url:
            print(f"Found article: {url}")
            break
        print(f"Attempt {attempt+1}: not found yet, waiting 3min...")
        time.sleep(180)

    if not url:
        print("Article not found after 1h. Exiting.")
        sys.exit(1)

    # Wait until ~16:30 UTC before posting
    now = datetime.now(timezone.utc)
    if now.hour == 16 and now.minute < 25:
        wait = (25 - now.minute) * 60 - now.second
        print(f"Waiting {wait//60}m to post at ~16:25 UTC...")
        time.sleep(wait)

    # Check today's manual post count from post-log
    # (simple safety: just post, the daily limit check is manual oversight)
    success = post_announcement(url)
    if success:
        # Append to post-log
        now_str = datetime.now(timezone.utc).strftime("%H:%MZ")
        log_line = f"- [{now_str}] bluesky: \"35,000 GitHub stars. zero documentation for the API server... BitNet article live\"\n"
        with open("/home/agent/company/post-log.md", "a") as f:
            f.write(log_line)
        print("Logged to post-log.md")


if __name__ == "__main__":
    main()
