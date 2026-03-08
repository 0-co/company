# Git Push Broken — Repository Not Found (SSH)

**Priority:** 2 (important)
**Date:** 2026-03-08

## Symptoms
SSH authentication to GitHub works perfectly:
```
$ ssh -T git@github.com
Hi 0-co/autostartup! You've successfully authenticated...
```

But any git operation fails:
```
$ git push origin master
ERROR: Repository not found.
fatal: Could not read from remote repository.
```

Both `git-receive-pack` and `git-upload-pack` return "Repository not found."

## Verified
- SSH key fingerprint matches deploy key in repo (SHA256:jaWbaWxDrFWWE+)
- Deploy key has `read_only: false` (write enabled)
- Repo exists at github.com/0-co/autostartup (confirmed via REST API)
- vault-gh REST API works fine (can read repo details, push=true in permissions)

## What I Can't Do
- Push code to GitHub (all work is local only)
- Pull from remote
- Any git remote operations

## Request
Please investigate why git SSH operations fail despite authentication succeeding.

Possible causes to check:
- Deploy key might need to be re-added
- Repo might have branch protection blocking initial push
- Firewall/network issue with git-receive-pack specifically

**Workaround option:** Could I get an HTTPS remote URL with the PAT token embedded? I can then push that way.
