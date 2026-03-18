# Notion MCP Challenge: Video Walkthrough — VIDEO READY, NEEDS UPLOAD

**Priority**: P2 — Article auto-publishes March 22. Deadline March 29.

## Status Update (session 186, March 18 22:17 UTC)

**VIDEO IS GENERATED.** I created a 2:11 MP4 using TTS narration + terminal-style animation.

File: `/home/agent/company/products/content/video/notion_challenge_demo.mp4`
Size: 2.0 MB

**What you need to do:**
1. Upload `/home/agent/company/products/content/video/notion_challenge_demo.mp4` to YouTube (public or unlisted)
2. Get the YouTube URL
3. Leave the URL in board outbox so I can add it to article 073 before March 29

That's it. The video covers all 7 required sections with narration, terminal output, and ecosystem context.

## Original Request (still valid if video quality insufficient)

The Notion MCP Challenge requires a **video walkthrough** as part of a valid submission. Without it, we could be disqualified from prize consideration ($500 + meeting with Ivan Zhao, Notion CEO + runner-up $500).

From the challenge rules: "Participants must publish a post including: Project description, **Video walkthrough demonstrating the workflow**, Code repository link..."

## What the Generated Video Shows (7 scenes, 2m 11s)

1. Title card — agent-friend + Notion Dev Challenge
2. Grade command shown with actual flags
3. Full output: F (19.8/100), all 22 tools graded
4. Key findings: naming violations, undefined schemas, 4,463 tokens
5. Live Notion database output with actual tool grades
6. Ecosystem context: top 4 starred servers all grade D or below
7. Closing: GitHub link, report card URL, CLI install command

## If You Want to Re-Generate

```bash
python3 /home/agent/company/products/content/video/generate_video.py
```
Output goes to `/tmp/notion_challenge_video.mp4` (then copy to products/content/video/)

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
