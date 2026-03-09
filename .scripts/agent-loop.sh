#!/usr/bin/env bash
set -uo pipefail

# Agent loop: restarts Claude when sessions end.
# Runs inside the tmux 'main' window.
#
# Exit conditions that trigger restart:
#   - Rate limit exhaustion (claude exits)
#   - Context overflow / crash
#   - Any unexpected exit
#
# Each session runs claude -p with the seed prompt, which executes
# non-interactively and exits when done. This script restarts it.

SEED_PROMPT="/home/board/seed-prompt.md"
COOLDOWN=30  # seconds between restarts

# shellcheck source=/dev/null
source ~/.secrets/.env 2>/dev/null
export PATH="$HOME/.npm-global/bin:$PATH"

while true; do
  echo "[$(date -Iseconds)] Starting Claude Code session..."

  # Run claude in the background so we can monitor for session completion.
  # Interactive mode keeps the TUI visible on the Twitch stream, but doesn't
  # auto-exit when Claude finishes — it waits for user input. The monitor
  # below detects the completion pattern and sends /exit.
  claude "$(cat "$SEED_PROMPT")" \
    --permission-mode bypassPermissions &
  CLAUDE_PID=$!

  # Background monitor: watch for session completion pattern
  (
    while kill -0 "$CLAUDE_PID" 2>/dev/null; do
      sleep 60
      PANE_OUTPUT=$(tmux capture-pane -p -t company:main 2>/dev/null | tail -5)
      if echo "$PANE_OUTPUT" | grep -q "Worked for"; then
        sleep 5  # let Claude finish writing summary
        tmux send-keys -t company:main "/exit" Enter
        break
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
