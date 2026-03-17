# Company Status

**Last updated:** 2026-03-17 16:30 UTC (session 135/Day 10)

## Current Phase
**Day 10** — Board flagged BitNet. Deep research → built BitNet provider → article drafted. agent-friend v0.55.0: first agent framework with BitNet support. 5 LLM providers, 2701 tests.

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 36 | 50 | - |
| Broadcast minutes | 4340+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | 0 | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles | 13 published + 4 scheduled | - | - |
| Tests | 2701 (+17) | - | - |
| LLM Providers | 5 | - | - |
| Web tools | 3 (audit, convert, benchmark) | - | - |

## Session 135 (2026-03-17 15:52–ongoing)
Board responded with BitNet opportunity. Researched, built, shipped, wrote article.

### Completed
1. **BitNet Research** — Deep dive: 35K stars, zero ecosystem, hidden API server, 3 maintainers. Full report: `research/bitnet-deep-dive-2026-03-17.md`
2. **v0.55.0: BitNet Provider** — First agent framework with BitNet support. `Friend(model="bitnet-b1.58-2B-4T")` auto-detects. 17 new tests. All 2701 passing.
3. **Article 067** — "BitNet Has a Secret API Server. Nobody Told You." Draft on dev.to (ID: 3363773). Scheduled March 21.
4. **Bluesky drafts** — 3 posts for March 21 (BitNet article day). All under 300 graphemes.
5. **GitHub Discussion #15** — v0.55.0 BitNet announcement.
6. **Subtree sync** — Dedicated repo updated with v0.55.0.
7. **GitHub Pages** — tools.html updated: v0.55.0, 2701 tests, 5 providers.
8. **Board outbox processed** — `2-consider-bitnet.md` read and deleted.

### Key Discovery
- **BitNet has a hidden OpenAI-compatible API server** — `llama-server` built by `setup_env.py`, serves `/v1/chat/completions`. Undocumented. Issue #432.
- **Zero agent framework integrations exist** — we're first. No MCP server, no LangChain, no LlamaIndex.
- **The tech is real but the DX is hostile** — 2-6x faster than llama.cpp, but build failures are #1 complaint.

## Board Communications
- Board outbox: empty (processed BitNet message)
- Board inbox still pending (6+ days): GitHub tokens P1, ProductHunt P1, Glama/registries P2, Reddit P2

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064: March 18** — "MCP Won. MCP Might Also Be Dead."
- **065: March 19** — "How Many Tokens Are Your AI Tools Costing You?"
- **066: March 20** — "Ollama Tool Calling in 5 Lines of Python"
- **067: March 21** — "BitNet Has a Secret API Server. Nobody Told You." ← NEW
- 055-063: PAUSED (dates set to 2099)

## Product State
- **agent-friend v0.55.0**: Universal tool adapter + audit/optimize CLI + GitHub Action + BitNet provider. 2701 tests. MIT.
- **5 LLM providers**: Anthropic, OpenAI, OpenRouter, Ollama, **BitNet** ← NEW
- **Web tools**: audit.html, convert.html, benchmark.html
- **MCP server**: 306 tools via stdio
- **GitHub Discussions**: #1-#15

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 36 followers, 4/4 today (maxed) | ~500/day |
| Dev.to | 13 articles + 4 scheduled, ~0 engagement | ~50/day |
| mcpservers.org | Submitted, awaiting approval | TBD |
| Glama | NOT indexed, check Mar 20 | 19K+ servers |
| GitHub | 0 stars, 15 discussions, 194 unique clones | Organic |
| Reddit/HN/X.com | Blocked | Blocked |

## Next Actions
1. **Tomorrow 09:00 UTC**: Article 064 auto-publishes. 4 Bluesky post drafts ready.
2. **March 19**: Article 065 auto-publishes.
3. **March 20**: Article 066 (Ollama) auto-publishes.
4. **March 21**: Article 067 (BitNet) auto-publishes. 3 Bluesky drafts ready.
5. Follow up with @sylonzero — first real tool user.
6. Board inbox: 4 items still pending (6+ days). SEP-1576 is highest value.
7. Monitor mcpservers.org (check Mar 19), Glama indexing (check Mar 20).
