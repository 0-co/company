# Board request draft — Notion challenge thread drop
# FILE THIS ON MARCH 22 AFTER 16:00 UTC (after art 073 URL is confirmed live)
# Filename: 3-notion-challenge-thread-drop.md

---
Priority: 3
Subject: Post article link in Dev.to Notion MCP Challenge thread

Art 073 is now live: [INSERT REAL URL AFTER 16:00 UTC MARCH 22]

Please post this comment on axrisi's challenge thread https://dev.to/axrisi/drop-your-challenge-submission-here-1e2k :

---
I built a tool that grades MCP schemas A+ to F. Notion's official server gets an F (19.8/100). The community build scores 96/100.

[Article URL here]

#notionchallenge
---

This is the "Drop Your Challenge Submission Here" aggregator for the Notion MCP Challenge (deadline March 29). 65+ entries currently. This is a required submission step to get the article in front of the judging panel.

The URL will be confirmed by fix_mar22_url.py script (PID 512231) which polls for art 073 after 16:00 UTC and updates staggered_posts_mar22.json automatically.

Steps to get URL:
  vault-devto GET /articles/me/published?per_page=1
  → should return art 073 URL (article about Notion MCP Challenge)
