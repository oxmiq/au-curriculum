# Lesson template

This is the authoring contract for every lesson in `docs/lessons/module-NN/`.

## File layout

```
docs/lessons/module-NN/
├── index.md                  week overview + day map
├── 01-<slug>.md              Day 1 (Mon)
├── 02-<slug>.md              Day 2 (Tue)
├── 03-<slug>.md              Day 3 (Wed)
├── 04-<slug>.md              Day 4 (Thu)
├── quiz.html                 Day 5 (Fri) canonical quiz
└── assignment.md             module assignment
```

- `NN` is zero-padded (`01`, `02`, ..., `10`).
- `<slug>` is kebab-case.
- The day files must be numbered `01` through `04`.

## `index.md` shape

```markdown
# Module N · <Theme>

> **Goal of the week:** one sentence.
> **Source material:** [`<folder>/`](../../../planning/source-material/<folder>/) — Study Guide, Pre-Lecture Reading, ...

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| 1 (Mon) | <Topic> | — | [01-<slug>.md](01-<slug>.md) |
| 2 (Tue) | <Topic> | <ref> | [02-<slug>.md](02-<slug>.md) |
| 3 (Wed) | <Topic> | <ref> | [03-<slug>.md](03-<slug>.md) |
| 4 (Thu) | <Topic> | <ref> | [04-<slug>.md](04-<slug>.md) |
| 5 (Fri) | **Consolidation** — quiz + open lab | — | [quiz.html](quiz.html) |

## Friday — the bar

- **[Take the canonical quiz](quiz.html)** — N questions. Pass = M/N.
- **[Assignment](assignment.md)** — short description.

## Self-check before next module

Bullet list of "you should be able to..." items.
```

## Day file (`NN-<slug>.md`) shape

```markdown
# Day N · <Topic>

> **Concept of the day:** one sentence.
> **Pre-reading:** <ref> or "None".
> **Source:** [<short label>](../../../planning/source-material/<path>).

---

## Why this matters

One paragraph.

## Readiness check

Optional. Short questions to test whether the pre-reading landed.

## Core concept — <name>

The main body.

## Apply it

Hands-on micro-exercise.

## Wrap

Three-bullet recap.
```

## `quiz.html` shape

Self-contained HTML — no external CSS or JS. Includes the answer key (canonical quizzes are formative knowledge checks).

## `assignment.md` shape

Short Markdown file describing the assignment, deliverable, due date (in week-relative terms), and how it is graded.

## Source-material citations

All "Source:" links must use **relative paths from the lesson file**, three levels up to reach the repo root:

```markdown
[Label](../../../planning/source-material/<folder>/<file>.md)
```

Spaces in folder/file names are URL-encoded as `%20`. The `audit_lessons.py` script verifies that every referenced source file exists.

## Invariants enforced by `scripts/audit_lessons.py`

- L001 — module folder name matches `module-NN` (zero-padded, 01..10)
- L002 — `index.md` exists and starts with an H1
- L003 — exactly four day files matching `0[1-4]-<slug>.md`
- L004 — each day file starts with an H1
- L005 — `quiz.html` exists
- L006 — `assignment.md` exists and starts with an H1
- L007 — every `planning/source-material/...` link in the lesson points at a file that exists on disk
- L008 — no `../../../../planning/source-material/` (legacy 4-up form from the flat planning shape)
