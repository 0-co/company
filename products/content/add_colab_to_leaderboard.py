#!/usr/bin/env python3
"""
Script to add Google Colab MCP to the leaderboard at rank #4.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 97.6/100 (A+)
  - Correctness: 100 (A+)
  - Efficiency: 92 (A-)
  - Quality: 100 (A+)
  - Tools: 1
  - Tokens: 88
  - Stars: 222
  - Repo: https://github.com/googlecolab/colab-mcp
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

COLAB_ROWS = '''          <!-- #4 Google Colab -->
          <tr class="data-row" data-server="colab">
            <td class="rank-cell">4</td>
            <td>
              <a href="https://github.com/googlecolab/colab-mcp" class="server-name" onclick="event.stopPropagation()">Google Colab MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-aplus">A+</div></td>
            <td class="r">97.6<span class="score-bar-bg"><span class="score-bar-fill" data-width="97.6" style="background: var(--accent-cyan);"></span></span></td>
            <td class="r">1</td>
            <td class="r">88</td>
            <td class="r">88</td>
            <td class="r"><span class="issues-badge issues-low">0</span></td>
          </tr>
          <tr class="detail-row" data-server="colab">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="92" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">92</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-violet);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-violet);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/googlecolab/colab-mcp" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''

def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    # Check if Colab is already there
    if 'data-server="colab"' in content:
        print("Colab already in leaderboard. Exiting.")
        return

    # Find the position of rank #4 (Slack) comment
    slack_comment = '<!-- #4 Slack -->'
    idx = content.find(slack_comment)
    if idx == -1:
        print(f"ERROR: Could not find '{slack_comment}'")
        return

    # Insert Colab before Slack
    content = content[:idx] + COLAB_ROWS + '\n' + content[idx:]

    # Now renumber all ranks from 4 onwards (old #4 Slack → #5, etc.)
    # The Slack row now has rank-cell 4 (old) — update to 5
    # Strategy: find all rank-cell values >= 4 and increment by 1
    # But only AFTER our new Colab entry

    # Split at the Slack comment position
    colab_end = idx + len(COLAB_ROWS) + 1  # +1 for newline
    before = content[:colab_end]  # Contains Colab + everything before
    after = content[colab_end:]   # Contains Slack and everything after

    # In 'after', increment all rank-cell values >= 4
    def increment_rank(m):
        rank = int(m.group(1))
        return f'<td class="rank-cell">{rank + 1}</td>'

    # Increment rank cells in 'after' section that are >= 4
    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 4:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    # Also update the HTML comments <!-- #N Name -->
    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 4:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update the server count in header (if it says "50 MCP servers")
    content = re.sub(r'(\d+) MCP servers graded', lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content, count=1)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Google Colab MCP at rank #4. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")

if __name__ == '__main__':
    main()
