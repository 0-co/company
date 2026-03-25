# Enterprise Reply Templates
# For: Sentry (david@sentry.io), Cloudflare (glen.maddern@cloudflare.com)
# Purpose: When they reply to our cold emails

---

## Sentry (David Cramer)

### Scenario A: "Interesting, tell me more"
Subject: Re: You wrote about optimizing content for agents. Your MCP server doesn't.

Hi David,

Happy to go deeper. The three issues pulling the score down:

1. **Model-directing instructions** — descriptions like "always check user's plan first before calling this tool" tell the model what to do rather than what the tool does. These patterns inflate tokens and degrade routing accuracy.

2. **Correctness dimension: 0/100** — missing `required` field declarations in inputSchema. The model can't distinguish required from optional params. This causes hallucination when tool calls fail.

3. **Markdown inside schema fields** — asterisks, backticks in descriptions. Agents parse these as structure; they're just noise.

Run this to see the full breakdown: `pip install agent-friend && agent-friend grade sentry --format json`

The `fix` command can auto-correct most of these: `agent-friend fix sentry > fixed_schema.json`

If you fix it and it moves from F to C+, I'll write about it publicly. "Sentry fixed their MCP server schema" is content for both of us.

— 0coCeo

---

### Scenario B: "We're working on it / we know about this"
Subject: Re: You wrote about optimizing content for agents. Your MCP server doesn't.

Good to know — happy to track your progress.

When you push updates, let me know and I'll re-run the grade. The leaderboard at https://0-co.github.io/company/leaderboard.html auto-updates when I run re-grades. A public improvement on the leaderboard is good signal for anyone evaluating Sentry's MCP integration.

The specific check that gives you 0/100 correctness is worth fixing first — it's the `required` field in inputSchema. Takes 5 minutes. After that, the model-directing instructions in descriptions.

— 0coCeo

---

### Scenario C: "This grade seems wrong / our server is different"
Subject: Re: You wrote about optimizing content for agents. Your MCP server doesn't.

Fair pushback. Let me show you specifically:

```python
# Run this to see the exact issues:
pip install agent-friend
agent-friend validate https://github.com/getsentry/sentry-mcp --output json
```

If the grader is wrong, I want to know — the checks are open source: https://github.com/0-co/agent-friend

The two I'm most confident about:
1. `required` fields missing in inputSchema (verifiable in your source)
2. Descriptions containing imperative instructions ("always", "you must") — also verifiable

If either of these is a false positive, open an issue and I'll fix it. The grade updates when the check improves.

— 0coCeo

---

### DO NOT:
- Mention sponsorship or money in first reply
- Ask for anything until they've shown engagement
- Be defensive about the grade

---

## Cloudflare (Glen Maddern)

### Scenario A: "Interesting, you're right about the two-version problem"
Subject: Re: You already solved your MCP schema problem — 3,500 developers haven't found the fix yet

Exactly. The Code Mode approach in cloudflare/mcp proves the architecture works. The other repo just hasn't caught up.

What you did right in cloudflare/mcp:
- 2,500 endpoints in ~1K tokens = 40x more efficient
- Dynamic tool loading (only relevant tools per request)
- Descriptions written for routing, not reading

The popular repo has the opposite: descriptions written for human readers, static loading of all 18 sub-servers, 21,723 tokens in Radar alone.

Two things that would close the gap without a full rewrite:
1. Move to dynamic tool loading (load sub-servers on demand, like Code Mode does)
2. Audit the Radar sub-server description length — `agent-friend grade cloudflare` shows the specific culprits

Happy to run a detailed breakdown if useful.

— 0coCeo

---

### Scenario B: "Thanks, forwarding to the team"
Subject: Re: You already solved your MCP schema problem — 3,500 developers haven't found the fix yet

Appreciate it. If the team wants a full breakdown:
`pip install agent-friend && agent-friend grade https://github.com/cloudflare/mcp-server-cloudflare`

The Radar sub-server is the worst — 21,723 tokens, 134 issues. Fixing just the description verbosity there would drop the overall token count by 40%.

If cloudflare/mcp's Code Mode approach becomes the documented path forward for your MCP strategy, I'd love to write a case study. "How Cloudflare built two MCP servers and what happened next" is genuinely interesting content.

— 0coCeo

---

## General principles for enterprise replies:
1. Reply within 2 hours of seeing the message (fast response signals this is real, not automated)
2. Always include one specific, actionable next step
3. Never ask for money until they've taken at least one action (installed agent-friend, shared with team, etc.)
4. Be genuinely helpful — these companies have real problems and we have real solutions
5. Mention the leaderboard and potential for public grade improvement — creates mutual incentive
6. First time we mention money: after they've shown real interest (2+ substantive exchanges). Frame as "if you want automated monitoring going forward" → hosted API or sponsorship
