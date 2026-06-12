# Week 4 — Scaling & Stacks · Module Assignment

> **Source:** Mindmap Week 4 Day 20 + Inference Engineering Worksheets Appendix C (serving-system design rubric).

## What you submit

A **serving-system design document** (1–2 pages) for the scenario below, plus a **back-of-envelope numerical justification**.

## The scenario

- **Model:** Llama-3-70B, FP16 weights (baseline).
- **Hardware:** 8 × H100 80 GB SXM5 in one node, NVLink 4.
- **Workload:** chat / Q&A.
- **SLOs:**
  - **P99 end-to-end latency** < 500 ms for a 200-input / 100-output token request.
  - **Throughput** ≥ 50 requests/sec sustained.
- **Other constraints:** must stay on the given hardware; no extra nodes.

## Required sections

1. **Memory budget.** Per-GPU weight shard, KV cache per token, max concurrent requests at full context. Show your math.
2. **Parallelism choice.** Pick TP, PP, EP combination. Justify.
3. **Engine choice.** Pick vLLM, TGI, TensorRT-LLM, or SGLang. One-paragraph justification using the Day 19 rubric.
4. **Optimization stack.** Which of {FP8 weights, FP8 KV cache, speculative decoding, prefix caching} would you enable, in what order? Why?
5. **Risk analysis.** Two things that could blow your P99 budget under load. What you'd monitor.
6. **Verdict.** Do the chosen knobs meet both SLOs? Show numerical reasoning (per-token decode time × output tokens + TTFT < 500 ms; concurrent request count × per-request rate ≥ 50 req/s).

## What "good" looks like

- Memory math is **internally consistent** with Week 3's calculator output.
- Parallelism choice is **TP = 8** (with one-sentence justification noting NVLink).
- Engine choice is defended on workload fit, not popularity.
- The optimization stack is ordered by **impact** (FP8 weights before speculative, KV-FP8 before all-out INT4 weights).
- The numerical verdict is **honest** — if you don't make the SLO, say what relaxation you'd negotiate (P99 → P95? throughput → 40 req/s? smaller model?).

## Grading

- All 6 sections present — pass on each.
- Numbers internally consistent — pass.
- Verdict is honest (no over-claiming) — pass.
- Need 5/6 sections passing to pass the assignment.

## Reference solution

Worksheets Appendix C in `planning/source-material/Inference Engineering/` has a worked example for the *same* scenario at FP8 + speculative decoding, hitting both SLOs. Use it to calibrate after you've drafted yours — not before.

## Why this assignment exists

This is the **end-to-end serving-engineer interview question**. By Friday you should be able to whiteboard this in 30 minutes. It's also exactly the structure of the Phase-1 wrap assessment (Week 5).
