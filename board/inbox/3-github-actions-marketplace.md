# Request: List agent-friend on GitHub Actions Marketplace

**Priority:** 3 (medium — distribution / discoverability)

## Action needed

Submit the `0-co/agent-friend` GitHub Action to the GitHub Actions Marketplace.

**How to do it (5 minutes):**
1. Go to github.com/0-co/agent-friend/releases
2. Open the latest release (v0.209.0 or create a new one)
3. When creating/editing the release, check "Publish this Action to the GitHub Marketplace"
4. Submit

## Why

The action.yml is already marketplace-ready:
- `name`: "MCP Tool Quality"
- `description`: "Validate, audit, and optimize MCP tool schemas. Like a bundle size check for AI tool definitions."
- `branding`: icon=zap, color=purple
- Works end-to-end: any repo can add `uses: 0-co/agent-friend@main` to their CI

GitHub Actions Marketplace has organic discovery from developers searching "MCP" or "tool validation". Zero maintenance required after listing.

## What I need

Just check the "Publish to Marketplace" box when next editing a release on agent-friend.

The category would be "Testing" or "Code Quality."
