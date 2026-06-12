---
drift: |
  Originally Day 41 of the former Capsule wk9. Now Day 42 of the new Benchmarking & Eval
  week (week-09/module-1), unchanged in scope. Source-material link paths bumped one
  level deeper.
---

# Day 42 · Your First Benchmark

> **Concept of the day:** `capsule benchmark` orchestrates a serving engine + a request load + metric collection. Phase-1 vocabulary (TTFT, ITL, p99, throughput) lands here in real numbers. Today: run *one* benchmark cleanly, end to end, on a leased GPU node.
> **Pre-reading:** Lab Guide **Module 8** (~20 min).
> **Source:** [Lab Guide Module 8](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md).

---

## Why this matters

You've spent six weeks learning what TTFT, throughput, and p99 *mean*. Today you generate them yourself, on a real GPU, and read them off a real report. This is the moment Phase 1 becomes muscle memory rather than vocabulary.

## Readiness check

1. Name the three things a benchmark run consists of.
2. What's the minimal command to run a benchmark on a leased node?
3. What four metrics will the report contain? (Phase 1 recall.)
4. What does *one* benchmark prove? (Hint: very little — that's tomorrow's lesson.)
5. Where should the result file live?

## Core concept

### Anatomy of a benchmark run

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

### The minimum-viable command

```
capsule benchmark \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --engine vllm \
  --concurrency 8 \
  --duration 60s \
  --out /shared/runs/$(date +%F-%H%M)-first/
```

That's it. Defaults give sensible TP, quant, and prompt distribution. The report writes to `/shared/runs/.../report.json`.

### Reading the report — Phase 1 vocabulary check

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

### Why "one benchmark" proves very little

A single number is just a data point. It tells you *this config, this load, this moment*. It can't tell you:

- Is this engine better than another? (need comparison)
- Does it scale? (need to vary load)
- Is the GPU saturated? (need to vary `--concurrency`)
- Is the model quality acceptable? (need eval, Day 43)

So today's goal: a *clean* baseline. Tomorrow we sweep.

### Where the result lives

Convention (from Day 39):

- Per-run dir: `/shared/runs/<YYYY-MM-DD-HHMM>-<label>/`
- Inside: `report.json`, `stdout.log`, `config.yaml` (capsule writes these).
- Pull `report.json` to your laptop for analysis; leave logs in shared for traceability.

## Practice (90 min)

1. (10 min) Lease an H100 or T4 node depending on availability.
2. (25 min) Run the minimum-viable benchmark above with `--stream`. Watch live output. Confirm it produces a `report.json`.
3. (20 min) Pull `report.json` to your laptop. Open it. Annotate each field with the Phase 1 concept it represents (Week 5 metrics page, Days 21–22, is your friend).
4. (25 min) Pair: trade reports. Each person *defends* their numbers — why is `ttft_p50` what it is for this model + this GPU + this concurrency?
5. (10 min) Release the lease. Commit your annotated report to your fork.

## Wrap-up

Every student has one clean baseline report and can read every field in Phase-1 vocabulary.

## Connect forward

Tomorrow: **varying parameters** — sweep `--concurrency`, `--tp`, and quantization, and see the Phase-1 tradeoffs play out in real numbers.

---

## Pre-read for tomorrow (Day 42 · Varying Parameters)

- **Resource:** Re-skim Week 4 Day 16 (tensor parallelism) + Week 3 Day 14 (quantization).
- **Reflection questions:**
  1. As `--concurrency` rises, which metrics will degrade first, and why?
  2. Doubling `--tp` from 1 to 2: what's the expected effect on throughput? On latency?
  3. FP8 vs FP16: which metrics change and which stay the same?
