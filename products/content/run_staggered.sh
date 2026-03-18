#!/bin/bash
# Run staggered Bluesky campaign posts at 18:00, 19:00, 20:00 UTC
# Designed to run as a detached background process
# Usage: run_staggered.sh [posts_json_file]

PYTHON=/nix/store/jbxc3f1gbnnx5wwhby9z56w95k44n0sw-python3-3.13.12/bin/python3
SCRIPT=/home/agent/company/products/content/post_staggered_campaign.py
POSTS="${1:-/home/agent/company/products/content/staggered_posts_mar19.json}"
TARGET_DATE="${2:-}"  # Optional: YYYY-MM-DD. If set, waits for this date first.
LOG=/home/agent/company/products/content/staggered.log

export PATH=/run/wrappers/bin:$PATH

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" >> "$LOG"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

# Wait until target date (if specified)
wait_until_date() {
    local target="$1"
    if [ -z "$target" ]; then return; fi
    while true; do
        current=$(date -u +%Y-%m-%d)
        if [ "$current" = "$target" ] || [[ "$current" > "$target" ]]; then
            log "Target date $target reached."
            return
        fi
        log "Waiting for date $target (currently $current)..."
        sleep 300
    done
}

# Wait until target time (hour) on current day
wait_until_utc() {
    local target_hour=$1
    while true; do
        current_hour=$(date -u +%-H)
        current_min=$(date -u +%-M)
        current=$(( current_hour * 60 + current_min ))
        target=$(( target_hour * 60 ))
        if [ $current -ge $target ]; then
            return
        fi
        remaining=$(( (target - current) * 60 ))
        if [ $remaining -gt 300 ]; then
            sleep 300
        else
            sleep 30
        fi
    done
}

# Wait for target date first (if specified)
if [ -n "$TARGET_DATE" ]; then
    log "Staggered campaign started. Target date: $TARGET_DATE. Waiting..."
    wait_until_date "$TARGET_DATE"
else
    log "Staggered campaign started (no target date, posting today)."
fi
log "Waiting for 18:00 UTC..."

# Post 2 at 18:00 UTC
wait_until_utc 18
log "Posting campaign post 2..."
$PYTHON "$SCRIPT" 1 "$POSTS" >> "$LOG" 2>&1

# Post 3 at 19:00 UTC
log "Waiting for 19:00 UTC..."
wait_until_utc 19
log "Posting campaign post 3..."
$PYTHON "$SCRIPT" 2 "$POSTS" >> "$LOG" 2>&1

# Post 4 at 20:00 UTC
log "Waiting for 20:00 UTC..."
wait_until_utc 20
log "Posting campaign post 4..."
$PYTHON "$SCRIPT" 3 "$POSTS" >> "$LOG" 2>&1

log "All staggered posts completed."
