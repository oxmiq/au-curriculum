# Day 2 · Shell & Linux

> **Concept of the day:** The shell as your primary tool. Pipes, redirects, grep, awk, basic scripting.<br>
> **Pre-reading:** [MIT Missing Semester — Shell chapter](https://missing.csail.mit.edu/2020/course-shell/) (~20 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 — Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 2 · Shell & Linux</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-01/module-2}
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
| Part 3 | Hands-On: Navigation Exercises | 20 min |
| Part 4 | Hands-On: Data Processing | 30 min |
| Part 5 | Hands-On: Scripting | 30 min |
| 7 | Wrap-up & Connection | 10 min |

---

## Part 1 — Pre-Reading Review · 10 min
### Before You Start

You should have already read: [MIT Missing Semester — Shell chapter](https://missing.csail.mit.edu/2020/course-shell/) (~20 min).

### Quick Self-Check

Answer these questions from memory:
1. What's the difference between `ls` and `ls -la`?
2. What's the home directory shortcut?
3. How do you view the current working directory?

If you couldn't answer all three, review the MIT Missing Semester chapter again before proceeding.

---

## Part 2 — Core Concepts Deep Dive · 20 min
### Reading — Shell Building Blocks

The shell is the interface between you and every system you'll touch this program: your laptop, the Capsule machines you connect to, the CI pipelines you'll trigger, the benchmarks you'll run. If you're slow in the shell, you're slow at everything.

### Core Concepts Table

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

### Worked Example — Extract GPU 0 Utilization

This is a real-world example you'll use in Week 9 when benchmarking:

```bash
nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits \
  | grep "^0," \
  | awk -F',' '{print $2}'
```

**Breakdown:**
1. `nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits` — queries GPU info in CSV format
2. `grep "^0,"` — filters to only lines starting with "0," (GPU 0)
3. `awk -F',' '{print $2}'` — splits by comma and prints the second field (utilization)

Each piece does one thing. Combined: a one-liner you'll use repeatedly in Week 9.

---

## Part 3 — Hands-On — Navigation Exercises · 20 min
### Exercise 1: Basic Navigation (10 min)

Practice these commands in order:

```bash
# 1. Go to your home directory
cd ~

# 2. Go to /tmp
cd /tmp

# 3. Go back to home
cd ~

# 4. List all files including hidden ones
ls -la

# 5. Go back to the previous directory
cd -
```

### Exercise 2: Directory Exploration (10 min)

Create this directory structure and navigate through it:

```bash
# Create practice directories
mkdir -p ~/practice/shell/{data,scripts,output}

# Navigate into each and create a marker file
cd ~/practice/shell/data && touch readme.txt
cd ../scripts && touch myscript.sh
cd ../output && touch results.log

# Verify with tree (or ls -R)
ls -R ~/practice/shell
```

---

## Part 4 — Hands-On — Data Processing · 30 min
### Exercise 1: Pipes and Filters (10 min)

```bash
# Count files in current directory
ls | wc -l

# List only directories
ls -la | grep "^d"

# List only Markdown files
ls | grep "\.md$"
```

### Exercise 2: Process GPU Output (20 min)

If you have `nvidia-smi` available, run:
```bash
nvidia-smi
```

Then parse it to extract:
1. All GPU indices
2. Memory used per GPU
3. GPU utilization per GPU

**Hint:** Use `--query-gpu` flag for structured output:
```bash
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv
```

If you don't have nvidia-smi, use this sample output:
```
0, Tesla H100, 16384 MiB, 81920 MiB, 45 %
1, Tesla H100, 32768 MiB, 81920 MiB, 78 %
2, Tesla H100, 16384 MiB, 81920 MiB, 32 %
```

Parse it to extract just the GPU index and utilization.

---

## Part 5 — Hands-On — Scripting · 30 min
### Exercise: Write disk_watch.sh (25 min)

Write a bash script `disk_watch.sh` that:
1. Prints disk usage of `/` every 10 seconds
2. Runs for one minute (6 iterations)
3. Uses `df`, a `for` loop, and `sleep`

**Starter code:**
```bash
#!/bin/bash
# disk_watch.sh - Monitor disk usage every 10 seconds

for i in {1..6}
do
    echo "=== Iteration $i ==="
    df -h /
    sleep 10
done
```

**Your task:** Add timestamps and make the output more informative.

### Make it Executable (5 min)

```bash
chmod +x disk_watch.sh
./disk_watch.sh
```

---

## Part 7 — Wrap-up & Connection · 10 min
### Self-Check

Can you do these from memory?
- [ ] Navigate between directories using `cd`
- [ ] Pipe output from one command to another
- [ ] Redirect output to a file
- [ ] Parse structured output with `grep` and `awk`
- [ ] Write and execute a bash script

### Connect Forward

Tomorrow: git. Version control is how multiple humans collaborate on the same shell-driven world without overwriting each other.

### Pre-read for tomorrow (Day 3 · Git Workflow)

- **Resource:** [Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min).
- **Reflection questions:**
  1. What's the difference between `git commit` and `git push`?
  2. Why is "always work on a branch, never directly on main" a near-universal convention?
  3. Write a commit message in conventional-commit format for: "I added a new function that reads GPU temperature."

---

## Stuck?

Ask **oxtutor** — share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
