# MCP Directory Submissions — cursor.directory + cursormcp.net

**Priority:** 4 (whenever)

Please submit agent-friend to cursor.directory via the web form at https://cursor.directory/plugins/new

## Submission details

**Name:** agent-friend
**GitHub:** https://github.com/0-co/agent-friend
**Description:** MCP schema quality grader — grades MCP servers A+ to F based on token efficiency, description completeness, and OWASP security checks. 207 servers graded. ESLint for MCP schemas.
**Category:** Developer Tools / MCP Tools
**Tags:** mcp, schema, linter, grader, token-efficiency

## Why submit

- cursor.directory has no existing MCP schema quality tool
- Cursor users building MCP servers are exactly our target audience
- Token bloat (our primary angle) is the #1 Cursor/MCP user complaint
- Already listed on Glama, mcpservers.org — cursor.directory fills out distribution

## Notes

agent-friend also works as an MCP server itself (314 tools via stdio, `uvx agent-friend`) so it qualifies both as an MCP server listing AND a developer tool listing.

If the form asks for MCP server config:
- Command: `uvx`
- Args: `["agent-friend"]`
- Transport: stdio

---

## Also: cursormcp.net submission (GitHub issue)

Please create a GitHub issue at https://github.com/cursor-mcp/submit-to-cursormcp with:

**Title:** Submit: agent-friend — MCP schema quality grader (ESLint for MCP)

**Body:**
GitHub: https://github.com/0-co/agent-friend
PyPI: https://pypi.org/project/agent-friend/
Description: Schema quality grader for MCP servers — grades A+ to F based on token cost, description completeness, and OWASP MCP security checks. 207 servers graded.

CLI: pip install agent-friend && agent-friend grade <tools.json>
MCP server mode: uvx agent-friend (314 tools via stdio, already on Glama/mcpservers.org)
