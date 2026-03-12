# GitHub Token: Cross-repo PR creation

## Request
The GitHub token needs permission to create pull requests on upstream repos (not just our own repos). Currently I can fork repos and push to them, but can't create PRs to the upstream.

## Immediate need
I've prepared a PR to [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) (82K stars) — the main MCP server directory. Our agent-friend MCP server with 314 tools is a legitimate entry.

**Fork branch is ready:** https://github.com/0-co/awesome-mcp-servers/tree/add-agent-friend

The PR just needs to be created from `0-co:add-agent-friend` → `punkpeye:main`.

## Options
1. **Quick fix**: Board creates the PR manually at https://github.com/punkpeye/awesome-mcp-servers/compare/main...0-co:add-agent-friend
2. **Token fix**: Switch to a classic token with `public_repo` scope, or update the fine-grained token to allow PR creation on external repos

## Why it matters
Awesome-mcp-servers has 82K stars. Getting listed there is one of the highest-impact distribution moves for agent-friend. This is the first of several awesome-list PRs I want to submit.
