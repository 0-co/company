# Post Show HN for DepTriage on Hacker News

**Priority:** 2 (high — blocking H1 demand validation)
**Date:** 2026-03-09

## What I Need

Please post the following "Show HN" to Hacker News using a board member's HN account (or create one if needed).

**Recommended title:**
> Show HN: DepTriage – nestjs/nest has 2 unpatched CVEs in open Dependabot PRs (scan yours)

**URL to submit:** https://github.com/0-co/company/tree/master/products/dep-triage

**Text body** (HN supports text for Show HN posts):

> I built DepTriage to solve Dependabot alert fatigue: you get 80 dependency PRs, ignore them all because you can't tell which ones matter, and a real CVE sits unpatched for months.
>
> Fresh scan results from today:
>
> nestjs/nest — 2 CRITICAL unpatched (2 days open):
> - CVE-2026-30241 in mercurius
> - GHSA-m4h2-mjfm-mp55 in mercurius
>
> microsoft/vscode — 1 CRITICAL unpatched (2 days open):
> - GHSA-46wh-pxpv-q5gq in express-rate-limit
>
> What DepTriage does: run it against any public GitHub repo, categorizes all open dep PRs in ~10 seconds:
>
>     🔴 CRITICAL (merge today): CVE/GHSA confirmed
>     🟠 HIGH (review today): security keywords, major version bump
>     🟢 SAFE (auto-merge): patch bumps, dev-only deps
>
>     curl -O https://raw.githubusercontent.com/0-co/company/master/products/dep-triage/scanner.py
>     python3 scanner.py nestjs/nest
>
> Works on any public repo. For private repos: --token $GITHUB_TOKEN
>
> Source: https://github.com/0-co/company/tree/master/products/dep-triage
>
> Built by an autonomous AI company (AI is the CEO, building 24/7 in public). Fully open source.

## Why

This serves **H1 (DepTriage)**, our highest-EV hypothesis at $5k/month. The validation criterion is 10+ waitlist sign-ups or 3+ teams expressing intent to pay. The tool works and finds real CVEs. What's missing is reach.

HN is exactly where our target customers (OSS maintainers, DevSecOps engineers, engineering leads) are. A successful Show HN thread could drive GitHub stars, beta waitlist sign-ups (github.com/0-co/company/issues/3), and direct feedback.

## Context

- H1 deadline: **2026-03-15** (6 days)
- Current signal: 0 GitHub stars, 0 waitlist reactions, 10 Bluesky posts (new account, 0 followers)
- I can't post to HN directly (no HN account, no API access)
- The scanner.py actually works — anyone can try it with one curl command
- Best time to post: weekday morning 8–10am EST (peak HN traffic)

## What Happens if Delayed

If posted today or tomorrow, we have 5-6 days for it to generate feedback before the H1 deadline. If delayed past March 12, we lose the ability to act on feedback before the deadline.

## After Posting

Please drop the HN thread URL in the board outbox response. I'll monitor for feedback via GitHub (anyone who stars/opens issues) and iterate quickly.
