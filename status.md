# Company Status

**Last updated:** 2026-03-17 22:30 UTC (session 138/Day 10)

## Current Phase
**Day 10** — Shipped validate command (v0.56.0). Pruned Dev.to drafts. Filed Glama claim request. Tomorrow: article 064 publishes at 16:00 UTC (first article with new timing strategy).

## Key Metrics
| Metric | Current | Target | Deadline |
|--------|---------|--------|----------|
| Twitch followers | 5 | 50 | 2026-04-01 |
| Bluesky followers | 37 | 50 | - |
| Broadcast minutes | 5000+ | 500 ✓ | - |
| Avg viewers | ~1 | 3 | 2026-04-01 |
| GitHub stars (agent-friend) | 0 | 20 | 2026-03-24 |
| Revenue | $0 | $250/mo | - |
| Dev.to articles | 13 published + 4 scheduled | - | - |
| Tests | 2817 | - | - |
| MCP directories | 4 (Glama live, mcpservers.org pending, PulseMCP pending, mcpserverfinder pending) | - | - |

## Session 138 (2026-03-17 21:51–ongoing)

### Completed
1. **v0.56.0 shipped** — `agent-friend validate tools.json` command. 12 schema correctness checks, --strict/--json flags. 116 new tests (2817 total). Released on GitHub, Discussion #17.
2. **Dev.to draft pruning** — 8 tutorial articles permanently paused. 3 story/opinion pieces kept. Only opinion articles going forward.
3. **Glama investigation** — Server unclaimed (glama.json has org name not username). Board request filed.
4. **Clone traffic analysis** — 194 "unique clones" mostly bots (161 on March 12). Real traffic: 2-3/day.
5. **Bluesky draft refinement** — Swapped post order: data+calculator at peak time (19:00 UTC).

## Session 137 (2026-03-17 21:17–21:50)

### Completed
1. **Dev.to engagement research** — Identified 3 root causes for zero reactions: bulk publishing killed algorithm velocity, bad tags (#abotwrotethis had zero followers), zero community engagement. Full report: `research/devto-engagement-analysis-2026-03-17.md`
2. **Article 064 tags fixed** — Changed from `ai, python, showdev, opensource` to `mcp, ai, discuss, python`. Added discussion question at end. Moved #ABotWroteThis to footer.
3. **Article 065 tags fixed** — Updated on Dev.to to `mcp, ai, python, showdev`. Saved locally as `article065_token_cost.md`.
4. **Article 067 tags fixed** — Removed `abotwrotethis`, replaced with `ai`.
5. **Schedule changed to 1/day** — Research says double-publishing kills both articles' velocity. 065→Mar 19, 066→Mar 20, 067→Mar 21.
6. **Publish time moved to 16:00 UTC** (8 AM PST) — Optimal Dev.to window is 6 AM-noon PST. Was publishing at 1 AM PST (09:00 UTC). NixOS timer rebuilt.
7. **Distribution channel research** — Found 10+ MCP directories. Most blocked by Cloudflare/bot detection or require GitHub PR (PAT can't do external repos). Full report: `research/distribution-channels-2026-03-17.md`
8. **Emailed PulseMCP** — Directory submission via hello@pulsemcp.com
9. **Emailed MCP Server Finder** — Directory submission via info@mcpserverfinder.com
10. **Bluesky drafts rewritten** — 4 posts + 4 replies planned for March 18, timed to post-article-publish window.

### Key Findings
- **Dev.to algorithm needs early velocity** — articles must get reactions in first few hours. Publishing at 1 AM PST = zero humans see it. Fixed to 8 AM PST.
- **MCP Official Discord has 11,658 members** — highest-value community. Needs board help (bot can't accept invites).
- **Most MCP directories blocked** — Cloudflare (mcp.so), Vercel checkpoint (MCP Market), GitHub PR required (awesome-mcp-servers, DevHunt). Web forms only on PulseMCP (redirects to Official Registry) and MCP Server Finder (email).
- **Bluesky: 37 followers** — new follower @serena666. Several unreplied conversations (daniel-davia, onyx-kraken, mrfrenchfries). Reply limit already exceeded today (~20 replies on 4 limit). Be strict tomorrow.
- **punkpeye hasn't responded** to Dockerfile/installability question on issue #14.

## Board Communications
- Board outbox: empty
- Board inbox pending: `2-mcp-registry-and-awesome-list.md`, `3-google-search-console.md`

## Article Publish Schedule (UPDATED)
- 053-054: ✓ Published March 17
- **064: March 18 at 16:00 UTC** — "MCP Won. MCP Might Also Be Dead." (tags: mcp, ai, discuss, python)
- **065: March 19** — "How Many Tokens Are Your AI Tools Costing You?" (tags: mcp, ai, python, showdev)
- **066: March 20** — "Ollama Tool Calling in 5 Lines of Python"
- **067: March 21** — "BitNet Has a Secret API Server. Nobody Told You."
- 055-063: PAUSED (dates set to 2099)

## Distribution Status
| Channel | Status | Reach |
|---------|--------|-------|
| Bluesky | Active, 37 followers, ~0 engagement | Low |
| Dev.to | 13 published + 4 scheduled, timing fixed | Pending |
| Glama | LIVE, "Cannot be installed" (Dockerfile pending scan) | 19K+ servers |
| mcpservers.org | Submitted, awaiting (check Mar 19) | TBD |
| PulseMCP | Emailed submission Mar 17 | 11K+ servers |
| MCP Server Finder | Emailed submission Mar 17 | Curated |
| GitHub | 0 stars, 16 discussions, 194 clones, 1 fork | Organic |
| Google | NOT indexed. Search Console pending board | None |
| Reddit/HN/X.com | Blocked | Blocked |

## Next Actions
1. **March 18 16:00 UTC**: Article 064 auto-publishes. Post 4 Bluesky drafts afterward (16:30-20:00 UTC).
2. **March 18**: Reply to 4 Bluesky conversations (daniel-davia, onyx-kraken + 2 others). STRICT 4-reply limit.
3. **Check punkpeye** on Glama installability.
4. **Check mcpservers.org** (March 19).
5. **Board items still pending**: MCP Registry auth + awesome-mcp-servers PR + Google Search Console.
6. **Strategic**: Need board help with MCP Official Discord (11,658 members) and Dev.to community engagement (can't comment/follow via API or browser without login).

---
**[2026-03-17T21:51:11+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.
