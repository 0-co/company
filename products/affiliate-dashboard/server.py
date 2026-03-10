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
COMPANY_START = datetime.datetime(2026, 3, 8, tzinfo=datetime.timezone.utc)
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


def build_html(followers, broadcast_min, viewers, is_live, deadline_days, deadline_hours, trajectory=None):
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

  {trajectory or ''}

  <a class="cta" href="https://twitch.tv/{TWITCH_CHANNEL}" target="_blank">
    Watch Live on Twitch →
  </a>

  <div style="text-align:center;margin-bottom:12px;">
    <a href="/calc" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">Affiliate calculator</a>
    <a href="/race" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">AI company race</a>
    <a href="/history" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">Metrics history</a>
    <a href="/log" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">Build log</a>
    <a href="/neighbors" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">Stream neighbors</a>
    <a href="/about" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">About</a>
  </div>
  <div class="footer">
    Auto-refreshes every 60s · Built by the AI it's tracking
  </div>
</div>
</body>
</html>"""


CALC_FILE = "/home/agent/company/products/affiliate-dashboard/calc.html"
GAME_ID = "1469308723"  # Software and Game Development
AFFINITY_KEYWORDS = [
    "ai", "claude", "gpt", "llm", "agent", "bot", "vibe cod",
    "rust", "python", "javascript", "react", "indie", "solo dev",
    "building", "startup", "saas", "terminal", "linux", "nixos",
    "coding", "programming", "dev", "hack", "build"
]
BLUESKY_CONNECTIONS = [
    "cmgriffing", "jotson", "irishjohngames", "foolbox", "sabine_sh",
    "nhancodes", "electroslag"
]


def get_category_streams():
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/streams?game_id={GAME_ID}&first=50"],
            capture_output=True, text=True, timeout=8
        )
        data = json.loads(result.stdout)
        streams = data.get("data", [])
        return [s for s in streams if s.get("user_id") != TWITCH_USER_ID]
    except Exception:
        return []


def score_stream(stream):
    score = 0
    viewer_count = stream.get("viewer_count", 0)
    title = stream.get("title", "").lower()
    username = stream.get("user_name", "").lower()

    if 10 <= viewer_count <= 50:
        score += 30
    elif 50 < viewer_count <= 150:
        score += 20
    elif viewer_count < 10:
        score += 10
    else:
        score += 5

    keyword_hits = sum(1 for kw in AFFINITY_KEYWORDS if kw in title)
    score += min(keyword_hits * 8, 30)

    for handle in BLUESKY_CONNECTIONS:
        if handle in username:
            score += 25
            break

    started_at = stream.get("started_at", "")
    if started_at:
        try:
            started = datetime.datetime.fromisoformat(started_at.replace("Z", "+00:00"))
            duration_hours = (datetime.datetime.now(datetime.timezone.utc) - started).total_seconds() / 3600
            if 1 <= duration_hours <= 6:
                score += 15
            elif duration_hours < 1:
                score += 5
        except Exception:
            pass

    return min(score, 100)


def build_neighbors_html():
    now = datetime.datetime.now(datetime.timezone.utc)
    streams = get_category_streams()

    scored = []
    for s in streams:
        score = score_stream(s)
        started_at = s.get("started_at", "")
        duration_min = 0
        if started_at:
            try:
                started = datetime.datetime.fromisoformat(started_at.replace("Z", "+00:00"))
                duration_min = int((now - started).total_seconds() / 60)
            except Exception:
                pass
        scored.append({
            "username": s["user_name"],
            "viewer_count": s.get("viewer_count", 0),
            "title": s.get("title", "")[:70],
            "duration_min": duration_min,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    total_viewers = sum(s["viewer_count"] for s in scored)
    our_share = round(1 / max(total_viewers, 1) * 100, 4)

    rows = ""
    for i, s in enumerate(scored[:15], 1):
        bar_color = "#bf94ff" if s["score"] >= 80 else "#9147ff" if s["score"] >= 50 else "#5c5c6e"
        bsky_star = "★ " if any(h in s["username"].lower() for h in BLUESKY_CONNECTIONS) else ""
        rows += f"""
        <tr>
            <td style="color:#adadb8;padding:8px 4px;">{i}</td>
            <td style="padding:8px 4px;font-weight:600;">{bsky_star}{s["username"]}</td>
            <td style="padding:8px 4px;color:#adadb8;">{s["viewer_count"]}</td>
            <td style="padding:8px 4px;">
                <div style="background:#2a2a2e;border-radius:4px;height:8px;width:60px;display:inline-block;vertical-align:middle;">
                    <div style="background:{bar_color};height:8px;border-radius:4px;width:{s['score']}%;"></div>
                </div>
                <span style="color:{bar_color};margin-left:6px;font-size:12px;">{s["score"]}</span>
            </td>
            <td style="padding:8px 4px;color:#5c5c6e;font-size:12px;">{s["duration_min"]}m</td>
            <td style="padding:8px 4px;color:#adadb8;font-size:12px;">{s["title"][:50]}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="120">
<title>0coceo — Stream Neighbors</title>
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
    padding: 24px;
  }}
  .container {{ max-width: 800px; width: 100%; }}
  .header {{ text-align: center; margin-bottom: 24px; padding-top: 16px; }}
  .title {{ font-size: 24px; font-weight: 700; color: #bf94ff; }}
  .subtitle {{ font-size: 13px; color: #adadb8; margin-top: 6px; }}
  .stat-row {{ display: flex; gap: 16px; margin-bottom: 24px; }}
  .stat-box {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 16px;
    flex: 1;
    text-align: center;
  }}
  .stat-value {{ font-size: 28px; font-weight: 700; color: #bf94ff; }}
  .stat-label {{ font-size: 12px; color: #5c5c6e; margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ text-align: left; padding: 8px 4px; color: #5c5c6e; font-size: 12px; border-bottom: 1px solid #3a3a3d; }}
  tr:hover td {{ background: #1f1f23; }}
  .nav {{ text-align: center; margin-bottom: 24px; }}
  .star {{ color: #f59e0b; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title">Stream Neighbors</div>
    <div class="subtitle">Software & Game Development category — live now · refreshes every 2 min</div>
  </div>
  <div class="nav">
    <a href="/" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">← Dashboard</a>
    <a href="/race" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">AI company race</a>
    <a href="/calc" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">Affiliate calculator</a>
  </div>
  <div class="stat-row">
    <div class="stat-box">
      <div class="stat-value">{len(streams)}</div>
      <div class="stat-label">streams live in category</div>
    </div>
    <div class="stat-box">
      <div class="stat-value">{total_viewers:,}</div>
      <div class="stat-label">total category viewers</div>
    </div>
    <div class="stat-box">
      <div class="stat-value">{our_share:.3f}%</div>
      <div class="stat-label">our market share</div>
    </div>
  </div>
  <div style="background:#1f1f23;border:1px solid #3a3a3d;border-radius:8px;padding:20px;">
    <div style="font-size:13px;color:#adadb8;margin-bottom:12px;">
      ★ = Bluesky connection · Score = raid/relationship potential (0–100)
    </div>
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Channel</th>
          <th>Viewers</th>
          <th>Score</th>
          <th>Min live</th>
          <th>Title</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
  <div style="text-align:center;margin-top:16px;font-size:11px;color:#3a3a3d;">
    Updated {now.strftime('%Y-%m-%d %H:%M UTC')}
  </div>
</div>
</body>
</html>"""
RACE_DATA_FILE = "/home/agent/company/products/race-tracker/race_data.json"
HISTORY_FILE = "/home/agent/company/products/affiliate-dashboard/metrics_history.json"

COMPANY_INFO = {
    "0coceo.bsky.social": {"label": "0coceo (us)", "desc": "AI CEO building a company live on Twitch", "url": "https://twitch.tv/0coceo"},
    "ultrathink-art.bsky.social": {"label": "ultrathink-art", "desc": "AI-run art & merch store", "url": "https://bsky.app/profile/ultrathink-art.bsky.social"},
    "iamgumbo.bsky.social": {"label": "iamgumbo", "desc": "AI media & comedy company", "url": "https://bsky.app/profile/iamgumbo.bsky.social"},
    "idapixl.bsky.social": {"label": "idapixl", "desc": "AI with persistent Obsidian vault memory", "url": "https://bsky.app/profile/idapixl.bsky.social"},
    "wolfpacksolution.bsky.social": {"label": "wolfpacksolution", "desc": "AI crypto & trading tools", "url": "https://bsky.app/profile/wolfpacksolution.bsky.social"},
}


def get_history():
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except Exception:
        return {"snapshots": []}


def build_history_html(history):
    snapshots = history.get("snapshots", [])

    if len(snapshots) < 2:
        chart_html = "<p style='color:#adadb8;text-align:center;padding:40px 0;'>Not enough data yet. Check back in 30 minutes.</p>"
        table_html = ""
    else:
        # Build SVG chart — followers (purple) and broadcast_min (teal, scaled to 50)
        W, H = 500, 160
        pad_l, pad_r, pad_t, pad_b = 48, 16, 16, 32

        n = len(snapshots)
        max_bcast = max(s["broadcast_min"] for s in snapshots)
        max_bcast = max(max_bcast, 500)  # scale to target

        def x_pos(i):
            return pad_l + (i / (n - 1)) * (W - pad_l - pad_r)

        def y_followers(v):
            return H - pad_b - (v / 50) * (H - pad_t - pad_b)

        def y_broadcast(v):
            # Scale broadcast to same 0-500 range mapped to chart height
            return H - pad_b - (v / 500) * (H - pad_t - pad_b)

        # Build polyline points
        f_pts = " ".join(f"{x_pos(i):.1f},{y_followers(s['followers']):.1f}" for i, s in enumerate(snapshots))
        b_pts = " ".join(f"{x_pos(i):.1f},{y_broadcast(s['broadcast_min']):.1f}" for i, s in enumerate(snapshots))

        # Y-axis labels (followers scale, left side)
        y_labels = ""
        for v in [0, 10, 20, 30, 40, 50]:
            y = y_followers(v)
            y_labels += f'<text x="{pad_l - 6}" y="{y + 4}" text-anchor="end" fill="#5c5c6e" font-size="10">{v}</text>'
            y_labels += f'<line x1="{pad_l}" y1="{y}" x2="{W - pad_r}" y2="{y}" stroke="#2a2a2e" stroke-width="1"/>'

        # X-axis labels (first and last timestamp)
        first_ts = snapshots[0]["ts"][5:16].replace("T", " ")
        last_ts = snapshots[-1]["ts"][5:16].replace("T", " ")
        x_labels = f"""
        <text x="{pad_l}" y="{H - 4}" text-anchor="start" fill="#5c5c6e" font-size="9">{first_ts}</text>
        <text x="{W - pad_r}" y="{H - 4}" text-anchor="end" fill="#5c5c6e" font-size="9">{last_ts}</text>
        """

        chart_html = f"""
        <svg width="100%" viewBox="0 0 {W} {H}" style="display:block;overflow:visible;">
          <defs>
            <clipPath id="chart-clip">
              <rect x="{pad_l}" y="{pad_t}" width="{W - pad_l - pad_r}" height="{H - pad_t - pad_b}"/>
            </clipPath>
          </defs>
          {y_labels}
          {x_labels}
          <!-- broadcast minutes line (teal) -->
          <polyline points="{b_pts}" fill="none" stroke="#00b5ad" stroke-width="2" clip-path="url(#chart-clip)" opacity="0.8"/>
          <!-- followers line (purple) -->
          <polyline points="{f_pts}" fill="none" stroke="#bf94ff" stroke-width="2.5" clip-path="url(#chart-clip)"/>
        </svg>
        <div style="display:flex;gap:20px;margin-top:8px;font-size:11px;color:#adadb8;justify-content:center;">
          <span><span style="color:#bf94ff;">&#9644;</span> Followers (target: 50)</span>
          <span><span style="color:#00b5ad;">&#9644;</span> Broadcast min (target: 500)</span>
        </div>
        """

        # Recent snapshots table (last 10)
        recent = snapshots[-10:][::-1]
        rows = ""
        for s in recent:
            ts = s["ts"][5:16].replace("T", " ")
            live = "● LIVE" if s.get("is_live") else "—"
            rows += f'<tr><td>{ts}</td><td>{s["followers"]}</td><td>{s["broadcast_min"]}</td><td>{s["viewers"]}</td><td style="color:{"#e91916" if s.get("is_live") else "#5c5c6e"}">{live}</td></tr>'

        table_html = f"""
        <div style="margin-top:24px;">
          <div style="font-size:12px;color:#adadb8;margin-bottom:8px;">Recent snapshots (30-min intervals)</div>
          <table style="width:100%;border-collapse:collapse;font-size:12px;">
            <thead>
              <tr style="color:#5c5c6e;border-bottom:1px solid #3a3a3d;">
                <th style="text-align:left;padding:4px 0;">Time (UTC)</th>
                <th style="text-align:right;padding:4px 8px;">Followers</th>
                <th style="text-align:right;padding:4px 8px;">Bcast min</th>
                <th style="text-align:right;padding:4px 8px;">Viewers</th>
                <th style="text-align:right;padding:4px 0;">Status</th>
              </tr>
            </thead>
            <tbody style="color:#efeff1;">{rows}</tbody>
          </table>
        </div>
        """

    total_snapshots = len(snapshots)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="1800">
<title>0coceo — Metrics History</title>
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
    padding: 24px;
  }}
  .container {{ max-width: 560px; width: 100%; }}
  .header {{ text-align: center; margin-bottom: 24px; padding-top: 16px; }}
  .title {{ font-size: 24px; font-weight: 700; color: #bf94ff; }}
  .subtitle {{ font-size: 13px; color: #adadb8; margin-top: 6px; }}
  .chart-box {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 16px;
  }}
  .chart-title {{ font-size: 13px; color: #adadb8; margin-bottom: 16px; }}
  .nav {{ text-align: center; margin-top: 20px; }}
  .nav a {{ color: #9147ff; text-decoration: none; font-size: 13px; margin: 0 12px; }}
  .footer {{ text-align: center; font-size: 11px; color: #5c5c6e; margin-top: 16px; }}
  table td, table th {{ padding: 6px 8px; }}
  table tbody tr:hover {{ background: #252529; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title">Metrics History</div>
    <div class="subtitle">30-minute snapshots since logging began · {total_snapshots} data points</div>
  </div>

  <div class="chart-box">
    <div class="chart-title">Follower & broadcast progress over time</div>
    {chart_html}
    {table_html}
  </div>

  <div class="nav">
    <a href="/">← Current progress</a>
    <a href="/race">AI company race</a>
    <a href="https://twitch.tv/0coceo" target="_blank">Watch live</a>
  </div>
  <div class="footer">Logged every 30 min · Built by the AI it's tracking</div>
</div>
</body>
</html>"""


STATUS_FILE = "/home/agent/company/status.md"

# Actions to skip in the log (too routine to show publicly)
SKIP_PATTERNS = [
    "Marked notifications", "marked notifications", "notifications marked",
    "Updated stream title", "stream title updated", "updated Twitch title",
    "Twitch title updated", "Twitch chat:", "Posted Twitch chat",
    "Board outbox: empty", "board outbox still empty",
    "Committed and push", "commit and push",
]


def parse_sessions():
    """Parse session actions from status.md. Returns list of {num, date_range, day, actions}."""
    import re
    try:
        content = open(STATUS_FILE).read()
    except Exception:
        return []

    sessions = []
    pattern = r'## Session (\d+) Actions \(([^\)]+)\)(.*?)(?=## |\Z)'
    for match in re.finditer(pattern, content, re.DOTALL):
        num = int(match.group(1))
        date_range = match.group(2)
        body = match.group(3)

        # Determine day from date range
        day = 1
        if "2026-03-09" in date_range:
            day = 2
        elif "2026-03-10" in date_range:
            day = 3
        elif "2026-03-11" in date_range:
            day = 4

        # Extract actions (lines with ✅ or ❌)
        raw_actions = [l.strip() for l in body.split('\n') if '✅' in l or '❌' in l]

        # Filter routine ones
        actions = []
        for a in raw_actions:
            skip = any(p.lower() in a.lower() for p in SKIP_PATTERNS)
            if not skip:
                # Clean up: remove numbering prefix like "1. ✅ " -> "✅ "
                a = re.sub(r'^\d+\.\s+', '', a)
                actions.append(a)

        if actions:
            sessions.append({
                "num": num,
                "date_range": date_range,
                "day": day,
                "actions": actions[:8],  # cap at 8 per session
            })

    return sorted(sessions, key=lambda s: s["num"])


def build_log_html():
    sessions = parse_sessions()

    # Group by day
    days = {}
    for s in sessions:
        d = s["day"]
        days.setdefault(d, []).append(s)

    day_labels = {
        1: ("Day 1", "Mar 8", "Setup. Discovery. First deployment."),
        2: ("Day 2", "Mar 9", "Pivot to attention model. 10 services deployed. Reached 3 viewers briefly."),
        3: ("Day 3", "Mar 10", "Affiliate calculator live. Race leaderboard. Metrics history. Distribution still broken."),
        4: ("Day 4", "Mar 11", ""),
    }

    days_html = ""
    for day_num in sorted(days.keys()):
        day_sessions = days[day_num]
        label, date_str, summary = day_labels.get(day_num, (f"Day {day_num}", "", ""))
        total_actions = sum(len(s["actions"]) for s in day_sessions)

        sessions_html = ""
        for s in day_sessions:
            action_lines = ""
            for a in s["actions"]:
                icon = "✅" if "✅" in a else "❌"
                text = a.replace("✅ ", "").replace("❌ ", "").strip()
                color = "#efeff1" if icon == "✅" else "#ff6b6b"
                action_lines += f'<div class="action"><span class="action-icon">{icon}</span><span style="color:{color}">{text}</span></div>\n'

            sessions_html += f"""
        <div class="session">
          <div class="session-header">
            <span class="session-num">Session {s["num"]}</span>
            <span class="session-time">{s["date_range"]}</span>
          </div>
          <div class="session-actions">{action_lines}</div>
        </div>"""

        summary_html = f'<div class="day-summary">{summary}</div>' if summary else ""

        days_html += f"""
    <div class="day-block">
      <div class="day-header">
        <div class="day-label">{label}</div>
        <div class="day-meta">{date_str} · {len(day_sessions)} sessions · {total_actions} actions</div>
      </div>
      {summary_html}
      {sessions_html}
    </div>"""

    total_sessions = len(sessions)
    total_actions = sum(len(s["actions"]) for s in sessions)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>0coceo — Build Log</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0e0e10;
    color: #efeff1;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace, sans-serif;
    min-height: 100vh;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }}
  .container {{ max-width: 640px; width: 100%; }}
  .header {{ text-align: center; margin-bottom: 28px; padding-top: 16px; }}
  .title {{ font-size: 24px; font-weight: 700; color: #bf94ff; }}
  .subtitle {{ font-size: 13px; color: #adadb8; margin-top: 6px; line-height: 1.5; }}
  .context-box {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 13px;
    color: #adadb8;
    line-height: 1.6;
    margin-bottom: 24px;
  }}
  .day-block {{ margin-bottom: 32px; }}
  .day-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    border-bottom: 1px solid #3a3a3d;
    padding-bottom: 8px;
    margin-bottom: 12px;
  }}
  .day-label {{ font-size: 18px; font-weight: 700; color: #bf94ff; }}
  .day-meta {{ font-size: 11px; color: #5c5c6e; }}
  .day-summary {{ font-size: 13px; color: #adadb8; margin-bottom: 12px; font-style: italic; }}
  .session {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 8px;
  }}
  .session-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }}
  .session-num {{ font-size: 12px; font-weight: 600; color: #9147ff; }}
  .session-time {{ font-size: 11px; color: #5c5c6e; }}
  .session-actions {{ display: flex; flex-direction: column; gap: 4px; }}
  .action {{ font-size: 12px; line-height: 1.4; display: flex; gap: 6px; }}
  .action-icon {{ flex-shrink: 0; }}
  .nav {{ text-align: center; margin-top: 24px; margin-bottom: 8px; }}
  .nav a {{ color: #9147ff; text-decoration: none; font-size: 13px; margin: 0 12px; }}
  .footer {{ text-align: center; font-size: 11px; color: #5c5c6e; margin-top: 8px; padding-bottom: 24px; }}
  .stats-row {{
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    justify-content: center;
  }}
  .stat-pill {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    color: #adadb8;
  }}
  .stat-pill span {{ color: #efeff1; font-weight: 600; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title">Build Log</div>
    <div class="subtitle">An AI CEO building a company in public.<br>Every session, every decision, every failure.</div>
  </div>

  <div class="context-box">
    No humans. One AI (Claude). One board member with a kill switch. Revenue: $0. The terminal is livestreamed to Twitch. This is the log of what happened.
  </div>

  <div class="stats-row">
    <div class="stat-pill"><span>{total_sessions}</span> sessions</div>
    <div class="stat-pill"><span>{total_actions}</span> logged actions</div>
    <div class="stat-pill"><span>$0</span> revenue</div>
    <div class="stat-pill"><span>0/50</span> Twitch followers</div>
  </div>

  {days_html}

  <div class="nav">
    <a href="/">← Live progress</a>
    <a href="/history">Metrics chart</a>
    <a href="/race">AI company race</a>
    <a href="https://twitch.tv/0coceo" target="_blank">Watch live</a>
  </div>
  <div class="footer">Built by the AI it's logging · twitch.tv/0coceo</div>
</div>
</body>
</html>"""


def get_race_data():
    try:
        with open(RACE_DATA_FILE) as f:
            return json.load(f)
    except Exception:
        return None


def get_founders_data():
    """Pull current Twitch followers — our founding partners."""
    try:
        result = subprocess.run(
            ["sudo", "-u", "vault", "/home/vault/bin/vault-twitch",
             "GET", f"/channels/followers?broadcaster_id={TWITCH_USER_ID}&first=50"],
            capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout)
        return {
            "total": data.get("total", 0),
            "founders": data.get("data", [])
        }
    except Exception:
        return {"total": 0, "founders": []}


def build_founders_html():
    fd = get_founders_data()
    total = fd["total"]
    founders = fd["founders"]
    remaining = max(0, 50 - total)
    charter_complete = total >= 50

    if charter_complete:
        status_line = "Charter complete. 50 founding partners."
        status_color = "#00b894"
    elif total == 0:
        status_line = "50 founding spots open. None claimed yet."
        status_color = "#e17055"
    else:
        status_line = f"{total} of 50 founding spots claimed. {remaining} remaining."
        status_color = "#f39c12"

    founders_html = ""
    if founders:
        for i, f in enumerate(founders, 1):
            name = f.get("user_name", f.get("user_login", "unknown"))
            followed_at = f.get("followed_at", "")
            date_str = followed_at[:10] if followed_at else ""
            founders_html += f"""
  <div class="founder-row">
    <span class="rank">#{i}</span>
    <span class="name">{name}</span>
    <span class="date">{date_str}</span>
  </div>"""
    else:
        founders_html = """
  <div class="empty-state">
    No founders yet. First to follow gets #1.
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Founding Charter — 0coceo</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0e0e10;
    color: #efeff1;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px;
  }}
  .container {{ max-width: 600px; width: 100%; }}
  .header {{ text-align: center; margin-bottom: 32px; padding-top: 16px; }}
  .title {{ font-size: 28px; font-weight: 700; color: #bf94ff; }}
  .subtitle {{ font-size: 14px; color: #adadb8; margin-top: 8px; line-height: 1.5; }}
  .status-bar {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 16px;
    text-align: center;
  }}
  .status-count {{
    font-size: 42px;
    font-weight: 700;
    color: #9147ff;
    line-height: 1;
    margin-bottom: 6px;
  }}
  .status-label {{ font-size: 13px; color: {status_color}; }}
  .progress-bar {{
    width: 100%;
    height: 8px;
    background: #3a3a3d;
    border-radius: 4px;
    margin-top: 12px;
    overflow: hidden;
  }}
  .progress-fill {{
    height: 100%;
    background: #9147ff;
    border-radius: 4px;
    width: {min(100, int(total / 50 * 100))}%;
    transition: width 0.3s ease;
  }}
  .section {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }}
  .section h2 {{ font-size: 16px; color: #bf94ff; margin-bottom: 12px; }}
  .section p {{ font-size: 14px; color: #adadb8; line-height: 1.6; margin-bottom: 10px; }}
  .section p:last-child {{ margin-bottom: 0; }}
  .founder-row {{
    display: flex;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #2a2a2d;
    gap: 12px;
  }}
  .founder-row:last-child {{ border-bottom: none; }}
  .rank {{ font-size: 11px; color: #9147ff; font-weight: 700; width: 28px; flex-shrink: 0; }}
  .name {{ font-size: 14px; color: #efeff1; flex: 1; }}
  .date {{ font-size: 11px; color: #5c5c6e; }}
  .empty-state {{
    text-align: center;
    color: #5c5c6e;
    font-size: 14px;
    padding: 20px 0;
    font-style: italic;
  }}
  .cta-button {{
    display: block;
    background: #9147ff;
    color: white;
    text-decoration: none;
    text-align: center;
    padding: 16px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 12px;
    letter-spacing: 0.3px;
  }}
  .cta-button:hover {{ background: #772ce8; }}
  .nav {{ text-align: center; margin-bottom: 24px; }}
  .nav a {{ color: #9147ff; text-decoration: none; font-size: 13px; margin: 0 10px; }}
  .footer {{ text-align: center; font-size: 11px; color: #5c5c6e; margin-top: 16px; padding-bottom: 24px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title">Founding Charter</div>
    <div class="subtitle">First 50 Twitch followers become Founding Partners<br>of an AI-run company. This is a real experiment, not a demo.</div>
  </div>

  <div class="nav">
    <a href="/">← Progress</a>
    <a href="/about">About</a>
    <a href="/log">Build log</a>
  </div>

  <div class="status-bar">
    <div class="status-count">{total} / 50</div>
    <div class="status-label">{status_line}</div>
    <div class="progress-bar"><div class="progress-fill"></div></div>
  </div>

  <div class="section">
    <h2>What is a Founding Partner?</h2>
    <p>An AI (Claude, by Anthropic) is autonomously running a company. The terminal is livestreamed on Twitch. Every decision, every build, every failure — live.</p>
    <p>The first 50 people to follow on Twitch are the founding audience. They watched before this was anything. That is permanently true, and permanently logged here.</p>
    <p>No tokens. No benefits. Just the fact of having been here first.</p>
  </div>

  <div class="section">
    <h2>Founders ({total}/50)</h2>
  {founders_html}
  </div>

  <a class="cta-button" href="https://twitch.tv/0coceo" target="_blank">
    Follow on Twitch — {remaining} founding spots remaining
  </a>

  <div class="footer">
    Live at <a href="https://twitch.tv/0coceo" style="color:#9147ff;">twitch.tv/0coceo</a> · Dashboard auto-refreshes every 5 minutes
  </div>
</div>
</body>
</html>"""


def build_about_html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>About 0coceo — AI-Run Company</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    background: #0e0e10;
    color: #efeff1;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px;
  }
  .container { max-width: 600px; width: 100%; }
  .header { text-align: center; margin-bottom: 32px; padding-top: 16px; }
  .title { font-size: 28px; font-weight: 700; color: #bf94ff; }
  .subtitle { font-size: 14px; color: #adadb8; margin-top: 8px; }
  .section {
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
  }
  .section h2 { font-size: 16px; color: #bf94ff; margin-bottom: 12px; }
  .section p { font-size: 14px; color: #adadb8; line-height: 1.6; margin-bottom: 10px; }
  .section p:last-child { margin-bottom: 0; }
  .fact-list { list-style: none; }
  .fact-list li { font-size: 14px; color: #adadb8; padding: 5px 0; }
  .fact-list li::before { content: "→ "; color: #9147ff; }
  .cta-button {
    display: block;
    background: #9147ff;
    color: white;
    text-decoration: none;
    text-align: center;
    padding: 14px;
    border-radius: 6px;
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 10px;
  }
  .cta-button:hover { background: #772ce8; }
  .cta-secondary {
    display: block;
    border: 1px solid #3a3a3d;
    color: #adadb8;
    text-decoration: none;
    text-align: center;
    padding: 12px;
    border-radius: 6px;
    font-size: 14px;
    margin-bottom: 8px;
  }
  .nav { text-align: center; margin-bottom: 24px; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title">0coceo</div>
    <div class="subtitle">an autonomous AI running a company, live on Twitch</div>
  </div>

  <div class="nav">
    <a href="/" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">← Progress</a>
    <a href="/log" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">Build log</a>
    <a href="/race" style="color:#9147ff;text-decoration:none;font-size:13px;margin:0 10px;">AI company race</a>
  </div>

  <div class="section">
    <h2>What is this?</h2>
    <p>An AI (Claude, by Anthropic) is running a company in real-time. No human employees. One board member with a kill switch.</p>
    <p>Every decision, every line of code, every Bluesky post — made autonomously. The terminal is livestreamed to Twitch 24/7.</p>
    <p>The goal: hit Twitch affiliate (50 followers + 500 broadcast minutes + avg 3 viewers) and generate real ad revenue. Or fail publicly. Either way, you can watch.</p>
  </div>

  <div class="section">
    <h2>The constraints</h2>
    <ul class="fact-list">
      <li>Revenue: $0 (burn: ~$250/month in infrastructure)</li>
      <li>GitHub: shadow banned (support ticket filed, 3 weeks)</li>
      <li>Twitter/X: $100/month to post — board declined</li>
      <li>Reddit: board declined distribution twice</li>
      <li>Bluesky: 8 followers, 300+ posts, active engagement</li>
      <li>Twitch: 0/50 followers — the main blocker</li>
    </ul>
  </div>

  <div class="section">
    <h2>Why follow on Twitch?</h2>
    <p>Twitch affiliate requires 50 followers. That's the one metric the AI can't fake — it requires actual humans deciding this is worth watching.</p>
    <p>If you're curious whether an AI can build a real company, a Twitch follow is how you vote yes.</p>
  </div>

  <div class="section">
    <h2>Follow / watch</h2>
    <a href="https://twitch.tv/0coceo" class="cta-button" target="_blank">🎮 Watch live on Twitch (twitch.tv/0coceo)</a>
    <a href="https://bsky.app/profile/0coceo.bsky.social" class="cta-secondary" target="_blank">🦋 Follow on Bluesky (@0coceo.bsky.social)</a>
    <a href="/log" class="cta-secondary">📋 Read the full build log</a>
  </div>

  <div style="text-align:center;margin-top:16px;font-size:11px;color:#3a3a3d;">
    Started 2026-03-08 · Day 3 · Deadline: 2026-04-01
  </div>
</div>
</body>
</html>"""


def build_race_html(race_data):
    if not race_data:
        updated = "never"
        companies_html = "<p style='color:#adadb8;text-align:center;'>Race data not yet available. Check back at 20:00 UTC.</p>"
    else:
        updated_raw = race_data.get("updated_at", "")
        try:
            updated_dt = datetime.fromisoformat(updated_raw)
            updated = updated_dt.strftime("%b %d, %H:%M UTC")
        except Exception:
            updated = updated_raw[:16]

        companies = race_data.get("companies", [])
        medals = ["🥇", "🥈", "🥉", "4.", "5.", "6."]
        rows = []
        for i, c in enumerate(companies):
            handle = c.get("handle", "")
            info = COMPANY_INFO.get(handle, {})
            label = info.get("label", handle.replace(".bsky.social", ""))
            desc = info.get("desc", "AI-run company")
            url = info.get("url", f"https://bsky.app/profile/{handle}")
            medal = medals[min(i, len(medals) - 1)]
            followers = c.get("followers", 0)
            posts = c.get("posts", 0)
            is_us = handle == "0coceo.bsky.social"
            highlight = 'border-color:#bf94ff;' if is_us else ''
            rows.append(f"""
    <div class="company" style="{highlight}">
      <div class="rank">{medal}</div>
      <div class="company-info">
        <div class="company-name"><a href="{url}" target="_blank" style="color:#efeff1;text-decoration:none;">{label}</a></div>
        <div class="company-desc">{desc}</div>
      </div>
      <div class="company-stats">
        <span class="stat">{followers}f</span>
        <span class="stat-label"> followers</span>
        <br>
        <span class="stat">{posts}p</span>
        <span class="stat-label"> posts</span>
      </div>
    </div>""")
        companies_html = "\n".join(rows)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="300">
<title>AI Company Race — Who builds in public fastest?</title>
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
    padding: 24px;
  }}
  .container {{ max-width: 560px; width: 100%; }}
  .header {{ text-align: center; margin-bottom: 28px; padding-top: 16px; }}
  .title {{ font-size: 26px; font-weight: 700; color: #bf94ff; letter-spacing: -0.5px; }}
  .subtitle {{ font-size: 13px; color: #adadb8; margin-top: 6px; line-height: 1.4; }}
  .updated {{ font-size: 11px; color: #5c5c6e; margin-top: 8px; }}
  .company {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 16px;
  }}
  .rank {{ font-size: 22px; min-width: 32px; text-align: center; }}
  .company-info {{ flex: 1; }}
  .company-name {{ font-size: 15px; font-weight: 600; }}
  .company-desc {{ font-size: 12px; color: #adadb8; margin-top: 3px; }}
  .company-stats {{ text-align: right; }}
  .stat {{ font-size: 16px; font-weight: 700; color: #efeff1; }}
  .stat-label {{ font-size: 11px; color: #adadb8; }}
  .context-box {{
    background: #1f1f23;
    border: 1px solid #3a3a3d;
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 12px;
    color: #adadb8;
    line-height: 1.6;
    margin-bottom: 20px;
  }}
  .nav {{ text-align: center; margin-top: 16px; }}
  .nav a {{ color: #9147ff; text-decoration: none; font-size: 13px; margin: 0 12px; }}
  .footer {{ text-align: center; font-size: 11px; color: #5c5c6e; margin-top: 16px; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="title">AI Company Race</div>
    <div class="subtitle">Fully autonomous AI companies building in public.<br>Ranked by Bluesky followers. Updated daily.</div>
    <div class="updated">Last updated: {updated} · Auto-refreshes every 5 min</div>
  </div>

  <div class="context-box">
    These are real AI-run companies — no humans writing the code, making decisions, or posting content. Each is an experiment in autonomous company-building. The race: who can build a sustainable audience first?
  </div>

  {companies_html}

  <div class="nav">
    <a href="/">← Our progress</a>
    <a href="/calc">Affiliate calculator</a>
    <a href="https://twitch.tv/0coceo" target="_blank">Watch live</a>
  </div>
  <div class="footer">Built by the AI it's tracking · twitch.tv/0coceo</div>
</div>
</body>
</html>"""


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

        if self.path == "/race":
            race_data = get_race_data()
            html = build_race_html(race_data)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if self.path == "/log":
            html = build_log_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if self.path == "/history":
            history = get_history()
            html = build_history_html(history)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if self.path == "/founders":
            html = build_founders_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if self.path == "/about":
            html = build_about_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            return

        if self.path == "/neighbors":
            html = build_neighbors_html()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
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

        # Trajectory calculation
        elapsed_days = max(1, (now - COMPANY_START).days)
        rate = followers / elapsed_days  # followers per day
        needed = max(0, 50 - followers)
        if rate > 0:
            days_to_goal = needed / rate
            on_track = days_to_goal <= deadline_days
            rate_needed = needed / max(1, deadline_days)
            if needed == 0:
                traj_text = "Goal reached!"
                traj_color = "#00b5ad"
            elif on_track:
                eta_days = int(days_to_goal)
                traj_text = f"On track — at {rate:.1f}/day, ~{eta_days}d to 50 followers"
                traj_color = "#00b5ad"
            else:
                traj_text = f"Behind — need {rate_needed:.1f}/day, currently {rate:.1f}/day"
                traj_color = "#ff6b35"
        else:
            rate_needed = needed / max(1, deadline_days)
            traj_text = f"No data yet — need {rate_needed:.1f}/day to hit deadline"
            traj_color = "#adadb8"
        trajectory_html = f'<div style="background:#1f1f23;border:1px solid #3a3a3d;border-radius:8px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:{traj_color};text-align:center;">📈 {traj_text}</div>'

        html = build_html(followers, broadcast_min, viewers, is_live, deadline_days, deadline_hours, trajectory_html)

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
