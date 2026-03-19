#!/usr/bin/env python3
"""
Script to add Supabase MCP to the leaderboard at rank #31.
Run after feature freeze lifts (16:10 UTC March 19).

Grade data:
  - Score: 63.5/100 (D)
  - Correctness: 80 (B-)
  - Efficiency: 95 (A)
  - Quality: 10 (F)
  - Tools: 32
  - Tokens: 2,330 total / 73 avg
  - Issues: 8 (2 warnings + 6 suggestions)
  - Stars: 2,541
  - Repo: https://github.com/supabase-community/supabase-mcp
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

SUPABASE_ROWS = '''          <!-- #31 Supabase MCP -->
          <tr class="data-row" data-server="supabase">
            <td class="rank-cell">31</td>
            <td>
              <a href="https://github.com/supabase-community/supabase-mcp" class="server-name" onclick="event.stopPropagation()">Supabase MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-d">D</div></td>
            <td class="r">63.5<span class="score-bar-bg"><span class="score-bar-fill" data-width="63.5" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">32</td>
            <td class="r">2,330</td>
            <td class="r">73</td>
            <td class="r"><span class="issues-badge issues-medium">8</span></td>
          </tr>
          <tr class="detail-row" data-server="supabase">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="80" style="background: var(--accent-green);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-green);">80</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="95" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">95</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="10" style="background: var(--accent-violet);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-violet);">10</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/supabase-community/supabase-mcp" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    # Check if Supabase is already there
    if 'data-server="supabase"' in content:
        print("Supabase already in leaderboard. Exiting.")
        return

    # Find the position of rank #31 (Stripe) comment
    stripe_comment = '<!-- #31 Stripe'
    idx = content.find(stripe_comment)
    if idx == -1:
        # Try finding the Stripe data-server row directly
        stripe_row = '<tr class="data-row" data-server="stripe">'
        idx = content.find(stripe_row)
        if idx == -1:
            print(f"ERROR: Could not find Stripe entry")
            return

    # Insert Supabase before Stripe
    content = content[:idx] + SUPABASE_ROWS + '\n' + content[idx:]

    # Now renumber all ranks from 31 onwards (old #31 Stripe → #32, etc.)
    supabase_end = idx + len(SUPABASE_ROWS) + 1
    before = content[:supabase_end]
    after = content[supabase_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 31:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 31:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    # Update the server count in header
    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content, count=1)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added Supabase MCP at rank #31. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
