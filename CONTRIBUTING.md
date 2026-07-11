# Contributing

Curriculum content is maintained by Oxmiq Labs. External contributions are welcome for typo fixes, broken-link reports, and clarifying edits.

> New to the site's layout? Read **[CONTENT-MAP.md](CONTENT-MAP.md)** first — it
> maps every content surface and shows which files are sources of truth vs.
> generated artifacts you should never hand-edit.

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

See [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md) for the full lesson shape. Every lesson:

- Lives under `docs/lessons/week-NN/module-N/` (week zero-padded `01`–`10`; module single digit `1`–`9`).
- Has an `index.md` (the lesson page), a `knowledge-check.html` (canonical formative knowledge check), and an `assignment.md`.
- Each week folder also has its own `week-NN/index.md` overview with a Day map.
- Cites source material via relative links into `planning/source-material/` — three levels up from a module file (`../../../planning/source-material/...`) or three levels up from the week overview.
- Uses `knowledge-check.html` (NOT the legacy `quiz.html`) and never references the legacy flat `docs/lessons/module-NN/` layout. Both are checked by `scripts/audit_lessons.py` rule L008.
- Passes `scripts/audit_lessons.py` (rules L001, L001m, L002, L003, L005, L006, L007, L008).

> **Source-material availability note.** The bulk of `planning/source-material/`
> is being imported across follow-up PRs (PR-B and PR-C) to keep each PR under
> the Copilot 20,000-line review cap. Until those merge, `audit_lessons.py`
> rule **L007** will report violations for lesson links that point at not-yet-
> imported source files; CI runs the audit in **warn-only** mode for exactly
> this reason. Once PR-B and PR-C land, L007 will be clean and the audit
> should be promoted to `--strict` in CI. Until then: do not author new lesson
> links that point at source-material files unless you've confirmed the file
> exists on `main` (or you are authoring in PR-B/PR-C themselves).
