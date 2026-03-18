# P3: Deploy agent-friend on Glama (1-click admin action)

Glama shows "cannot be installed / security not tested / quality not tested" because we haven't gone through their Docker deployment step. The server is already claimed. Need you to trigger the build.

## Action required (5 minutes)
1. Go to: https://glama.ai/mcp/servers/0-co/agent-friend/admin/dockerfile
2. The Dockerfile is already in the repo (products/agent-friend/Dockerfile) and should auto-detect
3. Click **Deploy**
4. Wait for build test to succeed
5. Click **Make Release**

## Why this matters
Glama is a major MCP discovery platform. Getting properly listed (with security/quality scores) = more installs/stars. Currently "cannot be installed" means users see a broken listing. The Dockerfile is correct and builds locally.

## Context
- Dockerfile: `FROM python:3.12-slim`, installs `mcp>=1.25`, copies agent_friend/ and mcp_server.py
- No secrets or env vars needed (pure stdio server)
- Should build clean
