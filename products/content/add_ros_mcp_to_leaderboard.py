#!/usr/bin/env python3
"""
Script to add ROS MCP Server to the leaderboard at rank #3.
Run AFTER add_danhilse_notion_to_leaderboard.py.

Grade data:
  - Score: 99.7/100 (A+)
  - Correctness: 100 (A+) — 0 warnings
  - Efficiency: 99 (A+) — 53.7 avg tokens/tool, 1,556 total
  - Quality: 100 (A+) — 0 suggestions
  - Tools: 29
  - Issues: 0 total
  - Stars: 1,088
  - Repo: https://github.com/robotmcp/ros-mcp-server

Narrative: ROS MCP joins the elite top 3 with near-perfect score.
29 tools for robotics control (topics, nodes, services, parameters, actions).
Excellent token efficiency despite many tools.
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

ROS_ROWS = '''          <!-- #3 ROS MCP Server -->
          <tr class="data-row" data-server="ros-mcp">
            <td class="rank-cell">3</td>
            <td>
              <a href="https://github.com/robotmcp/ros-mcp-server" class="server-name" onclick="event.stopPropagation()">ROS MCP Server</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-aplus">A+</div></td>
            <td class="r">99.7<span class="score-bar-bg"><span class="score-bar-fill" data-width="99.7" style="background: var(--accent-cyan);"></span></span></td>
            <td class="r">29</td>
            <td class="r">1,556</td>
            <td class="r">54</td>
            <td class="r"><span class="issues-badge issues-none">0</span></td>
          </tr>
          <tr class="detail-row" data-server="ros-mcp">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="99" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">99</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/robotmcp/ros-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    if 'data-server="ros-mcp"' in content:
        print("ROS MCP already in leaderboard. Exiting.")
        return

    # Insert before sqlite (now at rank #3 after danhilse-notion insertion)
    sqlite_row = '<tr class="data-row" data-server="sqlite">'
    idx = content.find(sqlite_row)
    if idx == -1:
        print("ERROR: Could not find SQLite entry")
        return

    content = content[:idx] + ROS_ROWS + '\n' + content[idx:]

    insert_end = idx + len(ROS_ROWS) + 1
    before = content[:insert_end]
    after = content[insert_end:]

    def maybe_increment(m):
        rank = int(m.group(1))
        if rank >= 3:
            return f'<td class="rank-cell">{rank + 1}</td>'
        return m.group(0)

    after = re.sub(r'<td class="rank-cell">(\d+)</td>', maybe_increment, after)

    def maybe_increment_comment(m):
        rank = int(m.group(1))
        name = m.group(2)
        if rank >= 3:
            return f'<!-- #{rank + 1} {name}-->'
        return m.group(0)

    after = re.sub(r'<!-- #(\d+) ([^-]+)-->', maybe_increment_comment, after)

    content = before + after

    content = re.sub(r'(\d+) MCP servers graded',
                     lambda m: f'{int(m.group(1)) + 1} MCP servers graded', content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added ROS MCP at rank #3. Renumbered all subsequent ranks.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
