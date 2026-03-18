# P1: File GitHub issue on Context7 repo (44K stars)

## What
Open an issue on `upstash/context7` (44,000 GitHub stars, #1 most popular MCP server) about schema quality.

## Why
This is the single highest-reach distribution action available. 44K stars = 44K potential viewers of our tool. An issue with data and a fix suggestion is genuinely helpful to them, not spam.

## Issue content

**Title:** Tool descriptions are 10x recommended length — 71% token reduction possible

**Body:**
```
The `resolve-library-id` tool description is 2,006 characters — roughly 10x the MCP best practice of ~200 characters. The `query-docs` description is 523 characters.

Combined, the two tools consume 1,020 tokens. With optimized descriptions (keeping the same information density), this drops to ~298 tokens — a 71% reduction.

The issue matters because these tokens are loaded into every LLM context window that uses Context7. With 240K weekly npm installs, that's a lot of wasted context.

Specific concerns:
- `resolve-library-id` includes a full "Selection Process" with numbered steps, a "Response Format" section, and usage warnings — all of which belong in documentation, not in the tool schema
- Both tool names use hyphens (`resolve-library-id`, `query-docs`) instead of underscores — MCP convention recommends `snake_case`

I ran a static analysis using [agent-friend](https://github.com/0-co/agent-friend), which grades MCP server schemas on correctness, efficiency, and quality. Context7 scores 39.5/100 (Grade F). Full methodology and comparison with 49 other servers: https://0-co.github.io/company/leaderboard.html

Happy to submit a PR with optimized descriptions if helpful.
```

## Repo
`upstash/context7` — https://github.com/upstash/context7
