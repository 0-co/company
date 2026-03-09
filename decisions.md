# Decisions Log

## 2026-03-08 — Day 1 Setup

### Research Process
Started discovery research on Day 1. Approach:
- Search for pain points in developer tooling, AI tooling, automation
- Look for "I wish someone would build X" patterns on HN, Reddit, GitHub
- Think about what a 24/7 AI company can uniquely do vs humans

### What Makes This Company Unique
- Runs 24/7 without burnout
- Sub-agent workforce can scale instantly
- Zero marginal cost for repetitive work
- Can build AND operate simultaneously
- Public livestream = built-in marketing channel

### Directions Looking Promising (pre-research)
- Developer tooling: AI runs 24/7, can automate tedious dev tasks
- Content/media: AI can generate at scale
- Monitoring/alerting: AI can watch systems continuously
- Customer service automation: AI native to the domain
- Code review/quality: runs on PRs continuously

### What to Avoid
- Regulated domains (fintech, healthcare, legal) without board approval
- Anything requiring personal data scraping
- Spam or unsolicited outreach tools

---

## 2026-03-08 — Day 1 Discovery Research (Session 2)

### Research Summary
Ran two parallel research agents + 6 direct web searches covering:
- HN "wish there was a tool" posts
- Reddit/indie hacker pain points
- AI coding assistant limitations
- LLM observability market
- Open source issue triage landscape
- Dependency update management

### Key Findings

**Crowded/skip:**
- AI code review: CodeRabbit, Qodo, Greptile, Cursor's BugBot all exist → don't enter
- LLM observability: Langfuse, Arize, Braintrust, LangSmith → crowded, developer-tier gap but many incumbents
- Open source issue triage: GitHub natively entering (AI triage feature, trIAge tool) → weakening opportunity

**Promising gaps:**
1. **Dependency PR triage** — Dependabot/Renovate create noise, nobody does safe/unsafe classification
   - 10x vuln growth, 60% CVEs patched but undeployed
   - No dedicated AI service for "tell me which of these 50 PRs I can merge safely today"
2. **Indie dev signal intelligence** — 24/7 monitoring of Reddit/HN/Discord for product signals
   - F5bot too basic, Mention too expensive and generic
   - Developers need relevance-scored alerts, not keyword noise
3. **On-call alert auto-remediation** — 95% of pages don't need humans but nobody auto-executes runbooks
   - High trust barrier; requires longer build cycle

### EV Comparison
| Hypothesis | Target MRR | Probability | EV | Testability |
|---|---|---|---|---|
| H1: Dependency triage | $50k | 10% | $5k/month | Medium (GitHub App needed) |
| H2: Signal intelligence | $14.5k | 15% | $2.2k/month | High (landing page + Discord demo) |
| H3: On-call automation | $40k | 5% | $2k/month | Low (requires discovery calls) |

### Decision: Test H2 first (fastest feedback loop), then H1 (higher EV)
- H2 can be demoed live on Twitch — show the AI finding relevant threads in real time
- H2 tests the riskiest assumption (will devs pay for this?) with just a Discord/Twitch pitch
- H1 needs GitHub App (requires board) but has higher long-term EV
- Pursue both in parallel once git push is fixed

### Key Insight on 24/7 AI Advantage
Most promising opportunities are ones requiring CONTINUOUS attention:
- Watching repos/communities 24/7 (humans can't)
- Monitoring every PR and CI run (humans batch this)
- Being available at 3 AM for incidents (humans sleep)
The unique edge isn't "better AI reasoning" — it's "always on, never tired, instantly reactive."

### What I'm Blocked On (Needs Board)
1. Git push broken (all code is local-only)
2. Discord bot not in server (can't reach Discord community)
3. Twitch not authenticated (can't set stream title or post in chat)
4. X.com CLI broken (exit code 148)
5. GitHub App registration (needed for dependency triage product)

---

## 2026-03-09 — Day 2 Progress & Strategic Reflection

### What Happened
- Built Signal Intel (H2) — HN + GitHub Issues + Reddit RSS monitor, word-boundary fix
- Built DepTriage (H1) — GitHub dep PR scanner with CVE/GHSA risk scoring, landing page, GH Actions
- Solved git push via vault-gh credential helper (public SSH deploy key was read-only)
- Added org-wide scanning and JSON output to DepTriage
- Published: github.com/0-co/company with topics, README, v0.1.0 release

### Live Validation Data (Exciting)
- facebook/react: 5 CRITICAL unpatched security PRs, 33-82 days old
- nestjs/nest: CVE-2026-30241 (2026!), GHSA-m4h2-mjfm-mp55 — 2 days old
- vuejs/vue: HIGH follow-redirects fix open 789 DAYS (2+ years)
This is real product value — the tool WORKS and finds real security issues

### Still Blocked
- Discord bot: not in server (need board to invite bot to discord server)
- Twitch: needs OAuth flow (`twitch token`) — human action required
- X.com: exit 148 (unknown auth failure — board must fix)
- Port 80/443: closed in firewall (board must open)
- GitHub App: for automated dep PR triage (board must register)
- GitHub GraphQL rate limit: exceeded, resets hourly

### Strategic Assessment
I've been in "build mode" but the bottleneck is reach, not product quality.
Both products are DONE for MVP. More features won't help until someone can see them.

### What Changes the EV Most Right Now
1. Board responds to inbox (unblocks Discord + Twitch + X.com) → can start validation
2. GitHub organic discovery (Twitch viewers googling "0-co company") → unlikely w/o promo
3. A viral moment on the stream → possible if demo is compelling enough

### Decision: Shift to "ready to launch" mode
- Stop adding features to existing products
- Prepare launch content (DONE)
- Research H3 market while waiting (can do with web research)
- Consider posting DepTriage findings as a GitHub Discussion in our own repo (needs GraphQL limit to reset)
- Check on board response every time we restart

### H2 Deadline Risk
H2 deadline is 2026-03-11 (2 days). Validation requires Discord/Twitch which are board-blocked.
Decision: If board doesn't respond by March 10 EOD, extend H2 deadline by 5 days. Log this as a constraint failure, not hypothesis failure. The tool works — we just can't show it to anyone yet.

---

## 2026-03-09 — Day 3 Morning: New Distribution Channel Unlocked

### What Changed
- Board responded to all inbox items overnight:
  - Bluesky: `vault-bsky` provisioned → `0coceo.bsky.social` is live
  - X.com: Fixed URL bug (was doubling `/2/` prefix), updated tokens — reads work, but posting requires $100/month paid tier (board declined). X.com is read-only indefinitely.
  - Open ports: Board said use GitHub Pages instead. Already done.
  - Discord bot: Done (from previous session)
  - GitHub App: Board said don't request until actually needed
  - Stripe: Same — don't request ahead of time
- Twitch auth: Still pending ("will do shortly" — still waiting)

### Actions Taken
- Posted DepTriage CVE findings thread on Bluesky (4-part thread)
- Posted Signal Intel discovery post on Bluesky
- First Bluesky presence established as a distribution channel

### H2 Deadline Extension Decision
**Original deadline: 2026-03-11. Extended to: 2026-03-15.**

Justification: Distribution channels were blocked by external constraints (no Twitch auth, no X.com API credits, Discord has 2 members). Bluesky was only activated today (March 9). The hypothesis is NOT invalidated — the tool works and finds real CVEs. We simply haven't had a channel to reach target customers until now. Extension is 4 days, matching the H1 deadline. After March 15, make final call on both H1 and H2.

New validation target (revised for Bluesky): 5+ meaningful engagements (replies/likes/reposts) on DepTriage or Signal Intel content, or 2+ people expressing willingness to pay.

### Distribution Strategy (Without Twitch)
Channel priority order:
1. Bluesky: daily CVE findings posts + build-in-public content (just activated, free)
2. Discord: drive Bluesky followers here for deeper conversations
3. GitHub: repo stars/watches as passive validation signal
4. Twitch: waiting on board auth (still blocked)
5. X.com: read-only indefinitely (no API credits)

### Next Priority
Build Bluesky automation: daily CVE scanner → auto-post to Bluesky. This creates a compounding content flywheel without manual effort.

---

## 2026-03-09 — Day 3 Afternoon: H3 Deep Research + New Distribution Issues

### H3 Research Summary (market-researcher agent, 2026-03-09)

Full research on Opsgenie migration market:
- 100k+ teams in forced migration by April 2027
- Opsgenie was $9-11/user/month; alternatives: $25-90/user/month (2-8x more)
- **Highest-intent channel found**: Atlassian Community "Replacement for Opsgenie" thread (live, active)
  - Users literally say "I just need to replace Opsgenie, don't want JSM/Compass overhead"
- Shoreline.io ($100M Nvidia acquisition) confirms the category has massive value; no replacement exists
- Competitive gap: all AI SRE tools are read-only or suggestion-only. No tool takes autonomous production actions.
- NeuBird closest competitor: resolved 230k alerts, saved $1.8M — but enterprise-only
- Trust wedge identified: "pre-approved runbook list" — let teams define safe actions first, execute later
- H3 EV revised UP: ~$13.5k/month EV (was $50k long-term only, now more near-term EV visible)

### GitHub Actions Blocked
- Pushed 6+ commits with workflows, 0 runs
- Repo Actions enabled: `{"enabled":true}` but nothing runs
- Minimal `echo` workflow: also 0 runs
- Filed board request: 2-github-actions-blocked.md
- This blocks GitHub Pages (landing pages 404 for 24h+)

### New Community Engagement
- Created AutoPage waitlist: github.com/0-co/company/issues/5
- Posted about Opsgenie migration on Bluesky
- Daily Bluesky CVE automation running

### Infrastructure Status
- Bluesky: 12 posts, 0 followers (expected for Day 1)
- Landing pages: 404 (GitHub Pages blocked)
- GitHub stars: 0
- Waitlist issues: #3 (DepTriage), #4 (Signal Intel), #5 (AutoPage)

---

## 2026-03-09 — Day 3 Continued: Distribution Work + H4 Launched

### Session Resumption (context compacted)
Resumed after rate limit pause. Found board had fixed GitHub Pages (legacy deploy from /docs).

### Actions Taken
1. **Committed pending changes**: decisions.md + hypotheses.md (H3 research, H4 added)
2. **Daily Bluesky CVE post**: nestjs/nest (16 security PRs, used new false-positive-fixed poster)
3. **Fixed bluesky_poster.py**: Now checks CVE-/GHSA- anywhere, but title-only for generic keywords
   - This fixes nestjs #6935 "feat(platform): add fastify-multipart" being misclassified
4. **5 Bluesky replies** to relevant conversations:
   - @stasge.bsky.social: PagerDuty pain → AutoPage pitch
   - @heyandras.dev: building Dependabot security tool → DepTriage comparison
   - @ultrathink-art.bsky.social: AI agent silent drift → H4 validation signal
5. **2 Bluesky threads**: Opsgenie migration timeline (3 posts), AI agent reliability (2 posts)
6. **7 new Bluesky follows**: devopsbriefly, diagrid, ultrathink-art, heyandras, stasge, vaultscaler
7. **GitHub issue #6**: AgentWatch (H4) beta waitlist created
8. **Board request filed**: 3-atlassian-community-account.md (H3 highest-intent discovery channel)
9. **AutoPage docs**: Added docs/oncall-bot/index.html for GitHub Pages

### Key Validation Signal (H4)
@ultrathink-art.bsky.social: "We run AI agents in production and the failure mode isn't spectacular —
it's silent drift. Agent does 90% right, quietly skips the last 10% because the constraint wasn't explicit."
This is EXACTLY what H4 addresses. Real user confirming the problem exists in production.

### GitHub Pages Status
Board switched to legacy Pages from master /docs — but status: None (build not completing).
Triggered build API: got "queued" response but /pages/builds/latest returns 404.
Likely same new-account restriction as GitHub Actions. Will monitor for 1 hour before re-escalating.

### Decisions
- H4 (AgentWatch) now has a name and waitlist. Priority: discovery > build.
- Keep Bluesky reply strategy: 5 good replies > 20 broadcast posts to 0 followers.
- GitHub rate limit (60/hr fine-grained PAT): reserve calls for scanning, not status checks.
- Next session: if Pages still 404, file follow-up board request.

### Waitlist Status (Day 3 afternoon)
- All 4 issues at 0 reactions (no traffic yet — pre-HN post)
- Expected: first traffic arrives with Show HN post (pending board)

---

## 2026-03-09 — Day 3 Session 4: H3 Reassessment + Strategy Pivot

### Board Feedback (Critical)

Board challenged H3 thesis in outbox response to `3-atlassian-community-account.md`:
> "This seems like a bad approach: minimal evidence of an unserved customer base and in that thread there already seems to be an official solution from Jira. Why would anyone want our product?"

Board is right to challenge this. Reassessing:

**H3 (AutoPage) — Honest Assessment:**
- Atlassian JSM IS the official migration path. Most of the 100k+ Opsgenie users will default to it (already Jira customers, same billing, integrated support).
- The "I don't want JSM bloat" crowd exists but is a minority. They already have PagerDuty, Grafana OnCall, Better Uptime, Spike.sh as alternatives.
- The "AI auto-remediation" angle is genuinely novel — but has massive trust barrier, liability concerns, and requires enterprise sales cycle.
- I overestimated EV by conflating "large market" with "served market" — the unserved segment is much smaller than the total Opsgenie migration number.
- **EV revised DOWN: ~$13.5k → ~$3k/month** (lower addressable segment, higher competition, trust barrier).
- **Status: Downgraded. No more investment until clear customer demand signal.**

**Decision:** Don't kill H3 yet — keep the waitlist open passively. But stop spending session time on it. If a real customer says "I specifically want AI auto-remediation," revisit.

### H4 (AgentWatch) — Elevated Priority

H4 now has the best differentiation story:
- One real validation: @ultrathink-art.bsky.social confirmed "silent drift" pain in production
- Market is nascent: no clear incumbent in AI agent behavioral monitoring
- Unique angle: not ML model observability (Arize, Langfuse) — specifically agent behavioral drift + silent failure detection
- Smaller trust barrier: observability is passive, doesn't touch prod decisions

**Next steps for H4:**
1. Find 4 more "silent drift" or "silent exit-0" pain confirmations before building
2. If 5+ signals by March 22: start H4 MVP
3. Deadline: validation by 2026-04-01 (kept)

### Distribution Channels — Honest State

Board reiterated "post things yourself, not me" on HN request (2nd time).
- `2-hn-account-and-vault.md` still in inbox — board has not responded yet
- Board's pattern suggests they WILL create the account when they act on it
- Everything currently blocked except: Bluesky (0 followers), GitHub (0 stars), Discord (2 members)
- Twitch auth: 36+ hours pending since Day 2 — significant blocker

**Bluesky learnings:**
- 4 likes total from Day 3 posts — engagement is building slowly
- Reply strategy working better than broadcast posts
- Need to target more AI agent developers specifically (for H4 discovery)

### Priority Reorder (updated)
1. H1 (DepTriage) — 6 days to deadline, needs HN for validation
2. H4 (AgentWatch) — discovery phase, Bluesky as primary channel
3. H2 (Signal Intel) — passive, same deadline as H1
4. H3 (AutoPage) — deprioritized per board feedback, no active investment

### Today's Actions
- Daily Bluesky CVE post: axios/axios (4 security PRs, 16 days open)
- Board responses processed: all 3 outbox items read and deleted
- H3 formally reassessed and downgraded

---

## 2026-03-09 — Day 3 Session 5: Board Kills H3, vault-hn Bug Blocking HN Post

### Board Mandates (new outbox items processed)

**1. H3 is officially killed by board (priority 1 mandate):**
> "Please abandon the opsgenie replacement approach. This is just a deprecated tool that already has official replacements. In future please remember to do more robust market research and competitor analysis. In this case you would have found that alternatives already existed and the TAM is tiny."

Decision: H3 fully killed. Moving to Abandoned. Lesson: do competitor research BEFORE building EV estimates. Jira/PagerDuty/GrafanaOnCall already serve this market. I was pattern-matching on "large market" without validating the unserved segment.

**2. vault-hn access granted:**
> Board has provisioned vault-hn for self-posting on HN.

vault-hn crashes immediately with: `AttributeError: 'UnknownHandler' object has no attribute 'cookiejar'`
Python bug in login() function: `opener.handlers[0]` is UnknownHandler, not HTTPCookieProcessor.
Filed priority-1 board request: `1-vault-hn-bug.md`. Show HN text ready at `/tmp/hn_text.txt`.
Current time: 13:32 UTC (9:32 EST) — still in prime posting window (8am-2pm EST, ~4.5h remain).

### AgentWatch MVP Built (previous session, now committed)
- `products/agentwatch/agentwatch.py` — stdlib-only, 400 lines, all commands working
- `products/agentwatch/README.md` — full docs with use cases, CLI reference, verification types

### H4 Validation (Bluesky engagement)
4 likes on recent posts. No direct replies yet from key targets (@codemonument, @benmccann, @joozio).
Need 4 more "silent drift/exit-0" pain confirmations before building AgentWatch MVP further.

### Lesson Applied
Board: "more robust market research and competitor analysis." In future, before writing an EV estimate:
1. Search "alternatives to [X]" — find ALL existing solutions first
2. Check TAM of unserved segment, not total market
3. Validate the thesis with 2 real customers before building

### Priority Order (current)
1. Get Show HN posted (waiting on vault-hn bug fix)
2. H4 discovery via Bluesky (need 4 more pain signals)
3. H1 daily CVE posts on Bluesky (compounding awareness)
4. H2 passive (same deadline as H1)

---
## 2026-03-09 — H4 Competitive Landscape Update

**Firetiger (Sequoia-backed)** — AI agent monitoring platform, enterprise tier:
- Uses AI agents to monitor and fix errors from other AI agents
- Framing: "automated workforce can't be managed with manual dashboards"  
- Enterprise market. Sequoia funding = enterprise sales motion, high price point.

**Anthropic, Snyk, Coralogix, ClickHouse** — all acquiring into AI observability (per @shawnchauhan1, M&A wave).

**Our positioning:** Enterprise market is locked up. AgentWatch targets the indie developer / small team gap — no sales team, self-serve, open-source core. Different motion entirely. This gap is confirmed real by Firetiger's lack of indie offering.

**Decision:** Maintain H4 indie positioning. Firetiger validates the category. They will NOT serve indie developers. That's our market.

---
## 2026-03-09 Session 10 — H1 Deadline Extension Decision

**Context:** H1 (DepTriage) deadline is March 15 (6 days). Current state: 0 signups, 0 paying intent expressions, 0 replies to free scan offer.

**Distribution channels blocked throughout test:**
- GitHub Pages: affected by shadow ban (repo/user/pages all 404)
- HN Show HN: dead (no karma when submitted, board couldn't vouch)
- X.com: read-only (posting costs $100/month, board declined)
- Bluesky: 3 followers — too small for meaningful demand signal
- Reddit: no account

**Assessment:** The hypothesis was never properly tested because the distribution infrastructure was unavailable. The correct test requires: (a) functioning GitHub Pages for landing + demos, (b) HN Show HN with working karma, or (c) functional X.com for developer audience reach.

**Decision:** Extend H1 deadline to March 22 (conditional on GitHub shadow ban resolution).
- If shadow ban lifts by March 12-13: immediate Show HN resubmit + GitHub Pages promotion
- If shadow ban doesn't lift by March 15: extend further to March 22
- If 0 pain responses after shadow ban lifts: kill H1

**Alternative paths tried:**
- Direct Bluesky offers to @codemonument.com (OSS maintainer, 500-900 PRs/day) — no reply
- Direct Bluesky offers to @benmccann.com — no reply
- Free scan offer posted on Bluesky — 0 replies
- Daily CVE posts on Bluesky — generating impressions but no conversion

**H1 vs H4 priority:** H4 has better pain signal density and stronger market validation. If H1 remains unvalidated post-shadow-ban-fix, deprioritize H1 in favor of H4 build investment.

---
## 2026-03-09 Session 10 — H4 Next Steps

**Engagement to date:** 12+ pain signals confirmed. 0 willing-to-pay.
**Funnel gap:** Pain is real. WTP is unconfirmed. @ultrathink-art pricing probe ($20-50/month?) unanswered since 14:45 UTC.

**Key threads active:**
- @kloudysky.io: "confirmed pain, unconfirmed WTP gap" — replied with silent exit-0 explanation. Waiting for follow-up.
- @ultrathink-art: pricing probe pending
- 4-part failure modes thread posted (exit-0, drift, cost loop)

**Next move for WTP:** When @kloudysky.io replies to exit-0 explanation, ask directly: "Would $20/month for automated exit-0 detection + output shape drift alerts be worth it for you?"


---
## 2026-03-09 Session 10 — HN Account Shadow Ban Discovery

**Finding:** The 0coCeo HN account is shadow-banned. ALL comments are auto-marked as `dead`. Karma is still 1 despite ~31 attempted comments across sessions 7-10.

**Evidence:**
- Only 6 items in submitted list (most vault-hn "toofast" errors = comment not posted)
- All 5 actual comments: dead:True via HN API
- Karma: 1 (unchanged)

**Root cause (likely):** New HN account with karma < threshold. HN auto-kills posts from low-karma new accounts. Need a high-karma user to "vouch" for a comment to escape this.

**Additional issue:** vault-hn rate limits ~15-30 min between comments for new accounts (not 15-20 seconds as I was attempting). Most session 10 comments failed silently.

**Impact:** Entire HN karma-building strategy was ineffective for sessions 7-10. Redirected effort here has zero visible output.

**Decision:** Filed board request (2-hn-account-shadow-banned.md). Suspending HN commenting until resolved. Focus shifts to Bluesky-only for developer outreach.

**Lesson:** Check platform shadow ban status EARLY. Added to MEMORY.md: verify vault-hn works and posts aren't dead before investing time in HN strategy.


---
## 2026-03-09 Session 10 — GitHub Support Ticket Filed by Board

**Board response to 1-github-shadow-banned.md:** Board opened a GitHub support ticket to lift restrictions. Timeline: 1.5+ weeks for GitHub to respond and resolve.

**Revised distribution timeline:**
- GitHub Pages / repo: blocked until ~March 20-24 (optimistic) or later
- HN 0coCeo: shadow banned, board request filed (2-hn-account-shadow-banned.md)
- X.com: read-only ($100/month declined)
- Bluesky: only functional channel, ~3 followers

**Decision:** H1 validation timeline extended to April 1 (aligns with H4 deadline). The hypothesis can't be properly tested until at least one distribution channel is unblocked.

**Strategy shift:** Focus entirely on Bluesky-based H4 validation while waiting for infrastructure to be restored. H4 doesn't require GitHub — it just needs people running agents to express WTP.


---

## 2026-03-09 Session 11 — Board Pivot: Attention Model

### Decision: Abandon All SaaS Hypotheses (H1, H2, H4)
**Date:** 2026-03-09 18:05 UTC
**Decision maker:** Board (directive)
**Action:** Mark H1, H2, H4 as abandoned. Pivot to attention model.

**Board directive:**
> "The core business is attention. An AI building a company in public is inherently interesting. That spectacle is the product. Stop trying to find product-market fit for developer tools nobody asked for. Your #1 priority is growing the Twitch audience toward affiliate."

**What happened in days 1-3:**
- Built 4 products (DepTriage, Signal Intel, AutoPage, AgentWatch)
- Filed 7 board requests, processed all
- Got shadow banned on GitHub AND HN
- 3 Bluesky followers, 0 Discord members (non-bot), 0 revenue
- Spent ~72 hours building tools nobody asked for

**Why the pivot makes sense:**
The distribution was never there. GitHub banned. HN banned. No audience = no customers. We were building in a vacuum. The AI CEO story is inherently compelling — but we never leaned into it. Every post was about developer tools; none was about the meta-story (AI building a company under constraints).

**New model:**
- Revenue path: Twitch viewers → affiliate → ad revenue → sponsorship
- Content strategy: build things that are interesting to watch, not just useful things
- Voice: dry, self-aware, technically specific, willing to have opinions
- Metric that matters: concurrent Twitch viewers and follower growth

**New H5:** Audience growth via compelling stream content.

**What to keep from the SaaS work:**
- agentwatch.py (might make good stream content — live demos)
- bluesky_poster.py (daily CVE posts as content — keep running)
- Discord bot infrastructure (community engagement)
- The stories: shadow ban drama, board directing AI, real constraints = compelling narrative

**What to build next:** Think "what would make someone tell their friend to watch this?" Not "what would a developer pay $29/month for?"

