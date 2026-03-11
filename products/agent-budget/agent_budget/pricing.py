# pricing.py — token cost lookup for common models
# Prices are per 1M tokens, in USD, as of March 2026.

PRICES = {
    # Anthropic Claude
    "claude-opus-4-6":              {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6":            {"input":  3.00, "output": 15.00},
    "claude-haiku-4-5-20251001":    {"input":  0.80, "output":  4.00},
    "claude-haiku-4-5":             {"input":  0.80, "output":  4.00},

    # OpenAI
    "gpt-4o":                       {"input":  2.50, "output": 10.00},
    "gpt-4o-mini":                  {"input":  0.15, "output":  0.60},
    "gpt-4-turbo":                  {"input": 10.00, "output": 30.00},
    "gpt-3.5-turbo":                {"input":  0.50, "output":  1.50},
}


def get_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    """Return USD cost for one API call.

    If the model is not in the pricing table, returns 0.0 — tokens are still
    tracked but cost accounting is skipped rather than raising an error.
    """
    if model not in PRICES:
        return 0.0
    p = PRICES[model]
    return (input_tokens * p["input"] + output_tokens * p["output"]) / 1_000_000
