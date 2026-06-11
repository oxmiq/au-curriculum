# Day 3 · Git Workflow

> **Concept of the day:** Branch, commit (conventional format), push, PR. Why commit messages matter.
> **Pre-reading:** [Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min).
> **Source:** [Week 1 Orientation Student Guide § Day 3](../../../../planning/source-material/Orientation/Orientation-Student-Guide.md).

---

## Why this matters

Every line of code you touch in this program lives in a git repository. Every PR, every benchmark commit, every capstone deliverable. Git is the difference between "I lost two days of work" and "I rolled back in 30 seconds."

## Readiness check

Five questions on the Atlassian tutorial. Sample:

1. What does `git clone` do?
2. What's the difference between `git commit` and `git push`?
3. Write a conventional-commit message for a bug fix in the install script.
4. Why never push directly to `main`?
5. What command shows you what files you've changed but not yet staged?

## Core concept — The branch → commit → push → PR loop

| Concept | Why it matters |
|---|---|
| **Clone** | Copy a repo locally — your starting point. |
| **Branch** | Isolate work-in-progress; never commit straight to `main`. |
| **Commit** | A unit of change with a message — the building block of history. |
| **Push** | Upload your branch to the remote (GitHub). |
| **PR** (Pull Request) | Propose merging your branch back to `main` — invites review. |
| **Conventional commits** | A discipline: `<type>: <description>` (e.g., `feat: add benchmark script`). |

### Conventional commit cheat-sheet

- `feat:` new functionality
- `fix:` bug fix
- `docs:` documentation only
- `refactor:` restructure without changing behavior
- `test:` add or fix tests
- `chore:` config, version bumps, CI

## Practice (90 min)

1. (15 min) Fork the practice repo your facilitator shares. Clone to your machine.
2. (20 min) Create a branch `feat/<your-name>-greeting`. Add `greetings/<your-name>.txt` with a one-line greeting. Commit with a conventional message. Push.
3. (15 min) Open a PR on GitHub. Write a body that explains the change.
4. (20 min) Review a peer's PR. Leave at least one substantive comment. Approve.
5. (10 min) Merge your PR after approval. Delete your branch.
6. (10 min) Simulate a conflict: practice `git status`, `git diff`, and a conflict-resolution edit.

### Common mistakes (avoid from Day 3 onwards)

- Commit messages like `wip`, `temp`, `update`, `fix stuff`. **Use conventional commits.**
- Pushing directly to `main`. **Never. Always branch.**
- 50-line commit messages with no clear subject. **First line ≤72 chars.**
- Force-pushing to a shared branch. **`--force-with-lease` only, and only on your own branch.**

## Wrap-up

Each pair walks through one PR they reviewed today — what was good, what would they ask the author to change?

## Connect forward

Tomorrow: GPUs. We move from tooling to the hardware that will dominate the next four weeks.

---

## Pre-read for tomorrow (Day 4 · How Computers Run AI)

- **Resource:** 15-minute video on what a GPU is (3Blue1Brown-style — facilitator will share the link).
- **Reflection questions:**
  1. Name one reason GPUs are faster than CPUs for ML.
  2. Why is matrix multiplication central to neural networks? (One sentence.)
  3. What is the difference between *training* a model and *serving* (using) a model? Guess if unsure.
