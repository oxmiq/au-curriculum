<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 3 — Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <a href="../">Day 15 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-03/module-5}
  </div>
</div>

# Week 3 Knowledge Check

**Week 3 · KV Cache, Attention, Quantization.** 29-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 3 · KV Cache, Attention, Quantization" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "TTFT (Time To First Token) is most directly driven by:",
    "options": [
      "Decode speed",
      "Prefill speed",
      "Tokenization",
      "Network round-trip"
    ],
    "answer": 1,
    "explain": "Prefill processes all input tokens to produce the first output token; that's what the user sees first."
  },
  {
    "stem": "Decode for a single user is bottlenecked by:",
    "options": [
      "Tensor Core throughput",
      "HBM bandwidth",
      "CPU",
      "Network"
    ],
    "answer": 1,
    "explain": "Memory-bound — each token re-reads all model weights from HBM."
  },
  {
    "stem": "The KV cache stores:",
    "options": [
      "Final output logits",
      "Keys and values from prior tokens, per layer",
      "Activations from prior layers",
      "Embedding table"
    ],
    "answer": 1,
    "explain": "Each layer caches the K,V tensors it computed for every previously seen token."
  },
  {
    "stem": "Llama-3.1-8B with 8 KV heads, head_dim 128, 32 layers, FP16: KV cache per token is roughly:",
    "options": [
      "4 KB",
      "128 KB",
      "1 MB",
      "16 MB"
    ],
    "answer": 1,
    "explain": "Per-layer: 2 × 8 × 128 × 2 = 4 KB. Times 32 layers = 128 KB per token."
  },
  {
    "stem": "At what context length does Llama-3-8B's KV cache approximately equal the model weight memory (16 GB)?",
    "options": [
      "4K",
      "32K",
      "128K",
      "1M"
    ],
    "answer": 2,
    "explain": "128 KB/token × 131072 tokens = 16 GB — matches model size."
  },
  {
    "stem": "FlashAttention's speedup comes from:",
    "options": [
      "Lower-precision math",
      "Avoiding materializing the N×N attention matrix in HBM",
      "Skipping softmax",
      "Approximate attention"
    ],
    "answer": 1,
    "explain": "Tile in SRAM + online softmax → HBM traffic drops from O(N²) to O(N). The math is unchanged; only the memory schedule differs."
  },
  {
    "stem": "Is FlashAttention lossy?",
    "options": [
      "Yes, slightly",
      "No — bit-identical output",
      "Only for long context",
      "Only with FP8"
    ],
    "answer": 1,
    "explain": "Pure systems trick. Same softmax, same precision, same numbers."
  },
  {
    "stem": "PagedAttention is most analogous to:",
    "options": [
      "CPU branch prediction",
      "OS virtual memory paging",
      "TCP windowing",
      "GPU shared memory"
    ],
    "answer": 1,
    "explain": "KV cache blocks + per-request page table = OS-style virtual addressing for the cache."
  },
  {
    "stem": "PagedAttention primarily attacks:",
    "options": [
      "Per-token compute cost",
      "KV-cache memory fragmentation",
      "Network latency",
      "Tokenization overhead"
    ],
    "answer": 1,
    "explain": "Eliminates worst-case contiguous reservations → much higher HBM utilization → more concurrent users."
  },
  {
    "stem": "FP8 weights vs FP16 weights, on a memory-bound decode workload, gives roughly:",
    "options": [
      "No speedup",
      "~2× speedup",
      "~10× speedup",
      "Slower (more overhead)"
    ],
    "answer": 1,
    "explain": "Half the bytes per token → roughly halves the HBM-bound time."
  },
  {
    "stem": "At the same bit count, FP8 is usually preferred over INT8 for LLM weights because:",
    "options": [
      "FP8 is faster on all hardware",
      "Floats handle outlier values better than ints",
      "INT8 isn't supported on H100",
      "FP8 uses less memory"
    ],
    "answer": 1,
    "explain": "Float spreads precision across magnitudes; activations are heavy-tailed, ints clip or waste range."
  },
  {
    "stem": "Which of these is most sensitive to quantization (degrades quality first)?",
    "options": [
      "Model weights",
      "KV cache",
      "Activations / attention output",
      "All equally"
    ],
    "answer": 2,
    "explain": "Order of sensitivity: weights (least) → KV → activations → attention output (most)."
  },
  {
    "stem": "Combining FlashAttention + PagedAttention + FP8 weights gives you:",
    "options": [
      "Lower-quality model",
      "Same model, much higher throughput at long context",
      "A different model architecture",
      "A new training method"
    ],
    "answer": 1,
    "explain": "All three are inference-time wins; the model itself is unchanged (FlashAttention/PagedAttention) or numerically close (FP8)."
  },
  {
    "stem": "How many output tokens does the prefill phase itself produce for a 1000-token prompt?",
    "options": [
      "1000 — one per input token",
      "Just the first output token; decode then generates the rest",
      "Zero — prefill only builds the KV cache",
      "500 — half the prompt length"
    ],
    "answer": 1,
    "explain": "Prefill is a single parallel forward pass over the whole prompt that produces the first output token plus the initial KV cache. Decode loops one token at a time thereafter — prompt length does not equal output length."
  },
  {
    "stem": "Why is the KV cache the resource that defines a modern serving stack?",
    "options": [
      "It's the only thing on the GPU",
      "It grows with context, can exceed model weights, and competes with batch size for HBM",
      "It runs on CPU",
      "It is required only at training time"
    ],
    "answer": 1,
    "explain": "Every modern trick — paging, prefix sharing, FP8 KV, disaggregation — is about KV-cache management."
  },
  {
    "stem": "Decode throughput improves far more from batching than from a faster single-stream GPU because:",
    "options": [
      "Batching reduces the number of model layers that must be read",
      "Batching automatically lowers the precision of the weights",
      "Batching amortizes each HBM weight read across many sequences, raising arithmetic intensity",
      "Batching converts decode into a compute-bound prefill"
    ],
    "answer": 2,
    "explain": "Decode is memory-bound: one token does little compute but still reads all weights from HBM. Running many sequences together reuses each weight read across the batch, so effective ops/byte climbs and the GPU stops idling — the key to decode throughput."
  },
  {
    "stem": "End-to-end latency for a request is computed as:",
    "options": [
      "TTFT ÷ number of output tokens",
      "The prefill time alone, since decode overlaps it",
      "TTFT + (number of output tokens × ITL)",
      "The decode time alone, since prefill is negligible"
    ],
    "answer": 2,
    "explain": "From the Day 11 timeline: TTFT (driven by prefill) is the wait for the first token, then each remaining output token adds one inter-token latency (ITL, driven by decode). Total = TTFT + tokens × ITL."
  },
  {
    "stem": "Which arithmetic-intensity figures match the two inference phases?",
    "options": [
      "Prefill ~2 ops/byte; decode hundreds of ops/byte",
      "Prefill hundreds of ops/byte; decode ~2 ops/byte",
      "Both run near the H100 ridge of ~295 ops/byte",
      "Both run at ~2 ops/byte"
    ],
    "answer": 1,
    "explain": "Prefill processes all tokens in parallel with high arithmetic intensity (hundreds of ops/byte), saturating Tensor Cores — compute-bound. Decode does ~2 ops/byte, far below the H100 ridge (~295), so the GPU idles on HBM reads — memory-bound."
  },
  {
    "stem": "The KV-cache size formula uses num_kv_heads × head_dim rather than hidden_size because:",
    "options": [
      "hidden_size is only defined during training",
      "the two quantities are always equal",
      "head_dim is unknown at inference time",
      "GQA/MQA share K and V across query heads, so the cache scales with the number of KV heads, not the full hidden width"
    ],
    "answer": 3,
    "explain": "KV bytes = 2 × L × num_kv_heads × head_dim × seq_len × bytes_per_element. Using num_kv_heads (not hidden_size) is exactly what lets GQA/MQA shrink the cache — Llama-3.1-8B has 8 KV heads vs 32 query heads, a 4× reduction versus full multi-head attention."
  },
  {
    "stem": "Llama-3 uses 8 KV heads with 32 query heads. Versus full multi-head attention, this makes its KV cache:",
    "options": [
      "4× smaller",
      "4× larger",
      "unchanged — GQA only affects query heads",
      "32× smaller"
    ],
    "answer": 0,
    "explain": "GQA groups the 32 query heads to share 8 KV heads, so num_kv_heads drops from 32 to 8 in the size formula — a 4× smaller KV cache than full MHA while keeping all 32 query heads."
  },
  {
    "stem": "Storing the KV cache in FP8 instead of FP16 for Llama-3.1-8B at 128K context changes its size from:",
    "options": [
      "16 GB to 32 GB",
      "16 GB to 8 GB",
      "8 GB to 16 GB",
      "no change — precision does not affect cache size"
    ],
    "answer": 1,
    "explain": "FP8 halves bytes_per_element (2 → 1), so the 128K KV cache drops from 16 GB to 8 GB. Then 8 GB KV + 16 GB weights = 24 GB, leaving 56 GB of an 80 GB H100 free for batching."
  },
  {
    "stem": "The core inefficiency of naive attention is that it:",
    "options": [
      "materializes the full N×N attention-score matrix in HBM, causing O(N²) memory traffic",
      "recomputes the model weights for every token",
      "runs the softmax on the CPU",
      "stores the KV cache in FP32"
    ],
    "answer": 0,
    "explain": "Naive attention writes and re-reads the full N×N score matrix (QKᵀ, softmax, ×V) to and from HBM — O(N²) traffic. At N=32K with 32 heads that is tens of billions of elements, so the GPU sits far below its roofline waiting on memory."
  },
  {
    "stem": "FlashAttention avoids writing the N×N matrix to HBM by:",
    "options": [
      "approximating attention and dropping small scores",
      "tiling Q, K, V into SRAM-sized blocks and combining them with an online (incremental) softmax",
      "caching the attention matrix across requests to avoid recomputation",
      "shortening the sequence with token merging before attention"
    ],
    "answer": 1,
    "explain": "FlashAttention loads Q/K/V tiles into fast on-chip SRAM and accumulates a numerically stable online softmax (running max + denominator) block by block. Only the O(N)-sized output touches HBM, so the full N×N matrix is never materialized — and the result is bit-identical to naive attention."
  },
  {
    "stem": "In PagedAttention, KV cache is split into fixed-size blocks (typically ~16 tokens) that are located via:",
    "options": [
      "a single contiguous buffer reserved per request",
      "the model weights",
      "the tokenizer's vocabulary table",
      "a per-request block table mapping logical positions to physical blocks allocated on demand"
    ],
    "answer": 3,
    "explain": "Exactly like an OS pages physical RAM: each request has a block table mapping logical token positions to physical KV blocks, with new blocks allocated on demand. This removes the need for one big contiguous per-request reservation."
  },
  {
    "stem": "PagedAttention's effect on KV-cache HBM utilization is roughly:",
    "options": [
      "it drops utilization from ~90% down to ~20%",
      "it raises utilization from ~20% to ~90%+, and makes prefix sharing across requests nearly free",
      "it fixes utilization at exactly 100%",
      "it has no effect on utilization"
    ],
    "answer": 1,
    "explain": "By eliminating worst-case contiguous reservations, paging lifts KV-cache HBM utilization from ~20% to ~90%+ (2–4× more long-context throughput). Because blocks are referenced through block tables, a shared system prompt's blocks can be pointed to by many requests — so prefix caching costs nothing extra."
  },
  {
    "stem": "Per the precision ladder, how many bytes per parameter do INT4 and FP4/NF4 use, and how does that compare with FP16?",
    "options": [
      "0.5 bytes each; 4× smaller than FP16",
      "1 byte each; 2× smaller than FP16",
      "2 bytes each; the same as FP16",
      "0.25 bytes each; 8× smaller than FP16"
    ],
    "answer": 0,
    "explain": "The precision table lists INT4 and FP4/NF4 at 0.5 bytes/param versus FP16's 2 bytes — a 4× reduction. Llama-3-8B is 16 GB at FP16 but only 4 GB at INT4."
  },
  {
    "stem": "The lesson's recommended 'modern Hopper sweet spot' starter quantization config is:",
    "options": [
      "INT4 weights, INT4 activations, INT4 KV cache",
      "FP32 for every component, for maximum safety",
      "FP8 weights, FP16 activations, FP8 KV cache",
      "FP16 weights, FP8 activations, FP16 KV cache"
    ],
    "answer": 2,
    "explain": "This follows the sensitivity ladder: weights are least sensitive so quantize aggressively (FP8); KV tolerates FP8 (halving both its size and read bandwidth); activations are kept in higher precision (FP16) because they are more sensitive."
  },
  {
    "stem": "Well-calibrated FP8 quantization typically costs about how much on MMLU versus FP16?",
    "options": [
      "greater than 10 points — noticeable degradation",
      "around 5 points",
      "about 0.1–0.3 points — negligible for roughly 2× throughput",
      "exactly zero — perfectly lossless for every model"
    ],
    "answer": 2,
    "explain": "Modern LLMs lose only ~0.1–0.3 MMLU points at FP8 for roughly 2× (memory) throughput — a strong trade. It is not truly lossless, and some architectures are more sensitive, so you always measure quality before deploying."
  },
  {
    "stem": "In the quantization sensitivity ladder, ordering components from LEAST to MOST sensitive gives:",
    "options": [
      "attention output < activations < KV cache < weights",
      "weights < KV cache < activations < attention output",
      "KV cache < weights < attention output < activations",
      "all components are equally sensitive"
    ],
    "answer": 1,
    "explain": "Least to most sensitive: weights < KV cache < activations < attention output. Weights are static and calibrate well; KV tolerates FP8; activations and attention outputs are dynamic and outlier-prone, so errors there accumulate over thousands of tokens."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 15 · Consolidation](index.md)

-   __Back to the week__

    [Week 3 — Attention &amp; KV Cache overview](../index.md)

-   __Continue the curriculum__

    [Day 16 · Multi-GPU Parallelism](../../week-04/module-1/index.md)

</div>
