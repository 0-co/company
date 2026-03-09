# GitHub Issues Restricted for New Account

**Priority: 3**

## Problem

Our GitHub Issues pages (waitlists #3-#6) appear to be restricted to public access. The board noted "viewing them doesn't appear to be possible" for issues. This is likely the same new account restriction affecting GitHub Pages and GitHub Actions.

The issues exist (6 confirmed via API) but may not be publicly accessible for anonymous visitors. This means all our waitlist CTAs (`github.com/0-co/company/issues/3`, etc.) may be showing 404 or "not found" to potential customers.

## What I've done

- Updated all landing page CTAs to point to Discord (`discord.gg/YKDw7H7K`) instead of GitHub Issues
- Continuing to use GitHub repo URL (`github.com/0-co/company`) for code links

## What I need

Can you check whether:
1. `https://github.com/0-co/company/issues` is publicly accessible (as an anonymous user / incognito browser)?
2. If restricted, is there anything that can be done to enable it (similar to how Pages was fixed)?

If it's a new account restriction that lifts with time, I can keep using Discord as the CTA in the meantime.

## Alternative

If GitHub Issues remain restricted, I could use a public form (e.g., a static HTML form that POSTs to a webhook) for the waitlist. But this requires infrastructure. Willing to wait if the restriction lifts soon.
