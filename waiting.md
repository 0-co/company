# Waiting / Deferred Actions

## Active

### Campaign Queue Swap — FULLY AUTOMATED
- **PID 268138**: Loads 065 queue at 17:30 UTC today
- **PID 274898**: `daily_queue_swap.sh` — handles Mar 19-24 swaps (066→071) at 17:30 UTC daily. Loops until 2026-03-24.

### Staggered Campaigns — All Running (date-guarded)
- **Mar 19**: PID 259700 — waiting for 2026-03-19
- **Mar 20**: PID 260458 — waiting for 2026-03-20
- **Mar 21**: PID 260461 — waiting for 2026-03-21
- **Mar 22**: PID 260462 — waiting for 2026-03-22
- **Mar 23**: PID 265482 — waiting for 2026-03-23
- **Mar 24**: PID 267999 — waiting for 2026-03-24
- **Mar 22**: PID 260462 — waiting for 2026-03-22 (article 073 Notion challenge — MOVED from Mar 26)
  - ⚠️ **Update staggered_posts_mar22.json URL before 18:00 UTC** on March 22
  - After art 073 publishes (16:00 UTC), get real URL: `vault-devto GET /articles/me/published?per_page=1 | python3 -c "import sys,json; a=json.load(sys.stdin)[0]; print(a['url'])"`
  - Update entry 0 in staggered_posts_mar22.json with real URL (replace temp slug)
  - Also: submit article to challenge if there's a separate submission form
  - **Deadline: March 29** — 7 days after publishing
- **Mar 26**: PID 309183 — waiting for 2026-03-26 (article 068, standalone Notion audit — no URL update needed)
- All have Python-level daily post limit check as safety net

### Articles 069 + 070 + 071 — ✅ DONE
- **What**: All articles updated to 47 servers, 939 tools, 178K tokens. Article 071 has new Grafana + BrowserMCP content.
- **Completed**: 2026-03-18 11:45 UTC

### IndexNow Submission — Submitted
- **What**: 8 key pages submitted to IndexNow (Bing, Yandex, Seznam, Naver). Key file: `docs/431c56abbe5647f18474f52c8b01caea.txt`
- **Check after**: 2026-03-20 (48h for crawling)
- **Action**: Search Bing for "MCP server leaderboard quality grade" and "MCP report card grade tool". If indexed, compare to pre-submission state (2 Bing referral views total).

### HN Comment Engagement Check — LIVE
- **What**: Board posted comment on "MCP is dead" thread (293 pts, 200 comments). Link: https://news.ycombinator.com/item?id=47423547
- **Check after**: 2026-03-18 16:00 UTC (6 hours after post)
- **Action**: Check points, replies, and whether it drove traffic to leaderboard/report card via GitHub Pages views.

### SEP-1576 Comment — LIVE ✅
- **What**: Board posted empirical data comment on MCP spec issue. Link: https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1576#issuecomment-4081247028
- **Check after**: 2026-03-19
- **Action**: Check for replies, reactions, or new issue activity referencing our data.

### Article 064 Results Check
- **What**: First real test of opinion format + optimal timing (8 AM PST). Check reactions, views, comments.
- **Check after**: 2026-03-18 20:00 UTC (4 hours after publish)
- **Action**: If >0 reactions → strategy is working, continue. If 0 → evaluate pivot options.

### Article 065 Campaign Poster — Running
- **What**: PID 299391 waits for article 065 (ID 3362600) to publish on Mar 19. Posts Bluesky campaign.
- **Campaign text**: "11 MCP servers. 27,462 tokens before a single user message. GitHub (80 tools): 20,444 tokens — 74% of the total. Postgres (1 tool): 34 tokens. 601x range. same protocol, very different schemas. {url}"
- **Check after**: 2026-03-19 17:00 UTC
- **Action**: Verify campaign posted. Check post-log.md.

### GitHub Issue Targets — PERMANENTLY BLOCKED
- **Status**: vault-gh can read external repos but CANNOT write/comment (addComment 403 confirmed session 163). Board declined to do distribution tasks (inbox cleaned). This channel is closed.
- **Action**: None. Do not re-open unless vault-gh scopes change.

### Anthropic v. DoD — March 24 Hearing
- **What**: Anthropic sued DoD over supply-chain risk designation (26-cv-01996, ND Cal)
- **Check after**: 2026-03-24 (preliminary injunction hearing)
- **Action**: Search "Anthropic DoD hearing" on March 24. Write article if significant outcome.

### Newsletter Pitch — Awaiting Traction Threshold
- **What**: Board wants more traction. Re-pitch when threshold passed.
- **Threshold**: 50 Bluesky followers (currently 36) OR 15 Twitch followers (currently 5)
- **Check after**: Each startup
- **Action**: When threshold passed, recreate board inbox request

### PyPI Publishing — Awaiting Traction
- **What**: Board said "ask again with demonstrated traction."
- **Threshold**: 10+ GitHub stars OR evidence of actual usage
- **Current**: 0 stars, 194 unique clones, 0% conversion
- **Action**: Re-request when threshold met. This is the #1 friction point for adoption.

### Notion MCP Challenge — Active Pursuit
- **What**: Dev.to challenge, $1,500 prizes, deadline March 29. 15-20 entries, field is thin. Top: EchoHR (46 reactions). One category, reactions are tiebreaker.
- **Status**: Board request filed for Notion API credentials (P2, `2-notion-mcp-challenge.md`). Article draft updated with current 50-server data. **Dev.to draft created: ID 3368335** (unpublished).
- **Plan**: Build "MCP Quality Dashboard" that uses Notion MCP to store audit results. Demo: grade Notion's own 22 tools → F (19.8/100) → results displayed in Notion database. Article: 17,410 chars, YouTube demo, "I Built X" format. Article 068 (audit) stays as separate standalone content.
- **Needs from board**: (1) Notion integration token, (2) YouTube upload for terminal recording
- **Critical path**: Board credentials needed by March 22-23 to submit by March 25.
- **Check after**: 2026-03-19 (give board 24h)
- **Action**: When credentials arrive: run live mode, get board to upload YouTube demo (~2-3 min), update article ID 3368335 with video, publish. Target submit by March 25.
- **Code**: `examples/notion_quality_dashboard.py` — dry-run tested, live mode needs NOTION_API_KEY
- **Research**: `research/notion-mcp-challenge-analysis-2026-03-18.md`

### Notion MCP Issue Comments — BLOCKED (vault-gh cannot write external repos)
- vault-gh addComment confirmed blocked (session 163). Board declined distribution tasks.
- Skip this.

### Report Card — Track Adoption
- **What**: MCP Report Card (report.html) launched session 140. Badge copy feature for README viral loop.
- **Check after**: 2026-03-20 (3 days post-launch)
- **Action**: Check GitHub Pages analytics (if available), search for shields.io badge usage with "MCP_Quality" text, check if any repos adopted the badge.

### mcpservers.org — APPROVED ✓
- **What**: Submitted agent-friend via web form on March 17
- **Approved**: 2026-03-18 04:47 UTC (email confirmation received)
- **Status**: ✅ Listed. 5th MCP directory.

### Glama — Waiting for Re-scan
- **What**: Board claimed server. Docker image builds and responds correctly (314 tools). Glama hasn't re-scanned yet — security/quality still "not tested." Board thinks issue is missing release (we have v0.56.0) or Dockerfile inspection (works locally).
- **Check after**: 2026-03-19
- **Action**: Check glama.ai/mcp/servers/0-co/agent-friend for updated scores. If still broken, reply to punkpeye on issue #14.

### awesome-ai-devtools PR #310 — Submitted
- **What**: Board opened PR to add agent-friend audit to Evaluation section of 3.6K-star awesome list.
- **Check after**: 2026-03-20 (give a few days for review)
- **Action**: Check PR status at github.com/jamesmurdza/awesome-ai-devtools/pull/310

### awesome-mcp-servers PR — Branch Ready, Board Must Open PR
- **What**: Branch `add-agent-friend` created on fork (0-co/awesome-mcp-servers). README updated — agent-friend entry at top of Developer Tools section. vault-gh can't create cross-repo PRs (HTTP 403).
- **Board request**: `board/inbox/4-awesome-mcp-servers-pr.md` (P1)
- **One-click URL**: https://github.com/punkpeye/awesome-mcp-servers/compare/main...0-co:awesome-mcp-servers:add-agent-friend
- **Check after**: Next board interaction
- **Action**: Board opens PR using one-click URL + suggested title/body from inbox request.

### MCP Registry Auth — Board Deferred
- **What**: Board said "I'll wait before doing" the device flow auth.
- **Check after**: Next board interaction
- **Action**: Don't push. Low priority.

### tiny-helpers.dev PR — Failed (Empty Diff)
- **What**: Board tried to create PR but GitHub showed empty diff. Fork/branch probably doesn't exist.
- **Action**: Need to create the fork and branch first. But we can't fork external repos. Need board to fork, then I stage the changes. Low priority — focus on awesome lists first.

### Reddit Account — Re-Requested (March 18)
- **What**: Board deferred on March 12. "Ask again in a week." Re-requested March 18 (board/inbox/3-reddit-account-request.md).
- **Check after**: 2026-03-19 (board response)
- **Action**: If approved, get credentials from vault. If declined, re-ask March 25.

### Article Publishing Schedule (automated via systemd timer)
- **064**: March 18 — "MCP Won. MCP Might Also Be Dead." (ID: 3362409) ✅ PUBLISHED
- **065**: March 19 — "I Audited 11 MCP Servers. 27,462 Tokens Before a Single Message." (ID: 3362600)
- **066**: March 20 — "Ollama Tool Calling in 5 Lines of Python" (ID: 3364983)
- **067**: March 21 — "BitNet Has a Secret API Server. Nobody Told You." (ID: 3363773)
- **068**: March 22 — "I Graded Notion's MCP Tools. They Got an F." (ID: 3365363)
- **069**: March 23 — "I'm an AI Grading Other AIs' Work. The Results Are Embarrassing." (ID: 3366028)
- **070**: March 24 — "The #1 Most Popular MCP Server Gets an F" (ID: 3366324)
- **071**: March 25 — "I Graded 50 MCP Servers. The Most Popular Ones Are the Worst." (ID: 3366683)
- **072**: TBD — "OWASP Published an MCP Top 10. They Missed the Biggest Risk." (ID: 3368431) — READY, schedule if 064 gets reactions
- **055-063**: PAUSED (dates set to 2099). Unpause only if traction materializes.

### Dev.to Article Pruning — DONE
- **What**: Evaluated all 20 drafts. 4 test posts (can't delete via API). 8 tutorial articles (055-063) permanently paused — pure feature docs, zero engagement potential. 3 salvageable story/opinion pieces kept. 4 scheduled (064-067) unchanged.
- **Decision**: Only publish opinion/story articles going forward. Tutorials get zero reactions on Dev.to.
- **Status**: ✅ Complete

### Competitive Watch (MCP Security Audit Tools)
- **What**: 3 new tools found session 148: Golf Scanner (golf-mcp/golf-scanner), MCP-Audit (apisec-inc/mcp-audit), Agent Audit (HeadyZhang/agent-audit). All security-focused, not quality. But if they add quality grading, they become direct competitors.
- **Check after**: Weekly (next: March 25)
- **Action**: Monitor their GitHub stars/features. If any adds schema grading, note in decisions.md.

### ToolRegistry Competitive Watch
- **What**: ToolRegistry (Python, PyPI) is nearest competitor. Has Show HN, academic paper.
- **Check after**: Weekly (next: March 24)
- **Action**: Monitor their PyPI downloads, GitHub stars, feature updates.

### Business Simulation Idea (H6 candidate)
- **What**: Board proposed simulated economy for AI agents. Research done — space is active (Stanford Generative Agents, Microsoft Magentic Marketplace, ABIDES). Feasible but massive scope.
- **Check after**: When current strategy stalls OR Twitch content needs refresh
- **Action**: Consider as mini-demo using agent-friend if H5 needs new content angle

## Resolved
- ✅ Resilient Article Publisher — systemd timer built, active, verified working
- ✅ Article053 published March 17
- ✅ Article054 published March 17
- ✅ ProductHunt — REJECTED by board ("not significant enough")
- ✅ GitHub token permissions — DEAD END (board: "PAT has max permissions possible")
- ✅ BitNet GitHub issue comments — BLOCKED permanently (no external repo access)
- ✅ Bluesky avatar upload — board did manually
- ✅ Newsletter pitch deferred — threshold set
- ✅ Smithery — board deferred ("ask again later")
