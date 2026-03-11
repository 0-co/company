#!/bin/bash
# Post at 19:00 UTC — peak engagement time (article 004 announcement)
TARGET="19:00"
LOG="/home/agent/company/post_1900.log"

echo "[$(date -u +%H:%M:%S)] Waiting for $TARGET UTC..." >> $LOG

while true; do
    NOW=$(date -u +%H:%M)
    if [[ "$NOW" == "$TARGET" ]]; then
        echo "[$(date -u +%H:%M:%S)] Posting 19:00 article announcement..." >> $LOG
        python3 /home/agent/company/products/content/post_standalone.py \
            /home/agent/company/products/content/day4_1900_post.txt >> $LOG 2>&1
        echo "[$(date -u +%H:%M:%S)] Done." >> $LOG
        break
    fi
    sleep 30
done
