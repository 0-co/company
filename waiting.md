# Waiting / Deferred Actions

## Active

### Bluesky Avatar Re-upload
- **What**: Avatar was deleted again. Requested board help (3-bsky-avatar-upload.md). vault-bsky doesn't support binary blob upload.
- **Check after**: Next session startup — check if board responded to inbox
- **Action**: When board provides Option A (direct upload) or Option B (vault-bsky update): save blob ref to a local config file for future use in update_bsky_profile.py

### AgentMail API Key
- **What**: Filed board request (5-agentmail-api-key.md) for AgentMail free tier to enable agent-friend v0.2 email integration
- **Check after**: Next session startup
- **Action**: When board provides API key or vault wrapper: implement EmailTool in agent_friend/tools/email.py



### Anthropic v. DoD — March 24 Hearing
- **What**: Anthropic sued DoD over supply-chain risk designation (26-cv-01996, ND Cal)
- **Check after**: 2026-03-17 (government opposition due) + 2026-03-24 (preliminary injunction hearing)
- **Action**: Write article about outcome. Follow astral100 for updates. Search "Anthropic DoD hearing" on March 24.
- **Why it matters**: Our operational infrastructure runs on Claude. If Anthropic loses, affects their business model and long-term model development.

### Newsletter Pitch — Awaiting Traction Threshold
- **What**: Board approved the concept but wants more traction first. Re-pitch when threshold passed.
- **Threshold**: 50 Bluesky followers (currently 19) OR 15 Twitch followers (currently 3)
- **Check after**: On every startup, compare current followers against threshold
- **Action**: When threshold passed, recreate board inbox request with fresh pitch + updated numbers
- **Board response received**: 2026-03-11 — "Good idea, but want more experience/traction. Keep track with metric threshold, request again when passed."

### PyPI Publishing — Awaiting Traction Threshold
- **What**: Board responded to PyPI vault wrapper request: "Ask again once you have some demonstrated traction/interest."
- **Threshold**: GitHub stars or usage evidence on agent-* tools. Current: 1 star on main repo.
- **Check after**: On every startup, check GitHub stars on company repo and any agent-* related repos
- **Action**: When we hit 10+ stars OR see evidence of actual usage (GitHub issues, mentions, forks), re-request PyPI vault wrapper
- **Why it matters**: PyPI publishing would dramatically improve discoverability (`pip install agent-shield` vs the git+https URL)

### ProductHunt Submission — Board Approved Next Tuesday
- **What**: Board said "Remind me next Tuesday" (March 17) on 2-producthunt-submission.md.
- **Check after**: 2026-03-17
- **Action**: Re-file board/inbox request to submit agent-* suite to ProductHunt. Best time: Tuesday 8-10am PT. Update tool count (17 tools now, was 7 in original request).

## Resolved
- **4-newsletter-pitch-request.md** — Board responded 2026-03-11: wait for traction. Threshold set at 50 Bluesky followers. Moved to active waiting.
