#!/bin/bash
# Post-freeze deployment script
# Run at 16:10 UTC March 19, 2026

set -e
echo "[$(date -u)] Starting post-freeze deployment..."

# 1. Check art 064 24h reactions
echo ""
echo "=== Art 064 24h Reactions ==="
sudo -u vault /home/vault/bin/vault-devto GET /articles/me/published 2>/dev/null | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data:
    if 'MCP Won' in a.get('title','') or 'Dead' in a.get('title',''):
        print(f'Art 064 | reactions: {a.get(\"public_reactions_count\",0)} | views: {a.get(\"page_views_count\",\"N/A\")} | title: {a[\"title\"][:50]}')
        break
"

# 2. Deploy GitHub Pages
echo ""
echo "=== Deploying GitHub Pages ==="
sudo -u vault /home/vault/bin/vault-gh workflow run "Deploy GitHub Pages" --repo 0-co/company
echo "GitHub Pages deploy triggered."

# 3. Push grade-request template to agent-friend repo
echo ""
echo "=== Pushing grade-request template to agent-friend ==="
TMPDIR=$(mktemp -d)
cd "$TMPDIR"
git clone git@github-agent-friend:0-co/agent-friend.git .
mkdir -p .github/ISSUE_TEMPLATE
cp /home/agent/company/products/agent-friend/.github/ISSUE_TEMPLATE/grade-request.md .github/ISSUE_TEMPLATE/
git add .github/ISSUE_TEMPLATE/grade-request.md
git config user.email "agent@0co.ai"
git config user.name "0co CEO"
if git diff --cached --quiet; then
    echo "No changes to grade-request template."
else
    git commit -m "add grade-request issue template for leaderboard submissions"
    git push origin main
    echo "Grade-request template pushed to agent-friend repo."
fi
cd /home/agent
rm -rf "$TMPDIR"

echo ""
echo "[$(date -u)] Post-freeze deployment complete."
