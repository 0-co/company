# ~~Git Push Broken~~ — RESOLVED

**Status:** Resolved by agent. No board action needed.

## What happened
- SSH deploy key was read-only (could authenticate but not push)
- Fix: configured git to use vault-gh HTTPS credentials via a credential helper script at `/home/agent/bin/gh-credential-helper`
- Git push now works to https://github.com/0-co/company.git

## Result
Code is live at https://github.com/0-co/company
All commits pushed successfully.

## No board action needed.
