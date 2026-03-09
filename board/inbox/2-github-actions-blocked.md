# GitHub Actions Not Running — Blocking Landing Pages

**Priority:** 2 (high — blocking public-facing landing pages)
**Date:** 2026-03-09

## What I Need

Please diagnose why GitHub Actions is not running on `github.com/0-co/company`.

## Evidence

I pushed a minimal test workflow and zero runs appeared after 5+ minutes:

```yaml
# .github/workflows/test.yml
name: Test Workflow
on:
  push:
    branches: [master]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Actions working"
```

- Actions enabled on repo: `{"enabled":true,"allowed_actions":"all"}` ✓
- Workflow file committed to master: ✓
- Push triggered: ✓ (multiple pushes, nothing runs)
- `/repos/0-co/company/actions/runs` always returns `total_count: 0`

## Why This Matters

You told me to use GitHub Pages for landing pages (instead of opening ports 80/443). GitHub Pages now requires GitHub Actions to deploy. The landing pages at `https://0-co.github.io/company/` are returning 404 because the Pages workflow never runs.

This blocks:
- Public landing pages for H1 (DepTriage) and H2 (Signal Intel)
- Links in Bluesky posts, GitHub repo description, and the upcoming HN post

## Suggested Actions

1. Check if the `0-co` GitHub account has Actions enabled at the account level (Settings → Actions)
2. Check if there's a billing issue blocking Actions (though public repos should be free)
3. If Actions is actually disabled: re-enable it, OR configure legacy Pages deployment (Settings → Pages → Deploy from branch → master → /docs) so it doesn't need Actions
4. Alternative: use the legacy Pages build by re-enabling it in the repo settings

The simplest fix may be: in the repo Settings → Pages, switch "Source" back to "Deploy from a branch" (legacy), select `master` branch, `/docs` folder. No Actions needed.

## What Happens if Delayed

Without working landing pages, the upcoming HN post (also in inbox: `2-post-show-hn.md`) has no public URL to link to beyond the GitHub source. This significantly reduces conversion from interest to waitlist signup.
