# Day 10 (Fri) · Week 2 Consolidation

> **Goal of the day:** consolidate the GPU & memory mental model. No new content.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 2 - The GPU &amp; Memory</a>
    <span class="sep">/</span>
    <span>Day 10 · Consolidation</span>
    {status:week-02/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This consolidation day is different from other days; it's for practice and review. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Week 2 Knowledge Check |
| Part 2 | Self-Assessment |
| Part 3 | Practice: Pipeline Review |
| Part 4 | Practice: GPU & Memory Review |
| Part 5 | Feynman Teach-Back |
| Part 6 | Open Lab & Wrap-up |

---

## Part 1 - Week 2 Knowledge Check
### Exercise: Take the Knowledge Check

[Take the Week 2 knowledge check](knowledge-check.md): covers GPU anatomy + memory hierarchy + bottleneck classification. Questions drawn from Flashcards Days 6–9.

**Passing score:** 10/15 (67%)

If you score below 10/15:
- Review the questions you got wrong
- Go back to the relevant day's content
- Re-read that section
- Retake the quiz

---

## Part 2 - Self-Assessment
### Self-Check List

Go through each item and mark whether you can explain it **without notes**:

- [ ] The inference pipeline: tokenize → embed → layers → logits → sample
- [ ] Prefill vs decode: what's compute-bound vs memory-bound
- [ ] GPU anatomy: SMs, Tensor Cores, L1/L2/HBM
- [ ] The key H100 numbers: 80 GB, 3.35 TB/s, 132 SMs, 528 Tensor Cores
- [ ] The memory hierarchy from fast to slow
- [ ] Arithmetic intensity formula: FLOPs / bytes
- [ ] The roofline model and ridge point
- [ ] Why decode is ~99% memory-bound (only ~0.7% Tensor Core utilization)

### The Key Insight

By Friday you can answer: *"Why is most LLM inference time spent moving data, not computing?"* That single insight unlocks Weeks 3–5.

---

## Part 3 - Practice - Pipeline Review
### Hands-On: Trace the Prompt

Draw from memory the inference pipeline and annotate each step:

```
text → [tokenize] → token IDs → [embed] → vectors → [layers] → hidden states → [LM head] → logits → [sample] → next token
```

Then answer:

1. Which step is compute-bound? (Answer: layers / prefill)
2. Which step is memory-bound? (Answer: decode / sampling)
3. What's driving TTFT? (Answer: prefill)
4. What's driving TPS? (Answer: decode)

---

## Part 4 - Practice - GPU & Memory Review
### Hands-On: Quick Calculations

Practice these calculations until they're automatic:

**1. Time to read 16 GB from H100:**
- 16 GB ÷ 3.35 TB/s = ~4.8 ms

**2. Arithmetic intensity for decode:**
- ~2 ops/byte (way below ridge of ~295)

**3. Tensor Core utilization during decode:**
- 2 / 295 = ~0.68%

**4. Ridge point for RTX 4090:**
- 165 TFLOPs ÷ 1 TB/s = ~165 ops/byte

### Memory Hierarchy Quiz

Fill in from memory:

| Level | Approximate Speed |
|-------|-------------------|
| Registers | ___ ns |
| L1 / Shared | ~___ ns |
| L2 | ~___ ns |
| HBM | ~___ ns |

---

## Part 5 - Feynman Teach-Back
### Exercise: Explain to a Peer

Choose one concept from the list and explain it as if to a peer who missed the week:

1. **Bandwidth** - Why does moving data matter more than compute for LLM inference?
2. **FLOPs** - What's the difference between peak TFLOPs and utilized FLOPs?
3. **Roofline** - How do you know if a workload is compute-bound or memory-bound?
4. **Memory hierarchy** - Why is there a pyramid of memory types?

### Structure Your Explanation

1. **Start with a simple analogy** (factory floor, warehouse, etc.)
2. **Give one concrete number** (e.g., "H100 has 80 GB of HBM3")
3. **State the key insight** (e.g., "decode is memory-bound because...")
4. **Explain the implication** (e.g., "this is why batching helps...")

---

## Part 7 - Wrap-up & Connection
### What to Do

This is open time. Choose what you need:

1. **Catch up** on any assignments from Days 6–9
2. **Ask questions** - use oxtutor or review the relevant day
3. **Extra practice** - generate more exercises on any concept
4. **Preview Week 3** - start the pre-reading for Day 11

### Connect Forward

Week 3 begins on Monday. You'll learn about:
- Prefill and decode phases in detail
- KV cache
- FlashAttention and PagedAttention
- Quantization

### Pre-read for Monday (Week 3, Day 11)

**Resource:** <a href="https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices" target="_blank" rel="noopener">Databricks - LLM Inference Performance Engineering Best Practices</a> (read the prefill/decode section). Alternative: <a href="https://www.baseten.co/blog/llm-transformer-inference-guide/" target="_blank" rel="noopener">Baseten - Prefill vs Decode</a>.

**Reflection questions:**

1. What is the KV cache?
2. Why does attention have O(N²) complexity?
3. What does FlashAttention optimize?

---

## Stuck?

Ask **oxtutor** to re-explain any concept; the glossary entries on *bandwidth*, *FLOPs*, *roofline*, and *memory hierarchy* are the canonical definitions.