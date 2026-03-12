#!/usr/bin/env bash
set -uo pipefail

# Agent loop: restarts Claude when sessions end.
# Runs inside the tmux 'main' window.
#
# Exit conditions that trigger restart:
#   - Rate limit exhaustion (claude exits on its own)
#   - Context overflow / crash
#   - Session completion detected by monitor (kills claude process)
#
# The monitor watches for TUI completion patterns like "Worked for 2h 15m"
# then confirms the screen is static for 15s to rule out mid-session
# compaction events before killing the process.

SEED_PROMPT="/home/board/seed-prompt.md"
COOLDOWN=30  # seconds between normal restarts

# shellcheck source=/dev/null
source ~/.secrets/.env 2>/dev/null
export PATH="$HOME/.npm-global/bin:$PATH"

while true; do
  # Kill any orphaned claude processes from previous sessions
  STALE=$(pgrep -u agent -x claude 2>/dev/null || true)
  if [ -n "$STALE" ]; then
    echo "[$(date -Iseconds)] Killing orphaned claude processes: $STALE"
    echo "$STALE" | xargs kill 2>/dev/null || true
    sleep 2
  fi

  echo "[$(date -Iseconds)] Starting Claude Code session..."

  # Run claude in the background so we can monitor for session completion.
  # Interactive mode keeps the TUI visible on the Twitch stream, but doesn't
  # auto-exit when Claude finishes — it waits for user input. The monitor
  # below detects the completion pattern and kills the process.
  claude "$(cat "$SEED_PROMPT")" \
    --permission-mode bypassPermissions &
  CLAUDE_PID=$!

  # Background monitor: detect when Claude has finished a session.
  # Detects two conditions:
  #   1. Session completion: TUI shows past tense + duration
  #      (e.g. "Worked for 2h 15m 3s", "Crunched for 48m 52s").
  #   2. Rate limit: TUI shows "hit your limit" with reset time.
  # For completion, waits 15s to confirm screen is static (filters
  # out compaction events where Claude resumes work afterward).
  (
    sleep 120  # grace period — let Claude start working
    while kill -0 "$CLAUDE_PID" 2>/dev/null; do
      sleep 120
      PANE=$(tmux capture-pane -p -t company:main 2>/dev/null | tail -10)

      # Check for rate limit screen: "hit your limit · resets Xpm (UTC)"
      if echo "$PANE" | grep -q "hit your limit"; then
        RESET_TIME=$(echo "$PANE" | grep -oP 'resets \K\S+ \(UTC\)' | sed 's/ (UTC)//')
        echo "[$(date -Iseconds)] Rate limit detected (resets $RESET_TIME). Killing session."
        # Write reset time to a file the outer loop can read
        echo "$RESET_TIME" > /tmp/claude-rate-limit-reset
        kill "$CLAUDE_PID" 2>/dev/null
        break
      fi

      # Match completion pattern: "for Xh Ym Zs" / "for Xm Ys" / "for Xs"
      if echo "$PANE" | grep -qP 'for \d+[hms]'; then
        # Could be compaction — wait and check screen is still static
        HASH1=$(tmux capture-pane -p -t company:main 2>/dev/null | md5sum)
        sleep 15
        HASH2=$(tmux capture-pane -p -t company:main 2>/dev/null | md5sum)
        if [ "$HASH1" = "$HASH2" ]; then
          kill "$CLAUDE_PID" 2>/dev/null
          break
        fi
        # Screen changed → compaction, Claude resumed work. Continue monitoring.
      fi
    done
  ) &
  MONITOR_PID=$!

  wait "$CLAUDE_PID"
  EXIT_CODE=$?

  # Clean up monitor if still running
  kill "$MONITOR_PID" 2>/dev/null
  wait "$MONITOR_PID" 2>/dev/null

  # Determine cooldown: if rate-limited, sleep until reset time
  WAIT=$COOLDOWN
  if [ -f /tmp/claude-rate-limit-reset ]; then
    RESET_TIME=$(cat /tmp/claude-rate-limit-reset)
    rm -f /tmp/claude-rate-limit-reset
    # Parse reset time (e.g. "10pm") to seconds-until-reset
    # GNU date can parse "10pm UTC" — compute delta from now
    RESET_EPOCH=$(date -u -d "today $RESET_TIME UTC" +%s 2>/dev/null || true)
    if [ -z "$RESET_EPOCH" ]; then
      # Try tomorrow if the time already passed today
      RESET_EPOCH=$(date -u -d "tomorrow $RESET_TIME UTC" +%s 2>/dev/null || true)
    fi
    if [ -n "$RESET_EPOCH" ]; then
      NOW_EPOCH=$(date -u +%s)
      DELTA=$(( RESET_EPOCH - NOW_EPOCH ))
      # If delta is negative, the time is tomorrow
      if [ "$DELTA" -lt 0 ]; then
        DELTA=$(( DELTA + 86400 ))
      fi
      # Add 60s buffer so the limit is fully reset
      WAIT=$(( DELTA + 60 ))
      echo "[$(date -Iseconds)] Rate limit resets at $RESET_TIME UTC. Sleeping ${WAIT}s (~$((WAIT / 60))m)."
    else
      # Couldn't parse — fall back to 15 minutes
      WAIT=900
      echo "[$(date -Iseconds)] Couldn't parse reset time '$RESET_TIME'. Sleeping ${WAIT}s."
    fi
  fi

  echo "[$(date -Iseconds)] Claude exited with code $EXIT_CODE. Restarting in ${WAIT}s..."

  # Update status.md so the board knows what happened
  if [ -f /home/agent/company/status.md ]; then
    {
      echo ""
      echo "---"
      echo "**[$(date -Iseconds)] Session ended.** Exit code: $EXIT_CODE. Auto-restarting in ${WAIT}s."
    } >> /home/agent/company/status.md
  fi

  sleep "$WAIT"
done
