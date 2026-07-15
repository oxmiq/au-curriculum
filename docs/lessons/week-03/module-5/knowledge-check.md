<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 3 - Attention &amp; KV Cache</a>
    <span class="sep">/</span>
    <a href="../">Day 15 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-03/module-5}
  </div>
</div>

# Week 3 Knowledge Check

**Week 3 · KV Cache, Attention, Quantization.** 29-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative, it never blocks you, but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-03-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 3 · KV Cache, Attention, Quantization" data-source="Canonical knowledge check">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "TTFT (Time To First Token) is most directly driven by:", "options": ["Decode speed", "Prefill speed", "Tokenization", "Network round-trip"]},
  {"stem": "Decode for a single user is bottlenecked by:", "options": ["Tensor Core throughput", "HBM bandwidth", "CPU", "Network"]},
  {"stem": "The KV cache stores:", "options": ["Final output logits", "Keys and values from prior tokens, per layer", "Activations from prior layers", "Embedding table"]},
  {"stem": "Llama-3.1-8B with 8 KV heads, head_dim 128, 32 layers, FP16: KV cache per token is roughly:", "options": ["4 KB", "128 KB", "1 MB", "16 MB"]},
  {"stem": "At what context length does Llama-3-8B's KV cache approximately equal the model weight memory (16 GB)?", "options": ["4K", "32K", "128K", "1M"]},
  {"stem": "FlashAttention's speedup comes from:", "options": ["Lower-precision math", "Avoiding materializing the N×N attention matrix in HBM", "Skipping softmax", "Approximate attention"]},
  {"stem": "Is FlashAttention lossy?", "options": ["Yes, slightly", "No - bit-identical output", "Only for long context", "Only with FP8"]},
  {"stem": "PagedAttention is most analogous to:", "options": ["CPU branch prediction", "OS virtual memory paging", "TCP windowing", "GPU shared memory"]},
  {"stem": "PagedAttention primarily attacks:", "options": ["Per-token compute cost", "KV-cache memory fragmentation", "Network latency", "Tokenization overhead"]},
  {"stem": "FP8 weights vs FP16 weights, on a memory-bound decode workload, gives roughly:", "options": ["No speedup", "~2× speedup", "~10× speedup", "Slower (more overhead)"]},
  {"stem": "At the same bit count, FP8 is usually preferred over INT8 for LLM weights because:", "options": ["FP8 is faster on all hardware", "Floats handle outlier values better than ints", "INT8 isn't supported on H100", "FP8 uses less memory"]},
  {"stem": "Which of these is most sensitive to quantization (degrades quality first)?", "options": ["Model weights", "KV cache", "Activations / attention output", "All equally"]},
  {"stem": "Combining FlashAttention + PagedAttention + FP8 weights gives you:", "options": ["Lower-quality model", "Same model, much higher throughput at long context", "A different model architecture", "A new training method"]},
  {"stem": "How many output tokens does the prefill phase itself produce for a 1000-token prompt?", "options": ["1000 - one per input token", "Just the first output token; decode then generates the rest", "Zero - prefill only builds the KV cache", "500 - half the prompt length"]},
  {"stem": "Why is the KV cache the resource that defines a modern serving stack?", "options": ["It's the only thing on the GPU", "It grows with context, can exceed model weights, and competes with batch size for HBM", "It runs on CPU", "It is required only at training time"]},
  {"stem": "Decode throughput improves far more from batching than from a faster single-stream GPU because:", "options": ["Batching reduces the number of model layers that must be read", "Batching automatically lowers the precision of the weights", "Batching amortizes each HBM weight read across many sequences, raising arithmetic intensity", "Batching converts decode into a compute-bound prefill"]},
  {"stem": "End-to-end latency for a request is computed as:", "options": ["TTFT ÷ number of output tokens", "The prefill time alone, since decode overlaps it", "TTFT + (number of output tokens × ITL)", "The decode time alone, since prefill is negligible"]},
  {"stem": "Which arithmetic-intensity figures match the two inference phases?", "options": ["Prefill ~2 ops/byte; decode hundreds of ops/byte", "Prefill hundreds of ops/byte; decode ~2 ops/byte", "Both run near the H100 ridge of ~295 ops/byte", "Both run at ~2 ops/byte"]},
  {"stem": "The KV-cache size formula uses num_kv_heads × head_dim rather than hidden_size because:", "options": ["hidden_size is only defined during training", "the two quantities are always equal", "head_dim is unknown at inference time", "GQA/MQA share K and V across query heads, so the cache scales with the number of KV heads, not the full hidden width"]},
  {"stem": "Llama-3 uses 8 KV heads with 32 query heads. Versus full multi-head attention, this makes its KV cache:", "options": ["4× smaller", "4× larger", "unchanged - GQA only affects query heads", "32× smaller"]},
  {"stem": "Storing the KV cache in FP8 instead of FP16 for Llama-3.1-8B at 128K context changes its size from:", "options": ["16 GB to 32 GB", "16 GB to 8 GB", "8 GB to 16 GB", "no change - precision does not affect cache size"]},
  {"stem": "The core inefficiency of naive attention is that it:", "options": ["materializes the full N×N attention-score matrix in HBM, causing O(N²) memory traffic", "recomputes the model weights for every token", "runs the softmax on the CPU", "stores the KV cache in FP32"]},
  {"stem": "FlashAttention avoids writing the N×N matrix to HBM by:", "options": ["approximating attention and dropping small scores", "tiling Q, K, V into SRAM-sized blocks and combining them with an online (incremental) softmax", "caching the attention matrix across requests to avoid recomputation", "shortening the sequence with token merging before attention"]},
  {"stem": "In PagedAttention, KV cache is split into fixed-size blocks (typically ~16 tokens) that are located via:", "options": ["a single contiguous buffer reserved per request", "the model weights", "the tokenizer's vocabulary table", "a per-request block table mapping logical positions to physical blocks allocated on demand"]},
  {"stem": "PagedAttention's effect on KV-cache HBM utilization is roughly:", "options": ["it drops utilization from ~90% down to ~20%", "it raises utilization from ~20% to ~90%+, and makes prefix sharing across requests nearly free", "it fixes utilization at exactly 100%", "it has no effect on utilization"]},
  {"stem": "Per the precision ladder, how many bytes per parameter do INT4 and FP4/NF4 use, and how does that compare with FP16?", "options": ["0.5 bytes each; 4× smaller than FP16", "1 byte each; 2× smaller than FP16", "2 bytes each; the same as FP16", "0.25 bytes each; 8× smaller than FP16"]},
  {"stem": "The lesson's recommended 'modern Hopper sweet spot' starter quantization config is:", "options": ["INT4 weights, INT4 activations, INT4 KV cache", "FP32 for every component, for maximum safety", "FP8 weights, FP16 activations, FP8 KV cache", "FP16 weights, FP8 activations, FP16 KV cache"]},
  {"stem": "Well-calibrated FP8 quantization typically costs about how much on MMLU versus FP16?", "options": ["greater than 10 points - noticeable degradation", "around 5 points", "about 0.1–0.3 points - negligible for roughly 2× throughput", "exactly zero - perfectly lossless for every model"]},
  {"stem": "In the quantization sensitivity ladder, ordering components from LEAST to MOST sensitive gives:", "options": ["attention output < activations < KV cache < weights", "weights < KV cache < activations < attention output", "KV cache < weights < attention output < activations", "all components are equally sensitive"]}
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Back to today's lesson__

    [Day 15 · Consolidation](index.md)

-   __Back to the week__

    [Week 3 - Attention &amp; KV Cache overview](../index.md)

-   __Continue the curriculum__

    [Day 16 · Multi-GPU Parallelism](../../week-04/module-1/index.md)

</div>
