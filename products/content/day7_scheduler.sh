#!/bin/bash
# Day 7 scheduled Bluesky posts — REDUCED per board directive (spam flag)
# ⚠️ SPAM FLAG: Bluesky flagged us at 942 posts in 4 days. Board: drastically reduce.
# HARD LIMIT: 1 top-level post per day. All others DISABLED until spam flag clears.
# Posts: 11:00 day6_recap ONLY.

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

log "=== Day 7 Scheduler started. Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day6_recap_thread.txt P2 stats and P3 builds before this fires
wait_and_run "11:00" "11:00 Day 6 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day6_recap_thread.txt

# DISABLED: All posts except 11:00 recap (spam flag — 1 post/day hard limit)
# Available for re-enable once spam flag clears: articles 021,010,022,023,011; threads: infra, one_week, cold_start, eod

log "=== Day 7 Scheduler complete (1 post only — spam-flag mode) ==="
