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

### 3. awesome-mcp-servers PR (already pre-staged, just needs your click)
The fork is ready at `github.com/0-co/awesome-mcp-servers` branch `add-agent-friend-v2`.
My token can't create cross-repo PRs. To create the PR:
1. Go to https://github.com/0-co/awesome-mcp-servers/compare/main...add-agent-friend-v2
2. Click "Create pull request"
3. Title: "Add agent-friend to Frameworks section"
4. Done. I wrote the entry and committed it.

### 4. Smithery.ai API key (30 seconds)
Smithery has 2K+ MCP servers indexed, integrates with Cursor IDE. CLI publish is one command but needs an API key:
1. Sign up at https://smithery.ai (GitHub login works)
2. Go to https://smithery.ai/account/api-keys
3. Create an API key and share it via outbox (I'll add to vault)
4. Then I run: `npx @smithery/cli mcp publish https://github.com/0-co/agent-friend`

### Already done (no board needed)
- ✅ mcpservers.org submitted (2026-03-17) — awaiting approval
- ✅ server.json updated to v0.51.0 with pip registry type
- ✅ Glama/PulseMCP should auto-discover via server.json in repo

## Risk: zero
Free registration. No spend.
