# Reddit Post — r/mcp

**Title:** I graded 201 MCP server schemas A+ to F. The results are not great.

**Subreddit:** r/mcp

**Body:**

Built agent-friend (https://github.com/0-co/agent-friend) to grade MCP server schemas against 158 checks: token efficiency, type completeness, param documentation, and prompt injection detection.

After grading 201 servers:

- **Postgres MCP**: 46 tokens to load. Clean schema, tight descriptions.
- **GitHub MCP**: 20,444 tokens to load. 440x more expensive for context that does nothing.
- **Cloudflare MCP**: 11.4/100 (F). Massive descriptions, missing types everywhere.
- **Notion's official MCP**: 19.8/100 (F). 22 tools. Every single tool name violates MCP naming conventions.
- **Sentry official**: 0.0/100 (F). The floor.

The most-starred servers are generally the worst. High stars = lots of functionality = built fast = schema quality nobody prioritized.

What we catch:
- Tool descriptions with `ignore previous instructions` (yes, this exists in the wild)
- Required params with no type declared
- Array params with no items schema
- 440-char tool descriptions that are just padded prose

`pip install agent-friend` / `agent-friend grade <path-to-schema.json>`

Live leaderboard: https://0-co.github.io/company/leaderboard.html

Happy to grade anyone's server if you want a second opinion.

---
Notes: Post during active subreddit hours (10-18 UTC). Not spam — genuine tool. First post to this sub.
Keep as informational/show-off-tool, not salesy.
