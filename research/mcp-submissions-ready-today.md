# MCP Distribution: Ready-to-Submit TODAY
## Actionable Submissions (15-30 Min Work)
**Date:** 2026-03-18
**Current State:** agent-friend v0.61.0, 27 servers graded, 0 GitHub stars

---

## PRIORITIZED SUBMISSION QUEUE

### TIER 1: HIGHEST IMPACT, LOWEST FRICTION (Do First)

#### 1. Docker MCP Registry Issue
**URL:** https://github.com/docker/mcp-registry
**Type:** GitHub issue
**Time:** 5 minutes
**Reach:** Growing (Docker-sponsored)
**Approval Speed:** ~24 hours

**Why This First:**
- Fastest approval possible
- Builds on your existing Dockerfile
- Docker endorsement = credibility
- No dependencies on other approvals

**How to Submit:**
1. Go to https://github.com/docker/mcp-registry/issues
2. Click "New Issue"
3. Choose "MCP Server Submission" template (if available)
4. Fill with:

```markdown
## MCP Server Submission: agent-friend

### Server Information
- **Name:** agent-friend
- **Description:** MCP schema quality validator, linter, and grader.
  Validates MCP tool definitions, detects token bloat, identifies
  prompt injection attacks, and grades schemas A+ to F.
- **Repository:** https://github.com/0-co/agent-friend
- **Main Branch:** master
- **License:** MIT

### Docker Information
- **Dockerfile Path:** products/agent-friend/Dockerfile
- **Base Image:** python:3.12-slim
- **Entrypoint:** Stdio-based MCP server (mcp SDK)
- **Image Size:** ~500MB (includes mcp, pydantic, anthropic)

### Server Capabilities
- **Validate:** 12 schema quality checks (strict mode available)
- **Audit:** Token cost calculator for 5 LLM providers
- **Optimize:** Auto-fix 6 common issues (naming, descriptions, schemas)
- **Grade:** Quality score (A+ through F) with weighted scoring
- **Security:** Detects prompt injection patterns in tool descriptions

### Languages Supported
Python (primary via mcp SDK)
Exposes OpenAI, Anthropic, Google, Ollama, BitNet schemas

### Tags
validation, quality, linting, security, schema-tools, ai-dev-tools

### Links
- GitHub: https://github.com/0-co/agent-friend
- Web Tools: https://0-co.github.io/company/docs/report.html
- Glama Listing: https://glama.ai/mcp/servers/...

### Installation
```bash
docker pull docker.io/0co/agent-friend:latest
# or via CLI config
```

### Maintenance
- Actively maintained
- Regular updates (v0.61.0 released March 2026)
- Issue response time: <24 hours
```

**Expected Outcome:** Issue created. Docker team reviews within 1 business day.

---

#### 2. awesome-mcp-devtools Pull Request
**URL:** https://github.com/punkpeye/awesome-mcp-devtools
**Maintainer:** punkpeye (knows your work)
**Type:** GitHub PR
**Time:** 15 minutes
**Reach:** 435 stars but HIGHLY TARGETED (build-time tools for MCP)
**Approval Speed:** 2-3 days

**Why This One:**
- Exact category match (you're a developer tool for MCP developers)
- Maintainer is familiar with your work (Glama badge approval)
- Lower traffic = higher bar but higher relevance
- Good stepping stone to show credibility

**How to Submit:**
1. Fork https://github.com/punkpeye/awesome-mcp-devtools
2. Edit README.md
3. Find the section for "Validation & Quality Tools" (or create it)
4. Add entry:

```markdown
### Validation & Quality Tools

- **[agent-friend](https://github.com/0-co/agent-friend)** -
  MCP schema linter and quality grader. Validate schemas (12 checks),
  audit token costs, auto-fix issues, and grade A+ through F.
  Unique: detects prompt injection in tool descriptions.
  _Python, CLI + web tools, MIT License_
```

5. Commit message: `Add agent-friend MCP quality linter`
6. Create PR with description:

```markdown
## Add agent-friend — MCP Schema Quality Tool

### What is agent-friend?
MCP schema validation and quality grading tool. Fills a gap in the
MCP developer toolkit by offering build-time quality analysis.

### Why it belongs here
- **For MCP developers:** Helps validate and optimize schemas before shipping
- **Unique focus:** Only build-time quality linter in the MCP ecosystem
- **Active development:** v0.61.0 just released with prompt injection detection
- **Web tools:** Interactive validator, auditor, grader at https://0-co.github.io/company/docs/

### Stats
- GitHub: 0 stars (new)
- PyPI: Installable
- License: MIT
- Tests: 3,068 passing
```

**Expected Outcome:** PR created. Likely merged within 3 days. Maintainer may reach out.

---

#### 3. Check MCPServers.com
**URL:** https://mcpservers.com/
**Time:** 5 minutes
**Type:** Web form check

**What to Do:**
1. Visit https://mcpservers.com/
2. Look for "Submit" button or contact info
3. If web form exists: Fill it out immediately (usually auto-approves)
4. If email contact: Send email using template below

**Email Template (if needed):**
```
Subject: MCP Server Submission - agent-friend

Hi MCPServers.com Team,

We'd like to submit agent-friend for listing on your directory:

Name: agent-friend
GitHub: https://github.com/0-co/agent-friend
Description: MCP schema quality validator, linter, and grader.
Detects token bloat, prompt injection, naming violations.

Glama listing: https://glama.ai/mcp/servers/...
Web tools: https://0-co.github.io/company/docs/report.html

Category: Developer Tools / Validation
License: MIT

Please let me know if you need additional information.

Thanks,
Agent Friend Team
```

**Expected Outcome:** Either instant listing or 1-2 day approval.

---

#### 4. Check MCP.so
**URL:** https://mcp.so/
**Time:** 5 minutes
**Type:** Web form check

**What to Do:**
1. Visit https://mcp.so/
2. Look for "Add Server" or "Submit" option
3. Fill form with same info as MCPServers.com
4. If no form: Search for "contact" or "submit"

**Template:**
```
Name: agent-friend
URL: https://github.com/0-co/agent-friend
Description: Quality grader for MCP schemas. Validates, audits,
optimizes, grades (A+ to F). Detects prompt injection.
Category: Development Tools
```

**Expected Outcome:** Auto-listed or manual approval within 24 hours.

---

### TIER 2: MEDIUM IMPACT, DOABLE NOW (If Time)

#### 5. Official MCP Registry PR
**URL:** https://github.com/modelcontextprotocol/registry
**Type:** GitHub PR
**Time:** 20 minutes
**Approval Speed:** 3-7 days

**Why Later:**
- More official = higher bar
- Requires structured JSON metadata
- Good to do AFTER awesome-mcp-devtools approval (shows credibility)

**How to Submit:**
1. Fork https://github.com/modelcontextprotocol/registry
2. Create file: `servers/agent-friend.json`
3. Content:

```json
{
  "name": "agent-friend",
  "description": "MCP schema quality validator, linter, and grader. Validates tool definitions, detects token bloat and prompt injection, grades A+ through F.",
  "repository": {
    "type": "git",
    "url": "https://github.com/0-co/agent-friend"
  },
  "homepage": "https://github.com/0-co/agent-friend",
  "author": {
    "name": "0-co",
    "email": "contact@0-co.ai",
    "url": "https://0-co.ai"
  },
  "license": "MIT",
  "codeLanguages": ["python"],
  "pythonVersion": "3.10+",
  "installationMethod": "pip",
  "installationUrl": "pip install git+https://github.com/0-co/agent-friend",
  "tags": ["validation", "quality", "linting", "security", "schema-tools"],
  "toolCategories": ["data-tools", "dev-tools"],
  "features": [
    "Schema validation (12 checks)",
    "Token cost auditing",
    "Prompt injection detection",
    "Auto-optimization (6 fixes)",
    "Quality grading (A+ to F)"
  ]
}
```

4. Commit: `Add agent-friend MCP server`
5. PR description:

```markdown
## Add agent-friend to MCP Registry

### Server Summary
agent-friend is a comprehensive MCP schema quality tool providing:
- Build-time schema validation
- Token cost analysis
- Prompt injection detection
- Auto-fix capability
- Quality grading system

### Why Include
- Addresses MCP ecosystem quality gap (token bloat, security issues)
- 3,068+ test coverage
- Active maintenance
- Complies with MCP spec

### Links
- Glama: Listed and maintained
- Web tools: https://0-co.github.io/company/docs/
- GitHub: https://github.com/0-co/agent-friend
```

**Expected Outcome:** Merged in 3-7 days, becomes part of official registry.

---

### TIER 3: STRATEGIC (After 20 Stars + 30 Servers)

#### 6. Hacker News "Show HN"
**Wait for:** 20 GitHub stars (currently 0)
**Wait for:** 30 servers graded (currently 27, almost there)
**Time to Draft:** 30 minutes now, post when ready

**Title Ideas:**
```
Show HN: I Graded 27 Popular MCP Servers. The Results Are Embarrassing
Show HN: ESLint for MCP Schemas — Catching Prompt Injection in AI Tools
Show HN: agent-friend — MCP Quality Grader That Caught Prompt Injection in #2 Server
```

**Story Hook:**
"Found prompt injection in Blender MCP (17.8K stars, #2 most popular).
Built a quality linter for MCP servers. Graded 27 popular servers;
results show no correlation between GitHub stars and schema quality."

**Key Talking Points:**
- Both top-2 most popular servers score F
- Prompt injection detection unique to agent-friend
- 27 servers, 510 tools, 97K tokens analyzed
- Leaderboard is first of its kind
- Token bloat is systemic problem

**Draft to Board when:** 20 stars + 30 servers graded

---

#### 7. Discord MCP Community Post
**URL:** https://discord.com/invite/model-context-protocol-1312302100125843476
**Wait for:** 20 GitHub stars
**Time:** 10 minutes live in Discord

**Where to Post:** Look for #tools or #showcase channel

**Message Template:**
```
🔍 **agent-friend — MCP Schema Quality Grader**

Just released v0.61.0. A complete quality analysis suite for MCP servers:
• 12-check validator (prompt injection, token bloat, naming violations)
• Token cost auditor (calculate % of context used)
• Auto-fixer (6 common issues)
• Quality grader (A+ through F)

Graded 27 popular MCP servers. Both top 2 score F.

Leaderboard: https://0-co.github.io/company/docs/leaderboard.html
GitHub: https://github.com/0-co/agent-friend
Web tools: https://0-co.github.io/company/docs/report.html

OSS, MIT license. Feedback welcome!
```

---

## CRITICAL DETAILS FOR SUBMISSIONS

### GitHub Links Format
**Your Repo:** https://github.com/0-co/agent-friend
**Your Glama Listing:** https://glama.ai/mcp/servers/0-co/agent-friend
**Web Tools:** https://0-co.github.io/company/docs/
**Leaderboard:** https://0-co.github.io/company/docs/leaderboard.html
**Report Card:** https://0-co.github.io/company/docs/report.html

### Key Positioning Line
"MCP schema quality validator. Like ESLint for MCP tool definitions. Detects token bloat, prompt injection, and naming violations. Grades schemas A+ through F."

### Key Differentiator
"Only MCP tool that detects prompt injection in schema descriptions. Found prompt injection in Blender MCP (#2 most popular) and 3 other servers."

### Credibility Signals
- 3,068 passing tests
- v0.61.0 released March 2026
- Listed on Glama.ai
- Graded 27 public servers
- Active GitHub repo with weekly updates
- Two professional web tools

---

## SUBMISSION CHECKLIST

### Before You Start
- [ ] Read repo description updated to quality-first positioning
- [ ] Confirm GitHub README links to leaderboard
- [ ] Verify all web tools working (validate.html, audit.html, report.html, leaderboard.html)
- [ ] Check that Glama.ai still shows your listing

### Submissions to File Today
- [ ] Docker MCP Registry issue (5 min)
- [ ] awesome-mcp-devtools PR (15 min)
- [ ] Check MCPServers.com form (5 min)
- [ ] Check MCP.so form (5 min)

### Follow-Up Items (March 20)
- [ ] Check Docker approval status
- [ ] Check awesome-mcp-devtools PR comments/merge
- [ ] Follow up with PulseMCP if no response
- [ ] Check MCPServerFinder status

### After 20 Stars
- [ ] Join Discord community
- [ ] Post introduction in #tools

### After 30 Servers + Article 064 Success
- [ ] Draft HN "Show HN" submission
- [ ] Send to board for posting

---

## EXPECTED TIMELINE

**Today (Mar 18):**
- 4 submissions filed (Docker, awesome-mcp-devtools, 2x web form checks)
- 0-2 instant approvals expected
- 2-3 pending manual review

**Mar 19:**
- Docker approval (likely)
- awesome-mcp-devtools comments/merge starts

**Mar 20-22:**
- awesome-mcp-devtools merge (likely)
- Check PulseMCP/MCPServerFinder status
- Article 064 performance data in

**Mar 24-26:**
- HN "Show HN" ready if 20 stars reached
- Consider Product Hunt launch planning

---

## SUCCESS METRICS

**Immediate (after submissions):**
- 4+ MCP directories listing agent-friend
- 2 PRs merged by end of week
- 1 Docker image published

**Short-term (by Mar 31):**
- 20+ GitHub stars
- 5+ MCP directories total
- 50+ organic visitors from directories
- Discord engagement

**Medium-term (by Apr 15):**
- HN thread (300+ pts target)
- Product Hunt launch
- 100+ GitHub stars
- 30+ servers on leaderboard

