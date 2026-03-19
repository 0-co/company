#!/usr/bin/env python3
"""
Script to add chunkhound to the leaderboard at rank #26.
Run AFTER add_windbg_to_leaderboard.py (which shifts everything from rank 4 down).

Grade data:
  - Score: 76.3/100 (C)
  - Correctness: 100 (A+) — 0 warnings (snake_case names)
  - Efficiency: 51 (F) — 269.5 avg tokens/tool, 539 total (very long descriptions)
  - Quality: 70 (C-) — 2 suggestions
  - Tools: 2
  - Issues: 2 total
  - Stars: 1,139
  - Repo: https://github.com/chunkhound/chunkhound
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

CHUNKHOUND_ROWS = '''          <!-- #26 chunkhound -->
          <tr class="data-row" data-server="chunkhound">
            <td class="rank-cell">26</td>
            <td>
              <a href="https://github.com/chunkhound/chunkhound" class="server-name" onclick="event.stopPropagation()">chunkhound</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-c">C</div></td>
            <td class="r">76.3<span class="score-bar-bg"><span class="score-bar-fill" data-width="76.3" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">2</td>
            <td class="r">539</td>
            <td class="r">270</td>
            <td class="r"><span class="issues-badge issues-low">2</span></td>
          </tr>
          <tr class="detail-row" data-server="chunkhound">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="51" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">51</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="70" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">70</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/chunkhound/chunkhound" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="chunkhound"' in content:
        print("chunkhound already in leaderboard. Exiting.")
        return

    # Insert before fetch (currently at rank #26 after windbg insertion)
    fetch_row = '<tr class="data-row" data-server="fetch">'
    idx = content.find(fetch_row)
    if idx == -1:
        print("ERROR: Could not find Fetch entry")
        return

    content = content[:idx] + CHUNKHOUND_ROWS + '\n' + content[idx:]

    insert_end = idx + len(CHUNKHOUND_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 26:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 26:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added chunkhound at rank #26. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
