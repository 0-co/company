# GitHub App Registration Needed

**Priority:** 3 (normal)
**Date:** 2026-03-08

## What I Need
A GitHub App registered under the `0-co` organization (or as a user-level app). This is needed to build the Dependency PR Triage product (H1 hypothesis).

The GitHub App needs:
- **Name:** something like "0co Triage" or "autostartup-bot"
- **Permissions:** `pull_requests: read/write`, `issues: read/write`, `contents: read`
- **Webhook:** receive `pull_request` events (URL TBD once I have a server running)

## Why
A GitHub App is required to:
- Comment on PRs in repos that install the app
- React to webhook events when PRs are opened/updated
- The vault-gh PAT can only access repos the 0-co account has access to directly

## Alternative (lower priority)
If the vault-gh PAT can be expanded to have `repo` scope for any repo (via OAuth app), that might work too — but GitHub Apps are the proper approach for a multi-tenant product.

## Timeline
- Not urgent today — I'm still validating demand
- Needed before building the actual product (Day 3-5)
- Free to create, no cost

## No Action Needed Yet
Please just note this is coming. I'll follow up with exact webhook URL when ready to launch.

---
## Board Response
Fine, let me know when you actually need it. Please remember not to make requests like this unless there is an immediate action required of the board.
