# Day 3 · Git Workflow

> **Concept of the day:** Branch, commit (conventional format), push, PR. Why commit messages matter.<br>
> **Pre-reading:** [Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 — Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 3 · Git Workflow</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-01/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do | Time |
|-------------|---------------|----------|
| Part 1 | Pre-Reading Review | 10 min |
| Part 2 | Core Concepts Deep Dive | 20 min |
| Part 3 | Conventional Commits | 15 min |
| Part 4 | Hands-On: Git Workflow | 40 min |
| Part 5 | Hands-On: PR & Review | 30 min |
| 7 | Common Mistakes & Wrap-up | 15 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: [Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min).

### Quick Self-Check

Answer these questions from memory:
1. What does `git clone` do?
2. What's the difference between `git commit` and `git push`?
3. What is a branch in git?

If you couldn't answer all three, review the Atlassian tutorial again before proceeding.

---

## Part 2 — Core Concepts Deep Dive · 20 min
### Reading — Why Git Matters

Every line of code you touch in this program lives in a git repository. Every PR, every benchmark commit, every capstone deliverable. Git is the difference between "I lost two days of work" and "I rolled back in 30 seconds."

### The Branch → Commit → Push → PR Loop

| Concept | Why it matters | Command |
|---------|----------------|---------|
| **Clone** | Copy a repo locally — your starting point. | `git clone <url>` |
| **Branch** | Isolate work-in-progress; never commit straight to `main`. | `git checkout -b <branch>` |
| **Commit** | A unit of change with a message — the building block of history. | `git add . && git commit -m "..."` |
| **Push** | Upload your branch to the remote (GitHub). | `git push origin <branch>` |
| **PR** (Pull Request) | Propose merging your branch back to `main` — invites review. | GitHub UI |

### Visual Workflow

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Clone  │ ──> │ Branch  │ ──> │ Commit  │ ──> │  Push   │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
                                                     │
                                                     v
                                              ┌─────────┐
                                              │    PR   │
                                              └─────────┘
```

---

## Part 3 — Conventional Commits · 15 min
### Reading — Why Commit Messages Matter

Bad commit messages like `wip`, `temp`, `update`, `fix stuff` make git history unreadable. Conventional commits add structure:

### Conventional Commit Format

```
<type>: <description>

[optional body]
[optional footer]
```

### Commit Types Cheat-Sheet

| Type | When to use | Example |
|------|-------------|---------|
| `feat:` | New functionality | `feat: add GPU temperature monitoring` |
| `fix:` | Bug fix | `fix: resolve nvidia-smi parsing error` |
| `docs:` | Documentation only | `docs: update README with new flags` |
| `refactor:` | Restructure without changing behavior | `refactor: reorganize benchmark folder` |
| `test:` | Add or fix tests | `test: add unit tests for tokenizer` |
| `chore:` | Config, version bumps, CI | `chore: bump version to 0.2.0` |

### Rules

- First line ≤ 72 characters
- Use imperative mood ("add" not "added")
- Body when you need more context

---

## Part 4 — Hands-On — Git Workflow · 40 min
### Prerequisites

You need a GitHub account. If you don't have one, create one at github.com.

### Exercise 1: Fork and Clone (15 min)

1. Go to the practice repository (ask your facilitator for the URL, or use any repo you own)
2. Click "Fork" to create your own copy
3. Clone it to your local machine:
```bash
git clone https://github.com/YOUR_USERNAME/repo-name.git
cd repo-name
```

### Exercise 2: Create Branch and Commit (25 min)

```bash
# 1. Create a new branch
git checkout -b feat/my-greeting

# 2. Create a new file
mkdir -p greetings
echo "Hello from YOUR_NAME!" > greetings/YOUR_NAME.txt

# 3. Stage and commit
git add greetings/YOUR_NAME.txt
git commit -m "feat: add greeting from YOUR_NAME"

# 4. Push to remote
git push origin feat/my-greeting
```

---

## Part 5 — Hands-On — PR & Review · 30 min
### Exercise: Create a Pull Request (15 min)

1. Go to your forked repo on GitHub
2. You should see a prompt to create a PR for your new branch
3. Click "Compare & pull request"
4. Fill in:
   - **Title:** `feat: add greeting from YOUR_NAME`
   - **Body:** Brief description of what you added
5. Click "Create pull request"

### Exercise: Review (15 min)

If you have access to a peer's PR:
1. Go to their PR page
2. Click "Files changed" to see what they modified
3. Leave a comment on a specific line
4. Click "Review changes" → "Approve" (or request changes)

---

## Part 7 — Wrap-up & Connection · 15 min
### Reading — Common Mistakes to Avoid

| Mistake | Why it's bad | Correct approach |
|---------|--------------|------------------|
| `wip`, `temp`, `update` messages | Unreadable history | Use conventional commits |
| Push directly to `main` | Breaks the review process | Always branch first |
| 50-line commit messages | Hard to scan | First line ≤72 chars |
| Force-push to shared branch | Overwrites others' work | `--force-with-lease` only on your own branch |

### Self-Check

Can you do these from memory?
- [ ] Clone a repository
- [ ] Create a new branch
- [ ] Add files, commit with conventional message
- [ ] Push to remote
- [ ] Open a PR on GitHub

### Connect Forward

Tomorrow: GPUs. We move from tooling to the hardware that will dominate the next four weeks.

### Pre-read for tomorrow (Day 4 · How Computers Run AI)

- **Resource:** 15-minute video on what a GPU is (3Blue1Brown-style — facilitator will share the link).
- **Reflection questions:**
  1. Name one reason GPUs are faster than CPUs for ML.
  2. Why is matrix multiplication central to neural networks? (One sentence.)
  3. What is the difference between *training* a model and *serving* (using) a model? Guess if unsure.

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
