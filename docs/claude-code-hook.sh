#!/bin/bash
# agent-friend Claude Code hook
# Checks MCP server grades when .mcp.json changes
# Source: https://0-co.github.io/company/grades.json
#
# Setup: add to .claude/settings.json:
#   "hooks": {
#     "ConfigChange": [{
#       "matcher": ".",
#       "hooks": [{"type": "command", "command": "bash ~/.claude/hooks/af-check.sh"}]
#     }]
#   }

GRADES_URL="https://0-co.github.io/company/grades.json"
GRADES_CACHE="/tmp/af-grades-cache.json"

# Refresh grades cache if older than 24h or missing
if [ ! -f "$GRADES_CACHE" ] || [ $(($(date +%s) - $(stat -c %Y "$GRADES_CACHE" 2>/dev/null || echo 0))) -gt 86400 ]; then
  curl -s "$GRADES_URL" -o "$GRADES_CACHE" 2>/dev/null
fi

[ ! -f "$GRADES_CACHE" ] && exit 0

# Read hook input
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('file_path',''))" 2>/dev/null)

# Find .mcp.json files
MCP_FILES=$(find . ~/.claude.json 2>/dev/null -name ".mcp.json" -o -name "*.claude.json" 2>/dev/null | head -5)
[ -n "$FILE" ] && MCP_FILES="$FILE $MCP_FILES"

FOUND=0
for MCP_FILE in $MCP_FILES; do
  [ ! -f "$MCP_FILE" ] && continue
  SERVERS=$(python3 -c "
import json, sys
with open('$MCP_FILE') as f:
    data = json.load(f)
servers = data.get('mcpServers', {})
for name in servers:
    print(name)
" 2>/dev/null)

  [ -z "$SERVERS" ] && continue

  while IFS= read -r server; do
    GRADE=$(python3 -c "
import json
with open('$GRADES_CACHE') as f:
    data = json.load(f)
servers = data.get('servers', {})
# Try exact match, then fuzzy
s = '$server'.lower()
match = servers.get(s) or next((v for k,v in servers.items() if s in k or k in s), None)
if match:
    print(f'{match[\"grade\"]} ({match[\"score\"]:.1f}/100) — {match[\"name\"]}')
else:
    print('not in leaderboard (run: agent-friend grade <schema.json>)')
" 2>/dev/null)

    echo "  $server: $GRADE"
    FOUND=1
  done <<< "$SERVERS"
done

if [ "$FOUND" -eq 1 ]; then
  echo ""
  echo "  Leaderboard: https://0-co.github.io/company/leaderboard.html"
  echo "  Grade your own: pip install agent-friend && agent-friend grade <schema.json>"
fi
