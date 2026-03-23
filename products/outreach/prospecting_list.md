# Cold Outreach Prospecting List

**REVISED STRATEGY (2026-03-22):** Based on market research, individual developer $200 audits are the wrong model. Real money comes from enterprise sponsorships ($5K-$15K/year) from companies who have F-grade servers on our PUBLIC leaderboard — reputational risk = payment motive.

Reference: trunk.io pays ESLint $7K/year to sponsor the tool that their product wraps.

**Goal:** 5-10 cold emails over 10 days, targeting large companies with F-grade servers
**Rate:** 1 cold outreach per day max
**Pitch:** "Your MCP server has a public F grade on a tool grading 201 servers. Here's exactly why. We can show you the path to A+. And here's why being an early sponsor matters."
**Ask for now:** A conversation about their MCP quality strategy. Not money yet. Build the relationship.
**Revenue from:** Enterprise sponsorship ($5K-$15K/year) once trust is established.

---

## Priority Targets

### 1. Sentry (sentry-official: 0.0/100)
- **Contact:** David Cramer (@dcramer) — co-founder, 766 commits on sentry-mcp
- **Why:** 606-star MCP server, 0.0 grade. Sentry = developer tool company that cares about quality. David is technical and opinionated.
- **Angle:** "Your observability tool has zero observability from an agent's perspective." Irony is the hook.
- **Goal:** Not payment — public engagement. If Cramer tweets about it = massive exposure.
- **Find email:** Sentry blog, getsentry.com about page, @dcramer on HN
- **Send:** March 24 (after Show HN results settle)

### 2. Browserbase (score ~41.6/100, D)
- **Contact:** Find MCP server maintainer on GitHub
- **Why:** Browser automation company, MCP is central to their developer product. Lower score = more impact.
- **Angle:** Token efficiency matters more for browser automation because each tool call description burns context that could be used for page understanding.
- **Goal:** Could become a paid customer for monitoring (their MCP server is their product)
- **Find email:** GitHub repo contributors
- **Send:** March 25

### 3. Cloudflare (11.4/100, F)
- **Contact:** MCP team — search GitHub contributors for cloudflare-mcp
- **Why:** 11.4/100 is embarrassingly bad for a company with a strong developer brand. "Cloudflare MCP: 11.4/100" is a headline they'd want to fix.
- **Angle:** Token bloat is especially bad for edge computing use cases (tight context budgets). Cloudflare developers care about efficiency.
- **Goal:** Might be too large for paid audit but could generate buzz if they publicly fix the score.
- **Send:** March 26

### 4. Any YC-backed company with a bad MCP server
- **Find:** Search YC directory for companies that mention MCP, search GitHub for their MCP servers
- **Why:** YC companies move fast, care about developer experience, have budget, decision-maker = founder
- **Target criteria:** F or D grade, <50 employees, MCP is part of their product
- **Send:** March 27-31

### 5. Agent-social (mchtshn1 — starred agent-friend, building MCP-native platform)
- **Contact:** @mchtshn1 on GitHub (Turkish developer, very recent project)
- **Why:** Already a warm contact (starred us). Building a product that will use many MCP servers. Perfect target for "grade your servers before launch."
- **Angle:** Not a sales pitch — a conversation. "I noticed you starred agent-friend — are you grading the servers you integrate with? Happy to walk through what good looks like."
- **Goal:** Customer development conversation, not immediate payment.
- **Send:** March 27

---

### 6. Cloudflare (mcp-server-cloudflare: 11.4/100, 3,560 stars)
- **Contact:** Glen Maddern (@geelen on GitHub/X) — Principal Systems Engineer, 48 commits, co-creator of the repo. LinkedIn: linkedin.com/in/glenmaddern/. Email likely: glen.maddern@cloudflare.com
- **Why special:** Cloudflare built TWO MCP servers: `mcp-server-cloudflare` (3,560 stars, 11.4/100 = F) and `mcp` (280 stars, explicitly token-efficient, "2,500 endpoints in 1K tokens via Code Mode"). They KNOW about the problem — they built an alternative solution. But 3,560 developers are using the bad one.
- **Angle:** "You built the efficient version. But 3,500 people are on the 11.4/100 version. The people who star `cloudflare/mcp` are the ones who found the problem. The people who star `cloudflare/mcp-server-cloudflare` haven't found it yet."
- **Send:** March 27
- **Blog:** blog.cloudflare.com/author/glen/

## Research Needed
- Find contact emails/socials for each target's MCP team lead
- Grade their servers with latest agent-friend (some scores may be outdated)
- Prepare personalized report for each (3-5 specific issues from their schema)

## Template Logic
Effective cold email = specific data + clear insight + low-friction ask

Bad: "Your MCP server has schema quality issues. Would you like an audit?"
Good: "Your MCP server's description for `browser_navigate` starts with 'This tool allows you to' — that's 5 wasted tokens per tool call. At 1,000 AI calls/day, that's $0.06/day in unnecessary API costs. Your full schema burns 8,420 tokens before the first message — 184x the sqlite MCP server. 10-minute fix: https://github.com/0-co/agent-friend#fix"

The good version shows I've actually looked at their specific schema and quantified the cost. Takes 5 minutes per target but converts much better.

## Tracking
| Date | Target | Sent | Response | Outcome |
|------|--------|------|----------|---------|
| Mar 24 | Sentry/dcramer | TBD | - | - |
