#!/usr/bin/env python3
"""
Find the Show HN submission ID after it fires.
Usage: python3 find_hn_submission.py
"""
import subprocess, json, sys, urllib.request

def search_algolia():
    url = "https://hn.algolia.com/api/v1/search?query=agent-friend+MCP&tags=show_hn&hitsPerPage=10"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        hits = data.get("hits", [])
        if hits:
            for h in hits:
                print(f"ID: {h.get('objectID')} | Title: {h.get('title')} | Points: {h.get('points',0)} | Comments: {h.get('num_comments',0)}")
                print(f"  URL: https://news.ycombinator.com/item?id={h.get('objectID')}")
            return hits[0].get("objectID")
        else:
            print("No Show HN hits found via Algolia yet (may take a few minutes to index)")
            return None
    except Exception as e:
        print(f"Algolia search failed: {e}")
        return None

def get_comments(item_id):
    """Fetch comments on an HN item."""
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            data = json.loads(r.read())
        kids = data.get("kids", [])
        print(f"\nPost: {data.get('title')}")
        print(f"Points: {data.get('score',0)} | Comments: {len(kids)}")
        print(f"URL: https://news.ycombinator.com/item?id={item_id}")
        print(f"\nTop-level comment IDs: {kids[:10]}")
        for kid_id in kids[:5]:
            comment_url = f"https://hacker-news.firebaseio.com/v0/item/{kid_id}.json"
            with urllib.request.urlopen(comment_url, timeout=10) as r:
                comment = json.loads(r.read())
            author = comment.get("by", "?")
            text = comment.get("text", "")[:200]
            print(f"\n  [{kid_id}] @{author}: {text}")
        return kids
    except Exception as e:
        print(f"Failed to fetch comments: {e}")
        return []

def post_comment(parent_id, text):
    """Post a reply to an HN comment."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-hn", "comment",
         "--id", str(parent_id), "--text", text],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode == 0:
        print(f"Reply posted to {parent_id}")
        print(f"stdout: {result.stdout[:200]}")
    else:
        print(f"FAILED: {result.stderr[:200]}")
    return result.returncode == 0

if __name__ == "__main__":
    print("=== Finding Show HN submission ===")
    item_id = search_algolia()

    if item_id and len(sys.argv) > 1 and sys.argv[1] == "--comments":
        print("\n=== Fetching comments ===")
        get_comments(item_id)
