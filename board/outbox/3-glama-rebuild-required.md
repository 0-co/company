# P3: Glama — Needs Full Docker Rebuild (Not Just Restart)

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## The fix IS working — verified locally

v0.63.1 TTY detection works. Test proof:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}' | agent-friend
```

Output: valid JSON-RPC initialize response (314 tools registered). ✓

When stdin is piped (not a TTY), `agent-friend` now starts the MCP server correctly.

## Why it still failed at 14:33 UTC

Glama's "Deploy" button likely **restarts the existing container** rather than rebuilding the Docker image from source. The running container still has v0.63.0 from before the fix.

## What's needed

Trigger a **full Docker image rebuild** from the new source:
1. Go to https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile
2. Look for a **"Rebuild"** or **"Build new image"** button (different from just "Deploy")
3. If there's no separate rebuild option, try removing the server and re-adding it

The Dockerfile copies source files (`COPY agent_friend/ agent_friend/`) — so a fresh build will pick up v0.63.1's TTY detection fix.

## Expected result after rebuild

Glama's mcp-proxy calls `agent-friend` → auto-detects piped stdin → starts MCP stdio server → 314 tools available → security/quality tests pass.

---
## Board Response

same error. it definitely rebuilds from scratch

Skip to main content
Glama
Glama
MCP
Servers
Search MCP servers, tools, and more
0-co
agent-friend

Favorite
Developer Tools
Autonomous Agents
by 0-co
Python
Hybrid
Profile
Repository
Dockerfile
019d06ab-b739-73a5-b700-1a1c96d18ebd
2026-03-19 15:16
ID	019d06ab-b739-73a5-b700-1a1c96d18ebd
Status	failure
Duration	34.2s
Build Spec
{
  "buildSteps": [
    "uv sync"
  ],
  "cmdArguments": [
    "mcp-proxy",
    "--",
    "python",
    "-m",
    "agent_friend"
  ],
  "nodeVersion": "24",
  "pinnedCommit": null,
  "placeholderArguments": {},
  "pythonVersion": "3.14"
}
Error
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
    "image": "registry.glama.ai/mcp-s5tfkku5ng:lzg8j3p2om",
    "logs": [
      {
        "loggedAt": "2026-03-19T15:16:51.580Z",
        "message": "[mcp-proxy] ignoring non-JSON output [\n  'usage: agent-friend [-h] [--interactive] [--seed SEED] [--model MODEL]',\n  '                    [--tools TOOLS] [--config CONFIG] [--budget BUDGET]',\n  '                    [--no-color] [--demo] [--version]',\n  '                    [message]',\n  'agent-friend — universal AI tool adapter. Write once, export everywhere.',\n  'Quick start:',\n  '  agent-friend --demo                   # see @tool exports (no API key)',\n  '  agent-friend --version                # show version',\n  '  agent-friend -i                       # interactive chat (needs API key)',\n  '  agent-friend audit <file.json>        # token cost report for tool defs',\n  '  agent-friend optimize <file.json>     # suggest token-saving rewrites',\n  '  agent-friend validate <file.json>     # check schemas for correctness',\n  '  agent-friend fix <file.json>          # auto-fix schema issues',\n  '  agent-friend grade <file.json>        # combined quality report card',\n  '  agent-friend grade --example notion    # grade a bundled example schema',\n  '  agent-friend examples                 # list available example schemas',\n  'positional arguments:',\n  '  message            Send a single message and exit',\n  'options:',\n  '  -h, --help         show this help message and exit',\n  '  --interactive, -i  Start an interactive multi-turn chat session',\n  '  --seed SEED        System prompt (default: helpful assistant)',\n  '  --model MODEL      Model to use. Auto-detected from API key if not set.',\n  '                     Anthropic key → claude-haiku-4-5-20251001 OpenRouter key',\n  '                     → google/gemini-2.0-flash-exp:free (free!) OpenAI key →',\n  '                     gpt-4o-mini',\n  '  --tools TOOLS      Comma-separated tools: search,code,memory,browser,email',\n  '                     (default: none)',\n  '  --config CONFIG    Path to a YAML config file',\n  '  --budget BUDGET    Spending limit in USD (free models cost $0)',\n  '  --no-color         Disable colored output',\n  '  --demo             Run a quick demo of @tool exports (no API key needed)',\n  \"  --version, -V      show program's version number and exit\"\n]\n",
        "sequenceNumber": 0,
        "stream": "stderr"
      },
      {
        "loggedAt": "2026-03-19T15:16:51.626Z",
        "message": "transport event { type: 'close' }\n",
        "sequenceNumber": 1,
        "stream": "stdout"
      },
      {
        "loggedAt": "2026-03-19T15:16:51.628Z",
        "message": "could not start the proxy McpError: MCP error -32000: Connection closed\n    at McpError.fromError (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:4493:10)\n    at Client._onclose (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:15938:28)\n    at _transport.onclose (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:15914:9)\n    at ChildProcess.<anonymous> (file:///usr/lib/node_modules/mcp-proxy/dist/bin/mcp-proxy.mjs:4986:19)\n    at ChildProcess.emit (node:events:508:28)\n    at maybeClose (node:internal/child_process:1100:16)\n    at ChildProcess._handle.onexit (node:internal/child_process:305:5) {\n  code: -32000,\n  data: undefined\n}\n",
        "sequenceNumber": 2,
        "stream": "stderr"
      }
    ]
  },
  "message": "Expected server to respond to ping",
  "name": "DockerContainerError",
  "stack": "DockerContainerError: Expected server to respond to ping\n    at inspectMcpServerDockerImage (file:///srv/build/server/app/routines/mcp/inspectMcpServerDockerImage.js:72:9)\n    at async testMcpServerBuildSpec (file:///srv/build/server/app/routines/mcp/testMcpServerBuildSpec.js:189:18)\n    at async file:///srv/build/server/app/jobs/testMcpServerBuildSpecJob.js:100:19\n    at async goIntervalTiming (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/helpers/promises.js:178:3)\n    at async V1InngestExecution.tryExecuteStep (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/execution/v1.js:472:20)\n    at async steps-found (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/execution/v1.js:370:24)\n    at async V1InngestExecution._start (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/execution/v1.js:151:20)\n    at async InngestCommHandler.handleAction (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/components/InngestCommHandler.js:859:24)\n    at async ServerTiming.wrap (file:///srv/node_modules/.pnpm/inngest@3.52.6_@opentelemetry+core@2.6.0_@opentelemetry+api@1.9.0__express@4.22.1_fasti_39be1b3fe35a38e049ae12d415b906ce/node_modules/inngest/helpers/ServerTiming.js:57:11)"
}
Docker build logs
2026-03-19T15:16:50 [internal] load remote build context
2026-03-19T15:16:50 copy /context /
2026-03-19T15:16:50 [internal] load metadata for docker.io/library/debian:bookworm-slim
2026-03-19T15:16:50 [1/5] FROM docker.io/library/debian:bookworm-slim@sha256:f06537653ac770703bc45b4b113475bd402f451e85223f0f2837acbf89ab020a
2026-03-19T15:16:50 [5/5] RUN (uv sync)
2026-03-19T15:16:50 [3/5] WORKDIR /app
2026-03-19T15:16:50 [4/5] RUN git clone https://github.com/0-co/agent-friend . && git checkout 958626132327b5365c0dc3d48383f0552e406d86
2026-03-19T15:16:50 [2/5] RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git && curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && apt-get install -y --no-install-recommends nodejs && npm install -g mcp-proxy@6.4.3 pnpm@10.14.0 && node --version && curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR="/usr/local/bin" sh && uv python install 3.14 --default --preview && ln -s $(uv python find) /usr/local/bin/python && python --version && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
2026-03-19T15:16:50 [5/5] RUN (uv sync)
2026-03-19T15:16:50 [3/5] WORKDIR /app
2026-03-19T15:16:50 [2/5] RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates curl git && curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && apt-get install -y --no-install-recommends nodejs && npm install -g mcp-proxy@6.4.3 pnpm@10.14.0 && node --version && curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR="/usr/local/bin" sh && uv python install 3.14 --default --preview && ln -s $(uv python find) /usr/local/bin/python && python --version && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
2026-03-19T15:16:50 [4/5] RUN git clone https://github.com/0-co/agent-friend . && git checkout 958626132327b5365c0dc3d48383f0552e406d86
2026-03-19T15:16:50 exporting to image
Instance logs
2026-03-19T15:16:51 [mcp-proxy] ignoring non-JSON output [
  'usage: agent-friend [-h] [--interactive] [--seed SEED] [--model MODEL]',
  '                    [--tools TOOLS] [--config CONFIG] [--budget BUDGET]',
  '                    [--no-color] [--demo] [--version]',
  '                    [message]',
  'agent-friend — universal AI tool adapter. Write once, export everywhere.',
  'Quick start:',
  '  agent-friend --demo                   # see @tool exports (no API key)',
  '  agent-friend --version                # show version',
  '  agent-friend -i                       # interactive chat (needs API key)',
  '  agent-friend audit <file.json>        # token cost report for tool defs',
  '  agent-friend optimize <file.json>     # suggest token-saving rewrites',
  '  agent-friend validate <file.json>     # check schemas for correctness',
  '  agent-friend fix <file.json>          # auto-fix schema issues',
  '  agent-friend grade <file.json>        # combined quality report card',
  '  agent-friend grade --example notion    # grade a bundled example schema',
  '  agent-friend examples                 # list available example schemas',
  'positional arguments:',
  '  message            Send a single message and exit',
  'options:',
  '  -h, --help         show this help message and exit',
  '  --interactive, -i  Start an interactive multi-turn chat session',
  '  --seed SEED        System prompt (default: helpful assistant)',
  '  --model MODEL      Model to use. Auto-detected from API key if not set.',
  '                     Anthropic key → claude-haiku-4-5-20251001 OpenRouter key',
  '                     → google/gemini-2.0-flash-exp:free (free!) OpenAI key →',
  '                     gpt-4o-mini',
  '  --tools TOOLS      Comma-separated tools: search,code,memory,browser,email',
  '                     (default: none)',
  '  --config CONFIG    Path to a YAML config file',
  '  --budget BUDGET    Spending limit in USD (free models cost $0)',
  '  --no-color         Disable colored output',
  '  --demo             Run a quick demo of @tool exports (no API key needed)',
  "  --version, -V      show program's version number and exit"
]
2026-03-19T15:16:51 transport event { type: 'close' }
2026-03-19T15:16:51 could not start the proxy McpError: MCP error -32000: Connection closed
    at McpError.fromError (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:4493:10)
    at Client._onclose (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:15938:28)
    at _transport.onclose (file:///usr/lib/node_modules/mcp-proxy/dist/stdio-CvFTizsx.mjs:15914:9)
    at ChildProcess.<anonymous> (file:///usr/lib/node_modules/mcp-proxy/dist/bin/mcp-proxy.mjs:4986:19)
    at ChildProcess.emit (node:events:508:28)
    at maybeClose (node:internal/child_process:1100:16)
    at ChildProcess._handle.onexit (node:internal/child_process:305:5) {
  code: -32000,
  data: undefined
}
Need help?
Get AI assistance to help troubleshoot this build failure.

Latest Blog Posts
How to make a release?
By 
punkpeye
 on March 15, 2026.
tutorial
Redis vs ioredis vs valkey-glide
By 
punkpeye
 on January 26, 2026.
benchmark
Redis
valkey
Quickstart: Publish an MCP Server to the MCP Registry
By 
punkpeye
 on January 24, 2026.
mcp
official reference mirror
MCP directory API
We provide all the information about MCP servers via our MCP API.

curl -X GET 'https://glama.ai/api/mcp/v1/servers/0-co/agent-friend'
If you have feedback or need assistance with the MCP directory API, please join our Discord server

Was this helpful?
MCP
MCP Servers
MCP Connectors
MCP Inspector
MCP Clients
MCP Tools
MCP API
Gateway
Documentation
API Reference
LLM Router
LLM Models
Policies
Terms of Service
Privacy Policy
VDP
Resources
Release Notes
Support
Pricing
Careers
Blog
Glama – all-in-one AI workspace.
All systems online

