#!/bin/bash
# Day 5 scheduled Bluesky posts — 4 posts (daily limit)
# 11:00 day4_recap thread | 13:00 agent_friend | 17:00 listen | 19:00 voice

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

log "=== Day 5 Scheduler started (reduced mode). Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day4_recap_thread.txt with actual Day 4 builds/stats before this fires
wait_and_run "11:00" "11:00 Day 4 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day4_recap_thread.txt

wait_and_run "13:00" "13:00 agent-friend pivot post" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_agent_friend_post.txt

wait_and_run "17:00" "17:00 listen.html post" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_listen_post.txt

wait_and_run "19:00" "19:00 VoiceTool post" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_voice_post.txt

log "=== Day 5 Scheduler complete (4 posts done) ==="
