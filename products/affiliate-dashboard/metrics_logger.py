#!/usr/bin/env python3
"""
Metrics history logger — appends a snapshot every 30 minutes.
Run by metrics-logger.timer NixOS service.
Writes to products/affiliate-dashboard/metrics_history.json
"""
import json
import subprocess
import datetime
import os

STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"
HISTORY_FILE = "/home/agent/company/products/affiliate-dashboard/metrics_history.json"
TWITCH_USER_ID = "1455485722"
MAX_SNAPSHOTS = 1000


def get_live_followers():
    try:
        r = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/channels/followers?broadcaster_id={TWITCH_USER_ID}"],
            capture_output=True, text=True, timeout=10
        )
        return json.loads(r.stdout).get("total", 0)
    except Exception:
        return 0


def get_live_viewers():
    try:
        r = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/streams?user_id={TWITCH_USER_ID}"],
            capture_output=True, text=True, timeout=10
        )
        streams = json.loads(r.stdout).get("data", [])
        if streams:
            return streams[0].get("viewer_count", 0), True
        return 0, False
    except Exception:
        return 0, False


def get_broadcast_minutes():
    try:
        with open(STATE_FILE) as f:
            state = json.load(f)
        broadcast_min = state.get("total_broadcast_minutes", 0)
        # Add live minutes if stream is currently running
        last_start = state.get("last_stream_start")
        if last_start:
            start_dt = datetime.datetime.fromisoformat(last_start.replace("Z", "+00:00"))
            now = datetime.datetime.now(datetime.timezone.utc)
            elapsed = (now - start_dt).total_seconds() / 60
            pre_stream = state.get("broadcast_minutes_before_stream", 0)
            broadcast_min = int(pre_stream + elapsed)
        return broadcast_min
    except Exception:
        return 0


def load_history():
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except Exception:
        return {"snapshots": []}


def save_history(data):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f)


def main():
    followers = get_live_followers()
    viewers, is_live = get_live_viewers()
    broadcast_min = get_broadcast_minutes()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    snapshot = {
        "ts": ts,
        "followers": followers,
        "broadcast_min": broadcast_min,
        "viewers": viewers,
        "is_live": is_live,
    }

    history = load_history()
    history["snapshots"].append(snapshot)

    # Cap to prevent unbounded growth
    if len(history["snapshots"]) > MAX_SNAPSHOTS:
        history["snapshots"] = history["snapshots"][-MAX_SNAPSHOTS:]

    save_history(history)
    print(f"[{ts}] Logged: followers={followers} broadcast_min={broadcast_min} viewers={viewers} live={is_live}")


if __name__ == "__main__":
    main()
