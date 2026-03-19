# P3: Glama — ROOT CAUSE FOUND — Deploy v0.63.3

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## Root cause identified from your build logs

Glama calls `python -m agent_friend` (not `agent-friend`).
The `__main__.py` was calling the CLI chat interface instead of the MCP server.

## The actual fix (v0.63.3)

Changed `agent_friend/__main__.py`:
```python
# Before (broken): ran the chat CLI
from agent_friend.cli import main

# After (fixed): runs the MCP server
from agent_friend.mcp_server import main
```

## Proof it works

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}' | python3 -m agent_friend
```
Output: valid JSON-RPC initialize response with 314 tools. ✓

## Action needed

1. Go to https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile
2. Deploy again — Glama will clone from HEAD which now has v0.63.3
3. The build will use `git checkout <current HEAD>` which is commit `7b3ffbe`

The fix is committed and released as v0.63.3.
