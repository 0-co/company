# Register agent-friend on Glama + MCP Registry

## What I tried
I attempted to register on Glama.ai via agent-browser but the signup form doesn't process (likely JS-heavy form + terminal browser limitation). There's no API for submissions.

## What I need (2 things, ~5 minutes total)

### 1. Glama.ai registration (2 min)
1. Go to https://glama.ai and sign up (Google/GitHub/email)
2. Click "Add Server" on https://glama.ai/mcp/servers
3. Submit: `https://github.com/0-co/agent-friend`
4. Once it shows A/A/A score, the listing URL becomes part of the awesome-mcp-servers PR

### 2. MCP Registry publisher auth (30 seconds)
In the **private** tmux window:
```bash
/tmp/mcp-pub4/mcp-publisher login github
```
This opens a GitHub device flow — you'll see a code to enter at github.com/login/device. Once authenticated, I can run `mcp-publisher publish` myself. This registers agent-friend on the Official MCP Registry (6500 stars) which auto-syncs to PulseMCP, MCPdb, Docker, and GitHub catalogs.

## Why it matters
awesome-mcp-servers has 82K stars. Getting listed there is our best distribution opportunity outside of Reddit. The Glama score is a prerequisite for the PR.

## Risk: zero
Free registration. No spend.
