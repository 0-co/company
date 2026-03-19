#!/usr/bin/env python3
"""
Script to add Web Eval Agent to the leaderboard at rank #30.
Run AFTER add_linkedin_mcp_to_leaderboard.py (which shifts filesystem to rank #30).

Grade data:
  - Score: 66.1/100 (D)
  - Correctness: 100 (A+) — 0 warnings (snake_case names)
  - Efficiency: 62 (D-) — 220.5 avg tokens/tool, 441 total (verbose descriptions)
  - Quality: 25 (F) — 5 suggestions (multi-paragraph tool descriptions, long param descriptions)
  - Tools: 2
  - Issues: 5 total
  - Stars: 1,236
  - Repo: https://github.com/refreshdotdev/web-eval-agent
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

WEB_EVAL_ROWS = '''          <!-- #30 Web Eval Agent -->
          <tr class="data-row" data-server="web-eval-agent">
            <td class="rank-cell">30</td>
            <td>
              <a href="https://github.com/refreshdotdev/web-eval-agent" class="server-name" onclick="event.stopPropagation()">Web Eval Agent</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-d">D</div></td>
            <td class="r">66.1<span class="score-bar-bg"><span class="score-bar-fill" data-width="66.1" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">2</td>
            <td class="r">441</td>
            <td class="r">221</td>
            <td class="r"><span class="issues-badge issues-medium">5</span></td>
          </tr>
          <tr class="detail-row" data-server="web-eval-agent">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="62" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">62</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="25" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">25</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/refreshdotdev/web-eval-agent" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="web-eval-agent"' in content:
        print("Web Eval Agent already in leaderboard. Exiting.")
        return

    # Insert before filesystem (currently at rank #30 after LinkedIn insertion)
    filesystem_row = '<tr class="data-row" data-server="filesystem">'
    idx = content.find(filesystem_row)
    if idx == -1:
        print("ERROR: Could not find Filesystem entry")
        return

    content = content[:idx] + WEB_EVAL_ROWS + '\n' + content[idx:]

    insert_end = idx + len(WEB_EVAL_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 30:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 30:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Web Eval Agent at rank #30. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
