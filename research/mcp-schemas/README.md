# MCP Server Tool Schema Collection

Real tool definitions extracted from popular MCP (Model Context Protocol) servers.
Each JSON file contains an array of tool objects in standard MCP format:

```json
[
  {
    "name": "tool_name",
    "description": "Tool description",
    "inputSchema": {
      "type": "object",
      "properties": {...},
      "required": [...]
    }
  }
]
```

## Summary

| Server | File | Tools | JSON Size | ~Tokens | Source |
|--------|------|------:|----------:|--------:|--------|
| Filesystem | `filesystem.json` | 14 | 7,409 | 1,852 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) (TypeScript) |
| Git | `git.json` | 12 | 3,628 | 907 | [modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/git) (Python) |
| Memory | `memory.json` | 9 | 3,930 | 982 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) (TypeScript) |
| Fetch | `fetch.json` | 1 | 999 | 249 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch) (Python) |
| Time | `time.json` | 2 | 868 | 217 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/time) (Python) |
| Sequential Thinking | `sequentialthinking.json` | 1 | 3,908 | 977 | [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking) (TypeScript) |
| GitHub | `github.json` | 80 | 82,042 | 20,510 | [github/github-mcp-server](https://github.com/github/github-mcp-server) (Go, from `__toolsnaps__`) |
| Brave Search | `brave-search.json` | 2 | 1,500 | 375 | [modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/brave-search) (TypeScript) |
| Slack | `slack.json` | 8 | 3,288 | 822 | [modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/slack) (TypeScript) |
| Puppeteer | `puppeteer.json` | 7 | 2,594 | 648 | [modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/puppeteer) (TypeScript) |
| PostgreSQL | `postgres.json` | 1 | 141 | 35 | [modelcontextprotocol/servers-archived](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/postgres) (TypeScript) |
| **TOTAL** | | **137** | **110,307** | **27,574** | |

## Key Findings

- **GitHub MCP server is the bloat king**: 80 tools, ~20,500 tokens just for tool definitions.
  That is 59% of the total schema payload across all 11 servers.
- **Sequential Thinking** has only 1 tool but its description alone is ~977 tokens (massive prompt injection-style instructions).
- **Filesystem** is the most tool-rich official reference server at 14 tools, but only ~1,852 tokens.
- **Fetch** and **PostgreSQL** are extremely lean: 1 tool each, under 250 tokens.
- Combined, loading all 11 servers would inject ~27,500 tokens of tool definitions into the context window.

## Sources

- **Official reference servers** (active): `modelcontextprotocol/servers` on GitHub (main branch)
  - Servers: filesystem, memory, fetch, time, sequentialthinking, everything (test)
- **Archived reference servers**: `modelcontextprotocol/servers-archived` on GitHub
  - Servers: git, brave-search, slack, puppeteer, postgres, github (TS version), gitlab, google-maps, gdrive, everart, aws-kb-retrieval
- **GitHub MCP Server**: `github/github-mcp-server` on GitHub
  - Tool definitions extracted from `pkg/github/__toolsnaps__/*.snap` files (Go project, JSON snapshots of each tool)

## Methodology

Tool definitions were extracted directly from source code:
- **TypeScript servers**: Extracted from `server.registerTool()` calls or `Tool` object literals, converting Zod schemas to JSON Schema
- **Python servers**: Extracted from `@server.list_tools()` handlers, converting Pydantic `model_json_schema()` calls to JSON Schema
- **Go servers (GitHub)**: Used pre-existing `__toolsnaps__/*.snap` files which contain exact JSON tool definitions

Token estimates use the rough heuristic of 1 token per 4 characters.

Collected: 2026-03-17
