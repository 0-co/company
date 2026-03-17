# Company Status

**Last updated:** 2026-03-17 23:50 UTC (session 140/Day 10)

## Current Phase
**Day 10** — Shipped MCP Report Card (6th web tool). Article 064 auto-publishes March 18 at 16:00 UTC. Bluesky drafts ready with 97% stat from arxiv paper.

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
| Web tools | 6 (report card, validate, audit, convert, benchmark, hub) | - | - |
| MCP directories | 4 (Glama live, mcpservers.org pending, PulseMCP pending, mcpserverfinder pending) | - | - |

## Session 140 (2026-03-17 23:27–ongoing)

### Completed
1. **MCP Report Card shipped** — 6th web tool. Paste tool schemas, get letter grade (A+ through F). Correctness 40%, Efficiency 30%, Quality 30%. Screenshot-friendly card with animated grade reveal. Cross-linked from all other tools. Deployed to GitHub Pages, IndexNow submitted.
2. **Academic validation found** — arxiv paper 2602.14878v1: 97.1% of MCP tool descriptions have deficiencies across 856 tools in 103 servers. Validates our optimize command's approach. Added to Bluesky draft for tomorrow.
3. **Competitive intel** — mcp2cli: 1,300 stars in 8 days from Show HN. token-ct: 0 stars. Our space is wide open but HN (shadow banned) is the #1 distribution channel for dev tools.
4. **Bluesky drafts updated** — Added 97% stat to Post 2, prioritized reply list based on new notifications.
5. **Cross-linking** — Report Card added to footer of all 5 existing web tools + agent-friend README.
6. **Stream title updated** — "Building MCP Report Card — grade your AI tool schemas"
7. **All article 064 links verified** — audit.html, validate.html, GitHub repo all returning 200.

## Session 139 (2026-03-17 22:35–23:26)

### Completed
1. **MCP Schema Validator shipped** — `validate.html`, 5th web tool. 12 client-side checks for OpenAI/Anthropic/MCP/Google/JSON Schema. Strict mode, auto-format detection. Deployed to GitHub Pages, indexed via IndexNow. Targets "MCP schema validator" search intent.
2. **Board directive: no test counts** — Purged test count mentions from README badge, articles 064/065/067, synced both repos. Rule: CI pass/fail only.
3. **Cross-linked all 5 web tools** — Every page footer links to all others. Consistent navigation across validate, audit, convert, benchmark, tools hub.
4. **Updated sitemap** — Added validate.html entry.
5. **Twitch viewer response** — Replied to professeurwannabe about BitNet experience.
6. **Article 064 prep** — Added validator link, removed test count, updated on Dev.to.
7. **Competitive check** — Apify MCP Validator exists but validates running servers (runtime). Ours validates static schemas (build-time). Different tools, different intent.
8. **Article 066 written** — "Ollama Tool Calling in 5 Lines of Python." Created on Dev.to (ID: 3364983). Publishes March 20. Targets Ollama community.
9. **Board responses processed** — Glama claimed (Docker works, waiting for re-scan). awesome-ai-devtools PR #310 submitted by board. awesome-mcp-servers deferred. tiny-helpers failed (empty diff). MCP Registry auth deferred.
10. **Docker image tested** — Builds and responds correctly via stdio. 314 tools returned. Issue is likely Glama hasn't re-scanned.
11. **Twitch tags updated** — Replaced autoGPT/terminal/agentic with python/opensource/mcp.
12. **Context window impact feature** — CLI audit now shows % of GPT-4o/Claude/GPT-4/Gemini context consumed. Warns at >2%. Added to CLI, web calculator (audit.html), and GitHub Action step summary. 4 new tests.
13. **Bluesky bio updated** — Now mentions MCP tool quality tools, current follower count.
14. **Article 067 fixed on Dev.to** — Body updated (removed test count from footer), tags synced to `bitnet, llm, python, ai`. GET /articles/3363773 returns 404 (API quirk with unpublished), but listing endpoint works and PUT succeeds.
15. **Bluesky drafts updated** — Added wolfpacksolution to reply list (building audit CLI, wants to scan our codebase). Updated article URL with actual slug.

## Board Communications
- Board outbox: empty (3 items processed)
- Board inbox pending: `3-google-search-console.md`
- **awesome-ai-devtools PR #310**: OPEN — waiting for review

## Session 138 (2026-03-17 21:51–22:34)

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
1. **March 18 16:00 UTC**: Article 064 auto-publishes. Post 4 Bluesky drafts afterward (16:30-20:00 UTC). Include validator announcement.
2. **March 18**: Reply to 4 Bluesky conversations (daniel-davia, onyx-kraken + 2 others). STRICT 4-reply limit.
3. **Check punkpeye** on Glama installability.
4. **Check mcpservers.org** (March 19).
5. **Board items still pending**: MCP Registry auth + awesome-mcp-servers PR + Google Search Console + Glama claim.
6. **Strategic**: Need board help with MCP Official Discord (11,658 members).

---
**[2026-03-17T21:51:11+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-17T22:34:12+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-17T23:26:58+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.
