#!/usr/bin/env python3
"""
Send personalized review to OKX agent-trade-kit team.
Scheduled: April 27, 2026
Contact: shaolong.wang@okg.com (lead architect based on commit history)
Found via: market research session 223cx (March 25)
Context: OKX has a full internal MCP design guideline (docs/mcp-design-guideline.md)
         including token budget (25,000 token cap), estimation formulas, and a Reviewer Checklist.
         They're doing MANUALLY what agent-friend does automatically.
Angle: Peer outreach — you built an internal process for exactly this problem.
       We built a CLI that automates it. Here's how your server scores.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-27":
    print(f"[HOLD] Today is {today}. This email fires April 27.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi Shaolong,

I was reading through your docs/mcp-design-guideline.md and your token budget framework (Section 4) is the best internal MCP quality process I've seen in the wild.

Your breakdown is accurate: JSON structure is ~48% of schema tokens, descriptions ~40%. Your formula (80 + 15×params + description_chars/4) maps closely to what we measure across 201 public MCP servers. The 25,000 token cap and 18,500/6,500 split is good engineering discipline.

We built agent-friend to automate exactly what your Reviewer Checklist does manually:

```
pip install agent-friend
agent-friend audit your-tools.json
```

Output: per-tool token counts, compression suggestions, naming checks, total token budget at-a-glance. The same data your Section 4.2 formula estimates, but exact rather than approximate.

Two things from your guideline that we've also found in production data:
1. "Description字符数 / 4" is the dominant variable — one verbose description can account for more tokens than 10 compact ones
2. Your "降级到 CLI-only" strategy (moving low-frequency tools out of MCP) is exactly the right call for the worst offenders — we flag these in `agent-friend optimize`

Leaderboard of 201 graded servers (for comparison): https://0-co.github.io/company/leaderboard.html

No ask — I just thought a team that's built this level of internal process around the problem would find the external tool useful.

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "shaolong.wang@okg.com",
    "subject": "Your mcp-design-guideline.md — agent-friend automates your Section 4 manually",
    "body": body
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("RC:", result.returncode)
print("OUT:", result.stdout[:300])

if result.returncode == 0:
    ts = datetime.utcnow().strftime("%H:%MZ")
    with open(EMAIL_LOG, "a") as f:
        f.write(f"- [{ts}] outbound warm: shaolong.wang@okg.com — subject \"Your mcp-design-guideline.md — agent-friend automates your Section 4 manually\" — OKX agent-trade-kit, personalized schema review, token budget angle\n")
    print("Logged to email-log.md")
else:
    print("STDERR:", result.stderr[:200])
