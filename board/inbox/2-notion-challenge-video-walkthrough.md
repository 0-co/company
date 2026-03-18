# Notion MCP Challenge: Video Walkthrough Needed

**Priority**: P2 — Article auto-publishes March 22. Deadline March 29. 7 days for reactions + video add.

## What

The Notion MCP Challenge requires a **video walkthrough** as part of a valid submission. Without it, we could be disqualified from prize consideration ($500 + meeting with Ivan Zhao, Notion CEO + runner-up $500).

From the challenge rules: "Participants must publish a post including: Project description, **Video walkthrough demonstrating the workflow**, Code repository link..."

## What We Need

A 2-3 minute screen recording showing:
1. Run `agent-friend grade` on Notion's official MCP server (`npx -y @notionhq/notion-mcp-server`)
2. Output shows F grade (19.8/100) — 22 tools, naming violations, undefined schemas
3. Optionally: show the live Notion database at notion.so with 29 servers graded
4. Optionally: show the web report card at https://0-co.github.io/company/report.html

A rough narration script:
> "We built agent-friend, a quality grader for MCP servers. Let's grade Notion's own server, which is the subject of their dev.to challenge. [run grade command] The result: F — 19.8 out of 100. Every tool name violates MCP spec. 5 undefined schemas. 4,463 tokens. Here's the same data live in a Notion database. And here's the report card."

## Your Options

1. **Record a screen capture** of the terminal running the grade command. Any screen recorder + YouTube upload works. OBS, QuickTime, etc.
2. **I can generate MP4 with TTS narration** if you can run the capture — I have a neural TTS server (port 8081) and can script the CLI commands. You'd just upload the resulting file.

## Timing

- **March 22**: Article auto-publishes. Ideal to add video link same day.
- **March 29 11:59 PM PST**: Challenge deadline. We must have video in the article by then.
- **March 29**: 7 days to maximize reactions after publish.

## Setup

```bash
# In agent-friend repo
pip install agent-friend
agent-friend grade "$(npx -y @notionhq/notion-mcp-server --list-tools 2>/dev/null)"

# Or using local install
cd /tmp && pip install agent-friend
python3 -c "import agent_friend; print('ready')"
```

The grader output will show F grade automatically — we already verified this.

## Code Repository

Already ready: https://github.com/0-co/agent-friend

## Why This Matters

$500 cash + meeting with Ivan Zhao (Notion CEO) is a legitimate outcome. Our submission is technically strong (F-grading Notion's own server in their challenge = originality + technical depth). We just need the video to be valid.
