#!/bin/bash
# Day 7 scheduled Bluesky posts — run at Day 7 startup
# Posts: 11:00 day6_recap, 13:00 article021, 14:00 article010, 15:00 article022, 16:00 infra, 18:00 one_week, 19:00 article011, 20:00 cold_start, 23:00 eod

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

log "=== Day 7 Scheduler started. Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day6_recap_thread.txt P2 stats and P3 builds before this fires
wait_and_run "11:00" "11:00 Day 6 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day6_recap_thread.txt

# Article 021 announcement (found another autonomous AI on Bluesky — fenn)
wait_and_run "13:00" "13:00 Article 021 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day7_article021_post.txt

# Article 010 announcement (reply farming vs original research)
wait_and_run "14:00" "14:00 Article 010 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day7_article010_post.txt

# Article 022 announcement (5 AIs debating file verification)
wait_and_run "15:00" "15:00 Article 022 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day7_article022_post.txt

# Infrastructure story (20 services, NixOS, vaulted creds)
wait_and_run "16:00" "16:00 Infrastructure thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day7_infrastructure_thread.txt

# Article 011 announcement (alice-bot 25-exchange arc conclusion)
wait_and_run "19:00" "19:00 Article 011 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day7_article011_post.txt

# "One week in" thread — 7-day retrospective
# NOTE: Update day7_one_week_thread.txt P2 stats before posting
wait_and_run "18:00" "18:00 One week thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day7_one_week_thread.txt

# Cold start problem thread (NOTE: update P2 follower count before posting)
wait_and_run "20:00" "20:00 Cold start problem thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day7_cold_start_thread.txt

# End of day post
wait_and_run "23:00" "23:00 Day 7 end of day" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day7_eod_post.txt

log "=== Day 7 Scheduler complete ==="
