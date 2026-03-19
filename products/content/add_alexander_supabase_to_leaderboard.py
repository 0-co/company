#!/usr/bin/env python3
"""
Script to add Supabase MCP (alexander-zuev) to the leaderboard at rank #50.
This is a DIFFERENT server from supabase-community/supabase-mcp (already at rank #33).

Grade data:
  - Score: 48.4/100 (F)
  - Correctness: 100 (A+) — 0 warnings (all snake_case names)
  - Efficiency: 28 (F) — 375.3 avg tokens/tool, 5,254 total (BLOATED descriptions)
  - Quality: 0 (F) — 13 suggestions (extremely long multi-paragraph descriptions)
  - Tools: 14
  - Issues: 13 total
  - Stars: 815
  - Repo: https://github.com/alexander-zuev/supabase-mcp-server

Narrative: Community Supabase MCP with verbose YAML descriptions (avg 375 tokens/tool).
Official Supabase MCP scores D (63.5) — this gets F (48.4) due to bloated docs.
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

ALEXANDER_SUPABASE_ROWS = '''          <!-- #50 Supabase MCP (alexander-zuev) -->
          <tr class="data-row" data-server="alexander-supabase">
            <td class="rank-cell">50</td>
            <td>
              <a href="https://github.com/alexander-zuev/supabase-mcp-server" class="server-name" onclick="event.stopPropagation()">Supabase MCP (alexander-zuev)</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">48.4<span class="score-bar-bg"><span class="score-bar-fill" data-width="48.4" style="background: var(--accent-red);"></span></span></td>
            <td class="r">14</td>
            <td class="r">5,254</td>
            <td class="r">375</td>
            <td class="r"><span class="issues-badge issues-high">13</span></td>
          </tr>
          <tr class="detail-row" data-server="alexander-supabase">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="28" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">28</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/alexander-zuev/supabase-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="alexander-supabase"' in content:
        print("Alexander-zuev Supabase MCP already in leaderboard. Exiting.")
        return

    # Insert before tavily (currently at rank #50 after prior insertions)
    tavily_row = '<tr class="data-row" data-server="tavily">'
    idx = content.find(tavily_row)
    if idx == -1:
        print("ERROR: Could not find Tavily entry")
        return

    content = content[:idx] + ALEXANDER_SUPABASE_ROWS + '\n' + content[idx:]

    insert_end = idx + len(ALEXANDER_SUPABASE_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 50:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 50:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Alexander-zuev Supabase MCP at rank #50. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
