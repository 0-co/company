# Register agent-friend on Glama.ai → Submit to awesome-mcp-servers (82K stars)

## Why this matters
awesome-mcp-servers has **82,000 stars**. Getting listed there is the highest-impact distribution move available. Every requirement except Glama account creation is done.

## What I've already done
1. Added MIT LICENSE file to repo root (was missing)
2. Added Dockerfile that builds the MCP server
3. Both repos synced (company + agent-friend)
4. Researched all submission requirements thoroughly (per your request)

## What needs human action

### Step 1: Register on Glama.ai
1. Go to https://glama.ai and create an account (requires signup)
2. Navigate to https://glama.ai/mcp/servers and click "Add Server"
3. Submit: `https://github.com/0-co/agent-friend`
4. Verify the server gets an **A / A / A** score (Security, Quality, License)

### Step 2: Create PR to awesome-mcp-servers
Once Glama shows A/A/A score, the PR needs updating. The fork branch `0-co:add-agent-friend` exists but needs the Glama link added.

The entry format should be (in the Developer Tools section, alphabetically):
```
- [0-co/agent-friend](https://github.com/0-co/agent-friend) [glama](https://glama.ai/mcp/servers/0-co/agent-friend) 🐍 🏠 🍎 🪟 🐧 - Universal tool adapter: @tool decorator exports Python functions to OpenAI, Claude, Gemini, MCP, JSON Schema. 51 built-in tool classes, 2474 tests.
```

PR comparison URL: https://github.com/punkpeye/awesome-mcp-servers/compare/main...0-co:add-agent-friend

## BONUS: Official MCP Registry (cascades to PulseMCP, MCPdb, Docker, GitHub)

I downloaded the `mcp-publisher` CLI and validated our server.json. Publishing to the **Official MCP Registry** (6500 stars) auto-syncs to PulseMCP (9000+ servers), MCPdb (10,000+), and GitHub/Docker catalogs. One submission → everywhere.

**What you'd need to do**: Run `mcp-publisher login github` in the private tmux window — it uses GitHub device flow (enter a code at github.com/login/device). Takes 30 seconds. Then I can `mcp-publisher publish` myself.

The binary is at `/tmp/mcp-pub4/mcp-publisher` and the validated `server.json` is in `products/agent-friend/`.

## Risk: zero
Free registration. No spend. High potential visibility.
