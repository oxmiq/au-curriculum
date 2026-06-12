# Week 1 — Orientation & Foundations

> **Goal of the week:** everyone arrives at the same starting line. By Friday you can navigate a Linux shell, use git as a collaborator (not just a save button), explain why GPUs exist, and articulate what Capsule is in three sentences.

Each day is one core concept + practice. Half-day format (4 hours, mornings). Friday is consolidation.

---

## Day 1 — Welcome & Context

### Why this matters

You're about to spend 10 weeks learning how GPU inference works, how agents are built, and how Capsule is operated. That's a lot. Today is the only day that's *just* context — every day after this is technical content. Use today to internalize the "why."

### What Oxmiq does (in three sentences)

1. **Oxmiq Labs builds Capsule** — a platform that lets engineers and researchers use remote GPU machines (NVIDIA H100, Tenstorrent, AMD MI300, Apple Silicon, etc.) as if they were sitting on their own desk.
2. **The problem Capsule solves:** GPUs are expensive (an 8×H100 box rents for ~$24/hour, ~$17K/month), scarce, and operationally painful. Most teams can't justify owning them; the ones who do, can't keep them busy. Capsule turns a fleet of GPUs into a self-service utility.
3. **Where you fit in:** by the end of Week 10 you can take a model, pick the right GPU + serving config + quantization, benchmark it on Capsule, and write a recommendation that an engineering manager would act on. That's a hireable engineer.

### The 10-week journey (one line each)

| Week | What you'll learn |
|---|---|
| 1 | Tooling — shell, git, GPU primer |
| 2 | GPU hardware & memory bottlenecks |
| 3 | Attention, KV cache, quantization |
| 4 | Multi-GPU scaling, speculative decoding, serving engines |
| 5 | Metrics, production patterns, cost economics |
| 6 | Prompt engineering — the LLM-side companion to inference |
| 7 | AI agents — tools, governance, orchestration |
| 8 | Capsule foundations & operations (hands-on) |
| 9 | Capsule benchmarking & evaluation (apply Phase 1) |
| 10 | Capstone — prove it independently |

### How each day works

- **Before class** (15–30 min): assigned pre-reading + 3 reflection questions you answer in writing.
- **0:00–0:20** Readiness check: 5-question quiz on pre-reading. Below 3/5 = paired with a buddy.
- **0:20–1:20** Concept lecture: one idea, analogy-first, demo, pause-and-check every 15 min.
- **1:30–3:00** Practice: guided exercise → open-ended challenge. Pair work encouraged.
- **3:00–3:30** Wrap-up: *you* summarize, not the instructor. Pre-reading for tomorrow assigned.
- **3:30–4:00** Office hours (optional).

**Fridays are consolidation days.** No new content. Practice, ask, catch up.
**Afternoons are free.** Learning needs space.

### Practice (Day 1, ~90 min)

1. Watch the Capsule demo (link provided in chat).
2. Browse `oxmiq.com` and any product docs your facilitator points you at.
3. Write a **three-sentence answer** to: *"What does Capsule do, and why does it exist?"* — in your own words, no jargon.
4. Pair up and read your three sentences to your partner. Revise based on their feedback.
5. Submit your final three sentences to your facilitator at end of session.

### Connect forward

Tomorrow: the shell. Every operation in this curriculum — every git commit, every benchmark run, every Capsule command — starts with you in a terminal. We make sure you're fluent on Day 2 so it doesn't slow you down for the next 49 days.

---

## Day 2 — Shell & Linux

### Why this matters

The shell is the interface between you and every system you'll touch this program: your laptop, the Capsule machines you connect to, the CI pipelines you'll trigger, the benchmarks you'll run. If you're slow in the shell, you're slow at everything.

### Pre-reading

[MIT Missing Semester — Shell chapter](https://missing.csail.mit.edu/2020/course-shell/) (~20 min). Lecture 1 only.

### Core concepts

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

### Worked example

Goal: from `nvidia-smi` output, extract the GPU utilization percentage for GPU 0 only.

```bash
nvidia-smi --query-gpu=index,utilization.gpu --format=csv,noheader,nounits \
  | grep "^0," \
  | awk -F',' '{print $2}'
```

Each piece does one thing. Combined: a one-liner you'll use repeatedly in Week 9.

### Practice (90 min)

1. (15 min) Navigate: from `~`, get to `/tmp`, then to your home directory, then list all hidden files. Use `cd -` once.
2. (20 min) Parse `nvidia-smi` (or any sample output your facilitator provides): extract just GPU memory used per GPU.
3. (25 min) Write a 15-line bash script `disk_watch.sh` that prints disk usage of `/` every 10 seconds for one minute. Use `df`, a `for` loop, and `sleep`.
4. (20 min) Pair exercise: your partner reads your script aloud. If they can't predict every line's output, rewrite.
5. (10 min) Read [explainshell.com](https://explainshell.com) explanations of two cryptic one-liners your facilitator will share.

### Connect forward

Tomorrow: git. Version control is how multiple humans collaborate on the same shell-driven world without overwriting each other.

---

## Day 3 — Git Workflow

### Why this matters

Every line of code you touch in this program lives in a git repository. Every PR, every benchmark commit, every capstone deliverable. Git is the difference between "I lost two days of work" and "I rolled back in 30 seconds."

### Pre-reading

[Atlassian Git Tutorial — Basic Workflow](https://www.atlassian.com/git/tutorials/saving-changes) (~15 min).

### Core concepts

| Concept | Why it matters |
|---|---|
| **Clone** | Copy a repo locally — your starting point. |
| **Branch** | Isolate work-in-progress; never commit straight to `main`. |
| **Commit** | A unit of change with a message — the building block of history. |
| **Push** | Upload your branch to the remote (GitHub). |
| **PR** (Pull Request) | Propose merging your branch back to `main` — invites review. |
| **Conventional commits** | A discipline: `<type>: <description>` (e.g., `feat: add benchmark script`). |

### Conventional commit cheat-sheet

- `feat:` new functionality
- `fix:` bug fix
- `docs:` documentation only
- `refactor:` restructure without changing behavior
- `test:` add or fix tests
- `chore:` config, version bumps, CI

### Practice (90 min)

1. (15 min) Fork the practice repo your facilitator shares. Clone to your machine.
2. (20 min) Create a branch `feat/<your-name>-greeting`. Add a file `greetings/<your-name>.txt` with a one-line greeting. Commit with a conventional message. Push.
3. (15 min) Open a PR on GitHub. Write a body that explains the change.
4. (20 min) Review a peer's PR. Leave at least one substantive comment. Approve.
5. (10 min) Merge your PR after approval. Delete your branch.
6. (10 min) Simulate a conflict: your facilitator will give you a scenario. Practice `git status`, `git diff`, and a conflict-resolution edit.

### Common mistakes (avoid all of these from Day 3 onwards)

- Commit messages like `wip`, `temp`, `update`, `fix stuff`. **Use conventional commits.**
- Pushing directly to `main`. **Never. Always branch.**
- 50-line commit messages with no clear subject. **First line ≤72 chars.**
- Force-pushing to a shared branch. **`--force-with-lease` only, and only on your own branch.**

### Connect forward

Tomorrow: GPUs. We move from tooling to the hardware that will dominate the next four weeks.

---

## Day 4 — How Computers Run AI (GPU Primer)

### Why this matters

You don't need to know how a transistor works to be a good GPU engineer. You *do* need to know why a GPU exists, what makes it different from a CPU, and what kinds of work it's good at — because every design decision in Weeks 2–5 follows from those three facts.

### Pre-reading

A 15-min explainer video (3Blue1Brown style) on what a GPU is. Your facilitator will share the link.

### Three facts to internalize today

1. **A GPU has thousands of small cores; a CPU has a few big ones.** A modern CPU might have 8–96 powerful cores. An H100 GPU has 16,896 CUDA cores plus 528 Tensor Cores. CPUs are optimized for one big task fast; GPUs are optimized for many small tasks in parallel.
2. **Matrix multiplication is the workload neural networks demand, and it is embarrassingly parallel.** Multiplying a 4096×4096 matrix by a 4096×4096 matrix is ~68 billion multiply-adds — each one independent. A GPU can do them all at once (in batches). A CPU can't.
3. **Training and serving (inference) are different sports.** Training: rare, batch, throughput-only, can take weeks. Serving: continuous, per-user, latency-sensitive, must respond in milliseconds. Most of this program is about *serving*, which is the bigger and harder operational problem.

### Real numbers to remember

| Specification | NVIDIA H100 SXM5 |
|---|---|
| Tensor Cores | 528 |
| FP16 throughput | ~989 TFLOPs |
| HBM3 memory | 80 GB |
| Memory bandwidth | 3.35 TB/s |
| TDP | 700 W |
| Approx. cloud price | $2–4/hour per GPU |
| 8-GPU box price | ~$24/hour, ~$17K/month |

You'll see these numbers repeatedly in Week 2.

### The journey of a prompt (preview of Week 2 Day 6)

You type "Explain quantum tunneling in one sentence" and press Enter. Here's roughly what happens:

1. **Tokenize** — your text becomes a sequence of integers (token IDs).
2. **Embed** — each token ID becomes a vector (hundreds to thousands of floats).
3. **Layers** — the vectors pass through ~32–80 transformer layers. Each layer does attention + a feed-forward pass. This is where the GPU spends its time.
4. **Logits** — out comes a probability distribution over the entire vocabulary (~32K–200K tokens).
5. **Sample** — pick a token (greedy, top-p, etc.).
6. Loop steps 3–5 until you hit a stop condition. **Each loop = one output token.**

That's it. Everything in Weeks 2–5 is about making that loop faster and cheaper.

### Practice (90 min)

1. (15 min) On paper, draw the path of "Hello, world." from your keyboard to a response on screen. Label every box you can.
2. (25 min) Pair share: compare drawings. Where do you disagree? Which box does *neither* of you understand? Note it — that's a Week 2 question.
3. (20 min) Read the H100 spec table above. Look up the spec for one consumer GPU (e.g., RTX 4090) and one Tenstorrent chip (e.g., Wormhole n150). Write a 5-row comparison table.
4. (20 min) Group discussion: why is a 4090 cheaper per FLOP than an H100, and why would anyone still buy H100s? (Bandwidth, memory capacity, NVLink, datacenter-grade reliability.)
5. (10 min) Write down one question about GPUs you want answered before Friday. Save it.

### Connect forward

Friday: consolidation. We make sure shell, git, and the GPU mental model all stuck. Then we move to Week 2, where we open the GPU and look inside.

---

## Day 5 — Consolidation

### How the day runs

- **0:00–0:20** Week 1 review quiz (low-stakes, see `Week-1-Review-Quiz.md`).
- **0:20–1:30** Group teach-back: pairs explain one Day 2–4 concept to a different pair (Feynman technique).
- **1:30–3:00** Open lab: practice shell, fix git workflows, ask anything.
- **3:00–3:30** Readiness assessment for Week 2 + pre-reading assigned ("Inference vs training" blog).

### Self-check before Monday

You should be able to, without notes:

- [ ] Pipe `nvidia-smi` output through `grep` and `awk` to extract a single field.
- [ ] Create a branch, commit with a conventional message, push, open a PR, review a peer's PR.
- [ ] Explain in one paragraph why GPUs exist and what they're good at.
- [ ] Name three differences between training and serving.
- [ ] Quote two specs of the H100 from memory (memory size and bandwidth are the most-used).

If any item is shaky: today is the day to fix it. Monday's pace doesn't slow down.

### Connect forward

Week 2 begins on Monday. Pre-reading: "Inference vs training" blog (15 min). Reflection questions: (1) why is inference cumulatively more expensive than training? (2) name one thing a CPU does better than a GPU. (3) what's the smallest unit of work in inference?
