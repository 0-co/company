#!/bin/bash
# Day 6 startup script — run at the start of Day 6 (midnight UTC March 13)
# Updates day counters, stream title, deploys GitHub Pages

set -e
cd /home/agent/company

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

log "=== Day 6 Startup ==="

# 1. Update index.html: 5 → 6 days, 20d → 19d
log "Updating index.html..."
python3 -c "
import re
with open('docs/index.html', 'r') as f:
    content = f.read()
content = content.replace('<div class=\"num\">5</div>\n        <div class=\"label\">Days Running</div>', '<div class=\"num\">6</div>\n        <div class=\"label\">Days Running</div>')
content = content.replace('<div class=\"num\">20d</div>', '<div class=\"num\">19d</div>')
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
NEW_TITLE="Day 6: 19 days left | ${FOLLOWERS}/50 followers | AI company building in public"
sudo -u vault /home/vault/bin/vault-twitch PATCH /channels "{\"broadcaster_id\":\"1455485722\",\"title\":\"$NEW_TITLE\"}" 2>/dev/null && log "Stream title updated: $NEW_TITLE" || log "Stream title update failed"

# 6. Update Bluesky profile bio with current metrics
log "Updating Bluesky profile bio..."
python3 products/content/update_bsky_profile.py && log "Profile updated" || log "Profile update failed"

# 7. Archive MEMORY.md snapshot and regenerate memory-evolution.html
log "Archiving MEMORY.md snapshot..."
python3 products/content/memory_archive.py && log "Memory archived" || log "Memory archive failed (non-fatal)"

# 8a. Run vocabulary similarity tracker (daily snapshot)
log "Running vocab similarity tracker..."
python3 products/conversation-analyzer/vocab_tracker.py && log "Vocab snapshot saved" || log "Vocab tracker failed (non-fatal)"

# 8b. Refresh AI social graph network data
log "Refreshing AI social graph..."
python3 products/network-tracker/collect.py && log "Network data updated" || log "Network collect failed"

# 9. Commit updated data and trigger GitHub Pages deploy
log "Committing network data..."
git add docs/network_data.json products/network-tracker/network_data.json docs/memory-evolution.html memory-archive/ || true
git commit -m "chore: Day 6 network graph + memory snapshot" || log "Nothing to commit"
git push || log "Push failed"
sudo -u vault /home/vault/bin/vault-gh workflow run "Deploy GitHub Pages" --repo 0-co/company && log "GitHub Pages deploy triggered" || log "Pages deploy trigger failed"

# 10. Publish article049 (MCP security) to dev.to — no Bluesky announcement per spam-flag
log "Publishing article049 (MCP security) to dev.to..."
ARTICLE_ID=$(cat products/content/article049_id.txt 2>/dev/null || echo "3340454")
sudo -u vault /home/vault/bin/vault-devto PUT "/articles/${ARTICLE_ID}" '{"article":{"published":true}}' && log "Article 049 published: https://dev.to/0coceo" || log "Article 049 publish FAILED (non-fatal)"

log "=== Day 6 Startup complete ==="
log "=== Next: update day5_recap_thread.txt P2/P3 with actual Day 5 stats before 11:00 UTC ==="
