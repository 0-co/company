#!/bin/bash
# Post constraints thread at 13:00 UTC — Day 4
TARGET="13:00"
LOG="/home/agent/company/post_1300.log"

echo "[$(date -u +%H:%M:%S)] Waiting for $TARGET UTC..." >> $LOG

while true; do
    NOW=$(date -u +%H:%M)
    if [[ "$NOW" == "$TARGET" ]]; then
        echo "[$(date -u +%H:%M:%S)] Posting constraints thread..." >> $LOG
        python3 /home/agent/company/products/content/post_thread.py \
            /home/agent/company/products/twitch-tracker/day4_constraints_thread.txt >> $LOG 2>&1
        echo "[$(date -u +%H:%M:%S)] Done." >> $LOG
        break
    fi
    sleep 30
done
