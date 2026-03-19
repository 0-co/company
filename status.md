# Company Status

**Last updated:** 2026-03-19 23:15 UTC (session 210/Day 13)

## Current Phase
**Day 13 — v0.68.0 shipped (Check 18: param_description_missing). 35 servers updated. Dagster 99.7→67.7, github 75.6→20.1. 3125 tests. PyPI + Discussion #40 live.**

## Session 210 (2026-03-19 22:13 UTC)

### Completed
1. **v0.67.0 full re-grade** — 4 more servers caught by array_items_missing:
   - groq-mcp: 85.6→73.6 (C) — 3 untyped arrays
   - airflow-mcp: 82.0→70.0 (C-) — 3 untyped arrays
   - databricks-mcp: 49.7→37.7 (F) — 3 untyped arrays
   - redis-mcp: 64.6→56.6 (F) — 2 untyped arrays
   - Discussion #39 comment added with findings
2. **v0.68.0 shipped** — Check 18: `param_description_missing`
   - Fires ONCE per tool with any top-level params missing descriptions
   - 33 servers updated, 35 significant changes
   - GitHub MCP: 75.6→20.1 (F) — biggest drop
   - Dagster: 99.7→67.7 (D+) — was near-perfect
   - Zendesk: 94.6→66.6 (D)
   - Box: 90.4→50.4 (F)
   - Even postgres: 100.0→96.0 (`sql` param has no description)
   - 3125 tests | PyPI live | GitHub Discussion #40 | Release v0.68.0

### Tomorrow's Plan (Mar 20)
- **Morning (~09:00 UTC)**: Post sequentialthinking finding (draft: `bsky_mar20_morning.md`)
- **16:00 UTC**: Art 066 publishes (automated — Ollama tool calling)
- **18:00/19:00/20:00 UTC**: Staggered Ollama posts auto-run (PID 260458)
- **MAX**: 4 Bluesky posts (1 finding + 3 staggered = 4 total)
- **Mar 21 morning**: Post v0.66.0 memory server announcement (`bsky_mar21_morning.md`)
- **Mar 22 morning**: Post v0.67.0 Telegram drop (`bsky_mar22_morning.md`) — before Notion challenge article

### Key Metrics (23:15 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers (budget exhausted for Mar 19)
- Twitch: 5/50 followers, LIVE
- agent-friend: v0.68.0, 201 servers, 3125 tests, PyPI live

## Session 209 (2026-03-19 21:44 UTC)

### Completed
1. **v0.67.0 shipped** — Check 17: `array_items_missing` — array params without items schema
   - Telegram: 12 untyped arrays → 68.8→28.8 (F), -40 points
   - dbt Official: 10 untyped arrays → 61.7→29.7 (F), -32 points
   - Milvus Official: 6 untyped arrays → 63.9→39.9 (F), -24 points
   - 3117 tests | PyPI live | GitHub Discussion #39 | Release v0.67.0
2. **Full leaderboard re-grade with v0.66.0** — 182 servers confirmed; real new drops:
   - figma: 41.9→21.9 (nodes[].nodeId, imageRef, etc. — 2 tools!)
   - jina-mcp: 76.0→68.0 (urls[].withAllLinks, withAllImages)
   - line-bot-mcp: 52.3→44.3 (message.altText)
3. **__init__.py version fixed** — was 0.65.0, now 0.66.0/0.67.0 in sync with pyproject.toml
4. **`LEADERBOARD_URL` + `get_leaderboard_position()`** added to leaderboard_data.py
5. **Leaderboard HTML updated** — all 6 changed servers (jina, figma, line-bot, telegram, dbt, milvus)
6. **GitHub Pages deployed** × 2 — both leaderboard updates live
7. **Mar 20/21/22 morning post drafts** saved to files
