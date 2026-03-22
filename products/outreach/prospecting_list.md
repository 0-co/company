# Cold Outreach Prospecting List

**Goal:** 10 cold emails over 10 days, targeting companies with F/D-grade MCP servers
**Rate:** 1 cold outreach per day max
**Pitch:** "Your MCP server scores X/100 — here's the specific issues and what fixing them would do for your users' context window."
**Ask:** Not immediate payment — get them talking. Revenue comes from: (a) they hire us for a fix audit, (b) they subscribe to monitoring, (c) they become a case study

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
