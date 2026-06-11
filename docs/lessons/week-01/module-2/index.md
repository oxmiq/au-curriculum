# Day 2 · Shell & Linux

> **Concept of the day:** The shell as your primary tool. Pipes, redirects, grep, awk, basic scripting.
> **Pre-reading:** [MIT Missing Semester — Shell chapter](https://missing.csail.mit.edu/2020/course-shell/) (~20 min).
> **Source:** [Week 1 Orientation Student Guide § Day 2](../../../../planning/source-material/Orientation/Orientation-Student-Guide.md).

---

## Why this matters

The shell is the interface between you and every system you'll touch this program: your laptop, the Capsule machines you connect to, the CI pipelines you'll trigger, the benchmarks you'll run. If you're slow in the shell, you're slow at everything.

## Readiness check

Five-question quiz on the MIT Missing Semester shell chapter. Sample items:

1. Navigate to `~/Downloads`. What command did you use?
2. Pipe `ls` into `grep` to list only Markdown files in the current directory.
3. What does `>` do, and how does it differ from `>>`?
4. What's the output of `echo $HOME`?
5. Make a script `hello.sh` executable. What command?

Below 3/5 → paired with a buddy.

## Core concept — Shell building blocks

| Concept | One-line definition | Example |
|---|---|---|
| `cd`, `pwd`, `ls` | Navigate the filesystem | `cd ~/Documents && ls -la` |
| Pipes `\|` | Send the output of one command into another | `ls \| wc -l` (count files) |
| Redirects `>`, `>>`, `<` | Send output to a file, append, or read from a file | `nvidia-smi > gpu.log` |
| `grep` | Filter lines matching a pattern | `ps aux \| grep python` |
| `awk` | Extract / process columns | `ls -la \| awk '{print $9}'` |
| `find` | Locate files by name / type / age | `find . -name "*.md" -mtime -1` |
| Globbing `*`, `?`, `[abc]` | Pattern-match filenames | `rm *.tmp` |
| Variables & `$()` | Capture values; run a command and use its output | `today=$(date +%F); echo $today` |
| Loops | Repeat over a list | `for f in *.csv; do wc -l "$f"; done` |
| Permissions `chmod` | Make a script executable | `chmod +x my_script.sh` |

### Worked example — extract GPU 0 utilization

```bash
nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits \
  | grep "^0," \
  | awk -F',' '{print $2}'
```

Each piece does one thing. Combined: a one-liner you'll use repeatedly in Week 9.

## Practice (90 min)

1. (15 min) Navigate: from `~`, get to `/tmp`, then to your home directory, then list all hidden files. Use `cd -` once.
2. (20 min) Parse `nvidia-smi` (or sample output from your facilitator): extract just GPU memory used per GPU.
3. (25 min) Write a 15-line bash script `disk_watch.sh` that prints disk usage of `/` every 10 seconds for one minute. Use `df`, a `for` loop, and `sleep`.
4. (20 min) Pair exercise: your partner reads your script aloud. If they can't predict every line's output, rewrite.
5. (10 min) Read [explainshell.com](https://explainshell.com) breakdowns of two cryptic one-liners your facilitator shares.

## Wrap-up

Each pair demos one shell trick they learned. Common one-liners go on the cohort cheat-sheet.

## Connect forward

Tomorrow: git. Version control is how multiple humans collaborate on the same shell-driven world without overwriting each other.

---

## Pre-read for tomorrow (Day 3 · Git Workflow)

- **Resource:** [Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min).
- **Reflection questions:**
  1. What's the difference between `git commit` and `git push`?
  2. Why is "always work on a branch, never directly on main" a near-universal convention?
  3. Write a commit message in conventional-commit format for: "I added a new function that reads GPU temperature."
