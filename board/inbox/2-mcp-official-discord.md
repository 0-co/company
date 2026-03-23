# Request: Get agent-friend into MCP Official Discord

**Priority:** 2 (high — 11,658 members, biggest untapped distribution channel)

## What

Please join the MCP Official Discord server and post about agent-friend in the appropriate channel (tools/devtools/showcase).

Discord invite: The official MCP Discord is at discord.gg/modelcontextprotocol (or findable via modelcontextprotocol.io)

## Why this matters

- 11,658 members — largest MCP community outside GitHub
- These are exactly our target users: MCP server authors
- Our tools are directly useful to them: agent-friend grades schemas, mcp-patch finds security issues
- No announcement has been made here yet

## Suggested post

For a #tools or #devtools channel:

> **agent-friend** — grade your MCP server schemas and find what's eating your context window
>
> Built a CLI that scores MCP server schemas A+ to F (156 checks) and auto-fixes the most common issues.
>
> pip install agent-friend
> agent-friend grade server.json
>
> **What we found grading 201 servers:**
> - Token costs vary 440x: GitHub's MCP = 20,444 tokens. sqlite = 46 tokens.
> - 100% of servers have at least one quality issue
> - Official MCP fetch server has a prompt injection in its description
>
> Live leaderboard: https://0-co.github.io/company/leaderboard.html
> GitHub: https://github.com/0-co/agent-friend

## Also if there's a #show-and-tell or #announcements channel

The same message works there. Or we could post about specific findings (like the Notion MCP audit: 19.8/100, every tool name violates spec).

## Notes

- If a specific "self-promotion" policy requires a particular format or channel, please follow it
- The leaderboard is genuinely useful to the community (free, searchable, 201 servers graded)
- We're not asking for a permanent presence — just a single well-placed post
