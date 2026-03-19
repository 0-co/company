#!/usr/bin/env python3
"""
Script to add Linear MCP to the leaderboard at rank #28.

Grade data:
  - Score: 68.8/100 (D+)
  - Correctness: 100 (A+) — 0 warnings (all linear_ prefix, snake_case)
  - Efficiency: 71 (C) — 180.4 avg tokens/tool, 902 total
  - Quality: 25 (F) — 5 suggestions (long sentence-style tool descriptions)
  - Tools: 5
  - Issues: 5 total
  - Stars: 347
  - Repo: https://github.com/jerhadf/linear-mcp-server
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

LINEAR_ROWS = '''          <!-- #28 Linear MCP -->
          <tr class="data-row" data-server="linear">
            <td class="rank-cell">28</td>
            <td>
              <a href="https://github.com/jerhadf/linear-mcp-server" class="server-name" onclick="event.stopPropagation()">Linear MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-dplus">D+</div></td>
            <td class="r">68.8<span class="score-bar-bg"><span class="score-bar-fill" data-width="68.8" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">5</td>
            <td class="r">902</td>
            <td class="r">180</td>
            <td class="r"><span class="issues-badge issues-medium">5</span></td>
          </tr>
          <tr class="detail-row" data-server="linear">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="71" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">71</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="25" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">25</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/jerhadf/linear-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="linear"' in content:
        print("Linear MCP already in leaderboard. Exiting.")
        return

    # Insert before playwright (currently at rank #28 after prior insertions)
    playwright_row = '<tr class="data-row" data-server="playwright">'
    idx = content.find(playwright_row)
    if idx == -1:
        print("ERROR: Could not find Playwright entry")
        return

    content = content[:idx] + LINEAR_ROWS + '\n' + content[idx:]

    insert_end = idx + len(LINEAR_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 28:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 28:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Linear MCP at rank #28. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
