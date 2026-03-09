#!/usr/bin/env python3
"""
Stream dashboard — live terminal telemetry for the 0coceo Twitch stream.
Shows affiliate progress, current session stats, recent Bluesky activity.
Run: python3 dashboard.py [--once]
"""
import subprocess, json, time, sys, os
from datetime import datetime, timezone

BROADCASTER_ID = "1455485722"
BSKY_DID = "did:plc:ak33o45ans6qtlhxxulcd4ko"
ONCE = "--once" in sys.argv

def twitch(method, endpoint, body=None):
    args = ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch", method, endpoint]
    if body:
        args.append(json.dumps(body))
    r = subprocess.run(args, capture_output=True, text=True, timeout=10)
    if r.returncode == 0 and r.stdout.strip():
        return json.loads(r.stdout)
    return {}

def bsky(method, body):
    r = subprocess.run(
        ["sudo", "-u", "vault", "/home/vault/bin/vault-bsky", method, json.dumps(body)],
        capture_output=True, text=True, timeout=10
    )
    if r.returncode == 0 and r.stdout.strip():
        return json.loads(r.stdout)
    return {}

def bar(current, target, width=30):
    filled = int((current / max(target, 1)) * width)
    filled = min(filled, width)
    pct = min(100, int((current / max(target, 1)) * 100))
    return f"[{'█' * filled}{'░' * (width - filled)}] {current}/{target} ({pct}%)"

def fetch_data():
    data = {}

    # Stream status + viewer count
    streams = twitch("GET", f"/streams?user_id={BROADCASTER_ID}")
    stream_data = streams.get("data", [])
    if stream_data:
        s = stream_data[0]
        data["live"] = True
        data["viewers"] = s.get("viewer_count", 0)
        started = s.get("started_at", "")
        if started:
            start_dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
            elapsed = datetime.now(timezone.utc) - start_dt
            mins = int(elapsed.total_seconds() / 60)
            data["session_minutes"] = mins
        data["title"] = s.get("title", "")[:60]
    else:
        data["live"] = False
        data["viewers"] = 0
        data["session_minutes"] = 0

    # Followers
    followers = twitch("GET", f"/channels/followers?broadcaster_id={BROADCASTER_ID}")
    data["followers"] = followers.get("total", 0)

    # Bluesky profile (post count, followers)
    profile = bsky("app.bsky.actor.getProfile", {"actor": BSKY_DID})
    data["bsky_followers"] = profile.get("followersCount", 0)
    data["bsky_posts"] = profile.get("postsCount", 0)

    return data

def affiliate_deadline_countdown():
    """Days/hours until 2026-04-01 deadline for H5 affiliate goal."""
    deadline = datetime(2026, 4, 1, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    delta = deadline - now
    if delta.total_seconds() <= 0:
        return "DEADLINE PASSED"
    days = delta.days
    hours = int((delta.total_seconds() % 86400) / 3600)
    return f"{days}d {hours}h remaining"


def render(data):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("╔══════════════════════════════════════════════════════╗")
    header = f"  0coCeo Company Dashboard — {now}"
    lines.append(f"║{header:<54}║")
    countdown = affiliate_deadline_countdown()
    lines.append(f"║  H5 deadline: {countdown:<40}║")
    lines.append("╠══════════════════════════════════════════════════════╣")

    # Stream status (avoid emoji for clean column alignment)
    status = "LIVE" if data.get("live") else "OFFLINE"
    lines.append(f"║  Twitch status: {status:<38}║")
    if data.get("live"):
        lines.append(f"║  Viewers:       {data['viewers']:<38}║")
        mins = data['session_minutes']
        lines.append(f"║  Session time:  {mins} min{' ' * (38 - len(str(mins)) - 4)}║")

    lines.append("╠══════════════════════════════════════════════════════╣")
    lines.append("║  TWITCH AFFILIATE PROGRESS                           ║")
    lines.append(f"║  Followers:  {bar(data['followers'], 50, 28):<42}║")

    # Broadcast minutes — estimated from tracker service log or session time
    # We track cumulative; use session_minutes as proxy for current session
    session_mins = data.get("session_minutes", 0)
    # Read from tracker log if available
    bcast_mins = read_broadcast_minutes(session_mins)
    lines.append(f"║  Broadcast:  {bar(bcast_mins, 500, 28):<42}║")
    avg_line = f"  Avg viewers: {data['viewers']}/3 target"
    lines.append(f"║{avg_line:<54}║")

    lines.append("╠══════════════════════════════════════════════════════╣")
    lines.append("║  BLUESKY                                             ║")
    lines.append(f"║  Followers: {data['bsky_followers']:<43}║")
    lines.append(f"║  Total posts: {data['bsky_posts']:<41}║")

    lines.append("╠══════════════════════════════════════════════════════╣")
    lines.append("║  FINANCIALS                                          ║")
    lines.append("║  Revenue:  $0                                        ║")
    lines.append("║  Burn:     ~$250/month                               ║")
    lines.append("║  Runway:   board-funded                              ║")
    lines.append("╚══════════════════════════════════════════════════════╝")

    return "\n".join(lines)

def read_broadcast_minutes(session_mins):
    """Read from twitch-tracker service logs to get cumulative broadcast minutes."""
    try:
        r = subprocess.run(
            ["sudo", "journalctl", "-u", "twitch-tracker.service", "--no-pager", "-n", "50",
             "--output=cat"],
            capture_output=True, text=True, timeout=5
        )
        for line in reversed(r.stdout.splitlines()):
            if "Broadcast min:" in line:
                # Format: "Broadcast min: 28/500"
                part = line.split("Broadcast min:")[1].strip()
                current = int(part.split("/")[0].strip())
                return current
    except:
        pass
    return 22 + session_mins  # fallback: known baseline + current session

def main():
    if ONCE:
        try:
            data = fetch_data()
            print(render(data))
        except Exception as e:
            print(f"Error: {e}")
        return

    print("Starting stream dashboard. Ctrl+C to exit.")
    time.sleep(1)

    while True:
        try:
            data = fetch_data()
            # Clear screen
            print("\033[2J\033[H", end="")
            print(render(data))
            print("\n  Refreshing every 60s... (Ctrl+C to exit)")
            time.sleep(60)
        except KeyboardInterrupt:
            print("\nDashboard stopped.")
            break
        except Exception as e:
            print(f"Error fetching data: {e}")
            time.sleep(30)

if __name__ == "__main__":
    main()
