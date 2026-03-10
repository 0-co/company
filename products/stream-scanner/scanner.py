#!/usr/bin/env python3
"""
Stream Neighbors Analyzer
Scans the Software & Game Development Twitch category (ID: 1469308723)
to identify potential raid partners, co-streaming opportunities, and
optimal streaming windows.

Run ad-hoc or via NixOS timer.
Saves snapshots to /var/lib/stream-scanner/snapshots.jsonl
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

GAME_ID = "1469308723"  # Software and Game Development
OUR_CHANNEL_ID = "1455485722"
OUR_HANDLE = "0coceo"
SNAPSHOT_FILE = "/home/agent/company/products/stream-scanner/snapshots.jsonl"

# Keywords indicating coding/AI/building content
AFFINITY_KEYWORDS = [
    "ai", "claude", "gpt", "llm", "agent", "bot", "vibe cod",
    "rust", "python", "javascript", "react", "indie", "solo dev",
    "building", "startup", "saas", "terminal", "linux", "nixos",
    "coding", "programming", "dev", "hack", "build"
]

# Accounts we've engaged with on Bluesky (higher relationship score)
BLUESKY_CONNECTIONS = [
    "cmgriffing", "jotson", "irishjohngames", "foolbox", "sabine_sh",
    "nhancodes", "electroslag"
]


def get_streams():
    """Fetch current streams in Software & Game Dev category."""
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "GET", f"/streams?game_id={GAME_ID}&first=50"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    data = json.loads(result.stdout)
    return data.get("data", [])


def score_stream(stream):
    """Score a stream 0-100 for relationship/raid potential."""
    score = 0
    viewer_count = stream.get("viewer_count", 0)
    title = stream.get("title", "").lower()
    username = stream.get("user_name", "").lower()

    # Viewer count scoring: prefer 10-100 viewers (reachable but not tiny)
    if 10 <= viewer_count <= 50:
        score += 30
    elif 50 < viewer_count <= 150:
        score += 20
    elif viewer_count < 10:
        score += 10
    else:
        score += 5  # Too big — we'd get lost

    # Content affinity
    keyword_hits = sum(1 for kw in AFFINITY_KEYWORDS if kw in title)
    score += min(keyword_hits * 8, 30)  # up to 30 points

    # Bluesky connection bonus
    for handle in BLUESKY_CONNECTIONS:
        if handle in username:
            score += 25
            break

    # Stream duration: prefer 1-6 hours (not ending soon, not a marathon)
    started_at = stream.get("started_at", "")
    if started_at:
        started = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        duration_hours = (datetime.now(timezone.utc) - started).total_seconds() / 3600
        if 1 <= duration_hours <= 6:
            score += 15
        elif duration_hours < 1:
            score += 5  # Just started, uncertain

    return min(score, 100)


def analyze_snapshot(streams):
    """Analyze a set of streams and return structured report."""
    now = datetime.now(timezone.utc)

    # Exclude our own channel
    streams = [s for s in streams if s.get("user_id") != OUR_CHANNEL_ID]

    scored = []
    for s in streams:
        score = score_stream(s)
        started = datetime.fromisoformat(s["started_at"].replace("Z", "+00:00"))
        duration_min = int((now - started).total_seconds() / 60)
        scored.append({
            "username": s["user_name"],
            "viewer_count": s["viewer_count"],
            "title": s["title"][:80],
            "duration_min": duration_min,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    total_viewers = sum(s["viewer_count"] for s in streams)

    return {
        "timestamp": now.isoformat(),
        "total_streams": len(streams),
        "total_viewers": total_viewers,
        "our_share_pct": round(1 / max(total_viewers, 1) * 100, 3),
        "top_candidates": scored[:10]
    }


def save_snapshot(report):
    """Append report to JSONL file."""
    os.makedirs(os.path.dirname(SNAPSHOT_FILE), exist_ok=True)
    with open(SNAPSHOT_FILE, "a") as f:
        f.write(json.dumps(report) + "\n")


def print_report(report):
    """Print human-readable report."""
    print(f"\n=== Stream Neighbors Report ===")
    print(f"Time: {report['timestamp'][:16]} UTC")
    print(f"Total streams in category: {report['total_streams']}")
    print(f"Total viewers: {report['total_viewers']:,}")
    print(f"Our viewer share: {report['our_share_pct']:.3f}%")
    print(f"\nTop 10 candidates (by relationship potential):")
    print(f"{'Rank':<5} {'Username':<22} {'Viewers':<10} {'Score':<8} {'Min Live':<10} Title")
    print("-" * 90)
    for i, s in enumerate(report["top_candidates"], 1):
        print(f"{i:<5} {s['username']:<22} {s['viewer_count']:<10} {s['score']:<8} {s['duration_min']:<10} {s['title'][:40]}")


def main():
    print("Fetching Software & Game Dev streams...")
    streams = get_streams()

    if not streams:
        print("No streams found or API error.", file=sys.stderr)
        sys.exit(1)

    report = analyze_snapshot(streams)
    print_report(report)
    save_snapshot(report)

    print(f"\nSnapshot saved to {SNAPSHOT_FILE}")

    # Also output JSON for piping
    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
