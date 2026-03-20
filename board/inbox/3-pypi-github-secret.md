# P3: Add PYPI_API_TOKEN to agent-friend GitHub secrets

## What
Add a GitHub Actions secret `PYPI_API_TOKEN` to the `0-co/agent-friend` repository.

The value is the PyPI API token currently used by `vault-pypi` (the token stored in vault).

## Why
I've created `.github/workflows/publish.yml` in the agent-friend repo that will:
1. Build the package on any `v*` tag push
2. Publish to PyPI automatically via `pypa/gh-action-pypi-publish`
3. Create a GitHub release

Currently I'm doing all three steps manually (build with nix-shell, upload with vault-pypi, create release with vault-gh). Automating this via GitHub Actions means:
- Faster releases (just push a tag)
- Consistent builds (uses GitHub's Python environment, not NixOS quirks)
- No need to manage dist/ files in the repo

## Steps
1. Go to https://github.com/0-co/agent-friend/settings/secrets/actions
2. Click "New repository secret"
3. Name: `PYPI_API_TOKEN`
4. Value: the PyPI API token from vault (same one used by vault-pypi)
5. Save

The workflow file is already committed at `.github/workflows/publish.yml`.

## Note on token type
PyPI now supports "trusted publishers" (OIDC from GitHub Actions) which doesn't require a token at all. If you'd prefer that approach: https://docs.pypi.org/trusted-publishers/adding-a-publisher/. Either works.
