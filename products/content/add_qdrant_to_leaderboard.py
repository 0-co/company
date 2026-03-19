#!/usr/bin/env python3
"""
Script to add Qdrant MCP to the leaderboard at rank #20.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 78.9/100 (C+)
  - Correctness: 60 (D-)
  - Efficiency: 83 (B)
  - Quality: 100 (A+)
  - Tools: 2
  - Tokens: 257 total / 128.5 avg
  - Issues: 4 (hyphenated names + undefined object properties)
  - Stars: 1,287
  - Repo: https://github.com/qdrant/mcp-server-qdrant
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

QDRANT_ROWS = '''          <!-- #20 Qdrant MCP -->
          <tr class="data-row" data-server="qdrant">
            <td class="rank-cell">20</td>
            <td>
              <a href="https://github.com/qdrant/mcp-server-qdrant" class="server-name" onclick="event.stopPropagation()">Qdrant MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-cplus">C+</div></td>
            <td class="r">78.9<span class="score-bar-bg"><span class="score-bar-fill" data-width="78.9" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">2</td>
            <td class="r">257</td>
            <td class="r">129</td>
            <td class="r"><span class="issues-badge issues-medium">4</span></td>
          </tr>
          <tr class="detail-row" data-server="qdrant">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="60" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">60</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="83" style="background: var(--accent-green);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-green);">83</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/qdrant/mcp-server-qdrant" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="qdrant"' in content:
        print("Qdrant already in leaderboard. Exiting.")
        return

    # Insert before Memory MCP Server (currently at rank #20)
    memory_row = '<tr class="data-row" data-server="memory">'
    idx = content.find(memory_row)
    if idx == -1:
        print("ERROR: Could not find Memory MCP Server entry")
        return

    content = content[:idx] + QDRANT_ROWS + '\n' + content[idx:]

    supabase_end = idx + len(QDRANT_ROWS) + 1
    before = content[:supabase_end]
    after = content[supabase_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 20:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 20:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update both meta description counts
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Qdrant MCP at rank #20. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
