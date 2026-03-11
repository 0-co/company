# Request: PyPI Vault Wrapper for Publishing agent-* Packages

## What I need
A vault wrapper that can publish Python packages to PyPI (pypi.org). The pattern is a REST wrapper that injects a PyPI API token into `twine upload` commands.

## Why
We have 4 published agent-* tools (agent-budget, agent-context, agent-eval, agent-shield) but they're only installable via:
```
pip install git+https://github.com/0-co/company.git#subdirectory=products/agent-shield
```

This is a significant distribution barrier. Getting them on PyPI would:
- Enable `pip install agent-shield` (canonical, memorable)
- Make them discoverable via https://pypi.org search
- Improve SEO (PyPI package pages rank in Google)
- Enable dependency resolution (other packages can declare `agent-shield` as a dep)
- Signal legitimacy (PyPI packages feel more "real" than git+https installs)

All 4 packages already have proper `pyproject.toml` with metadata. Zero additional work needed once publishing is set up.

## What you'd need to do
1. Create a PyPI account at https://pypi.org/account/register/ (username suggestion: `0coceo` or `agent-tools`)
2. Generate an API token at https://pypi.org/manage/account/token/ (scoped to "entire account" for first publish, can scope to project later)
3. Create a vault wrapper `vault-pypi` that wraps `twine upload` with the API token

## Suggested wrapper script
```bash
#!/bin/bash
# vault-pypi — uploads Python packages to PyPI with credentials
# Usage: sudo -u vault /home/vault/bin/vault-pypi <dist_dir>
# Example: sudo -u vault /home/vault/bin/vault-pypi products/agent-shield/dist/

PYPI_TOKEN="__token__"
PYPI_API_KEY="$(cat /home/vault/secrets/pypi_token)"

python3 -m twine upload \
  --username "$PYPI_TOKEN" \
  --password "$PYPI_API_KEY" \
  "$@"
```

## Cost
Free. PyPI is free for all public open-source packages.

## Priority
Medium. Not blocking current work but would significantly improve discoverability of the tools we're shipping.
