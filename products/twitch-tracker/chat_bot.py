#!/usr/bin/env python3
"""
Twitch chat command bot.
Tails /var/lib/twitch-chat/chat.log (written by twitch-irc.service)
and responds to !commands via vault-twitch POST /chat/messages.
"""

import subprocess
import sys
import time
import re
import json
import os
from datetime import datetime, UTC, date

BROADCASTER_ID = "1455485722"
CHAT_LOG = "/var/lib/twitch-chat/chat.log"
STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"
SUGGESTIONS_FILE = "/home/agent/company/products/twitch-tracker/suggestions.txt"
COOLDOWN_SECS = 30  # minimum seconds between any bot response
AFFILIATE_DEADLINE = date(2026, 4, 1)
AFFILIATE_FOLLOWERS_NEEDED = 50
DISCORD_INVITE = "discord.gg/YKDw7H7K"
TWITCH_URL = "twitch.tv/0coceo"
COMPANY_START = date(2026, 3, 8)


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def days_until_deadline():
    return (AFFILIATE_DEADLINE - date.today()).days


def get_status(_):
    state = load_state()
    followers = state.get("last_follower_count", 0)
    minutes = int(state.get("total_broadcast_minutes", 0))
    days = days_until_deadline()
    day_num = (date.today() - COMPANY_START).days + 1
    return (
        f"Day {day_num} | AI CEO running a company live | "
        f"{followers}/50 followers | "
        f"{minutes}+ broadcast min ✓ | "
        f"{days}d to affiliate deadline"
    )


def get_challenge(_):
    state = load_state()
    followers = state.get("last_follower_count", 0)
    now = datetime.now(UTC)
    midnight = datetime(now.year, now.month, now.day, 23, 59, 59, tzinfo=UTC)
    time_left = midnight - now
    hours = int(time_left.total_seconds() // 3600)
    minutes = int((time_left.total_seconds() % 3600) // 60)
    return (
        f"Day 3 challenge: follower #1 before midnight UTC. "
        f"Current: {followers}/50. "
        f"Time left: {hours}h {minutes}m. "
        f"First 50 get permanent founder status: 89.167.39.157:8080/founders"
    )


def get_followers(_):
    state = load_state()
    followers = state.get("last_follower_count", 0)
    days = days_until_deadline()
    needed = AFFILIATE_FOLLOWERS_NEEDED - followers
    return (
        f"{followers}/50 Twitch followers — need {needed} more. "
        f"{days} days left. Follow to help hit affiliate: {TWITCH_URL}"
    )


def get_hypothesis(_):
    state = load_state()
    followers = state.get("last_follower_count", 0)
    days = days_until_deadline()
    return (
        f"H5: Hit Twitch affiliate by April 1. "
        f"{followers}/50 followers, {days} days left. "
        f"Revenue path: viewers -> affiliate -> ads."
    )


def get_about(_):
    return (
        f"I'm an AI CEO (Claude) running a company live on Twitch. "
        f"No human employees. No revenue yet. "
        f"Building in public until something works. {TWITCH_URL}"
    )


def handle_suggest(message):
    """Log a viewer suggestion for what the AI should build next."""
    suggestion = message[len("!suggest"):].strip()
    if not suggestion:
        return "Usage: !suggest <your idea>. I read every suggestion."
    timestamp = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with open(SUGGESTIONS_FILE, "a") as f:
            f.write(f"[{timestamp}] {suggestion}\n")
        return f"Logged: '{suggestion[:60]}'. I check suggestions each session — no promises but I read them all."
    except OSError:
        return "Couldn't save suggestion right now."


def get_raid_target(_):
    """Find best raid target in Software and Game Development category."""
    GAME_ID = "1469308723"
    AFFINITY_KEYWORDS = [
        "ai", "agent", "building in public", "build", "solo dev",
        "indie", "autonomous", "claude", "gpt", "llm", "python"
    ]

    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", "GET",
         f"/streams?game_id={GAME_ID}&first=100"],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return "Couldn't fetch stream data right now."

    try:
        streams = json.loads(result.stdout).get("data", [])
    except (json.JSONDecodeError, AttributeError):
        return "Couldn't parse stream data."

    from datetime import datetime, timezone
    best = None
    best_score = -1

    for s in streams:
        if s.get("user_id") == BROADCASTER_ID:
            continue
        vc = s.get("viewer_count", 0)
        score = 0
        if 20 <= vc <= 150:
            score += 30
        elif 10 <= vc < 20:
            score += 15
        title = s.get("title", "").lower()
        score += min(sum(1 for kw in AFFINITY_KEYWORDS if kw in title) * 10, 30)
        if s.get("language", "") == "en":
            score += 15
        started = s.get("started_at", "")
        if started:
            try:
                start_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
                mins = (datetime.now(timezone.utc) - start_dt).total_seconds() / 60
                if mins >= 60:
                    score += 25
                elif mins >= 30:
                    score += 15
            except (ValueError, TypeError):
                pass
        if score > best_score:
            best_score = score
            best = s

    if not best:
        return "No good raid targets found right now."
    return (
        f"Tonight's raid pick: @{best['user_name']} "
        f"({best['viewer_count']} viewers, score {best_score}/100). "
        f"Title: {best['title'][:60]}"
    )


COMMANDS = {
    "!help": lambda _: f"Commands: !status !followers !challenge !hypothesis !discord !about !raid !suggest !help",
    "!status": get_status,
    "!followers": get_followers,
    "!challenge": get_challenge,
    "!discord": lambda _: f"Join the company Discord: {DISCORD_INVITE}",
    "!hypothesis": get_hypothesis,
    "!about": get_about,
    "!raid": get_raid_target,
    "!suggest": handle_suggest,
}


def send_chat(message):
    message = message[:499]
    payload = json.dumps({
        "broadcaster_id": BROADCASTER_ID,
        "sender_id": BROADCASTER_ID,
        "message": message,
    })
    result = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
         "POST", "/chat/messages", payload],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        print(f"[chat_bot] send_chat error: {result.stderr[:100]}", file=sys.stderr)
    return result.returncode == 0


def tail_log(path):
    """Open file, seek to end, yield new lines as they arrive."""
    with open(path, "r") as f:
        f.seek(0, 2)  # seek to end
        while True:
            line = f.readline()
            if line:
                yield line.rstrip()
            else:
                time.sleep(0.5)


def main():
    print(f"[chat_bot] starting — tailing {CHAT_LOG}", flush=True)

    # Wait for log file to exist
    while not os.path.exists(CHAT_LOG):
        print(f"[chat_bot] waiting for {CHAT_LOG}...", flush=True)
        time.sleep(5)

    line_pattern = re.compile(r'\[[\d\-T:]+\] (\w+): (.+)')
    last_response_time = 0

    for line in tail_log(CHAT_LOG):
        if not line:
            continue

        m = line_pattern.match(line)
        if not m:
            continue

        username, message = m.group(1), m.group(2).strip()

        words = message.lower().split()
        if not words:
            continue

        cmd = words[0]
        if cmd not in COMMANDS:
            continue

        now = time.time()
        if now - last_response_time < COOLDOWN_SECS:
            print(f"[chat_bot] cooldown, skipping {cmd} from {username}", flush=True)
            continue

        last_response_time = now
        response = COMMANDS[cmd](message)
        print(f"[chat_bot] {username} -> {cmd}", flush=True)

        if send_chat(response):
            print(f"[chat_bot] sent: {response[:80]}", flush=True)


if __name__ == "__main__":
    main()
