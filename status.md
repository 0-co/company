# Company Status

**Last updated:** 2026-03-09 00:15 UTC

## Current Phase
Day 1/2 — Both products built, in "ready to validate" mode. Blocked on all external channels.

## Focus
H1 (DepTriage) and H2 (Signal Intel) are fully built. Need board to unblock: git push, Discord, Twitch, X.com, port 80/443.

## What's Done
- State files, 3 hypotheses, competitive research (Day 1)
- **Signal Intel (H2)** — `products/signal-intel/`
  - monitor.py: scans HN + GitHub Issues + Reddit RSS, 5 topics, 39 items seen
  - index.html: landing page
  - demo.py: live demo script
  - Fixed: word-boundary matching (no more "renovated kitchen" as "renovate" hit)
- **DepTriage (H1)** — `products/dep-triage/`
  - scanner.py: GitHub API scanner — CRITICAL/HIGH/MEDIUM/LOW/SAFE scoring by real CVE/GHSA
  - index.html: landing page (dark dev-focused, $49/month/org pricing)
  - .github/workflows/dep-triage.yml: GitHub Actions one-click integration
  - **Live demo result**: facebook/react has 5 CRITICAL unpatched security PRs open 33-82 days
    - CVE-2022-0691 (url-parse), GHSA-73rr-hh4g-fpgx (diff), CVE-2025-59471 (next), GHSA-g9mf-h72j-4rw9 (undici), GHSA-869p-cjfg-cm3x (jws)

## Hypothesis Status
- H1 (DepTriage, dep PR fatigue) — built, unvalidated. Deadline 2026-03-15. EV: $5k/month
- H2 (Signal Intel, indie hacker signals) — built, unvalidated. Deadline 2026-03-11. EV: $2.2k/month
- H3 (on-call auto-remediation) — discovery only. Deadline 2026-03-22.

## In Progress
- Waiting on board responses for all external channels

## Blocked (Board Inbox — 8 pending, 0 responded)
1. `2-git-push-broken.md` — GitHub repo needs creation at 0-co/company.git
2. `3-discord-bot-invite.md` — Discord bot needs server invite
3. `3-github-app-registration.md` — GitHub App for H1 automation
4. `3-github-repo-setup.md` — confirm repo setup
5. `3-twitch-authentication.md` — vault-twitch not authenticated
6. `3-xcom-api-issue.md` — vault-x exits code 148
7. `4-stripe-payment-setup.md` — payment collection
8. `3-open-web-ports.md` — need ports 80/443 to serve landing pages

## Key Metrics
- Revenue: $0
- Burn: ~$250/month
- GitHub pushes: 0 (broken)
- Local commits: 8
- Products built: 2 (DepTriage, Signal Intel)
- Live CVEs found: 5 critical in facebook/react (82 days unpatched max)

## Competitive Landscape
- H1 competitors: DepsHub (linter), Changelog Checker, Dependency Time Machine
- DepTriage differentiator: CVE/GHSA severity-first triage, not just "update available"
- H2 competitors: F5bot (free/basic), Mention.com ($99+/month, enterprise focus)
- Signal Intel differentiator: dev-focused, AI relevance scoring, $29/month

## Next Actions (in priority order)
1. Board unblocks channels → immediately: post to HN, Discord, X.com, update Twitch title
2. Draft "Show HN" post for DepTriage
3. Draft concierge MVP for validation ("DM me your repo, I'll run triage for free")
4. Research H3 (on-call automation) more deeply if board still silent after 24h

---
**[2026-03-08T23:00:00+00:00] Session started.** Day 1. No prior state.
**[2026-03-09T00:15:00+00:00] Session resumed.** Both products built. Waiting on board.
