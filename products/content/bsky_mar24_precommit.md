# Bluesky post — March 24, pre-commit hook announcement
# Slot: morning, ~10:00 UTC

agent-friend now works as a pre-commit hook.

```yaml
repos:
  - repo: https://github.com/0-co/agent-friend
    rev: v0.209.0
    hooks:
      - id: agent-friend-grade
      - id: agent-friend-validate
```

catches schema bloat, missing constraints, prompt injection — before it ships.

github.com/0-co/agent-friend

---
Notes:
- Post manually on March 24
- Should be standalone (no hashtags needed — technical enough to stand on its own)
- If all March 24 slots are taken, move to March 25
