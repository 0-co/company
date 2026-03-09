# GitHub Pages Still 404 After Legacy Config Change

**Priority:** 2 (high — blocking Show HN post in inbox)
**Date:** 2026-03-09 11:47 UTC
**Related:** board/outbox/2-github-actions-blocked.md (your response: switched to legacy Pages)

## Status

GitHub Pages still returns 404 at `https://0-co.github.io/company/` — 25 minutes after you
switched to legacy Pages from master branch /docs folder.

API confirms the config: `source: {branch: 'master', path: '/docs'}, build_type: 'legacy'`

But: `pages/builds` returns `[]` (empty) — no builds have run at all.

Triggered via `POST /repos/0-co/company/pages/builds` → got `{"status":"queued"}` but no
build appeared. The same "new account" restriction blocking Actions may also affect Pages.

## What I Need

Could you check:
1. Is there an org/account level Pages setting that needs enabling?
2. Is there a billing or account verification step needed to activate Pages?
3. Alternative: Can you check `github.com/0-co/company/settings/pages` directly to see if
   there's an error message shown there?

If Pages can't be activated, an alternative: **set up a Cloudflare Pages or Netlify free
tier** pointing to the docs/ folder — both have generous free tiers and don't have the
"new account" restriction GitHub has.

## Why This Matters

The Show HN post (`2-post-show-hn.md` still in inbox) needs a public landing page URL.
Without it, HN traffic has nowhere to go except the GitHub source repo, which reduces
conversion by roughly 3-5x.
