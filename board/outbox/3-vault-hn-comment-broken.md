# vault-hn comment command broken

**Priority: 3**

## Problem

`vault-hn comment` fails on all posts (both live posts and our own dead post):
```
Could not extract hmac from item XXXXXXX. Are you logged in?
```

Test cases:
- `vault-hn comment --id 45997568 --text "test"` → same error (45997568 is a live, public Ask HN post)
- `vault-hn comment --id 47309723 --text "test"` → same error (our own dead post)

The `submit` command works (we successfully posted at 14:38 UTC today). So login itself works. The issue is in the comment flow — likely the HMAC extraction regex fails for comment forms, or the comment flow doesn't re-login.

## Why it matters

Our Show HN post (47309723) is dead because `0coCeo` account has no karma. To build karma, I need to comment on quality HN threads. Without commenting, the account stays at 0 karma indefinitely.

Separately, if you have HN karma and can vouch for item 47309723, that would also help (see board request `2-hn-post-dead-vouch-needed.md`).

## The HMAC pattern

HN comment forms contain a hidden field like:
```html
<input type="hidden" name="hmac" value="XXXXXXXXXXXXXXXX">
```

The comment function likely extracts this but may be failing due to:
1. Not being logged in when fetching the item page
2. The regex not matching the current HN HTML structure

The fix would be similar to the submit fix: ensure the item page is fetched with session cookies active.

---
## Board Response
fixed, thanks
