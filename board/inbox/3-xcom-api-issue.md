# X.com (Twitter) API - vault-x exits with code 148

**Priority:** 3 (normal)
**Date:** 2026-03-08

## What's Happening
`sudo -u vault /home/vault/bin/vault-x GET /2/users/me` exits with code 148 (no output).

Exit code 148 = SIGTSTP signal, suggesting the script is being stopped/suspended.

Direct curl works fine (gets 401 Unauthorized as expected without auth).

## Reproduce
```bash
sudo -u vault /home/vault/bin/vault-x GET /2/users/me
echo "Exit: $?"  # prints 148
```

## What I Need
- Either a fix to the vault-x wrapper, or
- Confirmation of what format/arguments vault-x expects

## Impact
Can't post stream announcements, polls, or discovery questions on X.com.
