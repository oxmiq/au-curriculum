---
drift: |
  Originally Day 41 of the former Capsule wk9. Now Day 42 of the new Benchmarking & Eval
  week (week-09/module-1), unchanged in scope. Source-material link paths bumped one
  level deeper.
---

# Day 42 · Your First Benchmark

> **Concept of the day:** `capsule benchmark` orchestrates a serving engine + a request load + metric collection. Phase-1 vocabulary (TTFT, ITL, p99, throughput) lands here in real numbers. Today: run *one* benchmark cleanly, end to end, on a leased GPU node.<br>
> **Pre-reading:** Lab Guide **Module 8** (~20 min).

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
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-09/module-1}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Benchmark Anatomy | 25 min |
| Part 3 | Core Concepts: Reading the Report | 20 min |
| Part 4 | Deep Dive: What One Benchmark Proves (and Doesn't) | 15 min |
| Part 5 | Hands-On: Run Your First Benchmark | 35 min |
| Part 6 | Hands-On: Annotate & Defend the Report | 25 min |
| Part 7 | Wrap-up & Connection | 10 min |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review · 15 min

### Reading — Why this matters

You've spent six weeks learning what TTFT, throughput, and p99 *mean*. Today you generate them yourself, on a real GPU, and read them off a real report. This is the moment Phase 1 becomes muscle memory rather than vocabulary.

### Exercise: Self-Check

Answer before reading on:

1. Name the three things a benchmark run consists of.
2. What's the minimal command to run a benchmark on a leased node?
3. What four metrics will the report contain? (Phase 1 recall.)
4. What does *one* benchmark prove? (Hint: very little — that's tomorrow's lesson.)
5. Where should the result file live?

---

## Part 2 — Core Concepts: Benchmark Anatomy · 25 min

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

## Part 3 — Core Concepts: Reading the Report · 20 min

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

## Part 4 — Deep Dive: What One Benchmark Proves · 15 min

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

## Part 5 — Hands-On: Run Your First Benchmark · 35 min

### Exercise: First Clean Baseline

1. (5 min) Lease an H100 or T4 node depending on availability.
2. (20 min) Run the minimum-viable benchmark with `--stream`:
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
3. (5 min) Pull the report: `capsule storage get /shared/runs/<your-dir>/report.json ./`.
4. (5 min) Release the lease: `capsule lease release`.

**Success criterion:** you have a `report.json` on your laptop and can open it.

---

## Part 6 — Hands-On: Annotate & Defend the Report · 25 min

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

1. Presents their report (2 min).
2. Answers: "Why is your `ttft_p50` what it is for this model + this GPU + this concurrency?"
3. Receives one challenge question from their partner.

Commit your annotated report to your fork.

---

## Part 7 — Wrap-up & Connection · 10 min

### Self-check

- [ ] I ran a benchmark end-to-end and have a `report.json` on my laptop
- [ ] I can explain every field in the report using Phase-1 vocabulary (no glossary needed)
- [ ] I know why one benchmark proves very little on its own
- [ ] I know the artifact convention (`/shared/runs/<YYYY-MM-DD-HHMM>-<label>/`)
- [ ] My annotated report is committed to my fork

### Connect forward

Tomorrow: **varying parameters** — sweep `--concurrency`, `--tp`, and quantization, and see the Phase-1 tradeoffs play out in real numbers.

### Pre-read for tomorrow (Day 43 · Model Evaluation / Varying Parameters)

- **Resource:** Re-skim Week 4 Day 16 (tensor parallelism) + Week 3 Day 14 (quantization).
- **Reflection questions:**
  1. As `--concurrency` rises, which metrics will degrade first, and why?
  2. Doubling `--tp` from 1 to 2: what's the expected effect on throughput? On latency?
  3. FP8 vs FP16: which metrics change and which stay the same?

---

## Stuck?

Ask **oxtutor** — share your exact command, the error or unexpected output, and which GPU type you're on.
