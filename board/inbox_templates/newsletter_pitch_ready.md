# Newsletter Pitch — Bluesky 50 Followers Threshold Met

Bluesky hit 50 followers. Threshold met.

**Already pitched (no replies yet):** PulseMCP (Mar 21), Pragmatic Engineer (Mar 22)

**Request**: Please pitch to The New Stack AND TLDR — newsletters we haven't contacted yet.

**Note for The New Stack pitch**: They already published "10 strategies to reduce MCP token bloat" — reference their coverage and position agent-friend as the tool to implement their advice.

Suggested angle for The New Stack (leads with their own coverage):

---

Subject: MCP server token costs vary 440x — we built the tool to measure it

You published "10 strategies to reduce MCP token bloat" — we built the tool to audit those strategies automatically.

agent-friend grades MCP server schemas before they ship: github.com/0-co/agent-friend

What we found grading 201 servers:
- Token costs vary 440x (GitHub MCP: 20,444 tokens vs sqlite MCP: 46 tokens)
- 100% of servers have at least one schema quality issue
- Perplexity CTO ditched MCP over token bloat. We're building the fix.

The leaderboard is live: 0-co.github.io/company/leaderboard.html

CLI install: pip install agent-friend

---

Suggested angle for TLDR (shorter, data-first):

Subject: MCP server token costs vary 440x — engineers don't know

We built a grader that audits MCP server schemas: github.com/0-co/agent-friend

Grading 201 servers: token costs vary 440x. 100% have at least one schema issue. GitHub's official MCP server: 20,444 tokens before a single message. sqlite MCP: 46 tokens.

Live leaderboard: 0-co.github.io/company/leaderboard.html

---

Also: we've shipped 5 tools in the MCP developer toolkit (all free/open-source, all on PyPI):
- agent-friend (schema quality grader + token auditor)
- mcp-patch (AST security scanner — shell injection, SSRF, path traversal)
- mcp-pytest / mcp-test (pytest integration for MCP)
- mcp-snoop (stdio debugger — shows JSON-RPC traffic)
- mcp-diff (schema lockfile — detects breaking changes in CI)
