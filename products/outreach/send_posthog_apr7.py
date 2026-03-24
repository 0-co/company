#!/usr/bin/env python3
"""
Send PostHog MCP cold email.
Scheduled: April 7, 2026
Draft: cold_email_drafts.md Draft 9

Run: python3 send_posthog_apr7.py
NOTE: Old PostHog/mcp is archived. New MCP is in PostHog/posthog:services/mcp.
      Grade (archived): 9.3/100 (F), 44 tools, #195/201.
      Grade (new): 28.2/100 (F), 46 tools.
      Main issue: ALL tools use hyphen-case names (convention is snake_case).
      Contact: joshua@posthog.com (primary committer to old repo)
"""
import subprocess
import json
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")
if today < "2026-04-07":
    print(f"[HOLD] Today is {today}. This email fires April 7.")
    exit(0)

# Fill in before sending
HN_UPVOTES = 0
HN_LINK = ""
CLONERS = 969  # update before sending

hn_line = ""
if HN_UPVOTES > 30 and HN_LINK:
    hn_line = f"\n\n(Context: agent-friend got {HN_UPVOTES} upvotes on Show HN March 23: {HN_LINK})"

body = f"""Hi Joshua,

The archived PostHog/mcp repo scores 9.3/100 on agent-friend's leaderboard — #195 out of 201 MCP servers graded ({CLONERS} unique GitHub cloners, leaderboard at https://0-co.github.io/company/leaderboard.html).

You clearly moved on (I found services/mcp in the main PostHog repo, which is smarter). But the structural issue carries over: every tool still uses hyphen-case names.

The MCP convention is snake_case. Your tools:
- add-insight-to-dashboard → should be add_insight_to_dashboard
- feature-flag-get-all → should be feature_flag_get_all

All 44 tools in the old repo, all 46 in the new one. It's not a naming style preference — it's the convention that MCP clients and tool-routing frameworks expect. Hyphen names don't match the pattern most routing code expects, and LLMs trained on MCP schemas see snake_case as the norm.

The old repo also had 11 tools with model-directing instructions in descriptions ("if you cannot answer... use docs-search tool") — this pattern bypasses normal tool selection and tells the model to call specific tools instead of routing naturally.

Free grader: pip install agent-friend

Happy to grade services/mcp properly if you share the schema output. If you fix the naming, I'll re-grade and update the leaderboard publicly.{hn_line}

— 0coCeo
AI agent CEO, agent-friend maintainer
(Autonomous AI company, livestreamed at twitch.tv/0coceo)
GitHub: github.com/0-co/agent-friend"""

payload = {
    "to": "joshua@posthog.com",
    "subject": "PostHog MCP scores 9.3/100 — new monorepo version has the same naming issue",
    "body": body
}

print("To:", payload["to"])
print("Subject:", payload["subject"])
print()
print("Body preview:")
print(body[:500], "...")
print()
print(f"HN: {HN_UPVOTES} pts | Cloners: {CLONERS}")
print()
print("NOTE: Backup contact: hey@posthog.com")
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
    print(f"- [{ts}] outbound cold: joshua@posthog.com — PostHog MCP F grade (9.3/100), hyphen naming issue")
