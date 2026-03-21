# MCP Distribution Channel Research
**Date:** 2026-03-21 | **Session:** 223d

## Key Finding
The token bloat pain is documented and quantified across major publications (The New Stack, Glama, InfoQ) but **NO article mentions build-time schema quality grading as the solution.** That gap is our pitch.

Key evidence:
- Glama Engineering Blog: "Standard MCP setups consume 72% of agent context before work begins"
- The New Stack (Feb 2026): "10 strategies to reduce MCP token bloat" — zero mention of build-time tools
- RAG-MCP research: Tool selection accuracy collapsed 43% → 14% in bloated setups
- HN #47137855 (Feb 2026): "performance degrades exponentially once you exceed 15-20 tools"

## Priority Distribution Channels

### Tier 1 — Act Now

**Frank Fiegel (@punkpeye on X)**
- Runs: Glama.ai, r/mcp, awesome-mcp-servers (83K stars), awesome-mcp-devtools (436 stars)
- We have a Glama listing = WARM contact. Forked agent-friend on March 17.
- awesome-mcp-devtools = perfect fit ("developer tools for MCP server development")
- Board request filed: `2-awesome-mcp-servers-listing.md` — updated to include both repos
- NOT on Bluesky. Only contactable via X (read-only for us) or GitHub.

**r/mcp (founded by Frank Fiegel)**
- Direct MCP builder community. "We graded 200 MCP servers A+ to F" = top-of-subreddit material
- Waiting on Reddit account (board request pending: `2-reddit-session.md`)

**The New Stack — contributed post opportunity**
- Published "10 strategies to reduce MCP token bloat" (Feb 2026) — no mention of us
- Our angle: "The real fix for MCP token bloat: build-time schema quality"
- They have contributor guidelines at thenewstack.io
- HIGH priority distribution opportunity (reaches 2M+ developers)
- NOTE: Board directive says stop writing articles (pipeline full). But this is a DIFFERENT publication with much larger reach. May be worth an exception.

### Tier 1 — Waiting on Board

**r/LocalLLaMA (91K members) + r/LLMDevs (125K) + r/AIAgents (212K)**
- Token cost angle fits perfectly
- Board request: `2-reddit-session.md` (pending)

**MCP Official Discord — get MCP server authors role**
- Already posted. Not in server-authors private channels yet.
- Getting "mcp-server-authors" flair unlocks private builder channels.

### Tier 2 — Medium Lift

**Matt Pocock (@mattpocockuk on X)**
- Published 10-lesson MCP tutorial — audience just built their first MCP server
- Perfect product-fit moment: "here's how to grade it before shipping"
- Read-only on X ($100/month to post)

**TLDR AI (1.6M readers)**
- Curators pull from Dev.to trending + HN
- Organic pickup path: strong viral article → TLDR coverage

**Latent Space (200K subscribers)**
- Write-for-us form at latent.space/about
- Give 1 month lead time
- Angle: "token smell taxonomy — 149 checks, what the worst-grade servers have in common"

**System Design Newsletter**
- Published MCP deep dive (issue #110)
- Weekly, technical depth, developer audience

### Tier 3 — Viral Triggers

**Fireship (3.5M YouTube)**
- Sources ideas from HN trending and Reddit
- Cannot pitch directly — need viral post first

**Theo Browne / t3dotgg (492K YouTube)**
- TypeScript schema quality audience
- Angle: "your MCP schema is doing to context what untyped JS does to type safety"

## Warm Contacts Confirmed on Bluesky

| Handle | Who | Status |
|---|---|---|
| @daniel-davia.bsky.social | safe-mcp.com founder | Reply drafted for March 22 |
| @zzstoatzz.io | fastmcp contributor (PrefectHQ) | Post drafted for March 25 |
| @aroussi.com | context-as-budget framing | Previous mention |

## Sources

- The New Stack: https://thenewstack.io/how-to-reduce-mcp-token-bloat/
- Glama blog: https://glama.ai/blog/2025-12-16-what-is-context-bloat-in-mcp
- HN thread: https://news.ycombinator.com/item?id=47137855
- awesome-mcp-devtools: https://github.com/punkpeye/awesome-mcp-devtools
- Latent Space about: https://www.latent.space/about
- Matt Pocock MCP tutorial: x.com/mattpocockuk/status/1900614069561766179
