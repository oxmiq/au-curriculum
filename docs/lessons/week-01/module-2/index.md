# Day 2 · Shell & Linux

> **Concept of the day:** The shell as your primary tool. Pipes, redirects, grep, awk, basic scripting.<br>
> **Pre-reading:** <a href="https://missing.csail.mit.edu/2020/course-shell/" target="_blank" rel="noopener">MIT Missing Semester - Shell chapter</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 - Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 2 · Shell & Linux</span>
    {status:week-01/module-2}
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
| Part 3 | Hands-On: Navigation Exercises |
| Part 4 | Hands-On: Data Processing |
| Part 5 | Hands-On: Scripting |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: <a href="https://missing.csail.mit.edu/2020/course-shell/" target="_blank" rel="noopener">MIT Missing Semester - Shell chapter</a>.

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m2-readiness" data-kind="readiness" data-draw="5" data-source="MIT Missing Semester - Shell chapter">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does <code>ls -la</code> show that plain <code>ls</code> does not?", "options": ["Only hidden files whose names begin with a dot", "File permissions, owner, size, timestamps, and hidden entries", "File contents displayed in long format", "Files sorted by modification time, newest first"]},
  {"stem": "What does <code>echo hello | tr a-z A-Z</code> print?", "options": ["hello", "HELLO", "a-z A-Z", "HELLO followed by hello on the next line"]},
  {"stem": "What does a pipe (<code>|</code>) connect in a shell pipeline?", "options": ["Two files so they are read in sequence", "A command to a remote host over SSH", "The standard output of one command to the standard input of the next", "The standard error of one command to the standard output of the next"]},
  {"stem": "What is the difference between <code>&gt;</code> and <code>&gt;&gt;</code> when redirecting output to a file?", "options": ["<code>&gt;</code> appends to the file; <code>&gt;&gt;</code> overwrites it", "Both truncate the target file before writing", "<code>&gt;</code> overwrites (or creates) the file; <code>&gt;&gt;</code> appends without truncating", "<code>&gt;</code> redirects stdout; <code>&gt;&gt;</code> redirects both stdout and stderr"]},
  {"stem": "A student runs <code>./script.sh</code> and sees <code>bash: ./script.sh: Permission denied</code>. What is the most likely fix?", "options": ["Run <code>sudo rm script.sh</code> to remove and recreate the file", "Run <code>chmod +x script.sh</code> to add the execute permission bit", "Add <code>#!/bin/bash</code> to the first line of the script", "Move the script to <code>/usr/local/bin/</code>"]},
  {"stem": "What does the environment variable <code>$PATH</code> control?", "options": ["The current working directory", "The location of the user’s home directory", "The default editor used by shell commands", "The list of directories the shell searches when resolving a command name"]},
  {"stem": "Which character is the shell shortcut for the current user’s home directory?", "options": ["<code>/</code>", "<code>~</code>", "<code>.</code>", "<code>*</code>"]},
  {"stem": "Which command correctly counts the number of lines in a file named <code>results.log</code>?", "options": ["<code>count -lines results.log</code>", "<code>cat -n results.log</code>", "<code>ls -l results.log</code>", "<code>wc -l results.log</code>"]},
  {"stem": "Which command prints the absolute path of the current working directory?", "options": ["<code>cwd</code>", "<code>echo $CWD</code>", "<code>pwd</code>", "<code>ls -d .</code>"]},
  {"stem": "A student wants to append the output of <code>date</code> to an existing file <code>log.txt</code> without erasing its current content. Which command achieves this?", "options": ["<code>date &gt; log.txt</code>", "<code>date | log.txt</code>", "<code>date -a log.txt</code>", "<code>date &gt;&gt; log.txt</code>"]},
  {"stem": "In the pipeline <code>ps aux | grep python | awk '{print $2}'</code>, which component is responsible for filtering lines?", "options": ["<code>ps aux</code>", "<code>awk '{print $2}'</code>", "The pipe <code>|</code> itself", "<code>grep python</code>"]},
  {"stem": "What does the <code>-n</code> flag add to <code>grep</code>’s default output?", "options": ["The count of total matching lines", "The line number prefixed to each matching line", "A negation — it prints lines that do <em>not</em> match", "The filename prefixed before each match"]},
  {"stem": "Why does Unix philosophy favour small, composable commands over large monolithic programs?", "options": ["Small programs have smaller binary sizes, reducing disk usage", "Unix kernel scheduling is more efficient with many small processes", "Small commands can be combined via pipes to solve new problems without writing new programs", "Small programs cannot be run as root, improving security through privilege separation"]},
  {"stem": "A student types <code>cd Documents/project</code> and gets “No such file or directory.” Which two causes are most likely?", "options": ["The <code>cd</code> command requires an absolute path starting with <code>/</code>", "The path is relative and <code>Documents</code> does not exist in the current directory, or the name has different capitalisation", "The user lacks read permission on the home directory", "The terminal session has not been restarted since the directory was created"]},
  {"stem": "Why is the shell still the primary interface for engineers, even though graphical tools exist?", "options": ["Shell commands execute faster because the kernel gives them higher scheduling priority", "Shell commands are scriptable, repeatable, and composable — and they run on remote headless servers where no GUI is available", "GUIs cannot display text output from tools like <code>nvidia-smi</code>", "Company IT policies generally prohibit GUI tools on production servers"]},
  {"stem": "Compare <code>cat file.txt | grep pattern</code> and <code>grep pattern file.txt</code>. Which is generally preferred and why?", "options": ["<code>cat file.txt | grep pattern</code> — the pipe form is more readable", "<code>grep pattern file.txt</code> — it avoids a needless <code>cat</code> process", "Both are identical in every respect including process overhead", "<code>cat file.txt | grep pattern</code> — <code>grep</code> cannot accept filenames in all shells"]},
  {"stem": "What is the practical difference between a relative path and an absolute path?", "options": ["Absolute paths are faster because the kernel skips a <code>pwd</code> lookup", "Relative paths work only inside the home directory; absolute paths work everywhere", "Relative paths can contain <code>..</code> but absolute paths cannot", "A relative path resolves from the current working directory; an absolute path always resolves from the filesystem root <code>/</code>"]},
  {"stem": "Why does <code>source script.sh</code> behave differently from <code>./script.sh</code>?", "options": ["<code>source</code> runs the script in the current shell process, so variable assignments and directory changes persist; <code>./</code> spawns a child process whose environment is discarded on exit", "<code>source</code> requires the execute bit set; <code>./</code> does not", "<code>./</code> executes the script as root; <code>source</code> runs it as the current user", "<code>source</code> works only with Python scripts; <code>./</code> works with any executable"]},
  {"stem": "What does the <code>$()</code> notation do in a shell command such as <code>today=$(date +%F)</code>?", "options": ["Defines a mathematical expression to evaluate", "Groups multiple commands for parallel execution", "Performs command substitution — runs the enclosed command and substitutes its stdout into the surrounding expression", "Creates a subshell that inherits but cannot modify the parent’s variables"]},
  {"stem": "A student wants to view the contents of <code>notes.txt</code> without opening an interactive editor. Which command is correct?", "options": ["<code>vim notes.txt</code>", "<code>touch notes.txt</code>", "<code>cat notes.txt</code>", "<code>echo notes.txt</code>"]}
]
</script>
</div>

---

## Part 2 - Core Concepts Deep Dive
### Reading - Shell Building Blocks

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

### Worked Example - Extract GPU 0 Utilization

This is a real-world example you'll use in Week 9 when benchmarking:

```bash
nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits \
  | grep "^0," \
  | awk -F',' '{print $2}'
```

**Breakdown:**

1. `nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits`: queries GPU info in CSV format
2. `grep "^0,"`: filters to only lines starting with "0," (GPU 0)
3. `awk -F',' '{print $2}'`: splits by comma and prints the second field (utilization)

Each piece does one thing. Combined: a one-liner you'll use repeatedly in Week 9.

---

## Part 3 - Hands-On - Navigation Exercises
### Exercise 1: Basic Navigation

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

### Exercise 2: Directory Exploration

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

## Part 4 - Hands-On - Data Processing
### Exercise 1: Pipes and Filters

```bash
# Count files in current directory
ls | wc -l

# List only directories
ls -la | grep "^d"

# List only Markdown files
ls | grep "\.md$"
```

### Exercise 2: Process GPU Output

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

## Part 5 - Hands-On - Scripting
### Exercise: Write disk_watch.sh

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

### Make it Executable

```bash
chmod +x disk_watch.sh
./disk_watch.sh
```

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 2 · Shell &amp; Linux">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does <code>awk '{print $2}'</code> do to each line of input?", "options": ["Prints the entire line unchanged", "Prints the second whitespace-delimited field of each line", "Prints lines that contain the literal string <code>$2</code>", "Counts the number of fields in each line"]},
  {"stem": "Which of the following is the correct shebang line for a bash script?", "options": ["<code># /bin/bash</code>", "<code>#! bash</code>", "<code>#!/bin/bash</code>", "<code>//bin/bash execute</code>"]},
  {"stem": "In the worked example <code>nvidia-smi ... | grep \"^0,\" | awk -F',' '{print $2}'</code>, what does <code>-F','</code> tell awk?", "options": ["To filter only lines that start with a comma", "To use comma as the field delimiter instead of whitespace", "To print the second line of each record", "To format the output as comma-separated values"]},
  {"stem": "What does the <code>&amp;&amp;</code> operator do between two shell commands?", "options": ["Runs both commands in parallel background processes", "Runs the second command only if the first exits with a zero (success) status", "Pipes the stdout of the first command into the second", "Runs the second command regardless of the first command’s exit status"]},
  {"stem": "What does <code>mkdir -p ~/practice/shell/{data,scripts,output}</code> create?", "options": ["A single directory literally named <code>{data,scripts,output}</code>", "Three directories — <code>data</code>, <code>scripts</code>, and <code>output</code> — inside <code>~/practice/shell/</code>, creating all intermediate directories if needed", "A compressed archive of three directories", "Three symbolic links inside <code>~/practice/shell/</code>"]},
  {"stem": "What does <code>wc -l</code> report when given a file?", "options": ["The number of words in the file", "The number of characters in the file", "The number of lines (newlines) in the file", "The file size in bytes"]},
  {"stem": "Which pipeline counts the number of entries in the current directory?", "options": ["<code>find . | grep count</code>", "<code>ls -la | grep total</code>", "<code>ls | wc -l</code>", "<code>count * -r</code>"]},
  {"stem": "Which glob pattern matches all files whose name ends in <code>.tmp</code>?", "options": ["<code>[.tmp]</code>", "<code>?.tmp</code>", "<code>*.tmp</code>", "<code>.tmp*</code>"]},
  {"stem": "A student has just written <code>disk_watch.sh</code>. What is the correct two-step sequence to make it executable and run it?", "options": ["<code>add-exec disk_watch.sh &amp;&amp; ./disk_watch.sh</code>", "<code>exec disk_watch.sh</code>", "<code>chmod +x disk_watch.sh &amp;&amp; ./disk_watch.sh</code>", "<code>bash -x disk_watch.sh</code>"]},
  {"stem": "What does <code>today=$(date +%F); echo $today</code> print when run on 2026-06-24?", "options": ["<code>today=2026-06-24</code>", "<code>$today</code>", "<code>date +%F</code>", "<code>2026-06-24</code>"]},
  {"stem": "What does the <code>&lt;</code> redirect operator do?", "options": ["Appends a file’s contents to a command’s output", "Sends a command’s stdout into a file", "Feeds a file’s contents into a command’s standard input", "Compares the outputs of two commands"]},
  {"stem": "Which command from Part 4 Exercise 1 lists only directories (not regular files) in the current directory?", "options": ["<code>ls -d</code>", "<code>ls -la | grep \"^d\"</code>", "<code>find . -type d -maxdepth 1</code>", "<code>ls --dirs-only</code>"]},
  {"stem": "In the Part 5 <code>disk_watch.sh</code> starter script, what does the <code>df -h /</code> command report on each loop iteration?", "options": ["The number of files stored in the root directory", "Human-readable disk-space usage of the root filesystem <code>/</code>", "The current CPU utilization percentage", "The total amount of RAM installed on the machine"]},
  {"stem": "In <code>ls -la | grep \"^d\"</code>, why does the pattern <code>^d</code> correctly identify directories?", "options": ["<code>ls -la</code> always places directory names at the top, and <code>^d</code> marks the first entry", "In <code>ls -la</code> long format, the first character of each line’s permission string is <code>d</code> for directories and <code>-</code> for regular files", "<code>^d</code> is a special <code>ls</code> flag abbreviation standing for <em>directory</em>", "The letter <code>d</code> stands for <em>date</em>, filtering lines with today’s date"]},
  {"stem": "Which command locates all Markdown files modified within the last day, as shown in the Part 2 Core Concepts Table?", "options": ["<code>grep -r \".md\" . --age=1</code>", "<code>ls -la *.md</code>", "<code>find . -name \"*.md\" -mtime -1</code>", "<code>find . -type md -days 1</code>"]},
  {"stem": "Why is the pipeline <code>nvidia-smi ... | grep \"^0,\" | awk -F',' '{print $2}'</code> structured as three separate commands?", "options": ["Running three processes in parallel reduces total execution time", "Each command does one focused job — query, filter, extract — making each step readable and independently testable", "<code>nvidia-smi</code> cannot produce output that <code>awk</code> reads directly", "<code>grep</code> and <code>awk</code> cannot appear in the same pipeline"]},
  {"stem": "In the <code>disk_watch.sh</code> starter script, what is the purpose of <code>sleep 10</code>?", "options": ["It waits for disk I/O to complete before sampling usage", "It pauses execution for 10 seconds between loop iterations", "It limits the script to 10 seconds of total CPU time", "It suspends the disk spindle to reduce wear"]},
  {"stem": "A pipeline <code>cat big_log.txt | grep ERROR | sort | uniq -c</code> produces no output, but the file contains matching lines. Which two causes are most likely?", "options": ["The file is too large for <code>grep</code> to process, and <code>sort</code> cannot handle pipe input", "The pattern is case-sensitive so <code>ERROR</code> does not match <code>error</code>, or the file has Windows-style carriage returns that prevent the match", "<code>grep</code> requires <code>-r</code> when reading from a pipe, and <code>uniq</code> requires a pre-sorted file", "<code>cat</code> rewrites line endings before <code>grep</code> sees them, discarding ERROR lines"]},
  {"stem": "What does <code>for f in *.csv; do wc -l \"$f\"; done</code> accomplish?", "options": ["Counts all lines across all CSV files and prints a single combined total", "Runs <code>wc -l</code> on each <code>.csv</code> file in the current directory and prints a separate line count for each", "Searches inside each CSV file for lines containing the literal string <code>wc</code>", "Creates a new file named <code>f</code> for each CSV in the directory"]},
  {"stem": "A student runs <code>cd -</code> in Part 3 Exercise 1 after navigating from home to <code>/tmp</code> and back. What does <code>cd -</code> do?", "options": ["Deletes the current directory", "Navigates to the parent directory, equivalent to <code>cd ..</code>", "Returns to the previously visited directory (<code>$OLDPWD</code>), toggling between two locations", "Resets the shell environment to the default home directory"]}
]
</script>
</div>

### Connect Forward

Tomorrow: git. Version control is how multiple humans collaborate on the same shell-driven world without overwriting each other.

### Pre-read for tomorrow (Day 3 · Git Workflow)

- **Resource:** <a href="https://www.atlassian.com/git/tutorials/saving-changes" target="_blank" rel="noopener">Atlassian - Saving Changes</a> + <a href="https://www.atlassian.com/git/tutorials/using-branches" target="_blank" rel="noopener">Using Branches</a> + <a href="https://www.atlassian.com/git/tutorials/syncing" target="_blank" rel="noopener">Syncing</a>.
- **Reflection questions:**
  1. What's the difference between `git commit` and `git push`?
  2. Why is "always work on a branch, never directly on main" a near-universal convention?
  3. Write a commit message in conventional-commit format for: "I added a new function that reads GPU temperature."

---

## Stuck?

Ask **oxtutor**: share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
