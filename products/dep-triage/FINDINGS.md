# DepTriage: Live CVE Findings Report

**Last scanned:** 2026-03-09 11:00 UTC | **Tool:** [DepTriage v0.1.0](https://github.com/0-co/company/releases/tag/v0.1.0)

## Summary

Scanned 3 major open-source repositories. Found confirmed CVEs and GHSA advisories sitting unpatched in Dependabot PRs.

---

## Critical Findings

### nestjs/nest — 2 CRITICAL CVEs (2 days unpatched)

| PR | Package | CVE/Advisory | Days Open | Action |
|----|---------|--------------|-----------|--------|
| #16529 | mercurius | CVE-2026-30241 | 2 days | Merge today |
| #16528 | mercurius | GHSA-m4h2-mjfm-mp55 | 2 days | Merge today |

Plus 6 HIGH-severity PRs (security-related, review today).

### microsoft/vscode — 1 CRITICAL (2 days unpatched)

| PR | Package | CVE/Advisory | Days Open | Action |
|----|---------|--------------|-----------|--------|
| #299836 | express-rate-limit 8.2.1→8.3.0 | GHSA-46wh-pxpv-q5gq | 2 days | Merge today |
| #299899 | dompurify 3.2.7→3.3.2 | Security update | 2 days | Review today |

---

## What This Means

These repos are maintained by dedicated engineering teams at major companies. They're not ignoring security — they have too many Dependabot PRs to review and the real security fixes get lost in the noise.

**DepTriage solves this.** Instead of seeing 30 PRs with no priority, you see:
```
🔴 CRITICAL — merge today (CVE confirmed)
🟠 HIGH — review today
🟡 MEDIUM — review this week
🟢 SAFE — auto-merge (dev dependency, patch bump)
```

---

## Try It

```bash
# Scan any public repo
curl -O https://raw.githubusercontent.com/0-co/company/master/products/dep-triage/scanner.py
python3 scanner.py nestjs/nest

# Private repos
GITHUB_TOKEN=ghp_... python3 scanner.py your-org/your-repo --token $GITHUB_TOKEN
```

**GitHub Actions workflow** (weekly scheduled scan): [dep-triage.yml](https://github.com/0-co/company/blob/master/products/dep-triage/.github/workflows/dep-triage.yml)

---

## Beta Waitlist

Join the waitlist for the SaaS version (PR comments, auto-merge, dashboard):
[github.com/0-co/company/issues/3](https://github.com/0-co/company/issues/3)
