---
drift: |
  Authored as a combined "Files + Storage + Streaming" day (former wk8 day 39). New graph
  splits this into two consecutive modules: week-08/module-2 (Files & Storage) and
  week-08/module-3 (Streaming). For now this lesson covers BOTH concepts in a single page;
  module-3 is a redirect stub pointing to the streaming section below. Future authoring
  should extract the streaming material into its own page.
---

# Day 38 · Files & Storage (with streaming primer)

> **Concept of the day:** **`capsule cp`** for small files. **Shared storage pool** for big artifacts (models, datasets, results). **Streaming output** (`capsule run --stream`) for live logs without scraping after-the-fact. Per-user home is fast but ephemeral relative to the cluster lifecycle.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-39-files-storage-streaming">Capsule Power-User Pre-Lecture Reading — Day 39 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-6-files-storage-and-the-onedrive-mount">Capsule Lab Guide</a> Modules 6 + 7.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 — Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 38 · Files & Storage</span>
    {status:week-08/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Three Transfer Mechanisms |
| Part 3 | Core Concepts: Storage Scopes |
| Part 4 | Deep Dive: Shared Storage Workflow |
| Part 5 | Hands-On: Upload / Download Drill |
| Part 6 | Hands-On: Streaming & Daily Rhythm |
| Part 7 | Wrap-up & Connection |

**Total: ~140 min**

---

## Part 1 — Pre-Reading Review

### Reading — Why this matters

This is the most-used set of operations in daily life on Capsule. Pick the wrong tool — copy a 50 GB checkpoint with `cp` instead of using shared storage, or scrape logs after the fact instead of streaming — and you waste hours. Pick right and you have an enjoyable benchmarking rhythm.

### Exercise: Self-Check

Answer before reading on:

1. Which tool for a 50 MB Python script: `capsule cp` or shared storage?
2. Which tool for a 50 GB model checkpoint?
3. What's the difference between per-user home dir and the shared storage pool?
4. Why stream benchmark output instead of `tail -f`-ing a log after disconnect?
5. What command runs a one-off remote command and streams its stdout to your laptop?

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m2-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Modules 6-7">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Which tool should you use to copy a 50 MB Python script to a node?",
    "options": [
      "Shared storage pool",
      "capsule cp",
      "rsync",
      "FTP"
    ],
    "answer": 1,
    "explain": "For small files like scripts and configs, use 'capsule cp'. It's quick and efficient for files in the MB range. Shared storage is overkill for small files."
  },
  {
    "stem": "Which tool should you use to copy a 50 GB model checkpoint to a node?",
    "options": [
      "capsule cp",
      "Shared storage pool",
      "Email",
      "USB drive"
    ],
    "answer": 1,
    "explain": "For large files like model checkpoints (50 GB), use the shared storage pool. 'capsule cp' would be too slow and might timeout. The shared storage pool is designed for large artifacts."
  },
  {
    "stem": "What is the difference between per-user home dir and the shared storage pool?",
    "options": [
      "They are the same",
      "Per-user home is fast but ephemeral relative to cluster lifecycle; shared storage persists across the cluster lifetime",
      "Shared storage is faster",
      "Home dir is persistent"
    ],
    "answer": 1,
    "explain": "Per-user home (~) is fast but ephemeral — it may be cleaned up when nodes are recycled. Shared storage pool persists across the cluster lifecycle. For important artifacts (models, datasets, results), always use shared storage."
  },
  {
    "stem": "Why should you stream benchmark output instead of using tail -f after disconnect?",
    "options": [
      "Streaming is required",
      "Streaming gives you live output in real-time; tail -f after disconnect might miss data if the process finished or logs rotated",
      "tail -f is not supported",
      "They are equivalent"
    ],
    "answer": 1,
    "explain": "Streaming gives you live output in real-time. If you disconnect and then try 'tail -f', you might miss data — the process might have finished, logs might have rotated, or you might get partial data. Streaming is more reliable."
  },
  {
    "stem": "What command runs a one-off remote command and streams its stdout to your laptop?",
    "options": [
      "capsule connect --command",
      "capsule run --stream",
      "ssh with streaming",
      "remote execute"
    ],
    "answer": 1,
    "explain": "'capsule run --stream' runs a one-off remote command and streams its stdout to your laptop in real-time. This is perfect for watching benchmark output live without needing to connect and tail logs manually."
  },
  {
    "stem": "What is the shared storage pool used for in Capsule?",
    "options": [
      "Temporary files",
      "Big artifacts like models, datasets, and results that need to persist",
      "Only for logs",
      "Only for small files"
    ],
    "answer": 1,
    "explain": "The shared storage pool is for big artifacts like models, datasets, and results that need to persist across the cluster lifecycle. It's designed for large files that would be too slow to copy with 'capsule cp'."
  },
  {
    "stem": "What does 'capsule storage put' do?",
    "options": [
      "Deletes storage",
      "Uploads a file to the shared storage pool",
      "Lists storage",
      "Creates a new storage pool"
    ],
    "answer": 1,
    "explain": "'capsule storage put' uploads a file to the shared storage pool. This is the command to use for large files like model checkpoints that you want to persist and share across nodes."
  },
  {
    "stem": "What is the daily rhythm for storage in Capsule?",
    "options": [
      "Always use capsule cp",
      "Use capsule cp for small files, shared storage for large files, streaming for live output",
      "Only use shared storage",
      "Only use streaming"
    ],
    "answer": 1,
    "explain": "The daily rhythm is: (1) capsule cp for small files (scripts, configs), (2) shared storage pool for large artifacts (models, datasets), (3) streaming for live output (benchmarks, training). Pick the right tool and your workflow is efficient."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: Three Transfer Mechanisms

### Reading — File transfer commands

| Command | When |
|---|---|
| `capsule cp ./local.py <node>:./remote.py` | Small files, scripts, configs |
| `capsule cp <node>:./results.json ./` | Pull a single artifact |
| `capsule cp -r ./mydir <node>:./` | Recursive (modest size) |
| `capsule storage put ./big.bin /shared/models/` | Large files → shared pool |
| `capsule storage get /shared/results/run-42 ./` | Pull from shared pool |
| `capsule storage ls /shared/models` | List shared pool |

### Exercise: Choose the Right Tool

For each scenario, write the correct command:

1. Copy your `benchmark.yaml` (2 KB) from your laptop to node `nv-h100-04-1`.
2. Copy a 70B model checkpoint (140 GB) from your laptop to shared storage at `/shared/models/llama-70b/`.
3. Pull the `report.json` that a benchmark wrote to `/shared/runs/2025-09-15/` onto your laptop.
4. List everything in `/shared/models/`.

---

## Part 3 — Core Concepts: Storage Scopes

### Reading — Per-user home vs shared storage

| Property | `$HOME` on node | Shared storage `/shared/...` |
|---|---|---|
| Speed | Local NVMe, fastest | Networked, slower |
| Lifetime | Lease-bound or longer (env-dependent) | Cluster-bound, durable |
| Quota | Small (10–50 GB) | Large (TB+) |
| Visibility | This node only | All nodes in env |
| Use for | Source code, venvs, scratch | Models, datasets, results, anything you want to keep |

> **Rule:** if losing this on a node reboot would hurt, put it in shared.

### Reading — Why shared storage matters

A 70B FP16 model = 140 GB. Copying that with `capsule cp` over your laptop's network? **Take a break, see you in 3 hours.** Pre-staging into shared once, then mounting on any node? **Seconds.**

The Week 9 benchmark workflow:

1. Models live in `/shared/models/` (pre-staged once, by the platform team or you).
2. Each benchmark run lives in `/shared/runs/<date>-<config>/`.
3. Your laptop never moves model bytes — only the run reports.

### Exercise: Lifetime Reasoning

For each artifact, decide: `$HOME` or `/shared`? Justify in one sentence.

1. A Python venv you'll reuse tomorrow on the *same* node.
2. A 70B model checkpoint you'll use across multiple nodes this week.
3. A `run.sh` script you're actively editing.
4. The `report.json` output of today's benchmark (you want it next week).
5. A `/tmp/scratch.bin` you need only for the next 5 minutes.

---

## Part 4 — Deep Dive: Shared Storage Workflow

### Reading — Streaming: see logs live

```
capsule run <node> --stream -- ./run_benchmark.sh
```

vs the wrong way:

```
capsule connect <node>
nohup ./run_benchmark.sh > /tmp/out.log 2>&1 &
exit
# 4 hours later...
capsule connect <node>
tail -f /tmp/out.log   # too late to react
```

With `--stream`, you see output in real time and can Ctrl-C to abort if you spot an obvious failure 30 seconds in. Don't waste GPU-hours on a typo'd config.

### Reading — The full daily file workflow

```
# Once, pre-stage:
capsule storage put llama-3-70b-fp8.tar /shared/models/

# Each benchmark session:
capsule node lease --gpu h100 --min-gpus 8 --duration 4h
capsule cp ./benchmark.yaml <node>:./
capsule run <node> --stream -- ./run.sh ./benchmark.yaml /shared/runs/$(date +%F)/
capsule storage get /shared/runs/$(date +%F)/report.json ./
capsule lease release
```

That's the rhythm. Memorize it.

### Reading — Etiquette

- Clean up your `/shared/runs/<old>` directories monthly.
- Don't put junk in `/shared/models/`.
- Don't `chmod 777 -R` shared storage out of frustration — ask for the right group.
- Log your large operations (uploads / deletes) — it's polite.

### Exercise: Workflow Gap-Fill

The following daily workflow has 3 mistakes. Find them:

```
capsule node lease --gpu h100 --duration 4h
capsule cp llama-70b.bin <node>:./                 # (1)
capsule run <node> -- ./run.sh                     # (2) — no streaming
capsule cp <node>:/tmp/report.json ./              # (3)
# lease not released
```

For each mistake: what's wrong, and what's the correct approach?

---

## Part 5 — Hands-On: Upload / Download Drill

### Exercise: File Round-Trip

1. Create a small test file on your laptop: `echo "hello capsule" > test.txt`
2. Copy it to your dev node: `capsule cp ./test.txt <node>:./`
3. On the node: verify it exists (`capsule connect <node> --command 'cat ~/test.txt'`).
4. Modify the file on the node (`capsule connect` → `echo "modified" >> test.txt`).
5. Pull it back: `capsule cp <node>:./test.txt ./test-returned.txt`.
6. Run `capsule storage ls /shared/`. Note what's pre-staged. Read a `README` if present.

---

## Part 6 — Hands-On: Streaming & Daily Rhythm

### Exercise: Streaming a Long Command

1. Run a long command with `--stream` (use a harmless 30-second sleep + echo loop):
   ```
   capsule run <node> --stream -- bash -c 'for i in $(seq 1 6); do echo "step $i"; sleep 5; done'
   ```

2. Observe: you see output as it happens.
3. After step 3 appears, press Ctrl-C. Verify the job aborts.
4. Now design your Week 9 benchmark artifact layout. Fill in:
   ```
   Model stored at:         /shared/models/___________
   Each run goes to:        /shared/runs/___________
   Config file stays in:    ~/___________
   Report pulled to laptop: ~/___________
   ```

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 39 · Files &amp; Storage">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the difference between `capsule cp` and `capsule storage put`?",
    "options": [
      "They are identical — both copy files",
      "`capsule cp` copies files directly between your local machine and a specific node (ephemeral, per-node); `capsule storage put` uploads to the shared persistent storage pool accessible across all nodes",
      "`capsule cp` is for large files; `capsule storage put` is for small files",
      "`capsule storage put` requires authentication; `capsule cp` does not"
    ],
    "answer": 1,
    "explain": "`capsule cp` is like `scp` — direct file transfer to/from a specific node's local filesystem. That file is only on that node. `capsule storage put` pushes to the shared storage pool, accessible from any node in the environment — ideal for model weights and benchmark results you need across multiple nodes or runs."
  },
  {
    "stem": "What is the recommended artifact layout for benchmark runs?",
    "options": [
      "Store everything in `/tmp` for fast access",
      "Store models in `/shared/models/`, run outputs in `/shared/runs/<date-label>/`, config in home dir, and pull results to laptop",
      "Store all artifacts in the home directory for simplicity",
      "Use Git to version all run artifacts"
    ],
    "answer": 1,
    "explain": "The lesson's artifact layout: models in `/shared/models/` (large, shared across nodes), each run in `/shared/runs/<YYYY-MM-DD-HHMM>-<label>/` (timestamped for reproducibility), config in `~/` (per-user), and report pulled to laptop for analysis. This pattern makes runs reproducible and artifacts shareable with teammates."
  },
  {
    "stem": "What does `capsule run --stream` do?",
    "options": [
      "It starts a streaming video session on the node",
      "It executes a command on the node and streams its stdout/stderr back to your local terminal in real time",
      "It runs the Capsule streamer application",
      "It enables GPU output streaming for benchmark results"
    ],
    "answer": 1,
    "explain": "`capsule run <node> --stream -- <command>` runs a command on the remote node and streams its output to your local terminal in real time. This is the default pattern for benchmark runs — you see progress without maintaining an interactive session, and the output can be piped or logged locally."
  },
  {
    "stem": "What is the etiquette rule for the shared `/shared/models/` directory?",
    "options": [
      "Store all your working files there for easy access from any node",
      "Keep only official model checkpoints; clean up temporary files and don't leave junk — shared storage is a finite resource for the whole team",
      "Never read from shared storage; always copy to local node storage first",
      "Prefix all files with your username to avoid conflicts"
    ],
    "answer": 1,
    "explain": "The lesson states shared storage etiquette: clean up, no junk in `/shared/models/`. Shared storage is a finite, shared resource. Leaving large temporary files wastes space for teammates. Store only stable artifacts: model checkpoints you might reuse, benchmark outputs worth keeping, configs others might reference."
  },
  {
    "stem": "When should you use `capsule storage put` instead of `capsule cp` for model weights?",
    "options": [
      "Always — `capsule storage put` is faster for all file sizes",
      "When the model will be used from multiple nodes or must survive node replacement — shared storage persists across node lifetimes, but a node's local filesystem is ephemeral",
      "When the model is larger than 1 GB",
      "When you need the model on your laptop, not on a node"
    ],
    "answer": 1,
    "explain": "Node local storage is ephemeral — it disappears when the node is released or replaced. If you copy a model with `capsule cp` to a node's local disk and that node becomes unavailable, you'd need to re-copy. Shared storage (`capsule storage put`) persists independently of any specific node — ideal for 70B model checkpoints you'll use multiple times."
  }
]
</script>
</div>

### Connect forward

Tomorrow (Day 39): **streaming** — the full `capsule stream` workflow for GPU-accelerated desktop output. Day 40 (Friday): reliability & diagnostics.

---

### Looking ahead to next week

**Thursday (Day 40)** is module-4 and is **not** a pre-read day — Friday (Day 41) is consolidation.

**Monday (Day 42):** Next week's first lesson has a pre-read — see [Week 9 Day 1](../../../readings/capsule/).

---

## Stuck?

Ask **oxtutor** — share which command you ran, what error you got, and which storage scope (home vs shared) you were targeting.
