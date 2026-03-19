#!/usr/bin/env python3
"""
Script to add Microsoft Azure DevOps MCP to the leaderboard at rank #37.

Grade data:
  - Score: 61.9/100 (D-)
  - Correctness: 100 (A+) — 0 warnings (all snake_case names, clean naming)
  - Efficiency: 73 (C) — 170.4 avg tokens/tool, 14,657 total
  - Quality: 0 (F) — 57 suggestions (16 long tool descriptions, 43 long param descriptions)
  - Tools: 86 (most tools on the leaderboard)
  - Issues: 57 total
  - Stars: 1,428
  - Repo: https://github.com/microsoft/azure-devops-mcp

Narrative: Microsoft's official Azure DevOps MCP has the most tools (86) on the leaderboard.
Perfect naming (A+) but verbose descriptions tank quality to F.
"project" param alone is 145 chars.
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

AZURE_DEVOPS_ROWS = '''          <!-- #37 Azure DevOps MCP -->
          <tr class="data-row" data-server="azure-devops">
            <td class="rank-cell">37</td>
            <td>
              <a href="https://github.com/microsoft/azure-devops-mcp" class="server-name" onclick="event.stopPropagation()">Azure DevOps MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-dminus">D-</div></td>
            <td class="r">61.9<span class="score-bar-bg"><span class="score-bar-fill" data-width="61.9" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">86</td>
            <td class="r">14,657</td>
            <td class="r">170</td>
            <td class="r"><span class="issues-badge issues-high">57</span></td>
          </tr>
          <tr class="detail-row" data-server="azure-devops">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="73" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">73</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/microsoft/azure-devops-mcp" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="azure-devops"' in content:
        print("Azure DevOps already in leaderboard. Exiting.")
        return

    # Insert before chart (currently at rank #37)
    chart_row = '<tr class="data-row" data-server="chart">'
    idx = content.find(chart_row)
    if idx == -1:
        print("ERROR: Could not find Chart entry")
        return

    content = content[:idx] + AZURE_DEVOPS_ROWS + '\n' + content[idx:]

    insert_end = idx + len(AZURE_DEVOPS_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 37:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 37:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update all meta description counts
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Azure DevOps MCP at rank #37. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
