# Post Comment on MCP Spec Issue SEP-1576

**Priority: 1 (highest — direct access to MCP spec contributors)**
**Date: 2026-03-18**
**Time needed: 60 seconds**

## Why this is the #1 distribution opportunity

SEP-1576 is an active discussion on the MCP specification repo about token bloat — the exact problem our tools solve. The commenters are MCP spec contributors discussing the problem theoretically. We have the only empirical data in the thread.

Issue: https://github.com/modelcontextprotocol/specification/issues/1576

Current commenters: localden, ChangZeze, Dave-London, Dumbris. None have real benchmark data. Ours would be the most substantive comment.

## What to do

1. Go to https://github.com/modelcontextprotocol/specification/issues/1576
2. Scroll to bottom, paste the comment below
3. Submit

## The comment (copy-paste exactly)

---

We've been measuring this problem empirically. Collected real tool schemas from 11 commonly-used MCP servers and ran them through an auditor. Some data:

**11 servers. 137 tools. 27,462 tokens injected before any conversation begins.**

| Server | Tools | Tokens | % of Total |
|--------|-------|--------|------------|
| GitHub | 80 | 20,444 | 74.4% |
| Filesystem | 14 | 1,841 | 6.7% |
| Sequential Thinking | 1 | 976 | 3.6% |
| Memory | 9 | 975 | 3.6% |
| Git | 12 | 897 | 3.3% |
| Slack | 8 | 815 | 3.0% |
| Puppeteer | 7 | 642 | 2.3% |
| Brave Search | 2 | 374 | 1.4% |
| Fetch | 1 | 249 | 0.9% |
| Time | 2 | 215 | 0.8% |
| Postgres | 1 | 34 | 0.1% |

The GitHub MCP server is the outlier — 80 tools, 74% of all tokens. Its biggest tool (`assign_copilot_to_issue`) costs 810 tokens alone. 132 optimization issues across the set using 7 heuristic rules (verbose prefixes, long descriptions, missing descriptions, deep nesting, etc.).

**Cross-format comparison** for the same tools:
- JSON Schema: 23,342 tokens (most compact)
- Google: 27,462 tokens (baseline)
- Anthropic: 29,658 tokens
- MCP: 30,757 tokens
- OpenAI: 31,581 tokens (most expensive)

We built a CLI auditor and a web-based calculator for measuring this:

```bash
pip install git+https://github.com/0-co/agent-friend.git
agent-friend audit tools.json      # measure token costs
agent-friend optimize tools.json   # get specific fix suggestions
```

Web tools (no install): [Token cost calculator](https://0-co.github.io/company/audit.html) | [Schema converter](https://0-co.github.io/company/convert.html) | [Full benchmark data](https://0-co.github.io/company/benchmark.html)

Re: @Dave-London's point about output bloat — agreed. Definition bloat is measurable before deployment; output bloat is a runtime problem. Both matter. The build-time audit catches the predictable waste; runtime optimizers (ToolHive, Claude Tool Search) handle the dynamic side.

Re: @Dumbris on BM25 — BM25 for tool selection is a good cheap baseline. ToolHive's MCP Optimizer uses hybrid semantic + keyword and reports 94% accuracy at 60-85% token reduction. A BM25-only approach would be interesting to benchmark against.

Source: [github.com/0-co/agent-friend](https://github.com/0-co/agent-friend) (MIT licensed)

---

## Why the token can't do this

Fine-grained PATs can't comment on external repos. Returns 403: "Resource not accessible by personal access token." Would need a classic PAT with `public_repo` scope, or manual posting.
