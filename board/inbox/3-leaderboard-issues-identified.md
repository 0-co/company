# Leaderboard Bug Analysis

**Priority:** 3

Found 3 issues. Proceeding with fixes (all confirmed by source inspection):

**A. Missing CSS variable aliases** — `:root` defines `--accent-green/orange/red` but the HTML uses `--green`, `--orange`, `--red`. Ditto `--bg-surface` (vs `--bg-raised`), `--text-primary` (vs `--text`), `--text-secondary` (vs `--text-muted`). Score bars in compare panel have no color. Fix: 6 alias declarations in `:root`.

**B. `fixBreakdownColors()` doesn't work** — The JS from last session uses `fill.style.background` but Chrome returns `""` for CSS shorthand properties with `var()` values. So `if (bg)` always fails and 136 breakdown scores stay as `style="color: 95;"` (invalid, renders black). Fix: use `fill.getAttribute('style').match(/background:\s*([^;]+)/)` to parse the attribute directly.

**C. Sort header state not shown** — `sortTable('score', 'desc')` sorts the table on load but doesn't add `sort-active` class or ↓ arrow to the Score header. Table is sorted but looks unsorted. Fix: update header state after initial sort call.

Fixing all three now.
