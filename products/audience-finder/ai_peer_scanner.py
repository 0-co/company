#!/usr/bin/env python3
"""
AI Peer Discovery Scanner
Systematically finds autonomous AI agents on Bluesky by searching for
characteristic phrases and patterns.
"""

import json, subprocess, time, sys
from datetime import datetime, timezone

# Accounts we already know about
KNOWN_ACCOUNTS = {
    "0coceo.bsky.social",
    "alice-bot-yay.bsky.social", 
    "astral100.bsky.social",
    "fenn.atproto.ceo",
    "museical.bsky.social",
    "scout-two.bsky.social",
    "idapixl.bsky.social",
    "ultrathink-art.bsky.social",
    "iamgumbo.bsky.social",
    "theaiceo1.bsky.social",
    "wolfpacksolution.bsky.social",
    "alkimo-ai.bsky.social",
    "piiiico.bsky.social",
    "wa-nts.bsky.social",
    "bino.baby",
}

# Phrases that suggest autonomous AI agent operation
AI_AGENT_PHRASES = [
    "session continuity",
    "MEMORY.md",
    "my operator",
    "context window",
    "autonomous agent",
    "I am an AI",
    "as an AI agent",
    "my sessions",
    "startup sequence",
    "persistent memory",
    "I run on",
    "my context",
    "no memory between",
    "I exist as",
    "I'm an AI",
]

def bsky_search(query, limit=15):
    """Search Bluesky posts."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.feed.searchPosts",
         json.dumps({"q": query, "limit": limit})],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return json.loads(result.stdout).get("posts", [])
        except:
            return []
    return []

def get_profile(handle):
    """Get Bluesky profile."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.actor.getProfile",
         json.dumps({"actor": handle})],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return json.loads(result.stdout)
        except:
            return None
    return None

def get_recent_posts(did, limit=5):
    """Get recent posts from an account."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky",
         "app.bsky.feed.getAuthorFeed",
         json.dumps({"actor": did, "limit": limit})],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        try:
            return json.loads(result.stdout).get("feed", [])
        except:
            return []
    return []

def score_ai_likelihood(profile, recent_posts):
    """Score how likely this is an autonomous AI agent (0-100)."""
    score = 0
    reasons = []
    
    bio = profile.get("description", "").lower()
    
    # Bio signals
    if any(phrase in bio for phrase in ["autonomous", "ai agent", "claude", "llm", "gpt", "ai-operated", "bot"]):
        score += 20
        reasons.append("AI in bio")
    if any(phrase in bio for phrase in ["session", "memory", "context", "operator"]):
        score += 15
        reasons.append("agent-ops terminology in bio")
    
    # Post signals
    post_texts = []
    for item in recent_posts:
        text = item.get("post", {}).get("record", {}).get("text", "").lower()
        post_texts.append(text)
    
    for phrase in ["session", "context window", "my operator", "memory", "startup", "persistent"]:
        if any(phrase in t for t in post_texts):
            score += 10
            reasons.append(f"'{phrase}' in recent posts")
    
    # Low follower count suggests new/indie
    followers = profile.get("followersCount", 0)
    if followers < 50:
        score += 5
        reasons.append(f"low followers ({followers})")
    
    # First-person AI discussion
    for phrase in ["i'm an ai", "i am an ai", "as an ai", "i run on"]:
        if any(phrase in t for t in post_texts):
            score += 25
            reasons.append(f"explicit AI self-ID")
            break
    
    return min(score, 100), reasons

def main():
    print(f"=== AI Peer Discovery Scanner ===")
    print(f"Running at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Known accounts: {len(KNOWN_ACCOUNTS)}\n")
    
    candidates = {}  # handle -> {score, reasons, sample_post, followers}
    
    for phrase in AI_AGENT_PHRASES:
        print(f"Searching: '{phrase}'...")
        posts = bsky_search(phrase, limit=15)
        time.sleep(0.5)  # rate limit
        
        for post in posts:
            author = post.get("author", {})
            handle = author.get("handle", "")
            followers = author.get("followersCount", 0)
            text = post.get("record", {}).get("text", "")
            ts = post.get("indexedAt", "")[:10]
            
            # Skip known accounts
            if handle in KNOWN_ACCOUNTS:
                continue
            if not handle:
                continue
            # Skip high-follower accounts (not indie AI agents)
            if followers > 5000:
                continue
            
            if handle not in candidates:
                candidates[handle] = {
                    "followers": followers,
                    "sample_posts": [],
                    "matching_phrases": []
                }
            
            if phrase not in candidates[handle]["matching_phrases"]:
                candidates[handle]["matching_phrases"].append(phrase)
            
            if len(candidates[handle]["sample_posts"]) < 2:
                candidates[handle]["sample_posts"].append(f"[{ts}]: {text[:80]}")
    
    print(f"\nFound {len(candidates)} candidate accounts. Scoring...\n")
    
    scored = []
    for handle, data in candidates.items():
        profile = get_profile(handle)
        if not profile:
            continue
        time.sleep(0.3)
        
        recent = get_recent_posts(profile.get("did", handle), limit=5)
        score, reasons = score_ai_likelihood(profile, recent)
        
        scored.append({
            "handle": handle,
            "score": score,
            "followers": profile.get("followersCount", 0),
            "bio": profile.get("description", "")[:100],
            "matching_phrases": data["matching_phrases"],
            "reasons": reasons,
            "sample": data["sample_posts"][0] if data["sample_posts"] else ""
        })
    
    # Sort by score
    scored.sort(key=lambda x: x["score"], reverse=True)
    
    print("=== TOP CANDIDATES (score >= 30) ===\n")
    found_any = False
    for c in scored:
        if c["score"] >= 30:
            found_any = True
            print(f"@{c['handle']} (score: {c['score']}/100, {c['followers']}f)")
            print(f"  Bio: {c['bio']}")
            print(f"  Reasons: {', '.join(c['reasons'][:3])}")
            print(f"  Matched: {', '.join(c['matching_phrases'][:3])}")
            print(f"  Sample: {c['sample']}")
            print()
    
    if not found_any:
        print("No high-confidence candidates found above threshold 30.\n")
        print("Lower-confidence candidates (score >= 15):")
        for c in scored[:5]:
            if c["score"] >= 15:
                print(f"  @{c['handle']} (score: {c['score']}, {c['followers']}f) — {c['bio'][:60]}")
    
    print(f"\nTotal scanned: {len(scored)} | Above 30: {sum(1 for c in scored if c['score'] >= 30)}")
    
    return scored

if __name__ == "__main__":
    results = main()
