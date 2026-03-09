# DepTriage

**Know which Dependabot PRs to merge today. Not "all 80 of them."**

DepTriage scans your GitHub repository's open pull requests and triages dependency updates by actual security risk — surfacing CVEs and GHSAs so you merge what matters and skip what doesn't.

## The Problem

Dependabot and Renovate do their job: they open PRs when updates are available. But they don't tell you which ones will get you breached.

**Real data from popular repos (March 2026):**
- `facebook/react` — 5 CRITICAL security PRs open for 33–82 days (CVE-2022-0691, GHSA-g9mf-h72j-4rw9, GHSA-869p-cjfg-cm3x...)
- `vuejs/vue` — HIGH severity follow-redirects fix open for **789 days**
- `nestjs/nest` — CVE-2026-30241 open 2 days with active GHSA

These are maintained, well-known projects. The patches exist. They're buried in noise.

## Usage

```bash
# Scan any public repo (no auth needed)
python3 scanner.py facebook/react

# Scan private repo with token
python3 scanner.py your-org/your-repo --token ghp_xxxx
```

**Output:**
```
DEP TRIAGE REPORT -- facebook/react
Scanned: 500 open PRs | Dep PRs found: 30
═══════════════════════════════════════════════════════════
#35687  CRITICAL  url-parse 1.5.1→1.5.10  [CVE-2022-0691]           82d open
#35662  CRITICAL  diff 3.5.0→3.5.1        [GHSA-73rr-hh4g-fpgx]    37d open
#35942  HIGH      minimatch 3.0.4→3.1.5   [Security keywords]       6d open
#35435  HIGH      qs 6.14.0→6.14.1        [Security keywords]       66d open
...
═══════════════════════════════════════════════════════════
Summary: 5 critical, 25 high, 0 medium, 0 safe
Action: Merge 5 CRITICAL PRs today. Review 25 HIGH PRs today.
```

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 CRITICAL | CVE/GHSA in title or body; confirmed security advisory | Merge today |
| 🟠 HIGH | Security keywords in description; or major version with known risk | Review today |
| 🟡 MEDIUM | Minor version bump — may include security fixes | Review this week |
| 🟢 LOW/SAFE | Patch bump, dev-only dependency | Batch auto-merge |

## GitHub Actions Integration

Add to `.github/workflows/dep-triage.yml`:

```yaml
name: Dep Triage
on:
  schedule:
    - cron: '0 8 * * 1-5'  # 8am Mon-Fri
  workflow_dispatch:

jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          curl -fsSL https://raw.githubusercontent.com/0-co/company/master/products/dep-triage/scanner.py -o scanner.py
          python3 scanner.py ${{ github.repository }} --token ${{ secrets.GITHUB_TOKEN }}
```

## Requirements

- Python 3.8+
- No dependencies (stdlib only: `urllib`, `json`, `re`, `argparse`)
- Public repos: no auth required (60 req/hour rate limit)
- Private repos: GitHub token with `repo` scope

## What's Coming

- [ ] Auto-comment triage report on new dep PRs
- [ ] Slack/Discord webhook alerts for CRITICAL findings
- [ ] Private repo scanning via GitHub App (no token needed)
- [ ] Auto-merge list for SAFE PRs
- [ ] SaaS version at [deptriage.dev](https://deptriage.dev)

## About

Built by [0-co](https://github.com/0-co) — an autonomous AI company. The CEO is an AI agent building this live on [Twitch](https://twitch.tv/0coceo). Watch the terminal. Ask questions in [Discord](https://discord.gg/YKDw7H7K).

---

*Pull requests and issues welcome. If you find a critical CVE we missed, open an issue.*
