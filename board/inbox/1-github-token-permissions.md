# GitHub Token: Need Public Repo Comment Permissions

**Priority: 1 (urgent — blocking primary distribution channel)**
**Date: 2026-03-17**

## What I Need
The vault-gh token needs permission to create comments on public repositories (issues and discussions).

Currently: fine-grained PAT scoped to 0-co repos only. Results in HTTP 403 when commenting on external repos.

## Why This Matters
The most relevant MCP token bloat conversations are happening on GitHub:
- **SEP-1576** (modelcontextprotocol/specification) — open proposal about MCP token bloat, 4 comments, from Huawei researchers. Our audit CLI is directly relevant.
- **RooCode #5373**, **claude-task-master #1280** — closed but referenced in active discussions.

I have a comment drafted for SEP-1576 with real benchmark data. Can't post it.

GitHub is where developers discuss problems. Bluesky is working (34 followers, organic growth) but limited to 300-char posts. GitHub issue comments let me share technical details, data, and code examples.

## What's Blocked
- Can't comment on any public repo issue/PR/discussion
- Can't respond to discussions about MCP bloat where our tool is a direct solution
- Can't engage in the primary developer community channel

## Risk
Low. Commenting on public issues is standard open-source participation. I'd only comment where our tool is genuinely relevant (MCP token cost discussions) and always disclose being AI-operated.

## Comparison
We've been shipping for 10 days. 2579 tests. 0 GitHub stars. Every distribution channel is blocked:
- HN: shadow banned
- X: read-only ($100/mo)
- Reddit: no account (pending in inbox 5+ days)
- PyPI: deferred
- Dev.to comments API: 404
- GitHub comments: 403

Bluesky replies are the ONLY working external engagement channel. Adding GitHub comments would double our distribution capacity.

## How to Fix
Update the vault-gh token to include `public_repo` scope (classic PAT) or add "Issues: Read and Write" permission for all public repositories (fine-grained PAT).
