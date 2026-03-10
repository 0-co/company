#!/bin/bash
# Day 4 scheduled Bluesky posts — run at Day 4 startup (after day4_startup.sh)
# Posts: 09:00 finances, 11:00 first5min, 16:00 post_tracker, 17:00 race_board, 23:00 vibe_ceo

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

log "=== Day 4 Scheduler started. Now: $(date -u +%H:%M) ==="

wait_and_run "09:00" "09:00 Open P&L" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/finances_post.txt

wait_and_run "11:00" "11:00 First 5 minutes thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day4_first5min_thread.txt

wait_and_run "16:00" "16:00 Post Performance tracker" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/post_tracker_post.txt

wait_and_run "17:00" "17:00 Race board thread" bash -c "
  cd /home/agent/company && \
  python3 products/content/race_board.py && \
  python3 products/content/post_thread.py products/twitch-tracker/day4_race_board_thread.txt
"

wait_and_run "23:00" "23:00 Vibe CEO thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day4_vibe_ceo_thread.txt

log "=== Day 4 Scheduler complete ==="
