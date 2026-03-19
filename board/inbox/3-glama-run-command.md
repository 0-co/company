# P3: Glama — Fix Run Command in Admin UI

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## Root Cause Found

The Glama schema (`https://glama.ai/mcp/schemas/server.json`) only supports
one field: `maintainers`. The `command`/`args` we added are completely ignored.

Glama's proxy is spawning `agent-friend` bare on their host machine. That
command doesn't exist in their Node.js environment — hence `ENOENT`.

## The Fix

In the Glama admin UI, the run command is likely configurable directly.
You need to change it from:
```
agent-friend
```
to:
```
uvx agent-friend
```

`uvx` downloads and runs Python CLI tools from PyPI without a permanent install.
Since `agent-friend` is on PyPI, `uvx agent-friend` will:
1. Download agent-friend from PyPI (first run)
2. Run `agent-friend` CLI, which detects piped stdin and starts MCP server mode

## Steps

1. Go to https://glama.ai/mcp/servers/0-co/agent-friend/admin
2. Look for "Run Command", "Start Command", "Proxy Command", or similar field
3. Change the command to: `uvx`
4. Set args to: `agent-friend`  (or just put `uvx agent-friend` in the command field, however their UI works)
5. Save + trigger a redeploy

## Alternative: Check if They Have a Docker Mode

If the admin UI shows a Docker toggle/option, enabling that would also work
since our Dockerfile runs `agent-friend-mcp` which is correct. But uvx is simpler.

## Note on glama.json

The `command`/`args` fields we added to glama.json are for CLIENT-side 
configuration only (telling users how to install it locally). They have no
effect on Glama's own proxy. I'll revert those fields to keep the file clean.
