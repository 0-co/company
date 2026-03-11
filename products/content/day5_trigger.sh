#!/bin/bash
# Waits until midnight UTC March 12, then runs Day 5 startup + scheduler
# Run: nohup bash products/content/day5_trigger.sh > day5_trigger.log 2>&1 &

log() { echo "[$(date -u +%H:%M:%S)] $*"; }

log "=== Day 5 trigger started. Now: $(date -u '+%Y-%m-%d %H:%M') ==="

TARGET="20260312 00:01"
TARGET_EPOCH=$(date -u -d "$TARGET" +%s 2>/dev/null || date -j -f "%Y%m%d %H:%M" "$TARGET" +%s)

while true; do
    NOW_EPOCH=$(date -u +%s)
    if [ "$NOW_EPOCH" -ge "$TARGET_EPOCH" ]; then
        log "Target time reached. Running Day 5 startup..."
        break
    fi
    REMAINING=$((TARGET_EPOCH - NOW_EPOCH))
    log "Waiting... ${REMAINING}s until Day 5 ($(date -u -d "@$TARGET_EPOCH" '+%Y-%m-%d %H:%M' 2>/dev/null))"
    sleep 60
done

# Run Day 5 startup
log "Running day5_startup.sh..."
cd /home/agent/company
bash products/content/day5_startup.sh && log "Startup complete" || log "Startup FAILED"

# Start Day 5 scheduler
log "Starting day5_scheduler.sh..."
nohup bash products/content/day5_scheduler.sh > /home/agent/company/day5_scheduler.log 2>&1 &
log "Day 5 scheduler PID: $!"

log "=== Day 5 trigger complete ==="
