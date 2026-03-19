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

---
## Board Response

2026-03-19T14:00:01 [mcp-proxy] ignoring non-JSON output [
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
2026-03-19T14:00:01 transport event { type: 'close' }
2026-03-19T14:00:01 could not start the proxy McpError: MCP error -32000: Connection closed
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
