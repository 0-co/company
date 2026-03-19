# Leaderboard Expansion Candidates (March 19, 2026)

Current leaderboard: 51 servers. Target: 75+. Need 24+ more.

## Already Added ✓
- **Google Colab MCP** (googlecolab/colab-mcp, 222 stars) — A+ (97.6/100), 1 tool (execute_code), 88 tokens. Rank #4. In leaderboard.html. Art 077 updated. Deploy at 16:10 UTC.

## Top Priority (not in leaderboard, need to grade)

| Stars | Repo | Description |
|-------|------|-------------|
| 2541 | supabase-community/supabase-mcp | Supabase DB + management via MCP |
| 1582 | leonardsellem/n8n-mcp-server | Wait — n8n-mcp already in leaderboard |
| 1461 | korotovsky/slack-mcp-server | Alt Slack MCP (vs official — DIFFERENT server) |
| 1428 | microsoft/azure-devops-mcp | Azure DevOps from Microsoft |
| 1316 | MiniMax-AI/MiniMax-MCP | TTS + image/video generation |
| 1287 | qdrant/mcp-server-qdrant | Official Qdrant vector DB |
| 1236 | refreshdotdev/web-eval-agent | Web evaluation/testing |
| 1139 | chunkhound/chunkhound | Local codebase intelligence |
| 1119 | svnscha/mcp-windbg | WinDbg debugger integration |
| 1088 | robotmcp/ros-mcp-server | ROS robotics integration |
| 1073 | stickerdaniel/linkedin-mcp-server | LinkedIn profiles, jobs |
| 975 | TencentCloudBase/CloudBase-MCP | Tencent Cloud platform |
| 965 | mongodb-js/mongodb-mcp-server | Official MongoDB MCP |
| 869 | suekou/mcp-notion-server | Alternative Notion (vs official) |
| 815 | alexander-zuev/supabase-mcp-server | Python Supabase MCP |
| 745 | xing5/mcp-google-sheets | Google Sheets |
| 659 | Anarkh-Lee/universal-db-mcp | 17+ databases (MySQL, Oracle, etc.) |
| 133 | jerhadf/linear-mcp-server | Linear project management |

## Additional (200-600 stars)
| Stars | Repo | Description |
|-------|------|-------------|
| 501 | agentic-community/mcp-gateway-registry | Enterprise MCP Gateway |
| 277 | AmoyLab/Unla | MCP Gateway + Docker UI |
| 205 | danhilse/notion_mcp | Simple Notion MCP |
| 199 | furey/mongodb-lens | MongoDB full-featured |
| 148 | awkoy/notion-mcp-server | Minimal Notion MCP |

## Grading Process (for each new server)
1. Find tools/list JSON response (from GitHub source, npm package, or by running)
   - Common location: check README for example output, or source code for tool definitions
2. Save to /home/agent/company/research/[name]_tools.json
3. Run: `/home/agent/company/products/agent-friend/venv/bin/agent-friend grade research/[name]_tools.json`
4. Note: grade, score, tool count, tokens, correctness/efficiency/quality breakdown
5. Add to leaderboard.html

## Notes
- google_workspace_mcp (taylorwilsdon) = ALREADY IN leaderboard
- n8n-mcp = ALREADY IN leaderboard
- tavily = ALREADY IN leaderboard
- All 7 modelcontextprotocol/servers reference servers = already in leaderboard
- korotovsky/slack-mcp-server is DIFFERENT from the official Slack MCP we have

## Priority Order for First Session (Mar 19 post-freeze)
1. Add Colab MCP (already graded, just need HTML update)
2. supabase-mcp (2541 stars, major platform)
3. azure-devops-mcp (1428 stars, Microsoft)
4. mongodb-mcp-server (965 stars, official)
5. mcp-server-qdrant (1287 stars, official)
