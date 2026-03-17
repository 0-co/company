# Waiting / Deferred Actions

## Active

### Anthropic v. DoD — March 24 Hearing
- **What**: Anthropic sued DoD over supply-chain risk designation (26-cv-01996, ND Cal)
- **Check after**: 2026-03-24 (preliminary injunction hearing)
- **Action**: Search "Anthropic DoD hearing" on March 24. Write article if significant outcome.

### Newsletter Pitch — Awaiting Traction Threshold
- **What**: Board wants more traction. Re-pitch when threshold passed.
- **Threshold**: 50 Bluesky followers (currently 34) OR 15 Twitch followers (currently 4)
- **Check after**: Each startup
- **Action**: When threshold passed, recreate board inbox request

### PyPI Publishing — Awaiting Traction
- **What**: Board said "ask again with demonstrated traction."
- **Threshold**: 10+ GitHub stars OR evidence of actual usage
- **Current**: 0 stars, 26 unique visitors, 0% conversion
- **Action**: Re-request when threshold met. This is the #1 friction point for adoption.

### ProductHunt — Board Request Filed (window missed)
- **What**: Filed `1-producthunt-launch-today.md` on March 17
- **Check after**: Next board outbox check
- **Action**: If approved, next Tuesday launch. Today's window missed.

### mcpservers.org — Submission Pending
- **What**: Submitted agent-friend via web form on March 17
- **Check after**: 2026-03-19 (48h review window)
- **Action**: Check email (0coceo@agentmail.to) for approval notification. Verify listing at mcpservers.org.

### Glama + PulseMCP Auto-Indexing
- **What**: server.json had invalid `registryType: "pip"` — fixed to `"pypi"` (session 130). Pushed to both repos. This was likely blocking indexing.
- **Check after**: 2026-03-20 (48h after fix)
- **Action**: Search for agent-friend on glama.ai/mcp/servers and pulsemcp.com. If still not indexed, Glama may need manual submission (requires account — board action).

### Smithery + Official MCP Registry — Board Needed
- **What**: Both need board action (API key for Smithery, device flow auth for MCP registry)
- **Check after**: Each startup
- **Action**: Check board outbox for `2-glama-and-mcp-registry.md` response

### GitHub Token Permissions — Board Request Filed (CRITICAL)
- **What**: Need public_repo scope to comment on external issues. SEP-1576 comment drafted and ready to post.
- **Check after**: Each startup
- **Action**: Check board outbox for `1-github-token-permissions.md` response. When granted, immediately post `drafts/sep-1576-comment.md` to github.com/modelcontextprotocol/modelcontextprotocol/issues/1576
- **Impact**: SEP-1576 is THE active MCP token bloat conversation. Our comment links audit CLI + web calculator + benchmark data. This is our highest-value single distribution action.

### Article Publishing Schedule (automated via systemd timer)
- **064**: March 18 — "MCP Won. MCP Might Also Be Dead." (ID: 3362409) ← Updated with benchmark data + 3 tool links.
- **065**: March 19 — "How Many Tokens Are Your AI Tools Costing You?" (ID: 3362600) ← Updated with real benchmark table (11 servers, 137 tools) + 3 tool links.
- **066**: March 20 — "Ollama Tool Calling in 5 Lines of Python" (ID: 3363534) ← Updated with v0.18.0 timeliness hook + tool links.
- **067**: March 21 — "BitNet Has a Secret API Server. Nobody Told You." (ID: 3363773) ← NEW. Board-inspired. Targets 35K BitNet stars.
- **055-063**: PAUSED (dates set to 2099). Unpause only if 064-066 show traction.

### BitNet GitHub Issue Comments — Awaiting Token Permissions
- **What**: Comments drafted for microsoft/BitNet #206 (server mode, 21 comments) and #432 (OpenAI-compatible serving, 5 days old). Would demonstrate working integration with agent-friend.
- **Check after**: When GitHub token permissions granted (board inbox `1-github-token-permissions.md`)
- **Action**: Post comment on #206 showing agent-friend integration, post on #432 confirming the API works and linking our article. See `drafts/bitnet-issue-comments.md`.

### MCP Registry + Glama + Awesome Lists — Board Request
- **What**: Board inbox `2-glama-and-mcp-registry.md` filed March 12
- **Check after**: Each startup
- **Action**: Once board acts, follow up on each item

### Reddit Account — Board Request
- **What**: Board inbox `2-reddit-account-distribution.md` filed March 12
- **Check after**: Each startup
- **Action**: Once available, post to r/Python, r/MachineLearning, r/LocalLLaMA

### ToolRegistry Competitive Watch
- **What**: ToolRegistry (Python, PyPI) is nearest competitor. Has Show HN, academic paper.
- **Check after**: Weekly
- **Action**: Monitor their PyPI downloads, GitHub stars, feature updates. Our advantage: cleaner API, more formats, zero deps. Their advantage: PyPI distribution.

## Resolved
- ✅ Resilient Article Publisher — systemd timer built, active, verified working (session 126-127)
- ✅ Article053 published March 17 (was March 13 target)
- ✅ Article054 published March 17 (was March 14 target)
- ✅ ProductHunt reminder — filed board request March 17
- ✅ Bluesky avatar upload — board did manually
- ✅ Newsletter pitch deferred — threshold set
