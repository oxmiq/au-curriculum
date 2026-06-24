# Widget Conversion Plan — Week 01 (Days 1–4)

**Branch:** `feat/content-fortification`  
**Pre-reading sources:** Orientation Pre-Lecture-Reading.md (Day 1 only);
external URLs for Days 2–3; facilitator video for Day 4.  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Readiness widget? | Wrap-up widget? | Special |
|--------|-----|-------|-------------------|-----------------|---------|
| module-1 | 1 | Welcome & Context | ❌ no pre-reading | ✅ | Self-Check only |
| module-2 | 2 | Shell & Linux | ✅ | ✅ | External URL source |
| module-3 | 3 | Git Workflow | ✅ | ✅ | External URL source |
| module-4 | 4 | How Computers Run AI (GPU Primer) | ✅ | ✅ | No URL; infer from lesson body |

---

## module-1 — Day 1 · Welcome & Context

**File:** `docs/lessons/week-01/module-1/index.md`  
**Pre-reading:** None (first day).  
**Action:** Wrap-up widget only. Part 1 (`## Part 1 — Why This Matters · 10 min`)
is a content part — do not rename or restructure it.

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Wrap-up | `week-01-m1-wrapup` | `wrap-up` | `Day 1 · Welcome & Context` |

### Part structure (for wrap-up question sourcing)
- Part 1 — Why This Matters (the AI moment, Phase 1–3 framing)
- Part 2 — Core Concepts (the 3 pillars: inference, agents, Capsule)
- Part 3 — The 10-Week Journey (week-by-week roadmap)
- Part 4 — Hands-On: Research Capsule (independent research exercise)
- Part 5 — Hands-On: Write Your Summary (synthesis writing)
- Part 7 — Wrap-up & Connection

### Wrap-up question outline (20 questions — test Parts 1–5)
Author questions that probe:

**Recall (6):**
1. The three-pillar framing of the curriculum (inference engineering, AI agents, Capsule operations)
2. Which weeks cover which phase (Phase 1 = weeks 1–5, Phase 2 = weeks 6–7, Phase 3 = weeks 8–9, Capstone = week 10)
3. What "Capsule" is in one sentence
4. The distinction between model training and model inference
5. What the assessment structure is (quiz cadence, capstone weight)
6. The single concept-of-the-day stated in the lesson intro

**Apply (8):**
7. Classify a described task as Phase 1, 2, or 3 work
8. Given a job posting phrase, identify which phase's skills it maps to
9. Identify which week a student should revisit for a given skill gap
10. Choose the correct description of the capstone deliverable
11. Match each pillar to its primary tooling (inference → hardware/engines; agents → LLM+tools; Capsule → fleet ops)
12. Given a bottleneck description, identify whether it's a Phase 1 or Phase 2 concern
13. Identify which phase deals with "prompt engineering + ReAct loop"
14. Pick the accurate statement about what the curriculum does and does not teach

**Analyse (6):**
15. Why does Phase 1 (inference) come before Phase 2 (agents) in this curriculum?
16. A student skips Phase 1 and tries to benchmark in Week 9 — what knowledge gap do they hit?
17. Distinguish "AI in production" from "AI product management" — which is this curriculum?
18. Why is the capstone in Week 10 rather than Week 6?
19. Compare the role of Capsule in Phase 2 vs Phase 3
20. What makes "inference engineering" a distinct skill from "prompt engineering"?

### Insertion point (wrap-up widget)
Replace the `### Self-Check` block inside `## Part 7` (currently a checkbox
list beginning with `- [ ]`). The widget div immediately follows:
```
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" ...>
```

---

## module-2 — Day 2 · Shell & Linux

**File:** `docs/lessons/week-01/module-2/index.md`  
**Pre-reading:** [MIT Missing Semester — Shell chapter](https://missing.csail.mit.edu/2020/course-shell/) (~20 min)  
**Pre-reading source:** External URL. The lesson itself contains a full summary
of the pre-reading content in its frontmatter and Part 1 (`### Before You Start`).
Author readiness questions from the **lesson's own pre-reading summary** (the
three reflection questions in the frontmatter and Part 1 content).  
**data-source label:** `MIT Missing Semester — Shell chapter`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-01-m2-readiness` | `readiness` | `MIT Missing Semester — Shell chapter` |
| Wrap-up | `week-01-m2-wrapup` | `wrap-up` | `Day 2 · Shell & Linux` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts Deep Dive (~20 min): navigation, redirection, pipes, variables, scripting
- Part 3 — Hands-On: Navigation Exercises (~20 min)
- Part 4 — Hands-On: Data Processing (~30 min): grep, awk, pipelines
- Part 5 — Hands-On: Scripting (~30 min): bash scripts, chmod, loops
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — test MIT Missing Semester / pre-reading)
The pre-reading covers: navigating a filesystem from the shell, basic commands
(`ls`, `cd`, `pwd`, `cat`, `echo`), pipes and redirects, environment variables.
The lesson's own pre-reading section asks three reflection questions — build
from those and expand.

**Recall (6):**
1. What does `ls -la` show that `ls` does not?
2. What character represents the home directory in most shells?
3. What is a pipe (`|`) and what does it connect?
4. What does `>` do vs `>>`?
5. What is the purpose of `chmod +x` on a file?
6. What does an environment variable like `$PATH` control?

**Apply (8):**
7. Predict the output of `echo hello | tr a-z A-Z`
8. Given a command that fails with "Permission denied", identify the fix
9. Choose the correct command to count lines in a file
10. Which command shows the current working directory?
11. Given a pipe chain, identify which component filters lines
12. Select the command that appends output to an existing file
13. Identify what `grep -n` adds to grep's output
14. Given `./script.sh: Permission denied`, what is the most likely cause?

**Analyse (6):**
15. Why are small composable commands preferred over large monolithic ones in Unix philosophy?
16. A student types `cd Documents/project` but gets an error. What are the two most likely causes?
17. Why is the shell still the primary interface for engineers despite GUIs?
18. Compare `cat file.txt | grep pattern` vs `grep pattern file.txt` — which is preferred and why?
19. What is the practical difference between a relative path and an absolute path?
20. Why does `source script.sh` behave differently from `./script.sh`?

### Wrap-up question outline (20 questions — test Parts 2–5)
Parts 2–5 cover: navigation, file operations, pipes/redirects, grep/awk,
scripting basics, bash loops, and practical pipeline construction.

**Recall (6):**
1. Which command prints the contents of a file to stdout?
2. What does `wc -l` output?
3. What is the shebang line in a bash script?
4. What does `awk '{print $2}'` do to each line?
5. What does `&&` mean between two shell commands?
6. Which flag makes grep output only the matching part of a line?

**Apply (8):**
7. Write the pipeline to count occurrences of "error" in a log file
8. Given a for-loop skeleton, identify the correct syntax
9. Choose the correct redirect to discard stderr
10. Select the awk expression that sums a column of numbers
11. Identify the correct command to make a script executable and run it
12. Given a pipe chain with grep and sort, predict the output order
13. Which flag to `ls` sorts by modification time (newest first)?
14. Select the correct way to define and reference a bash variable

**Analyse (6):**
15. A pipeline produces no output even though the file has matching lines — name two likely causes
16. Why does the lesson recommend `set -e` at the top of scripts?
17. Compare `grep -v` and `grep` — when would you use each?
18. A student's script works in the terminal but fails when run with cron — most likely cause?
19. Why does variable quoting matter in bash (`"$var"` vs `$var`)?
20. Given two equivalent ways to process a file (awk vs Python), when is awk the better choice?

### Insertion points
**Readiness widget:** Replace the `### Readiness Check` paragraph text inside
`## Part 1 — Pre-Reading Review · 10 min`. The existing block starts with the
checkbox list `- [ ] Navigate between directories...`. Replace from
`### Self-Check` through the last `- [ ]` line with the widget div, and also
ensure the `### Readiness Check` heading with "Not gated..." intro precedes it
in Part 1.

**Wrap-up widget:** Replace the `### Self-Check` block inside `## Part 7`
(the checkbox list starting with `- [ ] Navigate between directories...`).

---

## module-3 — Day 3 · Git Workflow

**File:** `docs/lessons/week-01/module-3/index.md`  
**Pre-reading:** [Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min)  
**Pre-reading source:** External URL. Author readiness questions from the
lesson's own pre-reading summary (Part 1 content + frontmatter reflection
questions).  
**data-source label:** `Atlassian Git Tutorial — Basic Workflow`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-01-m3-readiness` | `readiness` | `Atlassian Git Tutorial — Basic Workflow` |
| Wrap-up | `week-01-m3-wrapup` | `wrap-up` | `Day 3 · Git Workflow` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts Deep Dive (~20 min): init/clone, add/commit, push/pull, branches, merge
- Part 3 — Conventional Commits (~15 min): type/scope/description format
- Part 4 — Hands-On: Git Workflow (~40 min): end-to-end commit cycle
- Part 5 — Hands-On: PR & Review (~30 min): pull request workflow
- Part 7 — Wrap-up & Connection (~15 min)

### Readiness question outline (20 questions — test Atlassian pre-reading)
The Atlassian tutorial covers: `git init`, `git add`, `git commit`, staging
area, `git status`, `git log`, working directory vs index vs HEAD.

**Recall (6):**
1. What does `git add` do to a file?
2. What is the "staging area" (index) in Git?
3. What does `git status` show?
4. What does `git commit -m` do?
5. What is the difference between a tracked and untracked file?
6. What does `git log --oneline` display?

**Apply (8):**
7. A file is modified but not staged — which command stages it?
8. Given `git status` output, identify which files are ready to commit
9. Choose the correct sequence: modify file → stage → commit
10. After `git init`, what is the state of all existing files?
11. Identify the command to undo a `git add` before committing
12. Select the correct interpretation of a `git diff` output
13. Which command shows the history of commits on the current branch?
14. Given a commit message "fixed bug", identify why it's a poor message

**Analyse (6):**
15. Why does Git separate staging (`git add`) from committing (`git commit`)?
16. Compare `git diff` vs `git diff --staged` — what does each show?
17. A student runs `git commit` without `git add` — what happens?
18. Why is a short, descriptive commit message better than a long one?
19. What information does the staging area preserve that the working directory does not?
20. Why is git "distributed" rather than "centralised" — what does that mean operationally?

### Wrap-up question outline (20 questions — test Parts 2–5)
Parts 2–5 cover: full commit cycle, branch creation/switching, merge,
Conventional Commits format (type/scope/description), PR workflow, code review.

**Recall (6):**
1. What are the four required Conventional Commit types used in this curriculum?
2. What does `git checkout -b` do?
3. What is a pull request and what does it signal to the team?
4. What does `git merge` produce when there are no conflicts?
5. What is the difference between `git push origin main` and `git push`?
6. What does the `feat:` prefix in a commit message indicate?

**Apply (8):**
7. Given a task "add a new CLI flag", write the correct Conventional Commit prefix
8. Identify the correct branch name for a bug-fix per this curriculum's convention
9. Given a merge conflict marker, identify which section is "ours" vs "theirs"
10. Select the correct command to create a branch AND switch to it in one step
11. Given a PR description, identify what is missing per good practice
12. Which git command integrates remote changes into the local branch?
13. Select the correct commit message format from four candidates
14. Given `git log` output, identify the most recent commit hash

**Analyse (6):**
15. Why does this curriculum use Conventional Commits instead of freeform messages?
16. A student commits directly to `main` instead of a branch — what problems does this create?
17. Compare `git merge` and `git rebase` at a high level — which does this curriculum use and why?
18. Why should a PR cover one concern rather than many?
19. What is the purpose of a code review in a PR, beyond catching bugs?
20. A student's push is rejected with "non-fast-forward" — what does this mean and how is it resolved?

### Insertion points
Same pattern as module-2: Readiness widget in Part 1 (replace existing
`### Self-Check` checkbox block), Wrap-up widget in Part 7.

---

## module-4 — Day 4 · How Computers Run AI (GPU Primer)

**File:** `docs/lessons/week-01/module-4/index.md`  
**Pre-reading:** "15-min video on what a GPU is (facilitator shares link)"  
**Pre-reading source:** No accessible URL. The lesson body (Parts 2–4) covers
the same GPU primer content the video introduces. Author readiness questions
from the **lesson's own GPU primer content** (the video is assumed to cover
the same material). This is acceptable because the readiness widget is testing
"what the student should know before Parts 2–5 deep dives", which is exactly
what Part 2's "Core Concepts — CPU vs GPU" covers at the surface level.  
**data-source label:** `GPU Primer video (facilitator-shared)`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-01-m4-readiness` | `readiness` | `GPU Primer video (facilitator-shared)` |
| Wrap-up | `week-01-m4-wrapup` | `wrap-up` | `Day 4 · How Computers Run AI` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: CPU vs GPU (~20 min): parallelism, cores, use cases
- Part 3 — Deep Dive: The Numbers (~15 min): FLOPS, memory bandwidth, H100 spec
- Part 4 — Deep Dive: Journey of a Prompt (~20 min): tokenisation → prefill → decode → output
- Part 5 — Hands-On: GPU Comparison (~25 min): compare GPU classes on key metrics
- Part 6 — Hands-On: Draw the Path (~20 min): sketch the inference pipeline
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — test video / surface GPU primer)
The 15-min video is assumed to cover: what a GPU is, why it is different from
a CPU, that GPUs have thousands of cores, that AI training/inference uses GPUs
heavily. Author questions at the "just watched a 15-min intro video" level.

**Recall (6):**
1. Roughly how many cores does a modern CPU have vs a GPU?
2. What type of operations are GPUs specifically optimised for?
3. What does "FLOPS" stand for and what does it measure?
4. What is the primary difference between training a neural network and running inference?
5. What is HBM (High Bandwidth Memory) and where is it found?
6. Name one GPU that is widely used for large language model inference.

**Apply (8):**
7. A task requires sequential logic with many branches — CPU or GPU?
8. A task requires multiplying large matrices in parallel — CPU or GPU?
9. Given "a model with 7 billion parameters in FP16", estimate the minimum GPU memory needed
10. Classify: "tokenising text" — is this compute-bound or memory-bound?
11. Which hardware unit executes the bulk of a transformer's matrix multiplications?
12. A GPU has 80 GB HBM and 3.35 TB/s bandwidth — which stat matters more for inference?
13. Identify the GPU generation that introduced NVLink 4 and transformer engines
14. Select the correct description of "throughput" vs "latency" in the GPU context

**Analyse (6):**
15. Why are GPUs better than CPUs for matrix multiplication specifically?
16. A model that fits on a CPU still runs faster on a GPU — why?
17. Compare "training" and "inference" in terms of which phase is more memory-bandwidth bound
18. Why does adding more CPU cores beyond ~64 not proportionally speed up LLM inference?
19. Given that a GPU has 10× more cores than a CPU, why isn't inference 10× faster?
20. What is the relationship between model precision (FP32 vs FP16) and GPU memory usage?

### Wrap-up question outline (20 questions — test Parts 2–6)
Parts 2–6 cover: CPU vs GPU parallelism, FLOPS/bandwidth specs, H100 numbers,
prompt→token→prefill→decode→output pipeline, GPU class comparison.

**Recall (6):**
1. What are the three numbers the lesson says you should memorise about the H100?
2. What is "prefill" in the context of LLM inference?
3. What is "decode" in the context of LLM inference?
4. How many tokens does decode produce per step?
5. What does "embarrassingly parallel" mean?
6. What is the lesson's one-line definition of a "tensor"?

**Apply (8):**
7. Given H100 specs, calculate the memory bandwidth in TB/s
8. A model generates 500 output tokens — how many decode steps occur?
9. Classify each phase (prefill, decode) as compute-bound or memory-bound
10. Given a GPU comparison table, identify the best GPU for latency-sensitive inference
11. Map each stage (tokenise → embed → prefill → decode → detokenise) to its hardware bottleneck
12. A student runs a 7B model on a GPU with 16 GB VRAM in FP16 — does it fit? Show working.
13. Which metric is more important for a batch-processing workload: TTFT or throughput?
14. Select the correct interpretation of "H100 has 3.35 TB/s HBM bandwidth"

**Analyse (6):**
15. Why is decode slower per token than prefill, despite producing only one token at a time?
16. A team doubles the batch size — how does this affect TTFT and throughput?
17. Compare the H100 and A100 on the three key metrics from Part 3
18. Why does the "journey of a prompt" mental model matter for debugging latency issues?
19. Given two GPUs with equal FLOPS but different memory bandwidth, which is better for LLM serving and why?
20. The lesson says prefill is "one big parallel matmul" — why is decode fundamentally different?

### Insertion points
Same as module-2/module-3. Note: module-4 has **6 content parts** (Parts 1–6
+ Part 7) — the lesson-plan table has 6 rows before the wrap-up. When
replacing the self-check block in Part 7, verify the heading is
`## Part 7 — Wrap-up & Connection` (not Part 8).

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] module-1: add wrap-up widget only (no readiness)
- [ ] module-2: add both widgets; external pre-reading source; infer readiness Qs from Part 1 summary
- [ ] module-3: add both widgets; external pre-reading source
- [ ] module-4: add both widgets; no URL — use lesson body as readiness source
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: `git commit -m "feat(quiz): add readiness + wrap-up widgets to Day N · <title>"`
- [ ] After all 4 modules: run `python3 scripts/audit_lessons.py` — should still be 0 violations
