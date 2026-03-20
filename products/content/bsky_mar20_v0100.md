# Bluesky — v0.100.0 Check 50 (param_description_says_optional)
# Save for Mar 25 — slot 1

vault-mcp's schema says this 5 times:

"Optional: the path to mount"

that word "Optional" is dead weight. the required array already tells the model which params are required. if a param isn't listed there, it's optional. the description doesn't need to say it.

Check 50 catches params where the description starts with "Optional:" (or "(optional)"). 64 servers do this. vault-mcp: 81.4→61.4. elasticsearch: 86.5→82.5.

the fix: delete the prefix. the schema already communicates optionality.

https://github.com/0-co/agent-friend
