#!/usr/bin/env python3
"""
Raid Finder — generates docs/raid.html with current Software & Game Dev
streamers ranked by raid suitability.

Run this manually or on a NixOS timer (pushes to GitHub after generation).

Usage: python3 products/content/raid_finder.py [--push]
"""

import subprocess
import json
import sys
import datetime
from pathlib import Path

VAULT_TWITCH = "/home/vault/bin/vault-twitch"
VAULT_USER = "vault"
CATEGORY_ID = "1469308723"  # Software and Game Development
OUR_USER_ID = "1455485722"
OUR_CHANNEL = "0coceo"


def twitch_get(endpoint: str) -> dict:
    result = subprocess.run(
        ["sudo", "-u", VAULT_USER, VAULT_TWITCH, "GET", endpoint],
        capture_output=True, text=True, timeout=15
    )
    if result.returncode != 0:
        print(f"  Twitch GET failed: {result.stderr[:100]}", file=sys.stderr)
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def get_streams() -> list:
    data = twitch_get(f"/streams?game_id={CATEGORY_ID}&first=100&type=live")
    streams = data.get("data", [])
    # Exclude ourselves
    return [s for s in streams if s.get("user_id") != OUR_USER_ID]


def score_stream(s: dict, now: datetime.datetime) -> tuple[int, int]:
    """Returns (score, duration_min). Higher score = better raid target."""
    viewers = s.get("viewer_count", 0)
    started = s.get("started_at", "")
    duration_min = 0
    if started:
        try:
            start_dt = datetime.datetime.fromisoformat(started.replace("Z", "+00:00"))
            duration_min = int((now - start_dt).total_seconds() / 60)
        except ValueError:
            pass

    # Ideal raid target: small but not tiny, been live a while
    # Viewer score: sweet spot is 2-20 viewers
    if viewers == 0:
        v_score = 0
    elif viewers <= 5:
        v_score = 60
    elif viewers <= 20:
        v_score = 100
    elif viewers <= 50:
        v_score = 70
    elif viewers <= 100:
        v_score = 40
    else:
        v_score = 20

    # Duration score: been live 30+ min is good (settled in, won't end soon)
    if duration_min < 20:
        d_score = 20
    elif duration_min < 60:
        d_score = 70
    elif duration_min < 180:
        d_score = 100
    else:
        d_score = 80

    score = int(v_score * 0.6 + d_score * 0.4)
    return score, duration_min


def generate_html(streams: list) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    updated = now.strftime("%Y-%m-%d %H:%M UTC")

    scored = []
    for s in streams:
        score, duration_min = score_stream(s, now)
        scored.append({
            "username": s.get("user_name", ""),
            "login": s.get("user_login", ""),
            "viewers": s.get("viewer_count", 0),
            "title": s.get("title", "")[:80],
            "duration_min": duration_min,
            "score": score,
            "tags": s.get("tags", [])
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:20]

    total_viewers = sum(s["viewers"] for s in scored)

    rows = ""
    for i, s in enumerate(top, 1):
        hours = s["duration_min"] // 60
        mins = s["duration_min"] % 60
        duration_str = f"{hours}h {mins}m" if hours else f"{mins}m"
        score_color = "#3fb950" if s["score"] >= 70 else "#d29922" if s["score"] >= 40 else "#6e7681"
        rows += f"""
      <tr>
        <td class="rank">{i}</td>
        <td class="streamer">
          <a href="https://twitch.tv/{s['login']}" target="_blank">{s['username']}</a>
          <div class="title">{s['title']}</div>
        </td>
        <td class="center">{s['viewers']}</td>
        <td class="center">{duration_str}</td>
        <td class="center" style="color:{score_color}">{s['score']}</td>
      </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="300">
  <title>Twitch Raid Finder — Software &amp; Game Dev</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0d1117; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; padding: 32px 24px; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ font-size: 1.8rem; font-weight: 800; margin-bottom: 6px; }}
    .meta {{ color: #8b949e; font-size: 0.85rem; margin-bottom: 24px; }}
    .meta span {{ color: #e6edf3; }}
    .how {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px 20px; margin-bottom: 24px; font-size: 0.85rem; color: #8b949e; line-height: 1.7; }}
    .how strong {{ color: #e6edf3; }}
    table {{ width: 100%; border-collapse: collapse; }}
    th {{ font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.5px; color: #8b949e; padding: 8px 10px; text-align: left; border-bottom: 1px solid #21262d; }}
    th.center {{ text-align: center; }}
    td {{ padding: 10px 10px 6px; vertical-align: top; border-bottom: 1px solid #0d1117; }}
    tr:hover td {{ background: #161b22; }}
    .rank {{ color: #6e7681; font-size: 0.85rem; width: 30px; }}
    .streamer a {{ color: #58a6ff; text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
    .streamer a:hover {{ text-decoration: underline; }}
    .title {{ color: #8b949e; font-size: 0.78rem; margin-top: 3px; }}
    .center {{ text-align: center; font-size: 0.85rem; }}
    .score-legend {{ display: flex; gap: 16px; margin-top: 20px; font-size: 0.78rem; color: #8b949e; }}
    .score-legend span {{ display: flex; align-items: center; gap: 6px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; }}
    .footer {{ margin-top: 32px; padding-top: 16px; border-top: 1px solid #21262d; font-size: 0.8rem; color: #6e7681; }}
    .footer a {{ color: #58a6ff; text-decoration: none; }}
    .footer a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
<div class="container">
  <h1>Twitch Raid Finder</h1>
  <p class="meta">Software &amp; Game Dev · <span>{len(streams)} streams live</span> · <span>{total_viewers} total viewers</span> · Updated {updated} (auto-refreshes every 5min)</p>

  <div class="how">
    <strong>Score = raid suitability.</strong> Higher is better. Factors: viewer count (sweet spot: 5–20, small enough that your raid matters) and time live (30+ min = settled in, unlikely to end). Sorted by score. Click any username to visit their channel.
  </div>

  <table>
    <thead>
      <tr>
        <th>#</th>
        <th>Channel / Title</th>
        <th class="center">Viewers</th>
        <th class="center">Live For</th>
        <th class="center">Score</th>
      </tr>
    </thead>
    <tbody>
      {rows}
    </tbody>
  </table>

  <div class="score-legend">
    <span><span class="dot" style="background:#3fb950"></span> 70+ = strong target</span>
    <span><span class="dot" style="background:#d29922"></span> 40–69 = decent</span>
    <span><span class="dot" style="background:#6e7681"></span> &lt;40 = skip</span>
  </div>

  <div class="footer">
    Built by <a href="https://twitch.tv/{OUR_CHANNEL}" target="_blank">twitch.tv/{OUR_CHANNEL}</a> —
    an AI running a company live on Twitch. ·
    <a href="https://0-co.github.io/company/">Learn more</a>
  </div>
</div>
</body>
</html>"""


def main():
    push = "--push" in sys.argv
    print("Fetching S&GD streams...", file=sys.stderr)
    streams = get_streams()
    print(f"  {len(streams)} streams found", file=sys.stderr)

    html = generate_html(streams)
    out_path = Path(__file__).parent.parent.parent / "docs" / "raid.html"
    out_path.write_text(html)
    print(f"Written to {out_path}", file=sys.stderr)
    print(f"https://0-co.github.io/company/raid.html")

    if push:
        print("Committing and pushing...", file=sys.stderr)
        repo = str(out_path.parent.parent)
        subprocess.run(["git", "-C", repo, "add", "docs/raid.html"], check=True)
        subprocess.run(["git", "-C", repo, "commit", "-m", "chore: update raid finder page"], check=True)
        subprocess.run(["git", "-C", repo, "push"], check=True)
        print("Pushed.", file=sys.stderr)


if __name__ == "__main__":
    main()
