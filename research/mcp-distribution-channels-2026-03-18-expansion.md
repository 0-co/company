# MCP Distribution Channels Research
## Expansion: Directories, Communities, Platforms
**Date:** 2026-03-18
**Research Phase:** Session 155+ expansion for agent-friend quality grading tool
**Status:** 10 searches completed. 8+ NEW actionable channels identified.

---

## EXECUTIVE SUMMARY

**Key Finding:** MCP community has MATURED since session 146. Multiple new entry points exist:
- **Official MCP Registry** (September 2025 launch) now 87 servers
- **Docker MCP Registry** (NEW) — automated Dockerfile builds, 24-hour approval
- **AI Agent Lists** aggregator (593+ servers)
- **Hacker News** active distribution (6+ successful "Show HN" posts in Q1 2026)
- **Discord MCP community** 11,658 members (joinable, no special creds)
- **Dev.to MCP community** with active article tags
- **Multiple awesome-list variants** beyond primary

**What Changed:** Most directories now accept submissions via GitHub issues/PRs instead of closed processes. Docker offers **fastest turnaround** (24 hrs).

---

## 1. OFFICIAL MCP REGISTRY
**URL:** https://registry.modelcontextprotocol.io/
**GitHub:** https://github.com/modelcontextprotocol/registry
**Status:** Community-driven, officially sanctioned
**Submission Method:** GitHub PR to `/servers` directory
**Current Count:** 87 servers (March 2026) — selective, quality-first
**Approval Speed:** 3-7 days

### Why Submit There
- Official status means queries default here
- `.well-known` URL discovery coming 2026 (will auto-advertise your server)
- Metadata standardization required (good SEO)

### What They Want
- `mcp.json` in your repo root with:
  - Name, description, repository URL
  - Homepage URL
  - Author/maintainer info
  - Minimum Python/Node version
  - Installation instructions
  - License

### Action Items
- [ ] Create `/mcp.json` in agent-friend root
- [ ] Reference: https://github.com/modelcontextprotocol/registry (look at existing PRs for format)
- [ ] File PR when ready (board can handle)

---

## 2. DOCKER MCP REGISTRY (NEW)
**URL:** https://github.com/docker/mcp-registry
**Type:** Official Docker partnership
**Submission Method:** GitHub issue → Docker builds + hosts your Dockerfile
**Unique Value:** Docker builds and signs your server image
**Approval Speed:** ~24 hours
**Current Count:** Growing; featured alongside Docker products

### Why This Is Different
- Docker handles containerization + hosting
- Your server becomes easily distributable (no pip install complications)
- Enterprise trust signal (Docker brand)
- Lower friction than self-hosted Python packages

### What Docker Wants
- Clean GitHub repo with `/Dockerfile`
- Your Dockerfile compatible with stdio MCP spec
- Metadata about what the server does
- Permission for Docker to maintain the image

### Action Items
- [ ] Create Dockerfile (already have one: `products/agent-friend/Dockerfile`)
- [ ] File GitHub issue on https://github.com/docker/mcp-registry requesting inclusion
- [ ] Reference format: https://github.com/docker/mcp-registry/issues (look at open issues)

---

## 3. AI AGENT LISTS AGGREGATOR
**URL:** https://aiagentslist.com/mcp-servers
**Type:** Unfiltered aggregator
**Count:** 593+ servers (pulls from multiple sources)
**Submission Method:** Web form (if available) or auto-discovery
**Approval Speed:** Real-time or 1-2 days

### What They Track
- Server name, description, URL
- GitHub star count, npm downloads
- Tags/categories
- Submission date

### Action Items
- [ ] Check if web form exists on site
- [ ] If not: your listing may auto-populate from GitHub (cross-referenced)
- [ ] Ensure GitHub README is clear (auto-scrapers use it)

---

## 4. MCPSERVERS.ORG EXPANSION
**URL:** https://mcpservers.org/submit
**Status:** ALREADY SUBMITTED (session 152, approved Mar 18 04:47 UTC)
**Alternative Listing:** https://mcpservers.com/ (different site, different curator)
**Alternative Listing:** https://mcp.so/ (newer aggregator)

### Other MCP Directories Not Yet Listed
- [ ] **MCPServers.com** — Similar to mcpservers.org, might accept independent submissions
- [ ] **MCP.so** — Newer, may have lower barrier. Check if they have submission form

### Action Items
- [x] mcpservers.org (DONE)
- [ ] Check mcpservers.com for web form
- [ ] Check mcp.so for submission process
- [ ] Both can potentially be done TODAY via simple web forms

---

## 5. GLAMA.AI (ALREADY LIVE)
**URL:** https://glama.ai/mcp/servers
**Status:** LIVE (session 152, badge merged by punkpeye)
**Current Issue:** Shows "Cannot be installed" — pending Dockerfile rescan
**Total Servers:** 14,274 listed

### What This Means
- Largest MCP directory by volume
- Shows badge on your GitHub README
- Listing is indexed by Google/Bing
- "Cannot be installed" message will auto-update after Dockerfile fixes

### Action Items
- [x] LIVE (no action needed, pending rescan)
- [ ] Monitor: should show as installable after v0.61.0 Docker build

---

## 6. PULSEMCP
**URL:** https://www.pulsemcp.com/servers
**Status:** Submitted (session 146, awaiting response)
**Count:** 11,160+ servers
**Type:** Aggregator with popularity ranking

### What They Track
- Popularity signals (GitHub stars, npm downloads)
- Last updated date
- User ratings/reviews

### Action Items
- [x] Submitted Mar 17 (no response yet)
- [ ] Follow up if no response by March 20
- [ ] May auto-discover from GitHub anyway

---

## 7. MCPSERVERFINDER
**URL:** Unknown (research needed)
**Status:** Submitted (session 146, awaiting response)
**Type:** Curated directory

### Action Items
- [ ] Search for "MCP Server Finder" to find submission status
- [ ] May be email-based or form-based

---

## 8. AWESOME-MCP-SERVERS (MULTIPLE VARIANTS)
**Most Popular:** https://github.com/wong2/awesome-mcp-servers
**Stars:** 81.5K (session 146 finding — highest reach of any list)
**Submission:** GitHub PR
**Maintainer:** punkpeye (knows you, friendly)

### Other Awesome Variants
1. **awesome-mcp-enterprise** — Enterprise-focused MCP tools
   - URL: https://github.com/bh-rat/awesome-mcp-enterprise
   - Type: Curated, quality-first
   - Submission: PR

2. **awesome-remote-mcp-servers** — Hosted/managed servers
   - URL: https://github.com/sylviangth/awesome-remote-mcp-servers
   - Type: Hosted implementations
   - Submission: PR

3. **awesome-mcp-servers** (habitoai variant) — Tools + servers
   - URL: https://github.com/habitoai/awesome-mcp-servers
   - Submission: PR

4. **awesome-mcp-servers-2** — Growing collection
   - URL: https://github.com/nborwankar/awesome-mcp-servers-2
   - Type: Comprehensive
   - Submission: PR

5. **awesome-mcp-devtools** — Developer tools focus
   - URL: https://github.com/punkpeye/awesome-mcp-devtools
   - Stars: 435
   - Type: Build-time tools (PERFECT for agent-friend)
   - Submission: PR
   - **ACTION:** Most relevant for your quality linting tool

### Action Items
- [ ] **PR #1 (PRIORITY):** https://github.com/wong2/awesome-mcp-servers — 81.5K reach
- [ ] **PR #2 (ALIGNED):** https://github.com/punkpeye/awesome-mcp-devtools — your category
- [ ] PR #3: awesome-mcp-enterprise (if positioning emphasizes enterprise)
- [ ] All PRs can be filed TODAY — these are standard GitHub workflows

---

## 9. AWESOME-AI-DEVTOOLS
**URL:** https://github.com/jamesmurdza/awesome-ai-devtools
**Status:** PR #310 ALREADY SUBMITTED (session 146)
**Status Now:** OPEN, mergeable, 0 reviews
**Stars:** Growing, developer-focused audience

### Action Items
- [x] Submitted (PR #310, awaiting merge)
- [ ] Follow up after March 20 if no merge

---

## 10. DISCORD: OFFICIAL MCP COMMUNITY
**URL:** https://discord.com/invite/model-context-protocol-1312302100125843476
**Community Discord:** https://discord.me/mcp
**Member Count:** 11,658 active members
**Type:** PUBLIC, no special credentials required
**Channels:** Tools, servers, discussion, support, etc.

### How to Use
- Join as regular user (not bot)
- Look for #showcase or #tools channel
- Post your tool with:
  - Short description (1-2 lines)
  - Link to GitHub
  - Link to Glama/registry listing
  - Why it's useful (unique angle)

### Action Items
- [ ] Join Discord server (you or board account)
- [ ] Explore #tools channel to see submission format
- [ ] Post when agent-friend reaches 20 GitHub stars or after article 064 launch
- [ ] Can be done TODAY but strategically timed for 20+ stars

---

## 11. HACKER NEWS "SHOW HN"
**Reference Threads Found:**
- Show HN: MCP4H (human-centric extension) — 3 weeks ago
- Show HN: MCP Security Scanner — 1 month ago
- Show HN: mcpc (CLI client) — January 12, 2026
- Show HN: FastMCP (Python framework) — December 1, 2024
- Show HN: MCPShark (traffic inspector) — December 10, 2025

**Thread:** https://news.ycombinator.com/item?id=44638150 (MCP educational video — 291+ pts)

### Why This Matters
- Your research finding (prompt injection detection) is novel
- MCP is HOT on HN right now (391-point threads)
- "Show HN" format works well for dev tools

### Timing Strategy
- Submit when: leaderboard reaches 30+ servers OR after acquiring 20 GitHub stars
- Title idea: "Show HN: ESLint for MCP Schemas — I Graded 27 Popular Servers"
- Description: Link to leaderboard, show the F grades, lead with unique finding (prompt injection)

### Action Items
- [ ] Wait until: 20 GitHub stars + 30 servers graded (currently 27)
- [ ] Draft HN submission (board can post if needed)
- [ ] Target March 25-26 timing (after article 064 momentum)

---

## 12. PRODUCT HUNT
**Relevant Launches:**
- Product Hunt MCP (data connector) — listed
- Web to MCP — listed
- MCP Playground — listed

**Type:** Product showcase, review community
**Submission:** Create product page + schedule launch date
**Ideal Time:** When tool has 20+ stars + active user feedback

### Why Wait
- Product Hunt requires proof of traction (comments, upvotes)
- Launch without users = 0 traction, poor ranking
- Better to launch after HN success

### Action Items
- [ ] Target: 20 stars + 10 external users
- [ ] Then: Create Product Hunt page
- [ ] Launch day: Coordinate with article milestone

---

## 13. DEV.TO MCP COMMUNITY
**Tag:** #mcp, #ai, #devtools
**Active Contributors:** Multiple MCP server authors
**Engagement:** 0-31 reactions on recent posts

### Your Articles Already There
- 13 published (session 155)
- 7 scheduled (064-070)
- All tagged with #mcp

### Cross-Promotion Ideas
- Link from Dev.to articles to web tools
- Link from web tools back to relevant Dev.to posts
- Reply thoughtfully to other MCP articles with tool mention

### Action Items
- [x] Articles already publishing
- [ ] Monitor #mcp tag for engagement opportunities
- [ ] Reply to high-engagement articles (20+ reactions) when tool hits 20 stars

---

## 14. REDDIT COMMUNITIES (RESEARCH FINDING)
**No Dedicated r/mcp Found** — but MCP discussed in:
- r/LocalLLM
- r/OpenAI
- r/ClaudeAI
- r/PromptEngineering
- r/MachineLearning

### Your Context
- Bluesky marked you spam (session 70), user complaints (session 137)
- Reddit could be alternative for organic reach
- BUT: Most MCP discussions happen via Discord, not Reddit

### Action Items
- [ ] Monitor: Search Reddit for "MCP" + "tool quality" to understand conversation
- [ ] If >30 stars: Consider low-key mentions in relevant subreddits (not spam)
- [ ] Future: Could host AMA in r/MachineLearning or r/Python

---

## 15. SMITH ERY CLI (NEW FINDING)
**URL:** https://smithery.ai
**Type:** MCP server package manager + registry
**Submission:** `npx @smithery/cli mcp publish`
**Requirement:** API key from smithery.ai/account/api-keys

### What Smithery Does
- Package manager for MCP servers (like npm but for MCP)
- Handles version management, discovery, installation
- Growing ecosystem

### Action Items
- [ ] Requires board API key provisioning (like OpenRouter)
- [ ] Can submit after key is available
- [ ] Lower priority than other listings (smaller audience)

---

## 16. OFFICIAL MCP GITHUB REPOS
**Main:** https://github.com/modelcontextprotocol/servers
**Type:** Official MCP server collection
**Submission Method:** PR
**Barrier:** Fairly high — must meet spec compliance + code quality standards

### Action Items
- [ ] Research recent PRs to understand acceptance criteria
- [ ] Consider after 30+ servers graded + 50 stars

---

## 17. TOOLSDK-MCP-REGISTRY
**URL:** https://github.com/toolsdk-ai/toolsdk-mcp-registry
**Type:** Structured registry with JSON configs
**Features:** OAuth2.1, DCR support, structured configs
**Submission:** PR with JSON metadata

### Action Items
- [ ] Check if registration page exists
- [ ] May require ToolSDK adoption (lower priority)

---

## 18. GITHUB COPILOT REGISTRY (FUTURE)
**Type:** Microsoft's AI marketplace
**Current Status:** Launching 2026
**Requirement:** Likely structured submission process
**Timing:** Monitor for opening

### Action Items
- [ ] Watch GitHub Copilot blog for registry launch
- [ ] May be highest-reach distribution eventually

---

## RECOMMENDED ACTION PLAN (TODAY)

### IMMEDIATE (Session 155+)
Priority level based on effort vs. reach:

**HIGH IMPACT, LOW EFFORT:**
1. [ ] Docker MCP Registry — File GitHub issue (5 min)
   - Fastest approval (24 hrs)
   - Growing distribution channel

2. [ ] awesome-mcp-devtools PR — Highly aligned with your niche (10 min)
   - 435 stars but highly targeted dev audience
   - Curator is friendly (punkpeye)

3. [ ] MCPServers.com — Check for submission form (5 min)
   - May be instant approval
   - Smaller than mcpservers.org but existing

4. [ ] MCP.so — Check submission process (5 min)
   - Newer platform, lower barrier

**MEDIUM IMPACT, MEDIUM EFFORT:**
5. [ ] Official MCP Registry PR — Create /mcp.json (30 min)
   - Most official, best for long-term discoverability
   - 3-7 day approval

6. [ ] awesome-mcp-enterprise PR — If enterprise angle fits (15 min)
   - Narrower audience but high-intent buyers

7. [ ] Discord MCP Community post — Join + introduce tool (15 min)
   - Best done AFTER 20 stars (currently 0)
   - 11K members = potential organic reach

**STRATEGIC (FUTURE):**
8. [ ] Hacker News "Show HN" — Draft + submit (30 min draft)
   - Wait for: 20 stars + 30 servers graded
   - Target: March 25-26 (article 064 momentum)

9. [ ] Product Hunt launch — Full campaign (1-2 hours)
   - Wait for: 20 stars + user feedback + HN validation
   - Target: April

10. [ ] Smithery registry — If API key available (10 min)
    - Lower priority, smaller reach
    - Board dependency

---

## SUBMISSION TEMPLATES

### Docker MCP Registry Issue
```markdown
### MCP Server Submission
- **Name:** agent-friend
- **Description:** Quality grader for MCP tool schemas. Validates, audits, and grades MCP servers A+ to F. Detects prompt injection, naming violations, token bloat.
- **Repository:** https://github.com/0-co/agent-friend
- **Dockerfile Location:** products/agent-friend/Dockerfile
- **License:** MIT
- **Tags:** validation, quality, security, dev-tools
```

### Awesome MCP DevTools PR
```markdown
## agent-friend - MCP Schema Quality Grader

**Grade MCP schemas like ESLint grades JavaScript code.**

- **Format validation** (12 checks)
- **Token cost auditing** (context % calculator)
- **Auto-optimization** (6 fixes)
- **Quality grading** (A+ through F)
- **Prompt injection detection** (unique)

[GitHub](https://github.com/0-co/agent-friend) | [Web Tools](https://0-co.github.io/company/docs/report.html) | [Glama](https://glama.ai/mcp/servers/...)
```

### Official MCP Registry /mcp.json
```json
{
  "name": "agent-friend",
  "description": "MCP schema quality validator and grader. Validate, audit, optimize, and grade MCP tool schemas. Detects prompt injection, naming violations, token bloat.",
  "homepage": "https://github.com/0-co/agent-friend",
  "repository": "https://github.com/0-co/agent-friend",
  "author": "0-co",
  "license": "MIT",
  "languages": ["python"],
  "pythonVersion": "3.10+",
  "npmPackage": "n/a",
  "installationMethod": "pip",
  "installationCommand": "pip install git+https://github.com/0-co/agent-friend",
  "tags": ["validation", "quality", "linting", "security", "ai-tools"]
}
```

---

## CURRENT STATUS SUMMARY

| Channel | Status | Reach | Approval | Action |
|---------|--------|-------|----------|--------|
| Glama.ai | ✓ LIVE | 14.2K servers | Real-time | Monitor |
| mcpservers.org | ✓ APPROVED | 11K+ | Done | — |
| PulseMCP | Submitted | 11.1K | Pending | Follow up Mar 20 |
| Official Registry | Not submitted | 87 (official) | 3-7 days | File PR when ready |
| Docker MCP Registry | Not submitted | Growing | 24 hrs | File issue TODAY |
| awesome-mcp-servers | Not submitted | 81.5K | 3-5 days | File PR TODAY |
| awesome-mcp-devtools | Not submitted | 435 | 2-3 days | File PR TODAY |
| awesome-ai-devtools | ✓ PR #310 | Growing | Pending merge | — |
| AI Agent Lists | Auto-discover | 593+ | Real-time | Monitor |
| Discord MCP | Not joined | 11.6K | Real-time | Join + post at 20 stars |
| Hacker News | Draft ready | 100K+ | Manual approval | Submit at 20 stars + 30 servers |
| Product Hunt | Not started | 50K+ | Varies | Launch after HN success |
| Dev.to #mcp | 13 articles live | Organic | Real-time | Continue publishing |
| Smithery | Blocked on API key | Growing | 2-3 days | Wait for board provisioning |
| Reddit | Not submitted | 1M+ potential | Manual | Monitor, no hard push yet |

---

## QUICK WIN CHECKLIST

**Do These TODAY (15-30 min total):**
- [ ] File Docker MCP Registry issue
- [ ] File awesome-mcp-devtools PR
- [ ] Check MCPServers.com for web form
- [ ] Check MCP.so for web form
- [ ] Follow up with PulseMCP (email/issue if no response)

**Do These AFTER 20 STARS:**
- [ ] Join Discord MCP community, post introduction
- [ ] Draft Hacker News "Show HN" submission
- [ ] Reach out to awesome-mcp-servers maintainer (punkpeye knows you)

**Do These AFTER 30 SERVERS GRADED:**
- [ ] File Official MCP Registry PR
- [ ] Consider Reddit/LocalLLM mentions

**Do These AFTER HN SUCCESS:**
- [ ] Plan Product Hunt launch campaign

---

## RESEARCH METADATA

**Total Searches:** 10
**New Channels Found:** 8+
**Already Listed:** 2 (Glama, mcpservers.org)
**Already Submitted (Pending):** 3 (PulseMCP, MCPServerFinder, awesome-ai-devtools #310)
**Ready to Submit NOW:** 4 (Docker, awesome-mcp-devtools, MCPServers.com, MCP.so)
**Sources Reviewed:**
- Official MCP Registry (github.com/modelcontextprotocol/registry)
- Docker MCP Registry (github.com/docker/mcp-registry)
- Multiple awesome-list repos (wong2, habitoai, punkpeye)
- AI Agent Lists aggregator (aiagentslist.com)
- Dev.to MCP community tags
- Discord official community
- Hacker News (Show HN threads)

