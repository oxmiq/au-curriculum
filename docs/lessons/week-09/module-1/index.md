---
drift: |
  Originally Day 41 of the former Capsule wk9. Now Day 41 of the new Benchmarking & Eval
  week (week-09/module-1), unchanged in scope. Source-material link paths bumped one
  level deeper.
---

# Day 41 · Your First Benchmark

> **Concept of the day:** `capsule benchmark` orchestrates a serving engine + a request load + metric collection. Phase-1 vocabulary (TTFT, ITL, p99, throughput) lands here in real numbers. Today: run *one* benchmark cleanly, end to end, on a leased GPU node.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-41-your-first-benchmark">Capsule Power-User Pre-Lecture Reading - Day 41 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-8-model-evaluation-benchmarking-the-inferencemax-path">Capsule Lab Guide</a> Module 8.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 - Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 41 · Benchmarking</span>
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

## Part 1 - Pre-Reading Review

### Reading - Why this matters

You've spent six weeks learning what TTFT, throughput, and p99 *mean*. Today you generate them yourself, on a real GPU, and read them off a real report. This is the moment Phase 1 becomes muscle memory rather than vocabulary.

### Exercise: Self-Check

Answer before reading on:

1. Name the three things a benchmark run consists of.
2. What's the minimal command to run a benchmark on a leased node?
3. What four metrics will the report contain? (Phase 1 recall.)
4. What does *one* benchmark prove? (Hint: very little - that's tomorrow's lesson.)
5. Where should the result file live?

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m1-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 8">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Which four serving backends does `capsule benchmark` support?",
    "options": [
      "vllm, sglang, tensorrt-llm, triton",
      "vllm, ollama, mlx, transformers",
      "vllm, llamacpp, mlx, oxpython",
      "llamacpp, exllama, mlx, deepspeed"
    ],
    "answer": 2,
    "explain": "The four supported backends are vllm (default; best for NVIDIA, batched serving, paged-attention), llamacpp (CPU-friendly, GGUF quants), mlx (Apple Silicon), and oxpython (the OXMIQ Python runtime for in-house eval). SGLang is a common distractor but is NOT one of them."
  },
  {
    "stem": "Which flag chooses the serving backend for a benchmark run?",
    "options": [
      "--engine",
      "--serve",
      "--runtime",
      "--backend"
    ],
    "answer": 3,
    "explain": "The backend is selected with `--backend` (for example `--backend llamacpp`). There is no `--engine` flag in `capsule benchmark`; if you omit `--backend`, vllm is the default on an NVIDIA box."
  },
  {
    "stem": "What does `--num-prompts` (`-n`) control, and what is its default?",
    "options": [
      "The total number of requests sent; it defaults to concurrency × 10",
      "How long the load runs in seconds; it defaults to 60",
      "The number of GPUs to use; it defaults to 1",
      "The number of benchmark iterations; it defaults to 3"
    ],
    "answer": 0,
    "explain": "`--num-prompts` (`-n`) sets the total number of requests sent to the server, and it defaults to concurrency × 10. Run size is controlled by `--num-prompts`, not by any duration flag."
  },
  {
    "stem": "By default, where do the results of a `capsule benchmark` run go?",
    "options": [
      "They are written to /shared/runs/<timestamp>/report.json",
      "They are saved to ~/.capsule/results/ on the remote",
      "They are uploaded to the Capsule benchmark dashboard unless you pass --no-upload",
      "They are printed to stdout and then discarded"
    ],
    "answer": 2,
    "explain": "Results upload to the Capsule benchmark dashboard by default; pass `--no-upload` to suppress this while iterating. There is no `/shared/runs/` convention for benchmark output; the dashboard is the destination."
  },
  {
    "stem": "Which metrics does a `capsule benchmark` run report?",
    "options": [
      "Training loss, validation loss, and epoch count",
      "Throughput, latency percentiles, and cost-per-token",
      "CPU usage, disk I/O, and network latency",
      "Time-to-first-token only"
    ],
    "answer": 1,
    "explain": "`capsule benchmark` drives the inference server with InferenceMAX and reports throughput, latency percentiles, and cost-per-token. Those three families are exactly the Phase-1 vocabulary you built up over prior weeks."
  },
  {
    "stem": "What is the minimum-viable command to benchmark a model on a remote machine?",
    "options": [
      "capsule benchmark --model <model> --engine vllm --duration 60s",
      "capsule bench <model> --backend auto --out /shared/runs/",
      "capsule benchmark run <model> --concurrency 8 --duration 60s",
      "capsule benchmark <config-tag> <model>"
    ],
    "answer": 3,
    "explain": "`capsule benchmark <config-tag> <model>` is the minimal form: it provisions an inference server on the target machine and drives it with InferenceMAX using defaults (vllm on NVIDIA). The other options invent flags like `--engine` and `--duration` that don't exist."
  },
  {
    "stem": "How do you benchmark an OpenAI-compatible endpoint you already have, without provisioning a machine?",
    "options": [
      "capsule benchmark --api-base <url> --api-key <key> <model>",
      "capsule benchmark --external-endpoint <url> <model>",
      "capsule benchmark --remote <url> --no-deploy <model>",
      "You cannot; capsule benchmark always provisions a fresh server"
    ],
    "answer": 0,
    "explain": "`--api-base` plus `--api-key` skips provisioning entirely and benchmarks an OpenAI-compatible endpoint you already have (for example a local `capsule chat` server). No `<config-tag>` is needed in that form."
  },
  {
    "stem": "You are iterating on a config and don't want results published to the dashboard yet. Which flag do you add?",
    "options": [
      "--dry-run",
      "--local-only",
      "--no-upload",
      "--skip-dashboard"
    ],
    "answer": 2,
    "explain": "`--no-upload` suppresses the default dashboard upload: the right choice while you're iterating and don't want noisy in-progress runs cluttering the shared dashboard. The other flags are fabricated."
  }
]
</script>
</div>

---

## Part 2 - Core Concepts: Benchmark Anatomy

### Reading - The three-piece architecture

```
┌────────────┐        ┌───────────────┐        ┌──────────────┐
│ load gen   │ ─────▶ │ serving       │ ─────▶ │ metric       │
│ (requests/s│        │ engine        │        │ collection   │
│ prompts)   │ ◀───── │ (vllm, etc.)  │ ◀───── │              │
└────────────┘        └───────────────┘        └──────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │ report.json  │
                      └──────────────┘
```

Three pieces:

1. **Load generator** - what prompts, what concurrency, how long.
2. **Serving engine** - which engine, which model, which config (TP, quant, batching).
3. **Metric collection** - TTFT, ITL, throughput, p50/p95/p99, GPU util.

### Reading - The minimum-viable command

At its smallest, a benchmark is just the target machine and the model:

```
capsule benchmark <config-tag> meta-llama/Llama-3.1-8B-Instruct
```

Add flags to shape the load:

```
capsule benchmark <config-tag> \
  meta-llama/Llama-3.1-8B-Instruct \
  --backend vllm \
  --concurrency 8 \
  --input-length 256 \
  --output-length 256 \
  --num-prompts 80
```

That's it. Defaults give sensible TP, quant, and prompt distribution. Results upload to the Capsule benchmark dashboard unless you pass `--no-upload`.

### Exercise: Command Anatomy

Without looking at the documentation:

1. What does `--concurrency 8` control? (number of simultaneous in-flight requests)
2. What does `--num-prompts 80` control? (the total number of requests sent before the run stops)
3. Where do the results go by default, and what does `--no-upload` change? (they upload to the Capsule benchmark dashboard; `--no-upload` keeps them off it)
4. If you omit `--backend`, what happens? (vllm is the default on an NVIDIA box)
5. Write the command to benchmark `Qwen/Qwen2.5-7B-Instruct` on `<config-tag>` at concurrency 4 with 80 total prompts, suppressing the dashboard upload.

---

## Part 3 - Core Concepts: Reading the Report

### Reading - Phase-1 vocabulary check

A typical `report.json` excerpt:

```json
{
  "config": {"model": "...", "backend": "vllm", "concurrency": 8, "tp": 1, "quant": "fp16"},
  "latency_ms": {"ttft_p50": 142, "ttft_p99": 380, "itl_p50": 18, "itl_p99": 41},
  "throughput": {"tokens_per_sec": 1240, "requests_per_sec": 7.2},
  "gpu": {"util_avg": 0.83, "mem_used_gb": 18.4}
}
```

You should be able to read every field without checking a glossary. If `ttft_p99` is 380 ms: is that compute-bound or memory-bound territory? (Week 2, Day 9.)

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

## Part 4 - Deep Dive: What One Benchmark Proves

### Reading - The limits of a single data point

A single number is just a data point. It tells you *this config, this load, this moment*. It can't tell you:

- Is this engine better than another? (need comparison)
- Does it scale? (need to vary load)
- Is the GPU saturated? (need to vary `--concurrency`)
- Is the model quality acceptable? (need eval, Day 43)

So today's goal: a *clean* baseline. Tomorrow we sweep.

### Reading - Where the result lives

`capsule benchmark` uploads each run to the Capsule benchmark dashboard by default:

- The dashboard is the durable home for a run: throughput, latency percentiles, and cost-per-token, keyed to the model + config you ran.
- Pass `--no-upload` while iterating to keep noisy in-progress runs off the shared dashboard.
- Open the dashboard to compare runs side by side and share links with teammates.

### Exercise: Limitations List

Write one sentence describing what you'd need to run to answer each question:

1. "Is vLLM faster than llamacpp for this model?"
2. "At what concurrency does the GPU saturate?"
3. "Does AWQ hurt quality on my use-case prompts?"
4. "Is this performance typical, or did I get lucky?"

---

## Part 5 - Hands-On: Run Your First Benchmark

### Exercise: First Clean Baseline

1. Lease an H100 or T4 node depending on availability.
2. Run the minimum-viable benchmark:
   ```
   capsule benchmark <config-tag> \
     meta-llama/Llama-3.1-8B-Instruct \
     --backend vllm \
     --concurrency 8 \
     --input-length 256 \
     --output-length 256 \
     --num-prompts 80
   ```
   Watch the live output. Confirm the run completes and reports throughput, latency percentiles, and cost-per-token.

3. Open the Capsule benchmark dashboard and find your run.
4. Release the machine when done: `capsule session end` (or `capsule session endall`).

**Success criterion:** your run appears on the dashboard and you can read its metrics.

---

## Part 6 - Hands-On: Annotate & Defend the Report

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

## Part 7 - Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m1-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 41 · First Benchmark">
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
    "stem": "The lesson describes a benchmark run as a three-piece architecture. What are the three pieces?",
    "options": [
      "A load generator (prompts + concurrency), a serving engine (vllm etc. with a model/config), and metric collection (TTFT, ITL, throughput, percentiles)",
      "A dataset, a training loop, and a saved checkpoint",
      "A load balancer, a database, and a cache layer",
      "A tokenizer, an optimizer, and a learning-rate scheduler"
    ],
    "answer": 0,
    "explain": "Part 2's diagram breaks a benchmark into three pieces: the load generator (what prompts, what concurrency, how long), the serving engine (which engine, model, and config: TP, quant, batching), and metric collection (TTFT, ITL, throughput, p50/p95/p99, GPU util). Training-loop and web-infra options are distractors; a benchmark drives inference, it does not train."
  },
  {
    "stem": "You run `capsule benchmark <config-tag> meta-llama/Llama-3.1-8B-Instruct` on an NVIDIA node and omit `--backend`. Which serving backend runs?",
    "options": [
      "llamacpp",
      "mlx",
      "vllm",
      "oxpython"
    ],
    "answer": 2,
    "explain": "Defaults give sensible TP, quant, and prompt distribution; and vllm is the default backend on an NVIDIA box (it is best for batched serving with paged-attention). The four supported backends are vllm, llamacpp, mlx, and oxpython; mlx targets Apple Silicon and oxpython is the OXMIQ Python runtime, so neither is the NVIDIA default."
  },
  {
    "stem": "In `capsule benchmark ... --concurrency 8 --num-prompts 80`, what does `--num-prompts` control?",
    "options": [
      "How many seconds the load runs before stopping",
      "The number of GPUs allocated to the run",
      "The number of simultaneous in-flight requests",
      "The total number of requests sent before the run stops"
    ],
    "answer": 3,
    "explain": "`--num-prompts` is the total number of requests sent before the run stops; `--concurrency` is the number of simultaneous in-flight requests. Run size is set by `--num-prompts`, not by any duration flag; there is no `--duration` in `capsule benchmark`."
  },
  {
    "stem": "Today's goal was one clean baseline. Which question can that single benchmark run NOT answer on its own?",
    "options": [
      "What throughput this exact config achieved at this moment",
      "What TTFT p99 this config produced under this load",
      "Whether vllm is faster than llamacpp for this model: that needs a comparison run",
      "What the GPU memory usage was during the run"
    ],
    "answer": 2,
    "explain": "Part 4 lists what one benchmark can't tell you: is this engine better than another (need comparison), does it scale (vary load), is the GPU saturated (vary --concurrency), is quality acceptable (need eval, Day 43). A single run does report this config's own throughput, TTFT, and memory at this moment; those it can answer."
  },
  {
    "stem": "Why does one benchmark run prove very little on its own?",
    "options": [
      "One run is statistically insufficient; variance from thermal state, neighbor processes, KV cache warmup, and measurement noise requires multiple runs to establish reliable baselines",
      "One run only tests one user, not a full production load",
      "One run cannot be compared against other models",
      "One run uses the wrong precision"
    ],
    "answer": 0,
    "explain": "A single benchmark run has confounds: the GPU may be thermally throttled from prior work, a noisy neighbor process consumes bandwidth, the KV cache isn't warm, or the run happened during a network congestion window. Multiple runs with consistent warmup, no neighbors, and stable thermal state produce reliable baselines."
  },
  {
    "stem": "Where do the results of a `capsule benchmark` run go by default?",
    "options": [
      "To a per-run directory under /shared/runs/<YYYY-MM-DD-HHMM>-<label>/",
      "They are uploaded to the Capsule benchmark dashboard unless you pass --no-upload",
      "To ~/.capsule/results/ on the remote node",
      "They print to stdout and are then discarded"
    ],
    "answer": 1,
    "explain": "By default each run uploads to the Capsule benchmark dashboard, keyed to the model + config; that is the durable, shareable home for throughput, latency percentiles, and cost-per-token. Pass `--no-upload` to keep in-progress runs off the shared dashboard while iterating. There is no `/shared/runs/` directory convention for benchmark output."
  },
  {
    "stem": "If your benchmark shows TTFT_p99 = 850 ms, which Phase-1 concept explains this?",
    "options": [
      "The model's vocabulary size determines TTFT; larger vocabulary = slower tokenization",
      "TTFT is driven by the prefill phase (processing all input tokens); high P99 TTFT suggests long input prompts, a large model requiring many compute cycles, or insufficient GPU compute throughput",
      "TTFT is determined by decode speed; high TTFT means slow token generation",
      "TTFT only depends on network latency between the user and the server"
    ],
    "answer": 1,
    "explain": "TTFT ← prefill phase. High P99 TTFT means the tail of the input distribution has long prompts (more tokens to process in prefill) or the GPU is compute-bottlenecked during prefill (insufficient TFLOP/s). Using Phase-1 vocabulary to annotate benchmark fields is the core skill being developed this week."
  },
  {
    "stem": "Why is committing your annotated benchmark report to your fork important?",
    "options": [
      "GitHub automatically improves the benchmark with each commit",
      "It creates a reproducible record of your findings that serves as evidence for the capstone and portfolio; annotated reports show you can connect data to concepts",
      "Committing triggers an automatic re-run to verify the results",
      "It is required for access to the shared GPU pool"
    ],
    "answer": 1,
    "explain": "The lesson states: 'Commit your annotated report to your fork.' Your fork is your portfolio. An annotated report, raw numbers + Phase-1 explanations for each metric, is evidence of technical depth. Hiring managers can read it. The capstone builds directly on this artifact."
  }
]
</script>
</div>

### Connect forward

Tomorrow: **varying parameters** - sweep `--concurrency`, `--tp`, and quantization, and see the Phase-1 tradeoffs play out in real numbers.

### Pre-read for tomorrow (Day 42 · Model Evaluation / Varying Parameters)

- **Resource:** none new - builds on Day 41 + recalls Week 3–4.
- **Reflection questions:**
  1. As `--concurrency` rises, which metrics will degrade first, and why?
  2. Doubling `--tp` from 1 to 2: what's the expected effect on throughput? On latency?
  3. FP8 vs FP16: which metrics change and which stay the same?

---

## Stuck?

Ask **oxtutor**; share your exact command, the error or unexpected output, and which GPU type you're on.
