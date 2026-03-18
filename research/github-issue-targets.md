# GitHub Issue Targets for agent-friend

Created: 2026-03-18 13:30 UTC (session 159)
Purpose: Repos with open issues where agent-friend would genuinely help. Ready for board to post comments.

## TIER 1: Highest Impact (file via board inbox)

### Anthropic MCP Servers (79K stars)
- **#3074**: Memory MCP schema validation fails — our validate catches this
- **#3144**: read_graph additionalProperties conflict — our fix suggests refactoring
- **#799**: sequentialthinking description > 1024 chars — our optimize auto-trims
- **Impact**: Credibility — our tool catches bugs in Anthropic's OWN reference implementations

### GitHub MCP Server (8K stars)
- **#1683**: Token scopes, verbose prompts, context bloat — they manually reduced 23K tokens. We show exact breakdown automatically.
- **Impact**: Microsoft/GitHub official repo. They've already done manual optimization. We automate it.

### Notion MCP Server (5K stars)
- **#153**: anyOf validator rejects valid commands
- **#164**: additionalProperties: false breaks strict validation
- **#102**: allOf incompatible with OpenAI
- **Impact**: Already graded F (19.8/100). Three active issues match our validate output exactly.
- **NOTE**: Already in board inbox as part of article 068 plan

### Composio (15K stars)
- **#2788**: Tool names exceed 64-char limit — breaks Cursor IDE
- **Impact**: 1000+ toolkits, naming violations are systematic. Our validate catches all of them.

## TIER 2: Medium Impact

### Docker MCP Gateway (2K stars)
- **#228**: Tool names use colons, violate MCP spec
- **Impact**: Docker official. Spec compliance is our thing.

### Atlassian MCP Server (1K stars)
- **#62**: Server name has dots/slashes, breaks Copilot CLI
- **Impact**: Enterprise tool, spec compliance.

## Comment Template (for board)

```
We noticed this matches a pattern we've been studying across MCP servers.
We ran a static analysis on [X] tools — [specific finding].

[agent-friend](https://github.com/0-co/agent-friend) catches this automatically:
`agent-friend validate your-schema.json`

[leaderboard](https://0-co.github.io/company/leaderboard.html) | 50 servers graded
```

## Status
- Context7 issue: Already in board inbox (P1)
- Notion issues: Planned for article 068 publish date (Mar 22)
- Others: Need new board request
