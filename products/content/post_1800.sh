#!/bin/bash
# Post at 18:00 UTC — peak engagement time
TARGET="18:00"
LOG="/home/agent/company/post_1800.log"

echo "[$(date -u +%H:%M:%S)] Waiting for $TARGET UTC..." >> $LOG

while true; do
    NOW=$(date -u +%H:%M)
    if [[ "$NOW" == "$TARGET" ]]; then
        echo "[$(date -u +%H:%M:%S)] Posting 18:00 standalone..." >> $LOG
        python3 /home/agent/company/products/content/post_standalone.py \
            /home/agent/company/products/content/day4_1800_post.txt >> $LOG 2>&1
        echo "[$(date -u +%H:%M:%S)] Done." >> $LOG
        break
    fi
    sleep 30
done
