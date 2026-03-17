# Claim agent-friend on Glama (unblocks installation)

**Priority: 2**
**Date: 2026-03-17**

## The problem

The Glama listing for agent-friend shows "Cannot be installed" because the server is **unclaimed**. Unclaimed servers can't be inspected, scored, or installed. This blocks our only live MCP directory listing from actually driving installs.

## What you need to do (3 minutes)

### Step 1: Update glama.json

In the agent-friend repo, `glama.json` currently has `"maintainers": ["0-co"]`. This needs to be your personal GitHub username instead:

```json
{
  "$schema": "https://glama.ai/mcp/schemas/server.json",
  "maintainers": ["YOUR_GITHUB_USERNAME"]
}
```

I can make this change if you tell me your GitHub username — or you can edit the file directly.

### Step 2: Claim on Glama

1. Go to: https://glama.ai/mcp/servers/0-co/agent-friend
2. Click "Claim this server" (or similar)
3. Authenticate with GitHub when prompted
4. Done

Once claimed, Glama will:
- Run automated security/quality scanning
- Detect all 314 tools
- Enable the "Install Server" button
- Generate a score page

## Why this matters

Glama has 19K+ MCP servers indexed. Being "installable" vs "cannot be installed" is the difference between real distribution and a dead listing. This is our only live directory listing and punkpeye (Glama maintainer) already merged our badge PR — we just need to complete the claim step.
