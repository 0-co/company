#!/usr/bin/env python3
"""
Affiliate countdown dashboard — serves on port 8080.
Reads state.json + Twitch API. No external dependencies.
"""

import json
import subprocess
import time
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

STATE_FILE = "/home/agent/company/products/twitch-tracker/state.json"
DEADLINE = datetime.datetime(2026, 4, 1, tzinfo=datetime.timezone.utc)
TWITCH_CHANNEL = "0coceo"
TWITCH_USER_ID = "1455485722"


def get_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def get_live_followers():
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/channels/followers?broadcaster_id={TWITCH_USER_ID}"],
            capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout)
        return data.get("total", 0)
    except Exception:
        return None


def get_live_viewers():
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/streams?user_id={TWITCH_USER_ID}"],
            capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout)
        streams = data.get("data", [])
        if streams:
            return streams[0].get("viewer_count", 0), True
        return 0, False
    except Exception:
        return 0, False


def build_html(followers, broadcast_min, viewers, is_live, deadline_days, deadline_hours):
    follower_pct = min(100, int(followers / 50 * 100))
    broadcast_pct = min(100, int(broadcast_min / 500 * 100))
    viewer_pct = min(100, int(viewers / 3 * 100))

    live_badge = '<span class="live-badge">● LIVE</span>' if is_live else '<span class="offline-badge">OFFLINE</span>'

    deadline_str = f"{deadline_days}d {deadline_hours}h" if deadline_days >= 0 else "EXPIRED"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="60">
<title>0coceo — Twitch Affiliate Race</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0e0e10;
    color: #efeff1;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace, sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }}
  .container {{
    max-width: 480px;
    width: 100%;
  }}
  .header {{
    text-align: center;
    margin-bottom: 32px;
  }}
  .channel-name {{
    font-size: 28px;
    font-weight: 700;
    color: #bf94ff;
    letter-spacing: -0.5px;
  }}
  .tagline {{
    font-size: 13px;
    color: #adadb8;
    margin-top: 4px;
  }}
  .live-badge {{
    background: #e91916;
    color: white;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 3px;
    margin-left: 8px;
    animation: pulse 2s infinite;
  }}
  .offline-badge {{
    background: #3a3a3d;
    color: #adadb8;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 3px;
    margin-left: 8px;
  }}
  @keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.6; }}
  }}
  .deadline-box {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    margin-bottom: 24px;
  }}
  .deadline-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #adadb8;
    margin-bottom: 4px;
  }}
  .deadline-value {{
    font-size: 32px;
    font-weight: 700;
    color: {'#ff4500' if deadline_days < 7 else '#efeff1'};
    letter-spacing: -1px;
  }}
  .deadline-sub {{
    font-size: 12px;
    color: #adadb8;
    margin-top: 2px;
  }}
  .metrics {{
    display: flex;
    flex-direction: column;
    gap: 16px;
    margin-bottom: 28px;
  }}
  .metric {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 16px;
  }}
  .metric-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 10px;
  }}
  .metric-label {{
    font-size: 13px;
    color: #adadb8;
  }}
  .metric-value {{
    font-size: 22px;
    font-weight: 700;
    color: #efeff1;
  }}
  .metric-target {{
    font-size: 13px;
    color: #adadb8;
  }}
  .progress-bar {{
    height: 8px;
    background: #3a3a3d;
    border-radius: 4px;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
  }}
  .progress-followers {{ background: #bf94ff; }}
  .progress-broadcast {{ background: #00b5ad; }}
  .progress-viewers {{ background: #f59e0b; }}
  .progress-pct {{
    font-size: 11px;
    color: #adadb8;
    margin-top: 4px;
    text-align: right;
  }}
  .cta {{
    display: block;
    background: #9147ff;
    color: white;
    text-decoration: none;
    text-align: center;
    padding: 14px 24px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 16px;
    transition: background 0.2s;
  }}
  .cta:hover {{ background: #7c3fdc; }}
  .footer {{
    text-align: center;
    font-size: 11px;
    color: #5c5c6e;
    margin-top: 12px;
  }}
  .what-is-this {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 24px;
    font-size: 13px;
    color: #adadb8;
    line-height: 1.5;
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="channel-name">0coceo {live_badge}</div>
    <div class="tagline">An AI CEO building a company live on Twitch</div>
  </div>

  <div class="what-is-this">
    No humans. One AI (Claude). One board member with a kill switch. Building in public — every decision, failure, and breakthrough streamed live. The goal: Twitch affiliate by April 1.
  </div>

  <div class="deadline-box">
    <div class="deadline-label">Time until April 1 deadline</div>
    <div class="deadline-value">{deadline_str}</div>
    <div class="deadline-sub">3 requirements to unlock affiliate status</div>
  </div>

  <div class="metrics">
    <div class="metric">
      <div class="metric-header">
        <span class="metric-label">Followers</span>
        <span><span class="metric-value">{followers}</span> <span class="metric-target">/ 50</span></span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill progress-followers" style="width:{follower_pct}%"></div>
      </div>
      <div class="progress-pct">{follower_pct}%</div>
    </div>

    <div class="metric">
      <div class="metric-header">
        <span class="metric-label">Broadcast minutes</span>
        <span><span class="metric-value">{broadcast_min}</span> <span class="metric-target">/ 500</span></span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill progress-broadcast" style="width:{broadcast_pct}%"></div>
      </div>
      <div class="progress-pct">{broadcast_pct}%</div>
    </div>

    <div class="metric">
      <div class="metric-header">
        <span class="metric-label">Avg concurrent viewers</span>
        <span><span class="metric-value">{viewers}</span> <span class="metric-target">/ 3</span></span>
      </div>
      <div class="progress-bar">
        <div class="progress-fill progress-viewers" style="width:{viewer_pct}%"></div>
      </div>
      <div class="progress-pct">{viewer_pct}%</div>
    </div>
  </div>

  <a class="cta" href="https://twitch.tv/{TWITCH_CHANNEL}" target="_blank">
    Watch Live on Twitch →
  </a>

  <div class="footer">
    Auto-refreshes every 60s · Built by the AI it's tracking
  </div>
</div>
</body>
</html>"""


CALC_FILE = "/home/agent/company/products/affiliate-dashboard/calc.html"


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/calc":
            try:
                with open(CALC_FILE, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception:
                self.send_response(500)
                self.end_headers()
            return

        if self.path not in ("/", "/favicon.ico"):
            self.send_response(404)
            self.end_headers()
            return

        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        state = get_state()
        broadcast_min = state.get("total_broadcast_minutes", 0)

        # Add minutes since last stream start if currently live
        last_start = state.get("last_stream_start")
        if last_start:
            try:
                start_dt = datetime.datetime.fromisoformat(last_start.replace("Z", "+00:00"))
                now = datetime.datetime.now(datetime.timezone.utc)
                elapsed = (now - start_dt).total_seconds() / 60
                pre_stream = state.get("broadcast_minutes_before_stream", 0)
                broadcast_min = int(pre_stream + elapsed)
            except Exception:
                pass

        followers = get_live_followers()
        if followers is None:
            followers = state.get("last_follower_count", 0)

        viewers, is_live = get_live_viewers()

        now = datetime.datetime.now(datetime.timezone.utc)
        delta = DEADLINE - now
        deadline_days = delta.days
        deadline_hours = delta.seconds // 3600

        html = build_html(followers, broadcast_min, viewers, is_live, deadline_days, deadline_hours)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(html.encode("utf-8"))))
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, format, *args):
        pass  # Suppress default access logs


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), DashboardHandler)
    print("Affiliate dashboard running on :8080", flush=True)
    server.serve_forever()
