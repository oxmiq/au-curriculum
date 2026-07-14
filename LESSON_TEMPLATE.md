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
│   │   ├── knowledge-check.md   canonical formative knowledge check
│   │   └── assignment.md       module assignment (substantive deliverable lives in module-1 by convention)
│   ├── module-2/ … module-4/   Mon–Thu lesson modules (same shape)
│   └── module-5/               Friday consolidation module (same shape)
├── week-02/ … week-10/         same shape
```

- `NN` is zero-padded (`01`, `02`, …, `10`): enforced by audit rule **L001**.
- `N` (module) is a single digit `1`–`9`: enforced by audit rule **L001m**.
- The module count per week is sourced from `docs/kb/graph.json` and enforced by **L003**.

## `docs/lessons/week-NN/index.md` (week overview) shape

```markdown
# Week N · <Theme>

> **Goal of the week:** one sentence.

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| <Day> (Mon) | <Topic> | <ref or -> | [Day 1 · <slug>](module-1/index.md) |
| <Day> (Tue) | <Topic> | <ref>        | [Day 2 · <slug>](module-2/index.md) |
| <Day> (Wed) | <Topic> | <ref>        | [Day 3 · <slug>](module-3/index.md) |
| <Day> (Thu) | <Topic> | <ref>        | [Day 4 · <slug>](module-4/index.md) |
| <Day> (Fri) | **Consolidation** | - | [module-5/index.md](module-5/index.md) |

## Friday - the bar

- **[Canonical knowledge check](module-5/knowledge-check.html)** - N questions. Pass = M/N.
- **[Assignment](module-1/assignment.md)** - short description. The week's substantive assignment lives in `module-1/assignment.md` by convention; sibling `module-N/assignment.md` files are stubs that point back to it.
```

> **Day-map links must be relative to the week folder** (`module-N/index.md`),
> not `../module-N/index.md`; that would resolve outside the week directory and
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

## Core concept - <name>

The main body.

## Apply it

Hands-on micro-exercise.

## Wrap

Three-bullet recap.
```

YAML-style frontmatter (a leading `---` block) is permitted; drift markers
and other metadata live there. The audit script skips the frontmatter when
checking the H1 invariant (**L002**, **L006**).

## `knowledge-check.html` shape

Self-contained HTML: no external CSS or JS. The page is the **canonical
formative knowledge check** for the module. If the item bank is not yet
authored, ship a clearly-labelled stub so progress tooling can detect the
slot (**L005**); never self-link to a non-existent canonical elsewhere.

The page must define a `QUIZ` object so progress tooling can pick it up:

```html
<script>
const QUIZ = {
  module: "week-NN/module-N",
  title:  "Knowledge Check - week-NN/module-N",
  pass:   0.6,
  questions: [ /* … */ ]
};
</script>
```

The filename is **`knowledge-check.html`**: never the legacy `quiz.html`
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
> The week's main assignment is on the day where the substantive deliverable lands;
> see [module-1/assignment.md](../module-1/assignment.md).
```

## Source-material citations

All `Source:` links use **relative paths from the lesson file**: three levels
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

---

## Day-screen templates (four canonical shapes)

Every `module-N/index.md` must conform to **exactly one** of the four shapes
below. Mixing shapes (Hybrid) is forbidden.

### Shape B7 - Regular day (Mon–Fri weekday, non-consolidation, non-capstone)

> **Reference:** `docs/lessons/week-09/module-1/index.md`

```markdown
# Day NN · <Topic>

> **Concept of the day:** one sentence.
> **Pre-reading:** <citation> or "none".
> **Source:** [<label>](../../../planning/source-material/<path>).

<!-- AUTO-GEN:LESSON-HEADER:START -->…<!-- AUTO-GEN:LESSON-HEADER:END -->

## Lesson plan

| Part | What you do | Time |
| --- | --- | --- |
| 1 | Pre-Reading Review | 15 min |
| 2 | <Name> | X min |
| 3 | <Name> | X min |
| 4 | <Name> | X min |
| 5 | <Name> | X min |
| 6 | <Name> | X min |
| 7 | Wrap-up & Connection | 10 min |
| **Total** | | **~140 min** |

## Part 1 - Pre-Reading Review · 15 min
…

## Part 2 - <Name> · X min
…

## Part 3 - <Name> · X min
…

## Part 4 - <Name> · X min
…

## Part 5 - <Name> · X min
…

## Part 6 - <Name> · X min
…

## Part 7 - Wrap-up & Connection · 10 min

### Self-check

- [ ] <invariant 1>
- [ ] <invariant 2>
- [ ] <invariant 3>

### Connect forward

One sentence pointing to the next day's topic.

### Pre-read for tomorrow (Day NN+1 · <Topic>)

- **Resource:** <citation> (~N min).
- **Reflection questions:**
  1. …
  2. …
  3. …

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
```

**Invariants (enforced by L011/L012):**
- H1 matches `^# Day \d+` (any day number, optional `(Fri)` suffix).
- Frontmatter block-quote has `Concept of the day:`, `Pre-reading:`, `Source:`.
- `## Lesson plan` table present with ≥3 Part rows and a `**Total**` row.
- Exactly Parts 1–7 present as `## Part N - ` headings, in order.
- Part headings use `·` (U+00B7 middle dot) as time separator, not `:`.
- Part 7 heading text is `Wrap-up & Connection`.
- `### Pre-read for tomorrow` is H3 **inside Part 7**: not a standalone H2.
- `## Stuck?` present as the final H2.
- No legacy H2s: `## Wrap-up`, `## Connect forward`, `## Pre-read for tomorrow`
  (top-level H2 form is forbidden; must live inside Part 7 as H3).

---

### Shape F - Friday consolidation

> **Reference:** `docs/lessons/week-09/module-5/index.md`

```markdown
# Day NN (Fri) · Week N Consolidation

> **Goal of the day:** one sentence.

<!-- AUTO-GEN:LESSON-HEADER:START -->…<!-- AUTO-GEN:LESSON-HEADER:END -->

## Self-Study Time Buckets

| Bucket | Activity | Duration |
|---|---|---|
| 🔵 Bucket 1 | Knowledge Check | 30 min |
| 🟢 Bucket 2 | Self-Assessment | 25 min |
| 🟡 Bucket 3 | <Drill topic A> | 25 min |
| 🟠 Bucket 4 | <Drill topic B> | 25 min |
| 🔴 Bucket 5 | <Practice / project seed> | 25 min |
| 🟣 Bucket 6 | Open Lab & Next-Week Preview | 15 min |

---

## 🔵 Bucket 1: Knowledge Check (30 min)
…

## 🟢 Bucket 2: Self-Assessment - <Title> (25 min)
…

## 🟡 Bucket 3: <Drill topic A> (25 min)
…

## 🟠 Bucket 4: <Drill topic B> (25 min)
…

## 🔴 Bucket 5: <Title> (25 min)
…

## 🟣 Bucket 6: Open Lab & <Next> Preview (15 min)
…

## Stuck?

Ask **oxtutor**; share what you tried, the unexpected result, and your module.
```

**Invariants (enforced by L011/L013):**
- H1 contains `Consolidation` (or week's Friday special label).
- `## Self-Study Time Buckets` table present with ≥3 bucket rows.
- Bucket emoji sequence is `🔵 🟢 🟡 🟠 🔴 🟣` (in order).
- Bucket 1 is always the Knowledge Check.
- Bucket 2 is always the Self-Assessment.
- Final bucket is always Open Lab (or equivalent).
- `## Stuck?` present as the final H2.
- No `## Lesson plan` table (forbidden in F shape).
- No `## Part N` headings (forbidden in F shape).

---

### Shape C - Capstone day (week-10)

> **Reference:** `docs/lessons/week-10/module-1/index.md`

```markdown
# Day NN · <Capstone milestone title>

> **Concept of the day:** one sentence.

## Time budget for today

| Block | Activity | Duration |
|---|---|---|
| 1 | <Name> | X min |
| 2 | <Name> | X min |
| … | … | … |

## Why this matters
…

## Today's milestones
- [ ] <Milestone 1>
- [ ] <Milestone 2>
- [ ] <Milestone 3>

## <Specific guidance section(s) for the day>
…

## Detailed time budget
…

## Wrap-up

Three-bullet recap.

## Self-check before Day NN+1
- [ ] <Invariant>
- [ ] <Invariant>

## Stuck?

Ask **oxtutor**; share your charter / deliverable and where you are stuck.
```

**Invariants (enforced by L011/L014):**
- H1 matches `^# Day \d+`.
- `## Time budget for today` or `## Detailed time budget` present.
- `## Today's milestones` section present with at least one `- [ ]` item.
- `## Wrap-up` present.
- `## Self-check before Day` present.
- `## Stuck?` present as the final H2.
- No `## Lesson plan` table (forbidden in C shape).
- No `## Part N` headings (forbidden in C shape).

---

### Hybrid prohibition

No `module-N/index.md` may mix shapes. Specifically forbidden combinations:

| Forbidden | Why |
|---|---|
| `## Part N` headings + `## 🔵 Bucket` headings in same file | B7 × F mix |
| `## Lesson plan` table + `## Self-Study Time Buckets` in same file | B7 × F mix |
| `## Wrap-up` as top-level H2 alongside `## Part N` headings | legacy + B7 mix |
| Top-level `## Connect forward` alongside `## Part N` headings | legacy + B7 mix |
| Top-level `## Pre-read for tomorrow` (H2) alongside `## Part N` headings | legacy + B7 mix |

The audit script (rules L011/L012) enforces this at CI time.

---

## Week-overview template (canonical 4-column shape)

> **Reference:** `docs/lessons/week-02/index.md`

```markdown
# Week N · <Theme>

> **Goal of the week:** one sentence.

<!-- AUTO-GEN:CARD-GRID:START -->…<!-- AUTO-GEN:CARD-GRID:END -->

## Day map

| Day | Topic | Pre-read | Page |
|---|---|---|---|
| N (Mon) | <Topic> | <citation or -> | [Day NN · <slug>](module-1/index.md) |
| N+1 (Tue) | <Topic> | <citation or -> | [Day NN+1 · <slug>](module-2/index.md) |
| N+2 (Wed) | <Topic> | <citation or -> | [Day NN+2 · <slug>](module-3/index.md) |
| N+3 (Thu) | <Topic> | <citation or -> | [Day NN+3 · <slug>](module-4/index.md) |
| N+4 (Fri) | **Consolidation** | - | [Day NN+4 · Consolidation](module-5/index.md) |

## Friday - the bar

- **[Canonical knowledge check](module-5/knowledge-check.html)** - N questions. Pass = M/N.
- **[Assignment](module-1/assignment.md)** - short description.

## Big-picture connect

One or two sentences connecting this week to the broader arc.

## Stuck?

Ask **oxtutor**; glossary entries for this week are the canonical definitions.
```

**Invariants (enforced by L010):**
- H1 matches `^# Week \d+ · `.
- Frontmatter block-quote has `Goal of the week:`.
- `## Day map` present with **exactly 4 columns**: `Day | Topic | Pre-read | Page`.
- Every Page-column link is `[Day NN · <slug>](module-N/index.md)` (relative,
  no `../` prefix).
- Friday row Topic cell is `**Consolidation**` (special weeks may use
  `**Phase N Wrap**` or similar descriptive label, but must be documented).
- `## Friday - the bar` present (or `## The bar` for capstone weeks).
- `## Big-picture connect` and `## Stuck?` are optional but must appear in this
  order if present.
