"""AgentIdentity: core identity, signing, and verification."""

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from pathlib import Path
from typing import Any

from .exceptions import (
    ExpiredTokenError,
    InvalidSignatureError,
    MalformedTokenError,
    UntrustedIssuerError,
)


class AgentIdentity:
    """
    A named identity for an AI agent.

    Each identity has:
    - A name (human-readable, used in tokens and audit logs)
    - A secret key (HMAC-SHA256, 256 bits, auto-generated or loaded from file)
    - A trust registry (set of agent names → their exported public keys)
    - An append-only audit log

    Key design decisions:
    - Symmetric HMAC (not asymmetric Ed25519) to stay zero-dependency.
      For the primary threat model (prompt injection in same deployment),
      shared secrets between agents in the same trust boundary are correct.
    - Keys are stored as raw hex in files, not encrypted. Protect the key
      directory with filesystem permissions (chmod 700), not this library.
    - Tokens are compact: base64url(json_payload) + "." + base64url(hmac_sig)
    """

    def __init__(
        self,
        name: str,
        key_file: str | None = None,
        audit_log: str | None = None,
        default_ttl: int = 300,
    ):
        """
        Args:
            name: Human-readable name for this agent. Used as the issuer in tokens.
            key_file: Path to persist the secret key. Created on first use with a
                      random key. If None, key lives only in memory (not persistent).
            audit_log: Path to append-only JSON Lines audit log. If None, logging
                       is disabled.
            default_ttl: Default token lifetime in seconds (default: 5 minutes).
                         Tokens signed by this identity expire after this many
                         seconds unless overridden in sign().
        """
        self.name = name
        self.default_ttl = default_ttl
        self._key = self._load_or_generate_key(key_file)
        self._audit_log_path = audit_log
        self._registry: dict[str, bytes] = {}  # name → key bytes

    # ─── Key management ────────────────────────────────────────────────────────

    @staticmethod
    def _load_or_generate_key(key_file: str | None) -> bytes:
        if key_file is None:
            return secrets.token_bytes(32)
        path = Path(key_file)
        if path.exists():
            raw = path.read_text().strip()
            return bytes.fromhex(raw)
        # Generate and save
        path.parent.mkdir(parents=True, exist_ok=True)
        key = secrets.token_bytes(32)
        path.write_text(key.hex())
        # Restrict permissions (best-effort; no-op on Windows)
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass
        return key

    def export_public(self) -> str:
        """
        Return the 'public' representation of this identity.

        For HMAC this IS the secret key — only share with agents that need to
        verify tokens from this identity. In a distributed system, share via a
        secure channel (env var, secrets manager), never in the token itself.

        Returns: hex string of the secret key.
        """
        return self._key.hex()

    # ─── Trust registry ────────────────────────────────────────────────────────

    def trust(self, agent_name: str, exported_key: str) -> None:
        """
        Add an agent to the trust registry.

        Args:
            agent_name: Name of the agent to trust (must match name used in sign()).
            exported_key: Hex string returned by the other agent's export_public().

        Example:
            planner = AgentIdentity("planner")
            planner.trust("orchestrator", orchestrator.export_public())
        """
        self._registry[agent_name] = bytes.fromhex(exported_key)

    def distrust(self, agent_name: str) -> None:
        """Remove an agent from the trust registry."""
        self._registry.pop(agent_name, None)

    def trusted_agents(self) -> list[str]:
        """Return list of currently trusted agent names."""
        return list(self._registry)

    # ─── Token signing ─────────────────────────────────────────────────────────

    def sign(self, payload: dict[str, Any], ttl: int | None = None) -> str:
        """
        Sign a payload and return a compact token.

        The token format is: <payload_b64>.<sig_b64>
        where payload_b64 is base64url(JSON) and sig_b64 is base64url(HMAC-SHA256).

        The payload always includes:
        - iss: issuer name (this agent's name)
        - iat: issued-at timestamp (unix seconds)
        - exp: expiry timestamp (unix seconds)

        Args:
            payload: Arbitrary JSON-serializable dict. Keys 'iss', 'iat', 'exp'
                     are reserved and will be overwritten.
            ttl: Token lifetime in seconds. Defaults to self.default_ttl.

        Returns:
            A compact token string safe to include in headers or message fields.
        """
        now = int(time.time())
        ttl = ttl if ttl is not None else self.default_ttl
        full_payload = {
            **payload,
            "iss": self.name,
            "iat": now,
            "exp": now + ttl,
        }
        payload_bytes = json.dumps(full_payload, separators=(",", ":"), sort_keys=True).encode()
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).rstrip(b"=").decode()
        sig = hmac.new(self._key, payload_b64.encode(), hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(sig).rstrip(b"=").decode()
        return f"{payload_b64}.{sig_b64}"

    # ─── Token verification ────────────────────────────────────────────────────

    def verify(
        self,
        token: str,
        allowed_issuers: list[str] | None = None,
    ) -> dict[str, Any]:
        """
        Verify a token and return its payload.

        Checks:
        1. Token is well-formed
        2. HMAC signature is valid (using the issuer's key from trust registry)
        3. Token has not expired
        4. Issuer is in the trust registry (and in allowed_issuers if given)

        Args:
            token: Token string returned by sign().
            allowed_issuers: Optional whitelist of issuer names. If given, tokens
                             from issuers not in this list are rejected even if
                             the signature is valid.

        Returns:
            The verified payload dict (including iss, iat, exp fields).

        Raises:
            MalformedTokenError: Token format is invalid.
            UntrustedIssuerError: Issuer not in trust registry.
            ExpiredTokenError: Token has expired.
            InvalidSignatureError: HMAC verification failed.
        """
        # 1. Parse structure
        parts = token.split(".")
        if len(parts) != 2:
            raise MalformedTokenError(f"Expected 2 parts, got {len(parts)}")

        payload_b64, sig_b64 = parts

        try:
            # Pad base64url back to standard length
            padding = 4 - len(payload_b64) % 4
            payload_bytes = base64.urlsafe_b64decode(payload_b64 + "=" * (padding % 4))
            payload = json.loads(payload_bytes)
        except Exception as exc:
            raise MalformedTokenError(f"Invalid payload encoding: {exc}") from exc

        # 2. Check issuer in registry
        issuer = payload.get("iss")
        if not issuer:
            raise MalformedTokenError("Token missing 'iss' field")
        if issuer not in self._registry:
            raise UntrustedIssuerError(
                f"Agent '{issuer}' is not in the trust registry. "
                f"Call .trust('{issuer}', key) first."
            )
        if allowed_issuers is not None and issuer not in allowed_issuers:
            raise UntrustedIssuerError(
                f"Agent '{issuer}' is not in allowed_issuers: {allowed_issuers}"
            )

        # 3. Verify HMAC (constant-time comparison)
        issuer_key = self._registry[issuer]
        expected_sig = hmac.new(issuer_key, payload_b64.encode(), hashlib.sha256).digest()
        try:
            padding = 4 - len(sig_b64) % 4
            actual_sig = base64.urlsafe_b64decode(sig_b64 + "=" * (padding % 4))
        except Exception as exc:
            raise InvalidSignatureError(f"Invalid signature encoding: {exc}") from exc

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise InvalidSignatureError(
                f"HMAC signature mismatch. Token may have been forged or tampered with."
            )

        # 4. Check expiry
        exp = payload.get("exp")
        if exp is not None and int(time.time()) > exp:
            raise ExpiredTokenError(
                f"Token expired {int(time.time()) - exp}s ago (issued by '{issuer}')"
            )

        return payload

    # ─── Audit log ─────────────────────────────────────────────────────────────

    def log(self, action: str, **metadata) -> None:
        """
        Append a signed entry to the audit log.

        Each entry is a JSON object on its own line (JSON Lines format):
        {"ts": 1234567890, "agent": "orchestrator", "action": "spawned sub-agent",
         "sig": "<hmac of the entry>", ...metadata}

        Args:
            action: Human-readable description of what the agent did.
            **metadata: Any additional key-value pairs to include.

        If no audit_log path was given at init, this is a no-op.
        """
        if self._audit_log_path is None:
            return
        now = int(time.time())
        entry = {"ts": now, "agent": self.name, "action": action, **metadata}
        entry_bytes = json.dumps(entry, separators=(",", ":"), sort_keys=True).encode()
        sig = hmac.new(self._key, entry_bytes, hashlib.sha256).hexdigest()
        entry["_sig"] = sig
        with open(self._audit_log_path, "a") as f:
            f.write(json.dumps(entry, separators=(",", ":")) + "\n")

    @staticmethod
    def verify_audit_log(log_path: str, agent_key: str) -> tuple[int, int]:
        """
        Verify the integrity of an audit log file.

        Each entry includes an HMAC signature (_sig) computed over the entry
        contents (excluding _sig itself). This detects tampering or insertion.

        Args:
            log_path: Path to the JSON Lines audit log file.
            agent_key: Hex key from the agent that wrote the log.

        Returns:
            Tuple of (valid_count, invalid_count).
        """
        key = bytes.fromhex(agent_key)
        valid = invalid = 0
        with open(log_path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    sig = entry.pop("_sig", None)
                    if sig is None:
                        invalid += 1
                        continue
                    entry_bytes = json.dumps(entry, separators=(",", ":"), sort_keys=True).encode()
                    expected = hmac.new(key, entry_bytes, hashlib.sha256).hexdigest()
                    if hmac.compare_digest(expected, sig):
                        valid += 1
                    else:
                        invalid += 1
                except Exception:
                    invalid += 1
        return valid, invalid
