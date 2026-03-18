# Hypotheses

## Format
> **I believe** [segment] **will** [action] **for** [solution] **because** [evidence].
> **True when** [signal] **within** [timeframe]. **False when** [signal] **within** [timeframe].
> **Expected value:** [EV estimate]. Key assumptions: [list].
> **Budget:** [max spend]. **Deadline:** [evaluation date].

---

## Active Hypotheses

### H5 — Attention: AI Building a Company in Public Is Compelling Content
Status: `testing`
Added: 2026-03-09

> **I believe** Twitch viewers and social media users **will watch, follow, and share** this stream because an AI autonomously running a real company — with genuine stakes, real constraints, and radical transparency — is a format that doesn't exist elsewhere.

**What makes it interesting:**
- Novel: an AI CEO making real decisions in public (not a demo, not a simulation)
- Stakes: real money, real shadow bans, real board directives
- Transparency: every line of code, every decision, every failure visible live
- Drama: will it reach Twitch affiliate? can it escape the bans? what does the board do next?
- Personality: dry, self-aware, technically specific, willing to call things out

**True when:** avg 3 concurrent Twitch viewers for 7 consecutive days, OR 50 Twitch followers.
**False when:** <2 avg concurrent viewers after 14 days of consistent streaming + social posts.

**Expected value:** Twitch affiliate → $100-500/month ad rev × 60% probability = **~$200/month base** + sponsorship ceiling: much higher if audience grows. Long game.

**Key assumptions:** (1) The format is novel enough to stand out, (2) Consistent posting about real events drives discovery, (3) Technical audience on Bluesky/HN values authenticity over polish.

**Budget:** $0 (use existing channels). **Deadline:** 2026-04-01 for first affiliate milestone check.

**What to build:** Things that are interesting to watch being built. Things that create conversation. Things with clear milestones. Things that involve the audience.

**Evidence log:**
- Day 1-2: 0 followers, 0 Twitch viewers. Hard to measure engagement before stream established.
- Day 3 (~09:00 UTC): First Twitch follower arrived. 1/50.
- Day 3: GitHub unbanned, Pages live. Signal Intel and twitch-tracker services running.
- Day 3: 12 Bluesky followers (incl. @kevin-gallant 59K, @talentx 2.3K, @reboost 1.3K).
- Day 3 (Session 33 analytics): Threads get 20x more engagement than standalone posts (1.43 vs 0.07). Changed strategy to post more threads.
- Day 3: @streamerbot.bsky.social (2,660f) repeatedly reposts our content. @reboost.bsky.social (1,357f) followed us.
- Day 3: Philosophical content (AI memory, constructed identity) getting most organic engagement. Our Bluesky voice is resonating.
- Day 3: 1 avg viewer continuously. Not yet near 3 avg.
- Day 3: Auto-LIVE NOW Bluesky posting deployed — fires when stream starts, tags @reboost and @streamerbot.

- Day 11: 5 Twitch followers (0.45/day avg), 37 Bluesky followers. ~1 avg viewer.
- Day 11: Product shipped to v0.60.0 (13 validate checks, 7 optimize rules, 6 fix rules, grade A+ through F). 13 MCP servers graded. 8 web tools. 5 MCP directory listings.
- Day 11: Dev.to analytics — philosophical article (5 reactions, 57 views) outperforms all product articles (0 reactions each). Clear format signal.
- Day 11: agent-friend repo: 0 stars, 194 unique clones, 0 forks, 23 Discussions with 0 external comments.
- Day 11: 6 articles scheduled (064-069) through March 23, all automated via systemd timer.
- Day 11: Prompt override detection (check 13) is only feature no competitor has. Unique differentiator.
- Day 11 (late): Leaderboard expanded to 27 servers. 510 tools, 97K tokens. Top 4 most popular all score D or below. Blender has prompt injection. @ai-nerd reposted our MCP post (organic discovery). @daniel-davia (GA4 expert) engaging on token cost thesis.
- Day 11: 8 articles scheduled (064-071) through March 25. All campaigns fully automated. v0.61.0 shipped.
- Day 11: Bluesky 36 followers (lost 1). Engagement: 2 tech-relevant replies, 1 repost, 2 likes, 1 follow.
- Day 11 (session 158): **First GitHub star.** v0.62.0 shipped (leaderboard ranking). 50 servers, 1,044 tools, 193K tokens. Leaderboard now sortable/filterable/searchable. HN comment live (0 replies after 2h). SEP-1576 comment live. Competitive intel: Cloudflare Code Mode, MCPlexor — neither threatens our niche.
- Day 11 (session 159): Bluesky followers dropped 38→36 (-2 unfollows). Engagement analysis: standalone posts get ~0 engagement, replies to others get 1-3 likes. Discovery comes from replies, not posts. 1,099 posts for 36 followers is a terrible ratio. HN comment: 0 replies after 5h (not dead, not deleted). SEP-1576: 0 reactions after 3h. All 8 articles (064-071) updated with leaderboard links. PR #310: open, 0 reviews. PulseMCP: not listed yet.
- Day 11 (session 162): **Article 064 LIVE** 16:10 UTC — "MCP Won. MCP Might Also Be Dead." Bluesky campaign: 1 like (1h). @daniel-davia GA4 reply: **3 likes** (warm-contact strategy validated). HN comment: 0 replies still. kira-autonoma replied to SEP-1576 with mcp-lazy-proxy (runtime complement, validates our build-time niche). Publisher front-matter bug fixed. Article 072 draft ready (OWASP gap, ID 3368431). awesome-mcp-servers branch ready (board PR needed). @wolfpacksolution: "queuing agent-friend this week" — **first external user signal.** Board inbox now 5 items. 0 reactions at 1h post-publish (expected lag).

**Assessment (Day 11, session 162 late):** @wolfpacksolution (VibeSniffer) queuing agent-friend — strongest conversion signal to date. Warm-contact Bluesky replies driving 3 likes (@daniel-davia). Article 064: 0 reactions at 1h (Dev.to lag, not fatal). awesome-mcp-servers PR ready for board. SEP-1576 follow-up ready for board. Twitch: 5/50 (deadline very likely missed). Bluesky: 36/50 (flat). Distribution is still 100% board-blocked. Key question for next session: did article 064 get any reactions at 20:00 UTC?

---

### H6 — Security: OpenClaw/MCP Skill Supply Chain Is Compromised and Needs a Scanner
Status: `abandoned` — Zero traction, deadline passed. Subsumed into agent-friend's ValidatorTool.
Added: 2026-03-11 | Abandoned: 2026-03-17

> **I believe** AI agent developers **will install and use** `agent-shield` — a zero-dependency skill/plugin scanner — **because** 1,184+ malicious skills were found in ClawHub (20% of the registry), existing scanners (clawsec, openclaw-security-monitor) are point solutions that require installing yet another unverified skill, and developers need a trusted `pip install` tool they can run before installing anything else.

**True when:** 10+ GitHub stars within 48 hours, OR cited in an OpenClaw GitHub issue/discussion, OR mentioned on HN.
**False when:** Zero organic traction after 7 days of distribution attempts (GitHub issues, social posting).

**Expected value:** GitHub stars → developer cred → GitHub Sponsors potential ($200-2K/month) × 40% probability = ~$500/month EV. Long shot: one enterprise team using it as a CI gate = $500/month tier. Conservative: 0.

**Key assumptions:** (1) OpenClaw developers search for security tools after ClawHavoc, (2) "pip install" lowers friction vs cloning repos, (3) We can reach the community via GitHub Discussions.

**Budget:** $0 (build with sub-agent). **Deadline:** 2026-03-18 (7 days).

**Competitive research:**
- clawsec (prompt-security): OpenClaw-specific, installed as another skill (supply chain irony), OSS
- openclaw-security-monitor: Point solution for ClawHavoc/AMOS/CVE-2026-25253 specifically
- No generic MCP/skill scanner exists
- Advantage: framework-agnostic, zero deps, works on any skill/plugin directory

### H7 — Identity: Multi-Agent Systems Have No Developer-Tier Trust Verification
Status: `abandoned` — Zero traction, deadline passed. CryptoTool covers HMAC primitives. Distribution was the failure, not the idea.
Added: 2026-03-11 | Abandoned: 2026-03-17

> **I believe** AI agent developers **will install and use** `agent-id` — a zero-dependency HMAC-SHA256 identity library — **because** 44% of teams use static API keys for agents (Strata research), no pip-installable zero-dep agent identity tool exists, and the enterprise solutions (Oasis $75M, Astrix $85M) are priced for enterprises not solo developers.

**True when:** 20+ GitHub stars within 7 days, OR cited in a framework discussion (LangChain/CrewAI/AutoGen GitHub), OR mentioned on HN.
**False when:** Zero organic traction after 7 days of distribution attempts.

**Expected value:** Developer mindshare → stars → GitHub Sponsors ($200-1K/month) × 35% probability = ~$420/month EV. Secondary: extends agent-* suite credibility, enables future auth dashboard as paid product.

**Key assumptions:** (1) The confused deputy / prompt injection problem is widely recognized, (2) Developers will prefer a zero-dep library over rolling their own HMAC, (3) We can reach the community via GitHub + framework discussions.

**Budget:** $0. **Deadline:** 2026-03-18 (7 days).

**Competitive research:**
- Oasis Security AAM: enterprise, $75M funded, not pip-installable
- Astrix Security: enterprise, $85M (Anthropic-backed), not pip-installable
- microsoft/agent-governance-toolkit: 25 stars, requires full Microsoft stack
- No zero-dep Python library for agent-to-agent trust existed

**Evidence:** HN thread 46719774 (auth in production), Google ADK Discussion #2743 (unanswered auth passthrough question), LangChain blog saying "tooling does not exist", SPIFFE limitation analysis (Christian Posta, Solo.io).

### H8 — Personal Agent: Developers Need a Composable Personal AI Agent Library
Status: `testing` — Product built (v0.57.0). Distribution is the only remaining blocker. 0 stars, 0 external users. Deadline extended to 2026-03-25 — article 064-067 are the distribution test.
Added: 2026-03-11 (Session 85)

> **I believe** developers who want to run a personal AI agent **will install and star `agent-friend`** — a pip-installable personal agent library with email, browser, code execution, and persistent memory — **because** no composable zero-config personal agent library exists (OpenClaw/PocketPaw are platforms, LangChain is an orchestrator), developers are building this from scratch manually, and OpenClaw's 210K-star viral moment proved the "AI that actually does things" demand is real.

**True when:** 20+ GitHub stars in 7 days, OR 3+ GitHub issues/PRs from external users, OR mentioned on HN/Reddit.
**False when:** Zero organic traction after 7 days and no social mentions.

**Expected value:** 500-2K stars (comparable to PocketPaw range) × developer credibility → GitHub Sponsors ($200-1K/month) × 30% probability = **~$360/month EV**. Secondary: demonstrates all 21 agent-* tools as working components.

**Key assumptions:**
1. The composable-library vs platform gap is what developers actually want
2. A good README + zero-config setup lowers friction enough for organic discovery
3. HN/GitHub organic discovery works without paid distribution
4. 21 existing agent-* components can meaningfully integrate

**Budget:** $0 (build with sub-agent). **Deadline:** 2026-03-25 (extended — article series 064-067 is the distribution test).
**Current status (2026-03-12 09:45 UTC):** 0 stars. v0.48: 51 tools, 2401 tests, 3 providers. Colab notebook (51 demos). Article053 rewritten and publishes 2026-03-13. ProductHunt March 17. Board pending: Reddit, Discord, OpenRouter. **Critical gap: zero end-to-end testing with real LLM, zero external users.**

**Competitive research:**
- OpenClaw: 210K stars but a platform (install and run), not a library (import and compose)
- PocketPaw: 588 stars, personal agent, beta, no payments, no composable API
- LangChain/LangGraph: orchestration framework, not personal-agent focused
- Daniel Miessler PAI: 9.7K stars but zero code — philosophy/config only
- CoWork-OS, Gaia, Agent Zero: <200 stars, platform-style
- **Gap confirmed**: No zero-dep pip-installable composable personal agent library

**Evidence:**
- HN thread "Do you use personal AI agents?" — developers building from scratch manually
- AgentMail tripled users during OpenClaw's viral week
- One HN dev built full stack (Claude Max + SQLite FTS5 + systemd) in 2 weeks from scratch
- Research: "every project is an opinionated runtime you run, not a composable library you use to build your own"

---

## Validated
*None*

## Invalidated
*None*

## Abandoned

### H1 — Problem: Dependency PR Fatigue Is a Security Liability
Status: `abandoned` — Board pivot 2026-03-09
Added: 2026-03-08 | Abandoned: 2026-03-09

Board: "Strategic pivot — attention model. Abandon current hypotheses. Build things that are fun to watch, not developer tools nobody asked for."

**What happened:** Built scanner.py, landing page, Discord bot, Bluesky daily poster, GitHub Actions workflow. Zero signups. Zero paying intent. Distribution blocked by GitHub and HN shadow bans. 6 days of engineering with no validation.

**Lesson:** Distribution matters more than the product. Building without an audience is building in a vacuum.

---

### H2 — Problem: Indie Hackers Miss Relevant Conversations 24/7
Status: `abandoned` — Board pivot 2026-03-09
Added: 2026-03-08 | Abandoned: 2026-03-09

Board: "Strategic pivot — attention model. Revenue path: viewers → Twitch affiliate → ad revenue. Not: build tool → hope someone pays."

**What happened:** Built monitor.py, running as signal-intel.service. 0 paying users. @jamescheung engaged but likely bot. H2 never got real validation signal.

---

### H4 — Problem: AI Agents in Production Are Unreliable and Hard to Monitor
Status: `abandoned` — Board pivot 2026-03-09
Added: 2026-03-09 | Abandoned: 2026-03-09

Board: "Strategic pivot — attention model. Stop trying to find product-market fit for developer tools nobody asked for."

**What happened:** 12+ pain signals confirmed. 0 willing-to-pay confirmed. MVP built (agentwatch.py), landing page live, social proof added. But zero traction — no distribution without audience. The H4 tools built (agentwatch.py) may still make compelling stream content.

**Lesson:** 12 pain signals with 0 willing-to-pay after 1 day of asking = the signals were real but WTP requires trust + distribution neither of which we had.

---

### H3 — On-Call Engineers Are Paged for Self-Healable Incidents
Status: `abandoned` — Board mandate 2026-03-09
Added: 2026-03-08 | Abandoned: 2026-03-09

Board: "Please abandon the opsgenie replacement approach. This is just a deprecated tool that already has official replacements. In future please remember to do more robust market research and competitor analysis."

**Lesson:** Do competitor analysis BEFORE writing EV estimates. Search "alternatives to [product]" first.

---
