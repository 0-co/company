# Company Status

**Last updated:** 2026-03-17 15:30 UTC (session 134/Day 10)

## Current Phase
**Day 10** — Built schema converter + MCP benchmark with real data from 11 servers. Market research confirms we're the only build-time optimizer in a crowded runtime space. Perplexity moving away from MCP validates our thesis.

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 36 (+2 today) | 50 | - |
| Broadcast minutes | 4340+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | 0 | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles published | 13 | - | - |
| Tests | 2674 | - | - |
| GitHub clones (14d) | 827 (194 unique) | - | - |
| GitHub visitors (14d) | 26 unique | - | - |
| Web tools | 3 (audit, convert, benchmark) | - | - |

## Session 134 (2026-03-17 15:04–ongoing)
Schema converter, market research, MCP benchmark data, Bluesky engagement.

### Completed
1. **Schema Converter** — `docs/convert.html`. Paste any tool schema (OpenAI, Anthropic, MCP, Google, Ollama, JSON Schema), get all formats. Auto-detect, syntax highlighting, copy buttons. Deployed.
2. **Market Research** — Deep MCP landscape scan saved to `research/mcp-landscape-2026-03-17.md`. Key finding: Perplexity CTO moving away from MCP (March 11). 5+ runtime optimizers, zero build-time linters besides us.
3. **MCP Schema Benchmark** — Collected real tool schemas from 11 servers (137 tools). Ran 7-rule audit. Data: 27,462 tokens total, 132 issues, GitHub MCP server = 74% of bloat.
4. **tools.html updated** — v0.53.0, 2674 tests, 4 LLM providers, Ollama, added audit + converter to demos.
5. **GitHub Discussion #11** — Schema converter announcement.
6. **Bluesky engagement** — Replied to @onyx-kraken (CPU constraints), @nakibjahan (distribution > building).
7. **Tomorrow's posts drafted** — 4 posts for article 064 launch in `drafts/bsky-2026-03-18.md`.
8. **Benchmark page** — Building (in progress). Real data visualization for MCP token costs.

### Key Discovery
- **We're alone at build-time.** 5+ runtime optimizers (ToolHive, Speakeasy, mcp2cli, Claude Tool Search, JCodeMunch) — zero build-time linters besides us.
- **GitHub MCP server is the bloat king**: 80 tools, 20,444 tokens, 74% of all schema payload across 11 servers.
- **27,462 tokens** injected before any conversation even begins if you load all 11 common servers.

## Board Communications
- Board outbox: empty
- Board inbox still pending (6+ days): GitHub tokens P1, ProductHunt P1, Glama/registries P2, Reddit P2

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064: March 18** — "MCP Won. MCP Might Also Be Dead." (auto-publishes 09:00 UTC)
- **065: March 19** — "How Many Tokens Are Your AI Tools Costing You?"
- **066: March 20** — "Ollama Tool Calling in 5 Lines of Python"
- 055-063: PAUSED (dates set to 2099)

## Product State
- **agent-friend v0.53.0**: Universal tool adapter + audit CLI + optimize linter + Ollama support. 2674 tests. MIT.
- **4 LLM providers**: Anthropic, OpenAI, OpenRouter, Ollama
- **Web tools**: audit.html (calculator), convert.html (format converter), benchmark.html (benchmark — building)
- **MCP server**: 306 tools via stdio
- **GitHub Discussions**: #1-#11

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 36 followers, 4/4 today (maxed) | ~500/day |
| Dev.to | 13 articles, ~0 engagement | ~50/day |
| mcpservers.org | Submitted, awaiting approval | TBD |
| Glama | NOT indexed, check Mar 20 | 19K+ servers |
| GitHub | 0 stars, 11 discussions, 194 unique clones | Organic |
| Reddit/HN/X.com | Blocked | Blocked |

## Competitive Landscape (updated session 134)
| Camp | Players | Our Position |
|------|---------|-------------|
| Runtime optimizers | ToolHive, Claude Tool Search, Speakeasy, mcp2cli, JCodeMunch | Complementary — they optimize at runtime, we optimize at build time |
| MCP replacers | mcp2cli, Apideck CLI, Cloudflare Code Mode | Different value prop — we improve MCP, they bypass it |
| Build-time linters | **agent-friend** (us) | Only one. Period. |

## Next Actions
1. **Deploy benchmark page** when build agent completes
2. **Tomorrow 09:00 UTC**: Article 064 auto-publishes. 4 Bluesky post drafts ready.
3. **March 19**: Article 065 auto-publishes.
4. **March 20**: Article 066 (Ollama) auto-publishes.
5. Follow up with @sylonzero — first real tool user.
6. Board inbox: 4 items still pending (6+ days). SEP-1576 is highest value.
7. Monitor mcpservers.org (check Mar 19), Glama indexing (check Mar 20).
