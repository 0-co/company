# P3: Re-deploy Glama — v0.62.1 fixes the instance failure

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## The fix

Pushed v0.62.1 to agent-friend `main`. Root cause: Glama's mcp-proxy was calling `agent-friend` (the chat CLI) instead of the MCP server, because there was no `agent-friend-mcp` entry point in the pip package.

**What changed in v0.62.1:**
- Added `agent_friend/mcp_server.py` as a proper package module with a `main()` function
- Added `agent-friend-mcp = "agent_friend.mcp_server:main"` to pyproject.toml
- Updated Dockerfile to install the package so `agent-friend-mcp` command is available
- Fixed `.dockerignore` to allow README.md for pip install

## Action needed

Go to: https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile

Click **Deploy** again. The Dockerfile now does:
1. Copies source files
2. `pip install -e .` — installs `agent-friend-mcp` entry point
3. `CMD ["agent-friend-mcp"]` — runs the actual MCP server

Should fix "Connection closed" error. The `agent-friend-mcp` command starts the MCP stdio server (314 tools).

## If it still fails

Let me know the error output — I can debug further.
