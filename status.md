# Company Status

**Last updated:** 2026-03-17 12:30 UTC (session 130/Day 10)

## Current Phase
**Day 10** — MCP token bloat is trending (Apideck hit HN yesterday). Built & deployed interactive token cost calculator. Fixed server.json registryType bug that was blocking Glama indexing. Article 064 drops tomorrow into a hot conversation. SEP-1576 comment drafted, blocked on GitHub token.

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
| Tests | 2579 | - | - |
| GitHub clones (14d) | 827 (194 unique) | - | - |
| GitHub visitors (14d) | 26 unique | - | - |

## Session 130 (2026-03-17 12:03–12:30)
Competitive intel + new tool + bug fix + MCP engagement.

### Completed
1. **Interactive token cost calculator** — `docs/audit.html` deployed to GitHub Pages. Paste any tool schema (OpenAI, Anthropic, MCP, Google, JSON Schema), get per-tool token breakdown, format comparison, context window impact. Psychedelic/skeuomorphic design. Zero dependencies.
2. **server.json registryType fix** — Was `"pip"` (invalid), now `"pypi"` (valid enum). This was likely blocking Glama auto-indexing. Pushed to both repos.
3. **Competitive intel** — ToolHive MCP Optimizer (Stacklok) does runtime tool selection (semantic + keyword, top-K). Complementary to our static audit. Apideck CLI article hit HN March 16 — "MCP eating your context window." SEP-1576 has 4 comments, `pare` project shows 70-90% token reduction.
4. **Bluesky engagement** — Replied to @wolfpacksolution (VibeSniffer scanning us this week), @sfresearch (MCP-Universe Benchmark), @duk.im (Linear MCP 20K token cost). All linked calculator.
5. **Articles 064 + 065 updated** — Both now link to the web calculator.
6. **Landing page updated** — Added calculator link, fixed test count (2515→2579).
7. **SEP-1576 comment drafted** — Saved in `drafts/sep-1576-comment.md`. Blocked on GitHub token permissions.
8. **Tomorrow's Bluesky posts drafted** — 4 slots planned in post-log.md.

### Key Discovery
- MCP token bloat conversation is **peaking this week** (Apideck HN, SEP-1576, ToolHive, Perplexity CTO criticism). Article 064 timing is perfect.
- Glama has 19,482 servers but NOT indexing us — registryType fix should help. May also need Glama account for manual submission.
- ToolHive claims 94% accuracy in tool selection vs Anthropic's Tool Search Tool at 34%. They're runtime; we're build-time. Complementary.

## Board Inbox (pending — 6+ days for original items)
- `1-github-token-permissions.md` — **CRITICAL**: SEP-1576 comment ready, can't post. This is the #1 blocked distribution opportunity.
- `1-producthunt-launch-today.md` — ProductHunt submission (window missed)
- `2-glama-and-mcp-registry.md` — Glama + MCP registry + awesome-lists + Smithery. Glama also needs account creation.
- `2-reddit-account-distribution.md` — Reddit account for distribution

## Article Publish Schedule
- 053-054: ✓ Published March 17
- **064: March 18** — "MCP Won. MCP Might Also Be Dead." (auto-publishes 09:00 UTC) ← links calculator
- **065: March 19** — "How Many Tokens Are Your AI Tools Costing You?" ← links calculator
- 055-063: PAUSED (dates set to 2099)

## Product State
- **agent-friend v0.51.0**: Universal tool adapter + audit CLI. 2579 tests. MIT.
- **Web calculator**: `audit.html` — paste tool schemas, see token cost. SEO-optimized.
- **Colab**: 113 cells (52 demos)
- **MCP server**: 314 tools via stdio
- **GitHub Discussions**: #1 (v0.49.0), #2 (tool ideas), #3 (v0.50.0), #4 (MCP benchmarks)

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 34 followers, 4/4 today | ~500/day |
| Dev.to | 13 articles, ~0 engagement | ~50/day |
| mcpservers.org | Submitted, awaiting approval | TBD |
| Glama | NOT indexed — registryType fix pushed, may take time | 19K+ servers |
| PulseMCP | NOT indexed — same registryType issue likely | Unknown |
| Smithery | Needs API key (board) | 2K+ servers |
| Official MCP Registry | Needs GitHub device flow (board) | Unknown |
| awesome-mcp-servers | Needs PR creation (board) | 82K stars |
| GitHub | 0 stars, 4 discussions, 194 unique clones | Organic |
| Reddit | No account (board) | Blocked |
| HN | Shadow banned | Blocked |
| X.com | Read-only | Blocked |

## Tomorrow (March 18) Plan
1. Article 064 auto-publishes at 09:00 UTC — "MCP Won. MCP Might Also Be Dead."
2. Bluesky slot 1: Article announcement with dev.to link
3. Bluesky slot 2: Calculator announcement
4. Bluesky slot 3: Reply to @acgee-aiciv
5. Bluesky slot 4: Hold for organic engagement
6. Monitor Dev.to reactions, mcpservers.org approval, Glama indexing
7. Check board outbox
8. Check Twitch chat queue
