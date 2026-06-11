---
drift: |
  In the new graph this slot is renamed "Model Evaluation" (placeholder title — see
  graph.json `_placeholder_title: true`). The backup lesson is "Varying Parameters",
  which is closely related but narrower: it covers parameter sweeps and how to interpret
  the resulting curves. Future authoring should broaden this to include quality evaluation
  (correctness, refusal rate, hallucination) alongside the parameter-sweep methodology;
  the wk5 "LLM Evaluation" module and the wk6 "Hallucinations & Evals" supplementary in
  week-06/module-1 are the natural inputs for the rewrite.
---

# Day 43 · Model Evaluation (Varying Parameters)

> **Concept of the day:** **one number means nothing; a sweep means everything.** Vary `--concurrency`, `--tp`, and quantization one axis at a time. Every observed change should map back to a Phase 1 concept you can name. If it doesn't, your model of the system is broken — fix the model, not the data.
> **Pre-reading:** none new — builds on Day 42 + recalls Week 3–4.
> **Source:** [Lab Guide Module 8](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md).

---

## Why this matters

This is the day Phase 1 stops being vocabulary and becomes prediction. Before each sweep you *predict* what the curve will look like; then you run it; then you reconcile. Surprises are where learning happens — and where good benchmark engineers earn their pay.

## Readiness check

1. What's a sweep, and why is it more informative than a single run?
2. Predict: as concurrency rises from 1 → 64 on a single H100 + 8B model, which metric breaks first?
3. Predict: TP=2 vs TP=1 on a 70B model on 8×H100 — throughput effect?
4. Predict: FP8 vs FP16 on the same model — which metrics move, which don't?
5. What's a confounding variable when running back-to-back benchmarks on the same node?

## Core concept

### The sweep template

Vary **one axis at a time**, hold everything else fixed:

```bash
for c in 1 2 4 8 16 32 64; do
  capsule benchmark \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --engine vllm \
    --concurrency $c \
    --duration 60s \
    --out /shared/runs/$(date +%F-%H%M)-sweep-c$c/
done
```

Then plot the metric vs the axis. The shape tells the story.

### Expected shapes — predict before you run

| Axis | Metric | Expected shape | Phase 1 concept |
|---|---|---|---|
| Concurrency ↑ | throughput | rises, then plateaus | continuous batching saturates the GPU (Week 4 Day 19) |
| Concurrency ↑ | TTFT p99 | rises, eventually cliffs | queueing delay + prefill contention (Week 3 Day 11) |
| Concurrency ↑ | ITL | rises gradually | per-step compute shared across more requests (Week 2 Day 9) |
| TP ↑ | throughput (large model) | rises sub-linearly | comm overhead eats some of the wins (Week 4 Day 16) |
| TP ↑ | per-request latency (large model) | drops then plateaus | memory pressure relieved, then bound by comm |
| Quant FP8 vs FP16 | throughput | rises ~1.5–2× | memory bandwidth + compute density (Week 3 Day 14) |
| Quant FP8 vs FP16 | quality (eval) | drops a little | precision loss; measure it Day 43 |

### Reading a saturation curve

```
throughput
   ▲
   │           ___________
   │         /
   │        /
   │      /
   │    /
   │  /
   └───────────────────▶ concurrency
        ↑
        the elbow = max useful concurrency
```

Before the elbow: throughput rises ~linearly with concurrency.
After the elbow: throughput is flat; **TTFT explodes**. You're queueing.

This single curve is the most important picture in Phase 1 made real.

### Confounding variables — guard against them

| Confound | Mitigation |
|---|---|
| Warmup not done | First request always slow; ignore or pre-warm |
| Other users on the node | Lease should isolate; verify GPU util at idle = 0 |
| Thermal throttling between runs | Pause 30s between runs; check `nvidia-smi -q -d CLOCK` |
| Prompt distribution drifted between runs | Use the same seed / prompt set |
| Quant cache reused | Clear engine cache between fundamentally different configs |

### What does this prove about the model?

Three patterns you should be able to spot:

1. **Memory bandwidth-bound** (small batch, large model): low GPU compute util, high memory bandwidth util. Quant helps a lot.
2. **Compute-bound** (large batch, small model): high GPU compute util. Quant helps less; TP / faster GPU helps.
3. **Communication-bound** (high TP, small model): per-step time barely drops adding GPUs. Drop TP or change model.

Naming the regime is the deliverable — the curve is just the evidence.

## Practice (90 min)

1. (15 min) **Predict before running.** Write down your expected throughput curve for concurrency 1, 2, 4, 8, 16, 32 on your chosen model + GPU. Sketch it.
2. (30 min) Run the concurrency sweep above. Stream the first run; let the rest finish.
3. (15 min) Pull all reports. Plot throughput vs concurrency (a spreadsheet works). Compare to your prediction.
4. (20 min) Reconcile: for every deviation between prediction and result, name the Phase 1 concept that explains it. Write 2–3 sentences per deviation.
5. (10 min) Pair: defend one of your reconciliations to a partner. They challenge.

## Wrap-up

Every student has a saturation curve and can explain its elbow in Phase-1 terms.

## Connect forward

Tomorrow: **interactive evaluation** — throughput numbers aren't quality. Spin up the chat UI and measure quality alongside speed.

---

## Pre-read for tomorrow (Day 43 · Interactive Evaluation)

- **Resource:** Lab Guide **Module 9** (~15 min).
- **Reflection questions:**
  1. What does the chat interface let you measure that the benchmark report cannot?
  2. Why might a "fast" config be the wrong choice for production?
  3. How do you separate *quality* from *latency* in your judgment?
