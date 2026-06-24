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

> **Concept of the day:** **one number means nothing; a sweep means everything.** Vary `--concurrency`, `--tp`, and quantization one axis at a time. Every observed change should map back to a Phase 1 concept you can name. If it doesn't, your model of the system is broken — fix the model, not the data.<br>
> **Pre-reading:** none new — builds on Day 42 + recalls Week 3–4.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 — Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 43 · Model Evaluation</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-09/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: The Sweep Template | 25 min |
| Part 3 | Core Concepts: Expected Shapes & Phase-1 Recall | 20 min |
| Part 4 | Deep Dive: Saturation Curves & Regimes | 20 min |
| Part 5 | Hands-On: Predict, Then Run the Concurrency Sweep | 35 min |
| Part 6 | Hands-On: Reconcile Predictions Against Results | 20 min |
| Part 7 | Wrap-up & Connection | 10 min |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review · 15 min

### Reading — Why this matters

This is the day Phase 1 stops being vocabulary and becomes prediction. Before each sweep you *predict* what the curve will look like; then you run it; then you reconcile. Surprises are where learning happens — and where good benchmark engineers earn their pay.

### Exercise: Self-Check (Predict Before Reading)

Write your predictions now — before reading any further:

1. What's a sweep, and why is it more informative than a single run?
2. Predict: as concurrency rises from 1 → 64 on a single H100 + 8B model, which metric breaks first?
3. Predict: TP=2 vs TP=1 on a 70B model on 8×H100 — throughput effect?
4. Predict: FP8 vs FP16 on the same model — which metrics move, which don't?
5. What's a confounding variable when running back-to-back benchmarks on the same node?

Keep your written predictions — you'll compare them against reality in Part 6.

---

## Part 2 — Core Concepts: The Sweep Template · 25 min

### Reading — Vary one axis at a time

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

### Reading — Confounding variables: guard against them

| Confound | Mitigation |
|---|---|
| Warmup not done | First request always slow; ignore or pre-warm |
| Other users on the node | Lease should isolate; verify GPU util at idle = 0 |
| Thermal throttling between runs | Pause 30s between runs; check `nvidia-smi -q -d CLOCK` |
| Prompt distribution drifted between runs | Use the same seed / prompt set |
| Quant cache reused | Clear engine cache between fundamentally different configs |

### Exercise: Sweep Design

Design (don't run yet) three sweeps:

1. **Concurrency sweep:** axis = concurrency [1,2,4,8,16,32], everything else fixed. Write the loop command.
2. **TP sweep:** axis = tensor parallelism [1,2,4,8] on a 70B model. What GPU count do you need for TP=8?
3. **Quantization sweep:** same model, FP16 vs FP8 vs AWQ at fixed concurrency 8. What changes in the command?

---

## Part 3 — Core Concepts: Expected Shapes & Phase-1 Recall · 20 min

### Reading — Predict before you run

| Axis | Metric | Expected shape | Phase 1 concept |
|---|---|---|---|
| Concurrency ↑ | throughput | rises, then plateaus | continuous batching saturates the GPU (Week 4 Day 19) |
| Concurrency ↑ | TTFT p99 | rises, eventually cliffs | queueing delay + prefill contention (Week 3 Day 11) |
| Concurrency ↑ | ITL | rises gradually | per-step compute shared across more requests (Week 2 Day 9) |
| TP ↑ | throughput (large model) | rises sub-linearly | comm overhead eats some of the wins (Week 4 Day 16) |
| TP ↑ | per-request latency (large model) | drops then plateaus | memory pressure relieved, then bound by comm |
| Quant FP8 vs FP16 | throughput | rises ~1.5–2× | memory bandwidth + compute density (Week 3 Day 14) |
| Quant FP8 vs FP16 | quality (eval) | drops a little | precision loss; measure it Day 44 |

### Exercise: Phase-1 Link

For each row in the table above, write the exact Phase-1 concept in your own words (2 sentences). Do not copy from the table — use the Week number to find your notes if needed.

---

## Part 4 — Deep Dive: Saturation Curves & Regimes · 20 min

### Reading — Reading a saturation curve

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

### Reading — Three regimes to name

1. **Memory bandwidth-bound** (small batch, large model): low GPU compute util, high memory bandwidth util. Quant helps a lot.
2. **Compute-bound** (large batch, small model): high GPU compute util. Quant helps less; TP / faster GPU helps.
3. **Communication-bound** (high TP, small model): per-step time barely drops adding GPUs. Drop TP or change model.

Naming the regime is the deliverable — the curve is just the evidence.

### Exercise: Regime Identification

Given these observations, name the regime and explain your reasoning:

1. 8B model, concurrency 1, `gpu.util_avg: 0.08`, throughput: 200 tok/s. Adding concurrency to 8 → throughput 1100 tok/s.
2. 70B model, TP=1 (requires KV offload), GPU memory at 99%. Switching to TP=2 → throughput 2×.
3. 8B model, TP=4, throughput barely improves vs TP=2. GPU compute util: 0.35.

---

## Part 5 — Hands-On: Predict, Then Run the Concurrency Sweep · 35 min

### Exercise: Write Your Prediction First

Before running any commands, sketch the expected throughput curve for concurrency 1, 2, 4, 8, 16, 32 on your chosen model + GPU. Draw it (paper or whiteboard). Write down the concurrency value where you expect the elbow.

Then run the sweep:

```bash
for c in 1 2 4 8 16 32; do
  capsule benchmark \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --engine vllm \
    --concurrency $c \
    --duration 60s \
    --out /shared/runs/$(date +%F-%H%M)-sweep-c$c/
done
```

Stream the first run (`--stream`); let the rest finish.

---

## Part 6 — Hands-On: Reconcile Predictions Against Results · 20 min

### Exercise: Plot & Reconcile

1. Pull all reports: `capsule storage get /shared/runs/ ./sweeps/ --glob '*sweep-c*'`
2. Plot throughput vs concurrency (a spreadsheet works).
3. Mark the elbow you predicted vs the actual elbow.
4. For every deviation between prediction and result, write 2–3 sentences naming the Phase-1 concept that explains it.
5. Pair: defend one of your reconciliations. Your partner challenges.

---

## Part 7 — Wrap-up & Connection · 10 min

### Self-check

- [ ] I completed a 6-point concurrency sweep and have results for each point
- [ ] I can identify the elbow in my throughput curve and explain it with a Phase-1 concept
- [ ] I named the compute regime for today's experiment (memory-bound / compute-bound / comm-bound)
- [ ] I reconciled at least one prediction deviation in writing
- [ ] My sweep results are committed to my fork

### Connect forward

Tomorrow: **interactive chat evaluation** — throughput numbers aren't quality. Spin up the chat UI and measure quality alongside speed.

### Pre-read for tomorrow (Day 44 · Interactive Evaluation)

- **Resource:** Lab Guide **Module 9** (~15 min).
- **Reflection questions:**
  1. What does the chat interface let you measure that the benchmark report cannot?
  2. Why might a "fast" config be the wrong choice for production?
  3. How do you separate *quality* from *latency* in your judgment?

---

## Stuck?

Ask **oxtutor** — share your sweep results and the deviation you're trying to reconcile. It can help you trace back to the right Phase-1 concept.
