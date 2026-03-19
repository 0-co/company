#!/usr/bin/env python3
"""
Script to add MongoDB MCP to the leaderboard at rank #48.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 42.0/100 (F)
  - Correctness: 0 (F) — 40 warnings, all from hyphenated tool names
  - Efficiency: 100 (A+) — 45.1 avg tokens/tool, 2,076 total
  - Quality: 40 (F) — 4 suggestions
  - Tools: 46 (23 DB + 15 Atlas + 4 Atlas Local + 2 Assistant + missing export=1?)
  - Issues: 44 total
  - Stars: 965
  - Repo: https://github.com/mongodb-js/mongodb-mcp-server
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

MONGODB_ROWS = '''          <!-- #48 MongoDB MCP -->
          <tr class="data-row" data-server="mongodb">
            <td class="rank-cell">48</td>
            <td>
              <a href="https://github.com/mongodb-js/mongodb-mcp-server" class="server-name" onclick="event.stopPropagation()">MongoDB MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">42.0<span class="score-bar-bg"><span class="score-bar-fill" data-width="42.0" style="background: var(--accent-red);"></span></span></td>
            <td class="r">46</td>
            <td class="r">2,076</td>
            <td class="r">45</td>
            <td class="r"><span class="issues-badge issues-high">44</span></td>
          </tr>
          <tr class="detail-row" data-server="mongodb">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="40" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">40</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/mongodb-js/mongodb-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="mongodb"' in content:
        print("MongoDB already in leaderboard. Exiting.")
        return

    # Insert before GA4 (currently at rank #48)
    ga4_row = '<tr class="data-row" data-server="ga4">'
    idx = content.find(ga4_row)
    if idx == -1:
        print("ERROR: Could not find GA4 entry")
        return

    content = content[:idx] + MONGODB_ROWS + '\n' + content[idx:]

    insert_end = idx + len(MONGODB_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 48:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 48:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update all meta description counts
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added MongoDB MCP at rank #48. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
