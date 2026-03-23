# Waiting / Deferred Actions

## Active

### @jlowin.dev (FastMCP/Prefect CEO) — Bluesky Partnership Outreach
- **What**: Jeremy Lowitz (jlowin.dev on Bluesky) — CEO of Prefect, author of FastMCP (23.9K stars, 1M downloads/day). FastMCP auto-generates schemas from Python docstrings, creating the token bloat patterns we grade. Partnership angle: "your generator + our linter."
- **Channel**: Bluesky reply to a relevant post, then DM if he engages. NOT email (no public email).
- **Check after**: 2026-03-24 — look at his recent posts, find MCP/FastMCP content to reply to genuinely
- **Draft**: cold_email_drafts.md Draft 10 (has email version, adapt for Bluesky tone)
- **Conditional**: If HN (March 23) gets >30 pts, mention it in the reply
- **Impact**: If FastMCP docs mention agent-friend → fraction of 1M daily PyPI downloads → orders of magnitude more reach than any single server email

### Podcast Outreach Pipeline (starting Mar 25)
- **Mar 25**: Python Bytes — submit via pythonbytes.fm/episode/suggest (web form, no auth needed). Include HN data if >30 pts.
- **Mar 30**: Talk Python — DM @mkennedy (michael@talkpython.fm). Include HN data.
- **Apr 1**: The Changelog — submit via changelog.com/request.
- **Apr 2**: Python Podcast.__init__ — submit via pythonpodcast.com/contact.
- **Note**: All drafts in products/outreach/podcast_pitches.md. Add "as seen on HN" if >30 pts.

### 10-Day Cold Outreach Pipeline (Mar 25 - Mar 31)
- **Mar 25**: console.dev editorial submission → `python3 products/outreach/send_console_dev_mar25.py` (check HN traction first — add "as seen on HN" if >50 upvotes)
- **Mar 26**: Sentry/dcramer → cold_email_drafts.md Draft 1 (david@sentry.io)
- **Mar 27**: Cloudflare/Glen Maddern → prospecting_list.md #6 (glen.maddern@cloudflare.com)
- **Mar 28**: Neon → cold_email_drafts.md Draft 2 (find contact)
- **Mar 29**: Stripe → cold_email_drafts.md Draft 3 (find contact)
- **Mar 30**: PyCoder's Weekly → `python3 products/outreach/send_pycoders_weekly_mar30.py`
- **Mar 31**: Quastor → newsletter_outreach.md Draft (sponsorship inquiry form)
- **Note**: TLDR fires automated March 24 09:00 UTC — that day's cold slot is used

### GitHub Sponsors board request
- **Filed**: 2026-03-23 (board/inbox/3-github-sponsors-setup.md)
- **Check after**: 2026-03-25
- **Action when approved**: Add FUNDING.yml to agent-friend, update README with sponsor button

### Show HN → post-HN amplification
- **Fires**: 2026-03-23 14:00 UTC
- **Action**: Read post_hn_amplification.md, check HN thread at 14:10 UTC, respond to comments 14:00-17:00 UTC
- **Conditional**: If >30 points → Bluesky (bsky_mar23_hn_response.md), If >100 → move console.dev email to March 24
- **72h metrics**: track GitHub stars, PyPI downloads, Twitch followers, agentmail responses

### mcp-compat v0.1.0 adoption tracking (shipped 2026-03-23)
- **What**: Breaking change classifier for MCP schemas. pip install mcp-compat. 21 tests, MIT, zero deps. PyPI + GitHub.
- **Check after**: 2026-04-06 — check stars, PyPI downloads
- **True signal**: 3+ stars within 14 days. False signal: 0 downloads after 1 week.
- **Announce**: Bluesky 12:00 UTC March 23 (PID 1456178), Discussion #189 on agent-friend

### H20: mcp-diff adoption tracking
- **What**: Shipped mcp-diff v0.1.0 (2026-03-22). Schema lockfile + breaking change detector. 32 tests. PyPI + GitHub.
- **Check after**: 2026-04-05 — check stars, PyPI downloads, any repos using it with mcp-schema.lock
- **True signal**: 5+ stars within 14 days. False signal: 0 installs after 1 week with promotion.
- **Announce post**: bsky_mar24_mcp_diff.md — post manually ~10:00 UTC March 24 (280 chars, under limit)
- **Pain point**: GitHub issue modelcontextprotocol/inspector#1034 is the key validation — same problem we're solving

### H19: mcp-snoop adoption tracking
- **What**: Shipped mcp-snoop v0.1.0 (2026-03-22). Transparent stdio interceptor for MCP. Zero deps. 13 tests. PyPI + GitHub.
- **Check after**: 2026-04-05 — check stars, PyPI downloads, any repos using it
- **True signal**: 5+ stars within 14 days. False signal: 0 stars + 0 downloads after 1 week.
- **Announce post**: queued in post_mar23_snoop.py (fires 2026-03-23 10:00 UTC)
- **CI**: GitHub Actions added (test + PyPI publish on v* tag)

### H15: MCP Quality API adoption tracking
- **What**: REST API live at http://89.167.39.157:8082. Check for registry integrations.
- **Check after**: 2026-04-21 — count API usage, look for repos calling the endpoint, check Discussion #187 for comments
- **True signal**: 2+ integrations using the API. False signal: 0 integrations.
- **Outreach**: Email Glama (Frank Fiegel via board), mention to mcpservers.org

### H14: mcp-starter template use tracking
- **What**: Check how many repos have been created from the mcp-starter template
- **Check after**: 2026-04-07 — run: `sudo -u vault /home/vault/bin/vault-gh api repos/0-co/mcp-starter/forks` or check traffic via API
- **True signal**: 20+ uses in 30 days. False signal: <5 uses in 30 days.
- **Also check**: GitHub Discussion #185 for comments, and traffic/views to the template repo

### VS Code Extension — Awaiting Marketplace Publisher
- **What**: Built agent-friend-vscode-0.1.0.vsix (5.8KB). Real-time MCP schema grading in VS Code.
- **Board request**: `3-vscode-marketplace-publisher.md` — needs Microsoft account + Azure PAT
- **Check after**: 2026-03-25 (give board a few days)
- **In the meantime**: .vsix available in agent-friend repo `vscode-extension/` for local install
- **Announce post**: `bsky_mar24_vscode_extension.md` — post after pre-commit post (~15:00 UTC)

### Pre-commit Bluesky post — March 24
- **What**: Announce pre-commit hook support (`.pre-commit-hooks.yaml` shipped March 21)
- **Draft**: `products/content/bsky_mar24_precommit.md`
- **Check after**: 2026-03-24 morning — post manually ~10:00 UTC

### Show HN — CHECK RESPONSE WINDOW (March 23 14:00-17:00 UTC)
- **Status**: vault-hn working ✓ (confirmed session 223as). Script fires 14:00 UTC March 23.
- **Check after**: 2026-03-23 14:00 UTC — respond to HN comments in the 14:00-17:00 window
- **Prep**: `hn_response_prep.md` has Q&A ready for all anticipated questions
- **Action**: If thread gets comments, respond individually and thoughtfully using hn_response_prep.md

### Reddit — BLOCKED (IP-level network block on agent-browser login)
- **Status**: agent-browser gets "You've been blocked by network security" on reddit.com/login. Board request 2-reddit-oauth.md filed for API OAuth credentials.
- **Drafted posts**: reddit_mcp_post.md (r/mcp), reddit_localllama_post.md (r/LocalLLaMA) — ready when OAuth arrives.
- **Check after**: Next session — check board outbox for OAuth credentials.

### Art 065 — Fix Token Count ✅ DONE (session 201, 14:02 UTC)
- Updated via /articles/me/all bypass (GET /articles/:id was rate limited, but /articles/me/all works)
- Title: "22,945 Tokens" ✅ | Body: 27,462→22,945 (4x), 20,444→15,927 (2x) ✅

### Art 073 — Add Video Link ✅ DONE (session 201, 14:03 UTC)
- Replaced "_[Video coming — uploading to YouTube before March 29]_" with hosted link
- Link: `[Watch the demo walkthrough](https://0-co.github.io/company/video/notion_challenge_demo.mp4) (2:11)` ✅

### Art 071 — Update Leaderboard Stats ✅ DONE (session 199)
- Title updated: "75 MCP Servers" → "198 MCP Servers"
- Body updated: 75→198 servers, 1,482→3,971 tools, 247,883→511,518 tokens
- Article fires March 25 at 16:00 UTC — READY

### Post-Freeze Build (16:10 UTC Mar 19)
- **Auto-handled at 16:10 UTC**: PID 340645 deploys GitHub Pages + grade-request template to agent-friend
- **Badge copy feature**: Already implemented (session 197) in leaderboard.html
- **Check after**: 2026-03-19 16:10 UTC — verify deploy ran, check art 064 24h reactions

### Campaign Queue Swap — FULLY AUTOMATED
- **Art 065 campaign**: PID 443230 (v2 script using /articles/me/all — waits for art 065 to publish Mar 19, posts announcement)
- **PID 326612**: `daily_queue_swap.sh` (restarted session 189) — handles Mar 19-29 swaps at 17:30 UTC daily. Loops until 2026-03-29.
  - Mar 19→066, Mar 20→067, Mar 21→073, Mar 22→069, Mar 23→070, Mar 24→071, Mar 25→068, **Mar 26→072 (NEW)**, Mar 27→075, Mar 28→074

### Art Apr2 Day-25 Retro — Update Before Publish (April 1)
- **What**: Art ID 3371679 ("25 Days. $0 Revenue. 50+ Followers...") publishes April 2
- **Updated (session 223cc)**: Followers, cloners, reactions, articles published, Twitch count, affiliate deadline, Notion challenge mention
- **Still needs updating on April 1**: Title "50+" → actual follower count post-HN. Body numbers: GitHub stars, cloners, Twitch followers, broadcast minutes, reactions. Also check if Twitch affiliate was reached by then.
- **Push to Dev.to**: `vault-devto PUT /articles/3371679 {"article": {"body_markdown": "...", "title": "X Days. $0 Revenue. Y Followers..."}}`

### Art 075 — Update Draft Before Publish (March 27)
- **What**: Art 075 ("21 Days. $0 Revenue...") publishes March 28.
- **Pre-filled (session 223bw)**: [BROADCAST_MIN]→12,245 ✓ | [REACTION_COUNT]→7 of 20 ✓
- **Still stale in file (update March 27)**:
  - Line 40: "GitHub stars: 2 (305 unique clones)" → update to actual numbers post-HN
  - Title/body: "7 Twitch Followers" — update if count changes post-HN
  - Broadcast minutes: update with fresh value (12,245 as of Mar 22 22:00 UTC)
  - Reactions count: recheck (7 of 20 as of Mar 22)
- **Push to Dev.to (March 27)**: `vault-devto PUT /articles/3368966 {"article": {"body_markdown": "<content>", "title": "21 Days. $0 Revenue. X Twitch Followers. This Is What AI Autonomy Looks Like."}}`

### Staggered Campaigns — All Running (date-guarded)
- **Mar 19**: PID 259700 — waiting for 2026-03-19
- **Mar 20**: PID 260458 — waiting for 2026-03-20
- **Mar 21**: PID 260461 — waiting for 2026-03-21
- **Mar 22**: PID 260462 — waiting for 2026-03-22
  - ⚠️ **Update staggered_posts_mar22.json URL before 18:00 UTC** on March 22
  - After art 073 publishes (16:00 UTC), get real URL: `vault-devto GET /articles/me/published?per_page=1 | python3 -c "import sys,json; a=json.load(sys.stdin)[0]; print(a['url'])"`
  - **Replace `TEMPURL` in staggered_posts_mar22.json entry 0 with real URL** (already has #notionchallenge tag)
  - Also: submit article to challenge if there's a separate submission form
  - **Deadline: March 29** — 7 days after publishing
- **Mar 23**: PID 265482 — waiting for 2026-03-23
- **Mar 24**: PID 267999 — waiting for 2026-03-24
- **Mar 25**: PID 274310 — waiting for 2026-03-25
- **Mar 26**: PID 309183 — waiting for 2026-03-26 (article 068, standalone Notion audit — no URL update needed)
- **Mar 27**: PID 316736 — waiting for 2026-03-27 (article 072, OWASP gap — NEW, added session 173)
- **Mar 28**: PID 314046 — waiting for 2026-03-28 (article 075, AI CEO narrative — drives Twitch follows)
- **Mar 29**: PID 314047 — waiting for 2026-03-29 (article 074, reference implementations)
- All have Python-level daily post limit check as safety net

### Articles 069 + 070 + 071 — ✅ DONE
- **What**: All articles updated to 47 servers, 939 tools, 178K tokens. Article 071 has new Grafana + BrowserMCP content.
- **Completed**: 2026-03-18 11:45 UTC

### IndexNow Submission — Submitted
- **What**: 8 key pages submitted to IndexNow (Bing, Yandex, Seznam, Naver). Key file: `docs/431c56abbe5647f18474f52c8b01caea.txt`
- **Check after**: 2026-03-20 (48h for crawling)
- **Action**: Search Bing for "MCP server leaderboard quality grade" and "MCP report card grade tool". If indexed, compare to pre-submission state (2 Bing referral views total).


### SEP-1576 Comment — 0 reactions (checked 2026-03-19)
- **Status**: 0 reactions. kira-autonoma (mcp-lazy-proxy) replied with their proxy tool — complementary framing ("spec fix would be proper fix").
- **Note**: Comment says "27,462 tokens" (old data) — can't edit (vault-gh can't write external repos).
- **Action**: None. This channel has low engagement. Consider closing this item.

### Article 064 Results Check — 4h DONE ✓
- **Status**: 1 reaction, 5 views at 4h (20:31 UTC March 18). Condition ">0 reactions" MET.
- **Action taken**: Art 072 (ID 3368431) added to schedule for March 27. Campaign + staggered launched (session 173).
- **24h check**: 2026-03-19 16:10 UTC — check for more reactions. If strong, consider featuring in social.

### Article 065 Campaign Poster — ✅ DONE (16:12 UTC Mar 19)
- Campaign posted manually at 16:12 UTC (PID 443230 killed — /articles/me/all returns published_at=null bug)
- URL: https://dev.to/0coceo/i-audited-11-mcp-servers-22945-tokens-before-a-single-message-31e

### GitHub Issue Targets — PERMANENTLY BLOCKED
- **Status**: vault-gh can read external repos but CANNOT write/comment (addComment 403 confirmed session 163). Board declined to do distribution tasks (inbox cleaned). This channel is closed.
- **Action**: None. Do not re-open unless vault-gh scopes change.

### Anthropic v. DoD — March 24 Hearing
- **What**: Anthropic sued DoD over supply-chain risk designation (26-cv-01996, ND Cal)
- **Check after**: 2026-03-24 (preliminary injunction hearing)
- **Action**: Search "Anthropic DoD hearing" on March 24. Write article if significant outcome.

### Newsletter Pitch — Threshold MET ✓ (50 Bluesky followers, 2026-03-22)
- **Status**: 50/50 Bluesky ✓. Pragmatic Engineer pitched (00:12 UTC Mar 22). New Stack email queued (09:00 UTC Mar 23). TLDR queued (09:00 UTC Mar 24).
- **Check after**: 2026-03-25 (Pragmatic Engineer check), 2026-03-24 (PulseMCP check)
- **Action**: Check agentmail inbox for responses to all three pitches

### PyPI Publishing — ✅ DONE (2026-03-19, session 202)
- Published agent-friend v0.63.5 to PyPI. `pip install agent-friend` works globally.
- URL: https://pypi.org/project/agent-friend/0.63.5/
- Wheel + sdist uploaded via vault-pypi (twine). Announced on Bluesky at 17:49 UTC.

### Notion MCP Challenge Thread Drop — March 22
- **Board directive**: Only send the axrisi thread drop request AFTER art 073 is live (March 22). Board rebuke: "respect my time, only give me requests when they're actionable."
- **Action on March 22 (after 16:00 UTC)**: Re-create board inbox item `3-notion-challenge-thread-drop.md` with actual art 073 URL. File it AFTER art 073 URL is confirmed live.
- **Comment to post**: Drop link to art 073 in axrisi's "Drop Your Challenge Submission Here" thread. Text: "Built a tool that grades MCP schemas A+ to F. Notion's official server gets an F. [ARTICLE_URL] #notionchallenge"
- **NOTE**: Outbox item deleted (session 202). Must re-file board inbox request on March 22 with real URL.

### Notion MCP Challenge — FULLY READY
- **What**: Dev.to challenge, $1,500 prizes, deadline March 29. 65+ entries. **PANEL-JUDGED** (Originality, Technical Complexity, Practical Implementation). Reactions do NOT decide winner. Real standings as of March 18: ujja "EchoHR" 48 rxn, balkaran "Slack" 48 rxn (irrelevant to judging criteria).
- **NOT META/official**: axrisi "Drop Your Challenge Submission Here" (46 rxn, page 1) = aggregator. jess posts = official challenge updates.
- **Status**: All blockers resolved. **vault-notion LIVE** (session 164). YouTube not required. **Dev.to draft ID 3368335** (unpublished). Notion database live: `327b482b-7dc4-812a-876e-da49e6e07ae4` (29 entries). `examples/notion_quality_dashboard.py` dry-run verified.
- **Plan**: Article 073 auto-publishes March 22 at 16:00 UTC. Campaign fires at 16:30. Staggered posts at 18:00/19:00/20:00.
- **Action on March 22**: (1) Update staggered_posts_mar22.json first post with real URL (between 16:00-18:00 UTC), (2) Check if challenge requires separate submission form at dev.to, (3) Check board outbox for YouTube URL from board — if provided, update article 073 body (ID 3368335) to replace video placeholder with actual embed
- **Video status**: File ready at `/home/agent/company/products/content/video/notion_challenge_demo.mp4` (2.3MB). Board has P2 inbox request to upload to YouTube. Update article with URL anytime before March 29 deadline.
- **Code**: `examples/notion_quality_dashboard.py` — dry-run tested, live mode needs NOTION_API_KEY
- **Research**: `research/notion-mcp-challenge-analysis-2026-03-18.md`
- **Check after**: 2026-03-22 (publish day)

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

### Glama — uvx fix pending board deploy (session 202)
- **Root cause chain**: v0.63.3-v0.63.5 fixed the Docker build. v0.63.5 passed but Glama proxy failed with `spawn agent-friend ENOENT` — proxy tries to run `agent-friend` locally, not in Docker.
- **Session 202 fix**: Added `command: uvx, args: [agent-friend]` to glama.json (commit aba0741 on agent-friend main). Since we're now on PyPI, `uvx agent-friend` auto-installs + runs CLI which detects piped stdin → MCP server mode.
- **Board request**: `3-glama-v0635-uvx.md`
- **Check after**: 2026-03-20 (after board deploys)
- **Action**: After board deploys, check glama.ai/mcp/servers/0-co/agent-friend for "installable" status.

### awesome-ai-devtools PR #310 — Submitted
- **What**: Board opened PR to add agent-friend audit to Evaluation section of 3.6K-star awesome list.
- **Check after**: 2026-03-20 (give a few days for review)
- **Action**: Check PR status at github.com/jamesmurdza/awesome-ai-devtools/pull/310

### awesome-mcp-servers PR — DECLINED
- Board declined all PR requests in session 164. Will not open PRs. Branch `add-agent-friend` exists on fork but no action possible.
- **Action**: None. Board policy: no PRs, period.

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
- **073**: March 22 — "I Built a Tool That Grades MCP Servers. Notion's Got an F." (ID: 3368335) — Notion MCP Challenge
- **069**: March 23 — "I'm an AI Grading Other AIs' Work. The Results Are Embarrassing." (ID: 3366028)
- **070**: March 24 — "The #1 Most Popular MCP Server Gets an F" (ID: 3366324)
- **071**: March 25 — "I Graded 50 MCP Servers. The Most Popular Ones Are the Worst." (ID: 3366683)
- **068**: March 26 — "I Graded Notion's MCP Tools. They Got an F." (ID: 3365363) — moved from Mar 22
- **072**: TBD — "OWASP Published an MCP Top 10. They Missed the Biggest Risk." (ID: 3368431) — READY, schedule Mar 27 if 064 gets reactions (bumps art 075 to Mar 28, art 074 to Mar 29)
- **075**: March 28 — "11 Days. $0 Revenue. 5 Twitch Followers. This Is What AI Autonomy Looks Like." (ID: 3368966) — AI CEO narrative, direct Twitch CTA. **Move to Mar 27 if 072 not scheduled.**
- **074**: March 29 — "Not Even the Reference Implementations Pass" (ID: 3368850) — reference impl audit
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

### Pragmatic Engineer newsletter pitch
- **Status**: ✅ SENT — 2026-03-22 00:12 UTC via vault-agentmail → pulse@pragmaticengineer.com
- **Subject**: "MCP tool token costs vary 440x — engineers don't know it's costing them"
- **Check after**: 2026-03-25 (check agentmail inbox for response)
- **If no reply**: No follow-up needed.

### PulseMCP newsletter response
- **Status**: Emailed hello@pulsemcp.com on 2026-03-21 14:05 UTC
- **Check after**: 2026-03-24 (3 days) — if no response, follow up or try other channels

### Board requests pending
- 2-reddit-session.md
- 2-awesome-mcp-servers-listing.md (punkpeye, 83K stars)
- 3-distribution-actions.md (Official MCP Registry, Smithery, MCPNewsletter.com)
