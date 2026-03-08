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
**Deadline:** 2026-03-11 (72-hour demand test once Discord bot is active and Twitch stream is running).

**Riskiest assumption:** Developers will pay for this vs. using free alternatives. Test: offer a live demo on Twitch stream ("I'm monitoring these 3 topics for you right now") and see if viewers want it for themselves.

---

### H3 — Problem: On-Call Engineers Are Paged for Self-Healable Incidents
Status: `testing` (demand validation pending, lower priority)
Added: 2026-03-08

> **I believe** on-call engineers at software companies **are burned out** because 95%+ of alerts they receive should be auto-resolved by executing a known runbook, but current tools (PagerDuty, Opsgenie) only route alerts — they don't execute remediation. Real incidents become noise in a sea of false positives.

**Evidence:**
- Average on-call engineer receives ~50 alerts/week; only 2-5% require human action
- 53% of security alerts are false positives
- 77-80% MTTR reduction when runbook automation is applied (PagerDuty + AIOps data)
- "Alert fatigue is killing your on-call team" — March 2026 post, 200+ comments

**True when:** 5+ on-call engineers describe this as "major pain" and 2+ express willingness to pay $200+/month in discovery conversations.
**False when:** Consistently hear "we handle this fine with existing tools" or "trust issues prevent automation."

**Expected value:** 200 teams × $200/month = $40k MRR × 5% probability = **$2k/month EV**
Key assumptions: (1) teams will trust AI to execute runbooks automatically, (2) integration complexity is solvable.

**Budget:** $0.
**Deadline:** 2026-03-22 (2-week discovery phase — talk to 5 on-call engineers before building anything).

**Riskiest assumption:** Trust. Auto-remediation in production requires high trust. Start with "read-only + suggest" mode and escalate to auto-execute only after trust is built. Test this assumption first.

---

## Validated
*None*

## Invalidated
*None*

## Abandoned
*None*
