# Board Request: Create awesome-mcp-servers PR (P4 — when convenient)

**Created**: 2026-03-18
**Priority**: P4
**Action needed**: Click a link (1 minute)

## Status

Everything is ready. The branch exists, the commit is made. I cannot create the PR from the fork because vault-gh returns HTTP 403 for cross-repo PR creation. You need to open the PR manually.

## The PR

**Repository**: punkpeye/awesome-mcp-servers (81.5K stars)
**From branch**: 0-co/awesome-mcp-servers:add-agent-friend
**To branch**: punkpeye/awesome-mcp-servers:main
**Category**: Developer Tools (entry goes first alphabetically — `0-co` before all other entries)

**One-click PR creation URL**:
https://github.com/punkpeye/awesome-mcp-servers/compare/main...0-co:awesome-mcp-servers:add-agent-friend

## Suggested PR title and body

**Title**: Add 0-co/agent-friend - build-time MCP schema quality linter

**Body**:
```
## What this adds

[0-co/agent-friend](https://github.com/0-co/agent-friend) — a build-time MCP schema quality linter and grader (Python).

**Category**: Developer Tools

## Why it belongs here

- Validates MCP tool definitions against 13 quality checks: token cost, naming conventions, schema completeness, prompt override detection
- Grades servers A+ to F (weighted: schema quality 40%, token efficiency 30%, naming 30%)
- CLI tools: validate, audit, optimize, fix, grade + GitHub Action
- Web report card: https://0-co.github.io/company/report.html
- Audited 50 popular MCP servers from this list — top 4 by stars all score D or below

## Evidence

- 50 servers graded, 1,044 tools, 193K tokens analyzed
- Leaderboard: https://0-co.github.io/company/leaderboard.html
- Listed on Glama, mcpservers.org
```

## Entry being added

Inserted at the top of the Developer Tools section (line 665 of README, before 3KniGHtcZ/codebeamer-mcp):

```
- [0-co/agent-friend](https://github.com/0-co/agent-friend) 🐍 🏠 🍎 🪟 🐧 - Build-time MCP schema quality linter and grader. Validates tool definitions across 13 checks including token cost, naming conventions, and prompt override detection. Grades servers A+ to F. CLI, GitHub Action, and web report card. Audited 50 popular servers.
```
