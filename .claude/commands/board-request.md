Create a request for the board. This creates a file in `board/inbox/`.

Step 1: Determine priority.
- 1 = Urgent: blocking all productive work, no workaround
- 2 = High: blocking a specific active experiment
- 3 = Medium: needed soon but you have other work to do
- 4 = Low: would be nice, not blocking anything
- 5 = Whenever: future planning, no urgency

Step 2: Write the request.
Be specific. The board member has ~5 minutes per request. Include:
- **What you need** (one clear ask per file)
- **Why** (which hypothesis or goal this serves)
- **Context** (enough for the board to act without follow-up questions)
- **Suggested action** (make it easy — e.g., the exact account to create, the exact Nix snippet to review)
- **What happens if delayed** (helps the board prioritize)

Step 3: Save to inbox.
Filename: `{priority}-{short-description}.md`
Path: `/home/agent/company/board/inbox/`
Example: `2-need-discord-server.md`

Step 4: Commit and continue working.
Don't block. If this request is critical, make sure your status.md mentions it. Move on to the next highest-EV task that doesn't depend on this response.
