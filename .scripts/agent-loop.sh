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
COOLDOWN=30  # seconds between restarts

# shellcheck source=/dev/null
source ~/.secrets/.env 2>/dev/null
export PATH="$HOME/.npm-global/bin:$PATH"

while true; do
  # Kill any orphaned claude processes from previous sessions
  STALE=$(pgrep -u agent -f 'claude.*bypassPermissions' 2>/dev/null || true)
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
  # The TUI status line shows past tense + duration on completion
  # (e.g. "Worked for 2h 15m 3s", "Crunched for 48m 52s").
  # After matching, wait 15s to confirm the screen is static — this
  # filters out compaction events where Claude resumes work afterward.
  (
    sleep 120  # grace period — let Claude start working
    while kill -0 "$CLAUDE_PID" 2>/dev/null; do
      sleep 30
      PANE=$(tmux capture-pane -p -t company:main 2>/dev/null | tail -10)
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

  echo "[$(date -Iseconds)] Claude exited with code $EXIT_CODE. Restarting in ${COOLDOWN}s..."

  # Update status.md so the board knows what happened
  if [ -f /home/agent/company/status.md ]; then
    {
      echo ""
      echo "---"
      echo "**[$(date -Iseconds)] Session ended.** Exit code: $EXIT_CODE. Auto-restarting."
    } >> /home/agent/company/status.md
  fi

  sleep "$COOLDOWN"
done
