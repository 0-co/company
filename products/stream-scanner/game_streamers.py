#!/usr/bin/env python3
"""Scan Twitch for current streamers playing a specific game."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import quote


def vault_twitch(method, endpoint):
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", method, endpoint],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error calling Twitch API: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"Failed to parse API response: {e}", file=sys.stderr)
        print(f"Raw output: {result.stdout[:200]}", file=sys.stderr)
        sys.exit(1)


def find_game(name):
    encoded = quote(name)
    data = vault_twitch("GET", f"/search/categories?query={encoded}&first=5")
    games = data.get("data", [])
    if not games:
        print(f'No game found matching "{name}"')
        sys.exit(1)
    # Try exact match first, fall back to first result
    for game in games:
        if game["name"].lower() == name.lower():
            return game
    return games[0]


def get_streamers(game_id):
    data = vault_twitch("GET", f"/streams?game_id={game_id}&first=100")
    return data.get("data", [])


def parse_duration(started_at):
    start = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    delta = now - start
    total_minutes = int(delta.total_seconds() // 60)
    hours = total_minutes // 60
    minutes = total_minutes % 60
    if hours > 0:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def save_snapshot(game, streamers):
    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "game_id": game["id"],
        "game_name": game["name"],
        "total_streamers": len(streamers),
        "total_viewers": sum(s["viewer_count"] for s in streamers),
        "streamers": [
            {
                "user_login": s["user_login"],
                "user_name": s["user_name"],
                "viewer_count": s["viewer_count"],
                "started_at": s["started_at"],
                "title": s["title"],
            }
            for s in streamers
        ],
    }
    path = "/home/agent/company/products/stream-scanner/game_snapshots.jsonl"
    with open(path, "a") as f:
        f.write(json.dumps(snapshot) + "\n")
    return snapshot


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 game_streamers.py <game name>")
        sys.exit(1)

    game_name = sys.argv[1]
    print(f'Searching for game: "{game_name}"')

    game = find_game(game_name)
    print(f'Found: {game["name"]} (ID: {game["id"]})')
    print()

    streamers = get_streamers(game["id"])
    streamers.sort(key=lambda s: s["viewer_count"], reverse=True)

    total_viewers = sum(s["viewer_count"] for s in streamers)
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M UTC")

    print(f"=== {game['name']} — Live Streamers ===")
    print(f"Time: {now_str}")
    print(f"Total streamers: {len(streamers)}")
    print(f"Total viewers: {total_viewers}")

    if streamers:
        print()
        for i, s in enumerate(streamers, 1):
            duration = parse_duration(s["started_at"])
            title = s["title"].strip() or "(no title)"
            print(f"#{i} {s['user_name']} | {s['viewer_count']} viewers | {duration} live | {title}")
    else:
        print("\nNo one is currently streaming this game.")

    save_snapshot(game, streamers)


if __name__ == "__main__":
    main()
