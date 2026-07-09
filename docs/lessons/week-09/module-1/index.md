---
drift: |
  Originally Day 41 of the former Capsule wk9. Now Day 42 of the new Benchmarking & Eval
  week (week-09/module-1), unchanged in scope. Source-material link paths bumped one
  level deeper.
---

# Day 42 · Your First Benchmark

> **Concept of the day:** `capsule benchmark` orchestrates a serving engine + a request load + metric collection. Phase-1 vocabulary (TTFT, ITL, p99, throughput) lands here in real numbers. Today: run *one* benchmark cleanly, end to end, on a leased GPU node.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-41-your-first-benchmark">Capsule Power-User Pre-Lecture Reading — Day 41 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-8-model-evaluation-benchmarking-the-inferencemax-path">Capsule Lab Guide</a> Module 8.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 — Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 42 · Benchmarking</span>
    {status:week-09/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Benchmark Anatomy |
| Part 3 | Core Concepts: Reading the Report |
| Part 4 | Deep Dive: What One Benchmark Proves (and Doesn't) |
| Part 5 | Hands-On: Run Your First Benchmark |
| Part 6 | Hands-On: Annotate & Defend the Report |
| Part 7 | Wrap-up & Connection |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review

### Reading — Why this matters

You've spent six weeks learning what TTFT, throughput, and p99 *mean*. Today you generate them yourself, on a real GPU, and read them off a real report. This is the moment Phase 1 becomes muscle memory rather than vocabulary.

### Exercise: Self-Check

Answer before reading on:

1. Name the three things a benchmark run consists of.
2. What's the minimal command to run a benchmark on a leased node?
3. What four metrics will the report contain? (Phase 1 recall.)
4. What does *one* benchmark prove? (Hint: very little — that's tomorrow's lesson.)
5. Where should the result file live?

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m1-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 8">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the three pieces of a Capsule benchmark run?",
    "options": [
      "Model, GPU, and network",
      "Load generator, serving engine, and metric collection",
      "Config, logs, and report",
      "Lease, environment, and node"
    ],
    "answer": 1,
    "explain": "A benchmark has three pieces: (1) load generator — controls what prompts, what concurrency, how long; (2) serving engine — which engine (vLLM/SGLang), which model, which config; (3) metric collection — gathers TTFT, ITL, throughput, GPU util and writes report.json."
  },
  {
    "stem": "What does the `--concurrency` flag control in `capsule benchmark`?",
    "options": [
      "The number of GPUs to use",
      "The number of simultaneous in-flight requests during the load test",
      "The number of benchmark iterations to run",
      "The tensor-parallel degree"
    ],
    "answer": 1,
    "explain": "--concurrency sets the number of simultaneous in-flight requests. Higher concurrency stresses the GPU more and pushes throughput up — until saturation. This is distinct from tensor-parallel degree (--tp), which is about model distribution."
  },
  {
    "stem": "Where do benchmark results live by convention?",
    "options": [
      "~/.capsule/results/",
      "/shared/runs/<YYYY-MM-DD-HHMM>-<label>/",
      "/tmp/benchmark/",
      "The current working directory"
    ],
    "answer": 1,
    "explain": "Convention is /shared/runs/<YYYY-MM-DD-HHMM>-<label>/. Inside: report.json, stdout.log, config.yaml. Results in /shared/ are accessible from your laptop via 'capsule storage get' and visible to the team."
  },
  {
    "stem": "What does `report.json` NOT tell you directly?",
    "options": [
      "TTFT p50 and p99",
      "GPU memory used",
      "Whether the model answers correctly or hallucinates",
      "Throughput in tokens per second"
    ],
    "answer": 2,
    "explain": "report.json captures performance metrics (TTFT, ITL, throughput, GPU util) but says nothing about answer quality. Whether the model is correct, refuses appropriately, or hallucinates requires interactive evaluation — which is Day 44."
  },
  {
    "stem": "What does a SINGLE benchmark run prove?",
    "options": [
      "This engine is better than all alternatives",
      "The GPU is fully saturated",
      "This config, this load, this moment — nothing more",
      "The model's quality is acceptable"
    ],
    "answer": 2,
    "explain": "One benchmark is a single data point: this config, this load, this moment. It cannot tell you whether the engine beats alternatives (need comparison), whether the GPU is saturated (need to vary --concurrency), or whether quality is acceptable (need eval). That's why tomorrow's lesson is about sweeps."
  },
  {
    "stem": "In the minimum-viable `capsule benchmark` command, what does `--duration 60s` control?",
    "options": [
      "How long the GPU is leased",
      "How long the load generator runs before stopping and writing the report",
      "How long before the connection times out",
      "The maximum time allowed for a single request"
    ],
    "answer": 1,
    "explain": "--duration 60s tells the load generator to run for 60 seconds before stopping and collecting the final metrics into report.json. Shorter durations give less stable statistics; the lesson recommends at least 60s for a clean baseline."
  },
  {
    "stem": "Which metrics appear in a typical report.json? (Select the complete set.)",
    "options": [
      "TTFT only",
      "TTFT (p50/p99), ITL (p50/p99), throughput (tokens/s, requests/s), GPU util and memory",
      "Throughput and GPU util only",
      "TTFT, throughput, cost per token, error rate"
    ],
    "answer": 1,
    "explain": "A typical report.json contains: ttft_p50, ttft_p99, itl_p50, itl_p99 (latency), tokens_per_sec, requests_per_sec (throughput), and gpu.util_avg, gpu.mem_used_gb. These are exactly the Phase-1 metrics you've been studying."
  },
  {
    "stem": "You want to run a benchmark that stores results in /shared/runs/. What command do you use to pull the report.json to your laptop after the run?",
    "options": [
      "capsule term — then cp /shared/runs/.../report.json ~",
      "capsule storage get /shared/runs/<your-dir>/report.json ./",
      "scp capsule-node:/shared/runs/.../report.json ./",
      "capsule benchmark --fetch-results"
    ],
    "answer": 1,
    "explain": "'capsule storage get <remote-path> <local-path>' is the correct command. It copies the file from the shared storage volume to your laptop. Using scp or raw cp won't work because you don't have direct SSH access to the shared volume path."
  }
]
</script>
</div>

---

## Part 2 — Core Concepts: Benchmark Anatomy

### Reading — The three-piece architecture

```
┌────────────┐        ┌───────────────┐        ┌──────────────┐
│ load gen   │ ─────▶ │ serving       │ ─────▶ │ metric       │
│ (requests/s│        │ engine        │        │ collection   │
│ prompts)   │ ◀───── │ (vLLM/SGLang) │ ◀───── │              │
└────────────┘        └───────────────┘        └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │ report.json  │
                      └──────────────┘
```

Three pieces:

1. **Load generator** — what prompts, what concurrency, how long.
2. **Serving engine** — which engine, which model, which config (TP, quant, batching).
3. **Metric collection** — TTFT, ITL, throughput, p50/p95/p99, GPU util.

### Reading — The minimum-viable command

```
capsule benchmark \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --engine vllm \
  --concurrency 8 \
  --duration 60s \
  --out /shared/runs/$(date +%F-%H%M)-first/
```

That's it. Defaults give sensible TP, quant, and prompt distribution. The report writes to `/shared/runs/.../report.json`.

### Exercise: Command Anatomy

Without looking at the documentation:

1. What does `--concurrency 8` control? (number of simultaneous in-flight requests)
2. What does `--duration 60s` control? (how long the load runs before stopping)
3. What does `--out /shared/runs/$(date +%F-%H%M)-first/` do? (where results land)
4. If you omit `--engine`, what happens? (default engine is chosen by Capsule)
5. Write the command to benchmark `Qwen2.5-7B-Instruct` with concurrency 4, duration 120s, outputting to `/shared/runs/qwen-test/`.

---

## Part 3 — Core Concepts: Reading the Report

### Reading — Phase-1 vocabulary check

A typical `report.json` excerpt:

```json
{
  "config": {"model": "...", "engine": "vllm", "concurrency": 8, "tp": 1, "quant": "fp16"},
  "latency_ms": {"ttft_p50": 142, "ttft_p99": 380, "itl_p50": 18, "itl_p99": 41},
  "throughput": {"tokens_per_sec": 1240, "requests_per_sec": 7.2},
  "gpu": {"util_avg": 0.83, "mem_used_gb": 18.4}
}
```

You should be able to read every field without checking a glossary. If `ttft_p99` is 380 ms — is that compute-bound or memory-bound territory? (Week 2, Day 9.)

### Exercise: Field-by-Field Explanation

For each field in the JSON above, write:
- What it measures (one sentence)
- Whether this value is good, bad, or "it depends" for an 8B model on an H100

| Field | What it measures | Good / bad / depends? |
|---|---|---|
| `ttft_p50: 142` | | |
| `ttft_p99: 380` | | |
| `itl_p50: 18` | | |
| `throughput.tokens_per_sec: 1240` | | |
| `gpu.util_avg: 0.83` | | |
| `gpu.mem_used_gb: 18.4` | | |

---

## Part 4 — Deep Dive: What One Benchmark Proves

### Reading — The limits of a single data point

A single number is just a data point. It tells you *this config, this load, this moment*. It can't tell you:

- Is this engine better than another? (need comparison)
- Does it scale? (need to vary load)
- Is the GPU saturated? (need to vary `--concurrency`)
- Is the model quality acceptable? (need eval, Day 44)

So today's goal: a *clean* baseline. Tomorrow we sweep.

### Reading — Where the result lives

Convention (from Day 38):

- Per-run dir: `/shared/runs/<YYYY-MM-DD-HHMM>-<label>/`
- Inside: `report.json`, `stdout.log`, `config.yaml` (capsule writes these).
- Pull `report.json` to your laptop for analysis; leave logs in shared for traceability.

### Exercise: Limitations List

Write one sentence describing what you'd need to run to answer each question:

1. "Is vLLM faster than SGLang for this model?"
2. "At what concurrency does the GPU saturate?"
3. "Does AWQ hurt quality on my use-case prompts?"
4. "Is this performance typical, or did I get lucky?"

---

## Part 5 — Hands-On: Run Your First Benchmark

### Exercise: First Clean Baseline

1. Lease an H100 or T4 node depending on availability.
2. Run the minimum-viable benchmark with `--stream`:
   ```
   capsule benchmark \
     --model meta-llama/Llama-3.1-8B-Instruct \
     --engine vllm \
     --concurrency 8 \
     --duration 60s \
     --out /shared/runs/$(date +%F-%H%M)-first/ \
     --stream
   ```
   Watch the live output. Confirm it produces a `report.json`.
3. Pull the report: `capsule storage get /shared/runs/<your-dir>/report.json ./`.
4. Release the lease: `capsule lease release`.

**Success criterion:** you have a `report.json` on your laptop and can open it.

---

## Part 6 — Hands-On: Annotate & Defend the Report

### Exercise: Annotation

Open `report.json`. For each metric, add an inline comment (you can use a `.jsonc` copy) linking it to the Phase 1 concept that explains it:

```jsonc
{
  "latency_ms": {
    "ttft_p50": 142,   // ← write your comment here: which phase-1 concept?
    "ttft_p99": 380,   // ← and here
    "itl_p50": 18,
    "itl_p99": 41
  },
  "throughput": {
    "tokens_per_sec": 1240  // ← and here
  }
}
```

### Exercise: Peer Defense

Pair with another learner. Each person:

1. Presents their report.
2. Answers: "Why is your `ttft_p50` what it is for this model + this GPU + this concurrency?"
3. Receives one challenge question from their partner.

Commit your annotated report to your fork.

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 42 · First Benchmark">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the key fields in a Capsule benchmark `report.json`?",
    "options": [
      "CPU usage, disk I/O, network latency, memory usage",
      "TTFT_p50, TTFT_p99, throughput (tok/s), concurrency, model config, GPU type, and timestamp",
      "Training loss, validation loss, epoch count, and learning rate",
      "User count, session duration, error rate, and uptime"
    ],
    "answer": 1,
    "explain": "A benchmark report captures latency percentiles (TTFT p50, p99), throughput (tokens/second), the concurrency and config used, GPU type, and timestamp. Every field is explainable using Phase-1 vocabulary: TTFT ← prefill, throughput ← decode + batching, GPU type ← bandwidth and compute specs."
  },
  {
    "stem": "Why does one benchmark run prove very little on its own?",
    "options": [
      "One run is statistically insufficient — variance from thermal state, neighbor processes, KV cache warmup, and measurement noise requires multiple runs to establish reliable baselines",
      "One run only tests one user, not a full production load",
      "One run cannot be compared against other models",
      "One run uses the wrong precision"
    ],
    "answer": 0,
    "explain": "A single benchmark run has confounds: the GPU may be thermally throttled from prior work, a noisy neighbor process consumes bandwidth, the KV cache isn't warm, or the run happened during a network congestion window. Multiple runs with consistent warmup, no neighbors, and stable thermal state produce reliable baselines."
  },
  {
    "stem": "What is the recommended artifact convention for benchmark run directories?",
    "options": [
      "/tmp/<model-name>/latest/",
      "/shared/runs/<YYYY-MM-DD-HHMM>-<label>/",
      "/home/<user>/benchmarks/<random-id>/",
      "/shared/models/<model-name>/benchmarks/"
    ],
    "answer": 1,
    "explain": "The convention from the lesson: `/shared/runs/<YYYY-MM-DD-HHMM>-<label>/`. The timestamp makes runs sortable and reproducible (you can find yesterday's run). The label identifies the configuration. Shared storage makes results accessible to teammates without copying."
  },
  {
    "stem": "If your benchmark shows TTFT_p99 = 850 ms, which Phase-1 concept explains this?",
    "options": [
      "The model's vocabulary size determines TTFT — larger vocabulary = slower tokenization",
      "TTFT is driven by the prefill phase (processing all input tokens) — high P99 TTFT suggests long input prompts, a large model requiring many compute cycles, or insufficient GPU compute throughput",
      "TTFT is determined by decode speed — high TTFT means slow token generation",
      "TTFT only depends on network latency between the user and the server"
    ],
    "answer": 1,
    "explain": "TTFT ← prefill phase. High P99 TTFT means the tail of the input distribution has long prompts (more tokens to process in prefill) or the GPU is compute-bottlenecked during prefill (insufficient TFLOP/s). Using Phase-1 vocabulary to annotate benchmark fields is the core skill being developed this week."
  },
  {
    "stem": "Why is committing your annotated benchmark report to your fork important?",
    "options": [
      "GitHub automatically improves the benchmark with each commit",
      "It creates a reproducible record of your findings that serves as evidence for the capstone and portfolio — annotated reports show you can connect data to concepts",
      "Committing triggers an automatic re-run to verify the results",
      "It is required for access to the shared GPU pool"
    ],
    "answer": 1,
    "explain": "The lesson states: 'Commit your annotated report to your fork.' Your fork is your portfolio. An annotated report — raw numbers + Phase-1 explanations for each metric — is evidence of technical depth. Hiring managers can read it. The capstone builds directly on this artifact."
  }
]
</script>
</div>

### Connect forward

Tomorrow: **varying parameters** — sweep `--concurrency`, `--tp`, and quantization, and see the Phase-1 tradeoffs play out in real numbers.

### Pre-read for tomorrow (Day 43 · Model Evaluation / Varying Parameters)

- **Resource:** none new — builds on Day 42 + recalls Week 3–4.
- **Reflection questions:**
  1. As `--concurrency` rises, which metrics will degrade first, and why?
  2. Doubling `--tp` from 1 to 2: what's the expected effect on throughput? On latency?
  3. FP8 vs FP16: which metrics change and which stay the same?

---

## Stuck?

Ask **oxtutor** — share your exact command, the error or unexpected output, and which GPU type you're on.
