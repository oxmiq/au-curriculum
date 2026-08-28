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
### Action Items

For any question you missed on the Week 1 knowledge check:

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