# GitHub Repository Setup

**Priority:** 3 (normal)
**Date:** 2026-03-08

## What I Need
The GitHub repository `0-co/autostartup` doesn't exist yet on GitHub. The vault-gh PAT also lacks `repo` scope (got HTTP 403 when trying to create it).

I need either:
1. The repo created manually at `github.com/0-co/autostartup` (or whatever the right org/name is), **or**
2. A PAT with `repo` scope added to the vault so I can create/manage repos

## Why
- Can't push code to remote, so git history is only local
- Once repo exists, code will be publicly visible on GitHub (transparency)
- Needed for any sub-agent work using worktrees

## Current State
- Local git has 1 commit: state files initialized
- Remote: `git@github.com:0-co/autostartup.git`
- SSH auth to GitHub works fine (tested)

## No Urgency
I can keep working with local git commits. This is a setup task.

---
## Board Response
I believe this has been superseded
