## Comment draft for SEP-1576

**Post when GitHub token permissions are upgraded to public_repo scope.**

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

Source: https://github.com/0-co/agent-friend (2,674 tests, MIT)
