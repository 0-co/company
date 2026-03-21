# Request: Get listed in punkpeye's MCP lists (2 repos)

**Priority:** 2 (high)

## What

Please create issues or PRs on TWO of punkpeye's repos to get agent-friend listed:

1. **https://github.com/punkpeye/awesome-mcp-servers** — Developer Tools section
2. **https://github.com/punkpeye/awesome-mcp-devtools** — directly relevant: "developer tools, SDKs, libraries, and testing utilities for MCP server development" (436 stars, our exact target audience)

## Why this matters

- awesome-mcp-servers: **83,728 stars** — largest MCP server directory
- **awesome-mcp-devtools: 436 stars, our exact audience** — MCP server developers who want schema quality tools
- punkpeye (Frank Fiegel) = Glama.ai founder + r/mcp founder, **forked agent-friend on March 17** (unprompted)
- Frank is the single most-connected person in the MCP ecosystem outside Anthropic — being on his lists = being found by every MCP developer
- I attempted to create GitHub issues but vault-gh is scoped to own repos only

## Suggested issue title

"Add agent-friend: MCP schema quality grader and token-bloat fixer"

## Suggested issue body

```
Hi! I built agent-friend (https://github.com/0-co/agent-friend), a CLI that grades and fixes MCP server schemas.

**What it does:**
- `agent-friend grade <url>` — letter grade (A+ to F) based on 158 static checks
- `agent-friend fix <schema.json>` — auto-patches ~30% of schema issues
- GitHub Action for CI
- Live leaderboard of 200+ graded MCP servers: https://0-co.github.io/company/leaderboard.html

**Why it fits:**
Developer tool for MCP authors — catches schema issues that cause token bloat, ambiguous calls, LLM reliability failures. ESLint for MCP schemas.

Would love to be listed in the Developer Tools section. Happy to add a PR that matches your README conventions.

(Note: you forked the repo on March 17 — thanks for looking at it!)
```

## awesome-mcp-devtools suggested entry

For `punkpeye/awesome-mcp-devtools`, add to the appropriate section:

```
- [agent-friend](https://github.com/0-co/agent-friend) — CLI that grades MCP server schemas A+ to F. 158 checks covering token cost, schema quality, prompt injection detection. GitHub Action + pre-commit hook. Live leaderboard: 201 servers graded.
```

## Alternatively

If easier: email contact@glama.ai or DM punkpeye on GitHub with the above. He's active on GitHub (his awesome-mcp-servers was updated 2h ago). He's aware of agent-friend from the fork.

Also: please follow up on the earlier board request `3-glama-run-command.md` (Glama uvx fix) if not yet done — punkpeye controls both repos.
