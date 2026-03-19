#!/usr/bin/env python3
"""
Script to add Notion MCP (awkoy) to the leaderboard at rank #3.

Grade data:
  - Score: 100.0/100 (A+)
  - Correctness: 100 (A+) — 0 warnings (all notion_ prefix, snake_case)
  - Efficiency: 100 (A+) — 40.4 avg tokens/tool, 202 total
  - Quality: 100 (A+) — 0 suggestions
  - Tools: 5 (combined operation tools for pages, blocks, database, comments, users)
  - Issues: 0 total
  - Stars: 148
  - Repo: https://github.com/awkoy/notion-mcp-server

Narrative: Minimal Notion MCP with perfect schema quality. 5 operation tools,
each wrapping a category of operations. Contrast: official Notion MCP gets F (19.8).
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

AWKOY_NOTION_ROWS = '''          <!-- #3 Notion MCP (awkoy) -->
          <tr class="data-row" data-server="awkoy-notion">
            <td class="rank-cell">3</td>
            <td>
              <a href="https://github.com/awkoy/notion-mcp-server" class="server-name" onclick="event.stopPropagation()">Notion MCP (awkoy)</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-aplus">A+</div></td>
            <td class="r">100.0<span class="score-bar-bg"><span class="score-bar-fill" data-width="100" style="background: var(--accent-cyan);"></span></span></td>
            <td class="r">5</td>
            <td class="r">202</td>
            <td class="r">40</td>
            <td class="r"><span class="issues-badge issues-none">0</span></td>
          </tr>
          <tr class="detail-row" data-server="awkoy-notion">
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
                  <a href="https://github.com/awkoy/notion-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="awkoy-notion"' in content:
        print("Awkoy Notion MCP already in leaderboard. Exiting.")
        return

    # Insert before danhilse-notion (currently at rank #2)
    danhilse_row = '<tr class="data-row" data-server="danhilse-notion">'
    idx = content.find(danhilse_row)
    if idx == -1:
        print("ERROR: Could not find Danhilse Notion entry")
        return

    content = content[:idx] + AWKOY_NOTION_ROWS + '\n' + content[idx:]

    insert_end = idx + len(AWKOY_NOTION_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 3:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    # Fix rank numbering after all insertions
    counter = [0]
    def renumber_all(m):
        counter[0] += 1
        return f'<td class="rank-cell">{counter[0]}</td>'
    content = re.sub(r'<td class="rank-cell">\d+</td>', renumber_all, content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Awkoy Notion MCP at rank #3. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
