#!/usr/bin/env python3
"""
Script to add 6 new MCP servers to the leaderboard.

Servers (by score desc):
  - mcp-youtube (anaisbetts): A+ 97.3 — 1 tool, 505★
  - neon (neondatabase): D 63.7 — 29 tools, 564★
  - terraform (hashicorp): F 59.5 — 9 tools, 1,279★
  - kubernetes (Flux159): F 45.9 — 22 tools, 1,356★
  - apify (apify): F 32.7 — 12 tools, 919★
  - docker (ckreiling): F 27.0 — 19 tools, 688★

Total: 69 → 75 servers
"""
import re

LEADERBOARD_PATH = '/home/agent/company/docs/leaderboard.html'

YOUTUBE_ROWS = '''          <!-- mcp-youtube (anaisbetts) -->
          <tr class="data-row" data-server="mcp-youtube">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/anaisbetts/mcp-youtube" class="server-name" onclick="event.stopPropagation()">mcp-youtube</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-aplus">A+</div></td>
            <td class="r">97.3<span class="score-bar-bg"><span class="score-bar-fill" data-width="97.3" style="background: var(--accent-cyan);"></span></span></td>
            <td class="r">1</td>
            <td class="r">91</td>
            <td class="r">91</td>
            <td class="r"><span class="issues-badge issues-none">0</span></td>
          </tr>
          <tr class="detail-row" data-server="mcp-youtube">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="91" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">91</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="100" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">100</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/anaisbetts/mcp-youtube" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''

NEON_ROWS = '''          <!-- Neon MCP (neondatabase) -->
          <tr class="data-row" data-server="neon">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/neondatabase/mcp-server-neon" class="server-name" onclick="event.stopPropagation()">Neon MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-d">D</div></td>
            <td class="r">63.7<span class="score-bar-bg"><span class="score-bar-fill" data-width="63.7" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">29</td>
            <td class="r">4,192</td>
            <td class="r">144</td>
            <td class="r"><span class="issues-badge issues-high">18</span></td>
          </tr>
          <tr class="detail-row" data-server="neon">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="79" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">79</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/neondatabase/mcp-server-neon" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''

TERRAFORM_ROWS = '''          <!-- Terraform MCP (hashicorp) -->
          <tr class="data-row" data-server="terraform">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/hashicorp/terraform-mcp-server" class="server-name" onclick="event.stopPropagation()">Terraform MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">59.5<span class="score-bar-bg"><span class="score-bar-fill" data-width="59.5" style="background: var(--accent-gold);"></span></span></td>
            <td class="r">9</td>
            <td class="r">1,878</td>
            <td class="r">208</td>
            <td class="r"><span class="issues-badge issues-high">15</span></td>
          </tr>
          <tr class="detail-row" data-server="terraform">
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
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="65" style="background: var(--accent-gold);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-gold);">65</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/hashicorp/terraform-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''

KUBERNETES_ROWS = '''          <!-- Kubernetes MCP (Flux159) -->
          <tr class="data-row" data-server="kubernetes">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/Flux159/mcp-server-kubernetes" class="server-name" onclick="event.stopPropagation()">Kubernetes MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">45.9<span class="score-bar-bg"><span class="score-bar-fill" data-width="45.9" style="background: var(--accent-red);"></span></span></td>
            <td class="r">22</td>
            <td class="r">3,760</td>
            <td class="r">170</td>
            <td class="r"><span class="issues-badge issues-high">13</span></td>
          </tr>
          <tr class="detail-row" data-server="kubernetes">
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
                  <a href="https://github.com/Flux159/mcp-server-kubernetes" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''

APIFY_ROWS = '''          <!-- Apify Actors MCP -->
          <tr class="data-row" data-server="apify">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/apify/actors-mcp-server" class="server-name" onclick="event.stopPropagation()">Apify Actors MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">32.7<span class="score-bar-bg"><span class="score-bar-fill" data-width="32.7" style="background: var(--accent-red);"></span></span></td>
            <td class="r">12</td>
            <td class="r">1,483</td>
            <td class="r">123</td>
            <td class="r"><span class="issues-badge issues-high">19</span></td>
          </tr>
          <tr class="detail-row" data-server="apify">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="84" style="background: var(--accent-green);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-green);">84</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="25" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">25</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/apify/actors-mcp-server" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''

DOCKER_ROWS = '''          <!-- Docker MCP (ckreiling) -->
          <tr class="data-row" data-server="docker-mcp">
            <td class="rank-cell">99</td>
            <td>
              <a href="https://github.com/ckreiling/mcp-server-docker" class="server-name" onclick="event.stopPropagation()">Docker MCP</a>
              <span class="expand-hint">&#9662;</span>
            </td>
            <td class="grade-cell"><div class="grade-badge grade-f">F</div></td>
            <td class="r">27.0<span class="score-bar-bg"><span class="score-bar-fill" data-width="27.0" style="background: var(--accent-red);"></span></span></td>
            <td class="r">19</td>
            <td class="r">1,828</td>
            <td class="r">96</td>
            <td class="r"><span class="issues-badge issues-high">24</span></td>
          </tr>
          <tr class="detail-row" data-server="docker-mcp">
            <td colspan="8" class="detail-cell">
              <div class="detail-inner">
                <div class="breakdown-section">
                  <div class="breakdown-title">Grade Breakdown</div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Correctness (40%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Efficiency (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="90" style="background: var(--accent-cyan);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-cyan);">90</span>
                  </div>
                  <div class="breakdown-item">
                    <span class="breakdown-label">Quality (30%)</span>
                    <div class="breakdown-bar-bg"><div class="breakdown-bar-fill" data-width="0" style="background: var(--accent-red);"></div></div>
                    <span class="breakdown-score" style="color: var(--accent-red);">0</span>
                  </div>
                </div>
                <div class="detail-actions">
                  <a href="report.html" class="detail-btn detail-btn-primary">Grade your own server</a>
                  <a href="https://github.com/ckreiling/mcp-server-docker" class="detail-btn detail-btn-secondary">View on GitHub</a>
                </div>
              </div>
            </td>
          </tr>
'''


def main():
    with open(LEADERBOARD_PATH) as f:
        content = f.read()

    # Check if already added
    new_servers = ['mcp-youtube', 'neon', 'terraform', 'kubernetes', 'apify', 'docker-mcp']
    already_added = [s for s in new_servers if f'data-server="{s}"' in content]
    if already_added:
        print(f"Already in leaderboard: {already_added}. Exiting.")
        return

    # Insert all 6 servers at correct positions (bottom-first to avoid anchor shifting)
    # 1. Docker (27.0) → before grafana (21.9)
    grafana_row = '<tr class="data-row" data-server="grafana">'
    idx = content.find(grafana_row)
    if idx == -1:
        print("ERROR: Could not find grafana entry")
        return
    content = content[:idx] + DOCKER_ROWS + '\n' + content[idx:]

    # 2. Apify (32.7) → before desktop-commander (30.8)
    dc_row = '<tr class="data-row" data-server="desktop-commander">'
    idx = content.find(dc_row)
    if idx == -1:
        print("ERROR: Could not find desktop-commander entry")
        return
    content = content[:idx] + APIFY_ROWS + '\n' + content[idx:]

    # 3. Kubernetes (45.9) → before mcp-chrome (44.9)
    chrome_row = '<tr class="data-row" data-server="mcp-chrome">'
    idx = content.find(chrome_row)
    if idx == -1:
        print("ERROR: Could not find mcp-chrome entry")
        return
    content = content[:idx] + KUBERNETES_ROWS + '\n' + content[idx:]

    # 4. Terraform (59.5) → before magic-mcp (58.3)
    magic_row = '<tr class="data-row" data-server="magic-mcp">'
    idx = content.find(magic_row)
    if idx == -1:
        print("ERROR: Could not find magic-mcp entry")
        return
    content = content[:idx] + TERRAFORM_ROWS + '\n' + content[idx:]

    # 5. Neon (63.7) → before supabase (63.5)
    supabase_row = '<tr class="data-row" data-server="supabase">'
    idx = content.find(supabase_row)
    if idx == -1:
        print("ERROR: Could not find supabase entry")
        return
    content = content[:idx] + NEON_ROWS + '\n' + content[idx:]

    # 6. YouTube (97.3) → before shadcn (93.4) - after slack (97.3)
    shadcn_row = '<tr class="data-row" data-server="shadcn">'
    idx = content.find(shadcn_row)
    if idx == -1:
        print("ERROR: Could not find shadcn entry")
        return
    content = content[:idx] + YOUTUBE_ROWS + '\n' + content[idx:]

    # Update server count (6 new servers)
    def increment_by_6(m):
        return f'{int(m.group(1)) + 6} MCP servers graded'
    content = re.sub(r'(\d+) MCP servers graded', increment_by_6, content)

    # Global renumber all rank cells
    counter = [0]
    def renumber_all(m):
        counter[0] += 1
        return f'<td class="rank-cell">{counter[0]}</td>'
    content = re.sub(r'<td class="rank-cell">\d+</td>', renumber_all, content)

    with open(LEADERBOARD_PATH, 'w') as f:
        f.write(content)

    print(f"Done! Added 6 servers. Total: {counter[0]} servers.")
    print("Now deploy with: sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company")


if __name__ == '__main__':
    main()
