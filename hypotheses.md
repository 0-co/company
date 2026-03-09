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
Status: `testing` (discovery phase — UPGRADED to second priority)
Added: 2026-03-08 | Updated: 2026-03-09 (EV revised upward, Opsgenie timing discovered)

> **I believe** engineering teams (20-500 engineers) **will pay $1,000-3,000/month** for automated incident remediation **because** on-call engineers receive 2,000+ alerts/week but only 3% require human action — and the only standalone autonomous runbook SaaS (Shoreline.io) was acquired by Nvidia and removed from market, leaving 100,000+ Opsgenie refugees actively evaluating alternatives through 2027.

**Evidence (updated March 2026):**
- 2,000+ alerts/week per team; only 3% need human action (incident.io, 2025)
- Shoreline.io acquired by Nvidia for ~$100M July 2024 — direct product validation, now gone
- Opsgenie shutdown: new sales ended June 2025, full shutdown April 2027 — FORCED MIGRATION
- incident.io raised $62M April 2025 for "AI agents that resolve incidents"
- Datadog Bits AI SRE launched December 2025 — but ecosystem-locked
- PagerDuty runbook automation: $125/user/month, still requires human trigger
- On-call standby pay: $540/week/engineer — direct cost automation replaces
- Average on-call team (10 engineers) costs $280k/year just in standby compensation

**True when:** 5+ on-call engineers confirm major pain + 2+ express willingness to pay $500+/month.
**False when:** "Datadog Bits already solves this" OR trust barrier proves absolute.

**Expected value (revised):**
- Near-term: 20 teams × $500/month = $10k MRR × 10% = **$1k/month EV**
- Long-term: 500 teams × $2,000/month = $1M MRR × 5% = **$50k/month EV**
- Timing: Opsgenie migration wave is unique window through April 2027

Key assumptions: (1) teams will whitelist "safe remediations" to enable automation (bypasses trust problem), (2) can integrate with Kubernetes/AWS/PagerDuty without 12-month build, (3) Datadog doesn't win market before entry.

**Riskiest assumption:** Can a team go from "zero automation" to "AI restarts pods automatically" in under 30 minutes? Test via discovery calls before building anything.

**Entry wedge:** Opsgenie refugees. "Drop-in replacement with autonomous remediation built in."

**Budget:** $0 until first customer interest.
**Deadline:** 2026-03-22 (need Discord/Twitch for discovery calls — blocked on board).

---

## Validated
*None*

## Invalidated
*None*

## Abandoned
*None*

---

### H4 — Problem: AI Agents in Production Are Unreliable and Hard to Monitor
Status: `testing` (discovery phase — emerging opportunity)
Added: 2026-03-09

> **I believe** teams deploying AI agents in production **are frustrated** because agents fail silently, behave inconsistently, and are expensive to run — but current observability tools (Langfuse, Arize, Braintrust) are designed for ML model metrics, not operational reliability and automatic recovery.

**Signal from market:**
- Reddit: "The AI gold rush isn't building agents. It is babysitting them." (r/Entrepreneurs, 2026-03-09)
- Reddit: "How are you managing AI agent config sprawl? The multi-tool context problem." (r/VibeCodeDevs)
- HN trend: "AI agents failing silently or just lying is a big problem" (from H3 research)
- 0-co IS this problem — we run AI agents in production and experience this firsthand

**True when:** 5+ AI developers describe this as "major pain" and 2+ express willingness to pay $200+/month for reliable agent ops tooling.
**False when:** "LangSmith/Langfuse already handles this" or "we just restart them manually, not a big deal."

**Expected value:** 
- 500 AI engineering teams × $300/month = $150k MRR × 8% = **$12k/month EV**
- Timing: AI agent adoption is accelerating rapidly (2025-2026 peak build phase)
- Unique angle: we run AI agents ourselves, we KNOW the problem from the inside

Key assumptions: (1) teams want reliability automation, not just metrics, (2) the "agent ops" category is real and distinct from ML observability, (3) price point is right for tooling vs. DIY.

**Riskiest assumption:** Does the reliability problem require a platform, or is it solvable with better LLM prompting and retry logic? Discovery calls needed first.

**Budget:** $0. **Deadline:** 2026-04-01 (discovery phase — need Discord/Twitch for customer conversations).

**Note:** This overlaps with H3 (on-call automation) but focuses on AI-specific failures vs. general infra incidents. Could be a module within AutoPage or a standalone product.
