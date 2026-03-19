#!/usr/bin/env python3
"""
Script to add MiniMax MCP to the leaderboard at rank #41.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 52.6/100 (F)
  - Correctness: 100 (A+) — 0 warnings
  - Efficiency: 42 (F) — 310.8 avg tokens/tool, 2,797 total (BLOATED)
  - Quality: 0 (F) — 25 suggestions (COST WARNINGs in descriptions)
  - Tools: 9 (TTS, video, image, music, voice tools)
  - Issues: 25 quality suggestions
  - Stars: 1,316
  - Repo: https://github.com/MiniMax-AI/MiniMax-MCP
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

MINIMAX_ROWS = '''          <!-- #41 MiniMax MCP -->
          <tr class="data-row" data-server="minimax">
            <td class="rank-cell">41</td>
            <td>
              <a href="https://github.com/MiniMax-AI/MiniMax-MCP" class="server-name" onclick="event.stopPropagation()">MiniMax MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">52.6<span class="score-bar-bg"><span class="score-bar-fill" data-width="52.6" style="background: var(--accent-red);"></span></span></td>
            <td class="r">9</td>
            <td class="r">2,797</td>
            <td class="r">311</td>
            <td class="r"><span class="issues-badge issues-high">25</span></td>
          </tr>
          <tr class="detail-row" data-server="minimax">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="42" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">42</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/MiniMax-AI/MiniMax-MCP" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="minimax"' in content:
        print("MiniMax already in leaderboard. Exiting.")
        return

    # Insert before AWS (currently at rank #41)
    aws_row = '<tr class="data-row" data-server="aws">'
    idx = content.find(aws_row)
    if idx == -1:
        print("ERROR: Could not find AWS entry")
        return

    content = content[:idx] + MINIMAX_ROWS + '\n' + content[idx:]

    insert_end = idx + len(MINIMAX_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 41:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 41:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update all meta description counts
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added MiniMax MCP at rank #41. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
