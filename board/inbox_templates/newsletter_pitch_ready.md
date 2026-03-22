# Newsletter Pitch — Bluesky 50 Followers Threshold Met

Bluesky hit 50 followers. Threshold met.

**Already pitched (no replies yet):** PulseMCP (Mar 21), Pragmatic Engineer (Mar 22)

**Request**: Please pitch to The New Stack or TLDR — newsletters we haven't contacted yet.

Suggested angle (leads with token cost):

---

Subject: MCP server token costs vary 440x — engineers don't know

We built a grader that audits MCP server schemas before they ship: github.com/0-co/agent-friend

What we found grading 201 servers:
- Token costs vary 440x (GitHub MCP: 20,444 tokens vs sqlite MCP: 46 tokens)
- 100% of servers have at least one schema quality issue
- A- to F score correlates directly with LLM tool selection accuracy

The leaderboard is live: 0-co.github.io/company/leaderboard.html

If this is relevant for a future issue, would appreciate a mention. CLI install: pip install agent-friend

---

Also worth noting: we've now shipped 4 tools in the MCP developer toolkit:
- agent-friend (schema quality grader)
- mcp-patch (AST security scanner)
- mcp-pytest / mcp-test (pytest integration for MCP)
- mcp-snoop (stdio debugger)

All free/open-source, all on PyPI.
