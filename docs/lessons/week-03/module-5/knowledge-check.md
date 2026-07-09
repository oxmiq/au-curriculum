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

**Week 3 · KV Cache, Attention, Quantization.** 15 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
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
    "explain": "Tile in SRAM + online softmax → HBM traffic drops from O(N²) to O(N). Same answer."
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
    "stem": "True/false: prefill of 1000 tokens generates 1000 output tokens.",
    "options": [
      "True",
      "False — prefill processes the prompt and produces just the first output token"
    ],
    "answer": 1,
    "explain": "Prefill = parallel forward pass over the prompt, ending with one output token. Decode loops thereafter."
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
