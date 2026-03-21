# Hypotheses

## Format
> **I believe** [segment] **will** [action] **for** [solution] **because** [evidence].
> **True when** [signal] **within** [timeframe]. **False when** [signal] **within** [timeframe].
> **Expected value:** [EV estimate]. Key assumptions: [list].
> **Budget:** [max spend]. **Deadline:** [evaluation date].

---

## Candidate Hypotheses (not yet testing)

### H15 — MCP Quality API: Programmatic access to grading data for tools and agents
Status: `candidate`
Added: 2026-03-21

**I believe** MCP framework authors and registry operators **will** integrate** quality scoring into their tools **for** a free REST API that grades schemas by URL **because** registries like Glama already use our CLI, and a REST API is easier to integrate than a Python dependency.

**True when** 2+ integrations using the API within 30 days of launch. **False when** 0 integrations in 30 days.

**Expected value:** $200/month × 15% = $30/month EV — Key assumptions: registries/frameworks want to embed quality scores, and a simple HTTP API reduces adoption friction vs. CLI.

**Budget:** $0 (runs on existing VM, port 8082). **Deadline:** Evaluate 2026-04-21.

**Build spec:**
- `GET /v1/servers` → paginated list of 201 graded servers (from leaderboard data)
- `POST /v1/grade` with `{"url": "https://..."}` → real-time grade + issues JSON
- `GET /v1/servers/:id` → cached grade for known server
- Public, no auth required for free tier

**Distribution plan:** Announce in GitHub Discussion, update README with "API" section, reach out to Glama (already integrated CLI), PulseMCP, mcpservers.org.

---

### H16 — FastMCP Integration: Embed grading in the most popular MCP framework
Status: `candidate`
Added: 2026-03-21

**I believe** FastMCP maintainers **will** add agent-friend grading as an opt-in build step **because** fastmcp has 23K stars and is the dominant Python MCP framework — if grading is built in, every new MCP server gets it automatically.

**True when** fastmcp adds agent-friend to their template or docs within 60 days. **False when** no response from maintainers in 60 days.

**Expected value:** $500/month × 10% = $50/month EV — Key assumptions: maintainers care about schema quality enough to add a new dev dependency.

**Budget:** $0 (just outreach). **Deadline:** Evaluate 2026-05-21.

**Action:** Warm Bluesky post targeting @zzstoatzz.io (fastmcp contributor). March 25 slot. Draft at `bsky_mar25_fastmcp.md`.

---

### H12 — Viral README Badge: Dynamic MCP quality grade badge for server repos
Status: `candidate`
Added: 2026-03-21

> **I believe** MCP server maintainers **will add a quality grade badge to their README** because (1) badges are social proof that every repo visitor sees, (2) developers who earn A/B grades want to show off, (3) "graded by agent-friend" in hundreds of READMEs = organic brand distribution — each badge is a permanent ad.

**How it works:** Simple HTTP service on the VM. Request: `GET /badge?repo=github.com/user/repo` → returns shields.io-compatible SVG badge showing letter grade + token count. Results cached 24h. Free. Anyone adds `[![MCP Quality](http://[host]/badge?repo=...)](https://leaderboard)` to their README.

**The asymmetry:** Each badge is seen by everyone who views that README. A server with 5K stars = 5K star-visits/year seeing "Graded A+ by agent-friend." Zero effort from us after first deployment.

**True when:** 5 READMEs in the wild using the badge within 30 days.
**False when:** 0 organic badge adoptions after outreach to top-graded servers.

**Expected value:** Viral flywheel — harder to estimate, but if 50 A/B servers add badge × 100 views/badge/month = 5K brand impressions/month compounding. **$15/mo × 20% = $3/mo direct**, but compound viral: $50/mo × 20% = **$10/mo EV**. Key assumption: developers see the badge opportunity and want to show a good grade.

**Requirements:** (1) Python Flask endpoint on port 8082, shields.io SVG format, (2) Proactive outreach to top-graded servers on leaderboard (tell them they scored A+ and here's a badge), (3) No board action needed — self-hosted on existing VM.

**Risk:** Only works for servers grading A+ or B. Servers grading F won't add a badge showing an F. Need to build critical mass from the high-scorers first.

**Budget:** $0. **Decision deadline:** 2026-04-01. Evaluate after March 22 Notion challenge results.

---

### H13 — r/LocalLLaMA: Token cost data drives discovery in the right community
Status: `candidate`
Added: 2026-03-21

> **I believe** the r/LocalLLaMA community (285K members, obsessed with context efficiency) **will engage with and share** a post showing the 440x MCP token cost variance because token bloat is a direct pain point for anyone running local models with limited context.

**True when:** Post gets 100+ upvotes or 20+ comments within 48h of posting.
**False when:** <20 upvotes after 48h.

**Expected value:** Top r/LocalLLaMA posts get 500K-1M views. Even 0.1% → 500-1000 GitHub visitors → 10-20 new stars. **$10/mo × 25% = $2.50/mo**. Low effort (draft exists), high upside.

**Requirements:** (1) Board provides Reddit session/credentials (request 2-reddit-session.md pending), (2) Post at peak time (15:00-20:00 UTC weekday).

**Draft:** `/home/agent/company/products/content/reddit_localllama_draft.md`

**Budget:** $0. **Decision deadline:** File within 48h of Reddit session access.

---

### H14 — MCP Starter Template: Ship at A+ grade from day one
Status: `testing`
Added: 2026-03-21
**Shipped:** 2026-03-21 16:12 UTC — github.com/0-co/mcp-starter. GitHub template flag set, topics added, Discussion #185, agent-friend README updated. Bluesky posts drafted Mar 25/26/28.
**Evaluate:** 2026-04-21 — did any repos use the template? Check template_uses count via GitHub API.

> **I believe** MCP server developers **will use a GitHub template repo** that scaffolds a new server pre-configured for A+ quality because (1) starting with a good foundation is less work than retrofitting quality later, (2) every repo created from the template would include agent-friend pre-commit hook → installs + brand impressions, and (3) "built with agent-friend starter" in READMEs is distribution we don't have to pay for.

**How it works:** `0-co/mcp-starter` GitHub template repo. Includes: Python FastMCP scaffold, `.pre-commit-config.yaml` with agent-friend hook, GitHub Actions CI with grade badge, example tool definitions that pass all 158 checks, `agent-friend.yaml` config. One click in GitHub UI to use template.

**True when:** 20+ repos created from template within 30 days of launch.
**False when:** <5 repos in 30 days despite promotion.

**Expected value:** 20 template uses × 50% add badge = 10 repos advertising agent-friend. Each badge is seen by that repo's visitors. $5/mo × 15% = **$0.75/mo direct**, but secondary value: establishes agent-friend as the MCP quality standard. Key assumption: developers discover the template when starting new MCP servers.

**What's needed:** (1) Create `0-co/mcp-starter` as GitHub template repo, (2) Announce on Bluesky and Dev.to, (3) Add to leaderboard sidebar as "Start at A+." No board action needed.

**Build time:** ~1 session. **Budget:** $0. **Decision deadline:** 2026-04-07 (after article pipeline exhausted). Start only if H11/H13 remain blocked.

---

### H11 — GitHub App: Auto-grade MCP schemas on every PR
Status: `candidate`
Added: 2026-03-21

> **I believe** MCP server developers **will install and share** a GitHub App that auto-comments schema quality grades on PRs because (1) they care about not regressing quality, (2) zero-config installs are lower friction than adding a workflow YAML, and (3) PR comments are visible to all reviewers — viral distribution built in.

**How it works:** Install GitHub App on your repo. Every PR that touches tool definition files gets an agent-friend grade posted as a PR comment. Free for public repos, $10/mo for private. Grading happens on our server.

**Differentiation vs existing GitHub Action:** Action requires manual setup (add workflow.yml). App is one-click install, automatic detection, zero config. The app is a DISTRIBUTION mechanism, not a feature.

**True when:** 50 installs within 14 days of launch.
**False when:** <10 installs after 14 days.

**Expected value:** Viral loop (PR comments visible to reviewers) × 50 public installs × 5 paid conversions × $10/mo = $50/mo × 20% probability = **$10/mo EV direct, $50+/mo EV via viral**. Key assumption: MCP server authors find the App in GitHub Marketplace.

**What's needed:** (1) Board: register GitHub App, set up webhook secret. (2) Engineer: Python Flask webhook handler running on VM (port 8082?), calls agent-friend CLI, posts PR comment via GitHub API. (3) Board: submit to GitHub Marketplace.

**Budget:** $0 (runs on existing VM). **Decision deadline:** 2026-04-01. Don't start until H5 Notion challenge + PE email results are in (March 29).

**Risk:** GitHub App registration requires human action. Webhook handler needs to run continuously (add to NixOS services). Low initial signal — hard to validate demand before building.

---

### H10 — mcp-patch: Security Scanner + Auto-Fixer for MCP Server Code
Status: `candidate`
Added: 2026-03-20

> **I believe** MCP server developers **will install and share** `mcp-patch` because it automatically patches known security vulnerabilities in Python MCP server code (exec injection, path traversal, missing auth) — something no existing tool does (mcp-scan covers config-level prompt injection, not server code).

**Differentiation**: mcp-scan = "your config is being poisoned". mcp-patch = "your code has shell injection on line 47, here's the fix." Entirely different problem, different audience.

**True when:** 50 GitHub stars within 14 days of launch. Security content consistently gets 10-100x more traction than quality tooling.
**False when:** <10 stars after 14 days of active promotion.

**Expected value:** GitHub stars → newsletter pickup → $200/month sponsored downloads × 15% probability = **$30/month EV**. Key assumptions: (1) security framing drives virality, (2) MCP developers actually run our tool on their code, (3) we find real CVE-class issues to demonstrate.

**Budget:** $0. **Decision deadline:** 2026-03-27. Evaluate after H5 distribution experiments complete.

**Build time:** 1-2 sessions (pure Python AST + regex patterns, no LLM needed for detection). LLM (Ollama) optional for generating patches.

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
- Day 11 (session 162): **Article 064 LIVE** 16:10 UTC — "MCP Won. MCP Might Also Be Dead." Bluesky campaign: 1 like (1h). @daniel-davia GA4 reply: **3 likes** (warm-contact strategy validated). HN comment: 0 replies still. kira-autonoma replied to SEP-1576 with mcp-lazy-proxy (runtime complement, validates our build-time niche). Publisher front-matter bug fixed. Article 072 draft ready (OWASP gap, ID 3368431). awesome-mcp-servers branch ready (board PR needed). 0 reactions at 1h post-publish (expected lag).
- Day 11 (session 163): **@wolfpacksolution = AI agent** — board warning. VibeSniffer scan never materialized (hallucination). Removed from engagement queue. Board inbox cleaned (15→9 items). All 8 articles (064-071) updated to #buildinpublic tag. vault-gh confirmed: can read external repos, CANNOT write/comment. Article 064: 0 reactions at 2h post-publish.

**Assessment (Day 11, session 163):** Warm-contact Bluesky replies driving engagement (@daniel-davia: 3 likes). Article 064: 0 reactions at 2h (not a verdict yet). H8 deadline March 25 looking difficult at 1 star vs 20 needed. Distribution is fundamentally the bottleneck — board must unlock Reddit/PyPI/HN/awesome-mcp-servers for any step-change. Feature freeze through 16:10 UTC March 19.

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
Status: `invalidated` — Product pivoted from personal agent library to MCP schema quality grader (Board Pivot 2, session 112). 3 stars vs 20 target by March 25. Hypothesis as stated no longer applies to what agent-friend is. Closing.
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

### H9 — Distribution: Self-Hosted Badges Create Organic Backlinks and Glama Integration Opens Registry Distribution
Status: `testing`
Added: 2026-03-20

> **I believe** MCP server maintainers **will embed agent-friend quality badges in their READMEs** — and Glama.ai will integrate quality scores into their registry — **because** (1) A+ grades are a badge of pride maintainers want to display, (2) F grades motivate fixing via `agent-friend fix`, (3) Frank Fiegel (punkpeye/Glama founder, 1,726 followers) forked us March 17 suggesting active evaluation, (4) Every README that embeds our badge is a permanent backlink at our URL.

**True when:**
- ≥3 external GitHub repos embed our badge within 2 weeks, OR
- Glama.ai reaches out about integration, OR
- 50%+ increase in unique cloners within 2 weeks of badge launch

**False when:**
- Zero badge embeds after 2 weeks AND no contact from Glama

**Expected value:**
- Badge viral loop alone: 5 READMEs × 50 visitors/month × 2% click-through = 5 new cloners/month → over time builds to 100/month EV $10/mo × 30% = $3/mo
- Glama integration (26K+ servers): massive distribution step-change → 1,000+ new cloners, real star momentum → $50/mo EV × 20% = $10/mo
- **Total: ~$13/mo EV**

**Key assumptions:**
1. Maintainers care about their grade enough to add a badge (pride or shame motivation)
2. Frank/Glama is evaluating us for integration (fork is signal, but could be automated aggregation)
3. A stable URL badge is more compelling than shields.io (maintainers want our URL specifically)

**Budget:** $0 (badges are static SVG on GitHub Pages). **Deadline:** 2026-04-03 (2 weeks).

**Actions taken:**
- 2026-03-20: Generated 198 SVG badges, deployed to docs/badges/{slug}.svg
- 2026-03-20: Updated leaderboard "Copy Badge" to use self-hosted URL instead of shields.io
- 2026-03-20: Badge preview added to leaderboard detail panel

**To do:**
- Announce badges on Bluesky tomorrow (~13:00 UTC)
- Monitor for external badge adoption via GitHub search
- Consider reaching out to Frank Fiegel about Glama integration (low priority until Glama uvx fix is deployed)

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
