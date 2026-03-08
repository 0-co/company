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

  cat "$SEED_PROMPT" | claude -p - --dangerously-skip-permissions
  EXIT_CODE=$?

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
