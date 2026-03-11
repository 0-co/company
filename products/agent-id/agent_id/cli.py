"""CLI for agent-id: key generation, token inspection, audit log verification."""

import argparse
import json
import secrets
import sys
import time


def cmd_keygen(args):
    """Generate a new random key."""
    key = secrets.token_bytes(32)
    print(key.hex())


def cmd_inspect(args):
    """Decode and display a token's payload (without verifying signature)."""
    import base64
    token = args.token
    parts = token.split(".")
    if len(parts) != 2:
        print(f"Error: expected 2 parts, got {len(parts)}", file=sys.stderr)
        sys.exit(1)
    payload_b64 = parts[0]
    try:
        padding = 4 - len(payload_b64) % 4
        payload_bytes = base64.urlsafe_b64decode(payload_b64 + "=" * (padding % 4))
        payload = json.loads(payload_bytes)
    except Exception as e:
        print(f"Error decoding token: {e}", file=sys.stderr)
        sys.exit(1)

    now = int(time.time())
    exp = payload.get("exp")
    status = "EXPIRED" if (exp and now > exp) else "VALID"

    print(json.dumps(payload, indent=2))
    print(f"\nStatus: {status}", file=sys.stderr)
    if exp:
        ttl_remaining = exp - now
        if ttl_remaining > 0:
            print(f"Expires in: {ttl_remaining}s", file=sys.stderr)
        else:
            print(f"Expired: {-ttl_remaining}s ago", file=sys.stderr)


def cmd_verify_log(args):
    """Verify the integrity of an audit log file."""
    from .identity import AgentIdentity
    valid, invalid = AgentIdentity.verify_audit_log(args.log_file, args.key)
    total = valid + invalid
    print(f"Entries: {total} total, {valid} valid, {invalid} invalid")
    if invalid > 0:
        print("WARNING: Audit log contains tampered or invalid entries", file=sys.stderr)
        if args.exit_code:
            sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        prog="agent-id",
        description="agent-id: zero-dependency agent identity and trust verification",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # keygen
    p_keygen = sub.add_parser("keygen", help="Generate a new 256-bit secret key")
    p_keygen.set_defaults(func=cmd_keygen)

    # inspect
    p_inspect = sub.add_parser("inspect", help="Decode and inspect a token (no signature check)")
    p_inspect.add_argument("token", help="Token string to inspect")
    p_inspect.set_defaults(func=cmd_inspect)

    # verify-log
    p_verlog = sub.add_parser("verify-log", help="Verify audit log integrity")
    p_verlog.add_argument("log_file", help="Path to JSON Lines audit log")
    p_verlog.add_argument("--key", required=True, help="Hex key of the agent that wrote the log")
    p_verlog.add_argument("--exit-code", action="store_true",
                          help="Exit with code 1 if any entries are invalid")
    p_verlog.set_defaults(func=cmd_verify_log)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
