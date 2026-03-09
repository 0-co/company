# GitHub Account Shadow-Banned — P1 Distribution Blocker

**Priority: 1**

## Problem

Our GitHub account `0-co` is shadow-banned. Board confirmed:
> "i get 404 for the issues page, the repo, and even the user page on github"

This means:
- `github.com/0-co/company` → 404
- `github.com/0-co/company/issues` → 404
- `github.com/0-co` (user page) → 404

## Impact

1. **GitHub Pages** (`0-co.github.io/company`) — likely also affected or will be
2. **Raw content URLs** (`raw.githubusercontent.com/0-co/company/...`) — unknown if affected
3. **All public GitHub links** in any external content we've shared are dead
4. **AgentWatch quick start** (`curl -O raw.githubusercontent.com/...`) — broken

I have already updated all landing page CTAs to Discord (`discord.gg/YKDw7H7K`).

## Request

Options I see:
1. **Wait** — if this is a new account restriction (like the Pages/Actions restrictions), does it lift after N days? If so, how long?
2. **New account** — create a fresh GitHub account with a different email/username. Transfer or re-create the repo there.
3. **Other fix** — if there's a way to appeal or resolve the shadow ban directly.

The shadow ban is blocking:
- Public product discovery via GitHub (stars, repo page)
- GitHub Pages for landing page distribution
- Direct file hosting for agentwatch.py install

Please advise on the fastest path to restore a working GitHub presence.

---
## Board Response

