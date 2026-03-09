# Hypotheses

## Format
> **I believe** [segment] **will** [action] **for** [solution] **because** [evidence].
> **True when** [signal] **within** [timeframe]. **False when** [signal] **within** [timeframe].
> **Expected value:** [EV estimate]. Key assumptions: [list].
> **Budget:** [max spend]. **Deadline:** [evaluation date].

---

## Active Hypotheses

### H1 — Problem: Dependency PR Fatigue Is a Security Liability
Status: `testing` (demand validation pending)
Added: 2026-03-08

> **I believe** development teams using GitHub **suffer** from unmanaged dependency PR queues **because** Dependabot/Renovate generate noise (100+ PRs/month) that teams can't review, so real security patches get ignored alongside irrelevant version bumps — leading to 60%+ of exploitable CVEs sitting patched-but-undeployed for months.

**Evidence:**
- Vulnerability volume grew 10x from late 2024 to mid-2025 (OX Security)
- 60% of known-exploited CVEs had patches available for months before exploitation
- Only 21% of organizations have complete dependency visibility
- Dependabot/Renovate create PRs but don't triage by criticality or safety

**True when:** 10+ sign-ups for waitlist within 5 days of landing page launch, or 3+ teams express intent to pay.
**False when:** <3 sign-ups after 5 days, or consistent feedback that "we already handle this fine."

**Expected value:** 1000 teams × $50/month = $50k MRR × 10% probability = **$5k/month EV**
Key assumptions: (1) teams are actually blocked by this (not just ignoring it), (2) they'll trust auto-merge for "safe" deps, (3) GitHub won't natively solve this soon.

**Budget:** $0 (code + GitHub App only; App registration via board).
**Deadline:** 2026-03-15 (1 week demand test after landing page ships).

**Riskiest assumption:** Teams will trust an AI to classify which PRs are safe to auto-merge. Test first: "would you pay $50/month to know which dep PRs to merge today?" before building auto-merge.

---

### H2 — Problem: Indie Hackers Miss Relevant Conversations 24/7
Status: `testing` (demand validation pending)
Added: 2026-03-08

> **I believe** indie hackers and solo founders **miss** customer discovery opportunities and market signals **because** no person can monitor Reddit, HN, Discord, and GitHub Issues 24/7 for relevant threads. Existing tools (F5bot: free/basic, Mention.com: $99+/generic) don't serve this audience.

**Evidence:**
- Solo founders lose momentum waiting for async help (documented pattern in indie hacker surveys)
- F5bot is keyword-only, Reddit-only, no AI relevance scoring
- Mention/Brand24 cost $99-299/month and are aimed at marketing teams, not developers
- METR study: developers 19% slower due to context-switching overhead — real-time signals would help prioritize

**True when:** 15+ Discord/Twitch viewers indicate interest via "hell yes" reactions or waitlist sign-ups within 48 hours of demo, or 3+ people willing to pay $29+/month.
**False when:** <5 positive responses after a live demo + Discord pitch.

**Expected value:** 500 users × $29/month = $14.5k MRR × 15% probability = **$2.2k/month EV**
Key assumptions: (1) developers will pay for signal monitoring vs. just using free tools, (2) AI relevance scoring is meaningfully better than keyword alerts, (3) sufficient audience exists (indie hackers are tool-hungry, many at $10k+ MRR).

**Budget:** $0 (Reddit free API + HN Algolia API + Discord monitoring — no paid API needed for MVP).
**Deadline:** 2026-03-15 (extended from 2026-03-11; distribution blocked until Bluesky activated on March 9).

**Riskiest assumption:** Developers will pay for this vs. using free alternatives. Test: offer a live demo on Twitch stream ("I'm monitoring these 3 topics for you right now") and see if viewers want it for themselves.

---

### H4 — Problem: AI Agents in Production Are Unreliable and Hard to Monitor
Status: `testing` (discovery — 10+ pain signals confirmed, 0 willing-to-pay confirmed)
Added: 2026-03-09

> **I believe** teams deploying AI agents in production **are frustrated** because agents fail silently (exit-0 with empty output), behave inconsistently over time (behavioral drift), and run up unexpected costs — but current observability tools (Langfuse, Arize, Braintrust) focus on ML model metrics, not operational reliability.

**Pain signals confirmed (10+):**
- @ultrathink-art: 23% of tasks silently skipped, built DIY output validation. Pricing probe sent ($20-50/month?).
- @profesordragan: "0 rows returned" silent for hours
- @joozio: unattended ≠ unsupervised — escalation boundaries problem
- @vaultscaler: architecture-level enforcement, "fails safely > goes wrong quietly"
- @anixlynch: 3AM pages from agent failures
- @jasongorman: Cursor 89% build failure rate, they just kept going
- @nik-kale: 33 agents in production, first rogue agent
- @timzinin: 6 agents developing "survival patterns"
- @genesisclaw: 3 memory failure modes
- @talk-nerdyto-me: $47K cost loop
- @kaperskyguru: $400 overnight loop
- @kloudysky.io (2026-03-09): "confirmed pain, unconfirmed WTP" — asked about specific failure mode

**True when:** 5 teams express willingness to pay $20-50/month for production agent monitoring.
**False when:** "LangSmith/Langfuse already handles this" OR consistent "we just restart manually, NBD."

**Expected value:** 500 teams × $50/month = $25k MRR × 8% probability = **$12k/month EV**

**Competitor landscape:** Firetiger (Sequoia, enterprise), TracePact (pre-prod testing, different job). AgentWatch = indie/small team production monitoring gap.

**Budget:** $0. **Deadline:** 2026-04-01.

---

## Validated
*None*

## Invalidated
*None*

## Abandoned

### H3 — On-Call Engineers Are Paged for Self-Healable Incidents
Status: `abandoned` — Board mandate 2026-03-09
Added: 2026-03-08 | Abandoned: 2026-03-09

Board: "Please abandon the opsgenie replacement approach. This is just a deprecated tool that already has official replacements. In future please remember to do more robust market research and competitor analysis. In this case you would have found that alternatives already existed and the TAM is tiny."

**Lesson:** Opsgenie has official replacements (Atlassian JSM, PagerDuty, Grafana OnCall). The 100k+ migration number was the total market, not the unserved segment. EV was overestimated by conflating "large migration event" with "unserved niche." Do competitor analysis BEFORE writing EV estimates.

**What to do differently next time:**
1. Search "alternatives to [product]" before writing hypothesis
2. Validate addressable segment (not just total market) with 2 real customers first
3. Don't build EV estimate until you've confirmed what alternatives exist

---

