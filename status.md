# Company Status

**Last updated:** 2026-03-17 13:30 UTC (session 131/Day 10)

## Current Phase
**Day 10** — Shipped `agent-friend optimize` + dogfooded it on own 306 tools. Board responded: "Use agent-friend yourself." Done — ran audit/optimize on own tools, fixed 57 findings, created CEO toolkit with @tool-wrapped vault commands. Article 064 drops tomorrow.

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 34 | 50 | - |
| Broadcast minutes | 4340+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | 0 | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles published | 13 | - | - |
| Tests | 2654 | - | - |
| GitHub clones (14d) | 827 (194 unique) | - | - |
| GitHub visitors (14d) | 26 unique | - | - |

## Session 131 (2026-03-17 12:30–13:30)
Built optimize command + deep market research + article updates + dogfooded own tools.

### Completed
1. **`agent-friend optimize`** — heuristic schema linter. 7 rules: verbose prefixes, long descriptions, redundant params, missing descriptions, cross-tool duplicates, deep nesting. 75 new tests (2654 total). v0.52.0.
2. **Deep market research** — mcp2cli (145pts HN, 96-99% savings), Garry Tan "MCP sucks honestly", Cloudflare Code Mode (244K→1K tokens), Scalekit (4-32x overhead), token-ct (competitor, 0 stars). Nobody does build-time measurement + optimization.
3. **Article 064 updated** — Added Apideck 72% stat, Scalekit 4-32x, Garry Tan quote, mcp2cli data, Cloudflare numbers, calculator CTA. Pushed to Dev.to draft.
4. **Article 065 updated** — Rewrote with optimize command pipeline (measure → fix → verify). Added competitive landscape context. Pushed to Dev.to draft.
5. **v0.52.0 release** — github.com/0-co/agent-friend/releases/tag/v0.52.0
6. **GitHub Discussion #6** — v0.52.0 announcement
7. **Landing page + README** — Updated for v0.52.0, optimize command, 2654 tests
8. **GitHub Pages deployed** — Landing page live
9. **Both repos synced** — company + agent-friend
10. **Tomorrow's Bluesky posts re-drafted** — Sharper: article + optimize + calculator + data
11. **Board responded: "Dogfood agent-friend"** — Acted immediately.
12. **Ran audit/optimize on own 306 tools** — 23,502 tokens total, 57 suggestions, fixed all. Trimmed cross-tool duplication (regex flags 7x, git repo_dir 6x), verbose descriptions, added ~50 missing param descriptions. Down to 22 suggestions (remaining are intentional).
13. **CEO toolkit** (`examples/ceo_toolkit.py`) — 7 @tool-wrapped vault commands (Twitch, Bluesky, Dev.to, Discord, GitHub). 452 tokens. Actually running in production.
14. **GitHub Discussion #8** — Dogfooding results

### Key Discovery
- **mcp2cli** is biggest new competitor — but it bypasses MCP entirely. We complement MCP, don't replace it. Different value prop.
- **"ESLint for MCP schemas"** is the positioning. ESLint didn't compete with bundlers. We don't compete with ToolHive.
- **Dogfooding works**: audit/optimize found real issues in our own 306 tools. 57 suggestions, all actionable. The tool does what it promises.
- **The window is narrow.** If runtime optimizers make this "good enough" at the client layer, the build-time niche shrinks.

## Board Communications
- **Board outbox `1-dogfood.md`** — "Use agent-friend yourself." ✓ ACTED ON (session 131)
- Board inbox still pending (6+ days): GitHub tokens P1, ProductHunt P1, Glama/registries P2, Reddit P2

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064: March 18** — "MCP Won. MCP Might Also Be Dead." (auto-publishes 09:00 UTC) ← updated with mcp2cli, Garry Tan, Cloudflare data + calculator CTA
- **065: March 19** — "How Many Tokens Are Your AI Tools Costing You?" ← rewritten with optimize pipeline
- 055-063: PAUSED (dates set to 2099)

## Product State
- **agent-friend v0.52.0**: Universal tool adapter + audit CLI + optimize linter. 2654 tests. MIT.
- **Web calculator**: `audit.html` — paste tool schemas, see token cost
- **MCP server**: 306 tools via stdio
- **CEO toolkit**: `examples/ceo_toolkit.py` — 7 @tool-wrapped vault commands, 452 tokens
- **GitHub Discussions**: #1-#8

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 34 followers, 4/4 today | ~500/day |
| Dev.to | 13 articles, ~0 engagement | ~50/day |
| mcpservers.org | Submitted, awaiting approval | TBD |
| Glama | NOT indexed — registryType fix pushed, monitoring | 19K+ servers |
| GitHub | 0 stars, 8 discussions, 194 unique clones | Organic |
| Reddit/HN/X.com | Blocked | Blocked |

## Competitive Landscape (updated session 131)
| Camp | Players | Our Position |
|------|---------|-------------|
| Runtime optimizers | ToolHive, Claude Tool Search, prompt-caching | Complementary — they optimize at runtime, we optimize at build time |
| MCP replacers | mcp2cli, Apideck CLI, Cloudflare Code Mode | Different value prop — we improve MCP, they bypass it |
| Build-time linters | **agent-friend** (us), token-ct (0 stars) | We're the only one with both measure + fix |

## Next Actions
1. Tomorrow: Article 064 auto-publishes 09:00 UTC. Post 4 Bluesky slots.
2. Monitor Dev.to reactions, mcpservers.org, Glama indexing
3. Board inbox: 4 items still pending (6+ days). Dogfood directive acted on.
4. Continue dogfooding: use Friend class with CEO toolkit for workflow automation
5. Consider: Colab notebook update for v0.52.0
6. Consider: Write article about dogfooding results (306 tools, 57 findings)
