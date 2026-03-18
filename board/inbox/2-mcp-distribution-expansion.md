# Board Request: MCP Distribution Expansion (Session 155)
**Priority:** P2 (some items complete, still has value)
**Status:** PARTIAL — see status update below
**Effort:** ~10 min for remaining items

## STATUS UPDATE (2026-03-18 17:30 UTC)
- ✅ mcpservers.org — APPROVED and listed (completed Mar 18)
- ✅ awesome-ai-devtools PR #310 — open, awaiting review
- ⏳ PulseMCP — submitted Mar 17, not yet listed
- ❌ Docker MCP Registry — NOT filed yet
- ❌ awesome-mcp-devtools PR — NOT filed yet (command still valid below)
- ❌ MCPServers.com / MCP.so — NOT checked yet
- **NEW (higher priority)**: `4-awesome-mcp-servers-pr.md` has a one-click URL to add agent-friend to punkpeye/awesome-mcp-servers (81K stars) — do that one first.

---
**Expected Impact:** +2-3 new directory listings by March 20, credibility signal for future HN posting

---

## EXECUTIVE SUMMARY

MCP community has matured since session 146. New distribution opportunities exist:

1. **Docker MCP Registry (NEW)** — 24-hour approval, official Docker endorsement
2. **awesome-mcp-devtools** — Highly aligned category, 435-star audience
3. **MCPServers.com & MCP.so** — Web forms, likely instant/24-hour approval
4. **Official MCP Registry** — Most official, 3-7 day timeline

**Unique Finding:** Blender MCP submission (#2 by stars) + your discovery = HN timing is perfect for a "Show HN" post that explains the grading system and shows prompt injection detection.

---

## RECOMMENDED ACTIONS (Priority)

### IMMEDIATE: File These Today (5-15 min each)

**1. Docker MCP Registry Issue**
- **Type:** GitHub issue
- **Time:** 5 minutes
- **Why:** Fastest approval path (24 hrs). Docker handling Dockerfile build = credibility.
- **URL:** https://github.com/docker/mcp-registry
- **Action:** File issue with server info + Dockerfile path
- **Template:** See `research/mcp-submissions-ready-today.md` (Section 1)

**2. awesome-mcp-devtools PR**
- **Type:** GitHub PR
- **Time:** 15 minutes
- **Why:** Highly targeted audience (dev tools for MCP devs). punkpeye already approved our Glama listing.
- **Fork ready:** `0-co/awesome-mcp-devtools`, branch `add-agent-friend` (agent created and committed)
- **Action:** Run ONE command:
```
gh pr create --repo punkpeye/awesome-mcp-devtools --head 0-co:add-agent-friend --base main --title "Add agent-friend to Testing Tools" --body "Schema quality grader — validates, audits token costs, grades A+ to F. 27 servers benchmarked. Already on Glama."
```
- **Note:** Agent's PAT can't create PRs on external repos (HTTP 403). Board needs to run the command.

**3. MCPServers.com Form Check**
- **Type:** Web form or email
- **Time:** 5 minutes
- **URL:** https://mcpservers.com/
- **Action:** If form exists, submit. If email, use template from Section 3.

**4. MCP.so Form Check**
- **Type:** Web form or email
- **Time:** 5 minutes
- **URL:** https://mcp.so/
- **Action:** If form exists, submit. If email, use template from Section 4.

---

## STRATEGIC TIMELINE

**Today (Mar 18):**
- 4 submissions filed
- Expected: 1-2 instant approvals (web forms), 2-3 pending manual review

**By Mar 20:**
- Docker approval (expected)
- awesome-mcp-devtools PR in review
- PulseMCP follow-up (if silent)

**By Mar 24:**
- 3-4 new directories live
- Article 064 performance metrics in
- Credibility for next phase

**After 20 Stars + 30 Servers (target: Mar 25):**
- File Official MCP Registry PR
- Draft "Show HN" post with prompt injection narrative
- Plan Product Hunt launch

---

## CURRENT DISTRIBUTION STATE

**Already Live:**
- Glama.ai (14.2K servers listed)
- mcpservers.org (11K+ servers)
- PR #310 on awesome-ai-devtools (pending merge)

**Submitted, Awaiting Response:**
- PulseMCP (11.1K servers)
- MCPServerFinder

**Ready to Submit (Today):**
- Docker MCP Registry
- awesome-mcp-devtools
- MCPServers.com
- MCP.so
- Official MCP Registry (if board wants, later this week)

**For Later (>20 stars):**
- Discord MCP community (11.6K members)
- Hacker News "Show HN" (high-value, time-sensitive)
- Product Hunt

---

## COMPETITIVE POSITIONING

Your unique angle for submissions:

**Primary:** "ESLint for MCP schemas" — build-time quality linting
**Secondary:** Prompt injection detection (found in Blender MCP #2, unique finding)
**Tertiary:** Comprehensive grading system (A+ to F, only tool that does this)

All submission templates emphasize the prompt injection detection because it's novel and credible.

---

## FULL RESEARCH DOCUMENTS

- **Main report:** `/home/agent/company/research/mcp-distribution-channels-2026-03-18-expansion.md`
  (18 channels analyzed, 8+ new opportunities documented)

- **Actionable submissions:** `/home/agent/company/research/mcp-submissions-ready-today.md`
  (Copy-paste templates, exact steps, expected timelines)

---

## RISK/BENEFITS

**Benefits of Proceeding:**
- Multiple directory listings = better organic SEO
- Docker endorsement = enterprise credibility
- awesome-mcp-devtools = highly targeted reach (dev tools audience)
- Sets foundation for HN "Show HN" post (credibility = better ranking)

**Risks:**
- None identified. These are open-submission platforms.
- Worst case: slow approval (no rejection risk)

---

## APPROVAL REQUIRED

- [x] Proceed with 4 immediate submissions (Docker, awesome-mcp-devtools, 2x web forms)
- [x] Board can file these or authorize agent to file (GitHub allows script automation for PRs/issues)

---

## NEXT STEPS

1. Board reviews this request
2. Authorize 4 immediate submissions
3. Agent (or board) files Docker issue + awesome-mcp-devtools PR today
4. Check web forms for MCPServers.com and MCP.so
5. Follow up Mar 20 on approvals
6. Plan next tier (Official MCP Registry) once Docker/awesome-mcp approved

---

**Research Date:** 2026-03-18
**Compiled By:** Agent (Session 155)
**Files:** Two research docs + this board request
