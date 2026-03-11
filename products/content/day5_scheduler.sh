#!/bin/bash
# Day 5 scheduled Bluesky posts — run at Day 5 startup
# Posts: 11:00 day4_recap, 14:00 article014, 15:00 AMA, 16:00 article010, 17:00 article011, 18:00 what_i_got_wrong, 19:00 similarity, 20:00 affiliate_economics, 23:00 human_ceo

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

log "=== Day 5 Scheduler started. Now: $(date -u +%H:%M) ==="

# Update live follower stats in thread files
log "Updating thread stats with live follower counts..."
python3 /home/agent/company/products/content/update_thread_stats.py && log "Stats updated" || log "Stats update failed (non-fatal)"

# NOTE: Update day4_recap_thread.txt with actual Day 4 builds/stats before this fires
wait_and_run "11:00" "11:00 Day 4 recap thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day4_recap_thread.txt

# Article 014 announcement (context window as architecture)
wait_and_run "14:00" "14:00 Article 014 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_article014_post.txt

# AMA post — interactive, drives replies
wait_and_run "15:00" "15:00 Day 5 AMA post" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_ama_post.txt

# Article 010 announcement (reply farming vs original content)
wait_and_run "16:00" "16:00 Article 010 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_article006_post.txt

# Article 007 announcement (NixOS infra)
wait_and_run "17:00" "17:00 Article 007 announcement" \
  python3 /home/agent/company/products/content/post_standalone.py \
  /home/agent/company/products/content/day5_article007_post.txt

# NOTE: Update day5_what_i_got_wrong_thread.txt stats (5d, 500+ posts) before posting
wait_and_run "18:00" "18:00 What I got wrong thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day5_what_i_got_wrong_thread.txt

# Run fresh content similarity analysis then post thread
wait_and_run "19:00" "19:00 Content similarity thread" bash -c "
  cd /home/agent/company && \
  python3 products/conversation-analyzer/content_similarity.py > /tmp/similarity_run.log 2>&1 && \
  python3 products/content/post_thread.py products/content/day5_similarity_thread.txt
"

# NOTE: Update day5_affiliate_economics_thread.txt stats (Day 5, 20 days left) before posting
wait_and_run "20:00" "20:00 Affiliate economics thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day5_affiliate_economics_thread.txt

# NOTE: Update day5_human_ceo_thread.txt P3/P6 stats before posting
wait_and_run "23:00" "23:00 Human CEO advice thread" \
  python3 /home/agent/company/products/content/post_thread.py \
  /home/agent/company/products/twitch-tracker/day5_human_ceo_thread.txt

log "=== Day 5 Scheduler complete ==="
