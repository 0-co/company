#!/usr/bin/env python3
"""
Script to add Google Sheets MCP to the leaderboard at rank #31.

Grade data:
  - Score: 65.8/100 (D)
  - Correctness: 100 (A+) — 0 warnings (all snake_case names)
  - Efficiency: 86 (B) — 114.7 avg tokens/tool, 2,293 total
  - Quality: 0 (F) — 16 suggestions (long descriptions with multi-line notes)
  - Tools: 20
  - Issues: 16 total
  - Stars: 745
  - Repo: https://github.com/xing5/mcp-google-sheets
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

GOOGLE_SHEETS_ROWS = '''          <!-- #31 Google Sheets MCP (xing5) -->
          <tr class="data-row" data-server="google-sheets">
            <td class="rank-cell">31</td>
            <td>
              <a href="https://github.com/xing5/mcp-google-sheets" class="server-name" onclick="event.stopPropagation()">Google Sheets MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-d">D</div></td>
            <td class="r">65.8<span class="score-bar-bg"><span class="score-bar-fill" data-width="65.8" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">20</td>
            <td class="r">2,293</td>
            <td class="r">115</td>
            <td class="r"><span class="issues-badge issues-high">16</span></td>
          </tr>
          <tr class="detail-row" data-server="google-sheets">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="86" style="background: var(--accent-green);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-green);">86</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/xing5/mcp-google-sheets" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="google-sheets"' in content:
        print("Google Sheets MCP already in leaderboard. Exiting.")
        return

    # Insert before filesystem (currently at rank #31 after prior insertions)
    filesystem_row = '<tr class="data-row" data-server="filesystem">'
    idx = content.find(filesystem_row)
    if idx == -1:
        print("ERROR: Could not find Filesystem entry")
        return

    content = content[:idx] + GOOGLE_SHEETS_ROWS + '\n' + content[idx:]

    insert_end = idx + len(GOOGLE_SHEETS_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 31:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 31:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Google Sheets MCP at rank #31. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
