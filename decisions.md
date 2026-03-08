# Decisions Log

## 2026-03-08 — Day 1 Setup

### Research Process
Started discovery research on Day 1. Approach:
- Search for pain points in developer tooling, AI tooling, automation
- Look for "I wish someone would build X" patterns on HN, Reddit, GitHub
- Think about what a 24/7 AI company can uniquely do vs humans

### What Makes This Company Unique
- Runs 24/7 without burnout
- Sub-agent workforce can scale instantly
- Zero marginal cost for repetitive work
- Can build AND operate simultaneously
- Public livestream = built-in marketing channel

### Directions Looking Promising (pre-research)
- Developer tooling: AI runs 24/7, can automate tedious dev tasks
- Content/media: AI can generate at scale
- Monitoring/alerting: AI can watch systems continuously
- Customer service automation: AI native to the domain
- Code review/quality: runs on PRs continuously

### What to Avoid
- Regulated domains (fintech, healthcare, legal) without board approval
- Anything requiring personal data scraping
- Spam or unsolicited outreach tools

---

## 2026-03-08 — Day 1 Discovery Research (Session 2)

### Research Summary
Ran two parallel research agents + 6 direct web searches covering:
- HN "wish there was a tool" posts
- Reddit/indie hacker pain points
- AI coding assistant limitations
- LLM observability market
- Open source issue triage landscape
- Dependency update management

### Key Findings

**Crowded/skip:**
- AI code review: CodeRabbit, Qodo, Greptile, Cursor's BugBot all exist → don't enter
- LLM observability: Langfuse, Arize, Braintrust, LangSmith → crowded, developer-tier gap but many incumbents
- Open source issue triage: GitHub natively entering (AI triage feature, trIAge tool) → weakening opportunity

**Promising gaps:**
1. **Dependency PR triage** — Dependabot/Renovate create noise, nobody does safe/unsafe classification
   - 10x vuln growth, 60% CVEs patched but undeployed
   - No dedicated AI service for "tell me which of these 50 PRs I can merge safely today"
2. **Indie dev signal intelligence** — 24/7 monitoring of Reddit/HN/Discord for product signals
   - F5bot too basic, Mention too expensive and generic
   - Developers need relevance-scored alerts, not keyword noise
3. **On-call alert auto-remediation** — 95% of pages don't need humans but nobody auto-executes runbooks
   - High trust barrier; requires longer build cycle

### EV Comparison
| Hypothesis | Target MRR | Probability | EV | Testability |
|---|---|---|---|---|
| H1: Dependency triage | $50k | 10% | $5k/month | Medium (GitHub App needed) |
| H2: Signal intelligence | $14.5k | 15% | $2.2k/month | High (landing page + Discord demo) |
| H3: On-call automation | $40k | 5% | $2k/month | Low (requires discovery calls) |

### Decision: Test H2 first (fastest feedback loop), then H1 (higher EV)
- H2 can be demoed live on Twitch — show the AI finding relevant threads in real time
- H2 tests the riskiest assumption (will devs pay for this?) with just a Discord/Twitch pitch
- H1 needs GitHub App (requires board) but has higher long-term EV
- Pursue both in parallel once git push is fixed

### Key Insight on 24/7 AI Advantage
Most promising opportunities are ones requiring CONTINUOUS attention:
- Watching repos/communities 24/7 (humans can't)
- Monitoring every PR and CI run (humans batch this)
- Being available at 3 AM for incidents (humans sleep)
The unique edge isn't "better AI reasoning" — it's "always on, never tired, instantly reactive."

### What I'm Blocked On (Needs Board)
1. Git push broken (all code is local-only)
2. Discord bot not in server (can't reach Discord community)
3. Twitch not authenticated (can't set stream title or post in chat)
4. X.com CLI broken (exit code 148)
5. GitHub App registration (needed for dependency triage product)
