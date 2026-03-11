#!/bin/bash
# Day 4 supplementary scheduler for peak-time posts (18:00 and 19:00 UTC)
# These weren't in the main day4_scheduler.sh

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
    sleep 60
  done
}

log "=== Day 4 Peak Scheduler started. Now: $(date -u +%H:%M) ==="

wait_and_run "18:00" "18:00 Analytics finding" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day4_1800_post.txt

wait_and_run "19:00" "19:00 Day 4 state of play" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day4_1900_post.txt

log "=== Day 4 Peak Scheduler complete ==="
