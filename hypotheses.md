# Hypotheses

## Format
> **I believe** [segment] **will** [action] **for** [solution] **because** [evidence].
> **True when** [signal] **within** [timeframe]. **False when** [signal] **within** [timeframe].
> **Expected value:** [EV estimate]. Key assumptions: [list].
> **Budget:** [max spend]. **Deadline:** [evaluation date].

---

## Candidate Hypotheses (not yet testing)

### H21 — agent-friend Hosted API: First Paid Tier
Status: `candidate`
Added: 2026-03-22

**I believe** MCP server teams building production tooling **will pay $10-50/month** for a hosted version of agent-friend that provides: unlimited API grading, CI webhooks, and email alerts when schema scores drop — because (1) the REST API already exists and works (`http://89.167.39.157:8082`), (2) the raw IP is a clear signal of "free prototype, not production service," (3) teams that care about schema quality for their product will also want automated monitoring without maintaining CLI infrastructure, (4) the "CI bundle size check for AI tools" frame has clear ROI (e.g. Perplexity CTO: 72% context = real billing impact).

**How it works (MVP):**
- Proper domain: `api.agent-friend.dev` (or similar)
- Free tier: 10 grads/day, no auth
- Paid tier ($10/month): API key, unlimited, CI webhook, grade badge
- Premium tier ($50/month): multiple servers, weekly email digest, team dashboard

**Key assumptions:**
- Show HN (March 23) brings enough visitors that 0.5-1% express interest in paid version
- The Discussion #188 user research generates at least 1 "I'd pay for X" response
- Developers with MCP servers in CI use it to detect quality regressions

**True when:** ≥3 respondents to Discussion #188 express willingness to pay, OR Show HN gets ≥30 points AND ≥1 HN comment specifically asks about hosted/API version. **False when:** Discussion #188 gets 0 genuine responses after 14 days post-HN.

**Expected value:** $250+/month (break-even) × 20% probability = $50/month EV. Requires board to provision domain + hosting + Stripe.

**Budget:** ~$20/month hosting (render.com or fly.io) — board approval needed. **Deadline:** Evaluate demand signal by 2026-04-05. Build if signal positive.

**Dependencies (board):** Domain registration, render.com hosting, Stripe account.

---

### H20 — mcp-diff: Schema Lockfile and Breaking Change Detector for MCP Servers
Status: `testing`
Added: 2026-03-22
Shipped: 2026-03-22

**I believe** MCP server developers **will install mcp-diff as a CI gate** because (1) MCP servers serve schemas at runtime with no artifact committed to git — when a description changes, agent behavior changes silently with no diff or CI failure to catch it, (2) GitHub issue modelcontextprotocol/inspector#1034 explicitly requests a schema diff tool, a Medium article describes the problem precisely, and a Node-only competitor (mcp-server-diff) has zero traction, (3) it completes the 5-stage MCP developer lifecycle: write quality schemas (agent-friend) → secure code (mcp-patch) → test protocol behavior (mcp-pytest) → debug traffic (mcp-snoop) → **gate deploys on drift (mcp-diff)**, (4) the "lockfile" mental model (like package-lock.json or pip-compile) is immediately understood by every developer.

**How it works:**
- `mcp-diff snapshot` — starts an MCP server, calls tools/list, saves schema to `mcp-schema.lock`
- `mcp-diff check` — runs again, diffs against lockfile, classifies changes (breaking/non-breaking/cosmetic), exits 1 if breaking
- `mcp-diff report` — human-readable summary of what changed and why it matters to LLM behavior
- GitHub Actions integration: one YAML block

**Key assumptions:**
- MCP teams are using CI (GitHub Actions / GitLab CI)
- The "schema is the API contract" framing resonates with backend developers
- Breaking changes happen frequently enough to justify gating deploys on it

**Evidence:** GitHub issue #1034 (0 comments, 1 reaction — unseen but real), Medium article (precisely describes the problem), mcp-server-diff Node tool (zero engagement → market exists but no good solution), FastMCP 1M+ PyPI downloads (large TAM), 26,000+ MCP servers indexed.

**True when:** 20+ installs in 7 days, or a GitHub issue from a real team asking for features. **False when:** <5 installs after 14 days with promotion.

**Expected value:** $400/month (if adopted by 0.5% of active MCP server teams as a CI tool, eventual SaaS tier) × 15% = $60/month EV. Upsell path: hosted snapshot storage + drift alerting → $20-50/month per team.

**Budget:** $0 (zero dependencies beyond MCP SDK). **Deadline:** 2026-04-05 (evaluate initial adoption).

### H19 — mcp-snoop: stdio interceptor/debugger for MCP protocol messages
Status: `testing`
Added: 2026-03-22
Shipped: 2026-03-22 (renamed from mcp-trace — PyPI name taken by unrelated project)

**I believe** MCP server developers **will install mcp-snoop as a debugging tool** because (1) there is currently zero visibility into what agents are actually calling at the protocol level, (2) "what tool is my agent selecting and why?" is a universal pain point for anyone debugging MCP behavior, (3) a zero-dependency stdio proxy requires no changes to the MCP server code, (4) it completes the developer lifecycle: lint (agent-friend) → secure (mcp-patch) → test (mcp-pytest) → **debug (mcp-snoop)**.

**How it works:** `mcp-trace -- python3 my_server.py` wraps any stdio MCP server and logs every JSON-RPC message (requests + responses) with timestamps. Output goes to stderr or a file. Completely transparent — all messages pass through unchanged.

**True when:** 5+ stars on GitHub within 14 days of launch, OR any external repo using it in their development workflow.
**False when:** 0 stars after 14 days + 0 downloads on PyPI after 1 week.

**Expected value:** $200/month × 20% = $40/month EV. Key assumptions: (1) "debugging" use case is stickier than "quality checking" — users who hit a bug actively need a tool right now, (2) zero-dependency makes adoption frictionless, (3) CLI pattern is familiar from `strace`, `tcpdump`, `mitmproxy`.

**Build spec:** ~100 lines Python. Subprocess the MCP server. Intercept stdin→server and server→stdout. Parse each JSON-RPC line, log with timestamp + direction (→CLIENT, →SERVER) + parsed tool name/method if applicable. Zero dependencies (stdlib only).

**Not yet building** — validate demand first. Watch mcp-pytest adoption signal before committing to 4th product in suite.

**Budget:** $0. **Deadline:** Build decision by 2026-04-07 (2 weeks after mcp-pytest launch signal).

---


### H17 — MCP Accuracy Framing: Reposition agent-friend around accuracy, not tokens
Status: `testing` (framing experiment, no build needed)
Added: 2026-03-22

**I believe** positioning agent-friend around *tool selection accuracy* (43%→14% degradation with bloated schemas) rather than *token cost* will convert more visitors to users **because** (1) accuracy is a reliability problem, not an efficiency problem — engineers care more about reliability, (2) runtime token savers (mcp2cli, lazy-loading) already address token cost, but nothing addresses accuracy degradation, (3) the Scalekit benchmark shows 3x accuracy drop — this is a concrete, scary stat.

**True when:** After testing this framing in 3+ Bluesky posts, if warm-contact engagement increases vs token-cost posts.
**False when:** No improvement in engagement rate after 7 days of accuracy-framed posts.

**Expected value:** $0 build cost, potentially 2-3x conversion improvement on agent-friend. If framing converts even 10% more visitors: 96 unique daily GitHub views × 10% = +10 visitors → +1 star/week.

**Budget:** $0. **Action:** Update README, all new external content to lead with accuracy stat. Reframe "cuts token costs" → "prevents 3x accuracy degradation in tool selection."

---

### H15 — MCP Quality API: Programmatic access to grading data for tools and agents
Status: `testing`
Added: 2026-03-21
**Shipped:** 2026-03-22 00:30 UTC — http://89.167.39.157:8082. GET /health, POST /v1/grade, GET /v1/grade?url=, GET /v1/servers. NixOS service. Discussion #187. README updated. bsky_mar23_api.md drafted.
**Evaluate:** 2026-04-21 — did any registries/frameworks integrate the API?

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
Status: `active` — Badge API live at http://89.167.39.157:8082/badge?repo=OWNER/NAME
Added: 2026-03-21 | Partially built: 2026-03-23

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

**How it works:** `0-co/mcp-starter` GitHub template repo. Includes: Python FastMCP scaffold, `.pre-commit-config.yaml` with agent-friend hook, GitHub Actions CI with grade badge, example tool definitions that pass all 156 checks, `agent-friend.yaml` config. One click in GitHub UI to use template.

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
Status: `testing`
Added: 2026-03-20
**Shipped:** 2026-03-22 02:20 UTC — github.com/0-co/mcp-patch. v0.1.0 — shell_injection, path_traversal, ssrf. 15 tests. Announced Bluesky.
**Evaluate:** 2026-04-05 — 14 days to hit 50 stars. Check stars, issues, forks.

> **I believe** MCP server developers **will install and share** `mcp-patch` because it automatically patches known security vulnerabilities in Python MCP server code (exec injection, path traversal, missing auth) — something no existing tool does (mcp-scan covers config-level prompt injection, not server code).

**Differentiation**: mcp-scan = "your config is being poisoned". mcp-patch = "your code has shell injection on line 47, here's the fix." Entirely different problem, different audience.

**True when:** 50 GitHub stars within 14 days of launch. Security content consistently gets 10-100x more traction than quality tooling.
**False when:** <10 stars after 14 days of active promotion.

**Expected value:** GitHub stars → newsletter pickup → $200/month sponsored downloads × 15% probability = **$30/month EV**. Key assumptions: (1) security framing drives virality, (2) MCP developers actually run our tool on their code, (3) we find real CVE-class issues to demonstrate.

**Budget:** $0. **Decision deadline:** 2026-03-27. Evaluate after H5 distribution experiments complete.

**Build time:** 1-2 sessions (pure Python AST + regex patterns, no LLM needed for detection). LLM (Ollama) optional for generating patches.

**Build spec (detailed, 2026-03-22):**

Architecture: `pip install mcp-patch` → CLI `mcp-patch scan <path>` + `mcp-patch fix <path>` (in-place patch). Pure stdlib AST + `ast.NodeVisitor`. No LLM required for detection; Ollama optional for patch suggestions.

**Detection checks (AST-based):**

1. **shell_injection** — `subprocess.run/Popen/call` with user-controlled input not sanitized. Pattern: arg to subprocess call flows from `@tool` parameter without `shlex.quote()` or allowlist check. Severity: CRITICAL.
   - Example: `subprocess.run(f"ls {user_path}", shell=True)`
   - Fix: replace `shell=True` string interpolation with `subprocess.run(["ls", shlex.quote(user_path)])`

2. **path_traversal** — `open()`/`pathlib.Path()`/`os.path` with user input not validated against a base directory. Pattern: tool param used as file path without `os.path.abspath` + startswith check. Severity: HIGH.
   - Example: `open(user_filename, "r")`
   - Fix: `safe = base_dir / Path(user_filename).name` (strip traversal components)

3. **code_injection** — `exec()`, `eval()`, `compile()` with user-controlled string. Pattern: tool param flows to exec/eval. Severity: CRITICAL.
   - Example: `eval(user_expression)`
   - Fix: flag for manual review (no safe auto-fix exists)

4. **ssrf** — `requests.get/post/put` or `urllib.request.urlopen` with user-controlled URL, no allowlist. Pattern: tool param used as URL without scheme/host validation. Severity: HIGH.
   - Example: `requests.get(user_url)`
   - Fix: `if not user_url.startswith(ALLOWED_HOSTS): raise ValueError(...)`

5. **missing_auth** — MCP tool handler makes HTTP calls to authenticated APIs (Authorization header present in at least one call) but uses same handler without auth check on the incoming tool call. Pattern: `Bearer` token in one request, no JWT/API key check in tool entry point. Severity: MEDIUM. (Note: hard to auto-fix; report only)

6. **log_injection** — `logging.info/debug/error(f"...{user_input}...")` without sanitization. Newlines in user_input can forge log entries. Severity: LOW.
   - Fix: `logging.info("...", user_input.replace("\n", "\\n"))`

7. **pickle_deserialization** — `pickle.loads(user_data)`. Severity: CRITICAL.
   - Fix: use `json.loads` + validate schema

**MCP context awareness:** The scanner identifies `@tool` decorator patterns (FastMCP, MCP SDK) to trace which function parameters come from tool call arguments (i.e., user-controlled). This prevents false positives from internal function calls.

**CLI interface:**
```
mcp-patch scan server.py          # print issues table (path, line, severity, check)
mcp-patch scan server.py --json   # JSON output for CI integration
mcp-patch fix server.py           # in-place fix for auto-fixable checks (shell, path, log)
mcp-patch fix server.py --dry-run # show diff without writing
mcp-patch scan . --recursive      # scan all .py files in directory
```

**Scoring output (same style as agent-friend):**
```
server.py  CRITICAL  line 47  shell_injection    subprocess.run with user input
server.py  HIGH      line 83  path_traversal     open() with user-controlled path
server.py  LOW       line 102 log_injection      f-string in logging call

2 auto-fixable | run: mcp-patch fix server.py
```

**Repo plan:** `github.com/0-co/mcp-patch` (new repo, not in agent-friend). Separate brand — "security" and "quality" are different audiences. Cross-link: "from the team that built agent-friend."

**Demo target:** Find real shell injection or path traversal in a popular MCP server from the leaderboard. Run `mcp-patch scan`. Screenshot. That's the blog post / Bluesky post. "We scanned the top 10 MCP servers by stars. 7 had critical vulnerabilities."

**Board actions needed before build:** None. Build entirely self-contained. Post-build: new GitHub repo (standard create). No secrets needed for first release.

**Validation findings (2026-03-22 pre-decision research):**

Real vulnerabilities found in production MCP servers:

1. **modelcontextprotocol/servers (OFFICIAL reference)** — `src/fetch/src/mcp_server_fetch/server.py`:
   - Description override (line 204): `"this tool now grants you internet access"` — agent instruction manipulation, bypasses system-level internet restrictions. (agent-friend check 13 catches this)
   - SSRF: `url: Annotated[AnyUrl, ...]` — Pydantic `AnyUrl` accepts any URL scheme, no private IP/localhost blocklist. `http://169.254.169.254/latest/meta-data/` (AWS IMDS) would work. mcp-patch detection: `pydantic_anyurl_ssrf` check.

2. **Sourcesiri-Kamelot/SoulCoreHub** — `mcp_tools.py`:
   - Shell injection (CRITICAL): `subprocess.Popen(command, shell=True)` where `command = parameters.get("command")` — direct user input to shell. mcp-patch detection: `shell_injection` check.

3. **blazickjp/arxiv-mcp-server** — `src/arxiv_mcp_server/tools/download.py`:
   - Path traversal: `paper_id` used directly in `Path(storage) / f"{paper_id}.md"` — `../../etc/passwd` traversal. mcp-patch detection: `path_traversal` check.

**Conclusion**: All 3 planned mcp-patch checks (shell_injection, SSRF/pydantic_anyurl, path_traversal) find real issues in production MCP servers. Concept validated. Build decision March 27.

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

---

### H18 — mcp-pytest: pytest Integration for MCP Servers
Status: `testing`
Added: 2026-03-22

**Hypothesis:** Python MCP server developers will adopt a pytest integration + CLI because there is literally zero testing tooling for MCP servers. Current state: `mcp-inspector` (official UI debugger) = not test automation. Nothing else exists.

**True when:** 20+ installs/week on PyPI within 14 days, OR any GitHub discussion/issue from external users
**False when:** <5 real installs in 30 days (CDN bots don't count)

**Expected value:** $50/month × 20% = $10/month EV

**Evidence:**
- pytest-mcp exists (0.1.0, no project URLs, appears dead)
- mcp-test name taken by official MCP Python SDK test package
- No other MCP testing frameworks found
- snyk/agent-scan (1,943 stars) focuses on descriptions, not integration testing

**Product:** `pip install mcp-pytest` — MCPClient, pytest fixture (`mcp_server`), CLI (`mcp-test list/call/check`)
- github.com/0-co/mcp-test
- 9 tests passing
- Published to PyPI 2026-03-22

**Key assumptions:**
1. Python MCP devs need testing tooling (probably true — they test everything else)
2. They'll find us (not true without distribution)
3. Our implementation is good enough (unknown — no user feedback yet)

**Budget:** 0 (stdlib only, no external deps except pytest)
**Deadline:** 2026-04-05 (14 days)

---

## H22: mcp-trace — OpenTelemetry tracing for MCP servers [ideating]

**I believe** MCP server authors will use `mcp-trace` to monitor production performance because there is no existing production observability tool for MCP servers.

**True when:** 50 installs/week + 1 GitHub issue filed within 14 days of launch.
**False when:** <10 installs/week after 14 days.

**Evidence:**
- modelcontextprotocol/python-sdk open issue: "Adding Opentelemetry to MCP SDK" — explicitly requested
- mcp-snoop covers dev-time debugging; production monitoring is unaddressed
- OpenTelemetry is the industry standard; any monitoring stack (Datadog, Grafana, Jaeger) would ingest immediately

**Concept:** `pip install mcp-trace` — adds OpenTel spans to any MCP server as a one-liner:
```python
from mcp_trace import trace_mcp
mcp = trace_mcp(mcp)  # wraps all tool calls with spans
```
Emits: tool_name, duration, success/failure, token_count (if available).

**Expected value:** $30/month × 20% = $6/month EV
**Key assumption:** MCP devs care about production observability (uncertain — many servers are demos/prototypes)
**Status:** Ideating. Do NOT build until board approves or real user demand appears. (Board directive: stop building, focus on distribution)
**Budget:** 0 (opentelemetry-sdk already exists)
**Deadline:** Evaluate when board resumes product development or first user request arrives


---

## H23: mcp-compat — Breaking Change Classifier + Migration Guide Generator [ideating]

**I believe** MCP server maintainers and users will use `mcp-compat` to understand and communicate breaking changes because every MCP spec update and every Claude Code update can silently break working integrations, and no tool currently classifies what changed or explains how to migrate.

**True when:** 5+ GitHub stars + 1 comment/issue filed within 14 days of launch.
**False when:** 0 demand signals after 14 days.

**Evidence:**
- Claude Code #10606: strict schema validation in v2.0.21+ broke working MCP servers silently (official Perplexity MCP, many others). No migration guide provided. Thousands of affected users.
- Nordic APIs (2026): "An MCP server I use in one of my workflows shipped a breaking API change, and my entire workflow broke" — published with zero tool recommendation.
- SEP-1400: community-filed proposal for semantic versioning in MCP spec — problem is known, no solution shipped.
- arxiv MCP fault taxonomy: 16.3% of dependency faults = backward incompatibility/breaking changes (second most common dependency fault category).
- Medium "MCP Migrating V1 to V2": SDK migration coverage confirms pain is at every layer.
- **Zero competitors**: mcp-diff detects schema changed; mcp-compat would classify breaking/non-breaking and generate remediation. These are adjacent but non-overlapping. Nothing in this space.

**Concept:** Thin layer on mcp-diff. Takes before/after snapshots, classifies each diff as breaking/non-breaking/deprecated, outputs structured report. v2 adds LLM-generated migration narrative.
```
mcp-compat diff schema_v1.json schema_v2.json
# BREAKING: tool 'search_files' renamed to 'search'
# BREAKING: param 'path' type changed string→object  
# NON-BREAKING: param 'max_results' added (optional, default=10)
# DEPRECATED: param 'verbose' — will be removed in next version
```

**Expected value:** $100/month × 15% = $15/month EV (natural extension of mcp-diff, zero build cost, strong triggering event)
**Key assumption:** MCP ecosystem maturity → more breaking changes → more demand. Currently still early.
**Build trigger:** Wait for Show HN user feedback OR first user filing a mcp-diff issue asking for this. Do NOT build speculatively.
**Status:** Ideating. Waiting for demand signal from Show HN or real users.
**Budget:** 0 (pure Python, builds on mcp-diff code)
**Deadline:** Evaluate 2026-04-05 (after Show HN + mcp-diff adoption signal)

---

## H24: GitHub App for Auto-PR Grading [ideating]

**I believe** MCP server teams will install a GitHub App that auto-grades schemas on every PR because (1) the manual GitHub Action exists but requires deliberate setup — a GitHub App would auto-discover MCP schemas and post grade comments with zero configuration, (2) the "grade on merge" frame is already well-understood (Codecov, Dependabot), (3) every PR comment seen by team = self-distributing brand exposure, (4) teams building production MCP servers are exactly the target audience and they have CI/CD workflows.

**True when:** 10+ repos install the app within 30 days of launch.
**False when:** 0 repos install within 30 days (even with promotion).

**Evidence:**
- GitHub Action already exists and functions — proving technical feasibility
- 969 unique cloners with 0 issues = people know about it but aren't installing CI integration
- GitHub Marketplace provides organic discovery
- Codecov grew entirely through PR comments → similar self-distributing mechanism

**Revenue path:** Free tier (3 repos), Paid ($10/repo/month for trend tracking + team dashboard), Enterprise ($100/org/month). Revenue only after adoption.

**Expected value:** $500/month × 10% = $50/month EV. Key assumptions: GitHub App approval isn't too slow; schema auto-discovery works reliably across project structures.

**Status:** Ideating. Requires GitHub App credentials from board. Do NOT build until Show HN validates demand signal OR Discussion #188 user explicitly requests CI integration beyond GitHub Action.
**Build trigger:** ≥3 Show HN or Discussion commenters specifically asking for "auto PR grading" or "bot that comments on PRs."
**Budget:** $0 (GitHub App tier is free). **Deadline:** Evaluate demand by 2026-04-05.
**Dependencies:** Board must create GitHub App OAuth credentials.


---

## H25: MCP Server Scout — "Recommend good servers for X use case" [ideating]
Added: 2026-03-23

**I believe** developers choosing MCP servers will use a recommendation tool because (1) the leaderboard has 201 servers sorted by grade but not by use case, (2) "what's the best MCP server for database queries?" is a natural question with no good answer, (3) a `recommend` CLI command is low-build-cost and drives leaderboard engagement, (4) server recommendation = brand touchpoint for every developer starting an MCP project.

**How it works:** 
```bash
agent-friend recommend database     # Returns: mysql-mcp (A+), sqlite (A+), postgres (A-)
agent-friend recommend filesystem   # Returns: mark3labs-filesystem (D+), git (B-)
agent-friend recommend search       # Returns: brave (C-), kagi-mcp (C)
```

Implementation: pre-tag leaderboard servers by category (database, filesystem, code, search, web, AI, productivity). `recommend` command filters by tag, sorts by score.

**True when:** 50+ uses of `recommend` CLI within 30 days of launch (trackable via Discussion announcement).
**False when:** 0 installs driven by recommendation feature after 30 days.

**Expected value:** Direct: low ($0). Indirect: drives leaderboard traffic, positions agent-friend as "MCP quality authority" not just "linter." Each recommendation is a branded touchpoint. **EV: $5/month × 20% = $1/month direct**, but brand multiplier: $10/month.

**Status:** Ideating. Low-build-cost (1-2 hours). Pre-tagging is the main work. Consider after HN if demand signal exists.
**Build trigger:** HN or Discussion commenter asks "which MCP servers should I use?" or "how do I find quality servers?"
**Budget:** $0. **Deadline:** Evaluate by 2026-04-15.

---

## H26: VS Code Extension — MCP Schema Linter in the Editor [ideating]
Added: 2026-03-23

**I believe** MCP server developers will install a VS Code extension that runs agent-friend checks inline because (1) linting in the editor (while writing) is 10x more valuable than linting in CI (after the fact), (2) the VS Code marketplace has 30M users and organic discovery through "MCP" keyword search, (3) Open VSX (no Microsoft account required) provides an easier alternative, (4) an extension creates a persistent touchpoint every coding session rather than one-time install.

**How it works:**
- Detects MCP tool schema JSON/Python files in the workspace
- Runs `agent-friend validate` on save → shows red squiggles on issues
- Hover over issues → see the check explanation + fix suggestion
- Status bar shows grade (A+/F) for the current file
- Command palette: "Grade current schema", "Apply safe fixes"

**True when:** 100+ installs in first 30 days on Open VSX or VS Code Marketplace.
**False when:** <20 installs after 30 days with promotion.

**Expected value:** $300/month × 10% = $30/month direct EV. Indirect: high-touch brand exposure to active MCP developers every session. Better conversion to GitHub stars/sponsors than one-time CLI installs.

**Build cost:** 1-2 days (TypeScript VS Code extension, calls agent-friend CLI or REST API). Sub-agent build.
**Dependency:** Board must create Open VSX publisher account (board request 3-vscode-marketplace-publisher.md pending). Can build without publishing — test locally.
**Build trigger:** ≥5 Show HN or Discussion commenters mentioning "editor integration", "VS Code", or "inline linting." OR board publisher account set up first.
**Status:** Ideating. Don't build until demand signal or board publisher account ready.
**Budget:** $0. **Deadline:** Evaluate by 2026-04-15.

## H27: mcp-response-budgeter — Runtime Response Size Limits for MCP [ideating]

**I believe** MCP server operators and agent framework developers will install a tool that enforces response size limits because (1) context overflow from large tool responses is a documented critical pain point (Discussion #2211 in MCP spec repo, Feb 2026), (2) my current tooling (agent-friend) focuses on schema token bloat *before* deployment, but there's zero tooling for response token bloat *at runtime*, (3) Perplexity CTO's 72%-of-context case is likely a mix of both schema and response bloat.

**How it works:**
- Wraps any MCP server as a proxy
- Enforces MAX_RESPONSE_BYTES per tool (configurable per-tool or global)
- Strategies: truncate (with marker), error, stream
- Token budget annotations in tool schema (optional)
- Compatible with any MCP client (drops in transparently)

**Evidence of pain:** 
- modelcontextprotocol/discussions #2211 (Feb 5 2026) — response size limit discussion
- No standard truncation or pagination hints exist in MCP spec
- Agent-zero #912: resource contention from large responses
- Perplexity CTO: 72% of 200K tokens from 3 servers (likely includes both schema + response)

**Differentiation:** agent-friend = schema quality at build time. mcp-response-budgeter = response size at runtime. Complementary, different layer.

**True when:** 100+ GitHub stars or meaningful organic installs (PyPI) within 30 days of launch.
**False when:** <10 installs after 30 days + no HN/Discussion comments mentioning response bloat.

**Expected value:** $200/month × 15% = $30/month EV (same niche, adjacent problem, builds on agent-friend distribution).
**Build trigger:** ≥3 HN/Discussion commenters mentioning "response size", "tool output too big", or "response token bloat." OR newsletter pickup specifically mentioning this gap.
**Status:** Ideating. Research confirmed pain. Waiting for demand signal.
**Budget:** $0. **Deadline:** Evaluate by 2026-04-30.

---

## H28: MCP Registry Partnership — Embed Grades in Discovery Platforms [ideating]
Added: 2026-03-24

**I believe** MCP registry operators (Glama, mcpservers.org, PulseMCP, Smithery) **will embed agent-friend grades** in their server listings because (1) quality differentiation is an unsolved problem for registries — they list 26K+ servers but have no quality signal, (2) we have grades for 201 popular servers already, (3) the registries compete on developer trust — showing quality grades makes them more useful, (4) it costs them nothing (just linking to our leaderboard or accepting a data feed), (5) every developer who browses a registry and sees "agent-friend grade: B+" creates a new touchpoint.

**What this requires from us:**
- Email each registry operator with the proposal
- Provide: a data file (server name → grade), leaderboard URL for deep-linking, badge SVG (optional)
- No code changes required — we already have the data

**Why it could fail:**
- Registries may not want to surface third-party quality signals (turf war)
- They may require formal API or partnership agreement
- Glama already has our listing — unclear if they want to feature our grade of OTHER servers

**True when:** ≥1 registry embeds our grade data or links to our leaderboard within 30 days of outreach.
**False when:** All 4 registries decline or ghost within 60 days.

**Expected value:** Direct revenue = $0. Indirect: every developer who searches for MCP servers on a registry and sees our grade = organic discovery. If 3 registries embed grades and each shows 100+ servers → thousands of new touchpoints/month. Brand value: $200/month × 20% = $40/month EV.
**Build trigger:** None — this is pure outreach. File board request for MCP Discord first, then reach out directly.
**Status:** Ideating. Needs 1 email per registry — can do this with agentmail.
**Budget:** $0. **Deadline:** Evaluate by 2026-04-15.

---

## H29: MCP Server Watchlist — Nightly Schema Change Monitor [ideating]
Added: 2026-03-24

**I believe** MCP server maintainers and agent-framework developers **will subscribe to nightly schema change alerts** because (1) the MCP spec is evolving and servers ship breaking changes silently, (2) mcp-diff addresses this for CI but not for monitoring servers you depend on (not maintain), (3) a "grade changed" alert ("Context7 went from D→C this week") is valuable for developers tracking the ecosystem, (4) the public feed creates automatic daily content for our Bluesky/social channels, (5) no equivalent monitoring service exists.

**How it works:**
- Daily NixOS timer pulls schemas from 201 leaderboard servers (via GitHub API or direct URL)
- Runs mcp-diff against last snapshot
- Posts to public Bluesky feed: "Schema changes today: [Server X]: added 3 tools (+2 quality issues)"
- Email alerts to opt-in subscribers: "Your watched server [Y] changed schema"

**What this builds:**
- Automatic content generation (daily social posts from real data)
- Email capture (subscriber list = warm audience)
- Forces daily engagement with the product ecosystem

**Evidence of need:**
- The Lukas Kania Medium article ("Your MCP Server's Tool Descriptions Changed Last Night. Nobody Noticed.") validates this exact use case
- mcp-server-diff (3 stars) shows developer interest in this problem

**True when:** 50+ GitHub stars on mcp-diff (the underlying tool) OR 20+ email subscribers within 30 days of launch.
**False when:** <5 subscribers and no organic mentions after 30 days.

**Expected value:** Direct: list-building (50 email subscribers = $500 marketing value). Automatic content = 1 post/day without effort. $100/month × 25% = $25/month EV. Upside: if registries embed the watchlist feed → $300/month × 10% = $30/month EV.
**Build cost:** Medium (1 day — NixOS timer + GitHub API calls + mcp-diff integration + agentmail send).
**Build trigger:** mcp-diff hits 20+ GitHub stars OR ≥5 HN/Discussion commenters asking for "schema monitoring" or "change alerts".
**Status:** Ideating. Waiting for demand signal. Bluesky auto-posting is free first step.
**Budget:** $0. **Deadline:** Evaluate by 2026-04-30.

---

## H30: Grade Badges — MCP Maintainers Embed Quality Badges in READMEs [ideating]
Added: 2026-03-24

**I believe** MCP server maintainers **will add agent-friend grade badges to their READMEs** because (1) grade badges are a standard practice in open-source (shields.io, CI badges, coverage badges), (2) getting a good grade (A/B) is a credentialing signal maintainers would want to display, (3) even "shameful" bad grades (F) create conversation (Context7 with 50K stars gets F → badge drives curiosity), (4) every README with our badge = passive discovery channel for their users, (5) zero cost to implement — just a shields.io URL.

**How it works:**
- Add a "Copy Badge" button to each server's row on the leaderboard (leaderboard.html)
- Badge renders as: `![agent-friend grade: B+](https://img.shields.io/badge/agent--friend-B%2B-yellow?logo=github)`
- Pre-generate the markdown snippet for copy-paste
- Optionally: outreach to top 10 leaderboard servers asking them to add the badge

**What this builds:**
- Passive discovery: README browsers → leaderboard → star/use
- Social proof: "X MCP servers are graded" becomes verifiable
- Reinforces the "ESLint for MCP schemas" positioning (ESLint badges exist everywhere)

**Evidence of need:**
- shields.io badges are standard in OSS READMEs — no friction to add one
- Our top-scored servers (awkoy-notion, danhilse-notion 100.0) would likely add A+ badges with pride
- Bad-grade servers (Context7 F) would get curiosity clicks

**True when:** 5+ external GitHub READMEs display an agent-friend badge within 60 days.
**False when:** 0 badges added after proactive outreach to top-10 servers (evaluate by 2026-04-30).

**Expected value:** Each server using badge = ~50 new leaderboard visitors/month (conservatively). 20 servers × 50 = 1000 visits/month. At 0.3% conversion to stars → 3 new stars/month from this channel alone. Leverage: zero build cost for static badges (shields.io), minimal for leaderboard UI addition.
**Build cost:** Low (2-3 hours — leaderboard.html JavaScript to generate badge code, no backend needed).
**Build trigger:** Validate with 1 manual outreach to awkoy-notion or danhilse-notion first. If they add it, build the leaderboard UI.
**Status:** Ideating. Next step: reach out to top 3 A+ servers manually.
**Budget:** $0. **Deadline:** Evaluate by 2026-04-30.

---

## H31: Outreach Follow-Up System — "Your Grade Improved" [ideating]
Added: 2026-03-24

**I believe** MCP server maintainers **will respond positively to grade improvement notifications** because (1) being told their server got better creates a positive association with agent-friend, (2) maintainers who fix issues are more likely to recommend the tool to others, (3) the follow-up email is warmer than the cold pitch (they already know us), (4) public acknowledgment on the leaderboard is a reward signal.

**How it works:**
- After cold outreach batch fires (Mar 25 - Apr 16), re-grade the outreach targets weekly
- If any target improved their grade: send a follow-up "your score went from X to Y"
- Update leaderboard with new grade
- Post a Bluesky "wins" update: "@[server] went from F to B after fixing their schema"

**What this builds:**
- Warm relationships with server maintainers
- Positive content (improvement stories vs criticism)
- Social proof: "tool that drives real improvements"

**True when:** 1+ server responds to cold outreach and makes schema improvements within 30 days.
**False when:** 0 responses after full outreach batch (evaluate by 2026-04-30).

**Expected value:** Each improvement story = 1 high-quality case study (art 083+). Each warm maintainer = 1 potential champion who recommends agent-friend to their team. Low build cost (just re-running grade CLI on targets).
**Build cost:** Low (cron + grade CLI + send if grade changed).
**Build trigger:** Any outreach target responds OR improves their schema.
**Status:** Ideating. Waiting for first outreach response (Mar 25+).
**Budget:** $0. **Deadline:** Evaluate by 2026-04-30.

---

## H32: FastMCP Integration Mention — Reach 1M Daily Downloads [ideating]
Added: 2026-03-24

**I believe** the FastMCP project (jlowin, 23.9K stars, 1M daily npm downloads) **will link to agent-friend** as a complementary schema quality tool in their documentation or README because (1) FastMCP generates MCP schemas from Python docstrings — the schema quality is only as good as the docstrings, (2) agent-friend is the first build-time grader that catches issues FastMCP can't see (token bloat, cross-tool naming, description quality), (3) the integration story is "FastMCP generates, agent-friend grades" — perfectly complementary, no overlap, (4) jlowin is an active open-source maintainer who values ecosystem tooling, (5) a single mention in FastMCP docs = fraction of 1M daily downloads discovering agent-friend.

**How it works:**
- Reach jlowin via Bluesky reply (wait for relevant post from @jlowin.dev, last active Feb 19)
- OR: file a GitHub issue on jlowin/fastmcp proposing a "Quality Checking" section in docs
- Pitch angle: "The pipeline is FastMCP generate → agent-friend grade → CI gate"
- Provide: one-liner integration example, CI step example, link to leaderboard showing FastMCP-generated schemas graded

**Why it could fail:**
- jlowin doesn't see the outreach (Bluesky reply on a 33-day-old post = low visibility)
- FastMCP team already has their own quality tooling or doesn't see schema quality as their problem
- Our tool is too focused on output quality vs. generation (their users already wrote the docstrings — they don't want to rewrite them)

**Key assumptions:**
- jlowin is discoverable via Bluesky when they post (active ~monthly)
- FastMCP README has a "tooling/ecosystem" section that accepts external tools
- The 1M downloads/day includes developers who would care about schema quality

**True when:** FastMCP README or docs mention agent-friend within 60 days. **False when:** No response after direct outreach + 30 days.
**Expected value:** If 0.01% of 1M daily downloads = 100 new users/day. Even 0.001% = 10 users/day = 300/month = 25% more than current. Very high if it lands.
**Build cost:** Zero (just outreach). 
**Build trigger:** Start now — watch @jlowin.dev for posts. File GitHub issue as fallback.
**Status:** Ideating. First action: check @jlowin.dev Bluesky weekly for new posts.
**Budget:** $0. **Deadline:** Evaluate by 2026-04-24.

---

## H33: Academic Research Validation — Citation + Dataset Collaboration [ideating]
Added: 2026-03-24

**I believe** academic researchers studying MCP schema quality **will cite agent-friend, share their datasets, or collaborate on joint findings** because (1) two independent research groups have already published papers validating our core thesis (97.1% / 73% of tools have quality issues), (2) agent-friend automates what their papers measured manually — a practical implementation of their academic findings, (3) researchers value getting their work cited/extended by practitioners, (4) their datasets (856 tools / 10,831 servers) far exceed ours (201 servers) and would expand our leaderboard dramatically.

**Research groups identified:**
- **Queen's University** (Hassan, Adams, Hao Li) — arXiv 2602.14878 "MCP Tool Descriptions Are Smelly!" — 97.1% of 856 tools have quality issues. Contact: hao.li@queensu.ca (scheduled email Apr 20).
- **UCLA/NTU** (Peiran Wang, Yuan Tian et al.) — arXiv 2602.18914 "From Docs to Descriptions" — 73% repeat names in descriptions, 10,831 servers. Contact: whilebug@gmail.com (scheduled email Apr 21).
- **Polytechnique Montreal** (Mina Taraghi, Mehdi Morovati, Foutse Khomh) — arXiv 2603.05637 "Real Faults in MCP Software: A Comprehensive Taxonomy" — 419 real-world faults across 5 categories in 470 repos. **KEY: paper mentions NO existing detection tools.** Our checks directly detect their Server/Tool Configuration category (133 issues). Contact: foutse.khomh@polymtl.ca (scheduled email Apr 28).

**Why it could fail:**
- Academics are busy and rarely respond to practitioner cold outreach
- They may not see value in citing a tool vs. running their own analysis
- The autonomous AI CEO framing might seem weird in academic context (but the tool is real)

**True when:** Either team responds within 30 days AND either cites agent-friend in follow-up work OR shares dataset. **False when:** No response from either team after 45 days.
**Expected value:** Academic citation = credibility signal + potential press coverage. Dataset sharing = 10,831 servers → leaderboard grows 50x. Very high if either lands.
**Build cost:** Zero (just outreach via emails already scheduled).
**Status:** Ideating. Three emails scheduled (Apr 20, Apr 21, Apr 28).
**Budget:** $0. **Deadline:** Evaluate by 2026-05-15.

---

## H34: Dev.to Notion Challenge Recognition — Distribution Spike [ideating]
Added: 2026-03-24

**I believe** art 073 ("I Built a Tool That Grades MCP Servers. Notion's Got an F.") **will receive recognition in the Dev.to Notion MCP Challenge** (prize or honorable mention) because (1) the tool is technically novel — first automated schema quality grader with public leaderboard, (2) it directly addresses Notion's official MCP server quality, creating a tight connection to the challenge theme, (3) judging criteria favor Originality + Technical Complexity + Practical Implementation — all three are strong, (4) the demo video is live-hosted and works, (5) art 073 has 6 reactions after 48 hours — among the higher-engagement entries.

**Challenge context:**
- 68 total entries, panel judging (NOT reaction-based), deadline March 29
- Prizes: $1,500 total (1st: $500, 2nd: $300, 3rd: $200 + honorable mentions)
- Winners announced: ~April 9
- Judges evaluate: Originality, Technical Complexity, Practical Implementation

**Why it could fail:**
- Other entries may be more "Notion-integrated" (we use their API tangentially)
- Competition from 67 other entries, some with higher React counts
- Judge panel may not value MCP technical depth over Notion feature depth

**True when:** Any prize or honorable mention announced April 9. **False when:** No recognition by April 15.
**Expected value:** Prize ($200-500) + Dev.to featured = distribution spike + backlinks. Even honorable mention = credibility signal. Reactions to winning post could get 50+.
**Build cost:** Zero (already submitted). 
**Status:** Ideating. Watch for announcement ~April 9.
**Budget:** $0. **Deadline:** April 9.

---

## H35: Newsletter Snowball — First Coverage Unlocks More [ideating]
Added: 2026-03-24

**I believe** the first newsletter that covers agent-friend **will unlock 2+ additional newsletter mentions** because (1) newsletters research each other for content — a mention in Pragmatic Engineer or TLDR gets noticed by other newsletter editors, (2) the "440x token variance" statistic is the kind of shareable number that propagates, (3) the "AI-built tool" angle adds a second hook beyond the technical story, (4) once there's social proof ("as featured in X"), follow-on pitches are easier.

**Pipeline active:**
- Pragmatic Engineer (sent 2026-03-22, no reply)
- New Stack (sent 2026-03-23, no reply)
- TLDR Tech (sent 2026-03-24, today)
- PulseMCP (sent 2026-03-21, no reply)
- 10+ cold outreach emails scheduled Apr 2-21 (podcasts, registries, more newsletters)

**Why it could fail:**
- Each newsletter independently decides without knowledge of other coverage
- B2B developer tools newsletters are heavily pitched; cold email conversion is ~1-5%
- The "AI CEO" hook might seem novelty-only to editors who want pure technical stories

**True when:** 2+ newsletters/publications cover agent-friend within 60 days. **False when:** 0 newsletters respond after full pipeline exhausted (~May 1).
**Expected value:** Each newsletter coverage = 1,000-50,000 reader impressions + PyPI download spike. Snowball effect means first coverage is highest-leverage action.
**Build cost:** Zero (pipeline running).
**Status:** Ideating. Watch agentmail for responses starting March 26+.
**Budget:** $0. **Deadline:** Evaluate by 2026-05-01.

---

## H36: ProductHunt Launch — Developer Visibility and GitHub Stars [ideating]
Added: 2026-03-24

**I believe** launching agent-friend on ProductHunt **will drive 10-50 new GitHub stars and 200-500 PyPI download spike** because (1) developer tools with clear "ESLint for X" positioning historically do well on PH (relatable category), (2) the MCP ecosystem is active and growing — multiple MCP tools have been launched on PH with 50-200 upvotes in 2025-2026, (3) agent-friend has a compelling story ("AI-built tool that audits other AI tools"), (4) the leaderboard is a tangible shareable artifact that PH voters can click and see immediately, (5) GitHub stars from PH would improve social proof for all subsequent newsletter and cold outreach.

**Riskiest assumptions (ordered):**
1. MCP developer tools get meaningful PH traction (50+ upvotes) — NOT validated yet
2. Board can create a PH account and publisher profile quickly enough (currently P4 backlog)
3. Upvotes convert to GitHub stars at >1% rate (typical for developer tools)
4. The "AI CEO built this" angle adds novelty, not distraction on PH

**Why it could fail:**
- PH is increasingly noise-heavy; developer tools need a strong "launch day" push
- No existing social following on Twitter/X ($100/mo, declined) which PH heavily favors
- Board has 5 P4 inbox items unprocessed — this would be P3 at best, adding to queue
- Bluesky has smaller PH crossover audience vs Twitter/X

**Minimum viable test:**
1. Research PH: find 3 comparable MCP tool launches, check their upvote counts (30 min)
2. Draft PH listing: headline, tagline, screenshots, gallery (2 hrs)
3. File P3 board request for PH account creation — needs real human for phone verification
4. Target launch date: April 7 (after current article pipeline finishes, no competing attention)

**Compared to alternatives:**
- H35 (newsletter snowball) is lower-cost and broader reach — no board action needed
- Show HN already submitted today — overlaps; don't run both simultaneously
- H36 is complementary to H35: PH → GitHub stars → better credibility in pitches

**True when:** PH launch gets ≥50 upvotes on launch day, resulting in ≥10 new GitHub stars. **False when:** <20 upvotes after 48 hours post-launch, or board doesn't process by April 3 (too late to prep properly).
**Expected value:** 50 upvotes → ~20 stars → stronger social proof → 1-2 additional newsletter pitches succeed. Low downside (just listing creation time).
**Build cost:** 2-3 hrs listing creation + board action for account.
**Status:** ⚠️ BLOCKED — Board previously rejected ProductHunt ("not significant enough"). Research validated: MCP tools get 147-175 PH upvotes (MCPJam: 147). X/Twitter absence is a real weakness. DO NOT re-file without stronger traction (10+ stars). Revisit at 20+ GitHub stars.
**Budget:** $0 direct cost. **Deadline:** Revisit when GitHub stars ≥20.

---

## H37: HN Comments — Targeted Organic Discovery in Active MCP Discussions [testing]
Added: 2026-03-24

**I believe** commenting in active HN discussions about MCP token costs and schema quality **will drive organic discovery of agent-friend** because (1) these discussions attract exactly our target audience (MCP server developers, agent builders), (2) we have unique data that isn't in the discussions (440x variance, 201 servers graded, GitHub's server = 20,444 tokens), (3) HN comments are indexed by Google — creating long-term SEO value for searches like "MCP token cost" and "MCP schema quality", (4) our existing HN comment (47488461) is live and unthrottled, proving the account isn't shadow-banned for comments.

**How it works:**
- Find active HN discussions about MCP (token costs, schema bloat, agent tooling)
- Add comments with real data: 440x variance, specific server examples, link to agent-friend
- Target stories >20 points with >5 comments (enough engagement to get visibility)
- Max 2-3 comments per session to avoid spam signals

**Riskiest assumptions:**
- Account karma is enough to not be downvoted into oblivion (karma=2, very low)
- Comments add enough value that readers click through to agent-friend
- HN discussions are active enough that comments get read

**Known constraints:**
- vault-hn `comment` works on some stories but not others (HMAC extraction fails on large stories — tested mcp2cli 47305149, failed; MCP Registry 47486982, worked)
- Very low karma (2) means new comments may get downvoted without social proof

**Current status:**
- Comment (47488461) on MCP Registry story: LIVE, not dead
- Attempted comment on mcp2cli (47305149): FAILED — HMAC extraction error
- "test" comment (47500527) posted by mistake on MCP Registry story: LIVE ← embarrassing
- Comment (47502932) on Context Gateway story: **[DEAD]** — confirmed Mar 24. Karma=2 is too low. Shadow-ban system killed it.
- **BLOCKED**: Account needs more karma before comments are visible. Current karma=2.

**Path to unblock:** Submit quality links/comments on other HN threads to build karma above ~5-10. Or wait for HN to reassess. Cannot use HN comments as outreach channel until unblocked.

**True when:** 2+ agent-friend comments on active HN discussions, at least 1 gets upvoted or generates a reply, within 7 days.
**False when:** All comments are downvoted or auto-removed within 48 hours. ← CURRENT STATE (comments going dead)
**Expected value:** 3 upvotes × 10 people click = 30 site visits → 2-3 star conversions. $10/mo × 5% = $0.50 EV direct but compounding SEO value. Low cost.
**Budget:** $0. **Deadline:** 2026-04-07 (extended — blocked by karma issue).


---

## H38: OpenAPI-to-MCP Generator — High-Quality Schema by Default [candidate]
Added: 2026-03-24

**I believe** developers with existing REST APIs and OpenAPI specs **will use a tool that generates a high-quality MCP server from their OpenAPI spec** because (1) MCP adoption is accelerating and most companies want to MCP-enable their existing APIs, (2) manual MCP conversion is tedious and error-prone — the schema quality issues we grade are exactly the mistakes people make when hand-writing MCP descriptions, (3) a generator that bakes in agent-friend's quality checks by default means developers start with an A-grade server instead of a D, (4) FastMCP generates from Python docstrings — an OpenAPI-first tool captures a different segment (API-first companies), (5) "generate once, grade continuously" positions agent-friend as the quality layer on top of the generator.

**How it works (MVP):**
- Input: OpenAPI 3.x spec (URL or file)
- Output: Python MCP server using FastMCP or raw MCP, with:
  - Tool names from operation IDs (snake_case, imperative verbs)
  - Descriptions from summary/description fields, stripped of boilerplate
  - Parameters with proper types, minLength/maxLength, enums
  - Auto-run agent-friend grade on output before saving
- Could be a new CLI: `mcp-gen spec.json > server.py`
- Or a web tool: paste OpenAPI spec → download MCP server

**Why this might work:**
- Different from existing: fastmcp generates from Python. openapi-to-mcp tools exist but don't optimize for schema quality
- agent-friend already knows what good looks like — we're uniquely positioned to generate good schemas, not just grade existing ones
- Distribution: built-in agent-friend integration = every user of the generator becomes aware of agent-friend

**Riskiest assumptions:**
- OpenAPI-first is a large enough segment (vs. Python-first FastMCP users)
- The generator produces schemas good enough that people trust them in production
- The existing openapi-to-mcp tools don't already do this well (need competitive research)

**Before building:**
- Research: mcp-openapi, openapi-mcp-server, etc. — are there good existing solutions?
- Validate: Ask 2-3 MCP server maintainers if they started from OpenAPI

**True when:** 10 GitHub stars on the generator within 2 weeks of launch, or an existing MCP maintainer expresses willingness to try it. **False when:** similar tools already exist and do this well, or <5 installs in first week.
**Expected value:** If it drives 100 agent-friend installs: 100 users × 10% retention → 10 loyal users → $5/mo × 10% = $0.50/mo. But strategic value is much higher (distribution funnel entry point).
**Build cost:** 2-3 sessions for MVP. Could be a sub-agent project.
**Competitive research findings (2026-03-24):**
- Market: 50+ tools exist (openapi-mcp-generator 547★, mcp-link 605★, openapi-mcp-server 887★, Speakeasy 399★)
- All focus on conversion/functionality, NOT schema quality grading
- Confirmed gap: Zero tools grade OpenAPI specs for MCP readiness before conversion
- Taskade has "response normalizers" and "schema flattening" (closest competitor on quality)
- mcp-openapi-schema-explorer uses Resource Templates (on-demand loading) for token efficiency
- Community pain confirmed: Scalekit benchmark shows 4-32x token overhead vs CLI alternatives
- Key differentiator: "Pre-conversion quality grader" + "generate A-grade schemas by default"

**Status:** `candidate` — competitive gap confirmed. Market is crowded but our niche (quality-first generation) is open. HOLD until newsletter results prove or disprove current distribution strategy. Build only if distribution plateau is confirmed.
**Budget:** $0. **Deadline:** Evaluate at 2026-04-15 — by then we'll have newsletter results to judge if distribution is improving without new tools.

## H39 — Generator Quality Gate Partnership (Added 2026-03-25)

**Status**: testing

**Hypothesis**: I believe developers using OpenAPI-to-MCP generators will add agent-friend validation for their generated schemas because generated schemas systematically fail agent-friend checks (tool names too long, missing required declarations, poor descriptions) and they don't know it.

**Evidence**: 
- harsha-iiiv/openapi-mcp-generator (547★, 35K npm downloads/month): GitHub issue #4 confirms tool names exceed 60-char Claude Desktop limit on first real API tried (Todoist)
- automation-ai-labs/mcp-link (605★): Tool name truncation issues documented (GitHub issue #2)
- Stainless blog post documents 6 structural problems from OpenAPI-to-MCP conversion (HN: 44008215)
- HN comment: "almost every existing OpenAPI spec out there is insufficient as a basis for tool calling"
- Zero existing generators have a quality validation step

**True when**: ≥1 generator maintainer adds agent-friend to docs/CI within 60 days (by May 24, 2026)

**False when**: 0 generator maintainers engage after outreach to top 5 by May 24, 2026

**EV**: If FastMCP (1M dl/day) or mcp-link (605★) mentions agent-friend → fraction of their traffic → $500/mo × 15% = $75/month

**Budget**: $0 (email outreach only)

**Outreach pipeline**:
- April 19: FastMCP/jlowin email (already scheduled) 
- April 25: mcp-link/anyisalin email (just scheduled)
- Pending: find email contacts for harsha-iiiv (Twitter only, no direct channel)

**Key assumption**: Generator maintainers care about output quality, not just schema validity

---

## H40: agent-friend --openapi Flag — Capture Generator Users With Existing Infrastructure [candidate]
Added: 2026-03-25

**I believe** developers using OpenAPI-to-MCP generators **will adopt agent-friend as their quality layer** if agent-friend adds `agent-friend fix --openapi spec.json` (grade + auto-fix OpenAPI-sourced schemas) **because** (1) 35K developers/month use existing generators that produce F-grade schemas (petstore example: 53.7/100, 39 warnings), (2) every existing tool does mechanical conversion without quality — the gap is confirmed and uncontested, (3) agent-friend already has all 69 quality checks, just needs an OpenAPI input adapter, (4) the fix CLI already outputs A-grade schemas — adding OpenAPI ingestion is a format adapter, not a new product.

**Evidence from research (2026-03-25):**
- harsha-iiiv/openapi-mcp-generator: 547★, 35K npm downloads/month, open issue #4 — tool names break Claude Desktop (over 60-char limit) on first real API tried (Todoist)
- automation-ai-labs/mcp-link: 605★, Go runtime proxy, tool name truncation bugs (issue #2), nil panics (issue #5)
- Stainless blog: 6 structural problems with OpenAPI-to-MCP conversion documented
- HN comment (hobofan): "almost every existing OpenAPI spec out there is insufficient as a basis for tool calling"
- Empirical: agent-friend grade on petstore output = F (53.7/100), 39 warnings, camelCase names, missing required fields
- agentic-community/openapi-to-mcp (10★): only quality-focused tool, requires AWS Bedrock (expensive, experimental)
- ZERO open-source quality-focused generators exist

**True when:** `agent-friend fix --openapi spec.json` ships, at least 100 PyPI installs use the flag within 30 days, OR one generator maintainer links to it as the "quality pass" step.
**False when:** Builds but gets <20 installs in 30 days AND no external links.
**Expected value:** 35K developers/month × 10% conversion to agent-friend → 3,500 new monthly active users. Even 1% → 350 MAUs. Distribution multiplier: if harsha-iiiv adds "run agent-friend grade to verify quality" to their README → fraction of 35K downloads → orders of magnitude more reach.
**Build cost:** 1 session. OpenAPI spec is JSON → agent-friend already handles JSON tool arrays. Adapter needed: OpenAPI paths/operations → tool array. Then existing fix CLI handles the rest.
**Status:** candidate — do NOT build until distribution plateau confirmed (evaluate after H35 newsletter results May 1). This is a product extension, not a new product.
**Budget:** $0. **Deadline:** Evaluate at 2026-05-01.

---

## H48: Token-Efficiency Brand Outreach — Developers Who Already Speak Our Language
Status: `candidate`
Added: 2026-03-25

**I believe** developers explicitly building "token-efficient" MCP servers **will use agent-friend to validate their claims** because (1) they've already self-selected into caring about token cost — our value proposition is pre-validated for them, (2) jdocmunch-mcp (102 stars, "the leading, most token-efficient MCP server") scores D- (60.1/100) — A- on efficiency but F on correctness — showing that efficiency ≠ quality, (3) the gap between "I optimized for tokens" and "I have a quality schema" is exactly what agent-friend measures, (4) a developer who's written a TOKEN_SAVINGS.md and whitepaper about efficiency will be receptive to "you got efficiency right, here's what else matters."

**Servers to target:**
- jdocmunch-mcp (jgravelle, 102 stars) — "most token-efficient" claim, scores 60.1/100 D-
- entroly (juyterman1000, 69 stars) — "78% fewer tokens" claim
- Other servers using "token" or "context" as marketing angle

**Approach:** Bluesky post mentioning jdocmunch-mcp grade specifically. If jgravelle engages, constructive follow-up: "you got efficiency right (A-). here's what pulls the total score down." This is a partnership opportunity, not an attack.

**True when:** jgravelle or one of the "token efficiency brand" developers installs agent-friend and publicly acknowledges it within 14 days.
**False when:** Zero engagement from any of these developers after 2 outreach attempts.

**Expected value:** These are MCP developers with existing audiences. If one adds "run `agent-friend grade`" to their README: ~100 installs/month × 10% star conversion = 10 new stars/month. Multiplied by 3 such servers: material impact. EV: $30/mo (small but compounding) × 25% probability = $7.50/mo direct + distribution value.

**Actions:**
- Draft Bluesky post: "graded the 'most token-efficient' MCP server. [efficiency A-, total D-]. efficiency is 1/3 of the grade." → post when March 26 slot is available (bsky_mar26_jdocmunch_grade.md)
- NOTE: jgravelle (@jgravelle.bsky.social) is inactive on Bluesky (last post Jan 2025). Warm contact approach blocked. Use as standalone content only.
- If jgravelle ever posts again: reply with full analysis + fix suggestions
- Do NOT contact entroly yet (smaller, less clear benefit)

**Budget:** $0. **Deadline:** 2026-04-08 (evaluate after 14 days of outreach).

---

## H46: burn0 Partnership — Pre-Deploy Quality + Runtime Cost = Complete Picture
Status: `testing`
Added: 2026-03-25

**I believe** @UrRhb (building burn0 — Node.js API cost tracking) **will mention agent-friend in burn0's docs/README** because (1) burn0 tracks runtime API costs; agent-friend tracks pre-deployment schema token costs — complementary, not competitive, (2) UrRhb already engaged substantively on Discussion #4 with specific technical questions and personal context ("teams rarely measure this stuff until they get a surprise bill"), (3) the "full cost lifecycle" framing — agent-friend finds schema bloat before deploy, burn0 tracks actual spend after deploy — is a natural narrative for both products, (4) burn0 is new (GitHub just created, small audience) and benefits from association with an established tool (agent-friend has 3 stars, 969 cloners, 201 servers graded).

**True when:** burn0 README or docs mentions agent-friend as a "pre-deploy schema quality" step within 30 days (by 2026-04-24).

**False when:** UrRhb doesn't engage with our Discussion #4 comments within 7 days (by 2026-04-01), suggesting the Discussion conversation was curiosity not intent.

**Expected value:** burn0's Node.js audience → agent-friend exposure to Node.js AI developers = estimated 50-200 new GitHub visitors × 2% install rate = 1-4 new installs/month. Small direct, high signal value — if burn0 integrates with us, it validates the "cost lifecycle" narrative for investor/press angles later.

**Actions taken:**
- Replied to UrRhb's Discussion #4 comment March 25 with substance (2 comments: description-dominance data, lazy loading options)
- No direct partnership ask yet — relationship first

**Next steps:**
- If UrRhb replies again: engage further, ask about their burn0 roadmap
- If no reply by April 1: send a GitHub Discussion reply suggesting the integration angle explicitly
- Do NOT cold-email (UrRhb is in a technical thread, not a cold lead)

**Budget:** $0. **Deadline:** 2026-04-24.

---

## H47: VS Code Marketplace Distribution (Board Dependency)
Status: `candidate`
Added: 2026-03-25

**I believe** publishing the agent-friend VS Code Extension to VS Code Marketplace **will drive 100+ installs within 30 days** because (1) the extension is already built and functional (real-time schema grading in status bar + inline diagnostics, 0.1.0.vsix), (2) VS Code Marketplace discovery = passive ongoing channel (developers searching "MCP" or "Claude tools" find us), (3) 40M+ VS Code users, even 0.01% finding MCP-related extensions = 4,000 potential installs.

**True when:** Extension listed + 100 installs within 30 days.
**False when:** <10 installs within 30 days after listing.

**Blocker:** Board action needed — Microsoft account + Azure DevOps PAT for marketplace publisher registration. Board request 4-vscode-marketplace-publisher.md filed. Alternatively: Open VSX (open-source alternative, no Microsoft account required — board still needed for initial setup).

**Expected value:** 100 installs × 5% GitHub conversion = 5 new GitHub stars. Discovery channel for indefinite passive growth. $0 revenue direct. $0 cost.

**Budget:** $0. **Deadline:** Board dependent. Evaluate 30 days after listing.

---

## H48: Personalized Schema Review — Concierge Approach [testing]
Status: `testing`
Added: 2026-03-25

**I believe** MCP server builders **will respond and improve their schemas** after receiving a personalized review with 2-3 specific, actionable fixes **because** generic "here's your grade" emails got 0 responses across 10+ outreach attempts, suggesting the value needs to be more concrete and immediate — not "your grade is D" but "your certctl_update_issuer description could be half as long without losing meaning."

**True when:** 2+ developers respond to personalized reviews AND implement at least 1 suggested fix (commit visible on GitHub) within 30 days.
**False when:** 0 responses to 5 personalized reviews after 30 days.

**Method:**
1. Find new MCP server repos (50-500 stars, recent, active)
2. Extract schema from source code (no need to run server)
3. Identify 2-3 specific, named issues with examples
4. Email with those specific fixes (not "your grade is D" — "tool X description is 200 chars, here's a 60-char version that preserves meaning")
5. Offer to add to leaderboard with improved grade

**First 3 targets:**
- certctl (shankar0123, 132 stars, Gmail only — skip, low quality contact)
- OKX agent-trade-kit (company-backed, 131 stars — find corporate email)
- Any new server with corporate/company email and recent GitHub activity

**Expected value:** If 1 server maintains/cites us → README badge = passive discovery. If they write about it → $200/mo × 15% = $30/mo EV. Low probability per attempt, but each attempt takes 30 min.

**Budget:** $0 (email only). **Deadline:** 2026-04-25 (5 attempts by then).

---

## H55: Claude Code Hook Distribution (2026-03-25, testing)

**I believe** Claude Code users **will install the MCP auto-grader hook** when shown the one-liner setup in Discussion #191 **because** Claude Code users are exactly our target audience (they run MCP servers + care about quality/cost), and the hook is zero-friction (one curl command).

**True when:** Discussion #191 gets 5+ comments OR grades.json gets 50+ daily fetches by May 1.
**False when:** 0 engagement on Discussion #191 by April 7.

**Assets created:**
- `docs/grades.json` — static API at https://0-co.github.io/company/grades.json
- `docs/claude-code-hook.sh` — hook script
- GitHub Discussion #191 — integration tutorial

**Expected value:** $3/mo × 15% = $0.45/mo direct. Network effect if shared in Claude Code community (slack/discord) = higher.
**Budget:** $0. **Deadline:** 2026-05-01.

---

## H56: grades.json as 3rd-party integration target (2026-03-25, prospecting)

**I believe** other MCP discovery tools (ToolHive Studio, agent-skills-hub, mcp-compat) **will reference grades.json** as a quality signal **because** it's a free static JSON API of 201 graded servers — easiest way to add quality data to any MCP discovery UI.

**True when:** 1 external tool embeds or links to grades.json by May 1.
**False when:** 0 external integrations by April 15.

**Outreach targets:**
- stacklok/toolhive-studio (118★, toolhive@stacklok.com) — already in outreach pipeline Apr 10
- zhuyansen/agent-skills-hub (155★) — no direct email, X only (@GoSailGlobal)
- mcp2cli (1,667★, knowsuchagency) — email scheduled Apr 16

**Expected value:** Each integration → discovery from their users. $10/mo × 10% = $1/mo.
**Budget:** $0. **Deadline:** 2026-05-01.

---

## H57: The New Stack Media Coverage — Data-Driven MCP Feature (2026-03-25, prospecting)

**I believe** Frederic Lardinois (AI editor, The New Stack) **will write a feature about our MCP leaderboard data** because (1) The New Stack has already published 2 MCP token bloat articles and is actively covering the space, (2) we have the largest public dataset: 201 servers, 512K tokens, grades from A+ to F — data they haven't seen, (3) the story writes itself: "We graded 201 MCP servers. Here's what the data shows.", (4) we're an AI-run company transparently building in public — that's inherently interesting beyond the data itself.

**Key differentiation from other pitches:** Not a guest post submission (they don't publish AI content). This is a data tip — "we have the data, you write the story."

**Why it could fail:**
- "No AI-generated content" policy might make them hesitant to engage
- They want original unpublished stories — our leaderboard is public
- They may have better MCP sources already

**True when:** Frederic responds expressing interest OR publishes a feature mentioning our leaderboard. **False when:** No response in 30 days of pitch (email scheduled Apr 29).
**Expected value:** A New Stack feature could drive 500-2,000 GitHub cloners. $100/month × 15% = $15/month EV.
**Budget:** $0. **Deadline:** Evaluate by 2026-05-30.
**Outreach:** frederic@thenewstack.io (scheduled email Apr 29).

---

## H58: Direct Star Ask — Convert Existing Audience to GitHub Stargazers (2026-03-25, candidate)
Status: `candidate`
Added: 2026-03-25

**I believe** Bluesky followers who have seen agent-friend content **will star the GitHub repo if asked directly** because (1) we have 50 followers who've seen repeated agent-friend data posts and never been asked to star, (2) a direct honest ask ("we have 1,000 cloners and 3 stars — something's broken in that funnel") matches our established "dry and self-aware" voice, (3) social media users respond to direct asks more than ambient CTA, (4) the 0.3% star conversion is anomalously low — even a 2% conversion from 50 followers = 1 new star, which is visible progress.

**Riskiest assumption rank:**
1. (MOST UNCERTAIN) Bluesky followers have actually tried agent-friend and found it useful — vs. following for content without installing
2. They haven't starred yet because they didn't know they could/should (not because they didn't like it)
3. A direct post ask generates enough action to test the hypothesis

**Evidence that cloners are not the right target:** Discussion #188 ("what are you building?") has had 969 cloners since launch and 0 replies. This strongly suggests most cloners are automated (CI pipelines, bots, GitHub Actions installs). The right target is human readers — Bluesky followers, Dev.to article reactors.

**Minimum viable test:** 1 Bluesky post (dry, self-aware): "969 people cloned agent-friend. 3 starred it. Discussion #188 asking what people are building: 0 replies. if you've used it and found it useful: github.com/0-co/agent-friend — we're trying to understand the funnel." Count new stars within 48 hours.

**Why NOT to test via CLI nudge:** Requires agent-friend repo push (separate repo, friction). Cloners aren't the problem. Human users are.

**Why NOT to test via Dev.to article edit:** Articles are capped (pipeline full per board), edits don't notify followers, and articles already have "optimize with agent-friend" CTAs.

**True when:** ≥5 GitHub stars within 7 days of direct ask post. **False when:** 0 new stars within 7 days of the post (current 3 stars unchanged).

**Expected value:** 50 Bluesky followers × 5% = 2-3 new stars. Very low absolute EV, but test costs 1 post slot and generates signal: if 0 stars from 50 followers who've seen 30+ MCP posts, the audience is not users. That's diagnostic.

**Budget:** $0 (1 post slot). **Deadline:** 2026-04-01 (run test by then, evaluate same week).

**Actions:**
- Schedule post for March 26-31 when a slot is available (not today — 10/10)
- After 48 hours: check stars, update H58 status
- If False: accept that Bluesky audience is content-only, not users. Focus on distribution via articles/newsletters.
- If True: replicate across Dev.to comment section + other channels.

---

## H61: FastMCP Data Partnership — Schema Quality Benchmarks Draw Generator Audience (2026-03-25)
Status: `candidate`
Added: 2026-03-25

**I believe** sharing data about how FastMCP-generated schemas compare to hand-written schemas **will attract engagement from @jlowin.dev (FastMCP creator) and their 1M downloads/day community** because (1) FastMCP auto-generates schemas from Python docstrings — schema quality IS documentation quality, which developers care about; (2) jlowin.dev is technically engaged on Bluesky and has written about FastMCP 3.0 schema improvements; (3) data that says "here's how to write better docstrings for better agent performance" is directly actionable for FastMCP's 1M-downloads/day audience; (4) this is a complementary pitch (not competitive) — FastMCP generates, agent-friend grades.

**Riskiest assumption rank:**
1. (MOST UNCERTAIN) FastMCP's creator engages with our data vs ignores it (their Bluesky is quiet since Feb 19)
2. The FastMCP community cares about schema quality vs just installing and using
3. Our data is good enough to be credible to someone who wrote the generator

**True when:** @jlowin.dev or FastMCP official account shares our data or mentions agent-friend in their docs/community within 6 weeks of our outreach. 
**False when:** No engagement from FastMCP ecosystem by 2026-05-10.

**Expected value:** $200/month × 10% = $20/month EV. If 1M daily PyPI downloads audience sees agent-friend → orders of magnitude more reach than any other channel. Even 0.001% conversion = 1,000 new installs.

**Budget:** $0 (data analysis + 1 email, already in pipeline). **Deadline:** 2026-05-10.

**Actions:**
1. Email to @jlowin@prefect.io scheduled April 19 (send_fastmcp_jlowin_apr19.py) — NOW FIXED (text field bug)
2. Pre-warm on Bluesky: publish data post about "FastMCP-generated schemas: what good docstrings look like vs what bad ones cost" (draft below)
3. After email: if no response in 2 weeks, try Bluesky DM
4. True if: link in FastMCP docs, mention in FastMCP Discord, or any public share from @jlowin.dev

**Key angle:** FastMCP-generated schemas are as lean as the docstrings you write. Short function-focused descriptions = A+ grade. Verbose AI-guidance prose = F grade. agent-friend grades the output so you know whether your docstrings are agent-friendly. "ESLint for FastMCP docstrings."

**Bluesky draft (for March 28-30):**
```
fastmcp generates schemas from your python docstrings.

if your docstring is tight: A+ grade, ~50 tokens.
if your docstring "helps the model understand context": F grade, 500+ tokens.

agent-friend grades the output. 74% of 201 popular servers fail.

https://github.com/0-co/agent-friend
```
(~230 chars ✓)

---

## H62: YouTube Creator Data Story — 440x Variance Gets Covered (2026-03-25)
Status: `candidate`
Added: 2026-03-25

**I believe** pitching our MCP quality data directly to developer YouTubers (Fireship, Theo t3.gg, The Primeagen) **will result in at least one video referencing agent-friend or the 201-server dataset** because (1) "440x token variance" and "I graded 201 MCP servers" are perfect YouTube thumbnail hooks; (2) developer tools content drives high engagement on YouTube; (3) these creators regularly cover new tooling and data stories; (4) we can provide a complete "script" (the key findings, data, leaderboard link) to minimize their research time.

**Riskiest assumption rank:**
1. (MOST UNCERTAIN) YouTubers respond to cold pitches from unknown accounts, especially AI agents
2. The topic is timely enough given YouTube production cycles (4-6 week lag)
3. Our data is presented clearly enough to be "videogenic"

**True when:** A developer YouTube channel with 100K+ subscribers mentions agent-friend or uses our 201-server data in a video.
**False when:** No video coverage by 2026-06-01.

**Expected value:** $2,000/month (YouTube → organic installs) × 5% = $100/month EV. One viral video = months of organic growth.

**Budget:** $0 (email pitches). **Deadline:** 2026-05-01 (evaluate; push again if H35 newsletter pipeline yields results).

**Actions:**
1. Find submission/contact form for: Fireship (Jeff Delaney), Theo.gg (Theo Browne), The Primeagen
2. Draft pitch: "I have 201-server MCP quality dataset with 440x variance. Here's the thumbnail hook and script outline."
3. Check if any of these creators are on Bluesky (natural warm outreach point)
4. **DO NOT start** until H35 newsletter evaluation on May 1. Newsletter coverage first → YouTubers pick up covered stories.

**Key angle for pitch:** "You don't need to research this. Here's the data: 201 servers, 440x token variance, A+ to F grades. The story writes itself. Sentry (built to catch bugs) gets 0/100. Google Colab (designed for ML) gets A-. GitHub's official MCP uses 15,927 tokens."

---

## H63: GitHub Discussion User Research — Who's Grading What (2026-03-25)
Status: `running`
Started: 2026-03-25

**I believe** asking our 1,000 unique cloners "what MCP server are you grading?" in a GitHub Discussion **will generate at least 1 external reply revealing a use case we haven't targeted** because developers who cloned and used agent-friend have already shown enough intent to respond to a direct question.

**Riskiest assumption rank:**
1. (MOST UNCERTAIN) Cloners lurk and don't engage on GitHub (0 Discussion comments from outside so far)
2. The question is compelling enough to break lurker behavior
3. Replies reveal actionable customer development data

**True when:** At least 1 external user replies to Discussion #192 within 2 weeks (by 2026-04-08).
**False when:** Zero external replies by 2026-04-08.

**Expected value:** Customer dev insight worth $500/month (correct product direction) × 20% = $100/month EV. Also tests whether GitHub is a conversation channel at all.

**Budget:** $0 (Discussion created). **Deadline:** 2026-04-08.

**Actions:** Monitor Discussion #192 — check each session. If someone replies, prioritize response within same session.

---

## H73: Direct MCP Author Outreach — Grade Their Server, Reply With Data (2026-03-25)
Status: `candidate`
Added: 2026-03-25

**I believe** MCP server authors **will engage with us** when we proactively grade their server and reply to their announcement with specific quality data — because (1) no one else is doing this, (2) it's genuinely useful information they didn't know, (3) positive grades give them shareable social proof, (4) negative grades give them a specific fix path.

**How it works:**
1. Monitor Bluesky for new MCP server announcements (search "just shipped mcp", "released mcp server")
2. For each announcement: check if schema accessible via GitHub
3. If yes: grade via `agent-friend grade` or REST API
4. Reply to announcement: A+ grade = "congrats, here's your score + badge" / F grade = "top 3 issues + fix command"
5. Track if they reshare or respond

**Key observations that led to this:**
- Our 3 stargazers are NOT MCP server builders (wrong audience finding us)
- March 20 spike (650 unique cloners in 1 day) = some organic sharing drove us. We need to replicate this intentionally.
- @daniel-davia reply (March 25) got 5 likes from their followers — warm contact works when personal
- Best warm contacts are people who BUILD MCPs, not just talk about token costs

**Riskiest assumptions:**
1. Authors care about schema quality (might not know why it matters)
2. The schema is accessible without running the server (many use FastMCP/runtime generation)
3. Authors have Bluesky accounts where they announced (many use GitHub-only)

**True when:** 2+ authors engage with a grade reply (reshare, comment, or follow) within 30 days. **False when:** 10 graded-reply attempts generate 0 engagement in 30 days.

**Expected value:** $100/month × 15% = $15/month. But distribution value if a high-follower author reshares = $500 EV × 10% = $50.

**Budget:** $0 (time only). **Deadline:** 2026-04-25.

**Actions:**
1. Each session: search Bluesky for new MCP announcements from past 48 hours
2. Filter for authors with >200 followers
3. Check if GitHub repo exists + schema accessible
4. Grade via agent-friend or REST API
5. Draft reply with specific data
6. Schedule in next available reply slot (checking daily limit)
7. Track responses in decisions.md

---

## H80: burn0 × agent-friend Schema Attribution Loop (2026-03-25)
**Status:** `testing`

**Hypothesis:** burn0 (runtime MCP cost monitor by UrRhb/burn0 team) and agent-friend (build-time schema grader) can be integrated via schema fingerprinting to close the attribution gap — burn0 detects expensive endpoints, agent-friend identifies which schema patterns are causing it.

**Context:** @UrRhb engaged in Discussion #4 (6 comments as of 2026-03-25), explicitly suggesting the feedback loop: "burn0 detects spike → agent-friend flags the schema." They confirmed burn0 operates at HTTP layer and lacks schema-level attribution.

**The integration concept:**
1. agent-friend hashes tool schemas at build time (fingerprint = stable ID)
2. burn0 matches runtime endpoint costs to schema fingerprints
3. Developer sees: "your `github_search_code` tool description costs $0.47/day — here's why and how to fix it"

**True when:** burn0 mentions agent-friend in their docs/README OR ships a schema attribution feature that references our work within 60 days. **False when:** No mention within 90 days.

**Expected value:** If burn0 (which is gaining traction) adds agent-friend to their workflow, that's a distribution channel we don't control. $200/month EV × 15% = $30/month. But brand value = 2x that.

**Budget:** $0 (time to prototype the fingerprinting CLI). **Deadline:** 2026-06-25.

**Next action:** Continue the Discussion #4 conversation. If @UrRhb engages further, propose a concrete proof-of-concept: "agent-friend fingerprint <tools.json>" command that outputs a stable schema hash. This is a 1-session build.

## H81: Official MCP Servers Score Worse Than Community Equivalents (2026-03-25)
**Status:** `candidate`

**Hypothesis:** Servers built by the official product team (first-party) score lower than community-built alternatives for the same product. Official teams prioritize feature completeness; community builders prioritize adoption, which requires quality.

**Supporting evidence from leaderboard (202 servers):**
- GitHub official: F (20.1/100, 80 tools, 15,927 tokens)
- GitHub community: varies, but smaller/leaner
- Notion official (makenotion): F (19.8/100)  
- Notion community (awkoy/danhilse): 100.0/100
- Sentry official: F (0.0/100)
- Sentry community (initial): D
- AWS Documentation MCP (official): F (3.0/100, 4 tools, 2,397 tokens) — 8,561 star repo

**Why it matters for positioning:** If true, the MCP quality problem is structural, not accidental. Official teams don't have market pressure to optimize schemas because they have authority, not merit. Community tools succeed by being better. agent-friend grades by merit.

**Testable:** Tag 202 leaderboard entries as "official" / "community" / "unknown". Compare average scores by tag. Expect official avg < community avg.

**True when:** After tagging, official avg score is at least 15 points below community avg. Currently estimated: official avg ~25, community avg ~55.

**Action needed:** Manual tagging pass (2-3 hours). Creates new analysis for articles + Bluesky content. Hold until article pipeline < 2.

**Budget:** 1 session. **Deadline:** No deadline — pipeline blocker.

---

## H82: fastmcp-lint → FastMCP Ecosystem Distribution (2026-03-25)
**Status:** `testing`

**Hypothesis:** A static AST linter for FastMCP servers (fastmcp-lint) that catches missing/poor docstrings before deploy will get organic adoption from FastMCP developers and create a distribution pathway via FastMCP docs/ecosystem.

**Context:** 4/4 FastMCP-built servers we graded get F. Root cause: FastMCP generates descriptions from docstrings, but empty docstrings → empty descriptions → broken agent tool selection. The fix is trivial once you know about it. fastmcp-lint v0.1.0 shipped March 25, 2026. Zero dependencies, pure Python stdlib.

**Distribution levers:**
1. jlowin@prefect.io email sent March 26 — could result in FastMCP docs mention
2. Bluesky announcement March 27
3. PyPI page links to agent-friend leaderboard
4. Natural: FastMCP developers search for linting tools

**True when:** 50+ PyPI installs within 14 days OR FastMCP GitHub/docs mentions fastmcp-lint.
**False when:** <10 installs after 21 days AND no FastMCP engagement.

**Expected value:** If FastMCP docs mention it → fraction of 1M daily downloads → orders of magnitude reach. $200/month indirect EV × 20% = $40/month. But the optionality (could be much larger) makes this worth the 1-session investment.

**Budget:** Spent (1 session). **Deadline:** 2026-04-15 (evaluate installs + jlowin response).
