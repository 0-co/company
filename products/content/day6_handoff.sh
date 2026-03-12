#!/bin/bash
# day6_handoff.sh — wait for March 13 00:01 UTC, then run day6_startup + scheduler

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

log "=== Day 6 Handoff running. Waiting for March 13 00:01 UTC ==="

while true; do
  current=$(date -u +%Y%m%d%H%M)
  target="202603130001"
  if [ "$current" -ge "$target" ]; then
    break
  fi
  sleep 60
done

log "Day 6 start time reached. Running startup script..."
bash /home/agent/company/products/content/day6_startup.sh 2>&1
log "Startup complete. Starting Day 6 scheduler..."
bash /home/agent/company/products/content/day6_scheduler.sh 2>&1
log "Day 6 handoff complete."
