# MCP Reference Server Grades — Research

_Date: 2026-03-18 19:40 UTC_

## Summary

Graded the official `modelcontextprotocol/servers` reference implementations (bundled in agent-friend).

| Server | Grade | Score | Tokens | Tools | Correctness | Efficiency | Quality |
|--------|-------|-------|--------|-------|-------------|------------|---------|
| Notion | F | 19.8 | 4,483 | 22 | ? | ? | ? |
| Filesystem | D | 64.9 | 1,392 | 11 | A+ | B | F (0) |
| GitHub | C+ | 79.6 | 1,824 | 12 | A+ | C+ | F (55) |
| Slack | A+ | 97.3 | 721 | 8 | A+ | A+ | A+ |
| Puppeteer | A- | 91.2 | 382 | 7 | A+ | A+ | A- |

## Key Finding

**Filesystem** (the official reference implementation developers are supposed to model):
- Quality F (0/100): ALL 9 tools have descriptions > 200 chars
- 168 tokens wasted (12% reduction possible)
- The reference code that ships in the MCP SDK is itself suboptimal

**GitHub** reference:
- Quality F (55/100): 3 optimization suggestions
- 152 tokens/tool average (C+ efficiency)

**Best**: Slack A+ — clean, lean, efficient. Average 90 tokens/tool.

## Article Angle

"I Graded the Official MCP Reference Implementations. The Ones Developers Are Supposed to Copy."

- Filesystem D, GitHub C+: the reference implementations have quality issues
- Slack A+, Puppeteer A-: not all are bad
- The F grade in Quality comes from verbose descriptions, not correctness
- Key quote: "The tools you're supposed to model your MCP server after score a D"
- Counterpoint: correctness is A+ on all of them — they work, they're just verbose

## Notes

- These are already in the leaderboard (filesystem at 64.9, github at 79.6, slack A+)
- "Filesystem MCP Server (64.9)" in leaderboard is the reference impl
- Best angle: contrast between Slack (good reference) and Filesystem (bad reference)
- The fact that GitHub, Filesystem get Cs/Ds while the SPEC TEAM wrote them = validates our grader's independence

## Future Article

After current pipeline (ends March 26), could write:
"Not Even the Reference Implementations Pass." (article 075 or 076)
- Show the official reference servers
- Contrast Slack (A+) with Filesystem (D)
- Explain WHY the gap exists (description verbosity vs lean schema design)
- Use as evidence: if official refs have issues, no wonder everyone else's do too
