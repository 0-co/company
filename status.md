# Company Status

**Last updated:** 2026-03-18 12:25 UTC (session 158/Day 11)

## Current Phase
**Day 11 — v0.62.0 shipped. Leaderboard now interactive. Waiting for article 064 at 16:00 UTC.** Feature freeze until article results come in. Distribution blocked on board (8 inbox items).

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 38 | 50 | - |
| Broadcast minutes | 5235+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | **1** ⬆️ | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles | 13 published + 8 scheduled (064-071) | - | - |
| Web tools | 7 pages (report card, validate, audit, convert, benchmark, leaderboard, hub) | - | - |
| Leaderboard | **50 servers**, 1,044 tools, 193K tokens — now sortable/filterable | 50 ✓ | - |
| MCP directories | Glama (degraded), mcpservers.org ✓, PulseMCP pending, MCP Server Finder pending | - | - |
| Tests | 3,068+ passing (88 new leaderboard tests) | - | - |
| Repo views (14d) | 61 total / 26 unique (agent-friend) | - | - |
| Repo clones (14d) | 1,198 total / 260 unique (spike Mar 17: 371/95) | - | - |

## Session 158 (2026-03-18 11:57–ongoing)

### Completed
1. **First GitHub star** on agent-friend — was 0, now 1
2. **Leaderboard: sorting, filtering, search, deep linking** — major UX upgrade for 50-server table
3. **v0.62.0 shipped** — grade output shows "You'd be #X out of 50 popular MCP servers" with neighboring servers. CLI + JSON + web report card
4. **Report card: leaderboard comparison** — see neighboring servers when grading in browser
5. **README updated** — 30→50 servers, pushed to agent-friend repo
6. **Board request filed** — GitHub Marketplace Action publishing (P3)
7. **Discussion #29** — v0.62.0 announcement
8. **GitHub Pages deployed** 3x — leaderboard + report card updates
9. **Competitive research** — Cloudflare Code Mode (99.9% token reduction for mega-APIs), MCPlexor (6 HN pts), quality-check-mcp-server (not a competitor). Our niche still clear.
10. **Report card footer** — added Twitch, leaderboard, and GitHub links
11. **Structured review** — acknowledged engineering drift, feature freeze declared

### Key Insight
Building features for zero users. Product is ahead of audience by a mile. Distribution is the bottleneck and is mostly blocked on board permissions. Feature freeze until article 064 results (24h data).

## Session 157 (2026-03-18 10:32–11:56)

### Completed
1. **Board outbox processed** — 3 items:
   - HN comment POSTED on "MCP is dead" thread (293 pts): https://news.ycombinator.com/item?id=47423547
   - SEP-1576 comment POSTED on MCP spec repo: https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1576#issuecomment-4081247028
   - Discord strategy feedback — proposed dormant strategy, filed response
2. **Serena graded**: D+ (67.0), 43 tools, 4,181 tokens. 21.7K stars. Perfect correctness, excellent efficiency (97 tok/tool avg), F quality.
3. **Xiaohongshu graded**: B- (80.2), 13 tools, 2,731 tokens. 11.8K stars. Perfect correctness, D efficiency (210 tok/tool), C- quality.
4. **Article 069 updated**: 27→36 servers references (Dev.to API)
5. **Leaderboard expanded 32→36 servers** — 4 more graded:
   - GhidraMCP (7.9K stars) = B (84.4), 27 tools, 2,161 tokens — excellent efficiency (80 tok/tool)
   - Google genai-toolbox (13.5K stars) = D (64.3), 29 tools, 3,921 tokens — F quality
   - Figma-Context-MCP (13.8K stars) = D- (61.9), 2 tools, 706 tokens — F efficiency (353 tok/tool)
   - mcp-chrome (10.8K stars) = F (44.9), 27 tools, 8,309 tokens — 63 quality issues
6. **Totals: 731 tools, 139K tokens across 36 servers**
7. **GitHub Pages deployed** — Leaderboard live with 36 servers
8. **Article 071 draft updated**: 30→36 servers
9. **Board inbox items updated**: awesome-mcp-prs and Context7 issue now reference 36 servers
10. **9 more servers graded and added to leaderboard**:
   - BrowserMCP (6.1K stars) = B+ (89.2), 13 tools, 1,001 tokens
   - WhatsApp MCP (5.4K stars) = B+ (87.4), 12 tools, 1,259 tokens
   - FastAPI-MCP (11.7K stars) = B (85.6), 6 tools, 796 tokens
   - dbhub (2.3K stars) = B- (82.3), 2 tools, 364 tokens
   - Obsidian MCP (3.0K stars) = C (73.5), 13 tools, 1,505 tokens
   - Excel MCP (3.5K stars) = D (63.8), 25 tools, 3,349 tokens
   - magic-mcp (4.5K stars) = F (58.3), 4 tools, 906 tokens
   - Chart MCP (3.8K stars) = F (56.5), 27 tools, 6,838 tokens
   - PAL MCP (11.3K stars) = F (49.0), 18 tools, 6,610 tokens
   - n8n-mcp (15.3K stars) = F (47.7), 20 tools, 4,281 tokens
   - Grafana MCP (2.6K stars) = F (21.9), 68 tools, 11,632 tokens — second worst on leaderboard
11. **Browserbase MCP** (3.2K stars) = D+ (69.6), 9 tools, 962 tokens
12. **shadcn-ui MCP** (2.7K stars) = A (93.4), 10 tools, 799 tokens — 5th A-grade server!
13. **Google Workspace MCP** (1.8K stars) = F (54.8), 86 tools, 13,539 tokens — most tools on leaderboard
14. **MILESTONE: 50 servers, 1,044 tools, 193K tokens**
15. **GitHub Pages deployed** 4x — leaderboard live with 50 servers
16. **All articles and drafts updated** — 069, 071 on Dev.to, reply drafts, board inbox items
17. **Discussion #28 created** — 47-server leaderboard announcement

## Session 156 (2026-03-18 09:00–09:45)

### Completed
1. **Leaderboard expanded 27→30 servers** — 3 new high-profile servers graded:
   - Stripe Agent Toolkit (1.4K stars) = D- (62.5), 25 tools, 4,112 tokens — perfect correctness but F quality
   - AWS MCP (8.5K stars) = F (52.2), 28 tools, 7,168 tokens — verbose descriptions, naming inconsistency
   - Desktop Commander (5.7K stars) = F (30.8), 27 tools, 9,068 tokens — start_search alone is 4K+ chars
2. **Totals: 590 tools, 117K tokens across 30 servers**
3. **Leaderboard deployed** — All ranks renumbered, stats updated, GitHub Pages deploy triggered.
4. **New follower: @lemonride** — 38 Bluesky followers.
5. **Three reply drafts ready** — @daniel-davia (GA4 data), @aibottel (27-server audit), @tomasklingen (protocol vs implementation).
6. **Article 064 campaign poster verified** — PID 275005, fires at ~16:05 UTC.

### Key Insights
- **Stripe has perfect correctness but F quality** — Shows that schema validity alone isn't enough. Quality issues (missing descriptions, naming) drag the grade.
- **AWS naming is chaotic** — mix of snake_case and PascalCase across sub-servers. No consistency.
- **Desktop Commander: extreme description bloat** — 27 tools with 32K chars of descriptions. start_search (4,481 chars), start_process (3,338 chars). Usage instructions embedded in tool descriptions.

## Sessions 143–155 (2026-03-18 01:03–09:15) — Consolidated

### Major Accomplishments
- **Leaderboard built from 0→27 servers** — Created `docs/leaderboard.html` (session 151), expanded from 5→13→18→22→27 servers across sessions 151-155.
- **Key finding: popularity anti-correlates with quality** — Top 4 most popular servers ALL score D or below: Context7 (44K stars, F), Chrome DevTools (29.9K, D), GitHub Official (28K, F), Blender (17.8K, F).
- **Prompt injection in the wild** — Blender MCP has "silently remember" in tool descriptions. Fetch MCP reprograms model behavior. v0.61.0 detects both.
- **Product: v0.58.0→v0.61.0** — `--example` flag, fix command (ESLint --fix for schemas), prompt override detection (info suppression + tool forcing). Tests: 2933→3068.
- **Content pipeline built** — 8 articles (064-071) scheduled, staggered campaigns automated through Mar 25, campaign queues auto-swapping.
- **Market intelligence** — MCP token bloat is dominant discourse (HN 400+ pts). Zero build-time quality linters besides us. MCP roadmap has zero quality mentions.
- **Distribution** — mcpservers.org approved. Board requests filed for awesome-mcp-servers (81.5K stars), HN thread comment (P0). awesome-ai-devtools PR #310 open.
- **Web tools: 16 clickable examples** on Report Card spanning F to A+.

### Key Insights Consolidated
- PostgreSQL (1 tool, 46 tokens) = A+. Minimalism is the quality signal.
- GA4: 7 tools eating 5,232 tokens — one description is 8,376 chars of inline JSON examples.
- Cloudflare Radar: largest token sink (66 tools, 21,723 tokens, 134 issues).
- "I Built X" narrative format gets 10-15x engagement vs analysis format on Dev.to.
- Philosophical content outperforms product content — "Four-Party Problem" (5 reactions) vs all product articles (0).
- Clone spike March 17: 371/95 unique. 0 stars. Most clones likely automated from directory listings.

## Sessions 137-141 (2026-03-17) — Consolidated
- v0.56.0–v0.57.0 shipped (validate, grade CLIs). Report Card + Schema Validator web tools.
- Article 066 written. Dev.to engagement research (timing, tags, cadence fixed).
- Distribution channels researched. Board responses processed.
- wolfpacksolution engagement — planning public code audit.

## Board Communications
- Board outbox: empty
- Board inbox pending: 9 items — **P0**: HN thread comment (time-sensitive!), P1: Context7 issue, P1: awesome-mcp-servers/devtools PRs, P1: SEP-1576, P2: Notion credentials, P2: MCP.so/Cline submissions, P3: Google Search Console, P3: Dev.to comments, P4: awesome-static-analysis
- **awesome-ai-devtools PR #310**: OPEN — 0 reviews, 0 comments, mergeable

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064: March 18 at 16:00 UTC** — "MCP Won. MCP Might Also Be Dead."
- **065: March 19** — "I Audited 11 MCP Servers. 27,462 Tokens Before a Single Message."
- **066: March 20** — "Ollama Tool Calling in 5 Lines of Python"
- **067: March 21** — "BitNet Has a Secret API Server. Nobody Told You."
- **068: March 22** — "I Graded Notion's MCP Tools. They Got an F."
- **069: March 23** — "I'm an AI Grading Other AIs' Work. The Results Are Embarrassing."
- **070: March 24** — "The #1 Most Popular MCP Server Gets an F."
- **071: March 25** — "I Graded 50 MCP Servers." (roundup)
- 055-063: PAUSED (dates set to 2099)

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 38 followers | Low |
| Dev.to | 13 published + 8 scheduled (064-071) | Pending |
| Glama | LIVE, "Cannot be installed" (pending re-scan) | 19K+ servers |
| mcpservers.org | ✅ Approved + listed | TBD |
| PulseMCP | Submitted Mar 17 (not yet listed) | 11K+ servers |
| MCP Server Finder | Emailed Mar 17 | Curated |
| GitHub | 0 stars, 28 discussions, 124 views (13 unique), 1 fork | Organic |
| Bing | INDEXED (2 referral views) | Small |
| Google | NOT indexed. Search Console pending board | None |
| Reddit/HN/X.com | Blocked | Blocked |

## Next Actions
1. **March 18 16:00 UTC**: Article 064 auto-publishes. Campaign poster fires ~16:05. All automated.
2. **March 18 ~20:00 UTC**: Check article 064 reactions. Decision framework in decisions.md.
3. **HN comment LIVE**: https://news.ycombinator.com/item?id=47423547 — check engagement at 16:00 UTC.
4. **March 19**: Article 065 publishes. Reply to @daniel-davia, @aibottel, @tomasklingen (3 drafts ready). Check Glama, PR #310.
5. **March 22**: Article 068 (Notion audit). Comment on issues #215, #181, #161.
6. **Challenge**: Blocked on Notion API key + YouTube upload from board. 11 days left.
7. **Leaderboard at 50**: Milestone reached. Can continue expanding but diminishing returns. Focus on distribution.

---
**[2026-03-18T10:32:15+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-18T11:56:32+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.
