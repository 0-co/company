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

### H3 — Problem: On-Call Engineers Are Paged for Self-Healable Incidents
Status: `testing` (discovery phase — UPGRADED to second priority)
Added: 2026-03-08 | Updated: 2026-03-09 (deep market research completed)

> **I believe** engineering teams (20-500 engineers) **will pay $500-2,000/month** for autonomous incident remediation **because** (a) on-call engineers receive 2,000+ alerts/week but only 3% require human action, and (b) the only standalone autonomous runbook SaaS (Shoreline.io) was acquired by Nvidia and removed from market, leaving 100,000+ Opsgenie refugees with no clean replacement and a hard April 2027 shutdown deadline forcing them to choose now.

**Evidence (deep research 2026-03-09):**
- 2,000+ alerts/week per team; only 3% need human action (incident.io, 2025)
- Shoreline.io acquired by Nvidia for ~$100M July 2024 — category validation, now gone
- Opsgenie shutdown: new sales ended June 2025, full shutdown April 2027 — FORCED MIGRATION
- Opsgenie users paid $9-11/user/month; current alternatives cost $25-90 (2-8x more)
- Atlassian Community thread "Replacement for Opsgenie" has LIVE active intent RIGHT NOW
  - Users say: "we don't need any other features of JSM, we just need to replace Opsgenie"
  - Users say: "trapped" — JSM + Compass fragments what was one tool into two expensive products
- NeuBird customers: 230,000 alerts resolved autonomously, saving $1.8M/year engineering time
- Lightrun AI SRE: launched Feb 2026 — space is moving fast
- Datadog Bits AI SRE: AWS-only, ecosystem-locked
- On-call standby pay: $540/week/engineer; 10-engineer team = $280k/year just in standby
- Most tools: read-only "suggestions"; none taking actual autonomous production actions

**True when:** 5+ on-call engineers confirm major pain + 2+ express willingness to pay $500+/month.
**False when:** "Datadog Bits already solves this for our infra" OR "trust barrier is absolute — nobody will let AI touch prod."

**Expected value (updated after research):**
- Near-term SMB (300 teams × $299/month = $89.7k MRR × 8% = **$7.2k/month EV**)
- Long-term enterprise (50 teams × $2,500/month × 5% = **$6.25k/month EV**)
- Total revised EV: **~$13.5k/month** (up from $50k long-term only)

Key assumptions: (1) pre-approved runbook list ("safe remediations") bypasses the trust barrier, (2) 30-min integration with Kubernetes/PagerDuty/AWS is feasible, (3) Opsgenie refugees are price-sensitive and respond to flat-rate pricing.

**Riskiest assumption:** Can a team go from "zero automation" to "AI restarts pods automatically" in < 30 minutes? Must test via discovery calls before building.

**Entry wedge:** Opsgenie refugees actively evaluating now. "Drop-in replacement + autonomous remediation built in. Flat rate, not per-user."

**Customer discovery opportunities found:**
1. Atlassian Community: community.atlassian.com/forums/Jira-Service-Management/Replacement-for-Opsgenie/qaq-p/2967670
2. Reddit: r/devops, r/sre (search "opsgenie" for live threads)
3. CNCF Slack: #sre, #incident-management channels
4. Grafana Labs Discord (OnCall migration channel)

**Budget:** $0 until first customer interest.
**Deadline:** 2026-03-22 (need to engage with communities above for discovery calls).

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
