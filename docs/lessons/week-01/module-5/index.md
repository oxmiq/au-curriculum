# Day 5 (Fri) · Week 1 Consolidation

> **Goal of the day:** consolidate Mon–Thu. No new content: practice, ask, catch up.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 1 - Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <span>Day 5 · Consolidation</span>
    {status:week-01/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This consolidation day is different from other days; it's for practice and review. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Week 1 Knowledge Check |
| Part 2 | Self-Assessment |
| Part 3 | Practice: Shell Review |
| Part 4 | Practice: Git Review |
| Part 5 | Practice: GPU Review |
| Part 6 | Open Lab & Wrap-up |

---

## Part 1 - Week 1 Knowledge Check
### Exercise: Take the Knowledge Check

[Take the Week 1 knowledge check](knowledge-check.md): 15 questions across shell, git, and GPU primer.

**Passing score:** 10/15 (67%)

If you score below 10/15:
- Review the questions you got wrong
- Go back to the relevant day's content
- Re-read that section
- Retake the quiz

---

## Part 2 - Self-Assessment
### Self-Check List

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m5-wrapup" data-kind="wrap-up" data-draw="5" data-source="Week 1 consolidation (shell, git, GPU)">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "Which command extracts a single field from nvidia-smi output?", "options": ["nvidia-smi | grep", "nvidia-smi | grep | awk", "nvidia-smi --query-gpu", "nvidia-smi | cut"], "answer": 1, "explain": "`nvidia-smi | grep | awk` chains grep and awk to extract specific fields from the output."},
  {"stem": "What is the correct sequence for a git workflow?", "options": ["Push → Commit → Branch", "Clone → Branch → Commit → Push", "Commit → Push → Branch", "Branch → Clone → Push"], "answer": 1, "explain": "The workflow is: clone the repo, create a branch, make commits, then push to share."},
  {"stem": "What does a conventional commit message look like?", "options": ["wip", "update", "feat: add user login", "fixed stuff"], "answer": 2, "explain": "Conventional commits use format: `type: description`. Use imperative mood and keep first line under 72 chars."},
  {"stem": "Why are GPUs faster than CPUs for neural networks?", "options": ["They have fewer cores", "Thousands of cores run matrix multiplication in parallel", "They use less power", "They are cheaper"], "answer": 1, "explain": "GPUs have thousands of small cores that can all run the same operation (matrix multiplication) simultaneously."},
  {"stem": "What are three differences between training and serving?", "options": ["Same thing", "Training is batch (throughput); serving is real-time (latency); training happens once, serving is continuous", "Training uses CPU; serving uses GPU", "No differences"], "answer": 1, "explain": "Training: batch, high throughput, one-time. Serving: single requests, low latency, continuous."},
  {"stem": "What are the two most-used H100 specs to remember?", "options": ["Core count and price", "80GB memory and 3.35 TB/s bandwidth", "TDP and color", "Weight and size"], "answer": 1, "explain": "Memory (80GB) and bandwidth (3.35 TB/s) are the most-referenced specs in practice."},
  {"stem": "What is the journey of a prompt? (Select the correct first step)", "options": ["Matrix multiplication", "Tokenization", "Embedding", "Sampling"], "answer": 1, "explain": "Step 1: Tokenization - convert text to token IDs on CPU."},
  {"stem": "What command creates a new branch with a commit?", "options": ["git new branch", "git checkout -b && git commit", "git branch create", "git init branch"], "answer": 1, "explain": "`git checkout -b` creates a branch, then you add and commit files."},
  {"stem": "What is the correct commit type for documentation?", "options": ["feat:", "fix:", "docs:", "chore:"], "answer": 2, "explain": "Use `docs:` for documentation-only changes."},
  {"stem": "What does `git push origin <branch>` do?", "options": ["Creates a new repo", "Uploads branch to remote", "Deletes branch", "Merges to main"], "answer": 1, "explain": "This uploads your local branch to the remote repository."},
  {"stem": "What is 'embarrassingly parallel'?", "options": ["A problem that's embarrassing", "Operations that can all run independently at the same time", "A GPU error", "A commit type"], "answer": 1, "explain": "Matrix multiplication is embarrassingly parallel; each calculation is independent."},
  {"stem": "What is the H100's memory capacity?", "options": ["16 GB", "80 GB", "32 GB", "8 GB"], "answer": 1, "explain": "H100 has 80 GB of HBM3 memory."},
  {"stem": "What is the H100's memory bandwidth?", "options": ["500 GB/s", "3.35 TB/s", "1 TB/s", "100 GB/s"], "answer": 1, "explain": "H100 has 3.35 TB/s memory bandwidth."},
  {"stem": "What does `git add . && git commit -m` do?", "options": ["Only stages", "Stages all changes and commits with message", "Pushes to remote", "Creates branch"], "answer": 1, "explain": "This stages all changes and commits them in one command chain."},
  {"stem": "What is a pull request?", "options": ["A git command", "A proposal to merge changes for review", "A backup", "A delete command"], "answer": 1, "explain": "A PR proposes merging your branch into main and invites code review."},
  {"stem": "What is the key GPU design fact?", "options": ["Few powerful cores", "Thousands of small cores for parallel work", "No cores", "Single core"], "answer": 1, "explain": "GPUs have thousands of small cores optimized for parallel operations like matrix multiplication."},
  {"stem": "What happens in transformer layers?", "options": ["Data storage", "Attention and feed-forward operations on GPU", "CPU processing", "Network transfer"], "answer": 1, "explain": "Transformer layers run on the GPU, processing vectors through attention and feed-forward networks."},
  {"stem": "What is sampling in inference?", "options": ["Reading from disk", "Picking next token from probability distribution", "Compressing data", "Saving output"], "answer": 1, "explain": "Sampling selects the next token from the probability distribution over the vocabulary."},
  {"stem": "What is the correct order of the prompt journey?", "options": ["GPU → CPU → Output", "Tokenize → Embed → Layers → Logits → Sample → Output", "Input → Output", "CPU only"], "answer": 1, "explain": "The journey: Tokenize (CPU) → Embed (GPU) → Layers (GPU) → Logits (GPU) → Sample (CPU/GPU) → Output."},
  {"stem": "What should you do if you can't do an item from memory?", "options": ["Skip it", "Review the relevant day's content and practice", "Ask someone else to do it", "Ignore it"], "answer": 1, "explain": "Note which day it came from, spend 10 minutes reviewing, then practice until you can do it from memory."}
]
</script>
</div>

### Action Items

For any item you can't do:

1. Note which day it came from
2. Spend 10 minutes reviewing that day's content
3. Practice until you can do it from memory

---

## Part 3 - Practice - Shell Review
### Hands-On: Shell Drills

Practice these until they're automatic:

```bash
# 1. Count files in a directory
ls | wc -l

# 2. Find all .md files
find . -name "*.md"

# 3. Parse nvidia-smi output
nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv

# 4. Write a simple loop
for i in {1..5}; do echo "Count: $i"; done

# 5. Make a script executable
chmod +x myscript.sh
```

### Practice Exercise

Write a script that:

1. Lists all files in `/tmp`
2. Counts how many there are
3. Prints "Found X files"

```bash
#!/bin/bash
count=$(ls /tmp | wc -l)
echo "Found $count files in /tmp"
```

---

## Part 4 - Practice - Git Review
### Hands-On: Git Drills

If you have a GitHub account, practice these:

1. **Clone a repo** (use any public repo)
```bash
git clone https://github.com/dgerman/English-to-French.git
```

2. **Create a branch and make a commit**
```bash
git checkout -b practice-branch
echo "practice" > practice.txt
git add .
git commit -m "feat: add practice file"
```

3. **Push to your fork**
```bash
git push origin practice-branch
```

4. **Clean up** (delete the branch after)
```bash
git checkout main
git branch -d practice-branch
```

### Git Cheat Sheet

| Action | Command |
|--------|---------|
| Check status | `git status` |
| See changes | `git diff` |
| Stage file | `git add ` |
| Stage all | `git add .` |
| Commit | `git commit -m "type: message"` |
| Push | `git push origin <branch>` |
| Create branch | `git checkout -b <branch>` |
| Switch branch | `git checkout <branch>` |

---

## Part 5 - Practice - GPU Review
### Hands-On: GPU Knowledge Check

Write your answers to these from memory (no notes!):

1. Why are GPUs faster than CPUs for neural networks?
2. What does "embarrassingly parallel" mean?
3. What's the difference between training and serving?
4. What are the three most important H100 specs?
5. Draw the journey of a prompt (6 steps)

Compare your answers to what you wrote on Day 4. Have you improved?

---

## Part 7 - Wrap-up & Connection
### What to Do

This is open time. Choose what you need:

1. **Catch up** on any assignments from Mon–Thu
2. **Ask questions** - use oxtutor or review the relevant day
3. **Extra practice** - generate more exercises on any concept
4. **Preview Week 2** - start the pre-reading for Day 6

### Connect Forward

Week 2 begins on Monday. You'll learn about:
- GPU hardware in detail
- Memory bottlenecks
- The journey of a prompt (in depth)

### Pre-read for Monday (Week 2, Day 6)

**Resource:** <a href="https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices" target="_blank" rel="noopener">Databricks - LLM Inference Performance Engineering</a> (read the inference-pipeline overview: prefill/decode, KV cache, batching).

**Reflection questions:**

1. Why is inference cumulatively more expensive than training?
2. Name one thing a CPU does better than a GPU.
3. What's the smallest unit of work in inference?

---

## Stuck?

Ask **oxtutor** to re-explain any Week-1 concept, or to generate extra practice questions grounded in the day's page.