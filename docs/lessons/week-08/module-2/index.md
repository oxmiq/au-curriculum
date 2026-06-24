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
> **Pre-reading:** Lab Guide **Modules 6 + 7** (~30 min).

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
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-08/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Three Transfer Mechanisms | 20 min |
| Part 3 | Core Concepts: Storage Scopes | 20 min |
| Part 4 | Deep Dive: Shared Storage Workflow | 25 min |
| Part 5 | Hands-On: Upload / Download Drill | 30 min |
| Part 6 | Hands-On: Streaming & Daily Rhythm | 20 min |
| Part 7 | Wrap-up & Connection | 10 min |

**Total: ~140 min**

---

## Part 1 — Pre-Reading Review · 15 min

### Reading — Why this matters

This is the most-used set of operations in daily life on Capsule. Pick the wrong tool — copy a 50 GB checkpoint with `cp` instead of using shared storage, or scrape logs after the fact instead of streaming — and you waste hours. Pick right and you have an enjoyable benchmarking rhythm.

### Exercise: Self-Check

Answer before reading on:

1. Which tool for a 50 MB Python script: `capsule cp` or shared storage?
2. Which tool for a 50 GB model checkpoint?
3. What's the difference between per-user home dir and the shared storage pool?
4. Why stream benchmark output instead of `tail -f`-ing a log after disconnect?
5. What command runs a one-off remote command and streams its stdout to your laptop?

---

## Part 2 — Core Concepts: Three Transfer Mechanisms · 20 min

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

## Part 3 — Core Concepts: Storage Scopes · 20 min

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

## Part 4 — Deep Dive: Shared Storage Workflow · 25 min

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

## Part 5 — Hands-On: Upload / Download Drill · 30 min

### Exercise: File Round-Trip

1. (5 min) Create a small test file on your laptop: `echo "hello capsule" > test.txt`
2. (5 min) Copy it to your dev node: `capsule cp ./test.txt <node>:./`
3. (5 min) On the node: verify it exists (`capsule connect <node> --command 'cat ~/test.txt'`).
4. (5 min) Modify the file on the node (`capsule connect` → `echo "modified" >> test.txt`).
5. (5 min) Pull it back: `capsule cp <node>:./test.txt ./test-returned.txt`.
6. (5 min) Run `capsule storage ls /shared/`. Note what's pre-staged. Read a `README` if present.

---

## Part 6 — Hands-On: Streaming & Daily Rhythm · 20 min

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

## Part 7 — Wrap-up & Connection · 10 min

### Self-check

- [ ] I can `capsule cp` a file to/from a node in < 2 commands
- [ ] I know when to use `capsule storage put` vs `capsule cp`
- [ ] I can stream a command's output with `capsule run --stream`
- [ ] I have a personal artifact layout plan for Week 9 benchmarks
- [ ] I know the etiquette for shared storage (cleanup, no-junk-in-models)

### Connect forward

Tomorrow (Day 39): **streaming** — the full `capsule stream` workflow for GPU-accelerated desktop output. Day 40 (Friday): reliability & diagnostics.

---

## Pre-read for Friday (Day 40 · Reliability & Diagnostics)

- **Resource:** Lab Guide **Module 10 known-quirks table** + Glossary (~10 min).
- **Reflection questions:**
  1. What's the diagnostic sequence when a node "doesn't connect"?
  2. What's the diagnostic sequence when a GPU "isn't seen" by your container?
  3. What information must a good bug report contain?

---

## Stuck?

Ask **oxtutor** — share which command you ran, what error you got, and which storage scope (home vs shared) you were targeting.
