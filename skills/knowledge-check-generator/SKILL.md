---
name: knowledge-check-generator
description: >
  Generate a practice knowledge check (gradable HTML) for a module, grounded in that
  module's lesson file — not model recall — and write it to docs/practice/. Then hand off
  to progress-recorder to bump practice_attempts.
---

# knowledge-check-generator

**When:** the student asks for practice questions on a module.

**Input:** the module's `docs/lessons/week-xx/module-y/index.md` (read it first).

**Procedure:** generate questions GROUNDED IN that lesson file — not model recall — to
avoid wrong answer keys on dense technical content. Mirror the canonical
`knowledge-check.html` format exactly.

**Output contract:** one self-contained gradable HTML file written to
`docs/practice/week-xx/module-y/<YYYY-MM-DD>-<slug>.html`
(same data shape + renderer as the canonical knowledge check). Then hand off to
`progress-recorder` to bump `practice_attempts`.

> Driven from the agent's system prompt + `agents.md`.
