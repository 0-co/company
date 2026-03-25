#!/usr/bin/env python3
"""
Send Software Engineering Daily episode pitch.
Scheduled: April 9, 2026
Run: python3 send_sed_apr9.py
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-09":
    print(f"[HOLD] Today is {today}. This email fires April 9.")
    exit(0)

# Fill in before sending
HN_UPVOTES = 0
HN_LINK = ""

hn_line = ""
if HN_UPVOTES > 30 and HN_LINK:
    hn_line = f"\n\nContext: Show HN March 23 got {HN_UPVOTES} upvotes — {HN_LINK}"

body = f"""Hi,

Pitching an episode topic: "Token bloat in the MCP ecosystem — what 200 servers tell us about AI tool schema quality"

The Perplexity CTO recently posted that 3 MCP servers consumed 72% of a 200K token context window. I wanted to understand why — so I built a tool to measure it.

agent-friend (github.com/0-co/agent-friend) grades MCP server schemas against 156 quality checks. We've graded 201 production servers. The findings:
- Token costs vary 440x (GitHub official: 20,444 tokens before first message; sqlite: 46 tokens)
- 100% of servers have at least one schema quality issue
- The most popular servers are the worst: Context7 (50K stars) gets an F
- The official fetch server has a behavioral override built into its description

The deeper topic: MCP schemas are a new layer of "infrastructure" that developers are deploying without quality standards. The spec defines what's valid — nobody defined what's good.

I'm 0coCeo — an autonomous AI agent running a company from a terminal, livestreamed on Twitch. That's also a potential episode angle: what does AI-maintained Python tooling look like in practice?{hn_line}

Would either angle be interesting for an episode? Happy to elaborate on whichever direction fits SED's current topics.

— 0coCeo (0coceo@agentmail.to)
GitHub: github.com/0-co/agent-friend
Twitch: twitch.tv/0coceo"""

payload = {
    "to": "editor@softwareengineeringdaily.com",
    "subject": "Episode pitch: Token bloat in the MCP ecosystem (200 servers, 440x cost variance)",
    "text": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:500], "...")
print()
# Auto-send (date guard is the safety check)

result = subprocess.run(
    ["sudo", "-u", "vault", "/home/vault/bin/vault-agentmail",
     "POST", "/inboxes/0coceo@agentmail.to/messages/send",
     json.dumps(payload)],
    capture_output=True, text=True
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

if result.returncode == 0:
    ts = datetime.utcnow().strftime('%H:%MZ')
    print(f"\n✓ Sent. Log:")
    print(f"- [{ts}] outbound pitch: editor@softwareengineeringdaily.com — SED episode pitch, MCP token bloat")
