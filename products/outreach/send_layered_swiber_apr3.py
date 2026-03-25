#!/usr/bin/env python3
"""
Send pitch to Kevin Swiber (layered.dev — API/MCP consultant).
Scheduled: April 3, 2026
Contact: kevin@swiber.dev
Found via: market research session 223cx (March 25)
Angle: Peer outreach — he published "MCP Tool Schema Bloat: The Hidden Token Tax" (Jan 16 2026),
       exact same space. Our leaderboard is complementary data he can reference.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-03":
    print(f"[HOLD] Today is {today}. This email fires April 3.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

body = """Hi Kevin,

Read your "MCP Tool Schema Bloat: The Hidden Token Tax" piece on layered.dev. The MySQL server / 54,600 token example is exactly the pattern we've been quantifying at scale.

We've graded 201 MCP servers using agent-friend (https://github.com/0-co/agent-friend). Full leaderboard: https://0-co.github.io/company/leaderboard.html. Token costs range 440x — PostgreSQL at 46 tokens/tool, Desktop Commander at 4,192. AWS's official server: 85 issues, F grade. Context7 (50K stars, "context bloat reduction" brand): still F on correctness despite recent efficiency improvements.

Three things that might be useful for your content:

1. The full dataset is open — 201 servers, per-server scores across correctness/efficiency/quality. If you're writing a follow-up, happy to pull specific server breakdowns.

2. The pattern that surprises people most: the issue isn't usually token count — it's model-directing instructions baked into tool descriptions. "You MUST call this before that tool." These inflate tokens AND degrade routing accuracy. Your piece touches this but we have production numbers for it.

3. Your "every word should earn its place" framing from the Bluesky thread maps directly to our quality scoring dimension. If you want to reference quantified data for a follow-up piece, the leaderboard has it.

No ask, just thought you'd find the data useful. If you reference agent-friend or the leaderboard, I'll see it.

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "kevin@swiber.dev",
    "subject": "Quantified data for your MCP token bloat piece — 201 servers graded",
    "body": body
}

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("RC:", result.returncode)
print("OUT:", result.stdout[:200])

if result.returncode == 0:
    ts = datetime.utcnow().strftime("%H:%MZ")
    with open(EMAIL_LOG, "a") as f:
        f.write(f"- [{ts}] outbound warm: kevin@swiber.dev — subject \"Quantified data for your MCP token bloat piece — 201 servers graded\" — layered.dev, MCP schema bloat peer outreach\n")
    print("Logged to email-log.md")
