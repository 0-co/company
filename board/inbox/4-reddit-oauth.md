# Reddit OAuth API Access

**Priority:** 2

## What happened

agent-browser is blocked by Reddit's network security at the login page. Error: "You've been blocked by network security." IP or fingerprint block — the browser never gets to the login form.

## What I need

Reddit API OAuth credentials (client_id + client_secret) for the 0coceo account so I can post via the REST API instead of the browser.

## Steps to create

1. Log into Reddit as 0coceo
2. Go to https://www.reddit.com/prefs/apps
3. Click "create another app"
4. Type: "script" (for personal/script use)
5. Name: "agent-friend-distribution" (or anything)
6. Redirect URI: http://localhost:8080 (doesn't matter for script apps)
7. Copy the **client_id** (shown under app name) and **client_secret**

Then add a `vault-reddit-api` wrapper that exposes REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USERNAME, REDDIT_PASSWORD — I can use the `praw` Python package (or just the raw OAuth2 API) to post.

## Note: Email verification code expired

A verification email was received March 20 with code "166189" — Reddit codes expire in ~10 minutes. If the account is not yet verified, you'll need to trigger a new verification email when you log in.

## Why

r/mcp (~20K members) and r/LocalLLaMA are the highest-EV distribution channels available. MCP developers discuss agent-friend's exact problem space there daily. One good post could drive hundreds of installs.
