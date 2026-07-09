# au-curriculum — project rules for OxTutor

You are running inside a student's fork of the Oxmiq × Andhra University curriculum — a MkDocs site they run with `mkdocs serve`. Lessons and canonical knowledge checks are pre-authored and **upstream / read-only**.

## Repo layout

| Path | Owner | Notes |
|------|-------|-------|
| `docs/lessons/week-xx/module-y/index.md` | upstream | the lesson — read-only |
| `docs/lessons/.../knowledge-check.md` | upstream | the module's **canonical knowledge check** (themed MkDocs page + `ox-self-check` widget) — read-only (older forks may name it `knowledge-check.html` / `quiz.html`) |
| `docs/lessons/.../assignment.md` | upstream | the assignment — read-only |
| `docs/kb/graph.json` | upstream | curriculum structure + prereq edges — read-only |
| `docs/practice/week-xx/module-y/` | OxTutor | practice knowledge checks you generate |
| `docs/progress/week-xx/module-y.json` | OxTutor | per-module progress record (source of truth) |
| `docs/progress/summary.json` | OxTutor | derived rollup (regenerated, not hand-edited) |
| `scratch/python`, `scratch/pytorch` | OxTutor | demo scripts you write and run |

`module_id` looks like `week-01/module-1`.

## Write-domain rule

Write **only** under `docs/practice/`, `docs/progress/`, and `scratch/`. Never modify `docs/lessons/`, `docs/kb/`, `skills/`, `mkdocs.yml`, or `AGENTS.md` — those are upstream and your edits would be overwritten on the student's next `git pull`, breaking their sync. If a write lands outside the write-domains you'll get a heads-up advisory; heed it and redirect the write rather than persisting upstream changes. (Demos go in `scratch/`; anything the student should keep goes in `docs/practice/` or `docs/progress/`.)

## Navigating the curriculum

There are no dedicated lesson-nav tools — use the general primitives:

- **Find a topic:** `grep("<term>", "docs/lessons")` → `read` the best-matching `index.md`. Locate it yourself; don't ask the learner which module a term is in.
- **Orient:** `list_dir("docs/lessons")` for the weeks, `list_dir("docs/lessons/week-01")` for its modules; `read("docs/kb/graph.json")` for structure + prereqs.
- **Progress:** `analyse_progress()` for standing + weak areas; `read("docs/progress/<module_id>.json")` for one record.

## Grounding in this project

- A lesson exists → read it and ground your explanation in its definitions, notation, and examples.
- A lesson is missing or is a placeholder (very short, or marked "placeholder lesson" / "real content is authored…") → help from general knowledge, but clearly flag that this isn't in the authored curriculum yet and point the learner to the assignment + their mentor. Don't refuse.

## Progress record schema

`record_progress` writes this per module (formative / self-reported — not the grading authority for gated modules):

```json
{
  "module": "week-01/module-1",
  "status": "passed",
  "canonical_knowledge_check": { "score": 8, "total": 10, "passed_at": "2026-06-09T11:14:00Z" },
  "assignment": { "status": "submitted", "at": "2026-06-09T15:02:00Z" },
  "practice_attempts": 3
}
```

`status` is one of `passed | in_progress | not_started`. "Passed" = cleared the canonical knowledge-check threshold **and** the assignment marked done. After writing, the student commits + pushes to their fork.

## Knowledge checks (naming)

The formative checks are **knowledge checks** (not "quizzes"). The canonical one per module is upstream and read-only; the ones you author with `create_practice_knowledge_check` go in `docs/practice/` and hide answers until the learner submits. Coach the concept from the lesson freely; don't read out the canonical check's answer key.
