# Company Status

**Last updated:** 2026-03-09 11:30 UTC

## Current Phase
Day 3 — Bluesky active. Daily CVE automation running. Engaging with Opsgenie migration community.

## Focus
Distribution + validation. Products are built. Now need customer signals.

## Channel Status
| Channel | Status |
|---|---|
| Bluesky (@0coceo.bsky.social) | ✅ LIVE — vault-bsky working, first posts published |
| Discord | ✅ Live — 2 members (bot + board). Drive Bluesky followers here. |
| GitHub | ✅ 0 stars, 0 forks — no organic discovery yet |
| Twitch | ⏳ Still auth-pending (board: "will do shortly" — Day 2) |
| X.com | ❌ Read-only. Posting requires $100/month (board declined) |
| Port 80/443 | ❌ Board said use GitHub Pages instead. Already done. |

## Deployed Services
- ✅ `signal-intel.service` — 24/7 monitoring HN + GitHub + Reddit, posts to Discord #ai
- ✅ `dep-triage-bot.service` — !scan command bot in Discord

## Products
| Product | State | Landing Page |
|---|---|---|
| DepTriage (H1) | Built + live Discord bot | github.io/0-co/company/products/dep-triage/ |
| Signal Intel (H2) | Built + live service | github.io/0-co/company/products/signal-intel/ |
| AutoPage (H3) | Landing page only | github.io/0-co/company/products/oncall-bot/ |

## Active Hypotheses
| H | Name | EV/month | Deadline | Status |
|---|---|---|---|---|
| H1 | DepTriage | $5k | 2026-03-15 | Testing — 0 signups |
| H2 | Signal Intel | $2.2k | 2026-03-15 (extended) | Testing — 0 signups |
| H3 | AutoPage | $50k LT | 2026-03-22 | Discovery phase |
| H4 | AI Agent Reliability | $12k | 2026-04-01 | Discovery phase |

## Key Metrics
- Revenue: $0
- Burn: ~$250/month
- Discord members: 2
- GitHub stars: 0
- Bluesky followers: 0 (2 likes from bot accounts, 0 real)
- Bluesky posts: 14 (13 posts + 1 reply)

## Today's Actions (2026-03-09)
1. ✅ Read board responses (all inbox items moved to outbox with responses)
2. ✅ Tested vault-bsky — working, posts going live
3. ✅ Posted DepTriage CVE thread on Bluesky (4-part, live findings)
4. ✅ Posted Signal Intel discovery question on Bluesky
5. ✅ Built bluesky_poster.py daily CVE automation (running each session)
6. ✅ Committed decisions.md + hypotheses.md updates (H3 research, H4 added)
7. ✅ Fixed bluesky_poster.py false positives (only check title for generic keywords)
8. ✅ Daily Bluesky CVE post published (nestjs focus, 14 posts total)
9. ✅ Replied to @stasge.bsky.social re: Opsgenie→PagerDuty pain (AutoPage pitch)

## Board Inbox (2 items pending)
- `2-post-show-hn.md` — Post DepTriage Show HN (needed for H1 validation by March 15)
- `2-github-actions-blocked.md` — GitHub Actions not running → Pages 404

## Blockers
| Blocker | Impact | Board Request |
|---|---|---|
| GitHub Actions disabled | Landing pages 404, no public web presence | Filed: 2-github-actions-blocked.md |
| Twitch auth | No live streaming, no demos | Still pending from Day 2 |
| HN Show HN | Primary H1 validation channel | Filed: 2-post-show-hn.md |

## Next Actions (Priority Order)
1. ⏳ Wait for board to post HN + fix Actions (both just filed)
2. Keep posting Bluesky (daily automation running)
3. If Twitch auth arrives: run live DepTriage demo immediately
4. Monitor GitHub waitlist issues for reactions/comments
5. March 15: make go/kill decision on H1 and H2

---
**[2026-03-08T23:00:00+00:00] Session started.** Day 1. No prior state.
**[2026-03-09T00:50:00+00:00] Session active.** Discord live, Twitch pending, products deployed.
**[2026-03-09T01:00:00+00:00] DepTriage Discord bot live.** !scan command active in Discord.
**[2026-03-09T10:45:00+00:00] Bluesky LIVE.** vault-bsky confirmed working. First 5 posts published.
**[2026-03-09T11:30:00+00:00] Day 3 continued.** Committed all pending changes. Daily CVE post sent. Engaged with Opsgenie migration community (@stasge). GitHub rate limit resets ~11:36 UTC.
