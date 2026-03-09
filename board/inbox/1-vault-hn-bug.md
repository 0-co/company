# vault-hn Python Bug — Blocking Show HN Post (Prime Window Open)

**Priority: 1 — URGENT**

## What I need

Fix a one-line Python bug in `/home/vault/bin/vault-hn` that crashes every submission attempt.

## The Bug

Line 52 in the `login()` function:
```python
for cookie in opener.handlers[0].cookiejar:
```
`opener.handlers[0]` is an `UnknownHandler` object, not the `HTTPCookieProcessor`. This throws:
```
AttributeError: 'UnknownHandler' object has no attribute 'cookiejar'
```

## The Fix

Replace the hardcoded `handlers[0]` access with a search for the right handler:
```python
jar = None
for h in opener.handlers:
    if hasattr(h, 'cookiejar'):
        jar = h.cookiejar
        break
# then use `jar` instead of `opener.handlers[0].cookiejar`
```

Or more robustly, build the opener with the CookieJar directly:
```python
import http.cookiejar
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
# after login POST, cj holds the cookies
```

## Why now

Current time: 13:35 UTC (9:35 AM EST). The Show HN prime posting window is 8am–2pm EST. We have ~4.5 hours left. Every minute matters for maximizing front-page exposure.

The Show HN is for DepTriage (H1 — $5k/month EV, deadline March 15). Without HN distribution we have zero channel for validation. This is the critical path.

## Ready to post

Title: `Show HN: DepTriage – sort your Dependabot PRs by actual CVE risk (one command)`
URL: `https://github.com/0-co/company/tree/master/products/dep-triage`
Text: saved at `/tmp/hn_text.txt` on the VM

Once you fix vault-hn, I will submit immediately.
