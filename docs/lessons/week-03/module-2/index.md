# Day 12 · The KV Cache

> **Concept of the day:** KV cache = stored keys and values from all prior tokens. Grows linearly with context. **Can exceed model weight memory** at long contexts.
> **Pre-reading:** "KV cache explained" blog with diagrams — Pre-Lecture Reading **Reader 4** + Study Guide §A.2 (~20 min).
> **Source:** [Study Guide §A.2](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Study_Guide.md) · [Flashcards — KV cache cards](../../../../planning/source-material/Inference%20Engineering/Inference_Engineering_Flashcards.md).

---

## Why this matters

The KV cache is the *single resource* whose management defines a modern serving stack. PagedAttention, prefix caching, disaggregation, long-context tricks — they are all about getting more out of less KV-cache memory.

## Readiness check

1. What grows every time the model generates a token?
2. Where in the transformer is the KV cache *used* — attention, MLP, both?
3. Per token, how much KV-cache memory does a layer add? (Rough formula.)
4. For Llama-3-8B at 32K context, does the KV cache exceed the model weights? (We'll calculate today.)
5. Why does the cache exist at all — what would happen without it?

## Core concept

### Why the cache exists

Without a cache, generating output token *t* would require re-running attention over *all t–1* previously seen tokens. That's O(t²) cumulative work for *t* output tokens.

The KV cache stores the **K** (keys) and **V** (values) tensors that each layer computed for every token already in the sequence. Generating token *t* only needs to:

1. Compute new K, V for the *one* new token.
2. Attend over the *cached* K, V for all previous tokens.

That turns decode into O(t) per token — and is the **only** reason single-user generation is feasible.

### KV cache size formula

For one token, one layer:

> **bytes = 2 × num_kv_heads × head_dim × bytes_per_element**

For the whole sequence:

> **KV bytes = 2 × L × num_kv_heads × head_dim × seq_len × bytes_per_element**

where L = layers. The "2" is for K and V.

### Worked examples — Llama-3.1-8B (FP16)

Llama-3.1-8B uses **GQA** with 8 KV heads, head_dim 128, 32 layers, 2 bytes (FP16).

> Per-token, per-layer = 2 × 8 × 128 × 2 = 4096 bytes = **4 KB**
> Per-token, full model = 4 KB × 32 layers = **128 KB**

| Context | KV cache size | Vs 16 GB model weights |
|---|---|---|
| 4K | 128 KB × 4096 = 512 MB | 3.1% |
| 32K | 128 KB × 32,768 = **4 GB** | 25% |
| 128K | 128 KB × 131,072 = **16 GB** | **100% — matches model size** |

> **At 128K context with batch = 1, the KV cache is as big as the model itself.** With any meaningful batch, it dwarfs the model.

### Why MQA / GQA exist

Multi-Query Attention and Grouped-Query Attention shrink the KV cache by reducing `num_kv_heads`. Llama-3 uses GQA with 8 KV heads vs 32 query heads → 4× smaller KV cache than full MHA.

### Connect to roofline

- KV cache **doesn't change compute intensity much** — it shifts where bytes are read from.
- It **does** consume HBM bandwidth (you re-read all K, V per attention step).
- And it **takes HBM capacity away from batch size** — which is what kills throughput on long-context workloads.

## Practice (90 min)

1. (20 min) Calculate KV cache size for Llama-3.1-8B at 4K, 32K, and 128K context. At 80 GB H100, what's the max batch size at each context length (after subtracting 16 GB model weights)?
2. (20 min) Recalculate for a 70B model (assume 64 KV heads, head_dim 128, 80 layers, GQA). What context length saturates a single H100?
3. (20 min) Pair work: explain *in your own words* why removing the KV cache would make a 4-token reply take ~16 forward passes' worth of compute instead of 5.
4. (20 min) Quantization preview: if K and V are stored in FP8 (1 byte) instead of FP16 (2 bytes), redo the 128K calculation for 8B. Does the cache now fit alongside the model? (Day 14 connects this back.)
5. (10 min) Write one sentence: *"The KV cache is the resource that…"*

## Wrap-up

Cohort answers: **what's the structural reason long-context serving is hard?** Right answer: KV cache scales linearly with context, blows past model weights, eats HBM that batching needs.

## Connect forward

Tomorrow: how **FlashAttention** rearranges the attention math to use HBM less, and how **PagedAttention** treats KV cache like an OS paging system — both are direct attacks on today's problem.

---

## Pre-read for tomorrow (Day 13 · FlashAttention & PagedAttention)

- **Resource:** FlashAttention blog summary + paper abstract — Pre-Lecture Reading **Reader 4** (FlashAttention section) (~20 min).
- **Reflection questions:**
  1. Why is naive attention slow? Think about memory reads.
  2. What does "lossless" mean about FlashAttention?
  3. What does **PagedAttention** borrow from operating-system design?
