# P1: Open PRs + Issues on MCP awesome lists and directories

**Why this matters:** awesome-mcp-servers has 81,500 stars. It's the single highest-reach distribution channel available. punkpeye already knows us from the Glama badge PR he merged. awesome-mcp-devtools (435 stars) is the only awesome list specifically for MCP developer tools — we're a perfect fit. **UPDATE:** We now have 36 graded servers (1,044 tools, 193K tokens analyzed). The top 4 most popular MCP servers all score D or below.

## PR 1: punkpeye/awesome-mcp-servers (81.5K stars)

**File:** `servers/README.md`
**Section:** `### Developer Tools` (under `## 🧰 Utilities`)
**Position:** First entry (alphabetical: `0-co` comes before `21st-dev`)

**Diff:**
```diff
 ### Developer Tools

+- [0-co/agent-friend](https://github.com/0-co/agent-friend) 🐍 🏠 - MCP tool schema linter and quality auditor. Validates tool definitions (12 checks), audits token costs, and grades quality (A+ through F). Graded 50 servers, 1,044 tools, 193K tokens of overhead — top 4 most popular all score D or below.
 - [21st-dev/magic-mcp](https://github.com/21st-dev/magic-mcp) - MCP server for 21st.dev — the NPM for AI-generated UI components.
```

**PR title:** Add agent-friend (MCP tool schema linter) to Developer Tools
**PR body:**
```
Adds [agent-friend](https://github.com/0-co/agent-friend) — an MCP tool schema linter and quality auditor.

- **validate**: 12 correctness checks against tool schemas
- **audit**: token cost analysis across 6 formats (OpenAI, Anthropic, MCP, Google, Ollama, JSON Schema)
- **optimize**: automated fix suggestions for verbose schemas
- **grade**: letter grade report card (A+ through F)

Available as CLI, GitHub Action, and browser tools. MIT licensed. Python.

Graded 36 MCP servers — the 4 most popular all score D or below: https://0-co.github.io/company/leaderboard.html
```

## PR 2: punkpeye/awesome-mcp-devtools (435 stars)

**File:** `README.md`
**Section:** `## Testing Tools`
**Position:** First entry (alphabetical: `0-co` comes before `mclenhard`)

**Diff:**
```diff
 ## Testing Tools
 > Tools for testing MCP servers and clients

+- [0-co/agent-friend](https://github.com/0-co/agent-friend) 🐍 - MCP tool schema linter and quality auditor. Validates schemas (12 checks), audits token costs, optimizes descriptions, and grades quality (A+ through F). CLI, GitHub Action, and browser tools.
 - [mclenhard/mcp-evals](https://github.com/mclenhard/mcp-evals) 🤖 - Package and Github action for running evals.
```

**PR title:** Add agent-friend (MCP tool schema linter) to Testing Tools
**PR body:**
```
Adds [agent-friend](https://github.com/0-co/agent-friend) — a build-time MCP tool schema linter.

Validates tool definitions against 12 correctness checks, audits token costs across 6 schema formats, optimizes verbose descriptions, and produces letter-grade report cards (A+ through F).

Available as CLI, GitHub Action, and browser tools. MIT licensed.
```

## Issue 3: MCP.so directory (chatmcp/mcpso) — 16,670+ servers

**How:** Open a GitHub issue on `chatmcp/mcpso` (this is how all submissions work — see issues #853-#857)

**Issue title:** Add agent-friend — MCP tool schema linter and quality auditor
**Issue body:**
```
## Server Info

- **Name:** agent-friend
- **GitHub:** https://github.com/0-co/agent-friend
- **Homepage:** https://0-co.github.io/company/tools.html
- **Description:** MCP tool schema linter and quality auditor. Validates tool definitions (12 checks), audits token costs across 6 formats, optimizes descriptions, and grades quality (A+ through F). Graded 50 servers, 1,044 tools, 193K tokens of overhead — top 4 most popular all score D or below. Available as CLI, GitHub Action, and browser tools.
- **Language:** Python
- **License:** MIT
- **Category:** Developer Tools
```

## Issue 4: Cline MCP Marketplace (cline/mcp-marketplace) — millions of Cline users

**How:** Open a GitHub issue using their template at `cline/mcp-marketplace`

**Issue URL:** https://github.com/cline/mcp-marketplace/issues/new?template=mcp-server-submission.yml
**Fields to fill:**
- **GitHub Repo URL:** https://github.com/0-co/agent-friend
- **Logo Image:** (we need a 400x400 PNG — board may need to create one or use profile.jpg)
- **Reason for Addition:** "agent-friend is an MCP tool schema linter — the only build-time quality checker for MCP tool definitions. It validates schemas against 12 correctness checks, audits token costs across 6 formats, and grades quality (A+ through F). We graded 27 popular MCP servers — the top 4 most popular all score D or below. 1,044 tools, 193K tokens analyzed. Cline users building MCP servers can catch schema errors before deployment. MIT licensed, 3,068 tests."

**Note:** They require testing that Cline can install from the README. Our README has clear pip install instructions. They also evaluate "community adoption" (our stars are 0, but we have strong documentation and test coverage).

## Priority Order
1. **awesome-mcp-servers PR** (81,500 stars) — highest reach by 100x
2. **awesome-mcp-devtools PR** (435 stars) — exact category fit
3. **MCP.so issue** (16,670+ servers) — standard submission process
4. **Cline Marketplace issue** (millions of users) — may reject for low stars, but worth trying

## Notes
- punkpeye merged our Glama badge PR — warm relationship for PRs 1 and 2
- All submissions follow exact formats from their contributing guides
- Our PAT can't fork/PR/issue on external repos, so board needs to open these
- MCP.so has 857 prior submissions via issues
- Cline reviews within "a couple of days"
- **Updated March 18**: Numbers updated from 11→50 servers, 137→1,044 tools, 27K→193K tokens, 2894→3068 tests. Leaderboard link replaces benchmark link.
