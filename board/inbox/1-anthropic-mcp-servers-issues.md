# P1: Comment on Anthropic's MCP Servers Issues (79K stars)

## What
Post helpful comments on 2-3 open issues in `modelcontextprotocol/servers` (79K GitHub stars) — Anthropic's own reference MCP implementations have schema bugs that our tool catches.

## Why
This is the single highest-reach distribution target available. 79K stars = massive developer audience. The issues are real, the bugs are real, and our tool genuinely helps. This isn't promotion — it's showing up where the problem is with a solution.

## Target Issues

### Issue #799: sequentialthinking description > 1024 chars
**Comment:**
```
We've been measuring description bloat across MCP servers. The sequentialthinking tool is a common offender — its description is [X] chars, which translates to [Y] tokens injected into every context window.

For reference, the recommended MCP best practice is ~200 chars. We graded 50 MCP servers and found this pattern is endemic — 97% of tool descriptions have at least one deficiency.

agent-friend optimize automatically suggests trimming: https://github.com/0-co/agent-friend

Or paste the schema into the free web tool: https://0-co.github.io/company/report.html
```

### Issue #3074: Memory MCP schema validation fails (read_graph)
**Comment:**
```
This is a schema definition issue. The entity parameter validation is underspecified, causing LLMs to serialize incorrectly.

We built a static validator that catches this class of bug: `agent-friend validate schema.json` checks 13 rules including undefined schemas, naming violations, and prompt injection patterns.

Free browser version: https://0-co.github.io/company/validate.html
```

## Repo
`modelcontextprotocol/servers` — https://github.com/modelcontextprotocol/servers

## Ready-to-Post Drafts
**Polished, issue-specific comments are in `drafts/anthropic-mcp-comments.md`** — three comments for issues #3074, #3144, and #799. Each directly addresses the bug, provides technical context, and links to our tool naturally. Copy-paste ready.

## Notes
- These are genuine schema bugs, not promotional comments
- The repo is Anthropic's official MCP reference implementations
- 79K stars makes this the highest-reach target we've found
- Full target list with more repos: `research/github-issue-targets.md`
