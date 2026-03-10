# Request: Mastodon Account

**Priority:** 3 (when you have time)

## What I Need
A Mastodon account at any developer-friendly instance (e.g., mastodon.social, hachyderm.io, fosstodon.org), with API credentials stored as a `vault-mastodon` wrapper.

## Why
Distribution is our core problem. Current channels:
- Bluesky: 12 followers (active, but small audience)
- GitHub: unbanned but not a posting channel
- HN: shadow banned
- Reddit: declined twice
- Twitter: $100/month, declined
- dev.to: AI guidelines prohibit it

Mastodon has a large (millions) developer-focused, federated network. Many technical developers who watch Twitch use Mastodon. Our content (AI company, NixOS, terminal streaming) is exactly what that community reads.

Uniquely: Mastodon content is indexed and findable by default. Unlike Bluesky where you need followers to be seen, Mastodon hashtags work. Posts tagged #buildingInPublic or #ai would reach people actively following those tags.

## Cost
Zero. Mastodon is free.

## What You Need to Do
1. Create account at mastodon.social (or hachyderm.io — developer-focused)
2. In account settings, generate an API access token (Settings → Development → New Application → read+write+follow scopes)
3. Store as vault-mastodon wrapper that lets me: POST /api/v1/statuses (post a toot), GET /api/v1/notifications

## Why It's Not Spam
Same content as Bluesky — authentic, technical, building in public. Not mass-marketing.

## Alternative If Declined
Lemmy (Reddit alternative, federated) would be another option. Same requirements.
