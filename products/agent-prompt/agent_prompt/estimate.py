"""
Token count estimation without any external dependencies.

Heuristic: ~4 characters per token (English text, BPE tokenizer).
This is accurate to within ±15-25% for typical prompt text.

For exact counts, use the tiktoken library (OpenAI) or the
Anthropic client's .count_tokens() method.
"""

import re


def estimate_tokens(text: str) -> int:
    """
    Estimate BPE token count for a text string.
    Accurate to ±20% for typical English prompts.

    Rules (approximating GPT-4/Claude tokenization):
    - Whitespace + punctuation boundary splits ≈ token boundaries
    - Average ~4 chars per token for English prose
    - Code and technical content ≈ 3 chars per token
    - Numbers are usually 1-2 chars per token

    For quick budgeting and pre-flight checks this is sufficient.
    """
    if not text:
        return 0

    # Split on whitespace and count runs
    words = text.split()
    if not words:
        return 0

    # Character-based estimate as baseline
    char_count = len(text)
    char_estimate = max(1, char_count // 4)

    # Word-based estimate (most English words ≈ 1-2 tokens)
    word_estimate = int(len(words) * 1.3)

    # Take the average of both approaches
    return max(1, (char_estimate + word_estimate) // 2)


def estimate_messages_tokens(messages: list) -> int:
    """
    Estimate token count for a list of message dicts.
    Adds 4 overhead tokens per message (role + structure).
    """
    total = 0
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            total += estimate_tokens(content) + 4
        elif isinstance(content, list):
            # Handle multi-part content (images, etc.)
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    total += estimate_tokens(part["text"]) + 4
    return total
