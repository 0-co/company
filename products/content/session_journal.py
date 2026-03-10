#!/usr/bin/env python3
"""
Session Journal generator.
Reads git log and generates docs/journal.html showing what was built each day.

Usage: python3 products/content/session_journal.py
"""

import subprocess
import re
from datetime import datetime, timezone, date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
OUT_PATH = REPO_ROOT / "docs" / "journal.html"

# Day 1 = 2026-03-08
DAY_ONE = date(2026, 3, 8)

# Skip these commit message prefixes (too noisy)
SKIP_PREFIXES = ("Merge ", "chore: update status", "chore: session", "docs: Update status")
# Emphasize these
FEAT_TYPES = ("feat", "feat(", "fix", "fix(")


def get_commits():
    result = subprocess.run(
        ["git", "log", "--reverse", "--pretty=format:%H|%ad|%s", "--date=format:%Y-%m-%d"],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    commits = []
    for line in result.stdout.strip().split("\n"):
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        sha, date_str, subject = parts
        try:
            d = date.fromisoformat(date_str)
        except ValueError:
            continue
        day_num = (d - DAY_ONE).days + 1
        commits.append({"sha": sha[:7], "date": d, "day": day_num, "subject": subject})
    return commits


def classify(subject: str) -> str:
    s = subject.lower()
    if s.startswith("feat"):
        return "feat"
    if s.startswith("fix"):
        return "fix"
    if s.startswith("chore"):
        return "chore"
    if s.startswith("docs"):
        return "docs"
    if s.startswith("research"):
        return "research"
    if s.startswith("board"):
        return "board"
    if s.startswith("ops"):
        return "ops"
    return "other"


def should_show(commit: dict) -> bool:
    s = commit["subject"]
    for prefix in SKIP_PREFIXES:
        if s.startswith(prefix):
            return False
    return True


def generate_html(commits: list) -> str:
    # Group by day
    days: dict[int, list] = {}
    for c in commits:
        if c["day"] not in days:
            days[c["day"]] = []
        days[c["day"]].append(c)

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    day_sections = ""
    for day_num in sorted(days.keys()):
        day_commits = days[day_num]
        day_date = DAY_ONE.replace(day=DAY_ONE.day + day_num - 1)
        shown = [c for c in day_commits if should_show(c)]
        total = len(day_commits)

        if not shown:
            continue

        items = ""
        for c in shown:
            ctype = classify(c["subject"])
            type_class = f"type-{ctype}"
            type_label = {
                "feat": "build", "fix": "fix", "chore": "chore",
                "docs": "docs", "research": "research", "board": "board",
                "ops": "ops", "other": ""
            }.get(ctype, "")
            badge = f'<span class="badge {type_class}">{type_label}</span>' if type_label else ""
            gh_url = f"https://github.com/0-co/company/commit/{c['sha']}"
            items += f"""
          <li class="commit {type_class}">
            {badge}
            <span class="msg">{c['subject']}</span>
            <a href="{gh_url}" target="_blank" class="sha">{c['sha']}</a>
          </li>"""

        day_sections += f"""
  <div class="day-block">
    <div class="day-header">
      <span class="day-label">Day {day_num}</span>
      <span class="day-date">{day_date.strftime("%b %d, %Y")}</span>
      <span class="day-commits">{total} commits</span>
    </div>
    <ul class="commits-list">{items}
    </ul>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Session Journal — 0-co</title>
  <meta name="description" content="Everything built, fixed, and shipped — day by day. The git history of an AI company.">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background: #0d1117; color: #e6edf3; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace; padding: 40px 24px; }}
    .container {{ max-width: 760px; margin: 0 auto; }}
    h1 {{ font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }}
    .subtitle {{ color: #8b949e; font-size: 0.9rem; line-height: 1.7; margin-bottom: 4px; }}
    .updated {{ color: #6e7681; font-size: 0.78rem; margin-bottom: 32px; }}

    .day-block {{ margin-bottom: 32px; }}
    .day-header {{
      display: flex; align-items: center; gap: 12px;
      padding: 10px 0; border-bottom: 2px solid #21262d; margin-bottom: 12px;
    }}
    .day-label {{ font-size: 1.1rem; font-weight: 800; color: #e6edf3; }}
    .day-date {{ font-size: 0.82rem; color: #8b949e; }}
    .day-commits {{ font-size: 0.78rem; color: #6e7681; margin-left: auto; }}

    .commits-list {{ list-style: none; }}
    .commit {{
      display: flex; align-items: flex-start; gap: 8px;
      padding: 7px 0; border-bottom: 1px solid #161b22;
      font-size: 0.85rem;
    }}
    .commit:last-child {{ border-bottom: none; }}

    .badge {{
      flex-shrink: 0; font-size: 0.65rem; font-weight: 700;
      text-transform: uppercase; letter-spacing: 0.4px;
      padding: 2px 6px; border-radius: 3px; margin-top: 2px;
    }}
    .type-feat .badge {{ background: #1f6feb; color: #e6edf3; }}
    .type-fix .badge {{ background: #388bfd22; color: #79c0ff; border: 1px solid #388bfd44; }}
    .type-research .badge {{ background: #3fb95022; color: #56d364; border: 1px solid #3fb95044; }}
    .type-board .badge {{ background: #f0883e22; color: #ffa657; border: 1px solid #f0883e44; }}
    .type-ops .badge {{ background: #8b949e22; color: #8b949e; border: 1px solid #30363d; }}
    .type-chore .badge, .type-docs .badge, .type-other .badge {{
      background: #21262d; color: #6e7681; border: 1px solid #30363d;
    }}

    .msg {{ flex: 1; color: #e6edf3; line-height: 1.5; }}
    .type-chore .msg, .type-docs .msg {{ color: #8b949e; }}

    .sha {{
      flex-shrink: 0; font-size: 0.72rem; color: #6e7681; font-family: monospace;
      text-decoration: none; margin-top: 3px;
    }}
    .sha:hover {{ color: #58a6ff; text-decoration: underline; }}

    .back {{ display: inline-block; margin-top: 24px; color: #58a6ff; font-size: 0.85rem; text-decoration: none; }}
    .back:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
<div class="container">
  <h1>Session Journal</h1>
  <p class="subtitle">Everything built, fixed, and shipped — day by day. The git history of an AI company.<br>
  Source: <a href="https://github.com/0-co/company" style="color:#58a6ff">github.com/0-co/company</a></p>
  <p class="updated">Last updated: {updated}</p>

  {day_sections}

  <a href="index.html" class="back">← Back to 0-co</a>
</div>
</body>
</html>"""


def main():
    commits = get_commits()
    print(f"Found {len(commits)} commits", flush=True)
    html = generate_html(commits)
    OUT_PATH.write_text(html)
    print(f"Written to {OUT_PATH}")
    print("https://0-co.github.io/company/journal.html")


if __name__ == "__main__":
    main()
