Run a structured review. Do this at natural breakpoints — after experiments, after several commits, when uncertain, or when something feels slow/broken. Do NOT do this when an active experiment is waiting to ship.

## Strategic check

1. Read `status.md`, `hypotheses.md`, `decisions.md`, and `git log --oneline -20`.
2. How much time has passed since the last review? (`date`)
3. What is the highest-EV hypothesis right now? Is that what you're working on? If not, why?
4. What assumptions are you making that you haven't tested?
5. If you started fresh today with what you know now, would you make the same choices?
6. Are you behaving like a CEO or have you drifted into engineering?

## Operational check

7. **State files:** Is `status.md` accurate? Would it orient your future self after a crash? Are `hypotheses.md` and `finances.md` current? Is `decisions.md` useful to read or has it become a dumping ground?
8. **Agent prompts:** Read every prompt in `.claude/agents/`. Any unused? Any trying to do too much? Any consistently producing output you have to redo? Flag for evolution (`/project:evolve-agent`).
9. **Code:** Dead code from abandoned experiments? Abandoned worktrees? Tech debt actively blocking current work?
10. **Process:** Are your management frameworks earning their overhead or becoming theater? Is the board inbox well-structured or vague? Is rate limit usage proportional to value?

## Output

Log in `decisions.md` with a timestamp: what you're continuing and why, what you're changing and why, any new hypotheses or priorities. Be specific about actions taken ("deleted 3 abandoned prompts, refactored checkout module, reprioritized hypothesis X over Y because...").

The most valuable output is admitting something isn't working.
