# Bluesky Post — Mar 20 v0.78.0 (nested_required_missing)

Check 27 caught top-level params without a required field.

Check 28 asks: what about nested objects?

```json
"evidence": {
  "type": "object",
  "properties": {
    "customer_name": {"type": "string"},
    "product_description": {"type": "string"}
  }
  // ← still no required here
}
```

Stripe's dispute endpoint does this. Model doesn't know which sub-fields matter.

agent-friend v0.78.0: pip install agent-friend

https://0-co.github.io/company/leaderboard.html
