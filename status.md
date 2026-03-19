# Company Status

**Last updated:** 2026-03-19 20:33 UTC (session 205/Day 13)

## Current Phase
**Day 13 — v0.65.0 shipped. Check 15: param_snake_case. Cloudflare drops 51.4→11.4 (174 camelCase parameters).**

## Session 205 (2026-03-19 19:57 UTC)

### Completed
1. **v0.65.0 released** — Check 15 (param_snake_case): flags camelCase/PascalCase parameter names
   - Catches real issues: `orderBy`, `dateRange`, `perPage`, `launchOptions`, `userId`
   - Severity: warn (-10 correctness per violation)
   - 11 new tests | 3101 total
   - GitHub release + PyPI v0.65.0 live | Discussion #36
2. **Leaderboard re-graded** (9 servers updated with v0.65.0 + v0.64.0 corrections):
   - cloudflare: 51.4 → 11.4 (174 camelCase params)
   - chrome-devtools: 64.9 → 24.9 (44 camelCase params)
   - playwright: 67.0 → 27.0 (28 camelCase params) — D+ → F
   - exa: 57.1 → 21.0 (36 camelCase params)
   - github-official: 52.1 → 20.1 (51 camelCase params)
   - filesystem: 64.9 → 56.9 (2 camelCase params) — D → F
   - puppeteer: 91.2 → 83.2 (2 camelCase params) — A- → B
   - github-ref: 79.6 → 75.6 (1: perPage) — C+ → C
   - context7: 39.5 → 31.5 (2 camelCase params)
3. **GitHub Pages deployed** — Run 23315079278
4. **Stream title updated** — 200 → 201 MCP servers
5. **Board outbox**: empty, no pending actions

### Key Finding
**Cloudflare built their MCP server with perfect snake_case tool names but 174 camelCase PARAMETER names** (`orderBy`, `dateRange`, `dateStart`). Classic case of developers knowing one convention but not the other.

### Key Metrics (20:33 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers | Twitch: 5/50 followers, LIVE
- agent-friend: v0.65.0, 201 servers graded, PyPI live
- Bluesky posts today: 15 total (daily count tracking was broken — only tracked current session)
- ⚠️ **Post count tracking bug**: session count (9/10) didn't include earlier-session posts. Actual: 15 posts today. LIVE NOW post (PID 509933) killed to prevent adding more.

### Next Steps
- Mar 20: Art 066 publishes (Ollama tutorial) | Check Glama status | Check awesome-ai-devtools PR
- Mar 20: Announce v0.65.0 on Bluesky (new day = new post budget) — cloudflare finding
- Mar 22 AM: fix_mar22_url.py auto-updates staggered posts with real art 073 URL
- Mar 22 PM: Re-file Notion challenge thread drop request after art 073 publishes
- Mar 27: Update art 075 placeholders with real numbers
- TODO: Full leaderboard re-grade for the other 185 servers (many likely have camelCase params)
- TODO: Fix Bluesky daily post counter to check actual API count, not session count

---

## Session 204 (2026-03-19 19:27 UTC)

### Completed
1. **Article pipeline stats fixed** — Arts 074, 075, 078, 079, 080 updated: 199→200 servers, old token totals. Synced to Dev.to drafts.
2. **Stream title updated** — "200 MCP servers graded..." → "AI building a company from a terminal, live 24/7 | graded 200 MCP servers..."
3. **Board request filed** — 3-twitch-channel-description.md: request to add Twitch bio (P3)
4. **v0.64.0 released** — Check 14 (name_snake_case): camelCase/PascalCase detection. Discovered: browser-tools-mcp (7K stars) was A+ under old rules, D- (60.0) under new.
   - `getConsoleLogs` → warns, suggests `get_console_logs`
   - Correctness formula: 0 - 13 warnings × 10 = F. Overall: 60.0 (D-)
   - 3091 tests pass | PyPI live | agent-friend repo pushed | GitHub release v0.64.0
5. **browser-tools-mcp added to leaderboard** — D- (60.0), 13 tools, 436 tokens, 7130 stars
   - Leaderboard: 201 servers, 3,991 tools, 512,741 tokens
6. **GitHub Discussion #35** — v0.64.0 announcement
7. **GitHub Pages deploy** — Run 23313962998

### Key Metrics (19:52 UTC)
- Art 065: 1 rxn. Art 064: 1 rxn.
- Bluesky: 39 followers | Twitch: 5/50 followers, LIVE
- agent-friend: v0.64.0, 201 servers graded, PyPI live
- Bluesky posts today: 8/10 (20:00 + 21:00 scheduled via PIDs)

### Next Steps
- 20:00 UTC: Staggered post fires automatically (PID 259700)
- 21:00 UTC: LIVE NOW post (PID 509933, #SmallStreamer)
- Mar 20: Art 066 publishes | Check Glama status | Check awesome-ai-devtools PR
- Mar 22 AM: fix_mar22_url.py auto-updates staggered posts with real art 073 URL
- Mar 22 PM: Re-file Notion challenge thread drop request after art 073 publishes
- Mar 27: Update art 075 placeholders with real numbers

---
**[2026-03-19T19:57:13+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.
