"""
Built-in routing rule implementations.

These are factory functions that return condition callables: (messages, **context) -> bool.
"""


def input_tokens_under(n: int):
    """Route if estimated input token count < n.

    Estimates tokens as len(all_message_text) / 4 (rough but zero-dep estimate).
    """
    def condition(messages, **context):
        total_chars = sum(len(str(m.get('content', ''))) for m in messages)
        estimated_tokens = total_chars / 4
        return estimated_tokens < n
    return condition


def input_tokens_over(n: int):
    """Route if estimated input token count >= n."""
    def condition(messages, **context):
        total_chars = sum(len(str(m.get('content', ''))) for m in messages)
        estimated_tokens = total_chars / 4
        return estimated_tokens >= n
    return condition


def last_message_under(n_chars: int):
    """Route if last user message is under n_chars characters."""
    def condition(messages, **context):
        last = messages[-1] if messages else {}
        content = str(last.get('content', ''))
        return len(content) < n_chars
    return condition


def last_message_over(n_chars: int):
    """Route if last user message is over n_chars characters."""
    def condition(messages, **context):
        last = messages[-1] if messages else {}
        content = str(last.get('content', ''))
        return len(content) > n_chars
    return condition


def message_count_under(n: int):
    """Route if conversation has fewer than n messages (short conversations)."""
    def condition(messages, **context):
        return len(messages) < n
    return condition


def message_count_over(n: int):
    """Route if conversation has n or more messages."""
    def condition(messages, **context):
        return len(messages) >= n
    return condition


def contains_keyword(*keywords: str, case_sensitive: bool = False):
    """Route if any message contains any of the given keywords."""
    def condition(messages, **context):
        text = ' '.join(str(m.get('content', '')) for m in messages)
        if not case_sensitive:
            text = text.lower()
            keywords_check = [k.lower() for k in keywords]
        else:
            keywords_check = list(keywords)
        return any(kw in text for kw in keywords_check)
    return condition


def custom(func):
    """Wrap any (messages, **context) -> bool function as a routing condition."""
    return func


def always():
    """Always matches. Use as the final/default route."""
    def condition(messages, **context):
        return True
    return condition
