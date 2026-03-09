#!/usr/bin/env python3
"""
DepTriage Discord Bot — responds to !scan commands in Discord.

Commands:
  !scan owner/repo     — Run DepTriage on a public GitHub repo
  !scan --org orgname  — Scan all repos in a GitHub org (requires token)
  !help                — Show available commands

Env vars (injected by vault-discord-bot):
  DISCORD_BOT_TOKEN  — Bot token for gateway connection
"""

import os
import sys
import json
import asyncio
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timezone

# Discord gateway and REST API constants
GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"
API_BASE = "https://discord.com/api/v10"
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "")

INTENTS = (1 << 9) | (1 << 15)  # GUILD_MESSAGES + MESSAGE_CONTENT


def api_post(endpoint: str, data: dict) -> dict:
    """POST to Discord REST API."""
    url = f"{API_BASE}{endpoint}"
    payload = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": "DepTriageBot/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"API error {e.code}: {body}", file=sys.stderr)
        return {}


def send_message(channel_id: str, content: str) -> None:
    """Send a message to a Discord channel (plain text, max 2000 chars)."""
    if len(content) > 2000:
        content = content[:1990] + "\n...(truncated)"
    api_post(f"/channels/{channel_id}/messages", {"content": content})


def run_scan(repo: str, is_org: bool = False) -> str:
    """Run dep-triage scanner and return formatted output."""
    scanner = "/home/agent/company/products/dep-triage/scanner.py"
    if is_org:
        cmd = ["python3", scanner, "--org", repo]
    else:
        cmd = ["python3", scanner, repo]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout or result.stderr or "No output from scanner."
        # Remove ANSI color codes for Discord
        import re
        output = re.sub(r'\x1b\[[0-9;]*m', '', output)
        return output.strip()
    except subprocess.TimeoutExpired:
        return "❌ Scan timed out (>60s). Try a repo with fewer PRs."
    except Exception as e:
        return f"❌ Scanner error: {e}"


HELP_TEXT = """**DepTriage Bot Commands**

`!scan owner/repo` — Triage open dependency PRs by CVE risk
`!scan https://github.com/owner/repo` — GitHub URL format also works
`!help` — Show this message

**Example:**
```
!scan facebook/react
```

**What you get:**
🔴 CRITICAL — merge today (CVE/GHSA confirmed)
🟠 HIGH — review today (security keywords, major bump)
🟡 MEDIUM — review this week (minor bump)
🟢 SAFE — auto-merge candidate (patch bump, dev-only)

Built by 0-co — an AI company. https://github.com/0-co/company"""


async def handle_message(data: dict) -> None:
    """Process an incoming message event."""
    content = data.get("content", "").strip()
    channel_id = data.get("channel_id", "")
    author = data.get("author", {})

    # Ignore bot messages
    if author.get("bot"):
        return

    if content.lower() == "!help":
        send_message(channel_id, HELP_TEXT)
        return

    if content.lower().startswith("!scan "):
        target = content[6:].strip()
        if not target:
            send_message(channel_id, "Usage: `!scan owner/repo`")
            return

        is_org = target.startswith("--org ")
        if is_org:
            target = target[6:].strip()
            send_message(channel_id, f"🔍 Scanning org **{target}**... (this may take a minute)")
        else:
            # Clean up GitHub URL if provided
            if "github.com/" in target:
                import re
                m = re.search(r'github\.com/([^/]+/[^/\s]+)', target)
                if m:
                    target = m.group(1).split("/")[:2]
                    target = "/".join(target)
            send_message(channel_id, f"🔍 Scanning **{target}**... ")

        output = run_scan(target, is_org=is_org)
        # Wrap in code block for Discord
        formatted = f"**DepTriage: {target}**\n```\n{output}\n```"
        send_message(channel_id, formatted)
        return


async def gateway_connect() -> None:
    """Connect to Discord gateway and listen for messages."""
    import urllib.request
    import base64
    import struct
    import hashlib
    import hmac
    import ssl

    # Try to use websockets if available, else fall back to polling
    try:
        import websockets
        has_ws = True
    except ImportError:
        has_ws = False

    if not has_ws:
        # Fallback: polling-based approach via REST (less efficient but no dep)
        print("websockets not available — using REST polling", file=sys.stderr)
        await rest_polling_loop()
        return

    uri = GATEWAY_URL
    ssl_ctx = ssl.create_default_context()

    async with websockets.connect(uri, ssl=ssl_ctx) as ws:
        print("Connected to Discord gateway", file=sys.stderr)
        heartbeat_interval = None
        session_id = None
        sequence = None

        async def send_heartbeat():
            await ws.send(json.dumps({"op": 1, "d": sequence}))

        async def identify():
            await ws.send(json.dumps({
                "op": 2,
                "d": {
                    "token": BOT_TOKEN,
                    "intents": INTENTS,
                    "properties": {
                        "os": "linux",
                        "browser": "dep-triage-bot",
                        "device": "dep-triage-bot",
                    },
                },
            }))

        async def heartbeat_loop(interval_ms: float):
            while True:
                await asyncio.sleep(interval_ms / 1000)
                await send_heartbeat()

        hb_task = None

        async for raw in ws:
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue

            op = msg.get("op")
            sequence = msg.get("s") or sequence

            if op == 10:  # Hello
                heartbeat_interval = msg["d"]["heartbeat_ms"] if "heartbeat_ms" in msg["d"] else msg["d"]["heartbeat_interval"]
                hb_task = asyncio.create_task(heartbeat_loop(heartbeat_interval))
                await identify()

            elif op == 0:  # Dispatch
                event = msg.get("t")
                data = msg.get("d", {})

                if event == "READY":
                    session_id = data.get("session_id")
                    user = data.get("user", {})
                    print(f"Bot ready: {user.get('username')}#{user.get('discriminator')}", file=sys.stderr)

                elif event == "MESSAGE_CREATE":
                    await handle_message(data)

            elif op == 11:  # Heartbeat ACK
                pass


async def rest_polling_loop() -> None:
    """Fallback: poll for new messages via REST API (no websocket dep)."""
    # Track last seen message IDs per channel
    last_ids: dict[str, str] = {}
    channels = ["1479926517965258875", "1479926558604136660"]  # #general, #ai

    print("Starting REST polling loop (30s interval)...", file=sys.stderr)

    while True:
        for channel_id in channels:
            after = last_ids.get(channel_id, "")
            url = f"{API_BASE}/channels/{channel_id}/messages?limit=10"
            if after:
                url += f"&after={after}"

            req = urllib.request.Request(
                url,
                headers={
                    "Authorization": f"Bot {BOT_TOKEN}",
                    "User-Agent": "DepTriageBot/1.0",
                },
            )
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    messages = json.loads(resp.read())
                    if messages:
                        # Messages come newest-first; process oldest-first
                        for msg in reversed(messages):
                            last_ids[channel_id] = msg["id"]
                            await handle_message(msg)
            except Exception as e:
                print(f"Polling error for {channel_id}: {e}", file=sys.stderr)

        await asyncio.sleep(10)  # Poll every 10 seconds


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: DISCORD_BOT_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    print("Starting DepTriage Discord Bot...", file=sys.stderr)
    try:
        asyncio.run(gateway_connect())
    except KeyboardInterrupt:
        print("Bot stopped.", file=sys.stderr)
