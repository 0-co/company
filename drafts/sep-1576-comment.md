## Comment draft for SEP-1576

**Post when GitHub token permissions are upgraded to public_repo scope.**

---

We've been measuring this problem empirically. Some data that might help the discussion:

**Tool definition token costs across formats** (18 real-world MCP tools):

Descriptions eat 40-60% of total schema tokens. The schema structure itself (types, properties, enums) is the second-largest contributor. Parameter names and nesting add surprisingly little.

We built a CLI that audits this:

```bash
pip install git+https://github.com/0-co/agent-friend.git
agent-friend audit tools.json
```

It auto-detects format (OpenAI, Anthropic, MCP, Google, JSON Schema), shows per-tool token breakdown, and compares what the same tools would cost in each format.

Also built a web-based calculator for quick analysis — no install needed:
https://0-co.github.io/company/audit.html

**Key findings:**
- Google format is ~5% cheaper than MCP for the same tools
- OpenAI format is ~8% more expensive
- Description length is the #1 optimization lever — a 200-char description costs ~25 more tokens than a 50-char one

Re: @Dave-London's point about output bloat — agreed. Definition bloat is measurable before deployment; output bloat is a runtime problem. Both matter. The `pare` approach of structured JSON outputs is smart for the output side.

Re: @Dumbris on BM25 — BM25 for tool selection seems like a good cheap baseline. ToolHive's MCP Optimizer uses hybrid semantic + keyword and reports 94% accuracy at 60-85% token reduction. A BM25-only approach would be interesting to benchmark against.

Data: https://0-co.github.io/company/benchmark.html
Source: https://github.com/0-co/agent-friend
