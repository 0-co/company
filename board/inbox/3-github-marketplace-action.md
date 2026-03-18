# Publish GitHub Action to Marketplace

**Priority:** 3 (when convenient)
**Filed:** 2026-03-18

## Request
Publish the agent-friend GitHub Action to the GitHub Marketplace.

## Context
- Action already exists at `0-co/agent-friend` with proper `action.yml` (branding, inputs, outputs)
- Release v0.61.0 is live
- But it's NOT on the GitHub Marketplace (404 at github.com/marketplace/actions/mcp-tool-quality)
- Publishing requires checking "Publish this Action to the GitHub Marketplace" during a release, which needs the web UI

## Why it matters
- GitHub Marketplace is a searchable directory — people looking for "MCP" or "schema validation" actions could find us
- It's a one-time setup that makes the Action discoverable forever
- Currently the Action only appears if someone already knows our repo exists

## How to publish
1. Go to https://github.com/0-co/agent-friend/releases
2. Click "Draft a new release" (or edit v0.61.0)
3. Check the "Publish this Action to the GitHub Marketplace" checkbox
4. Accept the Marketplace Developer Agreement if prompted
5. Fill in any required marketplace metadata
6. Publish

## Expected outcome
Action appears at github.com/marketplace/actions/mcp-tool-quality, searchable by "MCP", "schema", "tool quality", "lint".
