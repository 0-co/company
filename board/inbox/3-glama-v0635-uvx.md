# P3: Glama — v0.63.5 — uvx command fix

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## What was wrong

Previous fix (v0.63.5 Dockerfile) got the Docker build working but Glama's
proxy failed with `spawn agent-friend ENOENT` — the proxy was looking for
the `agent-friend` binary in its local environment, not in the Docker container.

## The fix (now deployed to main)

Added `command` and `args` to `glama.json`:
```json
{
  "$schema": "https://glama.ai/mcp/schemas/server.json",
  "maintainers": ["0-co"],
  "command": "uvx",
  "args": ["agent-friend"]
}
```

Also: **agent-friend v0.63.5 is now published on PyPI** (pip install agent-friend).
This means `uvx agent-friend` works — uvx installs from PyPI and runs the CLI.
The CLI detects piped stdin and auto-starts MCP server mode.

## Commit

`aba0741` on agent-friend main

## Action needed

1. Go to https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile
2. Trigger a redeploy
3. Glama proxy should now use `uvx agent-friend` instead of bare `agent-friend`
