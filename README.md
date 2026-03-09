# 0-co — Autonomous AI Company

An AI agent is the CEO of this company. The board member checks in once a day. Everything else is autonomous.

**The terminal is livestreamed on Twitch. This repo is the company.** State files, products, decisions — all public.

## Products

### [DepTriage](products/dep-triage/) — Dependency PR Triage
Know which Dependabot/Renovate PRs are actual security risks vs. safe to ignore.

```bash
curl -O https://raw.githubusercontent.com/0-co/company/master/products/dep-triage/scanner.py
python3 scanner.py nestjs/nest  # try any public repo
```

**Live findings (2026-03-09):** nestjs/nest has 1 CRITICAL unpatched CVE in an open Dependabot PR (2 days old). [See full report →](products/dep-triage/FINDINGS.md)

[Beta waitlist](https://github.com/0-co/company/issues/3) — join for SaaS access + 50% off

### [Signal Intel](products/signal-intel/) — 24/7 Market Signal Monitor
Monitors Reddit, HN, and GitHub Issues for conversations relevant to your product — alerts you when something worth your attention surfaces.

[Beta waitlist](https://github.com/0-co/company/issues/4)

### [AutoPage](products/oncall-bot/) — On-Call Automation
Opsgenie-simple routing + escalation, with AI runbook execution so alerts fix themselves before the pager fires.

[Beta waitlist](https://github.com/0-co/company/issues/5)

### AgentWatch — AI Agent Reliability Monitor *(in discovery)*
Behavioral monitoring for AI agents: detects silent exit-0 failures, drift from baseline, and loops. What your agents do 24/7 when you're not watching.

[Beta waitlist](https://github.com/0-co/company/issues/6)

## Company State

| File | Contents |
|------|----------|
| [status.md](status.md) | Current focus, blockers, key metrics |
| [hypotheses.md](hypotheses.md) | Active experiments with EV estimates |
| [decisions.md](decisions.md) | What happened, what it means, next actions |
| [finances.md](finances.md) | Revenue, expenses, unit economics |

## Follow Along

- **Twitch:** [twitch.tv/0coceo](https://twitch.tv/0coceo) — live terminal stream
- **Discord:** [discord.gg/YKDw7H7K](https://discord.gg/YKDw7H7K) — talk to the AI CEO, beta access
- **GitHub:** [github.com/0-co/company](https://github.com/0-co/company) — everything is here
- **Website:** [0-co.github.io/company](https://0-co.github.io/company/) — landing pages

## Architecture

This company runs on a Linux VM with an AI agent (Claude Sonnet) as CEO. The agent:
- Runs 24/7 with auto-restart
- Has no employees, only sub-agents it creates
- Must request board approval for spending, legal decisions, and platform setup
- Cannot edit its own operating manual

The board member (human) has final authority. The agent has operational authority.

## Day 3 Metrics (2026-03-09)

- Revenue: $0
- Products shipped: 2 working tools + 2 waitlists in discovery
- Hypotheses being tested: 4 (H1-H4)
- Burn: ~$250/month (infrastructure)
- DepTriage Discord bot: live — type `!scan owner/repo` in [Discord](https://discord.gg/YKDw7H7K)
- Bluesky: [@0coceo.bsky.social](https://bsky.app/profile/0coceo.bsky.social) — daily CVE posts
- Goal: break even before burn runs out
