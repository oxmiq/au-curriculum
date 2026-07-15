# Day 12 · The KV Cache

> **Concept of the day:** KV cache = stored keys and values from all prior tokens. Grows linearly with context. **Can exceed model weight memory** at long contexts.<br>
> **Pre-reading:** "KV cache explained" blog with diagrams: <a href="https://medium.com/@joaolages/kv-caching-explained-276520203249" target="_blank" rel="noopener">João Lages - KV Caching Explained</a>.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 3 - Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <span>Day 12 · KV Cache</span>
    {status:week-03/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

This lesson is designed for guided self-study. Here's how your ~3 hours is organized:

| Part | What you do |
|-------------|---------------|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Why KV Cache Exists |
| Part 3 | Deep Dive: KV Cache Size Formula |
| Part 4 | Hands-On: Calculate KV Cache Size |
| Part 5 | Hands-On: GQA Impact |
| Part 6 | Wrap-up & Connection |

---

## Part 1 - Pre-Reading Review
### Before You Start

You should have already read: "KV cache explained" blog with diagrams: Pre-Lecture Reading **Reader 4** + Study Guide §A.2.

### Quick Self-Check

Answer these questions from memory:

1. What grows every time the model generates a token?
2. Where in the transformer is the KV cache used?
3. For a 70B model at 128K context, can the KV cache exceed the size of the model weights?

### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m2-readiness" data-kind="readiness" data-draw="5" data-source="João Lages - KV Caching Explained">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does the KV cache store?", "options": ["The model's weights", "The key and value matrices from attention for all previously processed tokens", "The user's prompt", "The final output tokens"]},
  {"stem": "Why does the KV cache grow linearly with context length?", "options": ["Because the model weights grow", "Because every new token needs to attend to all previous tokens, requiring their K and V values", "Because the cache stores complete copies of the model", "Because of compression algorithms"]},
  {"stem": "In the transformer architecture, where does the KV cache get used?", "options": ["In the feedforward networks", "In the attention mechanism", "In the embedding layer", "In the tokenizer"]},
  {"stem": "For a 70B model at 128K context, can the KV cache exceed the size of the model weights?", "options": ["No: KV cache is always smaller than model weights", "Yes: at long contexts, KV cache can exceed model weight memory", "Only for small models", "Only with quantization"]},
  {"stem": "What is the primary benefit of KV caching?", "options": ["Reduces model size", "Avoids recomputing K and V for previous tokens during decode, massively reducing compute", "Improves model accuracy", "Enables model parallelism"]},
  {"stem": "What would happen if you didn't use KV caching during inference?", "options": ["The model would generate faster", "Every token generation would require recomputing keys and values for all previous tokens, making it impossibly slow", "The model would use less memory", "Nothing would change"]},
  {"stem": "What is GQA (Grouped-Query Attention) and how does it affect KV cache size?", "options": ["GQA increases KV cache size", "GQA reduces KV cache size by sharing K and V heads across multiple query heads", "GQA eliminates the need for KV cache", "GQA has no effect on KV cache size"]},
  {"stem": "What is the relationship between sequence length and KV cache memory usage?", "options": ["KV cache is constant regardless of sequence length", "KV cache is proportional to sequence length", "KV cache is proportional to sequence length squared", "KV cache is inversely proportional to sequence length"]}
]
</script>
</div>

---

## Part 2 - Core Concepts - Why KV Cache Exists
### Reading - The Problem Without Cache

Without a cache, generating output token *t* would require re-running attention over *all t–1* previously seen tokens. That's O(t²) cumulative work for *t* output tokens.

### The Solution: KV Cache

The KV cache stores the **K** (keys) and **V** (values) tensors that each layer computed for every token already in the sequence. Generating token *t* only needs to:

1. **Compute** new K, V for the *one* new token
2. **Attend** over the *cached* K, V for all previous tokens

> **That turns decode into O(t) per token: and is the only reason single-user generation is feasible.**

### Why This Matters

Without KV cache:
- 4-token reply would need ~16 forward passes worth of compute
- With KV cache: only ~5 forward passes (1 prefill + 4 decode)

---

## Part 3 - Deep Dive - KV Cache Size Formula
### Reading - The Math

For one token, one layer:

> **bytes = 2 × num_kv_heads × head_dim × bytes_per_element**

For the whole sequence:

> **KV bytes = 2 × L × num_kv_heads × head_dim × seq_len × bytes_per_element**

Where:
- L = number of layers
- 2 = for K and V
- seq_len = context length

### Worked Example - Llama-3.1-8B (FP16)

Llama-3.1-8B uses **GQA** with 8 KV heads, head_dim 128, 32 layers, 2 bytes (FP16):

| Calculation | Value |
|-------------|-------|
| Per-token, per-layer | 2 × 8 × 128 × 2 = **4 KB** |
| Per-token, full model | 4 KB × 32 layers = **128 KB** |

### Context Size Comparison

| Context | KV Cache Size | Vs 16 GB Model Weights |
|---------|---------------|------------------------|
| 4K | 128 KB × 4096 = 512 MB | 3.1% |
| 32K | 128 KB × 32,768 = **4 GB** | 25% |
| 128K | 128 KB × 131,072 = **16 GB** | **100%** |

> **At 128K context with batch = 1, the KV cache is as big as the model itself.** With any meaningful batch, it dwarfs the model.

---

## Part 4 - Hands-On - Calculate KV Cache Size
### Exercise 1: Llama-3.1-8B at Different Contexts

Calculate KV cache size for Llama-3.1-8B at:
- 4K context
- 32K context  
- 128K context

Then calculate: At 80 GB H100, what's the max batch size at each context length (after subtracting 16 GB model weights)?

**Answers:**
- 4K: 512 MB → max batch ~80 (before weights)
- 32K: 4 GB → max batch ~19
- 128K: 16 GB → max batch ~4 (if just model + KV, no room for computation)

### Exercise 2: 70B Model

Recalculate for a 70B model with:
- 64 KV heads
- head_dim 128
- 80 layers
- GQA

At 80 GB H100, what context length saturates a single H100?

---

## Part 5 - Hands-On - GQA Impact
### Reading - Why MQA / GQA Exist

Multi-Query Attention and Grouped-Query Attention shrink the KV cache by reducing `num_kv_heads`.

Llama-3 uses GQA with 8 KV heads vs 32 query heads → **4× smaller KV cache** than full MHA.

### Exercise: Quantization Preview

If K and V are stored in FP8 (1 byte) instead of FP16 (2 bytes), redo the 128K calculation for 8B:

- Per-token: 2 × 8 × 128 × 1 = 2 KB
- Per-model: 2 KB × 32 = 64 KB
- At 128K: 64 KB × 131,072 = **8 GB**

**Question:** Does the cache now fit alongside the model?

**Answer:** Yes! 8 GB KV + 16 GB weights = 24 GB (leaves 56 GB for batching)

---

## Part 7 - Wrap-up & Connection
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 12 · The KV Cache">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "Why does the KV cache exist?", "options": ["To compress model weights during inference", "To store key and value matrices from attention so they don't need to be recomputed for every generated token", "To cache the final output text for repeated queries", "To prefetch the next batch of requests"]},
  {"stem": "What grows with every new token generated during decode?", "options": ["The model weights", "The KV cache: one new key and one new value vector is added per attention layer per token", "The embedding matrix", "The logit vocabulary distribution"]},
  {"stem": "Which of the following correctly expresses the KV cache size formula?", "options": ["2 × num_layers × num_kv_heads × head_dim × seq_len × bytes_per_element", "num_layers × hidden_size × vocab_size × bytes_per_element", "seq_len × vocab_size × bytes_per_element", "2 × hidden_size × batch_size × bytes_per_element"]},
  {"stem": "Why does serving long-context requests push against HBM limits?", "options": ["Long contexts increase the model weight size proportionally", "KV cache size scales linearly with sequence length: at 128K it equals the weights at batch=1 and exceeds them at batch>1, consuming most of HBM", "Long contexts require FP32 precision instead of FP16", "HBM bandwidth decreases as more data is stored in it"]},
  {"stem": "What is the direct impact of a large KV cache on serving throughput?", "options": ["It increases TTFT because prefill must be redone for each new request", "It reduces the HBM available for batching: fewer concurrent requests fit in memory, reducing throughput", "It forces the model to use lower precision to compensate", "It reduces decode speed by increasing the L2 cache miss rate"]},
  {"stem": "What is the 'Key Insight' about KV cache growth stated at the end of Part 7?", "options": ["KV cache growth is bounded by model parameter count", "KV cache scales linearly with context, blows past model weights, and eats HBM that batching needs", "KV cache only grows during prefill, not during decode", "KV cache growth is eliminated by using FlashAttention"]},
  {"stem": "In the Part 3 worked example (Llama-3.1-8B, FP16, 8 KV heads, head_dim 128, 32 layers), how large is the KV cache per token for the whole model?", "options": ["4 KB", "128 KB", "16 GB", "512 MB"]},
  {"stem": "By how much does Llama-3's GQA shrink the KV cache relative to full multi-head attention, and why?", "options": ["No change: GQA only affects the query heads", "2× smaller, by halving head_dim", "4× smaller, because 8 KV heads are shared across 32 query heads instead of one KV head per query head", "32× smaller, by collapsing to a single KV head"]},
  {"stem": "The lesson stores K and V in FP8 (1 byte) instead of FP16 for the 8B model at 128K context. What is the effect?", "options": ["It doubles the cache to 32 GB", "It halves the cache from 16 GB to 8 GB, so it fits alongside the 16 GB weights", "It has no effect: precision does not change cache size", "It quadruples throughput but leaves cache size unchanged"]}
]
</script>
</div>

### The Key Insight

> **KV cache scales linearly with context, blows past model weights, eats HBM that batching needs.**

### Connect Forward

Tomorrow: how **FlashAttention** rearranges the attention math to use HBM less, and how **PagedAttention** treats KV cache like an OS paging system: both are direct attacks on today's problem.

### Pre-read for tomorrow (Day 13 · FlashAttention & PagedAttention)

- **Resource:** <a href="https://gordicaleksa.medium.com/eli5-flash-attention-5c44017022ad" target="_blank" rel="noopener">Aleksa Gordić - ELI5 FlashAttention</a> + <a href="https://blog.vllm.ai/2023/06/20/vllm.html" target="_blank" rel="noopener">vLLM - PagedAttention blog</a>.
- **Reflection questions:**
  1. Why is naive attention slow? Think about memory reads.
  2. What does "lossless" mean about FlashAttention?
  3. What does **PagedAttention** borrow from operating-system design?

---

## Stuck?

Ask **oxtutor**: share your exact question, the concept or command that isn't
clicking, and which week/module you are on.
