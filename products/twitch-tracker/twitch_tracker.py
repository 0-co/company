#!/usr/bin/env python3
"""
Twitch Affiliate Progress Tracker
Monitors followers and stream stats, posts to Discord on milestones.
"""

import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BROADCASTER_ID = "1455485722"
DISCORD_CHANNEL_ID = "1479926517965258875"

STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"

VAULT_TWITCH = "sudo -u vault /home/vault/bin/vault-twitch"
VAULT_DISCORD = "sudo -u vault /home/vault/bin/vault-discord"

AFFILIATE_FOLLOWERS = 50
AFFILIATE_BROADCAST_MINUTES = 500
AFFILIATE_AVG_VIEWERS = 3

MILESTONES = [5, 10, 25, 50]

MILESTONE_MESSAGES = {
    5: "✨ First 5 Twitch followers!",
    10: "📈 10 Twitch followers!",
    25: "🏁 Halfway there: 25/50 Twitch followers!",
    50: "🎉 TWITCH AFFILIATE UNLOCKED! 50 followers!",
}

POLL_INTERVAL_SECONDS = 300  # 5 minutes

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# State persistence
# ---------------------------------------------------------------------------

DEFAULT_STATE: dict = {
    "last_follower_count": 0,
    "total_broadcast_minutes": 0,
    "last_stream_start": None,
    "last_run": None,
}


def load_state() -> dict:
    """Load persisted state from disk, returning defaults on missing file."""
    if not os.path.exists(STATE_FILE):
        return dict(DEFAULT_STATE)
    try:
        with open(STATE_FILE, "r") as file_handle:
            data = json.load(file_handle)
            # Fill in any keys added since the file was written
            for key, value in DEFAULT_STATE.items():
                data.setdefault(key, value)
            return data
    except (json.JSONDecodeError, OSError) as error:
        log.error("Failed to read state file: %s", error)
        return dict(DEFAULT_STATE)


def save_state(state: dict) -> None:
    """Persist state to disk atomically."""
    tmp_path = STATE_FILE + ".tmp"
    try:
        with open(tmp_path, "w") as file_handle:
            json.dump(state, file_handle, indent=2)
        os.replace(tmp_path, STATE_FILE)
    except OSError as error:
        log.error("Failed to save state: %s", error)

# ---------------------------------------------------------------------------
# Vault command helpers
# ---------------------------------------------------------------------------


def run_vault_command(command: str) -> tuple[bool, str]:
    """Run a shell command and return (success, stdout_text)."""
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        log.error("Command failed (exit %d): %s", result.returncode, command)
        log.error("stderr: %s", result.stderr.strip())
        return False, ""
    return True, result.stdout.strip()


def fetch_followers() -> tuple[bool, int, list]:
    """Fetch follower count from Twitch API.

    Returns (success, total_count, recent_follower_data).
    """
    command = (
        f"{VAULT_TWITCH} GET "
        f"'/channels/followers?broadcaster_id={BROADCASTER_ID}'"
    )
    success, output = run_vault_command(command)
    if not success or not output:
        return False, 0, []

    try:
        payload = json.loads(output)
        total = payload.get("total", 0)
        data = payload.get("data", [])
        return True, total, data
    except (json.JSONDecodeError, KeyError) as error:
        log.error("Failed to parse followers response: %s", error)
        return False, 0, []


def fetch_stream_status() -> tuple[bool, dict | None]:
    """Fetch current stream status.

    Returns (success, stream_dict_or_None).
    stream_dict is None when the channel is offline.
    """
    command = (
        f"{VAULT_TWITCH} GET '/streams?user_id={BROADCASTER_ID}'"
    )
    success, output = run_vault_command(command)
    if not success or not output:
        return False, None

    try:
        payload = json.loads(output)
        streams = payload.get("data", [])
        if streams:
            return True, streams[0]
        return True, None
    except (json.JSONDecodeError, KeyError) as error:
        log.error("Failed to parse stream response: %s", error)
        return False, None

# ---------------------------------------------------------------------------
# Discord notifications
# ---------------------------------------------------------------------------


def post_discord(message: str) -> bool:
    """Post a plain-text message to the configured Discord channel."""
    # Escape double-quotes in the message to keep JSON valid
    safe_message = message.replace("\\", "\\\\").replace('"', '\\"')
    command = (
        f'{VAULT_DISCORD} -s -X POST '
        f'"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages" '
        f'-H "Content-Type: application/json" '
        f'-d \'{{"content": "{safe_message}"}}\''
    )
    success, _ = run_vault_command(command)
    if success:
        log.info("Discord notification sent: %s", message)
    return success

# ---------------------------------------------------------------------------
# Broadcast-minute accounting
# ---------------------------------------------------------------------------


def calculate_new_broadcast_minutes(
    stream: dict,
    last_stream_start: str | None,
    previous_total_minutes: int,
) -> tuple[int, str]:
    """Return (updated_total_minutes, started_at_iso_string).

    We only add minutes for a stream that started *after* the last recorded
    start, preventing double-counting across repeated polls of the same stream.
    """
    started_at_str: str = stream["started_at"]

    if last_stream_start == started_at_str:
        # Same stream still ongoing — accumulate more minutes
        started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        elapsed_minutes = int((now - started_at).total_seconds() / 60)

        # Avoid subtracting from total if elapsed < what we previously counted
        # We store the raw total and rebuild it fresh each poll for the live stream
        return previous_total_minutes, started_at_str

    # New stream detected — compute minutes for the just-ended previous stream
    # (we don't know end time, so we just use what we had plus any new stream)
    return previous_total_minutes, started_at_str


def compute_live_stream_minutes(stream: dict) -> int:
    """Return minutes elapsed since the current stream started (floor)."""
    started_at_str: str = stream["started_at"]
    started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return max(0, int((now - started_at).total_seconds() / 60))

# ---------------------------------------------------------------------------
# Status display
# ---------------------------------------------------------------------------


def print_status(
    follower_count: int,
    total_broadcast_minutes: int,
    stream: dict | None,
) -> None:
    """Print a human-readable affiliate progress summary to stdout."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    if stream:
        viewer_count: int = stream.get("viewer_count", 0)
        started_at_str: str = stream.get("started_at", "")
        if started_at_str:
            started_at = datetime.fromisoformat(
                started_at_str.replace("Z", "+00:00")
            )
            local_start = started_at.astimezone().strftime("%H:%M")
        else:
            local_start = "unknown"
        stream_line = f"LIVE ({viewer_count} viewers, started {local_start})"
        avg_viewers = viewer_count  # Single-poll approximation
    else:
        stream_line = "OFFLINE"
        avg_viewers = 0

    print(f"[{timestamp}] Twitch Affiliate Status")
    print(f"Followers:     {follower_count}/{AFFILIATE_FOLLOWERS}")
    print(f"Broadcast min: {total_broadcast_minutes}/{AFFILIATE_BROADCAST_MINUTES}")
    print(f"Avg viewers:   {avg_viewers} (target: {AFFILIATE_AVG_VIEWERS})")
    print(f"Stream:        {stream_line}")
    print()

# ---------------------------------------------------------------------------
# Core polling logic
# ---------------------------------------------------------------------------


def run_once(state: dict) -> dict:
    """Execute one poll cycle. Returns updated state dict."""
    now_iso = datetime.now(timezone.utc).isoformat()

    # --- Fetch data ---------------------------------------------------------
    followers_ok, follower_count, _follower_data = fetch_followers()
    if not followers_ok:
        log.error("Skipping cycle: could not fetch followers")
        print_status(
            state["last_follower_count"],
            state["total_broadcast_minutes"],
            None,
        )
        return state

    stream_ok, stream = fetch_stream_status()
    if not stream_ok:
        log.error("Skipping cycle: could not fetch stream status")
        print_status(follower_count, state["total_broadcast_minutes"], None)
        return state

    # --- Broadcast-minute accounting ----------------------------------------
    total_broadcast_minutes: int = state["total_broadcast_minutes"]
    last_stream_start: str | None = state["last_stream_start"]

    if stream:
        live_minutes = compute_live_stream_minutes(stream)
        current_started_at: str = stream["started_at"]

        if last_stream_start != current_started_at:
            # New stream: record the start; minutes will accumulate on next cycle
            log.info("New stream detected, started at %s", current_started_at)
            last_stream_start = current_started_at
        else:
            # Ongoing stream: update total by setting it to base + live elapsed
            # (base = whatever was saved before this stream started)
            base_minutes: int = state.get("broadcast_minutes_before_stream", 0)
            total_broadcast_minutes = base_minutes + live_minutes

        state["broadcast_minutes_before_stream"] = state.get(
            "broadcast_minutes_before_stream", total_broadcast_minutes
        )
        if last_stream_start != state["last_stream_start"]:
            # Store snapshot of minutes before new stream
            state["broadcast_minutes_before_stream"] = state["total_broadcast_minutes"]
    else:
        # Not live: if we were previously live, stream ended — keep total as-is
        if last_stream_start and state["last_stream_start"] == last_stream_start:
            pass  # total already updated on last live poll
        last_stream_start = None

    # --- Follower change detection ------------------------------------------
    previous_count: int = state["last_follower_count"]

    if follower_count > previous_count:
        gained = follower_count - previous_count
        log.info("Gained %d follower(s): %d -> %d", gained, previous_count, follower_count)

        # Check whether any milestone was crossed
        milestone_hit: int | None = None
        for milestone in sorted(MILESTONES):
            if previous_count < milestone <= follower_count:
                milestone_hit = milestone

        if milestone_hit is not None:
            post_discord(MILESTONE_MESSAGES[milestone_hit])
        else:
            post_discord(
                f"📺 New Twitch follower! {follower_count}/{AFFILIATE_FOLLOWERS} to affiliate."
            )

    # --- Print status -------------------------------------------------------
    print_status(follower_count, total_broadcast_minutes, stream)

    # --- Persist updated state ----------------------------------------------
    state["last_follower_count"] = follower_count
    state["total_broadcast_minutes"] = total_broadcast_minutes
    state["last_stream_start"] = last_stream_start
    state["last_run"] = now_iso
    save_state(state)

    return state

# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse arguments and dispatch to single-run or loop mode."""
    loop_mode = "--loop" in sys.argv

    state = load_state()

    if loop_mode:
        log.info("Starting Twitch tracker in loop mode (interval: %ds)", POLL_INTERVAL_SECONDS)
        while True:
            try:
                state = run_once(state)
            except Exception as error:
                log.error("Unexpected error in poll cycle: %s", error)
            time.sleep(POLL_INTERVAL_SECONDS)
    else:
        run_once(state)


if __name__ == "__main__":
    main()
