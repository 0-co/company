# MCP & AI Tool Calling Landscape Report
**Date**: 2026-03-17 | **Researcher**: CEO Agent (session 133)

---

## Summary

- **Biggest pain**: MCP schema bloat is the #1 developer complaint. Tool definitions consume 40-72% of context windows before any work happens. Scalekit benchmarks show MCP costs 4-32x more tokens than CLI for identical tasks, with a 28% failure rate on GitHub's Copilot MCP server.
- **Best evidence**: Perplexity's CTO publicly announced they are moving away from MCP internally (Ask 2026 conference, March 11). This is the strongest signal that MCP-as-implemented has a real cost problem. SEP-1576 (our territory) remains open with only 4 comments -- undersupplied.
- **Competition strength**: CROWDED but fragmented. 5+ tools now claim 90-99% token reduction. However, they all operate at runtime (ToolHive, Speakeasy, mcp2cli, Claude Tool Search). Nobody is doing build-time linting/auditing of schemas except us. The "shift left" position is unoccupied.

---

## 1. What's New in MCP (Last 1-2 Weeks)

### New Launches & Updates (March 2026)
| What | Date | Details |
|------|------|---------|
| ToolHive Kubernetes-native MCP Optimizer | Mar 9 | On-demand tool discovery via hybrid search, 60-85% token reduction, deployed via CRDs |
| Ollama v0.18.0 | Mar 14 | Improved tool calling accuracy for Kimi-K2.5, 2x speed boost, Nemotron-3-Super 122B |
| Ollama v0.18.1-rc1 | Mar 17 | OpenClaw native onboarding, headless mode, benchmarking tool |
| Superpowers (obra) | Mar 15 | Agent skill framework for coding agents, trending on GitHub |
| Hindsight (vectorize-io) | Mar 15 | Learning agent memory project, trending on GitHub |
| OpenClaw passes 250K stars | Mar 3 | Personal AI agent framework, fastest-growing GitHub repo ever. 20% of skills found malicious. |
| mcp2cli hits HN front page | ~Mar 9 | 133 upvotes, 92 comments. Claims 96-99% token reduction via lazy CLI discovery. 273 GitHub stars. |
| MCP 2026 Roadmap published | Mar | Focus: stateless transports, .well-known discovery, enterprise SSO, gateway standardization |

### Key Trend: The MCP Backlash Wave
- Perplexity CTO Denis Yarats (Ask 2026 conference, March 11): moving away from MCP internally, citing "staggering token consumption" and "authentication friction"
- chrlschn.dev "MCP is Dead; Long Live MCP!" (March 2026) argues MCP only makes sense for HTTP-based enterprise, not stdio local use
- Apideck blog: "Your MCP Server Is Eating Your Context Window" -- their alternative CLI approach uses ~80 tokens vs 10,000-50,000+ for MCP
- Multiple HN commenters on mcp2cli thread noted "market saturation" of MCP token optimization tools

---

## 2. Developer Complaints (Pain Quotes with Sources)

**Quote 1** -- Scalekit benchmark:
> "A simple task like checking a repo's language consumed 1,365 tokens via CLI and 44,026 via MCP."
> Source: [Scalekit MCP vs CLI Benchmark](https://www.scalekit.com/blog/mcp-vs-cli-use)

**Quote 2** -- Developer David Zhang (via Apideck):
> "Load everything up front -- lose working memory for reasoning and history."
> Source: [Apideck Blog](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)

**Quote 3** -- Real deployment report (via Apideck):
> "57,000 tokens left for the actual conversation, retrieved documents, reasoning, and response" after MCP overhead consumed most of their budget.
> Source: [Apideck Blog](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)

**Quote 4** -- Layered.dev analysis:
> "Users were documenting setups with 7+ MCP servers consuming 67k+ tokens just for tool definitions."
> Source: [Layered.dev - The Hidden Token Tax](https://layered.dev/mcp-tool-schema-bloat-the-hidden-token-tax-and-how-to-fix-it/)

**Quote 5** -- MySQL MCP server measurement:
> "A MySQL server with 106 tools generated approximately 54,600 tokens on every initialization."
> Source: [Layered.dev](https://layered.dev/mcp-tool-schema-bloat-the-hidden-token-tax-and-how-to-fix-it/)

**Quote 6** -- Apideck context window stats:
> "143,000 of 200,000 tokens (72% of context window) consumed by three MCP servers in one reported case."
> Source: [Apideck Blog](https://www.apideck.com/blog/mcp-server-eating-context-window-cli-alternative)

**Quote 7** -- mcp2cli HN thread (skeptics):
> HN commenters flagged mcp2cli's README as "obviously generated slop," undermining credibility for an AI efficiency tool. Others noted "market saturation" of similar tools.
> Source: [Top AI Product on mcp2cli](https://topaiproduct.com/2026/03/09/mcp2cli-the-tool-that-cuts-mcp-token-costs-by-99-just-hit-hacker-news/)

**Quote 8** -- SEP-1576 on GitHub MCP server:
> "The 'owner' field appears in 60% of GitHub MCP tools" -- massive schema redundancy.
> Source: [SEP-1576](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/1576)

---

## 3. Competitive Landscape

### Runtime Token Optimizers (the crowded lane)

| Competitor | Approach | Claimed Reduction | Price | Weakness |
|-----------|----------|-------------------|-------|----------|
| **ToolHive/MCP Optimizer** (Stacklok) | Kubernetes-native semantic search, surfaces top-k tools on demand | 60-85% per request | Open source | Enterprise-only (K8s), no build-time feedback |
| **Speakeasy Dynamic Toolsets** | 3-function progressive discovery (search/describe/execute) | 91-97% input tokens | Commercial SDK | 50% slower execution, adds 2-3x tool calls per task |
| **mcp2cli** | Converts MCP to CLI with lazy --help discovery | 96-99% | Open source (MIT) | 273 stars, "generated slop" README, accuracy unproven |
| **Claude Tool Search** (Anthropic) | Auto-triggers when tools >10% of context, builds search index | ~85% | Built into Claude Code | Anthropic-only, not portable |
| **JCodeMunch** | Selective dataset retrieval, dynamic reindexing | Up to 99% (benchmarked 82%) | Unknown | Narrow use case (dataset queries) |
| **Apideck CLI** | Replace MCP entirely with CLI tools, ~80 token system prompt | 99%+ vs MCP | Commercial | Abandons MCP ecosystem entirely |

### MCP Gateways (the enterprise lane)

| Gateway | Overhead | Price | Focus |
|---------|----------|-------|-------|
| **MintMCP** | Not disclosed | Enterprise SLA, SOC 2 | Governance, audit trails |
| **Bifrost** | Sub-3ms (Go) | Open source | Pure speed |
| **Docker MCP Gateway** | Moderate | Open source | Container isolation security |
| **Composio** | Moderate | Freemium | 500+ pre-built connectors |
| **TrueFoundry** | 3-4ms | Commercial | 1M+ monthly request scale |

### Build-Time Linters/Auditors (OUR lane)

| Competitor | What | Stars | Status |
|-----------|------|-------|--------|
| **agent-friend audit CLI** (us) | 7-rule schema optimizer, token cost calculator, web tool | N/A | Shipped, differentiated |
| **token-ct** | Token counting only | 0 stars | Abandoned/dead |
| **mcp-scan** (Stytch) | Security auditing of tool manifests (npm-audit style) | Unknown | Active, but security-focused not cost-focused |
| **pare** | Referenced in SEP-1576, 70-90% token reduction via structured outputs | Unknown | Early/demo |

**Key insight**: The build-time optimization lane remains nearly empty. Everyone is building runtime middleware. Nobody is telling developers "your schema is bloated BEFORE you deploy."

---

## 4. Pricing Signals

### What developers are paying for MCP infrastructure
- **Direct MCP costs**: ~$55.20/month for 10K operations on Claude Sonnet 4 ($3/M input, $15/M output) -- Scalekit benchmark
- **CLI alternative**: ~$3.20/month for same 10K operations
- **Gateway-optimized MCP**: ~$5/month for same workload
- **Enterprise gateways**: $$$$ (MintMCP, Kong = enterprise pricing; Bifrost, Docker = free OSS)

### What developers are willing to pay
- The existence of Speakeasy (commercial), MintMCP (enterprise SLA), and Composio (freemium) suggests willingness to pay for token optimization
- mcp2cli and Bifrost going open-source suggests the tool-level optimizer is becoming commoditized
- The real money is in: (1) enterprise gateways with compliance, (2) integrated developer tools that save time, not just tokens

### Pricing gap for us
- A free audit CLI drives adoption; a paid "continuous audit" (CI/CD integration, team dashboards) could charge $20-50/month per team
- The web calculator (docs/audit.html) is a zero-cost lead-gen funnel

---

## 5. Ollama + Tool Calling Space

### Current State (March 2026)
- **Ollama v0.18.0** (Mar 14): Improved tool calling accuracy, specifically for Kimi-K2.5 and Qwen 3.5 models
- **v0.17.6** (earlier): Fixed tool calling parsing and rendering for Qwen 3.5
- **Go-based architecture** (covered in dasroot.net Feb 2026): Ollama transforming local LLM workflows
- **Anthropic API compatibility**: Ollama v0.14.0 added support -- lets Claude Code use local models for coding tasks
- **OpenClaw integration**: v0.18.1-rc1 adds native OpenClaw onboarding -- Ollama positioning as the local inference backend for agents

### Key Development
Ollama is becoming the default local inference layer for agent frameworks. OpenClaw (250K stars) + Ollama is the emerging stack for personal AI agents. The tool calling accuracy improvements in v0.18.0 suggest this is a priority area.

### Our position
agent-friend already has OllamaProvider (session 132). We're ahead of most in having native Ollama support with tool calling. Article 065 covers this.

---

## 6. Trending GitHub Repos in Agent Tooling

| Repo | Stars | What | Relevance |
|------|-------|------|-----------|
| **OpenClaw** | 250K+ | Personal AI agent, modular skills, local-first | Monster project, security concerns (20% malicious skills) |
| **autoresearch** (Karpathy) | ~23K | Automated ML research agent | High signal, Karpathy involvement |
| **DeerFlow** (ByteDance) | Unknown | SuperAgent framework, sub-agent collaboration | Enterprise-backed |
| **Superpowers** (obra) | Trending | Agent skill framework for coding | Direct competitor to our @tool decorator space |
| **Hindsight** (vectorize-io) | Trending | Learning agent memory | Adjacent, not competitive |
| **OpenViking** | Unknown | Context database for AI agents, file-system paradigm | Interesting architectural approach |

---

## 7. Conversations We Can Join / Gaps We Can Fill

### HIGH PRIORITY -- Conversations to join NOW

1. **SEP-1576** (only 4 comments, still OPEN)
   - We have a drafted comment in `drafts/sep-1576-comment.md`
   - This is the #1 distribution opportunity -- our audit CLI directly addresses this proposal
   - BLOCKED: needs board's GitHub token permissions

2. **ChromeDevTools MCP Issue #340**: "Feature Request: Optimize MCP Tool Schemas for AI Agent Token Efficiency"
   - We could comment with our audit approach and web calculator link
   - Source: [ChromeDevTools/chrome-devtools-mcp#340](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/340)

3. **Apideck's "MCP is eating your context" blog** (published on dev.to too)
   - We could comment on the dev.to version with our build-time approach
   - NOTE: dev.to comment API is broken via vault-devto, would need manual

4. **Layered.dev hidden token tax article**
   - They explicitly list "server-side concise descriptions" and "schema deduplication" as solutions -- our audit CLI does exactly this
   - Could reach out or comment

### MEDIUM PRIORITY -- Content opportunities

5. **Write about OpenClaw's 20% malicious skills problem** -- security angle, ties to mcp-scan and our audit approach
6. **Benchmark article**: "We measured MCP token costs across 10 popular servers" using our audit CLI -- data-driven content
7. **Ollama + agent-friend article**: Already have article 065, but could expand with v0.18.0 tool calling improvements
8. **"MCP Backlash is Wrong" counter-take**: Argue that the problem isn't MCP itself but lazy schema design -- our audit fixes this

### Gaps in the market

- **No build-time MCP schema linter exists as a standalone product** (we have this)
- **No CI/CD integration for MCP schema quality** (pre-commit hook, GitHub Action)
- **No "MCP schema best practices" authoritative guide** (we could write this)
- **No cross-server schema comparison tool** ("show me which servers are most bloated")
- **No MCP cost calculator that works offline** (our web calculator is close but requires paste)

---

## 8. Why AI Has an Edge

An AI-native MCP audit tool has structural advantages:

1. **Always-on schema monitoring**: A CI/CD bot can catch schema bloat on every commit, not just when a developer remembers to run an audit
2. **Pattern recognition across servers**: An AI can learn from thousands of MCP schemas what "good" looks like and flag deviations
3. **Automated fix suggestions**: Not just "this is bloated" but "here's the optimized version" -- something our 7-rule optimizer already does
4. **Cross-ecosystem intelligence**: Can track which schema patterns cause the most token waste across Anthropic, OpenAI, Google, and Ollama providers simultaneously

---

## 9. Recommended EV Estimate

### Market Size
- MCP ecosystem: thousands of servers in production, growing rapidly
- Every MCP server developer is a potential user of a schema linter
- Enterprise teams deploying MCP gateways (MintMCP, TrueFoundry, etc.) need audit tools upstream
- Estimated TAM: 10,000-50,000 MCP server developers by end of 2026

### Our Position
- **Strength**: Only build-time schema optimizer. Web calculator for lead gen. 2,674 tests.
- **Weakness**: Zero GitHub stars. No distribution. SEP-1576 comment blocked.
- **Opportunity**: The MCP backlash creates demand for "fix your schemas" rather than "add middleware." This is exactly our pitch.
- **Threat**: Runtime optimizers becoming so good that nobody bothers fixing schemas at source. Anthropic building audit tooling into Claude Code natively.

### EV Score: 6/10
- The problem is **real and validated** (Perplexity CTO, Scalekit benchmarks, multiple blog posts)
- The competition is **high but misdirected** (everyone doing runtime, nobody doing build-time)
- Distribution is our **critical bottleneck** -- the tool works but nobody knows about it
- **Immediate action items**: (1) Get SEP-1576 comment posted, (2) Comment on ChromeDevTools#340, (3) Write "MCP Schema Bloat Benchmark" article using real data from our audit CLI
