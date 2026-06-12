# Lesson template

This is the authoring contract for every lesson in `docs/lessons/week-NN/module-N/`.

> **Source of truth.** The invariants enforced by `scripts/audit_lessons.py`
> are the authoritative contract. This template documents the intended *shape*;
> the audit script is what CI runs.

## Repo layout

```
docs/lessons/
├── week-01/
│   ├── index.md                week overview + Day map
│   ├── module-1/
│   │   ├── index.md            lesson page
│   │   ├── knowledge-check.html canonical formative knowledge check
│   │   └── assignment.md       module assignment (substantive deliverable lives in module-1 by convention)
│   ├── module-2/ … module-4/   Mon–Thu lesson modules (same shape)
│   └── module-5/               Friday consolidation module (same shape)
├── week-02/ … week-10/         same shape (week-06 has an extra module-6 for the Phase 2 wrap)
```

- `NN` is zero-padded (`01`, `02`, …, `10`) — enforced by audit rule **L001**.
- `N` (module) is a single digit `1`–`9` — enforced by audit rule **L001m**.
- The module count per week is sourced from `docs/kb/graph.json` and enforced by **L003**.

## `docs/lessons/week-NN/index.md` (week overview) shape

```markdown
# Week N · <Theme>

> **Goal of the week:** one sentence.
> **Source material:** [`<folder>/`](../../../planning/source-material/<folder>/) — Study Guide, Pre-Lecture Reading, ...

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| <Day> (Mon) | <Topic> | <ref or —> | [Day 1 · <slug>](module-1/index.md) |
| <Day> (Tue) | <Topic> | <ref>        | [Day 2 · <slug>](module-2/index.md) |
| <Day> (Wed) | <Topic> | <ref>        | [Day 3 · <slug>](module-3/index.md) |
| <Day> (Thu) | <Topic> | <ref>        | [Day 4 · <slug>](module-4/index.md) |
| <Day> (Fri) | **Consolidation** | — | [module-5/index.md](module-5/index.md) |

## Friday — the bar

- **[Canonical knowledge check](module-5/knowledge-check.html)** — N questions. Pass = M/N.
- **[Assignment](module-1/assignment.md)** — short description. The week's substantive assignment lives in `module-1/assignment.md` by convention; sibling `module-N/assignment.md` files are stubs that point back to it.
```

> **Day-map links must be relative to the week folder** (`module-N/index.md`),
> not `../module-N/index.md` — that would resolve outside the week directory and
> break navigation.

## `docs/lessons/week-NN/module-N/index.md` (lesson page) shape

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

YAML-style frontmatter (a leading `---` block) is permitted — drift markers
and other metadata live there. The audit script skips the frontmatter when
checking the H1 invariant (**L002**, **L006**).

## `knowledge-check.html` shape

Self-contained HTML — no external CSS or JS. The page is the **canonical
formative knowledge check** for the module. If the item bank is not yet
authored, ship a clearly-labelled stub so progress tooling can detect the
slot (**L005**); never self-link to a non-existent canonical elsewhere.

The page must define a `QUIZ` object so progress tooling can pick it up:

```html
<script>
const QUIZ = {
  module: "week-NN/module-N",
  title:  "Knowledge Check — week-NN/module-N",
  pass:   0.6,
  questions: [ /* … */ ]
};
</script>
```

The filename is **`knowledge-check.html`** — never the legacy `quiz.html`
(**L008** flags any lingering `quiz.html` reference).

## `assignment.md` shape

Short Markdown file describing the assignment, deliverable, due date (in
week-relative terms), and how it is graded. Must start with an H1 (**L006**).

By convention, the **substantive weekly assignment lives in
`module-1/assignment.md`**. The other `module-N/assignment.md` files are
stub placeholders that point back to module-1:

```markdown
# Assignment · week-NN/module-N

> **No standalone assignment for this day.**
>
> The week's main assignment is on the day where the substantive deliverable lands —
> see [module-1/assignment.md](../module-1/assignment.md).
```

## Source-material citations

All `Source:` links use **relative paths from the lesson file** — three levels
up to reach the repo root (or four levels up from inside a `module-N/`
subdirectory, depending on file depth):

```markdown
[Label](../../../planning/source-material/<folder>/<file>.md)
```

Spaces in folder/file names are URL-encoded as `%20`. The `audit_lessons.py`
script verifies every referenced source file exists (**L007**).

## Invariants enforced by `scripts/audit_lessons.py`

The audit script is the authoritative contract. As of this PR:

| Rule  | Check |
|-------|-------|
| L001  | Week folder name matches `week-NN` (zero-padded, 01..10) |
| L001m | Module folder name matches `module-N` (1..9) |
| L002  | `index.md` exists and starts with an H1 (both week overview and each module) |
| L003  | Module count per week matches `docs/kb/graph.json` |
| L005  | `knowledge-check.html` exists in every module folder |
| L006  | `assignment.md` exists and starts with an H1 in every module folder |
| L007  | Every `planning/source-material/...` link in a lesson points at a file that exists on disk (URL-encoded paths are decoded before checking) |
| L008  | No legacy `quiz.html` references; no legacy flat `lessons/module-NN/` references |

Run locally before opening a PR:

```bash
python3 scripts/audit_lessons.py           # all weeks
python3 scripts/audit_lessons.py --week week-01
python3 scripts/audit_lessons.py --strict  # exit non-zero on violations
python3 scripts/audit_lessons.py --json    # machine-readable
```
