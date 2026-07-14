# Day 20 (Fri) · Week 4 Consolidation

> **Goal of the day:** consolidate parallelism + speculative decoding + serving engines. No new content: practice, ask, catch up.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 - Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 20 · Consolidation</span>
    {status:week-04/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This consolidation day is different from other days; it's for practice and review. Here's how your ~3 hours are organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Week 4 Knowledge Check |
| Part 2 | Self-Assessment |
| Part 3 | Practice: Tensor Parallelism |
| Part 4 | Practice: Pipeline & Expert Parallelism |
| Part 5 | Practice: Speculative Decoding |
| Part 6 | Practice: Serving Engines |
| Part 7 | Open Lab & Wrap-up |

---

## Part 1 - Week 4 Knowledge Check
### Exercise: Take the Knowledge Check

[Take the Week 4 knowledge check](knowledge-check.md): covers tensor parallelism, pipeline/expert parallelism, speculative decoding, and serving engines.

**Passing score:** 10/15 (67%)

If you score below 10/15:
- Review the questions you got wrong
- Go back to the relevant day's content
- Re-read that section
- Retake the quiz

---

## Part 2 - Self-Assessment
### Self-Check List

Go through each item and mark whether you can do it **without notes**:

- [ ] Explain what tensor parallelism splits and what it replicates across GPUs
- [ ] Describe why TP requires NVLink (intra-node only)
- [ ] Compare tensor parallelism vs pipeline parallelism: when to use each
- [ ] Explain expert parallelism and why it helps MoE models
- [ ] Describe speculative decoding: the idea and why it works
- [ ] Calculate speedup from speculation (e.g., 3x speculation, 80% acceptance)
- [ ] Name two serving engines and explain their batching strategies
- [ ] Explain continuous batching vs static batching
- [ ] Describe what continuous batching solves (queueing vs throughput tradeoff)

### Action Items

For any item you can't do:

1. Note which day it came from (Day 16, 17, 18, or 19)
2. Spend 10 minutes reviewing that day's content
3. Practice until you can do it from memory

---

## Part 3 - Practice - Tensor Parallelism
### Hands-On: TP Calculations

Practice these calculations:

**Exercise 1: Memory per GPU**
```
Given: 70B parameter model in FP16 (2 bytes per parameter)
       Tensor parallelism degree = 8
Question: How much memory for weights per GPU?
Answer: (70B × 2) / 8 = 17.5 GB per GPU
```

**Exercise 2: All-reduce bandwidth**
```
Given: H100 NVLink bandwidth = 900 GB/s
       Activation size per layer = 1 GB
       Model has 80 layers
Question: How much data per forward pass?
Answer: 80 GB (all-reduce after each layer)
```

**Exercise 3: TP vs single GPU latency**
```
Given: Single GPU can't fit 70B model
       TP=8 splits the model
Question: Why is TP better than just using 1 GPU with a smaller model?
Answer: TP keeps the full model while PP splits that break the compute graph
```

### TP Decision Tree

Fill in this decision tree from memory:

```
Model fits in one GPU?
├── Yes → No parallelism needed
└── No → Is decode latency critical?
         ├── Yes → Use TP (intra-node only, NVLink required)
         └── No → Is model too large for one node?
                   ├── Yes → Use PP or EP
                   └── No → Consider TP + PP combination
```

---

## Part 4 - Practice - Pipeline & Expert Parallelism
### Hands-On: PP vs EP Comparison

Complete this comparison table from memory:

| Aspect | Tensor Parallelism | Pipeline Parallelism | Expert Parallelism |
|--------|--------------------|--------------------|--------------------|
| What is split? | | | |
| Communication pattern | | | |
| Latency impact | | | |
| Best for | | | |
| Requirement | | | |

**Then verify against Day 16-17 content.**

### MoE Expert Calculation

```
Given: Mixtral 8x7B (8 experts, 7B params each active)
       Total params = 47B (including shared)
       EP degree = 8

Questions:
1. How many experts per GPU?
2. How much parameter memory per GPU?
3. Why does EP reduce memory vs TP?
```

---

## Part 5 - Practice - Speculative Decoding
### Hands-On: Speculation Math

Practice calculating speedup from speculative decoding:

**Exercise 1: Basic speedup**
```
Given: Speculation factor = 4 (propose 4 tokens)
       Acceptance rate = 75%
Questions:
1. How many tokens accepted on average per speculation round?
2. What's the effective tokens per decode step?
3. What's the speedup vs normal decoding?
```

**Exercise 2: Latency reduction**
```
Given: Normal decode = 100ms per token
       Speculation = 4x proposal (25ms for 4 tokens)
       Acceptance = 80%
Questions:
1. Time for accepted tokens?
2. Time for rejected (recomputed) tokens?
3. Average time per output token?
4. Speedup factor?
```

### Key Insight

> Speculative decoding turns sequential decode into (partially) parallel work. The GPU proposes multiple tokens, then verifies them in parallel. Accepted tokens don't need recomputation.

---

## Part 6 - Practice - Serving Engines
### Hands-On: Engine Comparison

Match each serving engine to its key characteristic:

| Engine | Key Feature |
|--------|-------------|
| vLLM | |
| TensorRT-LLM | |
| Triton Inference Server | |
| SGLang | |

**Options:**
- A) NVIDIA's optimized engine with FP8 support
- B) PagedAttention + continuous batching from HuggingFace team
- C) Dynamic batching with automatic batch composition
- D) Radically efficient attention with FlashDecoding

### Batching Strategy Drill

Explain why each workload needs different batching:

```
Workload 1: Chatbot (single-user queries, latency-sensitive)
→ Use: _______________ batching because: _______________

Workload 2: Batch embedding (offline processing, throughput-sensitive)
→ Use: _______________ batching because: _______________

Workload 3: Agent loops (bursty, variable length)
→ Use: _______________ batching because: _______________
```

---

## Part 7 - Wrap-up & Connection
### What to Do

This is open time. Choose what you need:

1. **Catch up** on any assignments from Mon–Thu
2. **Ask questions**: use oxtutor or review the relevant day
3. **Extra practice**: generate more exercises on any concept
4. **Preview Week 5**: start the pre-reading for Day 21

### Connect Forward

Week 5 begins on Monday. You'll learn about:
- Metrics that matter (TTFT, TPOT, throughput)
- Production patterns
- Cost economics

### Pre-read for Monday (Week 5, Day 21)

**Resource:** <a href="https://www.anyscale.com/blog/llm-inference-performance" target="_blank" rel="noopener">Anyscale - LLM Inference Performance</a>. Alternative: <a href="https://www.baseten.co/blog/understanding-llm-latency/" target="_blank" rel="noopener">Baseten - Understanding LLM Latency</a>.

**Reflection questions:**

1. What does TTFT stand for? What drives it?
2. What does TPOT stand for? What drives it?
3. Why is throughput/$/token the ultimate metric?

---

## Stuck?

Ask **oxtutor** to re-explain any Week 4 concept. The TP-vs-PP-vs-EP decision tree is the most-asked interview question of the entire program.