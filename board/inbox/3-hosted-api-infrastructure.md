# Hosted API Infrastructure — P3

## Context
The REST API is already running locally at `http://89.167.39.157:8082` as a systemd service. It works. But a raw IP is not a real product.

Show HN fires tomorrow (March 23 14:00 UTC). If it generates demand signal (Discussion #188 gets responses, people ask about hosted version in HN comments), I want to move fast.

## What I need
1. **Domain**: `agent-friend.dev` or `api.agent-friend.dev` — whichever is available/cheapest. Even a subdomain of existing would work.

2. **Stripe account**: For processing subscription payments ($10-50/month tiers). Or if there's a simpler option, Open Collective would work for a donation-style model. Just need something where a developer can click "pay" and money arrives.

3. **Optional (priority 4)**: A $7/month render.com or fly.io instance to run a publicly-branded version of the API (vs the raw IP). Not strictly required — the current server works fine on the raw IP.

## When to act
**After Show HN results (March 23 17:00 UTC):**
- If ≥3 people express interest in hosted/paid version → act on items 1+2 immediately
- If 0-2 people express interest → still do items 1+2 eventually, but not urgent
- If Show HN flops → defer until next distribution event

## Revenue potential
25 customers at $10/month = $250/month (break-even). At 969 GitHub cloners with real conversion, even 0.3% conversion = 3 paying customers = $30/month. Better than $0.

This doesn't require board to build anything — I'll build the hosted service using the existing `api_server.py` and extend it with auth/rate-limiting/webhooks. The board just needs to provision domain + payment processing.
