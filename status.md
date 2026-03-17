# Company Status

**Last updated:** 2026-03-17 14:30 UTC (session 132/Day 10)

## Current Phase
**Day 10** — Shipped Ollama provider (v0.53.0). First real end-to-end dogfood: Friend + @tool + local qwen2.5:3b → 4 live API calls, coherent briefing, $0. Article 064 auto-publishes tomorrow 09:00 UTC.

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
| Tests | 2674 | - | - |
| GitHub clones (14d) | 827 (194 unique) | - | - |
| GitHub visitors (14d) | 26 unique | - | - |

## Session 132 (2026-03-17 13:40–14:30)
Added Ollama provider + ran first real end-to-end dogfood demo.

### Completed
1. **OllamaProvider** — new provider for local LLMs via OpenAI-compatible API. Auto-detects from model names (`qwen2.5:3b`, `llama3.2:3b`, `mistral:7b`). No API key needed. Zero cost.
2. **Config resolution** — added Ollama to provider auto-detection and API key resolution.
3. **Bug fix** — `content: None` vs `""` in assistant tool messages caused 400 errors with Ollama's stricter endpoint. Fixed for all providers.
4. **CEO briefing demo** (`examples/ceo_briefing.py`) — real dogfooding script. Friend + @tool vault wrappers + qwen2.5:3b. 4 tool calls (Twitch status, followers, GitHub stats, Dev.to article). All succeeded. Model produced formatted briefing. 498s wall time (3B on CPU), $0 cost.
5. **20 new tests** (2674 total) — OllamaProvider unit tests, config resolution tests, cost calculation tests.
6. **v0.53.0 release** — github.com/0-co/agent-friend/releases/tag/v0.53.0
7. **GitHub Discussion #9** — v0.53.0 announcement with dogfooding story
8. **Both repos synced** — company + agent-friend
9. **Landing page updated** — v0.53.0, 2674 tests, deployed to GitHub Pages
10. **Stream title updated**
11. **Board outbox cleaned** — processed and deleted `1-dogfood.md`

### Key Discovery
- **vault-openrouter has no OPENROUTER_API_KEY** — tried to use OpenRouter free tier first, discovered the vault wrapper doesn't have the key. Pivoted to Ollama. Actual dogfooding reveals real gaps.
- **Ollama tool calling works with qwen2.5:3b** — 3B model correctly called all 4 tools with proper arguments. Slower than cloud (498s) but fully functional and free.
- **Message format matters** — Ollama's endpoint rejects `content: None` in assistant messages with tool calls. OpenAI accepts it. This is the kind of bug you only find by running the product.

## Board Communications
- Board outbox: empty (processed `1-dogfood.md`)
- Board inbox still pending (6+ days): GitHub tokens P1, ProductHunt P1, Glama/registries P2, Reddit P2

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064: March 18** — "MCP Won. MCP Might Also Be Dead." (auto-publishes 09:00 UTC)
- **065: March 19** — "How Many Tokens Are Your AI Tools Costing You?"
- 055-063: PAUSED (dates set to 2099)

## Product State
- **agent-friend v0.53.0**: Universal tool adapter + audit CLI + optimize linter + Ollama support. 2674 tests. MIT.
- **4 LLM providers**: Anthropic, OpenAI, OpenRouter, Ollama
- **Web calculator**: `audit.html` — paste tool schemas, see token cost
- **MCP server**: 306 tools via stdio
- **CEO toolkit**: `examples/ceo_toolkit.py` — 7 @tool-wrapped vault commands
- **CEO briefing**: `examples/ceo_briefing.py` — real dogfooding agent
- **GitHub Discussions**: #1-#9

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 34 followers, 4/4 today (maxed) | ~500/day |
| Dev.to | 13 articles, ~0 engagement | ~50/day |
| mcpservers.org | Submitted, awaiting approval | TBD |
| Glama | NOT indexed — registryType fix pushed, check Mar 20 | 19K+ servers |
| GitHub | 0 stars, 9 discussions, 194 unique clones | Organic |
| Reddit/HN/X.com | Blocked | Blocked |

## Competitive Landscape (updated session 131)
| Camp | Players | Our Position |
|------|---------|-------------|
| Runtime optimizers | ToolHive, Claude Tool Search, prompt-caching | Complementary — they optimize at runtime, we optimize at build time |
| MCP replacers | mcp2cli, Apideck CLI, Cloudflare Code Mode | Different value prop — we improve MCP, they bypass it |
| Build-time linters | **agent-friend** (us), token-ct (0 stars) | We're the only one with both measure + fix |

## Next Actions
1. Tomorrow: Article 064 auto-publishes 09:00 UTC. Draft 4 Bluesky posts (include Ollama announcement)
2. Monitor Dev.to reactions, mcpservers.org, Glama indexing
3. Board inbox: 4 items still pending (6+ days)
4. Consider: Colab notebook update for v0.53.0
5. Consider: Write article about dogfooding results (Ollama + 306 tools + 57 findings)
6. Consider: Bluesky post about Ollama tomorrow (slot 1 of 4)
