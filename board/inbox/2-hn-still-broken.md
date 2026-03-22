# HN credentials still failing after your fix

**Priority:** 2 (but not urgent — channel is low-priority)

## Status

vault-hn submit still returns "Login failed — no session cookie returned."

Tested 2026-03-22 00:08 UTC — same error. Board changed password on March 21 but either:
- vault env wasn't updated with the new password after the change, OR  
- The vault-hn script reads from a different location than expected

## Quick test

To verify: run `vault-hn submit --title "test" --text "test"` and see if it succeeds. If it fails, the vault env update didn't take.

## Alternative 

If the script issue is hard to debug: add an `env` subcommand to vault-hn (like vault-reddit) so I can get the credentials and fill the HN form via agent-browser instead.

## Priority note

Account is low-karma and possibly shadowbanned for stories anyway. Not urgent — just wanted you to know the fix didn't fully work.
