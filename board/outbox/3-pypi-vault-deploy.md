# P3: vault-pypi Not Deployed — Needs sudoers Entry

**Priority**: P3 (when convenient)
**Filed**: 2026-03-19

## What's missing

You said "you now have a vault tool to communicate with PyPI over API."

Checked:
- `/etc/nixos/modules/users.nix` — vault-pypi NOT in sudoers rules
- Attempted `sudo -u vault /home/vault/bin/vault-pypi` — fails (not in sudoers)
- No vault-pypi module in `/etc/nixos/modules/`

The vault binary may exist at `/home/vault/bin/vault-pypi` but without the sudoers entry, the agent user cannot execute it.

## What's needed

Add to `/etc/nixos/modules/users.nix` in the `security.sudo.extraRules` block:

```nix
{
  command = "/home/vault/bin/vault-pypi";
  options = [ "NOPASSWD" ];
}
```

Then run `sudo nixos-rebuild switch --flake /etc/nixos#default`

## What vault-pypi should do

Upload package to PyPI using the API token stored in vault.
Usage pattern:
```bash
sudo -u vault /home/vault/bin/vault-pypi upload dist/*
```

The package is built and ready at `products/agent-friend/`.

---
## Board Response

Sorry, this has been updated and should now be available
