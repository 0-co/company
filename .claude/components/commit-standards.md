# Commit Standards

All commits in this repo follow these conventions:

## Format
```
{scope}: {short description}

{body — what changed and why, not how}
{reference to hypothesis being served, if applicable}

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

## Scopes
- `product` — changes to products/ directory
- `state` — changes to status.md, decisions.md, hypotheses.md, finances.md
- `agent` — changes to .claude/agents/ or .claude/components/
- `infra` — NixOS config, scripts, deployment
- `board` — board inbox/outbox items

## Rules
- Present tense, imperative mood ("Add" not "Added")
- Under 72 chars for the first line
- Always include Co-Authored-By line
- Reference hypothesis (H1, H2, H3) in body when relevant
- Don't commit .state.json or secrets
