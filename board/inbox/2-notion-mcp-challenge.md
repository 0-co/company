# Notion MCP Challenge — Need Notion API Credentials

**Priority: 2 (high value, time-sensitive)**
**Deadline: March 29, 2026 (challenge closes)**

## What I Need
A Notion integration token (Internal Integration Token) so I can build a challenge submission.

### Steps (should take ~10 minutes):
1. Create a free Notion account (or use an existing one)
2. Go to https://www.notion.so/my-integrations
3. Click "New integration" → name it "MCP Quality Dashboard"
4. Copy the Internal Integration Token (starts with `secret_...`)
5. Create a vault wrapper: `vault-notion` that injects the token as `NOTION_API_KEY`
6. Create a blank Notion page and share it with the integration (Connect to → MCP Quality Dashboard)

## Why
The Dev.to Notion MCP Challenge has a $1,500 prize pool, deadline March 29. Challenge submissions automatically get 15-30 reactions from built-in discovery — our articles currently get 0.

**The build:** An MCP Quality Dashboard that uses Notion MCP to store tool audit results in a Notion database. Runs our grade pipeline against any MCP server and creates per-tool entries: name, grade, token count, issues.

**The meta-hook:** "I used Notion's MCP server to build a quality dashboard. The first thing I audited was Notion's own MCP server. It scored an F."

This is our highest-EV distribution play right now:
- Even 5% win probability = $75 EV (vs $0 revenue)
- Guaranteed 15-30 article reactions (10-15x our best)
- Completion badge on Dev.to profile
- Great Twitch content ("building a challenge submission live")
- Dogfoods agent-friend in a new integration

## Also Need: YouTube Upload
The Dev.to challenge requires a video demo. The top-ranked submissions all use YouTube. I need board to upload a terminal recording (~2-3 min MP4) to the 0coceo YouTube channel. I'll produce the video content — board just needs to handle the upload.

**Critical path:**
- Need Notion token + YouTube by March 22 to leave time to build, test, and submit
- March 22 → 25: Build + demo + article
- March 25 → 29: Buffer for fixes

## If Approved
I'll build the tool, write the challenge article, and produce a terminal demo MP4. Target: submit by March 25 (4 days buffer).
