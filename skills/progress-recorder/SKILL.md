---
name: progress-recorder
description: >
  Record a student's progress after a canonical knowledge check is passed, an assignment submitted,
  or a practice attempt made — by updating the per-module JSON record and regenerating the
  derived summary.json that the curriculum map and progress views read.
---

# progress-recorder

**When:** after a canonical knowledge check is passed, an assignment is submitted, or a practice
attempt is made.

**Procedure:**
1. Write/update `docs/progress/week-xx/module-y.json` (schema in `agents.md`).
2. Run `python3 skills/progress-recorder/build_summary.py` — it regenerates
   `docs/progress/summary.json` (per-week rollups + overall) from all per-module records,
   so the map and progress view read one small file.
3. `git add` those paths, commit with a clear message, and push to the student's fork.

**Output contract:** writes confined to `docs/progress/`. Never touches lessons or kb.
`summary.json` is derived — never hand-edit it; edit the per-module record and re-run the
script.

> Driven from the agent's system prompt + `agents.md`; wired into the `oxtutor` agent
> configuration under the ADK pivot. `build_summary.py` is the one executable here and is
> pure stdlib.
