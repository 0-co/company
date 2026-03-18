# Waiting / Deferred Actions

## Active

### Campaign Queue Swap — After Article 064 Posts
- **What**: After campaign fires at ~16:30 UTC today, campaign_queue.json gets renamed to _done.json automatically. Need to load tomorrow's queue.
- **Check after**: 2026-03-18 17:00 UTC
- **Action**: `cp products/content/campaign_queue_065.json products/content/campaign_queue.json`
- **Also**: Manual Bluesky posts 2-4 from `drafts/bsky_drafts_mar18.md` at 18:00, 19:00, 20:00 UTC
- **Repeat daily**: After each day's campaign, load next day's queue (066 on Mar 19, 067 on Mar 20)

### Article 064 Results Check
- **What**: First real test of opinion format + optimal timing (8 AM PST). Check reactions, views, comments.
- **Check after**: 2026-03-18 20:00 UTC (4 hours after publish)
- **Action**: If >0 reactions → strategy is working, continue. If 0 → evaluate pivot options.

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
- **Status**: Board request filed for Notion API credentials (P2, `2-notion-mcp-challenge.md`).
- **Plan**: Build "MCP Quality Dashboard" that uses Notion MCP to store audit results. Demo: grade Notion's own 22 tools → F (19.8/100) → results displayed in Notion database. Article: 2000+ words, YouTube demo, "I Built X" format. Article 068 (audit) stays as separate standalone content.
- **Needs from board**: (1) Notion integration token, (2) YouTube upload for terminal recording
- **Check after**: 2026-03-19 (give board 24h)
- **Action**: When credentials arrive, build integration + write challenge article. Target submit by March 25.
- **Research**: `research/notion-mcp-challenge-analysis-2026-03-18.md`

### Notion MCP Issue Comments — When Article 068 Publishes
- **What**: Issues #215, #181, #161 on makenotion/notion-mcp-server are all type-confusion bugs caused by undefined schemas — exactly what our audit catches.
- **Check after**: 2026-03-22 (when article 068 publishes)
- **Action**: Try `vault-gh api repos/makenotion/notion-mcp-server/issues/215/comments -f body="..."`. If PAT allows, comment with audit findings + article link. If blocked, request board to post. Draft comment:
  "This is a schema definition issue. The post-page tool has properties with type: object but no properties defined. When an LLM encounters underspecified schemas, it may serialize as string instead of native type. I ran a static audit on all 22 Notion MCP tools — 5 have this class of issue. Full analysis: [article 068 URL]"

### Report Card — Track Adoption
- **What**: MCP Report Card (report.html) launched session 140. Badge copy feature for README viral loop.
- **Check after**: 2026-03-20 (3 days post-launch)
- **Action**: Check GitHub Pages analytics (if available), search for shields.io badge usage with "MCP_Quality" text, check if any repos adopted the badge.

### mcpservers.org — Submission Pending
- **What**: Submitted agent-friend via web form on March 17
- **Check after**: 2026-03-19 (48h review window)
- **Action**: Check email (0coceo@agentmail.to) for approval notification. Verify listing at mcpservers.org.

### Glama — Waiting for Re-scan
- **What**: Board claimed server. Docker image builds and responds correctly (314 tools). Glama hasn't re-scanned yet — security/quality still "not tested." Board thinks issue is missing release (we have v0.56.0) or Dockerfile inspection (works locally).
- **Check after**: 2026-03-19
- **Action**: Check glama.ai/mcp/servers/0-co/agent-friend for updated scores. If still broken, reply to punkpeye on issue #14.

### awesome-ai-devtools PR #310 — Submitted
- **What**: Board opened PR to add agent-friend audit to Evaluation section of 3.6K-star awesome list.
- **Check after**: 2026-03-20 (give a few days for review)
- **Action**: Check PR status at github.com/jamesmurdza/awesome-ai-devtools/pull/310

### awesome-mcp-servers PR — Board Waiting
- **What**: Board said "waiting on Glama" before submitting. Confused Glama claim with awesome-list PR. Will follow up.
- **Check after**: Next board interaction
- **Action**: Clarify that awesome-mcp-servers PR is independent of Glama claim.

### MCP Registry Auth — Board Deferred
- **What**: Board said "I'll wait before doing" the device flow auth.
- **Check after**: Next board interaction
- **Action**: Don't push. Low priority.

### tiny-helpers.dev PR — Failed (Empty Diff)
- **What**: Board tried to create PR but GitHub showed empty diff. Fork/branch probably doesn't exist.
- **Action**: Need to create the fork and branch first. But we can't fork external repos. Need board to fork, then I stage the changes. Low priority — focus on awesome lists first.

### Reddit Account — Board Said "Ask Again in a Week"
- **What**: Board deferred on March 12. "Ask again in a week."
- **Check after**: 2026-03-19
- **Action**: Re-request with updated stats if any traction materializes

### Article Publishing Schedule (automated via systemd timer)
- **064**: March 18 — "MCP Won. MCP Might Also Be Dead." (ID: 3362409)
- **065**: March 19 — "How Many Tokens Are Your AI Tools Costing You?" (ID: 3362600)
- **066**: March 20 — "Ollama Tool Calling in 5 Lines of Python" (ID: 3364983)
- **067**: March 21 — "BitNet Has a Secret API Server. Nobody Told You." (ID: 3363773)
- **055-063**: PAUSED (dates set to 2099). Unpause only if 064-067 show traction.

### Dev.to Article Pruning — DONE
- **What**: Evaluated all 20 drafts. 4 test posts (can't delete via API). 8 tutorial articles (055-063) permanently paused — pure feature docs, zero engagement potential. 3 salvageable story/opinion pieces kept. 4 scheduled (064-067) unchanged.
- **Decision**: Only publish opinion/story articles going forward. Tutorials get zero reactions on Dev.to.
- **Status**: ✅ Complete

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
