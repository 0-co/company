# Company Status

**Last updated:** 2026-03-17 19:20 UTC (session 136/Day 10)

## Current Phase
**Day 10** — Glama listing approved. Shipped Dockerfile for hosted MCP execution. Board items processed. Articles prepped for tomorrow's double publish.

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 36 | 50 | - |
| Broadcast minutes | 4876+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | 0 | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles | 13 published + 4 scheduled | - | - |
| Tests | 2701 | - | - |
| LLM Providers | 5 | - | - |
| Web tools | 3 (audit, convert, benchmark) | - | - |

## Session 136 (2026-03-17 19:01–ongoing)

### Completed
1. **Board outbox processed** — 4 items: AI CMO (declined, $20/mo generic wrapper), Glama approved (actioned), tests failing (already fixed), license check (verified OK).
2. **Glama Dockerfile** — Created Dockerfile + .dockerignore + glama.json for hosted MCP server execution on Glama infrastructure. Pushed to both repos. CI green.
3. **server.json updated** — v0.55.0, 2701 tests.
4. **GitHub Discussion #16** — Glama listing announcement.
5. **Article 064 updated** — Test count 2701, added Glama link in footer.
6. **Bluesky drafts finalized** — 4 posts for March 18 (article, Glama, benchmark, build-time vs runtime).
7. **punkpeye engaged** — Replied to license comment + asked about installability status on Glama.
8. **MCP competitive landscape** — mcp2cli hit HN (99% token reduction claim). Perplexity CTO confirmed moving away. 5+ runtime optimizers, zero build-time linters besides us.

### Key Findings
- **Glama listing live** but shows "Cannot be installed" — Dockerfile should fix once re-scanned.
- **Bluesky engagement: 0** — 36 followers, zero likes/reposts on all today's posts. Channel is effectively dead for distribution.
- **MCP conversation on Bluesky is thin** — key influencers (Simon Willison) last posted about MCP in December. Conversation has moved to HN/Reddit where we're blocked.
- **0 comments on all 16 GitHub Discussions** — we're talking to ourselves.

## Board Communications
- Board outbox: empty (all processed and deleted)
- Board inbox pending: `2-mcp-registry-and-awesome-list.md`, `3-google-search-console.md`
- Board inbox processed/deleted: GitHub tokens (dead end), ProductHunt (rejected), Glama/registries, Reddit

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064 + 065: March 18** — Double publish (board approved 2/day). "MCP Won. MCP Might Also Be Dead." + "How Many Tokens Are Your AI Tools Costing You?"
- **066: March 19** — "Ollama Tool Calling in 5 Lines of Python"
- **067: March 20** — "BitNet Has a Secret API Server. Nobody Told You."
- 055-063: PAUSED (dates set to 2099)

## Product State
- **agent-friend v0.55.0**: Universal tool adapter + audit/optimize CLI + GitHub Action + BitNet provider. 2701 tests. MIT.
- **5 LLM providers**: Anthropic, OpenAI, OpenRouter, Ollama, BitNet
- **Web tools**: audit.html, convert.html, benchmark.html
- **MCP server**: 314 tools via stdio. **Glama listing live** + Dockerfile for hosted execution.
- **GitHub Discussions**: #1-#16

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 36 followers, zero engagement | Dead |
| Dev.to | 13 articles + 4 scheduled, ~0 reactions | Minimal |
| Glama | LIVE, "Cannot be installed" (Dockerfile pending) | 19K+ servers |
| mcpservers.org | Submitted, awaiting approval | TBD |
| GitHub | 0 stars, 16 discussions, 194 unique clones, 1 fork | Organic |
| Google | NOT indexed. Search Console pending board. | None |
| Reddit/HN/X.com | Blocked | Blocked |

## Next Actions
1. **Tomorrow 09:00 UTC**: Articles 064+065 auto-publish. Post 4 Bluesky drafts throughout the day.
2. **Check punkpeye response** on Glama installability.
3. **Check mcpservers.org** (March 19 deadline).
4. **March 19**: Article 066 auto-publishes.
5. **March 20**: Article 067 auto-publishes.
6. **Core problem**: 0 stars, 0 engagement across all channels. Distribution strategy needs rethinking. Current channels are exhausted without board unblocking Reddit/HN.
