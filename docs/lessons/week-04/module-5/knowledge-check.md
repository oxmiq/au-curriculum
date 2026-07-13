<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <a href="../">Day 20 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-04/module-5}
  </div>
</div>

# Week 4 Knowledge Check

**Week 4 · Scaling & Stacks.** 27-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-04-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 4 · Scaling &amp; Stacks" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Tensor parallelism reduces decode latency mainly because it:",
    "options": [
      "Divides each GPU's per-token weight reads by the TP size",
      "Eliminates the KV cache entirely",
      "Replaces FlashAttention with a faster kernel",
      "Adds more total HBM to the cluster"
    ],
    "answer": 0,
    "explain": "Decode is memory-bandwidth bound. Sharding the weights means each GPU reads only 1/tp of the model per token, so latency drops roughly linearly with tp until per-layer comms dominate."
  },
  {
    "stem": "Which components does TP leave replicated (not split) on every rank?",
    "options": [
      "The Q/K/V and output projection matrices",
      "The MLP up- and down-projection matrices",
      "LayerNorm parameters and the residual-stream activations",
      "The token embedding and unembedding tables"
    ],
    "answer": 2,
    "explain": "LayerNorm and the residual stream are small and needed by every shard, so they stay replicated. The dense attention/MLP matrices (and usually embeddings) are what TP splits column-wise."
  },
  {
    "stem": "TP must stay within a single node because:",
    "options": [
      "NVIDIA's license forbids cross-node tensor parallelism",
      "The per-layer all-reduce needs NVLink-class bandwidth (~900 GB/s) that cross-node fabrics can't sustain",
      "CUDA contexts cannot be shared between two processes",
      "Pipeline parallelism is always faster than TP"
    ],
    "answer": 1,
    "explain": "Every layer ends in an all-reduce that moves tens of GB/s between ranks. Only NVLink keeps up; PCIe (~64 GB/s) and InfiniBand (~50 GB/s/NIC) become the bottleneck and decode latency collapses."
  },
  {
    "stem": "For Llama-3-70B in FP16 at tp=8, the per-GPU weight shard is about:",
    "options": [
      "140 GB",
      "70 GB",
      "35 GB",
      "17.5 GB"
    ],
    "answer": 3,
    "explain": "70B params x 2 bytes = 140 GB total; 140 / 8 = 17.5 GB of weights per GPU, leaving room in an 80 GB H100 for KV cache and activations. This is why tp=8 is the canonical 70B config."
  },
  {
    "stem": "After each layer's sharded matmul, TP performs which communication primitive?",
    "options": [
      "All-reduce",
      "Point-to-point send",
      "Broadcast from rank 0",
      "All-to-all"
    ],
    "answer": 0,
    "explain": "Each rank computes a partial sum from its weight slice; one all-reduce per layer combines the partials so every rank holds the full activation before the next layer begins."
  },
  {
    "stem": "Raising TP from 4 to 8 sometimes lowers throughput. The most likely reason is:",
    "options": [
      "HBM bandwidth drops as more GPUs are added",
      "PyTorch silently caps TP at 4 ranks",
      "The per-layer all-reduce cost grows while per-GPU compute shrinks, so comms eventually dominate",
      "The KV cache disappears at tp=8"
    ],
    "answer": 2,
    "explain": "More ranks shrink per-GPU compute roughly linearly, but the all-reduce involves more participants and data. For small models or short sequences the comms overhead can overtake the sharding win."
  },
  {
    "stem": "Pipeline parallelism splits the model:",
    "options": [
      "Width-wise, within each layer",
      "Depth-wise, across contiguous groups of layers (stages)",
      "By attention head",
      "By numerical precision"
    ],
    "answer": 1,
    "explain": "Each stage holds a contiguous block of layers; a token's forward pass flows stage to stage, with only activations crossing the boundary. TP, by contrast, splits within a layer."
  },
  {
    "stem": "A 'pipeline bubble' is:",
    "options": [
      "A GPU manufacturing defect",
      "A KV-cache eviction event",
      "Idle time in a stage waiting for input from a prior stage",
      "An out-of-memory crash"
    ],
    "answer": 2,
    "explain": "Stages sit idle during pipeline fill and drain. Running many micro-batches concurrently shrinks it: bubble fraction is approximately (stages - 1) / micro-batches."
  },
  {
    "stem": "With 4 pipeline stages, the bubble fraction is smallest when you run:",
    "options": [
      "1 micro-batch",
      "4 micro-batches",
      "16 micro-batches",
      "64 micro-batches"
    ],
    "answer": 3,
    "explain": "Bubble fraction is about (stages - 1) / micro-batches = 3/64 = ~5%. More micro-batches keep the stages filled; real systems target under 10%."
  },
  {
    "stem": "Compared with TP, pipeline parallelism between stages needs:",
    "options": [
      "Much higher bandwidth than TP",
      "Much lower bandwidth — it passes activations, not weights, at stage boundaries",
      "Exactly the same bandwidth as TP",
      "No inter-GPU communication at all"
    ],
    "answer": 1,
    "explain": "PP sends only activations (batch x seq x hidden) point-to-point at stage boundaries, so InfiniBand (~50 GB/s) suffices. TP's per-layer all-reduce needs NVLink. That's why PP is the cross-node lever."
  },
  {
    "stem": "In an MoE model with top-2-of-8 routing, each token is processed by:",
    "options": [
      "All 8 experts",
      "4 experts",
      "2 experts",
      "1 expert"
    ],
    "answer": 2,
    "explain": "The router selects the top-K (here 2) experts per token — the 'active parameters'. Total params stay huge but per-token compute stays small (e.g. Mixtral: ~13B active of ~47B total)."
  },
  {
    "stem": "The operational risk unique to expert parallelism is:",
    "options": [
      "Hot experts — uneven routing overloads some GPUs while others idle",
      "The KV cache growing too large for HBM",
      "Quantization rounding error",
      "Weights loading slowly from disk"
    ],
    "answer": 0,
    "explain": "Routers rarely produce uniform load, so some experts receive disproportionate traffic and create stragglers. Capacity must be sized for worst-case, not average, expert load."
  },
  {
    "stem": "Expert parallelism routes tokens to their experts using which communication pattern?",
    "options": [
      "All-reduce, exactly like tensor parallelism",
      "Point-to-point activation passing, exactly like pipeline parallelism",
      "A single broadcast from a central parameter server",
      "All-to-all — activations are dispatched to the chosen experts and results returned"
    ],
    "answer": 3,
    "explain": "Each expert lives on a different GPU. Per token the router picks top-K experts, the activation is all-to-all'd out to them, each computes locally, and results are all-to-all'd back. Every token touches the network, which is why EP is expensive."
  },
  {
    "stem": "Why is Mixtral 8x7B only ~13B active parameters despite ~47B total?",
    "options": [
      "It quantizes ~34B of parameters down to zero",
      "Top-2-of-8 routing sends each token through only 2 of the 8 expert MLPs per layer",
      "~34B of parameters live on CPU and never run at inference",
      "Only the attention layers run per token; all experts are skipped"
    ],
    "answer": 1,
    "explain": "An MoE layer has many expert MLPs but each token is routed to a small subset. With top-2 of 8 (each ~7B), only ~13B parameters are active per token even though the model totals ~47B."
  },
  {
    "stem": "Speculative decoding works by:",
    "options": [
      "Skipping transformer layers for easy tokens",
      "A small draft model proposing K tokens that the target verifies in one parallel forward pass",
      "Pre-computing every possible output offline",
      "Lossily approximating the target model's logits"
    ],
    "answer": 1,
    "explain": "The tiny draft model proposes K tokens cheaply; the target verifies all K in a single forward pass (like a mini-prefill), turning memory-bound sequential decode into batched-style work. 2-3x speedup is typical."
  },
  {
    "stem": "Under proper speculative sampling, output quality versus vanilla decoding is:",
    "options": [
      "Lower — it is an approximation",
      "Higher than the target alone",
      "Provably identical to sampling from the target alone",
      "Random and workload-dependent"
    ],
    "answer": 2,
    "explain": "The rejection-sampling correction preserves the target model's exact output distribution, so speculative decoding is lossless (bit-exact) — a pure systems win, not a quality tradeoff."
  },
  {
    "stem": "How does the target model decide whether to accept a draft token?",
    "options": [
      "It accepts any token whose probability clears a fixed threshold the user sets",
      "It applies a rejection-sampling test — accept with probability min(1, p_target/p_draft), and resample on rejection",
      "It compares token embeddings for cosine similarity",
      "It takes a majority vote across several draft models"
    ],
    "answer": 1,
    "explain": "Acceptance is stochastic rejection sampling: each draft token is kept with probability min(1, p_target/p_draft), and on rejection the target resamples from the corrected distribution. This — not a fixed probability threshold — is what makes the output bit-exact."
  },
  {
    "stem": "If the draft is wrong on token 3 of a 5-token proposal, what happens to tokens 1-2?",
    "options": [
      "They are kept (accepted); only token 3 onward is reconsidered",
      "All 5 tokens are discarded and redrafted",
      "Tokens 1-2 are also rejected",
      "The draft model is disabled for the rest of the request"
    ],
    "answer": 0,
    "explain": "Acceptance is a prefix: tokens 1-2 stay accepted and only from the first rejection does the target take over. The next iteration continues from the corrected token."
  },
  {
    "stem": "What most commonly kills speculative decoding's speedup?",
    "options": [
      "High GPU temperature causing throttling",
      "The draft model using more memory than the target",
      "A low acceptance rate — the draft mismatches the target too often (e.g. creative / high-temperature text)",
      "Large batch sizes reducing output accuracy"
    ],
    "answer": 2,
    "explain": "Speedup scales with the acceptance rate. Predictable text (code, templates) gives high acceptance and big gains; surprising or high-temperature output gives low acceptance and the win shrinks. A too-slow or too-big draft also erodes it."
  },
  {
    "stem": "Why is decode specifically the phase that benefits from speculative decoding?",
    "options": [
      "Decode is memory-bound and serial, so Tensor Cores sit idle — verification turns wasted compute into extra tokens",
      "Decode is compute-bound and needs additional FLOPs the draft supplies",
      "The draft model runs on the CPU, freeing GPU memory",
      "It shrinks the KV cache during generation"
    ],
    "answer": 0,
    "explain": "Single-stream decode reads all the weights from HBM to make one token, leaving the Tensor Cores ~99.99% idle. Verifying K draft tokens in one pass uses that otherwise-wasted compute — 'free latency' if the workload is predictable."
  },
  {
    "stem": "Static batching is wasteful primarily because:",
    "options": [
      "It only runs on CPU",
      "It cannot use tensor parallelism",
      "New requests wait for the whole batch to finish, and short outputs idle until the longest completes",
      "It always runs out of GPU memory"
    ],
    "answer": 2,
    "explain": "The batch returns only when every request finishes, so the longest output dominates and short ones sit idle. Continuous batching fixes both by admitting/evicting at every decode step."
  },
  {
    "stem": "Continuous batching (iteration-level scheduling) means:",
    "options": [
      "The batch composition changes after every decode step — finished requests are evicted and new ones admitted",
      "Requests are sorted by length before one fixed batch runs to completion",
      "All requests must finish before any new one can start",
      "Each request is given its own dedicated GPU"
    ],
    "answer": 0,
    "explain": "The running batch is re-scheduled every token step: completed requests leave and waiting ones join, so the GPU stays saturated and new requests start almost immediately."
  },
  {
    "stem": "Continuous batching relies structurally on:",
    "options": [
      "FP8 weights",
      "Speculative decoding",
      "CPU offload of the KV cache",
      "Block-based KV-cache allocation (PagedAttention)"
    ],
    "answer": 3,
    "explain": "Admitting and evicting requests every step means KV slots are constantly allocated and freed at variable sizes. PagedAttention's block allocator prevents fragmentation — that's why vLLM ships both together."
  },
  {
    "stem": "PagedAttention reduces KV-cache waste by:",
    "options": [
      "Compressing the cache with FP8 quantization",
      "Storing the cache in fixed-size blocks (~16 tokens) allocated and freed independently, like OS virtual memory",
      "Offloading the cache to CPU RAM and paging it back on demand",
      "Discarding KV entries during the prefill phase"
    ],
    "answer": 1,
    "explain": "Traditional serving assumes a contiguous KV cache, so variable-length outputs cause internal fragmentation and OOM. Paged blocks that allocate/free independently drive fragmentation to near zero."
  },
  {
    "stem": "Plain PyTorch model.generate() is typically how much slower than vLLM for serving?",
    "options": [
      "No different",
      "About 5-10x",
      "About 100x",
      "It is actually faster than vLLM"
    ],
    "answer": 1,
    "explain": "Bare PyTorch lacks continuous batching, PagedAttention, FlashAttention kernels, hot-path quantization, and fused kernels — so throughput is roughly 5-10x lower and it collapses under real concurrency."
  },
  {
    "stem": "Best default engine for an OSS deployment on NVIDIA with broad model support:",
    "options": [
      "vLLM",
      "TGI",
      "TensorRT-LLM",
      "SGLang"
    ],
    "answer": 0,
    "explain": "vLLM is the OSS default (PagedAttention origin, broad model coverage). Reach for TensorRT-LLM to squeeze peak NVIDIA perf, SGLang for structured/tool-heavy output, and TGI for a simple HF deploy."
  },
  {
    "stem": "Which engine is best suited to heavy structured-output and tool-calling (agentic) workloads?",
    "options": [
      "TensorRT-LLM",
      "SGLang",
      "TGI",
      "Plain PyTorch"
    ],
    "answer": 1,
    "explain": "SGLang targets structured generation and multi-turn / tool-calling programs, adding RadixAttention for KV reuse across shared prefixes. vLLM is the versatile general-purpose default."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 20 · Consolidation](index.md)

-   __Back to the week__

    [Week 4 — Scaling &amp; Stacks overview](../index.md)

-   __Continue the curriculum__

    [Day 21 · Latency vs Throughput](../../week-05/module-1/index.md)

</div>
