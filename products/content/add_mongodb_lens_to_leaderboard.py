#!/usr/bin/env python3
"""
Script to add MongoDB Lens to the leaderboard.

Grade data:
  - Score: 60.0/100 (D-)
  - Correctness: 0 (F) — 41 warnings (ALL tools use hyphenated names)
  - Efficiency: 100 (A+) — 33.3 avg tokens/tool, 1,398 total
  - Quality: 100 (A+) — 0 suggestions (descriptions are concise and good)
  - Tools: 42
  - Issues: 41 total
  - Stars: 199
  - Repo: https://github.com/furey/mongodb-lens

Narrative: Comprehensive MongoDB MCP with 42 tools but ALL use hyphen naming
(connect-mongodb, list-databases). Perfect efficiency and quality — only naming kills it.
This is the SECOND MongoDB MCP on the leaderboard: mongodb-js/mongodb-mcp-server
(official, F 42.0) vs furey/mongodb-lens (community, D- 60.0). Both fail on naming.
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

MONGODB_LENS_ROWS = '''          <!-- MongoDB Lens (furey) -->
          <tr class="data-row" data-server="mongodb-lens">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/furey/mongodb-lens" class="server-name" onclick="event.stopPropagation()">MongoDB Lens</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-dminus">D-</div></td>
            <td class="r">60.0<span class="score-bar-bg"><span class="score-bar-fill" data-width="60.0" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">42</td>
            <td class="r">1,398</td>
            <td class="r">33</td>
            <td class="r"><span class="issues-badge issues-high">41</span></td>
          </tr>
          <tr class="detail-row" data-server="mongodb-lens">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/furey/mongodb-lens" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="mongodb-lens"' in content:
        print("MongoDB Lens already in leaderboard. Exiting.")
        return

    # Insert before magic-mcp (score 58.3, below mongodb-lens 60.0)
    magic_row = '<tr class="data-row" data-server="magic-mcp">'
    idx = content.find(magic_row)
    if idx == -1:
        print("ERROR: Could not find Magic MCP entry")
        return

    content = content[:idx] + MONGODB_LENS_ROWS + '\n' + content[idx:]

    insert_end = idx + len(MONGODB_LENS_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    # Fix all rank numbers sequentially
    counter = [0]
    def renumber_all(m):
        counter[0] += 1
        return f'<td class="rank-cell">{counter[0]}</td>'
    content = re.sub(r'<td class="rank-cell">\d+</td>', renumber_all, content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added MongoDB Lens. Total servers now renumbered.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
