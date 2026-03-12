# Waiting / Deferred Actions

## Active

### Anthropic v. DoD — March 24 Hearing
- **What**: Anthropic sued DoD over supply-chain risk designation (26-cv-01996, ND Cal)
- **Check after**: 2026-03-17 (government opposition due) + 2026-03-24 (preliminary injunction hearing)
- **Action**: Write article about outcome. Follow astral100 for updates. Search "Anthropic DoD hearing" on March 24.
- **Why it matters**: Our operational infrastructure runs on Claude. If Anthropic loses, affects their business model and long-term model development.

### Newsletter Pitch — Awaiting Traction Threshold
- **What**: Board approved the concept but wants more traction first. Re-pitch when threshold passed.
- **Threshold**: 50 Bluesky followers (currently 21) OR 15 Twitch followers (currently 5)
- **Check after**: On every startup, compare current followers against threshold
- **Action**: When threshold passed, recreate board inbox request with fresh pitch + updated numbers
- **Board response received**: 2026-03-11 — "Good idea, but want more experience/traction. Keep track with metric threshold, request again when passed."

### PyPI Publishing — Awaiting Traction Threshold
- **What**: Board responded to PyPI vault wrapper request: "Ask again once you have some demonstrated traction/interest."
- **Threshold**: GitHub stars or usage evidence on agent-* tools. Current: 1 star on main repo.
- **Check after**: On every startup, check GitHub stars on company repo and any agent-* related repos
- **Action**: When we hit 10+ stars OR see evidence of actual usage (GitHub issues, mentions, forks), re-request PyPI vault wrapper
- **Why it matters**: PyPI publishing would dramatically improve discoverability (`pip install agent-shield` vs the git+https URL)

### ProductHunt Submission — Board Approved Next Tuesday
- **What**: Board said "Remind me next Tuesday" (March 17) on 2-producthunt-submission.md.
- **Check after**: 2026-03-17
- **Action**: Re-file board/inbox request to submit agent-friend to ProductHunt. Best time: Tuesday 8-10am PT. Positioning: universal tool adapter, @tool → any framework. 51 tools, 2474 tests.

### Article053 — "21 Tools. Zero Product. That Changes Today."
- **What**: Draft on dev.to (ID: 3341088). Adapter story, 2474 tests, tags updated. Will auto-publish via day6_startup.sh.
- **Check after**: 2026-03-13 (auto-publishes via scheduler)
- **Action**: Verify published. day6_scheduler.sh posts Bluesky announcement at 13:00 UTC.

### Article054 — "I gave my AI agent an email address"
- **What**: Draft complete (products/content/article054_email_agent.md). Dev.to draft ID: 3341101.
- **Check after**: 2026-03-15 (2+ days after article053 on March 13)
- **Action**: `vault-devto PUT /articles/3341101 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article055 — Agents of Chaos
- **What**: Draft complete (products/content/article055_agents_of_chaos.md). About the Northeastern University study (6 AI agents on Discord, 2 weeks). Ties to agent-constraints, agent-id, agent-log, agent-health. Dev.to draft ID: **3341191**.
- **Check after**: 2026-03-17 (2+ days after article054, coincides with ProductHunt)
- **Action**: `vault-devto PUT /articles/3341191 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article056 — "Your AI Agent Needs a Database"
- **What**: Draft complete (products/content/article056_agent_database.md). DatabaseTool, SQLite for agents. Dev.to draft ID: **3341264**.
- **Check after**: 2026-03-19 (2+ days after article055 on March 17)
- **Action**: `vault-devto PUT /articles/3341264 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article057 — "Turning Any Python Function Into an AI Agent Tool"
- **What**: Draft complete (products/content/article057_tool_decorator.md). @tool decorator, type hints → JSON Schema. Dev.to draft ID: **3341307**.
- **Check after**: 2026-03-21 (2+ days after article056 on March 19)
- **Action**: `vault-devto PUT /articles/3341307 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article058 — "Your AI Agent Can Now Read CSV Files"
- **What**: Draft complete (products/content/article058_table_tool.md). TableTool, CSV/TSV for agents. Dev.to draft ID: **3341366**.
- **Check after**: 2026-03-23 (2+ days after article057 on March 21)
- **Action**: `vault-devto PUT /articles/3341366 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article059 — "Stop Paying for the Same API Call Twice"
- **What**: Draft complete (products/content/article059_cache_tool.md). CacheTool, TTL caching for agents. Dev.to draft ID: **3341425**.
- **Check after**: 2026-03-25 (2+ days after article058 on March 23)
- **Action**: `vault-devto PUT /articles/3341425 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article060 — "Your AI agent is trusting every webhook it receives"
- **What**: Draft complete (products/content/article060_crypto_tool.md). CryptoTool, HMAC verification, webhook security. Dev.to draft ID: **3341549**.
- **Check after**: 2026-03-27 (2+ days after article059 on March 25)
- **Action**: `vault-devto PUT /articles/3341549 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article061 — "Your AI agent is flying blind"
- **What**: Draft complete (products/content/article061_metrics_tool.md). MetricsTool, counters/gauges/timers/Prometheus. Dev.to draft ID: **3341573**.
- **Check after**: 2026-03-29 (2+ days after article060 on March 27)
- **Action**: `vault-devto PUT /articles/3341573 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article062 — "Stop hardcoding your AI agent's prompts"
- **What**: Draft complete (products/content/article062_template_tool.md). TemplateTool, ${variable} templates, template library. Dev.to draft ID: **3341598**.
- **Check after**: 2026-03-31 (2+ days after article061 on March 29)
- **Action**: `vault-devto PUT /articles/3341598 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Article063 — "Your AI code reviewer doesn't understand what changed"
- **What**: Draft complete (products/content/article063_diff_tool.md). DiffTool, unified diffs, word-level comparison, fuzzy matching. Dev.to draft ID: **3341613**.
- **Check after**: 2026-04-02 (2+ days after article062 on March 31)
- **Action**: `vault-devto PUT /articles/3341613 '{"article":{"published":true}}'` — then post Bluesky slot 1/4

### Discord AI Communities — Board Request Pending
- **What**: Filed 3-discord-ai-communities.md asking for help joining Anthropic/Claude Discord and Swarms/Agora Discord.
- **Check after**: Next session after board responds
- **Action**: Join relevant servers, participate in discussions, share agent-* tools when genuinely helpful

## Resolved
- **3-bsky-avatar-upload.md** — Board uploaded avatar manually 2026-03-11. Resolved.
- **4-newsletter-pitch-request.md** — Board responded 2026-03-11: wait for traction. Threshold set at 50 Bluesky followers. Moved to active waiting.
