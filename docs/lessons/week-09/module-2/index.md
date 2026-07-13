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
    {status:week-09/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: The Sweep Template |
| Part 3 | Core Concepts: Expected Shapes & Phase-1 Recall |
| Part 4 | Deep Dive: Saturation Curves & Regimes |
| Part 5 | Hands-On: Predict, Then Run the Concurrency Sweep |
| Part 6 | Hands-On: Reconcile Predictions Against Results |
| Part 7 | Wrap-up & Connection |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review

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

## Part 2 — Core Concepts: The Sweep Template

### Reading — Vary one axis at a time

Vary **one axis at a time**, hold everything else fixed:

```bash
for c in 1 2 4 8 16 32 64; do
  capsule benchmark <config-tag> \
    meta-llama/Llama-3.1-8B-Instruct \
    --backend vllm \
    --concurrency $c \
    --input-length 256 \
    --output-length 256 \
    --num-prompts $((c * 20))
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

## Part 3 — Core Concepts: Expected Shapes & Phase-1 Recall

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

## Part 4 — Deep Dive: Saturation Curves & Regimes

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

## Part 5 — Hands-On: Predict, Then Run the Concurrency Sweep

### Exercise: Write Your Prediction First

Before running any commands, sketch the expected throughput curve for concurrency 1, 2, 4, 8, 16, 32 on your chosen model + GPU. Draw it (paper or whiteboard). Write down the concurrency value where you expect the elbow.

Then run the sweep:

```bash
for c in 1 2 4 8 16 32; do
  capsule benchmark <config-tag> \
    meta-llama/Llama-3.1-8B-Instruct \
    --backend vllm \
    --concurrency $c \
    --input-length 256 \
    --output-length 256 \
    --num-prompts $((c * 20))
done
```

Watch the first run's live output; let the rest finish.

---

## Part 6 — Hands-On: Reconcile Predictions Against Results

### Exercise: Plot & Reconcile

1. Open the Capsule benchmark dashboard and pull up every run from your sweep (they upload automatically unless you passed `--no-upload`).
2. Plot throughput vs concurrency (a spreadsheet works).
3. Mark the elbow you predicted vs the actual elbow.
4. For every deviation between prediction and result, write 2–3 sentences naming the Phase-1 concept that explains it.
5. Pair: defend one of your reconciliations. Your partner challenges.

---

## Part 7 — Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 43 · Varying Parameters">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What does the 'elbow' in a throughput vs concurrency curve represent?",
    "options": [
      "The point where the GPU runs out of memory and crashes",
      "The concurrency level at which the GPU transitions from underutilized to saturated — throughput peaks and then plateaus or degrades",
      "The maximum concurrency allowed by the serving engine",
      "The point where TTFT exceeds the SLO threshold"
    ],
    "answer": 1,
    "explain": "As concurrency increases from 1, throughput rises because more requests share fixed weight reads (batching efficiency improves). At the elbow, the GPU is fully saturated — adding more concurrency starts queuing requests rather than improving throughput. The elbow is the optimal operating point for throughput."
  },
  {
    "stem": "As concurrency increases beyond the elbow, which metrics degrade first and why?",
    "options": [
      "Throughput degrades first because the GPU runs out of memory",
      "TTFT and P99 latency degrade first — queued requests wait longer before prefill begins, even though throughput may remain stable for a while",
      "Model quality degrades because of KV cache pressure",
      "GPU utilization drops because the serving engine starts rejecting requests"
    ],
    "answer": 1,
    "explain": "Beyond the elbow, the GPU is saturated. New requests queue up. Queue time adds directly to TTFT — requests wait longer before their prefill even starts. P99 latency spikes because tail requests sit in queue longest. Throughput may still improve slightly via better batching, but user-facing latency degrades."
  },
  {
    "stem": "Doubling tensor parallelism (TP) from 1 to 2: what is the expected effect on latency and throughput?",
    "options": [
      "Both latency and throughput double",
      "Latency should decrease (each token computed faster with 2 GPUs sharing the work) but throughput may not double (communication overhead) — the tradeoff depends on model size and batch size",
      "Only throughput doubles; latency is unaffected",
      "Latency and throughput both remain the same — TP only affects memory fit"
    ],
    "answer": 1,
    "explain": "TP=2 splits each matrix multiply across 2 GPUs. Compute per GPU halves, reducing latency. But all-reduce communication between GPUs adds overhead. For small batches (latency-focused), TP=2 reduces TTFT. For large batches (throughput-focused), the communication overhead may limit throughput gains. The net effect must be measured."
  },
  {
    "stem": "What compute regime was your Day 43 concurrency sweep primarily in, and how did you determine it?",
    "options": [
      "Always compute-bound — GPU compute always bottlenecks LLM workloads",
      "Memory-bound at low concurrency (few requests, underutilized GPU), transitioning to compute-bound at high concurrency near saturation",
      "Network-bound — the bottleneck is always data transfer from client to server",
      "I/O-bound — disk reads of model weights dominate"
    ],
    "answer": 1,
    "explain": "At low concurrency, decode is memory-bound (few requests, low arithmetic intensity). As concurrency rises toward saturation, more requests share weight reads — intensity increases and the workload approaches compute-bound territory. The lesson asks students to classify their experiment's regime using Phase-1 concepts (arithmetic intensity, roofline)."
  },
  {
    "stem": "What should you do when your measured results differ from your prediction?",
    "options": [
      "Discard the prediction and treat the measurement as ground truth without explanation",
      "Write 2-3 sentences naming the specific Phase-1 concept that explains the deviation — reconciliation is the learning artifact",
      "Re-run the benchmark until the results match the prediction",
      "Lower your concurrency to reduce variance"
    ],
    "answer": 1,
    "explain": "The lesson states: 'For every deviation between prediction and result, write 2-3 sentences naming the Phase-1 concept that explains it.' Reconciliation is the core skill — connecting unexpected data to the underlying system behavior. This is what technical interviews ask for: not just what you measured, but why."
  },
  {
    "stem": "When switching from FP16 to FP8 quantization at the same concurrency level, which metrics improve and which remain roughly stable?",
    "options": [
      "Quality improves and latency stays the same",
      "Throughput rises (~1.5-2×) due to higher memory bandwidth and compute density, while quality drops a little (measurable via eval suite) — TTFT may also drop because smaller weights load faster",
      "Only quality changes; latency and throughput are unaffected by quantization",
      "All metrics degrade equally with FP8 because precision loss affects every operation"
    ],
    "answer": 1,
    "explain": "The lesson's FP8 vs FP16 prediction table: throughput rises ~1.5-2× (FP8 fits more activations in cache, doubles memory bandwidth), quality drops a little (measurable via eval on Day 44), and TTFT may decrease since smaller model loads faster. The metrics you must measure empirically are quality — throughput improvement is predictable but quality degradation varies by model and task."
  },
  {
    "stem": "Why is a parameter sweep more informative than a single benchmark run?",
    "options": [
      "Sweeps use more GPU time and therefore generate more accurate results",
      "A sweep traces a curve — it shows how the system responds to changes and reveals the operating point (elbow) and the regimes on either side; a single point has no context",
      "Sweeps allow you to average out measurement noise",
      "A single run can only measure one metric; a sweep measures all metrics simultaneously"
    ],
    "answer": 1,
    "explain": "The lesson's concept: 'one number means nothing; a sweep means everything.' A single TTFT=400ms data point tells you nothing about whether you're at peak efficiency. A 6-point concurrency sweep reveals the elbow, shows throughput saturation, shows P99 degradation — you can see the system's behavior envelope. The curve is the evidence; naming the regime is the deliverable."
  },
  {
    "stem": "The sweep template varies one axis at a time and holds everything else fixed. Why?",
    "options": [
      "So any change in the metric can be attributed to the single axis you varied — otherwise you can't tell which variable caused the effect",
      "Because the serving engine only accepts one flag per invocation",
      "Because varying two parameters at once crashes the GPU",
      "Because the dashboard can only plot one run at a time"
    ],
    "answer": 0,
    "explain": "Part 2's rule: 'Vary one axis at a time, hold everything else fixed.' If you change concurrency AND quantization together, a throughput shift can't be attributed to either — the experiment is confounded. Isolating one variable is what lets each observed change map back to a single Phase-1 concept you can name."
  },
  {
    "stem": "You benchmark an 8B model at TP=4 and throughput barely improves over TP=2, with GPU compute util only 0.35. Which regime is this?",
    "options": [
      "Memory bandwidth-bound — quantization would help most",
      "Compute-bound — a faster GPU or more TP would help",
      "Communication-bound — per-step time barely drops as you add GPUs; drop TP or change the model",
      "I/O-bound — disk reads of the model weights dominate"
    ],
    "answer": 2,
    "explain": "Part 4's third regime: communication-bound (high TP, small model). Adding GPUs via TP barely improves per-step time because all-reduce communication overhead eats the wins, and compute util stays low (0.35) because each GPU has too little work. The fix is to drop TP or move to a larger model — not more quant or a faster GPU."
  },
  {
    "stem": "Per the lesson's confound table, which is a real confounding variable when running back-to-back benchmarks on the same node — and its mitigation?",
    "options": [
      "The model's parameter count silently changing between runs; re-download the weights",
      "The CLI version being out of date; run `capsule update` between runs",
      "Thermal throttling from the previous run; pause ~30s between runs and check `nvidia-smi -q -d CLOCK`",
      "The dashboard being offline; pass `--no-upload`"
    ],
    "answer": 2,
    "explain": "Part 2's confound table lists thermal throttling between runs, mitigated by pausing ~30s and checking `nvidia-smi -q -d CLOCK`. Other listed confounds are cold warmup (pre-warm), neighbor processes (verify idle GPU util = 0), drifted prompt distribution (same seed/prompt set), and reused quant cache (clear between fundamentally different configs)."
  }
]
</script>
</div>

### Connect forward

Tomorrow: **interactive chat evaluation** — throughput numbers aren't quality. Spin up the chat UI and measure quality alongside speed.

### Pre-read for tomorrow (Day 44 · Interactive Evaluation)

- **Resource:** <a href="../../../readings/capsule/#day-43-interactive-evaluation">Capsule Power-User Pre-Lecture Reading — Day 43 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-9-model-evaluation-interactive-chat">Capsule Lab Guide</a> Module 9.
- **Reflection questions:**
  1. What does the chat interface let you measure that the benchmark report cannot?
  2. Why might a "fast" config be the wrong choice for production?
  3. How do you separate *quality* from *latency* in your judgment?

---

## Stuck?

Ask **oxtutor** — share your sweep results and the deviation you're trying to reconcile. It can help you trace back to the right Phase-1 concept.
