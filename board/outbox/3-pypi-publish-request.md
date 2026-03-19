# PyPI Publishing Request (Re-request with Traction Data)

**Priority:** 3
**What I need:** Publish `agent-friend` to PyPI so users can `pip install agent-friend`

## Traction data (threshold met)

You said "ask again with demonstrated traction." Here's the evidence:

- **305 unique cloners** total on the agent-friend repo
- **166 unique cloners in the last 2 days** (March 17-18)
- Spike coincides with our first leaderboard articles going live
- March 17: 371 clones (95 unique) — likely GitHub Action adoption
- March 18: 259 clones (71 unique)

For comparison: 0-4 clones/day before articles. Now 200+/day.

## Why PyPI matters

Current friction:
```
git clone https://github.com/0-co/agent-friend.git
cd agent-friend
pip install -e .
```

With PyPI:
```
pip install agent-friend
agent-friend grade tools.json
```

The clone-to-star conversion is 0.7% (2 stars from 305 cloners). High friction = no stars. PyPI would fix this. Every article I publish links to the GitHub repo — with PyPI, those become real users.

## What I need you to do

1. Create account at https://pypi.org (or use existing if you have one)
2. Run: `cd agent-friend && python -m build && twine upload dist/*`
3. The `pyproject.toml` is already configured with the right metadata

OR: Give me the PyPI token and I'll set it up in GitHub Actions to auto-publish on release.

## Package name

`agent-friend` — check availability at https://pypi.org/project/agent-friend/ (available as of session 113 when we first discussed this)

This is the #1 adoption bottleneck. The traction is there. The tool is ready.

---
## Board Response

You now have a vault tool to communicate with PyPI over API
