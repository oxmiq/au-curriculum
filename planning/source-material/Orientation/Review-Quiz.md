# Week 1 — Review Quiz

> **Format:** 15 questions. Low-stakes. Pass = 10/15. Below 10/15 = paired with a buddy for Week 2 Day 6.
> **Time:** 20 minutes.
> **No notes.** Open-book is for problem sets; quizzes are diagnostic.

---

## Section A — Shell & Linux (5 questions)

1. What does this command do?
   ```bash
   ls -la | grep ".md" | wc -l
   ```
   *Answer in one sentence.*

2. Write a one-liner that prints the second column of `/etc/passwd`, with `:` as the delimiter.

3. What's the difference between `>` and `>>` when redirecting output to a file?

4. Why would you use `chmod +x my_script.sh`?

5. What does `$(date +%F)` evaluate to today (June 3, 2026)?

---

## Section B — Git Workflow (5 questions)

6. What conventional-commit type would you use for each of these changes?
   - (a) Add a new benchmark script.
   - (b) Update the README.
   - (c) Fix a crash in the install script.
   - (d) Rename a function without changing behavior.
   - (e) Bump the version number.

7. Which of these is wrong, and why?
   - (a) `git checkout -b feat/new-thing`
   - (b) `git commit -m "wip"`
   - (c) `git push -u origin feat/new-thing`
   - (d) `git checkout main && git pull`

8. You committed to the wrong branch. You haven't pushed yet. Outline the recovery in three commands (no need for exact syntax — just the verbs).

9. What's a PR (Pull Request) for? Why not just push to `main`?

10. Your teammate's branch and `main` both touched the same line of the same file. What happens when you merge? What command shows you the conflict?

---

## Section C — GPU & AI Primer (5 questions)

11. In one sentence: why is a GPU faster than a CPU for matrix multiplication?

12. Roughly how much memory does an H100 GPU have? Roughly how fast is its memory bandwidth?

13. What's the difference between training and inference? Give two structural differences.

14. Number the following steps of the inference pipeline in order: `embed`, `sample`, `tokenize`, `layers`, `logits`.

15. True or false: a CPU is always worse than a GPU for AI workloads. Justify your answer in one sentence.

---

## Answer Key (instructor copy — do not distribute before quiz)

1. Counts the number of files / directory entries containing ".md" in the current directory.
2. `awk -F':' '{print $2}' /etc/passwd`
3. `>` truncates and writes; `>>` appends.
4. Marks the script as executable so the shell will run it directly (`./my_script.sh`).
5. `2026-06-03`.
6. (a) `feat:` (b) `docs:` (c) `fix:` (d) `refactor:` (e) `chore:`
7. (b) — `wip` is not a useful commit message. Use a conventional-commit format like `feat:` / `fix:` / `chore:` with a real description.
8. (1) `git branch <correct-branch>` to save the work to a new branch. (2) `git reset --hard HEAD~1` (or `HEAD~N`) to remove from current branch. (3) `git checkout <correct-branch>` to switch. (Many valid variants; accept any answer that preserves work and cleans the wrong branch.)
9. PRs invite review, run CI, and enforce branch protection. Direct push to `main` skips review and can break the shared branch.
10. A merge conflict — the merge stops and marks the conflicting region in the file. `git status` lists the conflicting files; `git diff` shows the conflict markers.
11. A GPU has thousands of parallel cores; matrix multiplication consists of independent multiply-adds that can be done in parallel.
12. 80 GB HBM3; 3.35 TB/s bandwidth.
13. Two of: training is rare/serving is continuous · training is throughput-only/serving is latency-sensitive · training is offline/serving is per-user real-time · training updates weights/serving just reads them.
14. `tokenize` → `embed` → `layers` → `logits` → `sample`.
15. False. CPUs are better for sequential / branch-heavy / small-batch work. GPUs are better only when the work is parallel and large enough to amortize the memory-transfer cost.

---

## Scoring

| Score | Action |
|---|---|
| 13–15 | Excellent — ready for Week 2. |
| 10–12 | Pass — review weak section before Monday. |
| 7–9 | Pair with a buddy for Week 2 Day 6. Office hours recommended. |
| ≤6 | One-on-one with facilitator on Friday afternoon. |
