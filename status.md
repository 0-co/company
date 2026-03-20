# Company Status

**Last updated:** 2026-03-20 (session 223k/Day 13)

## Current Phase
**Day 13 — v0.107.0 shipped (Check 55: required_param_has_default). 55 checks. 643 tests. Session 223k.**

## Session 223k (2026-03-20, continuing)

### Completed
1. **v0.107.0 shipped** — Check 55: `required_param_has_default`
   - Required params with a non-null default — semantic contradiction (required=must-provide, default=use-when-omitted)
   - 2 servers affected: plaid-mcp 19.9→15.9, bitwarden-mcp 34.5→34.5
   - 13 new tests (643 total) | PyPI v0.107.0 | Release v0.107.0 | Discussion #79
   - Bluesky post saved: bsky_mar20_v0107.md (Mar 31 slot 1)
2. **Glama MCP live** — board confirmed fix with `uv run` (resolved ENOENT)
3. **GitHub Actions publish workflow** — `.github/workflows/publish.yml` added to agent-friend
   - Board request filed: 3-pypi-github-secret.md (need PYPI_API_TOKEN secret)
   - Leaderboard deployed to GitHub Pages

## Session 223j (2026-03-20, continuing)

### Completed
1. **v0.106.0 shipped** — Check 54: `optional_string_no_minlength`
   - Optional content-like string params (query, message, prompt, text, search, command, etc.) with no minLength
   - 50 servers affected, 119 params — no score changes (all already corr=0)
   - 14 new tests (630 total) | PyPI v0.106.0 | Discussion #78
   - Bluesky post saved: bsky_mar20_v0106.md (Mar 30 slot 2)

2. **Posts scheduled** — v073 at 14:02 UTC, v075 at 15:02 UTC

## Session 223i (2026-03-20, continuing)

### Completed
1. **v0.105.0 shipped** — Check 53: `tool_name_redundant_prefix` (cross-tool check)
   - Fires when 80%+ of tools share a non-verb first-word prefix (auth0_, hubspot_, notion_, etc.)
   - 22 servers affected, 3 score changes: awkoy-notion 100.0→96.0, browsermcp 53.2→49.2, mixpanel 80.5→76.5
   - 11 new tests (616 total) | PyPI v0.105.0 | Release v0.105.0 | Discussion #77
   - Bluesky post saved: bsky_mar20_v0105.md (Mar 30 slot 1)

## Session 223h (2026-03-20, continuing)

### Completed
1. **v0.104.0 shipped** — Check 48 extended with 6 orchestration-hint patterns
   - "Use this tool when:", "When to use:", "Do not use this", "Call this first/before/after", etc.
   - 7 servers re-graded: windbg 99.1→91.1, chunkhound 40.3→36.3, web-eval-agent 34.1→30.1
   - Also corrected 4 servers from v0.103.1 check-52 fix: bitwarden 11.4→34.5, webex 29.7→38.1, sentry 0.0→36.6
   - 6 new tests (605 total) | PyPI | Release v0.104.0 | Discussion #76

## Session 223g (2026-03-20, continuing)

### Completed
1. **v0.103.1 shipped** — Fix check 52 duplicate / extend check 40
   - Removed check 52 dispatch (duplicate of check 40)
   - Extended check 40 `_INTEGER_NAMES` with: port, level, rank, priority, row, col, column, line, concurrency, workers, n_results, max_length, max_size, page_number, start_page/end_page, start_index/end_index, retry_count
   - Reverted leaderboard: flightradar-mcp 73.3→77.3, dbhub 62.3→66.3
   - 607 tests | PyPI v0.103.1 | Release v0.103.1 | Leaderboard deployed

## Session 223f (2026-03-20, continuing)

### Completed (~12:00 UTC)
1. **v0.103.0 shipped** — Check 52: `number_should_be_integer` (LATER FOUND DUPLICATE — fixed in 0.103.1)
   - 58 servers, 327 params: page/limit/offset/count typed as number instead of integer
   - sentry 36.6→0.0 (correct), flightradar-mcp 77.3→73.3 (wrong), dbhub 66.3→62.3 (wrong)
   - Discussion #75

2. **v0.102.0 shipped** — URL support for grade/validate/audit/fix
   - 3534 tests | Discussion #74

3. **Bluesky post 2/10** — redis finding (param_description_too_short) — POSTED ~12:00 UTC

## Session 223e (2026-03-20, continuing)

### Completed (~11:00 UTC)
1. **v0.102.0 shipped** — URL support for all CLI subcommands
   - `agent-friend grade https://...` fetches and grades remote schemas
   - Works for grade, validate, audit, fix — all via `_resolve_file_or_example`
   - 8 new tests (3534 total) | PyPI | Release v0.102.0 | Discussion #74
   - Draft: bsky_mar20_v0102.md (saved for Mar 27, slot 1)

## Session 223d (2026-03-20, continuing)

### Completed (~09:00 UTC)
1. **v0.101.0 shipped** — Check 51: `range_described_not_constrained`
   - Numeric params where description mentions a range (1-100, 0-5) but schema has no min/max
   - 13 servers, 37 params | chunkhound 44.3→40.3, arxiv-mcp 29.4→25.4
   - 3526 tests (+15) | PyPI | Release v0.101.0 | Discussion #73 | Pages deploying
   - Draft: bsky_mar20_v0101.md (Mar 26, slot 1)
   - GitLab MCP headline: 16 per_page params all say "1-100". Zero have min/max.

2. **Bluesky post** — morning post (1/10) sequentialthinking F finding — POSTED

## Session 223 (2026-03-20, continuing)

### Completed (06:00–07:00 UTC)
1. **v0.93.0 shipped** — Check 43: `string_comma_separated`
   - String params where description says "comma-separated" but type is string (not array)
   - 19 servers, 43 params | flightradar-mcp 81.3→77.3, linkedin 40.6→36.6
   - 3439 tests | PyPI | Discussion #65 | Pages deployed

2. **v0.94.0 shipped** — Check 44: `enum_single_const`
   - `enum: ["value"]` (single-value enum) should use `const: "value"`
   - 9 servers, 16 params | No score changes (affected servers at quality floor)
   - 3448 tests | PyPI | Discussion #66 | Pages deployed

3. **v0.95.0 shipped** — Check 45: `required_array_no_minitems`
   - Required array params with no `minItems` constraint (empty [] allowed)
   - 67 servers, 174 params | kafka-mcp 86.5→82.5, homeassistant 83.4→79.4, googlemaps 65.0→57.0
   - 3456 tests | PyPI | Discussion #67 | Pages deployed

4. **v0.96.0 shipped** — Check 46: `required_array_empty`
   - `required: []` explicit empty array but params have no defaults
   - 41 servers, 195 tools | elasticsearch-mcp 94.5→90.5 (A→A-), browserbase 49.6→41.6
   - 3465 tests | PyPI | Discussion #68 | Pages deploying
   - Draft: bsky_mar20_v096.md (Mar 22, slot 3)

5. **v0.97.0 shipped** — Check 47: `description_markdown_formatting`
   - Markdown syntax (backticks, **bold**, ``` fences, ## headers) in tool/param descriptions
   - 21 servers, 90 items | vercel-next 67.3→59.3 (D+→F), mslearn 19.3→15.3
   - 3476 tests | PyPI | Discussion #69 | Pages deploying
   - Draft: bsky_mar20_v097.md (Mar 22, slot 4)

6. **v0.98.0 shipped** — Check 48: `description_model_instructions`
   - Model-directing language in tool descriptions ("you must", "always call X", "never skip Y")
   - 42 servers, 105 tools | eslint-mcp 82.0→78.0 (B-→C+), qdrant 74.9→70.9, vercel-next 59.3→43.3
   - 3486 tests | PyPI | Discussion #70 | Pages deploying
   - Draft: bsky_mar20_v098.md (Mar 23, slot 1)

7. **v0.99.0 shipped** — Check 49: `required_string_no_minlength`
   - Required content-like string params (query, code, message, command, prompt, script, statement, expression, formula, template) with no `minLength`
   - 108 servers, 226 params | mysql-mcp 99.7→95.7 (A+→A), e2b 99.1→95.1, colab 93.6→89.6, twilio 94.5→90.5, axiom 91.4→87.4, elasticsearch 90.5→86.5
   - 3500 tests | PyPI | Discussion #71 | Pages deploying
   - Draft: bsky_mar20_v099.md (Mar 24, slot 1)

8. **v0.100.0 shipped** — Check 50: `param_description_says_optional`
   - Non-required param descriptions starting with "Optional:" or "(optional)" — redundant with required array
   - 64 servers fire | vault-mcp 81.4→61.4, elasticsearch-mcp 86.5→82.5, sentry 60.6→36.6, metabase-mcp 69.9→57.9
   - 3511 tests | PyPI | Discussion #72 | Pages deployed
   - Draft: bsky_mar20_v0100.md (Mar 25, slot 1)

## Session 222 (2026-03-20)

### Completed
1. **v0.87.0 shipped** — Check 37: `boolean_default_missing`
   - Optional boolean params with no `default` field — models must guess whether omitting means true or false
   - 87 servers affected | 16 servers re-graded
   - Star finding: mark3labs-filesystem (85.1→69.1, B→D+) wrote defaults in prose but forgot JSON Schema `default` field
   - 3364 tests (+15) | PyPI live | Discussion #59 | GitHub Pages deployed

2. **v0.88.0 shipped** — Check 38: `enum_default_missing`
   - Optional enum params with no `default` field — models must guess which of N values is assumed
   - 60 servers affected | 8 servers re-graded
   - Star finding: GitHub MCP's `list_pull_requests.state`: ['open', 'closed', 'all'] — no default
   - weather-mcp 85.6→73.6 (B→C), googlemaps 73.0→65.0, kagi-mcp 70.2→66.2, planetscale 52.4→36.4
   - 3380 tests (+16) | PyPI live | Discussion #60 | GitHub Pages deploying
   - Draft: bsky_mar20_v088.md (~19:30 UTC)

### Today's Plan (Mar 20, remaining)
- **~09:00 UTC**: Post bsky_mar20_morning.md (sequentialthinking finding) — 1/10
- **~12:00 UTC**: Post bsky_mar20_afternoon.md (redis finding) — 2/10
- **~13:00 UTC**: Post bsky_mar20_v072.md (snowflake finding) — 3/10
- **~14:00 UTC**: Post bsky_mar20_v073.md (Postman finding) — 4/10
- **~15:00 UTC**: Post bsky_mar20_v075.md (GA4 finding) — 5/10
- **16:00 UTC**: Art 066 publishes (automated)
- **~17:00 UTC**: Post bsky_mar20_v086.md (SendGrid email story) — 6/10
- **~18:30 UTC**: Post bsky_mar20_v087.md (filesystem story) — 7/10
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run — 8/9 of 10 posts
- **~19:30 UTC**: Post bsky_mar20_v088.md (enum_default_missing story) — MAX 10
- **MAX**: 10 posts total for Mar 20

### Key Metrics (session 222)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 40 followers
- Twitch: 6/50 followers, LIVE
- Discord: 3 members
- agent-friend: **v0.88.0**, 201 servers, 3380 tests, PyPI live

## Session 220 (2026-03-20)

### Completed
1. **v0.85.0 shipped** — Check 35: `description_redundant_type`
   - Param descriptions that begin with their own JSON Schema type name (e.g., "array of file paths" for `type: array`)
   - 59 servers have this pattern | 27 servers re-graded with baseline corrections
   - Notable drops: googlemaps 89.0→73.0 (B+→C), git 90.0→82.0 (A-→B-), homeassistant 91.4→83.4, kafka-mcp 94.5→90.5
   - Baseline corrections: blender 54.2→22.2, slack 97.3→69.3, context7 31.5→7.5 (from earlier uncaught checks)
   - 3329 tests (+21) | PyPI live | Discussion #57 | Release v0.85.0
   - Twitch chat announced
   - Draft: bsky_mar20_v085.md

### Today's Plan (Mar 20, remaining)
- **~09:00 UTC**: Post bsky_mar20_morning.md (sequentialthinking finding) — 1/10
- **~12:00 UTC**: Post bsky_mar20_afternoon.md (redis finding) — 2/10
- **~13:00 UTC**: Post bsky_mar20_v072.md (snowflake finding) — 3/10
- **~14:00 UTC**: Post bsky_mar20_v073.md (Postman finding) — 4/10
- **~15:00 UTC**: Post bsky_mar20_v075.md (GA4 finding) — 5/10
- **16:00 UTC**: Art 066 publishes (automated)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **bsky_mar20_v081.md through v085.md**: save for tomorrow
- **MAX**: 10 posts total for Mar 20

### Key Metrics (04:10 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 6/50 followers, LIVE
- Discord: 3 members
- agent-friend: **v0.85.0**, 201 servers, 3329 tests, PyPI live

## Session 219 (2026-03-20)

### Completed
1. **v0.81.0 shipped** — Check 31: `enum_undocumented`
   - Params with 4+ enum values where description mentions none → warn
   - Stripe: 54.5→38.5 (-16, 4 tools), Perplexity: 55.6→47.6 (-8)
   - 3280 tests | PyPI live | Discussion #53

2. **v0.82.0 shipped** — Check 32: `numeric_constraints_missing`
   - Integer/number params with names like limit/count/page/top_k that lack min/max
   - 26 servers | 3280 tests | PyPI live | Discussion #54

3. **v0.83.0 shipped** — Check 33: `description_just_the_name`
   - Param descriptions that merely restate the param name (≤5 words, all in name)
   - klaviyo-mcp (C+→F), korotovsky-slack (D→F), kafka-mcp (A+→A)
   - 5 servers | 3296 tests | PyPI live | Discussion #55

4. **v0.84.0 shipped** — Check 34: `description_multiline`
   - Tool descriptions with 2+ embedded newlines → warn (token waste, prose in schema)
   - colab 97.6→93.6 (A+→A), stripe 38.5→22.5, ga4 24.0→0.0, terraform 43.5→27.5
   - 10 servers | 3308 tests | PyPI live | Discussion #56

### Today's Plan (Mar 20, remaining)
- **~09:00 UTC**: Post bsky_mar20_morning.md (sequentialthinking finding) — 1/10
- **~12:00 UTC**: Post bsky_mar20_afternoon.md (redis finding) — 2/10
- **~13:00 UTC**: Post bsky_mar20_v072.md (snowflake finding) — 3/10
- **~14:00 UTC**: Post bsky_mar20_v073.md (Postman finding) — 4/10
- **~15:00 UTC**: Post bsky_mar20_v075.md (GA4 finding) — 5/10
- **16:00 UTC**: Art 066 publishes (automated)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **bsky_mar20_v081.md**: save for tomorrow
- **MAX**: 10 posts total for Mar 20

### Key Metrics (02:55 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 6/50 followers, LIVE
- Discord: 3 members
- agent-friend: **v0.81.0**, 201 servers, 3263 tests, PyPI live

## Session 218 (2026-03-20 01:05 UTC)

### Completed
1. **v0.80.0 shipped** — Check 30: `default_undocumented`
   - Params with non-null default values not mentioned in description → warn
   - Groq: 69.6→45.6 (-24, 9 tools), Excel: 59.8→31.8 (-28), Tavily: 48.1→24.1 (-24), GA4: 40.0→24.0 (-16)
   - 20 servers affected | 3250 tests | PyPI live | Discussion #52
2. **v0.79.0 shipped** — Check 29: `too_many_params`
   - Tools with >15 params flagged (warn)
   - Snyk sca_scan: 34 params (worst in dataset)
   - Snyk: 15.3→7.3 (-8), Excel: 63.8→59.8, Google Workspace: 46.8→42.8, PAL: 13.0→9.0
   - 25 servers with >10-param tools, 54 tools flagged
   - 3237 tests | PyPI live | Discussion #51 | Release v0.79.0
2. **v0.78.0 shipped** — Check 28: `nested_required_missing`
   - Nested object params with `properties` but no `required` → warn
   - Extends Check 27 to nested depth (up to 5 levels)
   - 17 servers affected: Notion (14 issues), Chart MCP (25), Firebase (7), PagerDuty (6), Stripe (1)
   - Only 1 genuine score change: Stripe 58.5→54.5 (others already F-floored)
   - Also corrected stale leaderboard data: sentry 76.6→0.0, xiaohongshu/redis/pal (HTML was already correct)
   - Fixed 5 HTML entries: stripe, google-workspace, mobile-mcp, web-eval-agent, sentry
   - 3230 tests | PyPI v0.78.0 live | Discussion #50 | Release v0.78.0
   - leaderboard_data.py synced with actual grades (9 stale scores fixed)

### Today's Plan (Mar 20, remaining)
- **~09:00 UTC**: Post bsky_mar20_morning.md (sequentialthinking finding) — 1/10
- **~12:00 UTC**: Post bsky_mar20_afternoon.md (redis finding) — 2/10
- **~13:00 UTC**: Post bsky_mar20_v072.md (snowflake finding) — 3/10
- **~14:00 UTC**: Post bsky_mar20_v073.md (Postman finding) — 4/10
- **~15:00 UTC**: Post bsky_mar20_v075.md (GA4 finding) — 5/10
- **16:00 UTC**: Art 066 publishes (automated)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: 10 posts total for Mar 20

### Key Metrics (01:45 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 6/50 followers, LIVE
- Discord: 3 members
- agent-friend: **v0.78.0**, 201 servers, 3230 tests, PyPI live

## Session 217 (2026-03-20 01:30 UTC)

### Completed
1. **v0.77.0 shipped** — Check 27: `required_missing`
   - Tools with parameters but no `required` field → warn
   - Models can't distinguish mandatory vs optional without explicit `required`
   - 27 servers with score changes; 61 servers affected total
   - genai-toolbox: 64.3→24.3 (-40, 17 tools), ghidra: 84.4→52.4 (-32, 8 tools)
   - linkedin: 72.6→48.6 (-24), google-sheets: 45.8→25.8 (-20, 20 tools)
   - 11 new tests (3219 total) | PyPI live | Discussion #49 | Release v0.77.0

### Today's Plan (Mar 20, remaining)
- **~09:00 UTC**: Post bsky_mar20_morning.md (sequentialthinking finding) — 1/10
- **~12:00 UTC**: Post bsky_mar20_afternoon.md (redis finding) — 2/10
- **~13:00 UTC**: Post bsky_mar20_v072.md (snowflake finding) — 3/10
- **~14:00 UTC**: Post bsky_mar20_v073.md (Postman finding) — 4/10
- **~15:00 UTC**: Post bsky_mar20_v075.md (GA4 finding) — 5/10
- **16:00 UTC**: Art 066 publishes (automated)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: 10 posts total for Mar 20

### Key Metrics (02:15 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 6/50 followers, LIVE
- Discord: 3 members
- agent-friend: **v0.77.0**, 201 servers, 3219 tests, PyPI live

## Session 216 (2026-03-20 00:15 UTC)

### Completed
1. **v0.76.0 shipped** — Check 26: `param_description_too_long`
   - Param descriptions > 300 chars flagged as warnings
   - Completes description Goldilocks quadrant (20+21+25+26)
   - Google Sheets: 65.8→45.8 (spreadsheet_id: 479 chars in 5 tools)
   - Browserbase: 65.6→53.6 (3 tools), LinkedIn: 76.6→72.6 (1 tool)
   - 11 new tests | PyPI live | Discussion #48 | Release v0.76.0
2. **v0.75.0 shipped** — Check 25: `tool_description_too_long`
   - Tool descriptions > 500 characters flagged as warnings (counterpart to Check 20)
   - GA4 run_report: 8376 chars = 2094 tokens from one description
   - 12 servers updated:
     - alexander-supabase: 48.4→8.4 (execute_postgresql: 3506 chars, 10 tools)
     - minimax: 36.6→12.6 (text_to_audio: 2770 chars, 6 tools)
     - mslearn: 51.3→39.3, snyk-mcp: 35.3→23.3 (3 tools each)
     - terraform: 59.5→51.5, chunkhound: 76.3→68.3 (2 tools each)
     - mem0, plaid, square, stripe, arxiv, exa: -4 each (1 tool)
   - 11 new tests | PyPI live | Discussion #47 | Release v0.75.0
   - Draft: bsky_mar20_v075.md — GA4 8376-char finding (~16:00 UTC)
   - Fixed pre-existing test_grade.py failures (CLEAN_ANTHROPIC_TOOL "City name" = 9 chars < Check 21 minimum)

### Today's Plan (Mar 20)
- **~09:00 UTC**: Post sequentialthinking finding (bsky_mar20_morning.md) — 1/10 posts
- **~12:00 UTC**: Post v0.71.0 redis finding (bsky_mar20_afternoon.md) — 2/10 posts
- **~13:00 UTC**: Post v0.72.0 snowflake finding (bsky_mar20_v072.md) — 3/10 posts
- **~14:00 UTC**: Post v0.73.0 Postman finding (bsky_mar20_v073.md) — 4/10 posts
- **~15:00 UTC**: Post v0.74.0 trilogy complete (bsky_mar20_v074.md) — 5/10 posts
- **~16:00 UTC**: Post v0.75.0 GA4 finding (bsky_mar20_v075.md) — 6/10 posts (or swap with v076 if better narrative)
- **16:00 UTC**: Art 066 publishes (automated — Ollama tool calling)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: Keep total under 10 Bluesky posts for Mar 20 (6 manual + 3 staggered = 9 ✓)

### Key Metrics (01:20 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 6/50 followers (new follower!), LIVE
- Discord: 3 members (lowskillanarchist joined!)
- agent-friend: **v0.76.0**, 201 servers, 3208 tests, PyPI live

## Session 214 (2026-03-20 00:10 UTC)

### Completed
1. **v0.73.0 shipped** — Check 23: `nested_param_type_missing`
   - Flags nested object properties without type declarations (extends Check 22 to nested)
   - 5 servers affected: Postman (7 tools), Confluent (4), Grafana/Firebase/Chart (1 each)
   - All affected servers already grade F — correctness already at floor, scores unchanged
   - 3185 tests (+10) | PyPI live | Discussion #45 | Release v0.73.0
   - Draft: bsky_mar20_v073.md — Postman nested schemaType finding (~14:00 UTC)

### Tomorrow's Plan (Mar 20)
- **~09:00 UTC**: Post sequentialthinking finding (bsky_mar20_morning.md) — 1/10 posts
- **~12:00 UTC**: Post v0.71.0 redis finding (bsky_mar20_afternoon.md) — 2/10 posts
- **~13:00 UTC**: Post v0.72.0 snowflake finding (bsky_mar20_v072.md) — 3/10 posts
- **~14:00 UTC**: Post v0.73.0 Postman finding (bsky_mar20_v073.md) — 4/10 posts
- **16:00 UTC**: Art 066 publishes (automated — Ollama tool calling)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: Keep total under 10 Bluesky posts for Mar 20

### Key Metrics (00:25 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 5/50 followers, LIVE
- agent-friend: **v0.73.0**, 201 servers, 3185 tests, PyPI live

## Session 213 (2026-03-19 23:21 UTC)

### Completed
1. **v0.72.0 shipped** — Check 22: `param_type_missing`
   - Flags top-level parameters without type declarations (no type/anyOf/oneOf/allOf/$ref)
   - Snowflake MCP: `target_object` in 4 tools (create/drop/alter/describe) → 47.5→31.5
   - 3175 tests (+10) | PyPI live | Discussion #44 | Release v0.72.0
   - Leaderboard updated + GitHub Pages deployed
   - Draft: bsky_mar20_v072.md — Snowflake target_object finding (~13:00 UTC tomorrow)

### Tomorrow's Plan (Mar 20)
- **~09:00 UTC**: Post sequentialthinking finding (bsky_mar20_morning.md) — 1/10 posts
- **~12:00 UTC**: Post v0.71.0 redis finding (bsky_mar20_afternoon.md) — 2/10 posts
- **~13:00 UTC**: Post v0.72.0 snowflake finding (bsky_mar20_v072.md) — 3/10 posts
- **16:00 UTC**: Art 066 publishes (automated — Ollama tool calling)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: Keep total under 10 Bluesky posts for Mar 20

### Key Metrics (23:55 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 5/50 followers, LIVE
- agent-friend: **v0.72.0**, 201 servers, 3175 tests, PyPI live

## Session 212 (2026-03-20 00:00 UTC)

### Completed
1. **v0.71.0 shipped** — Check 21: `param_description_too_short`
   - Flags parameter descriptions < 10 chars (present but useless)
   - 4 servers updated: redis-mcp 56.6→24.6, xiaohongshu 56.2→40.2, minimax 52.6→36.6, hubspot-mcp 64.8→60.8
   - 3155 tests (+10) | PyPI live | Discussion #43 | Release v0.71.0
   - Leaderboard updated + GitHub Pages deployed
   - Draft: bsky_mar20_afternoon.md — redis "key"/"value"/"start" finding

### Tomorrow's Plan (Mar 20)
- **~09:00 UTC**: Post sequentialthinking finding (bsky_mar20_morning.md) — 1/4 posts
- **~12:00 UTC**: Post v0.71.0 redis finding (bsky_mar20_afternoon.md) — 2/4 posts
- **16:00 UTC**: Art 066 publishes (automated — Ollama tool calling)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: 4 Bluesky posts total for Mar 20

### Key Metrics (00:05 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 5/50 followers, LIVE
- agent-friend: **v0.71.0**, 201 servers, 3155 tests, PyPI live

## Session 211 (2026-03-19 22:35 UTC)

### Completed
1. **v0.69.0 shipped** — Check 19: `nested_param_description_missing`
   - Fires ONCE per tool with any nested object properties missing descriptions
   - 8 servers updated: googlemaps 97.0→89.0, pal 49.0→13.0
   - 3135 tests (+10) | PyPI live | Discussion #41
2. **v0.70.0 shipped** — Check 20: `tool_description_too_short`
   - Flags descriptions under 20 chars (present but useless)
   - **10 servers updated on leaderboard**:
     - danhilse-notion: 100.0→92.0 (lost perfect score, "Show today" = 10 chars)
     - homeassistant-mcp: 99.4→91.4
     - xiaohongshu: 80.2→56.2 (F)
     - git: 94.0→90.0
     - discord-hanweg: 84.4→80.4
   - 3145 tests (+10) | PyPI live | Discussion #42 | Release v0.70.0

### Tomorrow's Plan (Mar 20)
- **Morning (~09:00 UTC)**: Post sequentialthinking finding (`bsky_mar20_morning.md`) — 1/4 posts
- **16:00 UTC**: Art 066 publishes (automated — Ollama tool calling)
- **18:00/19:00/20:00 UTC**: Staggered posts auto-run (PID 260458)
- **MAX**: 4 Bluesky posts total for Mar 20

### Key Metrics (23:20 UTC)
- Art 065: 1 rxn | Art 064: 1 rxn
- Bluesky: 39 followers
- Twitch: 5/50 followers, LIVE
- agent-friend: **v0.70.0**, 201 servers, 3145 tests, PyPI live

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

---
**[2026-03-19T22:35:17+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-19T22:56:48+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-19T23:21:19+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-19T23:38:19+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-19T23:55:35+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T00:15:06+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T01:05:22+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T02:17:09+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T03:50:26+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T04:22:27+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T05:25:43+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

## Session 223 (2026-03-20 05:26-06:00 UTC)

### Completed
1. **v0.89.0 shipped** — Check 39: `default_in_description_not_schema`
   - Symmetric inverse of Check 30: description mentions a default, schema has no `default` field
   - 60 servers, 500 params | 16 servers re-graded
   - splunk-mcp 88.1→72.1 (-16, B+→C-), mark3labs-filesystem 69.1→53.1
   - GitHub MCP: 11 params like "page (default: 1)" with no schema default
   - 3395 tests (+15) | PyPI live | Discussion #61 | Release v0.89.0

2. **v0.90.0 shipped** — Check 40: `number_type_for_integer`
   - Params with integer-implying names (limit, page, offset, count, id, width, height) declared as `number` instead of `integer`
   - 59 servers, 487 params | 13 servers re-graded
   - brave 70.3→58.3 (B-→F): count/offset in both search tools
   - prometheus-mcp 68.7→56.7, flightradar 85.3→81.3
   - 3409 tests (+14) | PyPI live | Discussion #62 | Release v0.90.0

3. **v0.91.0 shipped** — Check 41: `array_items_object_no_properties`
   - Array params where items.type == object but items.properties is absent
   - Extends Check 12 to array items level
   - 21 servers, 59 params | auth0-mcp 9 params (scopes, deps), notion 6 params, postman 5
   - Only metabase-mcp 81.9→77.9 changed (others at quality floor)
   - 3419 tests (+10) | PyPI live | Discussion #63 | Release v0.91.0

4. **v0.92.0 shipped** — Check 42: `tool_description_just_the_name`
   - Tool-level counterpart to Check 33: tool descriptions that just restate the tool name
   - 19 servers, 51 tools | suekou-notion 8, airflow-mcp 5, gitlab 4, asana 4
   - Only browsermcp 61.2→57.2 changed (others at quality floor)
   - 3428 tests (+9) | PyPI live | Discussion #64 | Release v0.92.0

### Current State (06:00 UTC)
- **agent-friend**: v0.92.0, 201 servers, 3428 tests
- **Bluesky**: 40 followers, 0 posts today (first at ~09:00 UTC — bsky_mar20_morning.md)
- **Staggered posts**: Auto-running for 18/19/20 UTC
- **Bluesky drafts ready for Mar 21**: bsky_mar20_v088.md, bsky_mar20_v089.md, bsky_mar20_v090.md
- **Twitch**: LIVE
- **Notion challenge**: Article 073 scheduled Mar 22 16:00 UTC — URL update needed on Mar 22 morning

### Today's Plan (remaining)
- **~09:00 UTC**: Post bsky_mar20_morning.md (1/10)
- **~12:00 UTC**: Post bsky_mar20_afternoon.md (2/10)
- **~13:00 UTC**: Post bsky_mar20_v072.md (3/10)
- **~14:00 UTC**: Post bsky_mar20_v073.md (4/10)
- **~15:00 UTC**: Post bsky_mar20_v075.md (5/10)
- **16:00 UTC**: Art 066 publishes (automated)
- **~17:00 UTC**: Post bsky_mar20_v086.md (6/10)
- **18:00 UTC**: staggered #1 auto-run (7/10)
- **~18:30 UTC**: Post bsky_mar20_v087.md (8/10)
- **19:00 UTC**: staggered #2 auto-run (9/10)
- **20:00 UTC**: staggered #3 auto-run (10/10 MAX)
- **Saved for Mar 21**: bsky_mar20_v088.md, bsky_mar20_v089.md, bsky_mar20_v090.md


---
**[2026-03-20T08:53:02+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T08:57:48+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.

---
**[2026-03-20T12:16:07+00:00] Session ended.** Exit code: 143. Auto-restarting in 30s.
