#!/usr/bin/env python3
"""
Script to add WinDbg MCP to the leaderboard at rank #4.

Grade data:
  - Score: 99.1/100 (A+)
  - Correctness: 100 (A+) — 0 warnings (all snake_case, clean naming)
  - Efficiency: 97 (A+) — 63.1 avg tokens/tool, 442 total
  - Quality: 100 (A+) — 0 suggestions
  - Tools: 7
  - Issues: 0 total
  - Stars: 1,119
  - Repo: https://github.com/svnscha/mcp-windbg

Narrative: WinDbg MCP joins the elite top 5 with a near-perfect score.
Concise descriptions, clean naming, perfect schema quality.
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

WINDBG_ROWS = '''          <!-- #4 WinDbg MCP -->
          <tr class="data-row" data-server="windbg">
            <td class="rank-cell">4</td>
            <td>
              <a href="https://github.com/svnscha/mcp-windbg" class="server-name" onclick="event.stopPropagation()">WinDbg MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-aplus">A+</div></td>
            <td class="r">99.1<span class="score-bar-bg"><span class="score-bar-fill" data-width="99.1" style="background: var(--accent-cyan);"></span></span></td>
            <td class="r">7</td>
            <td class="r">442</td>
            <td class="r">63</td>
            <td class="r"><span class="issues-badge issues-none">0</span></td>
          </tr>
          <tr class="detail-row" data-server="windbg">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="97" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">97</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/svnscha/mcp-windbg" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="windbg"' in content:
        print("WinDbg MCP already in leaderboard. Exiting.")
        return

    # Insert before colab (currently at rank #4)
    colab_row = '<tr class="data-row" data-server="colab">'
    idx = content.find(colab_row)
    if idx == -1:
        print("ERROR: Could not find Colab entry")
        return

    content = content[:idx] + WINDBG_ROWS + '\n' + content[idx:]

    insert_end = idx + len(WINDBG_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 4:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 4:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added WinDbg MCP at rank #4. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
