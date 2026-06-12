# Week 8 — Capsule Foundations · Module Assignment

> **Source:** Capsule Power User Problem Sets §Set 40 (breakage-race exercise).

## What you submit

Three **bug reports** filed against three instructor-simulated breakages encountered during the Friday consolidation lab. Each report is a markdown file in your fork, plus a shared link to a tracking issue (instructor will provide a repo or stand-in).

## The 5-field bug-report format (mandatory)

Each report uses **exactly this structure**:

```markdown
# [short imperative title]

## Reproduction steps
1. ...
2. ...
3. ...

## Expected behavior
...

## Actual behavior
...

## Environment
- Capsule CLI version: ...
- OS / shell: ...
- Environment: ...
- Node: ...
- Date / time (UTC): ...

## Logs / evidence
```text
<paste minimal relevant log snippet — not 5,000 lines>
```

## Hypothesis & suggested fix
- Hypothesis: ...
- Suggested fix or workaround: ...
```

## Grading rubric

| Aspect | Pass requires |
|---|---|
| Reproduction | Steps a stranger can follow with no extra context |
| Expected vs actual | Both stated precisely; no "doesn't work" |
| Environment | All 5 environment fields filled |
| Logs | Minimal relevant snippet (not a wall) |
| Hypothesis | Plausible root cause referenced to Day 36–39 mental model |
| Suggested fix | Concrete, actionable, even if you can't implement it |

**3/3 reports passing all 6 aspects = pass.** Anything less = revise and resubmit.

## Why this assignment exists

Your job on Capsule isn't to never hit breakages — it's to handle them well. A good bug report:

- Saves the maintainer's time → gets fixed faster → unblocks you and the cohort.
- Forces *you* to localize the problem (often you solve it while writing the report).
- Builds a permanent record so the next person hitting it can recover in minutes.

You'll use this format throughout Phase 3. Internalize it.

## Tips

- Write the report **as you debug** — don't reconstruct from memory after.
- Run the diagnostic sequence from Flashcards Q25–Q28 before reporting "Capsule is broken."
- If you find a workaround during debugging, *both* the hypothesis and the workaround go in the suggested-fix field.
- Cross-reference Module 10's known-quirks table — if it's a known quirk, say so and don't re-file.
