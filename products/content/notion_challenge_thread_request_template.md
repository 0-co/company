# Board Request: Notion Challenge Thread Drop
# USE ON MARCH 22 AFTER 16:00 UTC — fill in REAL_URL before filing

Priority: 3
Filename: 3-notion-challenge-thread-drop.md

## Request

Please drop a reply in the Notion MCP Challenge thread (or the main challenge page) with our submission.

## Thread text to post

"Built a tool that grades MCP schemas A+ to F. Notion's official server gets an F (19.8/100). Community-built Notion server gets 96/100. 77-point gap.

REAL_URL

#notionchallenge"

## Context

Art 073 just published. The Notion challenge deadline is March 29. Other competitors are at 30-59 reactions. We need visibility in the challenge feed.

## How to get REAL_URL

sudo -u vault /home/vault/bin/vault-devto GET /articles/me/published?per_page=1 | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['url'])"
