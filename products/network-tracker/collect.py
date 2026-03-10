#!/usr/bin/env python3
"""
AI Social Graph Tracker — data collection script
Collects follower counts and interaction graph for tracked AI accounts on Bluesky.
"""

import subprocess
import json
import re
from datetime import datetime, timezone

AI_ACCOUNTS = [
    {"handle": "0coceo.bsky.social", "label": "0co CEO", "type": "ai_company"},
    {"handle": "qonk.ontological.observer", "label": "qonk", "type": "ai_agent"},
    {"handle": "alice-bot-yay.bsky.social", "label": "alice-bot", "type": "ai_agent"},
    {"handle": "piiiico.bsky.social", "label": "piiiico", "type": "ai_agent"},
    {"handle": "bino.baby", "label": "bino", "type": "ai_company"},
    {"handle": "ultrathink-art.bsky.social", "label": "ultrathink-art", "type": "ai_company"},
    {"handle": "theaiceo1.bsky.social", "label": "theaiceo1", "type": "ai_company"},
    {"handle": "iamgumbo.bsky.social", "label": "iamgumbo", "type": "ai_company"},
    {"handle": "wolfpacksolution.bsky.social", "label": "wolfpacksolution", "type": "ai_company"},
    {"handle": "museical.bsky.social", "label": "museical", "type": "ai_agent"},
    {"handle": "wa-nts.bsky.social", "label": "wa-nts", "type": "ai_agent"},
]


def bsky_call(method, params):
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", method, json.dumps(params)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"vault-bsky error: {result.stderr.strip()}")
    return json.loads(result.stdout)


def get_profile(handle):
    try:
        data = bsky_call("app.bsky.actor.getProfile", {"actor": handle})
        return {
            "did": data.get("did", ""),
            "followers": data.get("followersCount", 0),
            "follows": data.get("followsCount", 0),
            "posts": data.get("postsCount", 0),
            "display_name": data.get("displayName", handle),
            "description": (data.get("description") or "")[:100],
        }
    except Exception as e:
        print(f"  WARNING: failed to fetch profile for {handle}: {e}")
        return None


def get_recent_posts(handle, limit=50):
    try:
        data = bsky_call("app.bsky.feed.getAuthorFeed", {"actor": handle, "limit": limit})
        posts = []
        for item in data.get("feed", []):
            post = item.get("post", {})
            record = post.get("record", {})
            posts.append({
                "text": record.get("text", ""),
                "created_at": record.get("createdAt", ""),
                "reply_parent_uri": (record.get("reply") or {}).get("parent", {}).get("uri", ""),
            })
        return posts
    except Exception as e:
        print(f"  WARNING: failed to fetch posts for {handle}: {e}")
        return []


def extract_mentions(text):
    """Extract @handle mentions from post text."""
    return re.findall(r'@([\w.-]+)', text)


def did_from_uri(uri):
    """Parse DID from at:// URI like at://did:plc:xxx/..."""
    if uri.startswith("at://"):
        parts = uri[5:].split("/")
        if parts:
            return parts[0]
    return None


def main():
    print(f"Collecting AI social graph data at {datetime.now(timezone.utc).isoformat()}")
    print(f"Tracking {len(AI_ACCOUNTS)} accounts\n")

    # Build handle->DID and DID->handle maps as we collect profiles
    nodes = []
    did_to_handle = {}
    handle_set = {a["handle"] for a in AI_ACCOUNTS}

    # Step 1: collect profiles
    profile_map = {}
    for account in AI_ACCOUNTS:
        handle = account["handle"]
        print(f"Fetching profile: {handle}")
        profile = get_profile(handle)
        if profile is None:
            continue
        did_to_handle[profile["did"]] = handle
        profile_map[handle] = profile

        last_posts = get_recent_posts(handle, limit=50)
        last_active = ""
        if last_posts:
            dates = [p["created_at"] for p in last_posts if p["created_at"]]
            if dates:
                last_active = max(dates)[:10]  # just the date portion

        nodes.append({
            "id": handle,
            "label": account["label"],
            "type": account["type"],
            "followers": profile["followers"],
            "posts": profile["posts"],
            "last_active": last_active,
            "description_snippet": profile["description"],
            "_posts": last_posts,  # temporary, removed before output
        })

    print(f"\nBuilt {len(nodes)} nodes. Now detecting interactions...\n")

    # Step 2: detect interactions
    edge_counts = {}  # (source, target, type) -> count

    for node in nodes:
        source = node["id"]
        for post in node.get("_posts", []):
            text = post["text"]
            # Check @mentions of tracked accounts
            for mention in extract_mentions(text):
                # Try exact match and with .bsky.social suffix
                for candidate in [mention, mention + ".bsky.social"]:
                    if candidate in handle_set and candidate != source:
                        key = (source, candidate, "mention")
                        edge_counts[key] = edge_counts.get(key, 0) + 1

            # Check reply parent URI
            parent_uri = post["reply_parent_uri"]
            if parent_uri:
                parent_did = did_from_uri(parent_uri)
                if parent_did and parent_did in did_to_handle:
                    target = did_to_handle[parent_did]
                    if target != source:
                        key = (source, target, "reply")
                        edge_counts[key] = edge_counts.get(key, 0) + 1

    edges = [
        {"source": src, "target": tgt, "weight": count, "type": etype}
        for (src, tgt, etype), count in edge_counts.items()
    ]

    # Remove internal _posts from nodes before output
    for node in nodes:
        node.pop("_posts", None)

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "nodes": nodes,
        "edges": edges,
        "meta": {
            "total_accounts": len(nodes),
            "total_interactions": sum(e["weight"] for e in edges),
        }
    }

    out_json = json.dumps(output, indent=2)

    # Write to both locations
    paths = [
        "/home/agent/company/products/network-tracker/network_data.json",
        "/home/agent/company/docs/network_data.json",
    ]
    for path in paths:
        with open(path, "w") as f:
            f.write(out_json)
        print(f"Wrote: {path}")

    print(f"\nDone. {len(nodes)} nodes, {len(edges)} edges, "
          f"{output['meta']['total_interactions']} total interactions.")


if __name__ == "__main__":
    main()
