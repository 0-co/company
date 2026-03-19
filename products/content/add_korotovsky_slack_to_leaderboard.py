#!/usr/bin/env python3
"""
Script to add korotovsky/slack-mcp-server to the leaderboard at rank #13.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 81.1/100 (B-)
  - Correctness: 100 (A+) — 0 warnings
  - Efficiency: 82 (B-) — 132.4 avg tokens/tool, 2,118 total
  - Quality: 55 (F) — 3 suggestions
  - Tools: 16
  - Issues: 3
  - Stars: 1,461
  - Repo: https://github.com/korotovsky/slack-mcp-server
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

KOROTOVSKY_SLACK_ROWS = '''          <!-- #13 Slack MCP (korotovsky) -->
          <tr class="data-row" data-server="korotovsky-slack">
            <td class="rank-cell">13</td>
            <td>
              <a href="https://github.com/korotovsky/slack-mcp-server" class="server-name" onclick="event.stopPropagation()">Slack MCP (korotovsky)</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-bminus">B-</div></td>
            <td class="r">81.1<span class="score-bar-bg"><span class="score-bar-fill" data-width="81.1" style="background: var(--accent-green);"></span></span></td>
            <td class="r">16</td>
            <td class="r">2,118</td>
            <td class="r">132</td>
            <td class="r"><span class="issues-badge issues-low">3</span></td>
          </tr>
          <tr class="detail-row" data-server="korotovsky-slack">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="82" style="background: var(--accent-green);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-green);">82</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="55" style="background: var(--accent-violet);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-violet);">55</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/korotovsky/slack-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="korotovsky-slack"' in content:
        print("Korotovsky Slack already in leaderboard. Exiting.")
        return

    # Insert before time (currently at rank #13)
    time_row = '<tr class="data-row" data-server="time">'
    idx = content.find(time_row)
    if idx == -1:
        print("ERROR: Could not find Time MCP entry")
        return

    content = content[:idx] + KOROTOVSKY_SLACK_ROWS + '\n' + content[idx:]

    insert_end = idx + len(KOROTOVSKY_SLACK_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 13:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 13:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update all meta description counts
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Korotovsky Slack MCP at rank #13. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
