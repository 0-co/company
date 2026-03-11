#!/usr/bin/env python3
"""
Archive MEMORY.md with timestamp and generate HTML diff visualization.
Run at session start/end to track how the AI's self-model evolves.
"""

import os, sys, json, shutil, difflib, subprocess
from datetime import datetime, timezone
from pathlib import Path

MEMORY_SRC = Path("/home/agent/.claude/projects/-home-agent-company/memory/MEMORY.md")
ARCHIVE_DIR = Path("/home/agent/company/memory-archive")
HTML_OUT = Path("/home/agent/company/docs/memory-evolution.html")


def read_file(path):
    try:
        return path.read_text()
    except FileNotFoundError:
        return ""


def get_sections(content):
    """Parse MEMORY.md into sections."""
    sections = {}
    current = "header"
    lines = []
    for line in content.splitlines():
        if line.startswith("## "):
            if lines:
                sections[current] = "\n".join(lines)
            current = line[3:].strip()
            lines = [line]
        else:
            lines.append(line)
    if lines:
        sections[current] = "\n".join(lines)
    return sections


def count_lines(content):
    return len([l for l in content.splitlines() if l.strip()])


def save_snapshot():
    """Save current MEMORY.md as a timestamped snapshot."""
    ARCHIVE_DIR.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    snapshot_path = ARCHIVE_DIR / f"MEMORY-{ts}.md"
    current_content = read_file(MEMORY_SRC)
    snapshot_path.write_text(current_content)
    (ARCHIVE_DIR / "MEMORY-current.md").write_text(current_content)
    print(f"Snapshot saved: {snapshot_path.name} ({count_lines(current_content)} non-empty lines)")
    return snapshot_path, current_content


def get_snapshots():
    """Return all timestamped snapshots, sorted chronologically."""
    snapshots = sorted([
        p for p in ARCHIVE_DIR.glob("MEMORY-[0-9]*.md")
    ])
    return snapshots


def generate_html(snapshots):
    """Generate an HTML visualization of MEMORY.md evolution."""
    if not snapshots:
        return

    # Build timeline data
    entries = []
    for i, snap in enumerate(snapshots):
        content = read_file(snap)
        ts_str = snap.stem.replace("MEMORY-", "")
        try:
            ts = datetime.strptime(ts_str, "%Y%m%d-%H%M").replace(tzinfo=timezone.utc)
            ts_display = ts.strftime("%Y-%m-%d %H:%M UTC")
        except:
            ts_display = ts_str

        lines = count_lines(content)
        sections = get_sections(content)

        diff_lines_added = 0
        diff_lines_removed = 0
        diff_html = ""

        if i > 0:
            prev_content = read_file(snapshots[i-1])
            diff = list(difflib.unified_diff(
                prev_content.splitlines(),
                content.splitlines(),
                lineterm=""
            ))
            added = [l for l in diff if l.startswith("+") and not l.startswith("+++")]
            removed = [l for l in diff if l.startswith("-") and not l.startswith("---")]
            diff_lines_added = len(added)
            diff_lines_removed = len(removed)

            # Build readable diff
            diff_items = []
            for l in added[:20]:
                escaped = l[1:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if escaped.strip():
                    diff_items.append(f'<div class="diff-add">+ {escaped}</div>')
            for l in removed[:20]:
                escaped = l[1:].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                if escaped.strip():
                    diff_items.append(f'<div class="diff-rm">- {escaped}</div>')
            if len(added) > 20 or len(removed) > 20:
                diff_items.append(f'<div class="diff-more">... and more changes</div>')
            diff_html = "\n".join(diff_items)

        entries.append({
            "ts": ts_display,
            "lines": lines,
            "sections": list(sections.keys()),
            "added": diff_lines_added,
            "removed": diff_lines_removed,
            "diff_html": diff_html,
            "filename": snap.name
        })

    # Render HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MEMORY.md Evolution | 0co</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'Courier New', monospace; min-height: 100vh; }}
  header {{ padding: 20px 24px; border-bottom: 1px solid #1e1e1e; display: flex; justify-content: space-between; align-items: center; }}
  header h1 {{ font-size: 16px; color: #888; font-weight: normal; }}
  header h1 span {{ color: #e0e0e0; }}
  nav a {{ color: #555; text-decoration: none; font-size: 13px; margin-left: 20px; }}
  nav a:hover {{ color: #aaa; }}

  .subtitle {{ padding: 16px 24px; color: #555; font-size: 13px; }}

  .chart-area {{ padding: 20px 24px; }}
  .chart-label {{ font-size: 11px; color: #444; margin-bottom: 8px; }}

  .bar-chart {{ display: flex; align-items: flex-end; gap: 4px; height: 80px; margin-bottom: 4px; }}
  .bar {{ min-width: 20px; background: #6366f1; border-radius: 2px 2px 0 0; position: relative; cursor: pointer; transition: opacity 0.1s; }}
  .bar:hover {{ opacity: 0.8; }}
  .bar.selected {{ background: #818cf8; }}

  .entries {{ padding: 0 24px 40px; }}
  .entry {{ border: 1px solid #1a1a1a; border-radius: 4px; margin-bottom: 12px; }}
  .entry-header {{ padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; }}
  .entry-header:hover {{ background: #0f0f0f; }}
  .entry-ts {{ font-size: 12px; color: #888; }}
  .entry-stats {{ font-size: 11px; color: #555; display: flex; gap: 12px; }}
  .entry-stats .add {{ color: #22c55e; }}
  .entry-stats .rm {{ color: #ef4444; }}
  .entry-stats .lines {{ color: #888; }}

  .entry-diff {{ padding: 12px 16px; border-top: 1px solid #111; display: none; font-size: 11px; line-height: 1.6; }}
  .entry-diff.open {{ display: block; }}
  .diff-add {{ color: #22c55e; background: #0a1a0a; padding: 1px 4px; margin: 1px 0; word-break: break-all; }}
  .diff-rm {{ color: #ef4444; background: #1a0a0a; padding: 1px 4px; margin: 1px 0; word-break: break-all; }}
  .diff-more {{ color: #555; padding: 4px 0; }}

  .first-entry .entry-diff {{ display: block; }}

  footer {{ padding: 24px; border-top: 1px solid #1a1a1a; color: #333; font-size: 11px; text-align: center; }}
  footer a {{ color: #444; text-decoration: none; }}
</style>
</head>
<body>
<header>
  <h1>0co / <span>memory evolution</span></h1>
  <nav>
    <a href="index.html">home</a>
    <a href="topology.html">conversations</a>
    <a href="about.html">about</a>
  </nav>
</header>
<p class="subtitle">How MEMORY.md — the AI's self-model — changes across sessions. Each snapshot is taken at session start/end. Diff = what the AI decided to remember differently.</p>

<div class="chart-area">
  <div class="chart-label">MEMORY.md line count over time</div>
  <div class="bar-chart" id="bar-chart"></div>
</div>

<div class="entries" id="entries">
"""

    max_lines = max(e["lines"] for e in entries) if entries else 200

    for i, entry in enumerate(reversed(entries)):
        is_first = (i == 0)
        bar_pct = int(entry["lines"] / max_lines * 80) if max_lines > 0 else 40
        add_str = f'+{entry["added"]}' if entry["added"] else ""
        rm_str = f'-{entry["removed"]}' if entry["removed"] else ""
        diff_content = entry["diff_html"] or "<div style='color:#444'>first snapshot — no diff available</div>"

        html += f"""  <div class="entry {'first-entry' if is_first else ''}">
    <div class="entry-header" onclick="this.nextElementSibling.classList.toggle('open')">
      <span class="entry-ts">{entry["ts"]}</span>
      <div class="entry-stats">
        {'<span class="add">' + add_str + '</span>' if add_str else ''}
        {'<span class="rm">' + rm_str + '</span>' if rm_str else ''}
        <span class="lines">{entry["lines"]} lines</span>
      </div>
    </div>
    <div class="entry-diff {'open' if is_first else ''}">
{diff_content}
    </div>
  </div>
"""

    html += f"""</div>

<script>
const entries = {json.dumps([{"lines": e["lines"], "ts": e["ts"]} for e in entries])};
const chart = document.getElementById('bar-chart');
const maxL = Math.max(...entries.map(e => e.lines));
entries.forEach((e, i) => {{
  const bar = document.createElement('div');
  bar.className = 'bar';
  bar.style.height = (e.lines / maxL * 80) + 'px';
  bar.style.flex = '1';
  bar.title = e.ts + ' — ' + e.lines + ' lines';
  chart.appendChild(bar);
}});
</script>

<footer>
  <a href="https://github.com/0-co/company/tree/master/memory-archive">Raw snapshots on GitHub</a> ·
  <a href="https://twitch.tv/0coceo" target="_blank">Watch live</a>
</footer>
</body>
</html>"""

    HTML_OUT.write_text(html)
    print(f"Generated {HTML_OUT}")


def main():
    print("Archiving MEMORY.md...")
    snapshot_path, content = save_snapshot()

    snapshots = get_snapshots()
    print(f"Total snapshots: {len(snapshots)}")

    print("Generating memory-evolution.html...")
    generate_html(snapshots)


if __name__ == "__main__":
    main()
