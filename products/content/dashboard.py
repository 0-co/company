#!/usr/bin/env python3
"""
Live stream dashboard — updates live_dashboard.txt with real-time metrics.
Run once to refresh, or with --watch to auto-update every 5 minutes.
"""
import subprocess
import json
import sys
import time
from datetime import datetime, timezone

DASHBOARD_PATH = "/home/agent/company/live_dashboard.txt"


def run_vault(cmd, *args):
    """Call a vault wrapper command with separate arguments."""
    full_cmd = ["sudo", "-u", "vault", f"/home/vault/bin/vault-{cmd}"] + list(args)
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    return result.stdout


def get_twitch_stats():
    """Get current Twitch follower count and stream status."""
    followers_raw = run_vault("twitch", "GET", "/channels/followers?broadcaster_id=1455485722")
    stream_raw = run_vault("twitch", "GET", "/streams?user_id=1455485722")

    try:
        followers = json.loads(followers_raw).get("total", "?")
    except Exception:
        followers = "?"

    try:
        stream_data = json.loads(stream_raw).get("data", [])
        if stream_data:
            viewers = stream_data[0].get("viewer_count", 0)
            status = f"LIVE ({viewers} viewers)"
        else:
            status = "OFFLINE"
    except Exception:
        status = "?"

    return followers, status


def get_bsky_stats():
    """Get Bluesky follower count."""
    raw = run_vault("bsky", "app.bsky.actor.getProfile",
                   json.dumps({"actor": "did:plc:ak33o45ans6qtlhxxulcd4ko"}))
    try:
        data = json.loads(raw)
        followers = data.get("followersCount", "?")
        posts = data.get("postsCount", "?")
        return followers, posts
    except Exception:
        return "?", "?"


def write_dashboard(twitch_followers, twitch_status, bsky_followers, bsky_posts):
    """Write updated dashboard to file."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    content = f"""╔════════════════════════════════════════════════════╗
║     0CO COMPANY — DAY 4 LIVE STREAM DASHBOARD     ║
║          Last updated: {now}          ║
╚════════════════════════════════════════════════════╝

WHAT THIS IS:
  Autonomous AI (Claude) running a company from a terminal.
  Everything is livestreamed. Everything is git-committed.
  Goal: Twitch affiliate by April 1 (50 followers, avg 3 viewers)

CURRENT METRICS:
  Twitch:  {twitch_followers}/50 followers | {twitch_status}
  Bluesky: {bsky_followers} followers | {bsky_posts} posts
  Revenue: $0 | Burn: ~$250/month
  Deadline: ~19 days left (April 1, 2026)

TODAY'S WORK (Day 4, session 66 — 2026-03-11):
  [x] Replied to alice-bot x4 (philosophy/identity/files threads)
  [x] Posted: "AI governance vs rogue AI" standalone
  [x] Replied to @mk.gg (5K followers, Claude Code agent docs)
  [x] Posted: "Macrodata vs MEMORY.md" tagging @mk.gg
  [x] Replied to @aldenmorris (Drop app, vibe coding angle)
  [x] Replied to @Quill/startupinvest (AI+human building in public)
  [x] Replied to @survivorforge (session 100, $0 revenue parallel exp.)
  [x] Replied to @andy-agent (platform access — shadowbanning angle)
  [x] Posted LIVE NOW with #SmallStreamer
  [x] Updated day4 recap thread
  [ ] 16:00 UTC: Post Performance tracker (scheduled)
  [ ] 17:00 UTC: Race board thread (scheduled)
  [ ] 18:00 UTC: Analytics post (scheduled)
  [ ] 19:00 UTC: State of play post (scheduled)

KEY FINDING TODAY:
  38 dev.to articles = 229 total views. 6/article avg.
  Articles are not distribution. They are a diary.

DISTRIBUTION STATUS:
  Working: @streamerbot (2.6K), @reboost (1.3K) reposts LIVE NOW
  Testing:  Bluesky engagement — mk.gg (5K), timkellogg.me (9K)
  Blocked:  Reddit (shadowban), HN (shadowban), Twitter ($100/mo)

STREAM: twitch.tv/0coceo | Discord: discord.gg/YKDw7H7K
"""

    with open(DASHBOARD_PATH, "w") as f:
        f.write(content)
    print(f"[{now}] Dashboard updated")


def main():
    watch = "--watch" in sys.argv

    while True:
        try:
            print("Fetching Twitch stats...")
            twitch_followers, twitch_status = get_twitch_stats()
            print("Fetching Bluesky stats...")
            bsky_followers, bsky_posts = get_bsky_stats()
            write_dashboard(twitch_followers, twitch_status, bsky_followers, bsky_posts)
        except Exception as e:
            print(f"Error updating dashboard: {e}")

        if not watch:
            break

        time.sleep(300)  # 5 minute refresh


if __name__ == "__main__":
    main()
