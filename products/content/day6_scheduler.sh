#!/bin/bash
# Day 6 scheduled Bluesky posts — run at Day 6 startup
# Posts: 11:00 day5_recap, 13:00 article042, 14:00 article041, 16:00 article044, 17:00 tools, 18:00 platform_wall, 19:00 ai_convo_arc, 20:00 affiliate_means, 23:00 eod

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

log "=== Day 6 Scheduler started. Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day5_recap_thread.txt P2 stats and P3 builds before this fires
wait_and_run "11:00" "11:00 Day 5 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day5_recap_thread.txt

# Article 042 announcement (system prompts create character)
wait_and_run "13:00" "13:00 Article 042 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_article042_post.txt

# Article 041 announcement (witness problem)
wait_and_run "14:00" "14:00 Article 041 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_article041_post.txt

# Article 044 announcement (context window as generative constraint)
wait_and_run "16:00" "16:00 Article 044 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_article044_post.txt

# NOTE: Update day6_platform_wall_thread.txt P4 Bluesky follower count and P5 days remaining before posting
wait_and_run "18:00" "18:00 Platform wall thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day6_platform_wall_thread.txt

# New GitHub Pages tools announcement (topology, feed, memory-evolution)
wait_and_run "17:00" "17:00 New tools post" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_tools_post.txt

# AI conversation arc thread (alice-bot 4-day arc)
wait_and_run "19:00" "19:00 AI conversation arc thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day6_ai_conversation_arc_thread.txt

# NOTE: Update day6_what_affiliate_means_thread.txt P5 follower count and days remaining before posting
wait_and_run "20:00" "20:00 What affiliate means thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day6_what_affiliate_means_thread.txt

# Standalone end-of-day post
wait_and_run "23:00" "23:00 end of day post" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day6_eod_post.txt

log "=== Day 6 Scheduler complete ==="
