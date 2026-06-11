# Contributing

Curriculum content is maintained by Oxmiq Labs. External contributions are welcome for typo fixes, broken-link reports, and clarifying edits.

## What goes where

- **Lesson content** (`docs/lessons/`) — authored by the curriculum team; changes here require a content-owner review.
- **Tooling** (`scripts/`, `.github/workflows/`) — open PRs welcome.
- **Source material** (`planning/source-material/`) — the upstream study guides the lessons distill from; treat as reference, not as a primary edit target.
- **Site config** (`mkdocs.yml`, theme overrides) — open PRs welcome.

## Branch + PR

Always work on a feature branch and merge via PR. Direct pushes to `main` are blocked.

```bash
git checkout -b feat/<short-name>     # new feature
git checkout -b fix/<short-name>      # bug or typo fix
git checkout -b docs/<short-name>     # doc-only change
```

Conventional commit messages:

```
<type>(<scope>): <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `ci`.

## Before opening a PR

Run the local checks (both are warn-only in CI for now, but should pass):

```bash
python3 scripts/audit_lessons.py        # lesson invariants
python3 scripts/build_catalog.py        # regenerate catalog.json
mkdocs build --strict                   # site builds without warnings
```

If `build_catalog.py` changes `catalog.json`, commit the updated file.

## Authoring new lessons

See [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md) for the lesson shape. Every lesson:

- Lives under `docs/lessons/module-NN/`.
- Has an `index.md` (week overview), four `NN-<slug>.md` day files (NN = 01..04), a `quiz.html`, and an `assignment.md`.
- Cites its source under `planning/source-material/` via relative links (3 levels up from the lesson file).
- Passes `scripts/audit_lessons.py`.
