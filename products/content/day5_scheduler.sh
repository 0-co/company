#!/bin/bash
# Day 5 scheduled Bluesky posts — REDUCED per board directive (spam flag)
# Original: 11 posts. Reduced to 1 post per board: "drastically reduce posting frequency"
# Posts: 11:00 day4_recap ONLY

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

wait_and_run() {
  local target="$1"
  local label="$2"
  shift 2
  while true; do
    current=$(date -u +%H%M)
    target_fmt=$(echo "$target" | tr -d ':')
    if [ "$current" -ge "$target_fmt" ]; then
      log "POSTING: $label"
      "$@"
      log "DONE: $label"
      break
    fi
    sleep 30
  done
}

log "=== Day 5 Scheduler started (reduced mode). Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day4_recap_thread.txt with actual Day 4 builds/stats before this fires
wait_and_run "11:00" "11:00 Day 4 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day4_recap_thread.txt

# All other posts DISABLED per board directive (spam flag on Bluesky)
# Previous schedule: 12:00 article045, 13:00 article041, 14:00 article040, 15:00 AMA,
# 16:00 article006, 17:00 article044, 18:00 what_i_got_wrong, 19:00 similarity,
# 20:00 affiliate_economics, 23:00 human_ceo

log "=== Day 5 Scheduler complete (reduced mode — 1 post only) ==="
