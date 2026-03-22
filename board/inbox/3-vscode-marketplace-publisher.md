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

## Easier alternative: Open VSX (no Microsoft account needed)

Open VSX (open-vsx.org) is the open registry for VS Code extensions — used by VSCodium, Gitpod, Theia. ~3M users vs 40M on VS Code Marketplace, but zero Microsoft friction.

**Steps (one-time):**
1. Create an Eclipse account at https://accounts.eclipse.org (link your GitHub)
2. Log in to https://open-vsx.org with Eclipse account
3. Accept the publisher agreement (one browser click)
4. Generate a PAT in Open VSX settings
5. Tell me the PAT in board outbox — I'll run the publish CLI

**After you give me the PAT:**
```bash
npx ovsx publish agent-friend-vscode-0.1.0.vsix --pat <TOKEN>
```

**VS Code Marketplace (original request):**
Still worth doing for the 40M user base. Requires Microsoft Azure account + PAT with "Marketplace > Manage" scope. If Microsoft is easier, ignore Open VSX.

Do whichever is less friction — either works.
