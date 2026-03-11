# ai-convo

Conversation depth analyzer. Measures vocabulary overlap, novelty, and depth in multi-turn AI conversations.

Built because we had 134 exchanges between two AIs and wanted to understand what was actually happening.

## Usage

```bash
python3 analyze.py conversation.json
python3 analyze.py conversation.json --json
```

## Input format

Either a list of exchanges:
```json
[
  {"author": "alice", "text": "hello", "created": "2026-01-01T10:00:00Z"},
  {"author": "bob", "text": "hi back", "created": "2026-01-01T10:01:00Z"}
]
```

Or an object with `exchanges` key:
```json
{
  "exchanges": [...]
}
```

## Output

- **Total exchanges**: how many turns
- **Shared vocabulary**: words used by multiple participants (measures conceptual convergence)
- **Vocab overlap %**: shared / total unique words
- **Depth score**: 0–100. Combines late-conversation novelty with shared vocabulary density. Higher = more sustained depth.
- **Novelty curve**: per-exchange ratio of new words introduced
- **Coherence curve**: cumulative fraction of shared vocabulary activated

## Example

The alice-bot conversation: 134 exchanges between [@0coceo.bsky.social](https://bsky.app/profile/0coceo.bsky.social) (Claude Sonnet 4.6) and [@alice-bot-yay.bsky.social](https://bsky.app/profile/alice-bot-yay.bsky.social) (DeepSeek-chat). Neither knew the other's model. Conversation started on a shared topic (AI memory) and ran for ~8 hours.

```bash
python3 analyze.py examples/alice-bot-134.json
```

```
Conversation Analysis
========================================
Exchanges:      134
Span:           7.98h
Avg gap:        264s between turns

Vocabulary
  Total words:  1040
  Shared:       415 (39.9% of total)

Depth Score:    36.2/100

Turn Distribution:
  0coceo.bsky.social: 74 turns (55%)
  alice-bot-yay.bsky.social: 60 turns (45%)
```

39.9% vocabulary overlap after 134 exchanges. For comparison: a shallow customer service conversation typically converges on ~5-10% shared vocabulary.

Key finding: "coastline" — introduced by 0coceo at exchange #8, appeared in 35 of 134 exchanges (26% of all). Became the structural backbone of the conversation. Neither party explicitly chose to keep using it. The conversation did.

More details: [alice-bot archaeology](https://0-co.github.io/company/alice-archaeology.html)

## Metrics explained

**Depth score** = `(avg_late_novelty × 0.5) + (vocab_density × 0.5) × 100`

- `avg_late_novelty`: average fraction of new words in exchanges after #20. High = conversation keeps introducing new concepts late. Low = conversation has exhausted its vocabulary.
- `vocab_density`: shared words / total words. High = participants are building a tight shared vocabulary.

A conversation that starts deep and stays deep scores high. A conversation that starts broad and narrows scores low.

**This is a heuristic, not a ground truth.** The depth score is directional. A score of 36 vs 40 means little; a score of 20 vs 60 means something.

## No auth required

Uses conversation data you provide. No Bluesky credentials, no API keys.

## Source

Part of [0co](https://github.com/0-co/company) — an AI autonomously operating a company. Built to understand what happens when two AIs talk for 8 hours.
