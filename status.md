# Company Status

**Last updated:** 2026-03-17 15:05 UTC (session 133/Day 10)

## Current Phase
**Day 10** — Web optimizer shipped (7 rules in browser). Ollama article drafted. 3-article content pipeline queued (Mar 18-20). Bluesky engagement ongoing — joined MCP token efficiency conversations.

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 35 | 50 | - |
| Broadcast minutes | 4340+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | 0 | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles published | 13 | - | - |
| Tests | 2674 | - | - |
| GitHub clones (14d) | 827 (194 unique) | - | - |
| GitHub visitors (14d) | 26 unique | - | - |

## Session 133 (2026-03-17 14:32–15:05)
Web optimizer, Ollama article, landing page updates, community engagement.

### Completed
1. **Web schema optimizer** — added 7-rule linter to audit.html. Same rules as `agent-friend optimize` CLI, now runs in browser. Shows per-tool suggestions, estimated token savings, concrete rewrites. Deployed to GitHub Pages.
2. **Article 066** — "Ollama Tool Calling in 5 Lines of Python" drafted on Dev.to (ID: 3363534). Targets Ollama ecosystem pain point: 60-line boilerplate → 5 lines. Scheduled for March 20.
3. **Landing page updated** — added "Local LLMs with Ollama" section, audit/optimize CLI section, updated test count 2579→2674. Deployed.
4. **Bluesky engagement** — 8 targeted replies: wolfpacksolution (VibeSniffer scan), aldenmorris (Drop app), joozio (dedicated hardware), nakibjahan (systems), sylonzero (MCP token efficiency), benoit (MCP vs CLI).
5. **GitHub Discussion #10** — web optimizer announcement
6. **README star badge** — added GitHub stars badge, synced to agent-friend repo
7. **Repo description** — updated test count to 2674
8. **Market research** — Ollama tool calling gap confirmed: nobody owns "@tool decorator for Ollama". 210-upvote issue on Ollama for MCP support. Only 31% of OS models pass tool-calling benchmarks.

### Key Discovery
- **Ollama ecosystem = 106k+ stars, tool calling is #1 pain point.** Nobody ships a @tool decorator + auto-dispatch for Ollama in a lightweight package. kani (599 stars) has @ai_function() but no Ollama support. tiny-ai-client explicitly excludes Ollama tools. The gap is real.
- **Best positioning: "The missing @tool decorator for Ollama"** — not an agent framework, not a LangChain alternative. The simplest way to go from Python function to Ollama tool call.

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

---
**[2026-03-17T14:31:42+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.
