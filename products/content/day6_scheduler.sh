#!/bin/bash
# Day 6 scheduled Bluesky posts — 4 posts (daily limit)
# 11:00 day5_recap thread | 13:00 article053 | 17:00 open source | 19:00 TBD

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

log "=== Day 6 Scheduler started. Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day5_recap_thread.txt P2 stats and P3 builds before this fires
wait_and_run "11:00" "11:00 Day 5 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day5_recap_thread.txt

wait_and_run "13:00" "13:00 article053 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_article053_post.txt

wait_and_run "17:00" "17:00 agent-friend open source" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_open_source_post.txt

log "=== Day 6 Scheduler complete (3 posts — recap + article053 + open source) ==="
