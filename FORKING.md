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

4. **Create a virtualenv and install the tooling**:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate            # Windows: .venv\Scripts\activate
   python3 -m pip install -r requirements.txt
   ```

   Re-run the `activate` line each time you open a new shell. `.venv/` is
   gitignored, so it never lands in your fork.

5. **Install `oxtutor`** per the instructions you received at cohort kickoff. Configure it with the LiteLLM gateway key issued to you.

## Daily flow

```bash
source .venv/bin/activate               # Windows: .venv\Scripts\activate
mkdocs serve                            # local site at http://localhost:8000
oxtutor                                 # tutor agent (key required)
```

## Pulling new lessons

Pull at the **start of each week**, and any time an instructor announces a
change. You are serving the site from your own clone, so nothing reaches you
until you do.

This is not only about getting new content. An assessment retired upstream still
renders in a stale fork, and submitting it fails with a grading error, because
its answer key no longer exists on the server. Pulling is the fix.

```bash
git fetch upstream
git merge upstream/main                 # or: git rebase upstream/main
git push origin main                    # keep your GitHub fork in sync too
```

You will only ever get **fast-forward merges** if you have not edited lesson files yourself. `oxtutor` is configured to write only to `docs/practice/`, `docs/progress/`, and `scratch/` for exactly this reason; those paths never collide with upstream.

If `git merge upstream/main` reports a conflict in `docs/lessons/`, `docs/kb/`, `scripts/`, or `mkdocs.yml`, something has written outside the allowed paths. Open an issue; do not force-resolve.

## Sharing your progress with instructors

**Sign in with GitHub on any knowledge check.** That is the whole mechanism.

Every readiness, wrap-up and weekly check is graded and stored server-side the
moment you submit it. The instructor cohort view reads that store directly, so
your results appear there without you pushing anything.

Two things follow, both the opposite of what you might expect:

- **Your fork's visibility does not affect progress tracking.** Public or
  private, it makes no difference — your attempts never travel through the repo.
- **Committing and pushing does not record progress.** If you never sign in,
  nothing is tracked no matter how many commits you push.

The same sign-in drives the progress pill in the site header and the status
ticks on the **Roadmap**: they read back your own attempts (and only yours).
Signed out, the pill reads "Sign in to track progress" rather than 0%, because
nobody can tell the difference between "no work done" and "not signed in".

> Use the **same GitHub account** for your fork and for signing in. The site
> shows a banner if it spots a mismatch.
