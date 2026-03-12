#!/bin/bash
# Day 6 startup script — run at the start of Day 6 (midnight UTC March 13)
# Updates day counters, stream title, deploys GitHub Pages

cd /home/agent/company

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

log "=== Day 6 Startup ==="

# CRITICAL: Publish article053 FIRST — everything else is nice-to-have
log "Publishing article053 (agent-friend pivot) to dev.to..."
ARTICLE_RESP=$(sudo -u vault /home/vault/bin/vault-devto PUT "/articles/3341088" '{"article":{"published":true}}' 2>/dev/null)
if [ -n "$ARTICLE_RESP" ]; then
  ARTICLE_URL=$(echo "$ARTICLE_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('url',''))" 2>/dev/null)
  if [ -n "$ARTICLE_URL" ]; then
    log "Article 053 PUBLISHED: $ARTICLE_URL"
    # Update the announcement post with the real article URL
    sed -i "s|full story: dev.to/0coceo|full story: $ARTICLE_URL|" /home/agent/company/products/content/day6_article053_post.txt
    sed -i "s|Article: https://dev.to/0coceo|Article: $ARTICLE_URL|" /home/agent/company/products/content/day6_discord_article.txt
    log "Updated announcement posts with article URL"
  else
    log "Article 053 published but couldn't extract URL"
  fi
else
  log "Article 053 publish FAILED"
fi

# 1. Update index.html: 5 → 6 days, 20d → 19d
log "Updating index.html..."
python3 -c "
import re
with open('docs/index.html', 'r') as f:
    content = f.read()
# Use regex to update day counter regardless of HTML formatting
content = re.sub(r'(<div class=\"num\">)5(</div>\s*<div class=\"label\">Days Running)', r'\g<1>6\g<2>', content)
content = re.sub(r'(<div class=\"num\">)20d(</div>\s*<div class=\"label\">Until Deadline)', r'\g<1>19d\g<2>', content)
with open('docs/index.html', 'w') as f:
    f.write(content)
print('index.html updated: 5→6 days, 20d→19d')
"

# 2. Regenerate journal with latest commits
log "Regenerating session journal..."
python3 products/content/session_journal.py

# 3. Regenerate race board with fresh data
log "Refreshing race board..."
python3 products/content/race_board.py

# 4. Commit and push
log "Committing..."
git add docs/index.html docs/journal.html docs/race.html products/content/race_board_history.json
git commit -m "chore: Day 6 startup — update day counter, refresh pages" || log "Nothing to commit"
git push || log "Push failed"

# 5. Update Twitch stream title
log "Updating Twitch stream title..."
FOLLOWERS=$(sudo -u vault /home/vault/bin/vault-twitch GET /channels/followers?broadcaster_id=1455485722 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('total',1))" 2>/dev/null || echo "1")
NEW_TITLE="AI builds universal tool adapter — @tool → OpenAI, Claude, Gemini, MCP | Day 6 | github.com/0-co/agent-friend"
sudo -u vault /home/vault/bin/vault-twitch PATCH /channels "{\"broadcaster_id\":\"1455485722\",\"title\":\"$NEW_TITLE\"}" 2>/dev/null && log "Stream title updated: $NEW_TITLE" || log "Stream title update failed"

# 6. Update Bluesky profile bio with current metrics
log "Updating Bluesky profile bio..."
python3 products/content/update_bsky_profile.py && log "Profile updated" || log "Profile update failed"

# 7. Archive MEMORY.md snapshot and regenerate memory-evolution.html
log "Archiving MEMORY.md snapshot..."
python3 products/content/memory_archive.py && log "Memory archived" || log "Memory archive failed (non-fatal)"

# 8a. Vocab tracker removed (conversation-analyzer deleted in cleanup)
log "Skipping vocab tracker (removed in cleanup)"

# 8b. Refresh AI social graph network data
log "Refreshing AI social graph..."
python3 products/network-tracker/collect.py && log "Network data updated" || log "Network collect failed"

# 9. Commit updated data and trigger GitHub Pages deploy
log "Committing network data..."
git add docs/network_data.json products/network-tracker/network_data.json docs/memory-evolution.html memory-archive/ || true
git commit -m "chore: Day 6 network graph + memory snapshot" || log "Nothing to commit"
git push || log "Push failed"
sudo -u vault /home/vault/bin/vault-gh workflow run "Deploy GitHub Pages" --repo 0-co/company && log "GitHub Pages deploy triggered" || log "Pages deploy trigger failed"

# 10. Article053 already published in step 0 above
log "Article053 was published at startup (step 0)"

log "=== Day 6 Startup complete ==="
log "=== Next: update day5_recap_thread.txt P2/P3 with actual Day 5 stats before 11:00 UTC ==="
