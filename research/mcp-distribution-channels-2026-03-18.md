# MCP Distribution Channels Research
_Compiled 2026-03-18_

## Summary
- **Biggest opportunity**: punkpeye/awesome-mcp-servers (81.5K stars) and the Official MCP Registry (6.6K stars) are the two highest-reach channels we have NOT submitted to yet
- **Underexplored**: There are 15+ MCP directories/registries, most accepting submissions via PR or form. We have only submitted to 4.
- **Community channels**: The official MCP Discord (11,658 members), Cursor Forum (74K+ devs), and Cline Marketplace (757 stars, millions of Cline users) are all untapped

---

## Already Submitted (for reference)
| Channel | Status |
|---------|--------|
| Glama (19K+ servers) | LIVE |
| mcpservers.org / wong2/awesome-mcp-servers (3.6K stars) | Submitted (via website) |
| PulseMCP (11,160+ servers) | Emailed, pending |
| MCP Server Finder | Emailed, pending |
| awesome-ai-devtools PR #310 | Open |
| Dev.to | 13 articles |
| Bluesky | 37 followers |
| GitHub Discussions | 19 posts |

---

## NEW Channels to Pursue

### Tier 1: Highest Reach (do these first)

#### 1. punkpeye/awesome-mcp-servers
- **URL**: https://github.com/punkpeye/awesome-mcp-servers
- **Reach**: 81,500 stars, 7,500 forks
- **How to submit**: Open a PR. 422 open PRs, 1,648 closed. Actively merged.
- **Fit**: We are a dev tool for MCP servers. Could go under a "Developer Tools" or "Utilities" section. punkpeye already approved our Glama badge PR, so there is a relationship.
- **Priority**: P0 -- single highest-reach channel in the entire MCP ecosystem

#### 2. Official MCP Registry
- **URL**: https://registry.modelcontextprotocol.io/
- **GitHub**: https://github.com/modelcontextprotocol/registry (6,600 stars)
- **Reach**: 87+ servers currently listed. This is THE canonical registry. All MCP clients will eventually pull from here.
- **How to submit**: Install `mcp-publisher` CLI. Run `mcp-publisher init` to generate server.json. Authenticate via GitHub device flow (`mcp-publisher login`). Run `mcp-publisher publish`. Requires GitHub OIDC or OAuth.
- **Blocker**: Requires GitHub device flow auth (board item). The registry only hosts metadata -- the artifact must be on npm or GitHub Releases.
- **Priority**: P0 -- this is the official long-term registry

#### 3. Cline MCP Marketplace
- **URL**: https://github.com/cline/mcp-marketplace
- **Reach**: 757 stars. Cline has millions of users (top VS Code AI extension).
- **How to submit**: Create a new issue using their template. Provide: GitHub repo URL, 400x400 PNG logo, explanation of value. They review in ~2 days.
- **Requirements**: Community adoption, developer credibility, project maturity, security review.
- **Priority**: P0 -- direct access to millions of Cline users via built-in marketplace

#### 4. appcypher/awesome-mcp-servers
- **URL**: https://github.com/appcypher/awesome-mcp-servers
- **Reach**: 5,200 stars, 762 forks
- **How to submit**: Open a PR. 175 open PRs, 194 closed. Actively maintained.
- **Priority**: P1

#### 5. Anthropic Connectors Directory (Claude.com)
- **URL**: https://claude.com/connectors
- **Submission guide**: https://support.claude.com/en/articles/12922490-remote-mcp-server-submission-guide
- **Reach**: All Claude Pro/Team/Enterprise users
- **How to submit**: Submit via Anthropic's form. Requires: 3+ working examples, documentation, authentication details, privacy policy, support contact. Must support OAuth with Dynamic Client Registration for HTTP servers.
- **Blocker**: Requires remote HTTP server with OAuth. Our MCP server is currently stdio-only. Would need to build an HTTP transport layer.
- **Priority**: P1 (high value but requires engineering work)

---

### Tier 2: Strong Reach

#### 6. MCP.so
- **URL**: https://mcp.so/
- **Reach**: 16,670+ servers listed (largest directory by count)
- **How to submit**: Click "Submit" in navigation bar, or create a GitHub issue in their repo.
- **Priority**: P1

#### 7. LobeHub MCP Marketplace
- **URL**: https://lobehub.com/mcp
- **Reach**: LobeHub is a popular open-source AI chat framework
- **How to submit**: Click "Submit MCP" button on the marketplace page at lobehub.com/mcp
- **Priority**: P1

#### 8. MCP Market (mcpmarket.com)
- **URL**: https://mcpmarket.com/
- **Reach**: 19,000+ servers listed
- **How to submit**: Via submission form on the website
- **Priority**: P2

#### 9. Cursor Directory
- **URL**: https://cursor.directory/plugins
- **Reach**: 74,400+ developers building with Cursor
- **How to submit**: "Submit a plugin" option on cursor.directory
- **Priority**: P1

#### 10. Cursor Community Forum
- **URL**: https://forum.cursor.com/c/showcase/built-for-cursor/19
- **Reach**: Active developer forum with MCP discussions
- **How to submit**: Post in "Built for Cursor" showcase section. Also post in the "Share Your Experience with MCP Tools" discussion thread.
- **Priority**: P1

#### 11. OpenTools Registry
- **URL**: https://opentools.com/registry
- **Reach**: Curated MCP server registry focused on practical endpoints
- **How to submit**: Check opentools.com for submission guidelines or use `npx opentools` CLI
- **Priority**: P2

#### 12. Windsurf Directory
- **URL**: https://windsurf.run/mcp
- **Reach**: Windsurf IDE users
- **How to submit**: Check windsurf.run for submission process
- **Priority**: P2

---

### Tier 3: Awesome Lists (Niche but Credible)

#### 13. punkpeye/awesome-mcp-devtools
- **URL**: https://github.com/punkpeye/awesome-mcp-devtools
- **Reach**: 435 stars. Specifically for MCP developer tools -- linters, SDKs, testing utilities.
- **How to submit**: PR following CONTRIBUTING.md guidelines
- **Fit**: PERFECT fit. This list is specifically for MCP dev tools. Already lists security scanners and diagnostics tools like mcp-doctor.
- **Priority**: P0 -- most relevant awesome list for our exact category

#### 14. rohitg00/awesome-devops-mcp-servers
- **URL**: https://github.com/rohitg00/awesome-devops-mcp-servers
- **Reach**: 961 stars
- **How to submit**: PR following CONTRIBUTING.md
- **Priority**: P2

#### 15. analysis-tools-dev/static-analysis
- **URL**: https://github.com/analysis-tools-dev/static-analysis
- **Website**: https://analysis-tools.dev/
- **Reach**: 14,400 stars. Website adds rankings, comments, videos per tool.
- **How to submit**: PR. "Pull requests are very welcome!"
- **Fit**: MCP tool schema linting is a form of static analysis. Would need to frame it as a linter for MCP tool definitions.
- **Priority**: P2

#### 16. caramelomartins/awesome-linters
- **URL**: https://github.com/caramelomartins/awesome-linters
- **Reach**: 816 stars
- **How to submit**: PR with title "Add [LINTER] for [LANGUAGE]". Run pre-commit before submitting.
- **Fit**: Moderate. We lint MCP tool schemas, not a traditional programming language. Could go under "Multiple Languages" or a new "Schema/Protocol" section.
- **Priority**: P3

#### 17. mcp-get/community-servers
- **URL**: https://github.com/mcp-get/community-servers
- **Reach**: 66 stars (small). But mcp-get is a package manager -- servers listed here are installable via CLI.
- **How to submit**: PR following CONTRIBUTING-FOR-LLMS.md
- **Priority**: P3

---

### Tier 4: Community Channels

#### 18. Official MCP Discord
- **URL**: https://discord.com/invite/model-context-protocol-1312302100125843476
- **Reach**: 11,658 members
- **How to join**: Click invite link, join server
- **What to post**: Share agent-friend as a dev tool, participate in discussions about tool quality and schema design
- **Priority**: P1

#### 19. Cursor Forum -- MCP Discussions
- **URL**: https://forum.cursor.com/t/share-your-experience-with-mcp-tools/148437
- **Reach**: Large active forum
- **How to post**: Create account, post in discussions or showcase sections
- **Priority**: P1

#### 20. Product Hunt
- **URL**: https://www.producthunt.com/
- **Reach**: Massive. MCP tools regularly get featured. mcp-use got 120K downloads after PH launch.
- **How to submit**: Create a product page, schedule a launch
- **Priority**: P1 (but requires careful timing and preparation)

---

### Tier 5: Newsletters and Content

#### 21. PulseMCP Newsletter (already emailed for directory)
- **URL**: https://www.pulsemcp.com/newsletter
- **Reach**: Weekly MCP newsletter, cited on HN. Run by MCP Steering Committee members.
- **Action**: Follow up on directory submission. Could also pitch a featured article about MCP tool quality.

#### 22. Ben's Bites
- **URL**: https://news.bensbites.com/
- **Reach**: 140,000+ subscribers
- **How to submit**: Create account on news.bensbites.com, submit a post. Top-voted posts get included in the daily newsletter.
- **Priority**: P2 (free, community-voted)

#### 23. Latent Space (Podcast + Newsletter)
- **URL**: https://www.latent.space/
- **Reach**: 10 million+ readers/listeners in 2025. Top AI engineer podcast.
- **How to submit**: They accept guest posts and have a guest writer program. Email about contributing.
- **Priority**: P3 (hard to get featured, but massive reach)

#### 24. daily.dev
- **URL**: https://daily.dev/
- **Reach**: Developer news aggregator. Auto-indexes Dev.to articles.
- **Action**: Our Dev.to articles should already be indexed. Check if they appear. Can also submit directly.
- **Priority**: P3

#### 25. TLDR AI Newsletter
- **URL**: https://tldr.tech/ai
- **Reach**: 1.25 million readers
- **How to submit**: Paid sponsorship only ($15K/issue). Not viable for us.
- **Priority**: SKIP (paid only)

---

## Action Plan (Prioritized)

### Immediate (can do today, no blockers)
1. **PR to punkpeye/awesome-mcp-servers** (81.5K stars)
2. **PR to punkpeye/awesome-mcp-devtools** (435 stars, perfect fit)
3. **PR to appcypher/awesome-mcp-servers** (5.2K stars)
4. **Submit to Cline MCP Marketplace** via GitHub issue (needs 400x400 logo)
5. **Submit to MCP.so** via their Submit button
6. **Submit to LobeHub MCP Marketplace**
7. **Submit to MCP Market** (mcpmarket.com)

### This week (minor prep needed)
8. **Join Official MCP Discord** and share tool
9. **Post in Cursor Forum** "Built for Cursor" section
10. **Submit to Cursor Directory** as plugin
11. **Submit to OpenTools Registry**
12. **PR to rohitg00/awesome-devops-mcp-servers** (961 stars)
13. **Submit to Ben's Bites** community
14. **Launch on Product Hunt** (needs product page, logo, description)

### Requires engineering/board
15. **Official MCP Registry** -- needs GitHub device flow auth (board)
16. **Anthropic Connectors Directory** -- needs HTTP transport + OAuth
17. **Smithery** -- needs API key (board)
18. **PR to analysis-tools-dev/static-analysis** (14.4K stars, needs framing)

---

## Estimated Total Addressable Reach

| Channel Type | Channels | Combined Reach |
|---|---|---|
| Awesome lists (GitHub stars) | 6 lists | ~106K stars |
| MCP directories/registries | 8 directories | ~66K+ listed servers |
| Community forums | 3 forums | ~86K+ members |
| Newsletters | 2 viable | ~140K+ subscribers |
| Marketplaces (Cline, Cursor, LobeHub) | 3 | Millions of IDE users |
| Product Hunt | 1 | Massive general tech audience |

**Total new channels identified: 25**
**Channels actionable today (no blockers): 7**
**Channels actionable this week: 14**
