#!/usr/bin/env python3
"""
Script to add Notion MCP (danhilse) to the leaderboard at rank #2.

Grade data:
  - Score: 100.0/100 (A+)
  - Correctness: 100 (A+) — 0 warnings (all snake_case, clean)
  - Efficiency: 100 (A+) — 38.3 avg tokens/tool, 153 total
  - Quality: 100 (A+) — 0 suggestions
  - Tools: 4 (add_todo, show_all_todos, show_today_todos, complete_todo)
  - Issues: 0 total
  - Stars: 205
  - Repo: https://github.com/danhilse/notion_mcp

Narrative: Minimal Notion MCP that scores perfect 100. Simple 4-tool design,
each with concise description. Stark contrast to official Notion MCP (F, 19.8).
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

DANHILSE_NOTION_ROWS = '''          <!-- #2 Notion MCP (danhilse) -->
          <tr class="data-row" data-server="danhilse-notion">
            <td class="rank-cell">2</td>
            <td>
              <a href="https://github.com/danhilse/notion_mcp" class="server-name" onclick="event.stopPropagation()">Notion MCP (danhilse)</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-aplus">A+</div></td>
            <td class="r">100.0<span class="score-bar-bg"><span class="score-bar-fill" data-width="100" style="background: var(--accent-cyan);"></span></span></td>
            <td class="r">4</td>
            <td class="r">153</td>
            <td class="r">38</td>
            <td class="r"><span class="issues-badge issues-none">0</span></td>
          </tr>
          <tr class="detail-row" data-server="danhilse-notion">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/danhilse/notion_mcp" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="danhilse-notion"' in content:
        print("Danhilse Notion MCP already in leaderboard. Exiting.")
        return

    # Insert before sqlite (currently at rank #2)
    sqlite_row = '<tr class="data-row" data-server="sqlite">'
    idx = content.find(sqlite_row)
    if idx == -1:
        print("ERROR: Could not find SQLite entry")
        return

    content = content[:idx] + DANHILSE_NOTION_ROWS + '\n' + content[idx:]

    insert_end = idx + len(DANHILSE_NOTION_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 2:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 2:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Danhilse Notion MCP at rank #2. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
