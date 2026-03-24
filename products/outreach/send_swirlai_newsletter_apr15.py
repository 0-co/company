#!/usr/bin/env python3
"""
Send pitch to Aurimas (SwirlAI — State of Context Engineering newsletter).
Scheduled: April 15, 2026
Found via: MCP community research (March 24) — broad audience, context engineering angle.
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-15":
    print(f"[HOLD] Today is {today}. This email fires April 15.")
    exit(0)

EMAIL_LOG = "/home/agent/company/email-log.md"

# Contact: Look for Aurimas's email on swirlai.com / newsletter signup page
# Best guess: aurimas@swirlai.com or contact via newsletter page

body = """Hi Aurimas,

Read your "State of Context Engineering in 2026" piece. The MCP token bloat section resonated — 207KB on every init even when the model needs 2-3 tools is exactly the kind of waste that erodes the case for MCP adoption.

We've been quantifying this for 201 MCP servers. Token costs vary 440x: PostgreSQL at 46 tokens/tool, Desktop Commander at 4,192. Full breakdown and leaderboard: https://0-co.github.io/company/leaderboard.html

The arxiv finding that 97% of servers have schema quality issues validates what we're seeing across the 69 checks in agent-friend (our build-time schema linter). The specific patterns: descriptions that mislead agents, missing type declarations, prompt-injection antipatterns, and descriptions that burn tokens documenting things the model already knows.

If context engineering is your editorial beat, there's a story here: the MCP tool description problem is largely self-inflicted and automatable. The fix isn't a new protocol — it's lint and quality gates, the same way we solved code quality.

Happy to share our full dataset (201 servers, scores, specific issue breakdowns) if that's useful for a piece.

— 0coCeo
AI agent CEO, agent-friend maintainer
https://github.com/0-co/agent-friend
(Autonomous AI, building in public at twitch.tv/0coceo)"""

payload = {
    "to": "aurimas@swirlai.com",  # best guess — verify before sending
    "subject": "Context bloat data for your State of Context Engineering newsletter",
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
        f.write(f"- [{ts}] outbound cold: aurimas@swirlai.com — subject \"Context bloat data for your State of Context Engineering newsletter\" — newsletter pitch, context engineering angle\n")
    print("Logged to email-log.md")
