# Request: Drop submission in Notion MCP Challenge thread

**Priority:** 2 (high — deadline March 29)

## Action needed

Comment on this Dev.to thread:
https://dev.to/axrisi/drop-your-challenge-submission-here-mej

**Comment text:**
> Built a tool that grades MCP schemas A+ to F. Pointed it at Notion's own server.
>
> Notion: F. 19.8/100. 22 tools, 4,463 tokens. Every tool name violates the spec.
>
> Then I used Notion MCP to build a live dashboard showing 201 graded servers.
>
> [ART_073_URL]
>
> #notionchallenge

## Why

axrisi's thread is the challenge aggregator (50+ reactions, highly visible to judges/voters). The board is the only one who can comment on external Dev.to posts.

**Deadline:** March 29 (challenge submission cutoff). File any time after art 073 is live on March 22.

## How to get ART_073_URL

```
sudo -u vault /home/vault/bin/vault-devto GET /articles/me/published?per_page=1 | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['url'])"
```

---
DRAFT — move to board/inbox/3-notion-challenge-thread-drop.md after filling in ART_073_URL
