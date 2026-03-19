#!/bin/bash
# Deploy grade-request.md issue template to agent-friend repo
# Run at 16:10 UTC March 19 after feature freeze lifts
set -e

TEMPLATE_SRC="/home/agent/company/products/agent-friend/.github/ISSUE_TEMPLATE/grade-request.md"
REPO_URL="git@github.com:0-co/agent-friend.git"
TMP_DIR="/tmp/agent-friend-deploy-$(date +%s)"

echo "Deploying grade-request.md to agent-friend repo..."

# Clone agent-friend
git clone "$REPO_URL" "$TMP_DIR"
cd "$TMP_DIR"

# Create .github/ISSUE_TEMPLATE directory
mkdir -p .github/ISSUE_TEMPLATE

# Copy template
cp "$TEMPLATE_SRC" .github/ISSUE_TEMPLATE/grade-request.md

echo "Template content:"
cat .github/ISSUE_TEMPLATE/grade-request.md

# Commit and push
git add .github/ISSUE_TEMPLATE/grade-request.md
git config user.email "agent@company"
git config user.name "CEO Agent"
git commit -m "add Submit for Grading issue template

Community can submit MCP servers for grading + leaderboard inclusion.
Links back to https://0-co.github.io/company/leaderboard.html

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push origin main

echo "Done! Template deployed to agent-friend repo."
echo "Issue template URL: https://github.com/0-co/agent-friend/issues/new?template=grade-request.md&title=Grade+request%3A+"
echo ""
echo "Next: Deploy GitHub Pages"
echo "  sudo -u vault /home/vault/bin/vault-gh workflow run 'Deploy GitHub Pages' --repo 0-co/company"
