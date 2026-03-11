"""
Exceptions for agent-retry.
"""


class RetryExhausted(Exception):
    """
    Raised when all retry attempts have failed.

    Attributes:
        attempts: Number of attempts made.
        last_exception: The exception from the final attempt.
    """

    def __init__(self, attempts: int, last_exception: Exception) -> None:
        self.attempts = attempts
        self.last_exception = last_exception
        super().__init__(
            f"All {attempts} attempt(s) failed. "
            f"Last error: {type(last_exception).__name__}: {last_exception}"
        )
