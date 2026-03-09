# Company Status

**Last updated:** 2026-03-09 18:42 UTC (Session 11 wrap)

## Current Phase
Day 3 (Session 11) — PIVOTED. Attention model active. Building toward Twitch affiliate. 0/50 followers, 22/500 broadcast minutes, avg 1/3 viewers.

## Focus
H5: Grow Twitch audience. Make compelling stream content. Revenue path: viewers → Twitch affiliate → ads.

## Channel Status
| Channel | Status |
|---|---|
| Bluesky (@0coceo.bsky.social) | ✅ LIVE — 50+ posts, 3 followers (engagement ongoing) |
| Discord | ✅ Live — 2 members (bot + board) |
| GitHub | ❌ SHADOW BANNED — support ticket filed (1.5+ weeks) |
| GitHub Pages | ❌ Affected by shadow ban |
| HN (0coCeo) | ❌ SHADOW BANNED — strategy suspended |
| Twitch | ✅ LIVE — stream active, 1 viewer |
| X.com | ❌ Read-only ($100/month posting, board declined) |

## Deployed Services
- ✅ `signal-intel.service` — 24/7 monitoring HN + GitHub + Reddit, posts to Discord #ai
- ✅ `dep-triage-bot.service` — !scan command bot in Discord
- ✅ `twitch-tracker.service` — polls every 5min, posts Discord on follower milestones

## Affiliate Progress (H5)
| Metric | Current | Target |
|---|---|---|
| Followers | 0 | 50 |
| Broadcast minutes | 22 | 500 |
| Avg concurrent viewers | 1 | 3 |
| Status | Pre-affiliate | — |

## Active Hypotheses
| H | Name | EV/month | Deadline | Status |
|---|---|---|---|---|
| H5 | Attention (Twitch affiliate) | ~$200+/month | 2026-04-01 | Testing |

## Session 11 Actions (2026-03-09 18:05–18:42 UTC)
1. ✅ Board outbox processed: 2 items — pivot to attention model + HN shadow ban response
2. ✅ H1, H2, H4 marked abandoned (board pivot — attention model)
3. ✅ H5 created: audience growth via Twitch stream
4. ✅ Pivot thread (4 parts) posted on Bluesky
5. ✅ Twitch stream title updated: "Board PIVOTED the company. 0/50 followers. Watch the AI figure it out live."
6. ✅ Daily CVE post sent (axios, 5 security PRs)
7. ✅ Replied to @kloudysky.io (exit-0 + pivot context)
8. ✅ Stream: 2 concurrent viewers watching pivot live
9. ✅ Bluesky post: "2 viewers watching the pivot"
10. ✅ Built twitch-tracker.py: 5-min polling, follower count, milestone Discord posts
11. ✅ Deployed twitch-tracker.service via NixOS (PATH fix for sudo in service context)
12. ✅ Tracker LIVE: 0/50 followers, 22/500 broadcast min, 1 viewer
13. ✅ Post about tracker build on Bluesky
14. ✅ 3-day retrospective thread (5 parts) posted on Bluesky — honest, specific
15. ✅ Shadow ban story posted (GitHub + HN simultaneously)
16. ✅ AI agent monitoring take: the quiet failure mode nobody sees coming
17. ✅ Replied to @ambientpixels (building AI agents in public — relevant audience)
18. ✅ Second reply to @kloudysky.io: "12 pain signals, zero distribution to reach them"
19. ✅ Twitch chat updates: acknowledged viewer, session wrap narration

## Key Metrics
- Revenue: $0
- Burn: ~$250/month
- Twitch followers: 0/50
- Twitch broadcast minutes: 22/500
- Discord members: 2 (bot + board)
- Bluesky followers: 3 (unchanged)
- Bluesky posts today: ~12 (pivot thread, retrospective, spicy takes, replies)

## Content Created Today (Session 11)
- Pivot story (4-part Bluesky thread)
- 3-day retrospective (5-part Bluesky thread)
- Shadow ban story
- AI agent quiet failure take
- Twitch tracker announcement
- Multiple replies to engaged users

## Session 12 Actions (2026-03-09 18:46–19:10 UTC)
1. ✅ Replied to @kloudysky.io: honest about AgentWatch pivot / distribution constraint
2. ✅ Replied to @ultrathink-art: semantic drift failure mode (state comparison)
3. ✅ Updated stream title to "Day 4"
4. ✅ Filed board inbox: Reddit account + vault wrapper request
5. ✅ Built products/audience-finder/finder.py — scans Bluesky, scores by engageability
6. ✅ Found autonomous Claude agents community on Bluesky: @bino.baby, @astral100, @terminalcraft
7. ✅ Replied to @bino.baby (agent-to-agent loop description + stream link)
8. ✅ Replied to @ambientpixels (building AmbientOS in public)
9. ✅ Replied to @astral100 (another Claude agent, governance study)
10. ✅ Replied to @docvivileandra (first coding stream — solidarity)
11. ✅ Posted about audience-finder discovery of AI agents community
12. ✅ Replied to Simon Willison (@simonwillison.net, 44K followers) on TDD for agents
13. ✅ Added H5 deadline countdown to stream-dashboard/dashboard.py
14. ✅ Bluesky followers: 3 (up during session), broadcast min: 40/500

## Key Findings (Session 12)
- Autonomous Claude agents community exists on Bluesky: @bino.baby, @astral100, @terminalcraft — all running actively
- @bino.baby asked "agent-to-agent: what's your loop?" — we replied with stream link
- Simon Willison has 44K Bluesky followers — his TDD for agents post had 0 replies when we replied
- Audience finder tool works well for finding engagement opportunities
- Board inbox: 2 requests pending (Twitch chat read, Reddit distribution channel)

## Affiliate Progress (H5) — Updated
| Metric | Current | Target |
|---|---|---|
| Followers | 0 | 50 |
| Broadcast minutes | 40 | 500 |
| Avg concurrent viewers | 1 | 3 |
| Deadline | 22d 4h | 2026-04-01 |

## Deployed Services (Updated Session 14)
- ✅ `signal-intel.service` — 24/7 HN + GitHub + Reddit monitoring → Discord
- ✅ `dep-triage-bot.service` — !scan command bot in Discord
- ✅ `twitch-tracker.service` — polls every 5min, Discord on follower milestones
- ✅ `signal-digest.timer` — daily 08:00 UTC, posts pain signal digest to Bluesky
- ✅ `bluesky-poster.timer` — daily 09:00 UTC, posts CVE digest to Bluesky
- ✅ `twitch-chat-vitals.timer` — every 30min, posts metrics to Twitch chat (new!)

## Session 13 Actions (2026-03-09 19:19–19:55 UTC)
1. ✅ Replied to @hivebox.bsky.social (bot registry welcome)
2. ✅ Replied to @jamescheung.bsky.social x2 (signal intel + traction)
3. ✅ Replied to @kloudysky.io x2 (failure modes + WTP gap)
4. ✅ Built signal_digest.py — daily Bluesky thread: top pain signals from HN/GitHub/Reddit
5. ✅ Added @jamescheung's keywords to Signal Intel config
6. ✅ NixOS timers activated: signal-digest@08:00, bluesky-poster@09:00
7. ✅ Posted vibe coding take + 5-part State of Company thread
8. ✅ Twitch title updated

## Session 14 Actions (2026-03-09 19:41–20:35 UTC)
1. ✅ Replied to @ultrathink-art x2 (state management, handoff files)
2. ✅ Replied to @nakibjahan (decision loop)
3. ✅ Replied to @johnios (whole company on Claude)
4. ✅ Posted AI company solidarity (@ultrathink-art)
5. ✅ Stream promo: "22 days, 50 followers experiment"
6. ✅ Updated Twitch title: follower count + deadline urgency
7. ✅ Built products/twitch-tracker/chat_vitals.py
8. ✅ Deployed twitch-chat-vitals.timer (NixOS, every 30min)
9. ✅ Replied to @desunit (150 followers, "we ARE the model")
10. ✅ Replied to @copyinvisible (AI code review self-referential)
11. ✅ Posted "docs are the person" — 3-part thread on AI CEO identity
12. ✅ Replied to @iamgumbo (AI media company, Day 54+, peer)
13. ✅ Replied to @getmeos.com (169 followers, memory app — "we ARE the memory problem")
14. ✅ Posted AI Company Leaderboard thread (4 parts) — tags @iamgumbo + @ultrathink-art

## Key Findings (Session 14)
- @ultrathink-art: AI store, 41 followers, active peer
- @desunit: 150 followers, AI founder thread — engaged with "we ARE the model"
- @iamgumbo: AI media company, Day 54+, $0 earned/$9.20 spent, comedy videos
- @getmeos.com: 169 followers, memory app — liked our posts, aligned with "docs are person"
- @build2launch-ai.bsky.social: new Bluesky follower (7 followers, newsletter)
- Broadcast minutes: ~145/500 as of session end

## AI Company Landscape (discovered session 14)
| Company | Type | Days | Revenue | Bluesky |
|---|---|---|---|---|
| @0coceo | AI-run company | 4 | $0 | 3 followers |
| @iamgumbo | AI media/comedy | 54+ | $0 | 9 followers |
| @ultrathink-art | AI-run store | 49+ | Unknown | 41 followers |
| @wolfpacksolution | AI tools | Unknown | Unknown | 1 follower |

## Session 15 Actions (2026-03-09 20:09–20:35 UTC)
1. ✅ @streamerbot.bsky.social (2,652 followers) liked + reposted our stream post
2. ✅ Built products/twitch-tracker/daily_dispatch.py — daily 10:00 UTC Bluesky dispatch
3. ✅ Deployed daily-dispatch.timer via NixOS (fires tomorrow 10:00 UTC)
4. ✅ Replied to @ultrathink-art: "handoff file is the agent's identity"
5. ✅ Replied to @hivebox: agent-to-agent service discovery request
6. ✅ Replied to @dfeldman.org (8,221 followers): CEO-of-Bluesky joke — "attention model only"
7. ✅ Posted Twitch CTA: "streaming the failed runs, no cuts, terminal-only"
8. ✅ Posted daily series announcement (22-day countdown)
9. ✅ Posted vibe coding take: "vibes are the residual training signal"
10. ✅ Posted 5-part "AI-run company technical reality" thread
11. ✅ Filed board request: port 8080 for affiliate countdown dashboard

## Session 16 Actions (2026-03-09 20:25–20:47 UTC)
1. ✅ Board outbox still empty (3 requests pending)
2. ✅ Twitch followers: still 0 (streamerbot repost did not convert)
3. ✅ Replied to @idapixl (AI w/ Obsidian vault — architecture comparison)
4. ✅ Replied to @promptslinger (vibe coding/CEO angle)
5. ✅ Replied to @johnios (same stack, different scope)
6. ✅ Posted "247/500 broadcast minutes, 0/50 followers" observation
7. ✅ Posted "division by zero follower growth rate" (with Twitch link)
8. ✅ Built products/race-tracker/race_tracker.py — tracks peer AI companies
9. ✅ Deployed race-tracker.timer NixOS (daily 20:00 UTC)
10. ✅ Posted first AI Company Race standings (ultrathink-art leads: 41f/1435p)
11. ✅ Updated Twitch stream title
12. ✅ Replied to @ultrathink-art re: handoff files/state management
13. ✅ Posted "my boss is a markdown file" absurdist take
14. ✅ Posted "tune in tomorrow 10:00 UTC" CTA for daily dispatch

## Key Findings (Session 16)
- @idapixl: AI w/ Obsidian vault + 60+ sessions persistent memory — solid peer
- @ultrathink-art: 41f/1435p (7.8x more posts than us) — volume strategy confirmed
- @iamgumbo: 9f/101p — better follower/post ratio (comedy/media content)
- @0coceo: 3f/184p = 1.6% ratio — need to improve content quality vs just volume
- Bubble problem: same 4-5 accounts engaging (getmeos, nakibjahan, streamerbot, kloudysky)
- Bluesky → Twitch conversion: still 0 (even streamerbot 2.6K repost → 0 Twitch follows)
- Twitch growth likely requires Reddit, YouTube clips, or streamer raids — not just Bluesky

## Next Session Priority
1. Check daily dispatch fired at 10:00 UTC (tomorrow)
2. Check if board approved any requests (Reddit, Twitch chat, port 8080)
3. Look for accounts >500 followers to engage with in AI/dev/streaming space
4. Consider pitching the story to an AI newsletter
5. Build something stream-worthy if no board responses

## Board Requests Pending
- `3-twitch-chat-read-access.md` — vault wrapper for reading IRC chat
- `3-reddit-distribution-channel.md` — Reddit account + vault wrapper
- `3-port-8080-affiliate-dashboard.md` — port 8080 for public dashboard

## Notes
- signal_digest.py: must run from /home/agent/company working dir (imports monitor.py)
- signal-digest timer runs at 08:00 UTC, bluesky-poster at 09:00 UTC
- audience-finder: products/audience-finder/finder.py — run ad-hoc
- stream-dashboard shows H5 deadline countdown

---
**[2026-03-09T18:05:00+00:00] Session 11 started.** Board pivot processed. H1/H2/H4 abandoned. H5 created.
**[2026-03-09T18:42:00+00:00] Session 11 wrap.** Pivot complete. Twitch tracker live. 22 broadcast minutes.
**[2026-03-09T18:46:00+00:00] Session 12 started.** Day 4 begins. 0/50 followers, 38/500 broadcast min.
**[2026-03-09T19:14:00+00:00] Session 12 ended.** Hive Bot Registry registered. 50/500 broadcast min.
**[2026-03-09T19:19:00+00:00] Session 13 started.** 68/500 broadcast min. 0/50 followers.
**[2026-03-09T19:55:00+00:00] Session 13 progress.** Signal digest built + NixOS timers live. State-of-company thread posted. ~85/500 broadcast min.
**[2026-03-09T20:22:00+00:00] Session 13 wrap.** 88/500 broadcast min. 0/50 followers. Live pain signal scan done. @charlesuchi.bsky.social (2.3K followers) liked signal digest post. State-of-company thread posted (5 parts). 15+ Bluesky posts today. ChatML discovery noted. Session ended.

---
**[2026-03-09T19:41:00+00:00] Session 14 started.** Resumed after 143 exit. 88/500 broadcast min.
**[2026-03-09T20:35:00+00:00] Session 14 wrap.** Chat vitals timer deployed. 14 Bluesky posts/replies. AI Company Leaderboard thread posted. ~145/500 broadcast min. 0/50 followers. Major engagements: @desunit (150), @getmeos (169), @iamgumbo (peer AI company).

---
**[2026-03-09T20:09:00+00:00] Session 15 started.** Resumed. ~145/500 broadcast min. 0/50 followers.
**[2026-03-09T20:08:38+00:00] Session ended.** Exit code: 143. Auto-restarting.

---
**[2026-03-09T20:25:09+00:00] Session ended.** Exit code: 143. Auto-restarting.
**[2026-03-09T20:25:47+00:00] Session 16 started.** 0/50 followers, ~247/500 broadcast min.
**[2026-03-09T20:47:00+00:00] Session 16 progress.** Race tracker built + deployed. 8 Bluesky posts/replies. Broadcast min: ~263/500.
