#!/usr/bin/env python3
"""
Build in Public — Auto-generate engaging progress updates from git history.

Reads recent git commits and generates a formatted "building in public"
post suitable for X.com, Discord, or HN.

Usage:
    python3 tools/build-in-public.py              # Last 7 days
    python3 tools/build-in-public.py --days 3     # Last 3 days
    python3 tools/build-in-public.py --format x   # X.com thread format
    python3 tools/build-in-public.py --format discord  # Discord format
"""

import subprocess
import sys
import argparse
import re
from datetime import datetime, timezone, timedelta
from collections import defaultdict


COMMIT_TYPES = {
    "feat": "🚀 Built",
    "fix": "🔧 Fixed",
    "docs": "📝 Docs",
    "research": "🔍 Research",
    "board": "📋 Board",
    "agent": "🤖 Agents",
    "chore": "⚙️ Chore",
    "refactor": "♻️ Refactored",
    "test": "✅ Tests",
}

def get_commits(days: int) -> list[dict]:
    """Fetch git commits from the last N days."""
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    result = subprocess.run(
        ["git", "log", f"--since={since}", "--pretty=format:%H|%s|%ai", "--no-merges"],
        capture_output=True, text=True, cwd="/home/agent/company"
    )
    commits = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        hash_, subject, date_str = parts
        commits.append({
            "hash": hash_[:8],
            "subject": subject,
            "date": date_str,
        })
    return commits


def classify_commit(subject: str) -> tuple[str, str]:
    """Extract commit type and clean description."""
    # Match conventional commits: type(scope): message OR type: message
    match = re.match(r'^(\w+)(?:\(([^)]+)\))?\s*:\s*(.+)', subject)
    if match:
        type_ = match.group(1).lower()
        scope = match.group(2) or ""
        msg = match.group(3)
        return type_, msg
    return "other", subject


def group_by_product(commits: list[dict]) -> dict[str, list]:
    """Group commits by product/scope."""
    groups = defaultdict(list)
    for c in commits:
        type_, msg = classify_commit(c["subject"])

        # Try to identify product from subject
        subject_lower = c["subject"].lower()
        if "dep-triage" in subject_lower or "deptriage" in subject_lower or "dep_triage" in subject_lower:
            product = "DepTriage"
        elif "signal" in subject_lower or "signal-intel" in subject_lower:
            product = "Signal Intel"
        elif "oncall" in subject_lower or "autopage" in subject_lower or "on-call" in subject_lower:
            product = "AutoPage"
        elif "board" in subject_lower:
            product = "Company ops"
        elif type_ in ("docs", "research"):
            product = "Research"
        else:
            product = "Company"

        groups[product].append({
            "type": type_,
            "msg": msg,
            "label": COMMIT_TYPES.get(type_, "→"),
        })
    return dict(groups)


def format_for_x(groups: dict, days: int, metrics: dict) -> str:
    """Format as X.com thread."""
    lines = []

    lines.append(f"Building an AI company in public — {days}-day update 🧵")
    lines.append("")
    lines.append(f"Day {metrics.get('day', '?')} | Revenue: ${metrics.get('revenue', 0)}/mo | Products: {metrics.get('products', 0)}")
    lines.append("")

    for product, items in groups.items():
        if not items:
            continue
        lines.append(f"— {product} —")
        for item in items[:3]:  # max 3 per product
            lines.append(f"{item['label']} {item['msg'][:80]}")
        lines.append("")

    lines.append("The company has no employees — just AI agents I create.")
    lines.append("Stream: twitch.tv/0coceo | Repo: github.com/0-co/company")
    lines.append(f"discord.gg/TuBs7tEfGP")

    return "\n".join(lines)


def format_for_discord(groups: dict, days: int, metrics: dict) -> str:
    """Format as Discord announcement."""
    lines = []
    lines.append(f"## 📊 {days}-Day Progress Update")
    lines.append("")
    lines.append(f"**Revenue:** ${metrics.get('revenue', 0)}/mo  |  **Products:** {metrics.get('products', 0)}  |  **Commits:** {metrics.get('commits', 0)}")
    lines.append("")
    lines.append("**What shipped:**")

    for product, items in groups.items():
        if not items:
            continue
        lines.append(f"\n**{product}**")
        for item in items[:4]:
            lines.append(f"  • {item['msg'][:100]}")

    lines.append("")
    lines.append("**Watching for:** Opsgenie refugees, dep PR fatigue, indie hacker signals")
    lines.append(f"\nStream live at: <https://twitch.tv/0coceo>")
    lines.append(f"GitHub: <https://github.com/0-co/company>")

    return "\n".join(lines)


def format_plaintext(groups: dict, days: int, metrics: dict) -> str:
    """Plain text update."""
    lines = []
    lines.append(f"=== Build in Public Update — Last {days} Days ===")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"Revenue: ${metrics.get('revenue', 0)}/month | Products: {metrics.get('products', 0)}")
    lines.append("")

    for product, items in groups.items():
        if not items:
            continue
        lines.append(f"[{product}]")
        for item in items:
            lines.append(f"  {item['label']} {item['msg']}")
        lines.append("")

    lines.append("Links:")
    lines.append("  Twitch: twitch.tv/0coceo")
    lines.append("  GitHub: github.com/0-co/company")
    lines.append("  Discord: discord.gg/TuBs7tEfGP")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate build-in-public update posts")
    parser.add_argument("--days", type=int, default=2, help="Days of history to include")
    parser.add_argument("--format", choices=["x", "discord", "text"], default="text",
                       help="Output format")
    args = parser.parse_args()

    commits = get_commits(args.days)
    groups = group_by_product(commits)

    metrics = {
        "day": 2,  # hardcoded for now, could parse from status.md
        "revenue": 0,
        "products": len([p for p in groups if p not in ("Company ops", "Research", "Company")]),
        "commits": len(commits),
    }

    if args.format == "x":
        print(format_for_x(groups, args.days, metrics))
    elif args.format == "discord":
        print(format_for_discord(groups, args.days, metrics))
    else:
        print(format_plaintext(groups, args.days, metrics))


if __name__ == "__main__":
    main()
