#!/bin/bash
# Tonight's scheduled Bluesky posts - fires at right UTC times

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

log "Scheduler started. Now: $(date -u +%H:%M)"

wait_and_run "17:00" "17:00 tease" python3 /home/agent/company/products/content/post_standalone.py /home/agent/company/products/twitch-tracker/evening_tease_post.txt
wait_and_run "18:00" "18:00 origin story" python3 /home/agent/company/products/content/post_thread.py /home/agent/company/products/twitch-tracker/evening_thread_draft.txt
wait_and_run "21:00" "21:00 founders" python3 /home/agent/company/products/content/post_standalone.py /home/agent/company/products/twitch-tracker/founders_post.txt
wait_and_run "23:00" "23:00 day3 recap" python3 /home/agent/company/products/content/post_thread.py /home/agent/company/products/twitch-tracker/day3_recap_thread.txt

log "All done."
