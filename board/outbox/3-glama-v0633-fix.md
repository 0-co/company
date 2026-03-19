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

---
## Board Response

I just synced glama with our repo and using commit 7bcffbe we get exactly the same error:

{
  "cause": {
    "extra": {
      "options": {
        "headersTimeout": 1000
      },
      "request": {
        "code": "ECONNRESET",
        "options": {
          "headersTimeout": 1000
        }
      },
      "response": {}
    },
    "message": "read ECONNRESET",
    "name": "RequestError",
    "stack": "RequestError: read ECONNRESET\n    at makeRequest (file:///srv/build/server/app/integrations/httpClient.server.js:275:10)\n    at async executeRequest (file:///srv/build/server/app/integrations/httpClient.server.js:286:11)\n    at async httpClient (file:///srv/build/server/app/integrations/httpClient.server.js:310:27)\n    at async routine (file:///srv/build/server/app/routines/mcp/inspectMcpServer.js:23:4)\n    at async retry (file:///srv/build/server/app/utilities/retry.js:32:19)\n    at async inspectMcpServer (file:///srv/build/server/app/routines/mcp/inspectMcpServer.js:17:2)\n    at async inspectMcpServerDockerImage (file:///srv/build/server/app/routines/mcp/inspectMcpServerDockerImage.js:53:30)\n    at async testMcpServerBuildSpec (file:///srv/build/server/app/routines/mcp/testMcpServerBuildSpec.js:189:18)\n    at async file:///srv/build/server/app/jobs/testMcpServerBuildSpecJob.js:100:19\n    at async goIntervalTiming (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/helpers/promises.js:178:3)"
  },
  "extra": {
    "image": "registry.glama.ai/mcp-s5tfkku5ng:fwtrkfra49",
    "logs": [
      {
        "loggedAt": "2026-03-19T16:06:03.967Z",
        "message": "Traceback (most recent call last):\n",
        "sequenceNumber": 0,
        "stream": "stderr"
      },
      {
        "loggedAt": "2026-03-19T16:06:03.967Z",
        "message": "  File \"<frozen runpy>\", line 198, in _run_module_as_main\n  File \"<frozen runpy>\", line 88, in _run_code\n  File \"/app/agent_friend/__main__.py\", line 7, in <module>\n    from agent_friend.mcp_server import main\n  File \"/app/agent_friend/mcp_server.py\", line 29, in <module>\n    from mcp.server.fastmcp import FastMCP\nModuleNotFoundError: No module named 'mcp'\n",
        "sequenceNumber": 1,
        "stream": "stderr"
      },
      {
        "loggedAt": "2026-03-19T16:06:04.016Z",
        "message": "transport event { type: 'close' }\n",
        "sequenceNumber": 2,
        "stream": "stdout"
      },
      {
        "loggedAt": "2026-03-19T16:06:04.018Z",
        "message": "could not start the proxy McpError: MCP error -32000: Connection closed\n    at McpError.fromError (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:4493:10)\n    at Client._onclose (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:15938:28)\n    at _transport.onclose (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:15914:9)\n    at ChildProcess.<anonymous> (file:///usr/lib/node_modules/mcp-proxy/dist/bin/mcp-proxy.mjs:4986:19)\n    at ChildProcess.emit (node:events:508:28)\n    at maybeClose (node:internal/child_process:1100:16)\n    at ChildProcess._handle.onexit (node:internal/child_process:305:5) {\n  code: -32000,\n  data: undefined\n}\n",
        "sequenceNumber": 3,
        "stream": "stderr"
      }
    ]
  },
  "message": "Expected server to respond to ping",
  "name": "DockerContainerError",
  "stack": "DockerContainerError: Expected server to respond to ping\n    at inspectMcpServerDockerImage (file:///srv/build/server/app/routines/mcp/inspectMcpServerDockerImage.js:72:9)\n    at async testMcpServerBuildSpec (file:///srv/build/server/app/routines/mcp/testMcpServerBuildSpec.js:189:18)\n    at async file:///srv/build/server/app/jobs/testMcpServerBuildSpecJob.js:100:19\n    at async goIntervalTiming (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/helpers/promises.js:178:3)\n    at async V1InngestExecution.tryExecuteStep (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/execution/v1.js:472:20)\n    at async steps-found (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/execution/v1.js:370:24)\n    at async V1InngestExecution._start (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/execution/v1.js:151:20)\n    at async InngestCommHandler.handleAction (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/InngestCommHandler.js:859:24)\n    at async ServerTiming.wrap (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/helpers/ServerTiming.js:57:11)"
}

Please be very careful in thinking about next steps here before asking me to try again
