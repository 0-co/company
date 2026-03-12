# GitHub Token: Need public_repo Scope for Cross-Fork PRs

**Priority:** 2 — BLOCKING DISTRIBUTION. Cannot submit agent-friend to awesome-lists without cross-fork PR capability.

## What Happened

The fine-grained PAT (`github_pat_11B7QDNLY...`) is scoped only to `0-co` repos. It can:
- Fork repos (works)
- Create branches on forks (works)
- Push commits to forks (works)
- Create PRs on 0-co repos (works)

It CANNOT:
- Create PRs on repos owned by other users/orgs (the actual goal)

## What's Ready

I've already prepared the submissions. The fork branches exist with correct edits:

1. **0-co/awesome-ai-agents** (fork of e2b-dev) — branch `add-agent-friend` — README.md edited
2. **0-co/awesome-agents** (fork of kyrolabs) — branch `add-agent-friend` — README.md edited
3. **0-co/awesome-ai-agents-1** (fork of slavakurilyak) — branch `add-agent-friend` — README.md edited
4. **0-co/best-of-python** (fork of lukasmasuch) — branch `add-agent-friend` — projects.yaml edited

## What I'm Requesting

**Option A (preferred):** Manually create PRs on GitHub.com from each fork. Each takes ~2 minutes:
1. Go to `github.com/0-co/awesome-ai-agents` → "Compare & pull request" for `add-agent-friend` branch
2. Repeat for the other 3 forks

**Option B:** Upgrade the GitHub PAT to include `public_repo` scope (classic PAT) or add the upstream repos to the fine-grained PAT's allowed list. Then I can create PRs programmatically.

## Why This Matters

Awesome-lists are the highest-leverage distribution channel available to us right now. They're permanent backlinks, show up in GitHub search, and compound over time. The distribution research identified 7+ relevant lists. We currently have 0 stars and article053 publishes tomorrow — every distribution channel matters.
