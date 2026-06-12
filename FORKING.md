# Forking this repo as a cohort student

If you are an enrolled student, you'll work in your **own fork** of this repo. Your fork holds the same lesson content as upstream, plus your own progress records and practice quizzes.

## One-time setup

1. **Fork** `oxmiq/au-curriculum` on GitHub (use the Fork button).
2. **Clone your fork**:

   ```bash
   git clone git@github.com:<your-username>/au-curriculum.git
   cd au-curriculum
   ```

3. **Add the upstream remote** so you can pull new lessons as they ship:

   ```bash
   git remote add upstream git@github.com:oxmiq/au-curriculum.git
   git remote -v
   ```

4. **Install the tooling**:

   ```bash
   pip install mkdocs mkdocs-material pymdown-extensions
   ```

5. **Install `oxtutor`** per the instructions you received at cohort kickoff. Configure it with the LiteLLM gateway key issued to you.

## Daily flow

```bash
mkdocs serve                            # local site at http://localhost:8000
oxtutor                                 # tutor agent (key required)
```

## Pulling new lessons

```bash
git fetch upstream
git merge upstream/main                 # or: git rebase upstream/main
```

You will only ever get **fast-forward merges** if you have not edited lesson files yourself. `oxtutor` is configured to write only to `docs/practice/`, `docs/progress/`, and `scratch/` for exactly this reason — those paths never collide with upstream.

If `git merge upstream/main` reports a conflict in `docs/lessons/`, `docs/kb/`, `scripts/`, or `mkdocs.yml`, something has written outside the allowed paths. Open an issue; do not force-resolve.

## Sharing your progress with instructors

The instructor cohort view recomputes from each fork's `docs/progress/summary.json` on demand. Make sure your fork is **public** (the default) and you push your progress commits regularly.
