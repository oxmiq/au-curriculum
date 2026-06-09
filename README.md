# Oxmiq × Andhra University — Internship Curriculum

Your personal learning environment for the 10-week program. You'll **fork** this repo, run it locally, and use **oxtutor** as your on-demand tutor.

## Quickstart

```bash
# 1. Fork this repo on GitHub, then clone YOUR fork
git clone git@github.com:<your-username>/au-curriculum.git
cd au-curriculum

# 2. Run the site locally
pip install mkdocs mkdocs-material
mkdocs serve            # open http://localhost:8000

# 3. Stay current with new lessons (safe — you only ever write to your own folders)
git pull upstream main
```

Open the **Curriculum Map** to see every concept, what you've passed, and what unlocks next. Click a concept to read its lesson, then take the canonical knowledge check.

## Working with oxtutor

oxtutor is your tutor: it re-explains lessons, generates practice knowledge checks, and records your progress. It only ever writes to `practice/`, `progress/`, and `scratch/` — your lessons stay clean for `git pull`. See `agents.md` for how it navigates this repo.

## Layout

- `docs/lessons/` — the lessons + canonical knowledge checks (read-only; synced from upstream)
- `docs/kb/` — the curriculum map
- `docs/practice/`, `docs/progress/`, `scratch/` — yours; oxtutor writes here
- `agents.md`, `skills/` — how oxtutor is configured
