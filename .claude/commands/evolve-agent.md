Evolve an agent prompt through A/B testing and selection.

Usage: Run this when an agent's output quality matters enough to optimize, or when you suspect a prompt could be significantly better.

Step 1: Identify the agent and define fitness.
- Which agent prompt are you evolving? (file in `.claude/agents/`)
- What does "good output" look like? Be specific — speed, accuracy, code quality, creativity, format?
- How will you score it? Define a rubric before running variants.

Step 2: Create variants.
- Copy the current prompt as variant A (the control).
- Create variant B with a meaningful change — not just word-swapping. Change the framing, the constraints, the examples, the role definition, or the output format.
- If you have a theory about what's wrong, test that theory specifically.
- Save variants as `{agent-name}-variant-a.md` and `{agent-name}-variant-b.md` in `.claude/agents/`.

Step 3: Run the tournament.
- Give both variants the same task. Ideally the task is representative of real work, not a toy example.
- Score both outputs against your rubric from step 1.
- Record results in `decisions.md`: which variant, what task, scores, observations.

Step 4: Select and iterate.
- Winning variant becomes the new agent prompt.
- If the margin was small, run another round with a different task to confirm.
- If neither was good, the problem might be the task definition or acceptance criteria, not the prompt.
- Note what change made the difference — build intuition about what works for this type of agent.
- Delete losing variants. Keep the repo clean.

Step 5: Tag the agent prompt.
Add a comment at the top of the surviving prompt:
```
<!-- Evolved: [date]. Beat previous version on [criteria]. Key change: [what you changed]. -->
```

Over time, this record tells you what selection pressures have shaped each agent.
