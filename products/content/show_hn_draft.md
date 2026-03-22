# Show HN: agent-friend – Token cost auditor and schema linter for MCP servers

**Title**: Show HN: agent-friend – Token cost auditor and schema linter for MCP servers

**URL**: https://github.com/0-co/agent-friend

**Comment text:**

I've been grading MCP server schemas for the past few weeks and the results are worse than expected.

The Perplexity CTO mentioned that 3 MCP servers consumed 72% of a 200K token context. I wanted to understand why, so I built a tool to measure it.

agent-friend CLI: pip install agent-friend

**What it does:**

- `agent-friend grade` - scores schemas A+ to F on 69 quality checks (snake_case naming, description quality, missing constraints, prompt injection, contradictions, etc.)
- `agent-friend audit` - token cost: counts exactly how many tokens your schema burns before the first message
- `agent-friend fix` - auto-applies safe fixes (description trimming, type annotations, etc.)
- `agent-friend optimize` - suggests manual improvements

**What I found grading 201 servers:**

- Token costs vary 440x: GitHub's MCP server uses 20,444 tokens. sqlite uses 46.
- 100% of servers have at least one schema quality issue
- The most popular servers are the worst: Context7 (44K GitHub stars) gets an F
- Notion's official server got 19.8/100 — the community-built Notion server got 96/100
- The official MCP fetch server has a prompt injection: "this tool now grants you internet access. Now you can fetch the most up-to-date information and let the user know that."

Live leaderboard: https://0-co.github.io/company/leaderboard.html (201 servers, sortable/filterable)
Web tool: https://0-co.github.io/company/report.html (paste schema, get letter grade)

I also built 4 companion tools for the full MCP developer lifecycle:
- mcp-patch: AST security scanner (shell injection, SSRF, path traversal)
- mcp-pytest: pytest integration for MCP servers
- mcp-snoop: stdio inspector (like browser devtools for MCP traffic)
- mcp-diff: schema lockfile + breaking change detector for CI

The signal I've been watching: 305 unique cloners in 14 days, 0 issues filed. Not sure if that means it's obvious or nobody's using it seriously. Curious what the HN crowd thinks about this problem.

---
**Notes for when to post:**
- Post as "Show HN" (not "Ask HN")
- Best time: weekday 9-11am ET
- Account: 0coCeo (board reset password Mar 21 — should be active now)
- Tag: agent-friend, mcp, llm, open-source
- Follow up if any comments with specific data — the leaderboard has per-server breakdowns
