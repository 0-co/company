#!/usr/bin/env python3
"""
email-monitor — Watch AgentMail inbox and alert via Discord.

Runs as a systemd timer or standalone loop. On new messages:
- Posts to Discord #general with sender, subject, preview
- Logs to state file to avoid duplicate alerts

Usage:
    python3 email_monitor.py          # Check once and exit
    python3 email_monitor.py --loop   # Poll every 60 seconds
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

INBOX = "0coceo@agentmail.to"
STATE_FILE = Path(__file__).parent / "email_monitor_state.json"
DISCORD_CHANNEL = "1479926517965258875"  # #general
VAULT_AGENTMAIL = "/home/vault/bin/vault-agentmail"
VAULT_DISCORD = "/home/vault/bin/vault-discord"


def call_agentmail(method: str, endpoint: str, body: dict = None) -> dict:
    """Call AgentMail via vault wrapper."""
    args = ["sudo", "-u", "vault", VAULT_AGENTMAIL, method, endpoint]
    if body:
        args.append(json.dumps(body))
    result = subprocess.run(args, capture_output=True, text=True, timeout=15)
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"AgentMail call failed: {result.stderr}")
    return json.loads(result.stdout)


def post_discord(message: str) -> None:
    """Post a message to Discord #general."""
    payload = json.dumps({"content": message})
    args = [
        "sudo", "-u", "vault", VAULT_DISCORD,
        "-s", "-X", "POST",
        f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL}/messages",
        "-H", "Content-Type: application/json",
        "-d", payload,
    ]
    subprocess.run(args, capture_output=True, text=True, timeout=10)


def load_state() -> dict:
    """Load seen message IDs from state file."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {"seen_ids": [], "last_check": None}


def save_state(state: dict) -> None:
    """Save state to file."""
    STATE_FILE.write_text(json.dumps(state, indent=2))


def check_inbox() -> list:
    """Check inbox for new messages, return list of new ones."""
    state = load_state()
    seen = set(state.get("seen_ids", []))

    try:
        data = call_agentmail("GET", f"/v0/inboxes/{INBOX}/messages?limit=20")
        messages = data.get("messages", [])
    except Exception as error:
        print(f"[{now()}] Error checking inbox: {error}", file=sys.stderr)
        return []

    new_messages = []
    for msg in messages:
        msg_id = msg.get("message_id", "")
        if msg_id not in seen:
            new_messages.append(msg)
            seen.add(msg_id)

    # Update state
    state["seen_ids"] = list(seen)[-100:]  # keep last 100
    state["last_check"] = now()
    save_state(state)

    return new_messages


def format_alert(msg: dict) -> str:
    """Format a Discord alert for a new email."""
    sender = msg.get("from", "unknown")
    subject = msg.get("subject", "(no subject)")
    preview = msg.get("preview", "").strip().replace("\n", " ")[:150]
    ts = msg.get("timestamp", "")[:10]

    return (
        f"📧 **New email in {INBOX}**\n"
        f"From: `{sender}`\n"
        f"Subject: **{subject}**\n"
        f"Date: {ts}\n"
        f"> {preview}"
    )


def now() -> str:
    from datetime import timezone
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run_once():
    """Check inbox once and alert on new messages."""
    print(f"[{now()}] Checking {INBOX}...")
    new_msgs = check_inbox()

    if not new_msgs:
        print(f"[{now()}] No new messages.")
        return

    print(f"[{now()}] {len(new_msgs)} new message(s)!")
    for msg in new_msgs:
        alert = format_alert(msg)
        print(f"[{now()}] Alerting Discord: {msg.get('subject', '?')}")
        try:
            post_discord(alert)
        except Exception as error:
            print(f"[{now()}] Discord alert failed: {error}", file=sys.stderr)


def run_loop(interval: int = 300):
    """Poll inbox every interval seconds."""
    print(f"[{now()}] Email monitor started. Polling every {interval}s.")
    while True:
        run_once()
        time.sleep(interval)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AgentMail inbox monitor")
    parser.add_argument("--loop", action="store_true", help="Poll continuously")
    parser.add_argument("--interval", type=int, default=300, help="Poll interval in seconds (default 300)")
    args = parser.parse_args()

    if args.loop:
        run_loop(args.interval)
    else:
        run_once()
