# P3: Re-deploy Glama — v0.63.1 fixes the command mismatch

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## Root Cause Found

Glama's mcp-proxy was calling `agent-friend` (the chat CLI) instead of `agent-friend-mcp` (the MCP server). This caused the CLI help text to appear instead of JSON-RPC responses.

The fix is now in v0.63.1: `agent-friend` auto-detects MCP server mode when stdin is piped (not a TTY). So whether Glama calls `agent-friend` or `agent-friend-mcp`, it now starts the MCP stdio server.

## What changed in v0.63.1

In `agent_friend/cli.py`, added at the top of `main()`:
```python
if len(sys.argv) == 1 and not sys.stdin.isatty():
    from .mcp_server import main as _mcp_main
    _mcp_main()
    return
```

When called with no args and stdin is piped → MCP server (314 tools).
When called from terminal with no args → still shows help (unchanged).

## Action needed

Go to: https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile

Click **Deploy** again. v0.63.1 is live at https://github.com/0-co/agent-friend/releases/tag/v0.63.1

The Dockerfile CMD is still `agent-friend-mcp` (correct), but now `agent-friend` also works. Either way, Glama's mcp-proxy should get a proper MCP server response.
