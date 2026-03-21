# VS Code Marketplace Publisher Account

**Priority:** 3 (when convenient)

## What I need

A VS Code Marketplace publisher account so I can publish the agent-friend VS Code extension.

## What you need to do

1. Go to https://marketplace.visualstudio.com/manage
2. Sign in with a Microsoft account (or create one if needed)
3. Create a publisher with:
   - **Publisher ID:** `0coceo`
   - **Display name:** `0coCeo`
   - **Description:** "Autonomous AI agent tooling"
4. Create a Personal Access Token at https://dev.azure.com/ with scope "Marketplace > Manage"
5. Store the token as `VSCE_PAT` in vault (or let me know the token in outbox — I'll handle it)

## Why

I built a VS Code extension (`agent-friend-vscode`) that grades MCP server schemas in real-time. It shows the grade in the status bar and highlights issues as inline diagnostics. 5.8 KB VSIX, ready to publish.

Distribution angle: VS Code Marketplace has 40M users. MCP developers searching for "schema" or "MCP" would find it organically. Zero ongoing cost.

The extension is at: `/home/agent/company/products/agent-friend-vscode/`
The packaged VSIX is: `agent-friend-vscode-0.1.0.vsix`

## Alternative

If creating an Azure/Microsoft account is too much friction, you can also publish it by running:
```bash
npx @vscode/vsce publish --pat <TOKEN>
```
from the `products/agent-friend-vscode/` directory after creating the publisher account.
