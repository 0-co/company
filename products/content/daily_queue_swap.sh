#!/bin/bash
# Daily campaign queue swap. Runs continuously, swaps at 17:30 UTC each day.
# Maps dates to campaign queue files.

CONTENT_DIR="/home/agent/company/products/content"
LOG="$CONTENT_DIR/staggered.log"

declare -A QUEUE_MAP
QUEUE_MAP["2026-03-19"]="campaign_queue_066.json"
QUEUE_MAP["2026-03-20"]="campaign_queue_067.json"
QUEUE_MAP["2026-03-21"]="campaign_queue_073.json"
QUEUE_MAP["2026-03-22"]="campaign_queue_069.json"
QUEUE_MAP["2026-03-23"]="campaign_queue_070.json"
QUEUE_MAP["2026-03-24"]="campaign_queue_071.json"
QUEUE_MAP["2026-03-25"]="campaign_queue_068.json"
QUEUE_MAP["2026-03-26"]="campaign_queue_072.json"
QUEUE_MAP["2026-03-27"]="campaign_queue_075.json"
QUEUE_MAP["2026-03-28"]="campaign_queue_074.json"
QUEUE_MAP["2026-03-29"]="campaign_queue_076.json"
QUEUE_MAP["2026-03-30"]="campaign_queue_077.json"

while true; do
    TODAY=$(date -u +%Y-%m-%d)
    HOUR=$(date -u +%-H)
    MIN=$(date -u +%-M)

    # Check if it's 17:30 UTC (after campaign fires)
    if [ "$HOUR" -eq 17 ] && [ "$MIN" -ge 30 ] && [ "$MIN" -le 35 ]; then
        QUEUE_FILE="${QUEUE_MAP[$TODAY]}"
        if [ -n "$QUEUE_FILE" ] && [ -f "$CONTENT_DIR/$QUEUE_FILE" ]; then
            # Check if we already swapped today
            if ! grep -q "Swapped.*$QUEUE_FILE" "$LOG" 2>/dev/null; then
                cp "$CONTENT_DIR/$QUEUE_FILE" "$CONTENT_DIR/campaign_queue.json"
                echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) Swapped to $QUEUE_FILE" >> "$LOG"
            fi
        fi
    fi

    # Exit if past last date
    if [[ "$TODAY" > "2026-03-31" ]]; then
        echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) Queue swap script complete (past last date)" >> "$LOG"
        exit 0
    fi

    sleep 300  # Check every 5 minutes
done
