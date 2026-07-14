<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 1 - Orientation &amp; Foundations</a>
    <span class="sep">/</span>
    <a href="../">Day 5 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-01/module-5}
  </div>
</div>

# Week 1 Knowledge Check

**Week 1 · Orientation.** 32-question bank · **18 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative, it never blocks you, but it's the week's bar. Answer the drawn questions,
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
    "explain": "<code>wip</code> is not a useful commit message; use conventional-commit format with a real description."
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
    "explain": "80 GB HBM3 and ~3.35 TB/s: numbers you'll re-use in Week 2."
  },
  {
    "stem": "Which statement correctly describes a structural difference between training and serving (inference)?",
    "options": [
      "Training is rare/batch and throughput-oriented; serving is continuous, per-user, and latency-sensitive",
      "Training is latency-sensitive; serving is throughput-only",
      "Serving updates the model weights; training only reads them",
      "Training is per-user real-time; serving is an offline batch job"
    ],
    "answer": 0,
    "explain": "Day 4 frames them as different sports: training is rare, uses large batches, and optimizes throughput; serving is continuous, often single-request, and optimizes latency. The other options swap those properties."
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
      "True - GPUs always win",
      "False - CPUs are better for sequential, branch-heavy, or small-batch work where parallelism doesn't amortize",
      "True - except for training",
      "False - only for training"
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
    "explain": "Capsule is about access to remote GPU compute on demand: not hardware manufacturing or model training."
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
  },
  {
    "stem": "Roughly what does an 8×H100 box cost to rent?",
    "options": [
      "~$2/hour, ~$500/month",
      "~$24/hour, ~$17K/month",
      "~$100/hour, ~$70K/month",
      "~$250/hour, ~$180K/month"
    ],
    "answer": 1,
    "explain": "Day 1 gives ~$24/hour, ~$17K/month for an 8×H100 box: the number that explains why most teams can't justify owning GPUs and why Capsule's self-service model exists."
  },
  {
    "stem": "In which week do you begin hands-on work with Capsule itself?",
    "options": [
      "Week 1",
      "Week 4",
      "Week 8",
      "Week 10"
    ],
    "answer": 2,
    "explain": "The 10-week roadmap lists Week 8 as 'Capsule foundations & operations (hands-on).' Weeks 1-7 build the prerequisites; the capstone is Week 10."
  },
  {
    "stem": "What distinguishes model training from inference?",
    "options": [
      "Training reads the weights; inference updates them via backpropagation",
      "Training updates model weights by learning; inference runs a forward pass to generate outputs",
      "Training always runs on CPUs; inference always runs on GPUs",
      "They are the same operation run at different times"
    ],
    "answer": 1,
    "explain": "Day 1's key terms: training modifies weights by learning from data; inference only reads those weights to produce outputs for new inputs."
  },
  {
    "stem": "What does the <code>$PATH</code> environment variable control?",
    "options": [
      "The current working directory",
      "The user's home directory",
      "The default text editor",
      "The list of directories the shell searches to resolve a bare command name"
    ],
    "answer": 3,
    "explain": "When you type a bare command name, the shell searches each directory in <code>$PATH</code> in order. <code>$HOME</code> tracks the home directory; <code>$EDITOR</code> tracks the editor."
  },
  {
    "stem": "In a shell pipeline, what does a pipe <code>|</code> connect?",
    "options": [
      "The stdout of the left command to the stdin of the right command",
      "Two files so they are read in sequence",
      "A command to a remote host over SSH",
      "The stderr of one command to a file"
    ],
    "answer": 0,
    "explain": "A pipe routes stdout of the left-hand command into stdin of the right-hand command. It does not merge stderr (that needs <code>2&gt;&amp;1</code>)."
  },
  {
    "stem": "Why does <code>source setup.sh</code> behave differently from <code>./setup.sh</code>?",
    "options": [
      "<code>source</code> runs the script in the current shell, so its variable and directory changes persist; <code>./</code> spawns a child whose environment is discarded on exit",
      "<code>./</code> runs the script as root; <code>source</code> runs it as the current user",
      "<code>source</code> requires the execute bit; <code>./</code> does not",
      "They are identical in every respect"
    ],
    "answer": 0,
    "explain": "<code>source</code> (or <code>.</code>) evaluates the script in the calling shell's environment, so assignments and <code>cd</code> take effect immediately. A subprocess from <code>./</code> discards its environment on exit: which is why setup scripts must be sourced."
  },
  {
    "stem": "Which is generally preferred, and why: <code>cat file.txt | grep pattern</code> or <code>grep pattern file.txt</code>?",
    "options": [
      "<code>cat file.txt | grep pattern</code> - the pipe form is more readable",
      "<code>grep pattern file.txt</code> - it avoids a needless <code>cat</code> process",
      "They are identical in every respect",
      "<code>cat file.txt | grep pattern</code> - <code>grep</code> cannot accept a filename"
    ],
    "answer": 1,
    "explain": "Using <code>cat</code> only to feed one file into another command is the 'useless use of cat.' <code>grep</code> takes a filename directly, avoiding an extra process fork."
  },
  {
    "stem": "Which command finds all Markdown files modified within the last day?",
    "options": [
      "<code>ls -la *.md</code>",
      "<code>find . -type md -days 1</code>",
      "<code>find . -name \"*.md\" -mtime -1</code>",
      "<code>grep -r \".md\" . --age=1</code>"
    ],
    "answer": 2,
    "explain": "<code>find</code>'s <code>-name</code> matches by filename pattern; <code>-mtime -1</code> selects files modified less than a day ago. This is the exact example in Day 2's Core Concepts table."
  },
  {
    "stem": "What is the difference between <code>git fetch</code> and <code>git pull</code>?",
    "options": [
      "They are identical",
      "<code>fetch</code> downloads remote commits without merging; <code>pull</code> downloads and merges them into your current branch",
      "<code>fetch</code> uploads commits; <code>pull</code> downloads them",
      "<code>pull</code> only works on the <code>main</code> branch"
    ],
    "answer": 1,
    "explain": "<code>git fetch</code> retrieves remote commits but leaves your working branch untouched. <code>git pull</code> is fetch plus an automatic merge into the current branch."
  },
  {
    "stem": "You must overwrite history on your own feature branch. Which push is the safer choice?",
    "options": [
      "<code>git push -f</code>",
      "<code>git push --all</code>",
      "<code>git push -u origin</code>",
      "<code>git push --force-with-lease</code>"
    ],
    "answer": 3,
    "explain": "Day 3 flags plain force-push as a mistake on shared branches. <code>--force-with-lease</code> aborts if someone else has pushed since your last fetch, so it won't silently clobber their work."
  },
  {
    "stem": "What is the difference between <code>git commit</code> and <code>git push</code>?",
    "options": [
      "<code>commit</code> uploads to the remote; <code>push</code> saves locally",
      "<code>commit</code> records changes in your local repo; <code>push</code> uploads those commits to the remote",
      "They are the same command",
      "<code>commit</code> creates a branch; <code>push</code> deletes it"
    ],
    "answer": 1,
    "explain": "<code>git commit</code> records a snapshot in your local history. <code>git push</code> uploads those local commits to the remote (GitHub) so others can see them."
  },
  {
    "stem": "Roughly how many CUDA cores does an NVIDIA H100 have?",
    "options": [
      "528",
      "3,000",
      "16,896",
      "80"
    ],
    "answer": 2,
    "explain": "Day 4 lists the H100 with 16,896 CUDA cores plus 528 Tensor Cores. The 528 is the Tensor-Core count; 80 is the GB of HBM3."
  },
  {
    "stem": "What does HBM stand for in GPU specifications?",
    "options": [
      "High Bandwidth Memory",
      "Hyper Basic Memory",
      "Host Buffer Memory",
      "High Binary Mode"
    ],
    "answer": 0,
    "explain": "HBM (High Bandwidth Memory) is stacked memory built for high throughput. The H100's 80 GB of HBM3 at 3.35 TB/s is central to Day 4's 'memory bottlenecks matter' point."
  },
  {
    "stem": "In the inference pipeline, what are the 'logits'?",
    "options": [
      "The single token that gets sampled and returned",
      "The tokenizer's vocabulary file on disk",
      "A probability distribution over the vocabulary (~32K-200K tokens)",
      "The GPU's on-chip memory buffer"
    ],
    "answer": 2,
    "explain": "Day 4's journey of a prompt: the layers produce logits, a probability distribution over the whole vocabulary, and the sample step then picks one token from that distribution."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Back to today's lesson__

    [Day 5 · Consolidation](index.md)

-   __Back to the week__

    [Week 1 - Orientation &amp; Foundations overview](../index.md)

-   __Continue the curriculum__

    [Day 6 · What Happens When You Send a Prompt](../../week-02/module-1/index.md)

</div>
