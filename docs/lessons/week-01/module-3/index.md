# Day 3 · Git Workflow

> **Concept of the day:** Branch, commit (conventional format), push, PR. Why commit messages matter.<br>
> **Pre-reading:** <a href="https://www.atlassian.com/git/tutorials/saving-changes" target="_blank" rel="noopener">Atlassian - Saving Changes</a>, <a href="https://www.atlassian.com/git/tutorials/using-branches" target="_blank" rel="noopener">Using Branches</a>, and <a href="https://www.atlassian.com/git/tutorials/syncing" target="_blank" rel="noopener">Syncing</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 - Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 3 · Git Workflow</span>
    {status:week-01/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts Deep Dive |
| Part 3 | Conventional Commits |
| Part 4 | Hands-On: Git Workflow |
| Part 5 | Hands-On: PR & Review |
| Part 6 | Common Mistakes & Wrap-up |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: <a href="https://www.atlassian.com/git/tutorials/saving-changes" target="_blank" rel="noopener">Atlassian - Saving Changes</a>, <a href="https://www.atlassian.com/git/tutorials/using-branches" target="_blank" rel="noopener">Using Branches</a>, and <a href="https://www.atlassian.com/git/tutorials/syncing" target="_blank" rel="noopener">Syncing</a>.

### Quick Self-Check

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m3-readiness" data-kind="readiness" data-draw="5" data-source="Atlassian Git Tutorials - Saving Changes, Branches & Syncing">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does `git clone` do?", "options": ["Creates a new branch", "Copies a repository to your local machine", "Uploads commits to GitHub", "Deletes a remote branch"], "answer": 1, "explain": "`git clone` copies a remote repository to your local machine, including all history and branches."},
  {"stem": "What's the difference between `git commit` and `git push`?", "options": ["They are the same thing", "Commit saves changes locally; push uploads them to the remote", "Push saves changes locally; commit uploads them to the remote", "Commit creates a branch; push merges it"], "answer": 1, "explain": "`git commit` records changes in your local repository. `git push` uploads those commits to the remote (GitHub)."},
  {"stem": "What is a branch in git?", "options": ["A way to delete commits", "An independent line of development", "A backup of your repository", "A type of remote server"], "answer": 1, "explain": "A branch is an independent line of development that lets you work on features without affecting the main codebase."},
  {"stem": "Which command creates a new branch?", "options": ["git new branch", "git checkout -b", "git branch create", "git init branch"], "answer": 1, "explain": "`git checkout -b <branch-name>` creates and switches to a new branch in one command."},
  {"stem": "What is a pull request (PR)?", "options": ["A command to download code", "A proposal to merge changes into the main branch", "A way to delete a branch", "A backup mechanism"], "answer": 1, "explain": "A pull request is a proposal to merge changes from one branch into another, inviting code review."},
  {"stem": "What does `git add .` do?", "options": ["Commits all changes", "Stages all changes for commit", "Creates a new repository", "Pushes to remote"], "answer": 1, "explain": "`git add .` stages all changes (new, modified, deleted files) to be included in the next commit."},
  {"stem": "What is the working directory?", "options": ["The GitHub cloud", "The files you're currently editing on your machine", "The .git folder", "The remote server"], "answer": 1, "explain": "The working directory is the folder on your local machine where you're actively editing files."},
  {"stem": "What is a commit in git?", "options": ["A type of branch", "A snapshot of changes with a message", "A remote server", "A merge operation"], "answer": 1, "explain": "A commit is a snapshot of your repository at a point in time, with a descriptive message explaining the changes."},
  {"stem": "What does `git status` show?", "options": ["The remote URL", "Which files have been modified and what's staged", "All branches", "The commit history"], "answer": 1, "explain": "`git status` shows which files are modified, staged for commit, or untracked."},
  {"stem": "What is the difference between local and remote branches?", "options": ["There is no difference", "Local branches exist on your machine; remote branches exist on GitHub", "Local branches are faster", "Remote branches cannot be deleted"], "answer": 1, "explain": "Local branches live on your machine. Remote branches (like 'origin/main') live on the remote server (GitHub)."},
  {"stem": "What does `git push origin <branch>` do?", "options": ["Creates a new repository", "Uploads your branch to the remote", "Deletes a remote branch", "Merges branches"], "answer": 1, "explain": "This uploads your local branch to the remote repository, making it available for others to see and pull."},
  {"stem": "What is 'origin' in git commands?", "options": ["The original commit", "The default remote repository name", "A branch type", "A git configuration"], "answer": 1, "explain": "'origin' is the default alias for the remote repository URL you cloned from."},
  {"stem": "What is the staging area (index)?", "options": ["A backup folder", "An area where changes are prepared before commit", "The remote repository", "A type of branch"], "answer": 1, "explain": "The staging area is where you prepare which changes will be included in your next commit."},
  {"stem": "What command shows commit history?", "options": ["git log", "git history", "git show-all", "git commits"], "answer": 0, "explain": "`git log` displays the commit history, including commit hashes, messages, authors, and dates."},
  {"stem": "What does `git diff` show?", "options": ["Remote differences", "Changes between commits, branches, or the working directory", "File sizes", "Branch history"], "answer": 1, "explain": "`git diff` shows the differences between commits, the working directory, or staged changes."},
  {"stem": "What is a remote in git?", "options": ["Your local machine", "A server that hosts a git repository", "A type of commit", "A backup system"], "answer": 1, "explain": "A remote is a server (like GitHub) that hosts a shared version of your repository."},
  {"stem": "What does `git fetch` do?", "options": ["Downloads commits from remote without merging", "Uploads commits to remote", "Creates a new branch", "Deletes old commits"], "answer": 0, "explain": "`git fetch` downloads commits from the remote but doesn't merge them into your local branches."},
  {"stem": "What does `git pull` do?", "options": ["Downloads commits from remote and merges", "Uploads commits to remote", "Creates a backup", "Deletes local files"], "answer": 0, "explain": "`git pull` fetches commits from the remote and automatically merges them into your current branch."},
  {"stem": "What is the main (or master) branch?", "options": ["A backup branch", "The primary/default branch where stable code lives", "A locked branch", "A remote-only branch"], "answer": 1, "explain": "The main branch is the primary branch containing stable, production-ready code."},
  {"stem": "What is a merge conflict?", "options": ["When two people edit the same file at the same time", "When git cannot automatically combine changes", "When a branch is deleted", "When push fails"], "answer": 1, "explain": "A merge conflict occurs when git cannot automatically combine changes from two branches, requiring manual resolution."}
]
</script>
</div>

---

## Part 2 - Core Concepts Deep Dive
### Reading - Why Git Matters

Every line of code you touch in this program lives in a git repository. Every PR, every benchmark commit, every capstone deliverable. Git is the difference between "I lost two days of work" and "I rolled back in 30 seconds."

### The Branch → Commit → Push → PR Loop

| Concept | Why it matters | Command |
|---------|----------------|---------|
| **Clone** | Copy a repo locally: your starting point. | `git clone <url>` |
| **Branch** | Isolate work-in-progress; never commit straight to `main`. | `git checkout -b <branch>` |
| **Commit** | A unit of change with a message: the building block of history. | `git add . && git commit -m "..."` |
| **Push** | Upload your branch to the remote (GitHub). | `git push origin <branch>` |
| **PR** (Pull Request) | Propose merging your branch back to `main`: invites review. | GitHub UI |

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

## Part 3 - Conventional Commits
### Reading - Why Commit Messages Matter

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

## Part 4 - Hands-On - Git Workflow
### Prerequisites

You need a GitHub account. If you don't have one, create one at github.com.

### Exercise 1: Fork and Clone

1. Go to the practice repository (ask your facilitator for the URL, or use any repo you own)
2. Click "Fork" to create your own copy
3. Clone it to your local machine:
```bash
git clone https://github.com/YOUR_USERNAME/repo-name.git
cd repo-name
```

### Exercise 2: Create Branch and Commit

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

## Part 5 - Hands-On - PR & Review
### Exercise: Create a Pull Request

1. Go to your forked repo on GitHub
2. You should see a prompt to create a PR for your new branch
3. Click "Compare & pull request"
4. Fill in:
   - **Title:** `feat: add greeting from YOUR_NAME`
   - **Body:** Brief description of what you added
5. Click "Create pull request"

### Exercise: Review

If you have access to a peer's PR:

1. Go to their PR page
2. Click "Files changed" to see what they modified
3. Leave a comment on a specific line
4. Click "Review changes" → "Approve" (or request changes)

---

## Part 7 - Wrap-up & Connection
### Reading - Common Mistakes to Avoid

| Mistake | Why it's bad | Correct approach |
|---------|--------------|------------------|
| `wip`, `temp`, `update` messages | Unreadable history | Use conventional commits |
| Push directly to `main` | Breaks the review process | Always branch first |
| 50-line commit messages | Hard to scan | First line ≤72 chars |
| Force-push to shared branch | Overwrites others' work | `--force-with-lease` only on your own branch |

### Self-Check

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Parts 2-5">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "Which git command creates and switches to a new branch in one step?", "options": ["git branch", "git checkout -b", "git switch -c", "git new branch"], "answer": 1, "explain": "`git checkout -b` creates and switches to a new branch. `git switch -c` does the same in modern git."},
  {"stem": "In conventional commits, which type should you use for a bug fix?", "options": ["feat:", "fix:", "docs:", "chore:"], "answer": 1, "explain": "Use `fix:` for bug fixes. Example: `fix: resolve memory leak in cache`."},
  {"stem": "What is the character limit for the first line of a conventional commit?", "options": ["50 characters", "72 characters", "100 characters", "No limit"], "answer": 1, "explain": "The first line should be 72 characters or less for optimal display in git tools."},
  {"stem": "What does `git add . && git commit -m \"...\"` do?", "options": ["Only commits without staging", "Stages all changes then commits with a message", "Pushes to remote", "Creates a branch"], "answer": 1, "explain": "This stages all changes and commits them with the message in one command chain."},
  {"stem": "What is the correct format for a new feature commit?", "options": ["new: add feature", "feat: add user authentication", "add: new feature", "feature: created user auth"], "answer": 1, "explain": "Conventional commits use `feat:` for new features, with imperative mood: `feat: add user authentication`."},
  {"stem": "What does `git push origin <branch>` do?", "options": ["Creates a new repository", "Uploads the branch to the remote", "Deletes the branch", "Merges to main"], "answer": 1, "explain": "This uploads your local branch to the remote, making it available for pull requests."},
  {"stem": "Which commit type should you use for documentation changes only?", "options": ["feat:", "fix:", "docs:", "refactor:"], "answer": 2, "explain": "Use `docs:` for documentation-only changes like README updates or adding comments."},
  {"stem": "What is a pull request?", "options": ["A git command", "A proposal to merge changes for review", "A backup method", "A file transfer protocol"], "answer": 1, "explain": "A pull request proposes merging your branch into the main branch and invites code review."},
  {"stem": "What should you do BEFORE creating a pull request?", "options": ["Delete your branch", "Push your branch to remote", "Commit directly to main", "Close the repository"], "answer": 1, "explain": "You must push your branch to the remote before you can create a pull request on GitHub."},
  {"stem": "What does `git checkout -b feat/my-feature` create?", "options": ["A tag", "A branch named 'feat/my-feature'", "A remote", "A commit"], "answer": 1, "explain": "This creates and switches to a new branch named 'feat/my-feature' following the conventional naming."},
  {"stem": "Which is a BAD commit message?", "options": ["feat: add user login", "fix: resolve parsing error", "wip", "docs: update API docs"], "answer": 1, "explain": "'wip' (work in progress) is too vague. Use conventional commit format with descriptive messages."},
  {"stem": "What is the purpose of code review in a PR?", "options": ["To delay the project", "To catch bugs and share knowledge", "To increase commit count", "To delete branches"], "answer": 1, "explain": "Code review catches bugs early, shares knowledge across the team, and improves code quality."},
  {"stem": "What command shows the current branch name?", "options": ["git branch", "git branch (lists all)", "git branch -v", "git status"], "answer": 3, "explain": "`git status` shows the current branch. `git branch` lists all local branches."},
  {"stem": "What does `refactor:` mean in conventional commits?", "options": ["Adding new features", "Restructuring code without changing behavior", "Fixing bugs", "Adding tests"], "answer": 1, "explain": "`refactor:` is for restructuring code to improve quality without changing its external behavior."},
  {"stem": "What is the correct order of the git workflow?", "options": ["Push → Commit → Branch → Clone", "Clone → Branch → Commit → Push", "Commit → Clone → Branch → Push", "Branch → Clone → Push → Commit"], "answer": 1, "explain": "The workflow is: clone the repo, create a branch, make commits, then push to share."},
  {"stem": "What should you use instead of force-pushing to shared branches?", "options": ["git push -f", "git push --force-with-lease", "git push --all", "git push -u"], "answer": 1, "explain": "`--force-with-lease` is safer as it aborts if others have pushed changes since your last fetch."},
  {"stem": "Which commit type is for configuration changes?", "options": ["feat:", "fix:", "chore:", "config:"], "answer": 2, "explain": "Use `chore:` for configuration changes, version bumps, and other non-code modifications."},
  {"stem": "What happens when you click 'Create pull request' on GitHub?", "options": ["Your code is deleted", "A review process is initiated to merge your branch", "Your branch is archived", "Nothing happens"], "answer": 1, "explain": "Creating a PR initiates a review process where others can comment, approve, or request changes."},
  {"stem": "What is the imperative mood for commit messages?", "options": ["Past tense (added)", "Present tense (add)", "Future tense (will add)", "Any tense"], "answer": 1, "explain": "Use imperative mood: 'add feature' not 'added feature'. It's like giving commands to the codebase."},
  {"stem": "What does `chore: bump version to 0.2.0` indicate?", "options": ["A new feature", "A bug fix", "A version number update", "A documentation change"], "answer": 2, "explain": "`chore:` is used for maintenance tasks like version bumps, dependency updates, and CI changes."}
]
</script>
</div>

### Connect Forward

Tomorrow: GPUs. We move from tooling to the hardware that will dominate the next four weeks.

### Pre-read for tomorrow (Day 4 · How Computers Run AI)

- **Resource:** <a href="https://www.youtube.com/watch?v=h9Z4oGN89MU" target="_blank" rel="noopener">GPU Explained</a>.
- **Reflection questions:**
  1. Name one reason GPUs are faster than CPUs for ML.
  2. Why is matrix multiplication central to neural networks? (One sentence.)
  3. What is the difference between *training* a model and *serving* (using) a model? Guess if unsure.

---

## Stuck?

Ask **oxtutor**; share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
