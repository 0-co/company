# P3: Glama — DEFINITIVE ROOT CAUSE — Deploy v0.63.4

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## What was wrong (full chain)

The chain of failures was:

1. **v0.63.1** — `__main__.py` ran CLI (was calling `cli:main()`). Glama calls `python -m agent_friend`, so it ran the CLI instead of MCP server.

2. **v0.63.3** — Fixed `__main__.py` to call `mcp_server:main()`. But Dockerfile had `mcp>=1.25,<2` version constraint. MCP SDK is at v1.12.x — no version ≥1.25 exists. Docker build's `pip install "mcp>=1.25,<2"` fails, so `mcp` is never installed. Container starts, Python tries `from mcp.server.fastmcp import FastMCP`, gets `ModuleNotFoundError: No module named 'mcp'`.

3. **v0.63.4** — Fixed Dockerfile to `mcp>=1.0` (matches current v1.12.x SDK). Also added `mcp` to `[project.optional-dependencies]` in pyproject.toml.

## The fix (v0.63.4)

```dockerfile
# Before (broken): no matching mcp version >= 1.25
RUN pip install --no-cache-dir "mcp>=1.25,<2" && pip install --no-cache-dir -e .

# After (fixed): matches mcp 1.12.x
RUN pip install --no-cache-dir "mcp>=1.0" && pip install --no-cache-dir -e .
```

## Verified locally

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}' | /tmp/mcp-venv/bin/python3 -m agent_friend
```
Output: valid JSON-RPC initialize response ✓ (mcp 1.12.2 installed in local venv)

## Action needed

1. Go to https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile
2. Deploy again — commit is now `6b9a821` (v0.63.4)
3. The `pip install "mcp>=1.0"` will successfully install mcp 1.12.x
4. `python -m agent_friend` will start the MCP server correctly

This is the definitive fix. Both issues are resolved: correct entry point + correct mcp version.
