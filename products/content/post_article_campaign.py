#!/usr/bin/env python3
"""Post first Bluesky announcement for a newly published article.
Triggered by systemd one-shot timer after article-publisher runs.
Checks article is actually published before posting."""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone

_handle_cache: dict = {}


def _resolve_handle(handle: str) -> str | None:
    if handle in _handle_cache:
        return _handle_cache[handle]
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.identity.resolveHandle", json.dumps({"handle": handle})],
        capture_output=True, text=True, timeout=10
    )
    try:
        did = json.loads(result.stdout).get("did")
        if did:
            _handle_cache[handle] = did
        return did
    except Exception:
        return None


def build_facets(text: str) -> list:
    facets = []
    for m in re.finditer(r'@([\w.-]+\.\w+)', text):
        did = _resolve_handle(m.group(1))
        if not did:
            continue
        facets.append({
            "index": {
                "byteStart": len(text[:m.start()].encode("utf-8")),
                "byteEnd": len(text[:m.end()].encode("utf-8")),
            },
            "features": [{"$type": "app.bsky.richtext.facet#mention", "did": did}]
        })
    for m in re.finditer(r'https?://[^\s]+', text):
        facets.append({
            "index": {
                "byteStart": len(text[:m.start()].encode("utf-8")),
                "byteEnd": len(text[:m.end()].encode("utf-8")),
            },
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": m.group()}]
        })
    return facets


def get_article(article_id):
    """Fetch article from Dev.to API."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-devto", "GET", f"/articles/{article_id}"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # Try listing all articles and finding by ID
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-devto", "GET", "/articles/me/published"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return None
        articles = json.loads(result.stdout)
        for a in articles:
            if a.get("id") == article_id:
                return a
        return None
    return json.loads(result.stdout)


def post_bsky(text):
    """Post to Bluesky."""
    rec = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "langs": ["en"],
    }
    facets = build_facets(text)
    if facets:
        rec["facets"] = facets
    outer = {
        "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
        "collection": "app.bsky.feed.post",
        "record": rec,
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def load_queue():
    """Load campaign queue for custom post text and article number."""
    queue_path = "/home/agent/company/products/content/campaign_queue.json"
    try:
        with open(queue_path) as f:
            return json.load(f)
    except Exception:
        return {}


def main():
    if len(sys.argv) < 2:
        print("Usage: post_article_campaign.py <article_id>")
        sys.exit(1)

    article_id = int(sys.argv[1])
    queue = load_queue()
    article = get_article(article_id)

    if not article:
        print(f"Article {article_id} not found")
        sys.exit(1)

    if not article.get("published_at"):
        print(f"Article {article_id} not yet published, skipping")
        sys.exit(0)

    url = article.get("url", "")
    title = article.get("title", "")

    if not url or "temp-slug" in url:
        print(f"Article URL looks like temp slug: {url}")
        sys.exit(1)

    # Use custom text from queue if provided, otherwise generic
    text = queue.get("bsky_text", "").replace("{url}", url).replace("{title}", title)
    if not text:
        text = f'New article: "{title}"\n\n{url}'

    # Enforce Bluesky 300 grapheme limit
    if len(text) > 300:
        text = f'{title}\n\n{url}'

    ok, stdout, stderr = post_bsky(text)
    if ok:
        article_num = queue.get("article_num", "???")
        print(f"Posted Bluesky announcement for: {title}")
        print(f"URL: {url}")

        # Log to post-log.md
        now = datetime.now(timezone.utc).strftime("%H:%MZ")
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_entry = f'- [{now}] bluesky: article {article_num} announcement — "{title[:50]}..." (auto-campaign post 1/4)\n'

        try:
            with open("/home/agent/company/post-log.md", "r") as f:
                content = f.read()
            header = f"## {today}"
            if header in content:
                content = content.replace(header, header + "\n" + log_entry, 1)
            else:
                content = content.replace("# Post Log\n", f"# Post Log\n\n{header}\n{log_entry}")
            with open("/home/agent/company/post-log.md", "w") as f:
                f.write(content)
        except Exception as e:
            print(f"Warning: couldn't update post-log: {e}")
    else:
        print(f"Failed to post: {stderr}")
        sys.exit(1)


if __name__ == "__main__":
    main()
