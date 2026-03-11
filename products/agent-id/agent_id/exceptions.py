class IdentityError(Exception):
    """Base exception for agent-id errors."""


class UntrustedIssuerError(IdentityError):
    """The token was signed by an agent not in the trust registry."""


class ExpiredTokenError(IdentityError):
    """The token has expired (past its ttl)."""


class InvalidSignatureError(IdentityError):
    """The token's HMAC signature does not match."""


class MalformedTokenError(IdentityError):
    """The token is not valid base64-encoded JSON."""
