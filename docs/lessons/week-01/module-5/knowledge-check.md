<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 1 — Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <a href="../">Day 5 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-01/module-5}
  </div>
</div>

# Week 1 Knowledge Check

**Week 1 · Orientation.** 18 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-01-m5-canonical" data-kind="wrap-up" data-draw="18" data-lesson="Week 1 · Orientation" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What does <code>ls -la | grep '.md' | wc -l</code> do?",
    "options": [
      "Lists every Markdown file in the directory",
      "Counts every entry whose name (or details) contains '.md'",
      "Deletes Markdown files",
      "Opens Markdown files in a pager"
    ],
    "answer": 1,
    "explain": "ls -la lists everything; grep filters lines containing '.md'; wc -l counts the surviving lines."
  },
  {
    "stem": "Which one-liner prints the second <code>:</code> -delimited field of <code>/etc/passwd</code>?",
    "options": [
      "<code>cut -f2 /etc/passwd</code>",
      "<code>awk -F':' '{print $2}' /etc/passwd</code>",
      "<code>grep ':' /etc/passwd | head -2</code>",
      "<code>sed 's/:/ /' /etc/passwd</code>"
    ],
    "answer": 1,
    "explain": "awk with -F':' sets the field separator; $2 is the second column."
  },
  {
    "stem": "What's the difference between <code>></code> and <code>>></code> when redirecting to a file?",
    "options": [
      "No difference",
      "<code>></code> appends; <code>>></code> truncates",
      "<code>></code> truncates and writes; <code>>></code> appends",
      "<code>></code> writes to stderr; <code>>></code> writes to stdout"
    ],
    "answer": 2,
    "explain": "Single arrow replaces file contents; double arrow appends to whatever is already there."
  },
  {
    "stem": "Why would you run <code>chmod +x my_script.sh</code>?",
    "options": [
      "To make the file readable",
      "To mark the script executable so you can run it directly",
      "To compress the script",
      "To attach it to a cron job"
    ],
    "answer": 1,
    "explain": "+x adds the execute bit; without it you'd need to invoke an interpreter explicitly."
  },
  {
    "stem": "What does <code>$(date +%F)</code> evaluate to?",
    "options": [
      "The literal string <code>date +%F</code>",
      "Today's date in <code>YYYY-MM-DD</code> format",
      "An error",
      "The current Unix timestamp"
    ],
    "answer": 1,
    "explain": "$( ... ) runs the command and substitutes its output; %F is the ISO date format."
  },
  {
    "stem": "Which conventional-commit type fits 'Add a new benchmark script'?",
    "options": [
      "<code>docs:</code>",
      "<code>fix:</code>",
      "<code>feat:</code>",
      "<code>chore:</code>"
    ],
    "answer": 2,
    "explain": "New functionality is <code>feat:</code>."
  },
  {
    "stem": "Which of these is the WRONG thing to do?",
    "options": [
      "<code>git checkout -b feat/new-thing</code>",
      "<code>git commit -m \"wip\"</code>",
      "<code>git push -u origin feat/new-thing</code>",
      "<code>git checkout main && git pull</code>"
    ],
    "answer": 1,
    "explain": "<code>wip</code> is not a useful commit message — use conventional-commit format with a real description."
  },
  {
    "stem": "You committed to the wrong branch, haven't pushed yet. The cleanest recovery is:",
    "options": [
      "Force-push to main and hope",
      "Create the correct branch from current HEAD, then <code>git reset --hard HEAD~1</code> on the wrong branch",
      "Delete the repo and re-clone",
      "Open a PR from the wrong branch"
    ],
    "answer": 1,
    "explain": "Preserve the work on a new branch first, then rewind the wrong branch."
  },
  {
    "stem": "Why do teams use PRs instead of pushing straight to <code>main</code>?",
    "options": [
      "PRs are required by GitHub for free accounts",
      "To invite review, run CI, and enforce branch protection",
      "PRs are faster than direct pushes",
      "PRs avoid the need for commit messages"
    ],
    "answer": 1,
    "explain": "PRs are the review + CI + protection gate; direct push skips all three."
  },
  {
    "stem": "Your branch and <code>main</code> both touched the same line of the same file. On merge, what happens?",
    "options": [
      "Git silently picks <code>main</code>",
      "Git silently picks your branch",
      "Git stops with a merge conflict; <code>git status</code> lists the conflicting files",
      "The repo becomes corrupted"
    ],
    "answer": 2,
    "explain": "Concurrent edits to the same lines produce a conflict you resolve by hand."
  },
  {
    "stem": "Why is a GPU faster than a CPU for matrix multiplication?",
    "options": [
      "GPUs have higher clock speeds than CPUs",
      "GPUs have thousands of parallel cores; matrix multiplies are independent multiply-adds done in parallel",
      "GPUs use less memory than CPUs",
      "GPUs cache the model weights on-chip"
    ],
    "answer": 1,
    "explain": "Parallelism over thousands of small cores is the structural reason."
  },
  {
    "stem": "Roughly, what memory + bandwidth does an H100 SXM5 have?",
    "options": [
      "16 GB DDR5, 100 GB/s",
      "40 GB HBM2, 1 TB/s",
      "80 GB HBM3, ~3.35 TB/s",
      "192 GB HBM3e, ~8 TB/s"
    ],
    "answer": 2,
    "explain": "80 GB HBM3 and ~3.35 TB/s — numbers you'll re-use in Week 2."
  },
  {
    "stem": "Pick TWO structural differences between training and serving (inference).",
    "options": [
      "Training is rare/batch; serving is continuous/per-user",
      "Training is latency-sensitive; serving is throughput-only",
      "Training updates weights; serving just reads them",
      "Training is per-user real-time; serving is offline"
    ],
    "answer": 0,
    "explain": "Options A and C are both correct; option A is the single best summary. (B and D have the two sports swapped.)"
  },
  {
    "stem": "Put these inference-pipeline stages in order:",
    "options": [
      "tokenize → embed → layers → logits → sample",
      "embed → tokenize → sample → layers → logits",
      "layers → tokenize → embed → sample → logits",
      "sample → logits → layers → embed → tokenize"
    ],
    "answer": 0,
    "explain": "Text → tokens → vectors → transformer layers → logits → sampled token."
  },
  {
    "stem": "True or false: a CPU is always worse than a GPU for AI workloads.",
    "options": [
      "True — GPUs always win",
      "False — CPUs are better for sequential, branch-heavy, or small-batch work where parallelism doesn't amortize",
      "True — except for training",
      "False — only for training"
    ],
    "answer": 1,
    "explain": "GPUs win only when work is parallel and large enough to amortize memory transfer cost."
  },
  {
    "stem": "What core problem does Oxmiq's Capsule platform address?",
    "options": [
      "Making GPUs cheaper to manufacture",
      "Giving engineers on-demand access to remote GPU compute",
      "Training new foundation models from scratch",
      "Replacing CPUs in laptops"
    ],
    "answer": 1,
    "explain": "Capsule is about access to remote GPU compute on demand — not hardware manufacturing or model training."
  },
  {
    "stem": "In one forward pass, a language model produces:",
    "options": [
      "The entire response at once",
      "One output token",
      "A full sentence",
      "Nothing until decoding ends"
    ],
    "answer": 1,
    "explain": "One forward pass = one token out; generation loops the pass to build the response."
  },
  {
    "stem": "Across the 10 weeks, which sequence is correct?",
    "options": [
      "Capstone → Inference → Orientation",
      "Orientation → Inference Engineering → Agents → Capsule → Capstone",
      "Agents → Orientation → Capsule",
      "Inference → Capstone → Orientation"
    ],
    "answer": 1,
    "explain": "Orientation first to level-set, then inference engineering, agents, hands-on Capsule, and finally the capstone."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 5 · Consolidation](index.md)

-   __Back to the week__

    [Week 1 — Orientation &amp; Foundations overview](../index.md)

-   __Continue the curriculum__

    [Day 6 · What Happens When You Send a Prompt](../../week-02/module-1/index.md)

</div>
