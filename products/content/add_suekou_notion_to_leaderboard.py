#!/usr/bin/env python3
"""
Script to add suekou/mcp-notion-server to the leaderboard at rank #53.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 36.4/100 (F)
  - Correctness: 40 (F) — 6 warnings (undefined nested object properties)
  - Efficiency: 68 (D+) — 193.4 avg tokens/tool, 3,482 total
  - Quality: 0 (F) — 36 suggestions (formatParameter duplicated 18x, long descriptions)
  - Tools: 18
  - Issues: 42 total
  - Stars: 869
  - Repo: https://github.com/suekou/mcp-notion-server

Narrative: Community Notion MCP gets F (36.4) vs Official Notion MCP F (19.8).
Both fail, but community version scores nearly 2x better.
The formatParameter pattern (same 205-char description on every tool) kills quality score.
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

SUEKOU_NOTION_ROWS = '''          <!-- #53 Notion MCP (suekou) -->
          <tr class="data-row" data-server="suekou-notion">
            <td class="rank-cell">53</td>
            <td>
              <a href="https://github.com/suekou/mcp-notion-server" class="server-name" onclick="event.stopPropagation()">Notion MCP (suekou)</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">36.4<span class="score-bar-bg"><span class="score-bar-fill" data-width="36.4" style="background: var(--accent-red);"></span></span></td>
            <td class="r">18</td>
            <td class="r">3,482</td>
            <td class="r">193</td>
            <td class="r"><span class="issues-badge issues-high">42</span></td>
          </tr>
          <tr class="detail-row" data-server="suekou-notion">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="40" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">40</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="68" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">68</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/suekou/mcp-notion-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="suekou-notion"' in content:
        print("Suekou Notion already in leaderboard. Exiting.")
        return

    # Insert before firecrawl (currently at rank #53)
    firecrawl_row = '<tr class="data-row" data-server="firecrawl">'
    idx = content.find(firecrawl_row)
    if idx == -1:
        print("ERROR: Could not find Firecrawl entry")
        return

    content = content[:idx] + SUEKOU_NOTION_ROWS + '\n' + content[idx:]

    insert_end = idx + len(SUEKOU_NOTION_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 53:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 53:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update all meta description counts
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added suekou Notion MCP at rank #53. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
