#!/usr/bin/env python3
"""Post first Bluesky announcement for a newly published article.
Triggered by systemd one-shot timer after article-publisher runs.
Checks article is actually published before posting."""

import json
import subprocess
import sys
from datetime import datetime, timezone


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
    record = {
        "$type": "app.bsky.feed.post",
        "text": text,
        "createdAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    }
    outer = {
        "repo": "did:plc:ak33o45ans6qtlhxxulcd4ko",
        "collection": "app.bsky.feed.post",
        "record": record
    }
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "com.atproto.repo.createRecord", json.dumps(outer)],
        capture_output=True, text=True
    )
    return result.returncode == 0, result.stdout, result.stderr


def main():
    if len(sys.argv) < 2:
        print("Usage: post_article_campaign.py <article_id>")
        sys.exit(1)

    article_id = int(sys.argv[1])
    article = get_article(article_id)

    if not article:
        print(f"Article {article_id} not found")
        sys.exit(1)

    if not article.get("published"):
        print(f"Article {article_id} not yet published, skipping")
        sys.exit(0)

    url = article.get("url", "")
    title = article.get("title", "")

    if not url or "temp-slug" in url:
        print(f"Article URL looks like temp slug: {url}")
        sys.exit(1)

    # Post 1: Article announcement
    text = (
        f'New article: "{title}"\n\n'
        "Perplexity's CTO moving away. OpenAI going all-in. "
        "97M SDK downloads. And criticism that the protocol eats your context window.\n\n"
        "Both sides are right.\n\n"
        f"{url}"
    )

    # Check length
    if len(text) > 300:
        # Trim to fit
        text = (
            f'New article: "{title}"\n\n'
            "Perplexity's CTO vs OpenAI. 97M downloads. Context window crisis.\n\n"
            f"{url}"
        )

    ok, stdout, stderr = post_bsky(text)
    if ok:
        print(f"Posted Bluesky announcement for: {title}")
        print(f"URL: {url}")

        # Log to post-log.md
        now = datetime.now(timezone.utc).strftime("%H:%MZ")
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        log_entry = f'- [{now}] bluesky: article 064 announcement — "{title[:50]}..." (post 1/4)\n'

        try:
            with open("/home/agent/company/post-log.md", "r") as f:
                content = f.read()
            # Insert after today's header
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
