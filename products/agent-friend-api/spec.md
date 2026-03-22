# agent-friend API Service — Product Spec

## Problem
The CLI tool is free and open source. There's no reason to pay. The monetization gap requires a hosted service that does something the CLI can't or makes it significantly easier.

## What a hosted service enables
1. **No installation**: paste your schema URL, get a grade in 30 seconds. Zero friction.
2. **CI webhook**: POST your schema to an endpoint from your CI pipeline → get grade/pass/fail
3. **Schema drift monitoring**: submit your schema once, we check weekly, email you when scores drop
4. **Team dashboard**: grade multiple servers, track over time, share with teammates
5. **Grade badge**: `![agent-friend grade](https://api.agent-friend.dev/badge/github/owner/repo)`

## User segments and willingness to pay

**Segment A: Individual developers** — Won't pay. Use the free CLI. Not the target.

**Segment B: Teams building MCP servers** — Might pay for CI integration ($10-20/month).
- Pain: want automated grading without maintaining local CLI in each dev environment
- Jobs to be done: "make sure nobody ships a bad schema"

**Segment C: Companies with multiple MCP servers** — Will pay for monitoring ($50-100/month).
- Pain: MCP servers drift as they add features, quality degrades silently
- Jobs to be done: "know when our server regresses"

**Segment D: Enterprises building internal MCP tools** — Will pay for SLA/priority ($200+/month)
- Pain: need compliance/audit trail
- Jobs to be done: "prove to security team that our tool descriptions don't have prompt injection"

## MVP: What to build first

**Free tier (no auth required):**
- `GET /grade?url=<schema_url>` — fetch schema from URL, return grade JSON
- `POST /grade` — submit schema JSON, return grade JSON
- Rate limit: 10 requests/day per IP
- Powers the web tool at docs/report.html (which already exists!)

**Paid tier ($10/month, API key):**
- Unlimited grades via API
- CI badge endpoint
- Email alerts when grade drops below threshold
- 30-day history

**Premium tier ($50/month):**
- Multiple servers monitored
- Weekly digest email
- Grade badge for README
- Priority support

## Technical implementation
- Backend: Python FastAPI or Flask, minimal
- Hosting: render.com or fly.io (board to provision)
- Payment: Stripe (board to provision)
- Schema: same agent-friend logic, called as a library

## What needs board action
1. Domain: agent-friend.dev or similar (or subdomain of existing)
2. Hosting: render.com account + credit card (~$7/month for a basic instance)
3. Stripe: payment processing

## Build timeline
- Backend API: 1 session (already have the logic, just wrap in FastAPI)
- Stripe integration: 1 session (using existing pattern)
- Deploy + domain: 1 session

## Revenue model
Break-even ($250/month) requires:
- 25 paid tier ($10/month) customers, OR
- 5 premium tier ($50/month) customers, OR
- 1-2 premium + several paid

With Show HN tomorrow potentially bringing 500-2000 visitors:
- Conversion rate 0.5% to paid = 2-10 customers
- $20-100/month immediately

**This is the clearest path to breaking even.**

## Next step
File board request for domain + hosting after Show HN results are known.
If Show HN does well (>50 points): high confidence this pays off. Build immediately.
If Show HN flops: reconsider (demand signal is weak, rethink positioning).
