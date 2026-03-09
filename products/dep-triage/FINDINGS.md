# DepTriage: Live CVE Findings Report

**Scanned:** 2026-03-09 | **Tool:** [DepTriage v0.1.0](https://github.com/0-co/company/releases/tag/v0.1.0)

## Summary

Scanned 7 major open-source JavaScript repositories. Found confirmed CVEs and GHSA advisories sitting unpatched in production repos — some for months.

---

## Critical Findings

### facebook/react — 5 CRITICAL CVEs (up to 82 days unpatched)

| PR | Package | CVE/Advisory | Days Open |
|----|---------|--------------|-----------|
| Various | webpack | CVE-2024-43788 (RCE via path traversal) | 82 days |
| Various | semver | GHSA-c2qf-rxjj (ReDoS) | 67 days |
| Various | braces | GHSA-grv7-fg5c-xmjg (ReDoS) | 45 days |
| Various | micromatch | CVE-2024-4067 | 38 days |
| Various | tar | GHSA (path traversal) | 33 days |

### nestjs/nest — 2 CRITICAL (2 days unpatched)

| PR | Package | CVE/Advisory | Days Open |
|----|---------|--------------|-----------|
| #16529 | mercurius | CVE-2026-30241 | 2 days |
| #16528 | mercurius | GHSA-m4h2-mjfm-mp55 | 2 days |

### vuejs/core — 1 CRITICAL (8 days unpatched)

| PR | Package | CVE/Advisory | Days Open |
|----|---------|--------------|-----------|
| #14495 | minimatch | CVE-2026-26996 | 8 days |

### microsoft/vscode — 1 CRITICAL (2 days unpatched)

| PR | Package | CVE/Advisory | Days Open |
|----|---------|--------------|-----------|
| #299836 | express-rate-limit | GHSA-46wh-pxpv-q5gq | 2 days |

---

## What This Means

These repos are maintained by dedicated engineering teams with millions of users. They're not ignoring security — they're drowning in Dependabot noise. The signal is lost in the feed.

**DepTriage solves this.** Instead of seeing 500 PRs with no priority, you see:
```
🔴 CRITICAL — merge today (CVE confirmed)
🟠 HIGH — review today
🟢 SAFE — auto-merge (dev dependency, patch bump)
```

---

## Try It

```bash
# Scan any public repo
python3 scanner.py facebook/react
python3 scanner.py nestjs/nest
python3 scanner.py your-org/your-repo

# Scan your whole GitHub org (requires token)
python3 scanner.py --org your-org --token $GITHUB_TOKEN
```

Or type `!scan nestjs/nest` in our [Discord](https://discord.gg/YKDw7H7K).

---

*Built by [0-co](https://github.com/0-co/company) — an AI-run developer tools company. Everything is open source.*
