# Inference Engineering — Flashcards

*Spaced-repetition flashcards for the Inference Engineering phase (Weeks 2–5). Format: `Q` on one side, `A` on the other. Use Anki, Mochi, or any SR tool — or just cover the answer column and self-test. Organized by day, with a numerical-anchor tier for back-of-envelope facts.*

---

## Day 6 — What Happens When You Send a Prompt

| # | Q | A |
|---|---|---|
| 1 | What is the difference between training and inference? | Training learns the weights from data once (capital expense). Inference uses those fixed weights to answer requests, continuously (operational expense). |
| 2 | What is a token? | The unit an LLM reads and writes — a sub-word chunk (~4 chars / ~0.75 words in English). The model predicts one token at a time. |
| 3 | What is the context window? | The maximum number of tokens (prompt + generation) the model can attend to in one request. Everything outside it is invisible to the model. |
| 4 | What does temperature control? | How sharply the next-token probability distribution is sampled. Low temperature → deterministic/repetitive; high → diverse/creative. Temperature 0 ≈ greedy (argmax). |
| 5 | Why can the same prompt give different answers? | Sampling is stochastic: at temperature > 0 the model draws from a probability distribution, so runs differ unless you fix the seed and set temperature 0. |
| 6 | What are the two phases of generating a response? | Prefill (process the whole prompt in parallel, produce the first token) then decode (generate the rest one token at a time, each conditioned on the last). |

---

## Day 7 — Meet the GPU

| # | Q | A |
|---|---|---|
| 7 | Why are GPUs used for inference instead of CPUs? | GPUs have thousands of cores optimized for the massively parallel matrix multiplies at the heart of a transformer; CPUs have few, latency-optimized cores. |
| 8 | What is a Streaming Multiprocessor (SM)? | The GPU's fundamental compute unit — a cluster of cores that execute threads in parallel. An H100 has ~132 SMs. |
| 9 | What are Tensor Cores? | Dedicated hardware units that do fused matrix-multiply-accumulate on small tiles, giving the bulk of an LLM GPU's FLOPs (esp. at FP16/FP8). |
| 10 | Name the GPU generations in order (recent NVIDIA). | Pascal → Volta → Ampere (A100) → Hopper (H100/H200) → Blackwell (B200). Each adds bandwidth, memory, and lower-precision formats. |
| 11 | What is the CUDA stack? | The software layers between your model and the metal: CUDA (kernels) → cuDNN/cuBLAS → framework (PyTorch) → inference engine (vLLM). |
| 12 | What is HBM? | High-Bandwidth Memory — the GPU's large, fast on-package DRAM (e.g. 80 GB on an H100) where weights and the KV cache live. |

---

## Day 8 — Memory Is the Bottleneck

| # | Q | A |
|---|---|---|
| 13 | Name the tiers of the GPU memory hierarchy, fastest to slowest. | Registers → shared memory / L1 → L2 cache → HBM (device memory) → host (CPU) RAM. Capacity grows as speed drops. |
| 14 | What is memory bandwidth and why does it matter? | The rate data moves between HBM and the compute units (H100 ≈ 3.35 TB/s). Decode reads all weights per token, so bandwidth caps token throughput. |
| 15 | Why is decoding usually memory-bound, not compute-bound? | Generating one token touches every weight but does little math per byte loaded, so the GPU waits on HBM reads rather than on the ALUs. |
| 16 | Where does the KV cache live, and why is that a problem? | In HBM, alongside the weights. It grows with sequence length × batch, competing with weights for scarce memory and capping concurrency. |
| 17 | Two things consuming GPU memory during serving? | (1) Model weights (fixed). (2) The KV cache (grows with tokens in flight). Activations are comparatively small during decode. |

---

## Day 9 — Compute-Bound vs Memory-Bound

| # | Q | A |
|---|---|---|
| 18 | What is arithmetic intensity? | FLOPs performed per byte of memory moved. High intensity → compute-bound; low intensity → memory-bound. |
| 19 | What is the roofline model? | A chart of achievable FLOPs vs arithmetic intensity: performance is capped by memory bandwidth (sloped part) until intensity is high enough to be capped by peak compute (flat part). |
| 20 | Is prefill compute-bound or memory-bound? | Compute-bound — it multiplies the whole prompt through the weights in parallel (high arithmetic intensity). |
| 21 | Is decode compute-bound or memory-bound? | Memory-bound — one token at a time reuses each weight once, so it is limited by HBM bandwidth. |
| 22 | How does batching change the bound? | Batching raises arithmetic intensity (weights loaded once, reused across many sequences), pushing decode toward compute-bound and lifting throughput. |

---

## Day 10 — Consolidation: The GPU & Memory

| # | Q | A |
|---|---|---|
| 23 | In one sentence, why is inference a memory problem before it is a compute problem? | Decode rereads gigabytes of weights and KV cache from HBM for every token, so bandwidth — not raw FLOPs — sets the ceiling for most workloads. |
| 24 | You want more tokens/sec on a memory-bound workload. First lever? | Increase batch size (more concurrency) so each weight load is amortized across many sequences — until memory or latency limits are hit. |
| 25 | Why does a longer context slow generation even before the window fills? | A larger KV cache means more bytes read from HBM per decode step and less room for concurrent requests. |
| 26 | Prefill vs decode: which sets time-to-first-token and which sets tokens-per-second? | Prefill sets TTFT; decode sets steady-state TPS. |

---

## Day 11 — Prefill vs Decode

| # | Q | A |
|---|---|---|
| 27 | What happens during prefill? | The entire prompt is processed in one parallel pass, building the KV cache for all prompt tokens and emitting the first output token. |
| 28 | What happens during decode? | Tokens are generated autoregressively — one forward pass per token, each attending to the growing KV cache. |
| 29 | What is TTFT and which phase drives it? | Time To First Token — the latency until the first token appears; driven by prefill (and queueing). |
| 30 | What is ITL and which phase drives it? | Inter-Token Latency — the gap between successive tokens during streaming; driven by decode (memory-bound). |
| 31 | What is prefill–decode disaggregation? | Running prefill and decode on separate GPU pools so the compute-heavy prefill doesn't stall latency-sensitive decode, and each pool is tuned independently. |

---

## Day 12 — KV Cache

| # | Q | A |
|---|---|---|
| 32 | What does the KV cache store, and why? | The key and value vectors for every past token, so each new token can attend to history without recomputing prior tokens' K/V every step. |
| 33 | What drives KV cache size? | Roughly 2 (K and V) × layers × kv-heads × head-dim × sequence-length × batch × bytes-per-value. It grows linearly with tokens and batch. |
| 34 | What problem does PagedAttention solve? | KV-cache memory fragmentation. It stores the cache in fixed-size non-contiguous blocks (like OS paging), so memory isn't wasted and blocks can be shared. |
| 35 | How does PagedAttention enable prefix sharing? | Identical prompt prefixes can point to the same physical KV blocks (copy-on-write), saving memory across requests that share a system prompt. |
| 36 | One trick to shrink the KV cache at the model level? | Grouped-Query Attention (GQA) or Multi-head Latent Attention (MLA) — fewer/compressed KV heads mean a much smaller cache. |

---

## Day 13 — FlashAttention

| # | Q | A |
|---|---|---|
| 37 | What is self-attention, in one line? | Each token computes a weighted sum over all tokens' values, where weights come from query·key similarity — how the model mixes context. |
| 38 | What is the naive cost of attention in sequence length? | O(N²) in both compute and memory to materialize the full N×N attention score matrix. |
| 39 | What does FlashAttention change? | It fuses the attention computation into tiles kept in fast SRAM and never writes the full N×N matrix to HBM — same math, O(N) memory, far less IO. |
| 40 | Is FlashAttention an approximation? | No — it is exact attention. The speedup comes purely from IO-aware tiling and recomputation, not from dropping terms. |
| 41 | Why does FlashAttention help most on long contexts? | The O(N²) HBM traffic it eliminates grows with sequence length, so the IO savings compound as contexts get longer. |

---

## Day 14 — Quantization

| # | Q | A |
|---|---|---|
| 42 | What is quantization? | Representing weights/activations in fewer bits (FP16 → INT8 → INT4) to cut memory and bandwidth, trading a little numeric precision for speed and capacity. |
| 43 | Bytes per value: FP16, INT8, INT4? | FP16 = 2 bytes, INT8 = 1 byte, INT4 = 0.5 byte. Halving precision roughly halves the memory and bandwidth for that tensor. |
| 44 | What is the sensitivity ladder, least to most sensitive? | Weights < KV cache < activations < attention output. Weights tolerate the most aggressive quantization; attention outputs are the most fragile. |
| 45 | Why quantize weights before activations? | Weights are static and least sensitive, so low-bit weights give big memory wins with little quality loss; activations are dynamic and higher-risk. |
| 46 | How do you know quantization didn't break the model? | Run an eval suite (incl. a refusal/safety category) and compare against the full-precision baseline — speed alone can hide quality regressions. |

---

## Day 15 — Consolidation: Attention & KV Cache

| # | Q | A |
|---|---|---|
| 47 | Why is the KV cache the central object of inference optimization? | It is the fast-growing, memory-hungry state that limits concurrency and context length; most serving tricks (paging, GQA/MLA, quantized KV) target it. |
| 48 | FlashAttention vs PagedAttention — what does each optimize? | FlashAttention optimizes the *compute* of attention (IO-aware tiling). PagedAttention optimizes the *storage* of the KV cache (block paging). |
| 49 | You must serve a 128k-context model on limited memory. Two levers? | Quantize the KV cache (e.g. to INT8) and use a smaller-KV attention variant (GQA/MLA); page the cache to avoid fragmentation. |

---

## Day 16 — Multi-GPU Parallelism

| # | Q | A |
|---|---|---|
| 50 | What is tensor parallelism? | Splitting individual weight matrices across GPUs within a layer; each GPU computes a shard and results are combined with an all-reduce every layer. |
| 51 | What interconnect does tensor parallelism demand, and why? | Fast intra-node links (NVLink) — it all-reduces activations every layer, so slow links (PCIe/Ethernet) throttle it badly. |
| 52 | What is data parallelism? | Replicating the whole model on each GPU and splitting *requests* across replicas. Scales throughput, not model size. |
| 53 | Tensor parallelism vs data parallelism — when each? | Tensor parallelism when the model is too big for one GPU (split the model); data parallelism when it fits and you need more throughput (replicate it). |
| 54 | What is the `--tp` (tensor-parallel size) flag controlling? | How many GPUs one model instance is sharded across. |

---

## Day 17 — Pipeline Parallelism + MoE

| # | Q | A |
|---|---|---|
| 55 | What is pipeline parallelism? | Splitting the model's *layers* across GPUs in stages; activations flow stage to stage, with micro-batches keeping stages busy. |
| 56 | What is the "bubble" in pipeline parallelism? | Idle time while the pipeline fills and drains; micro-batching shrinks it but never fully removes it. |
| 57 | What is a Mixture of Experts (MoE)? | An FFN split into many "expert" sub-networks; a router sends each token to only the top-k experts, so total params are huge but active params per token are small. |
| 58 | Why is MoE attractive for inference? | You get the quality of a very large parameter count while only paying compute for the few experts activated per token. |
| 59 | What is Multi-head Latent Attention (MLA)? | An attention variant that compresses keys/values into a low-rank latent, drastically shrinking the KV cache while preserving quality. |

---

## Day 18 — Speculative Decoding

| # | Q | A |
|---|---|---|
| 60 | What is speculative decoding? | A small "draft" model proposes several tokens ahead; the large "target" model verifies them in a single parallel pass, keeping the longest correct prefix. |
| 61 | Why does speculative decoding speed things up? | Decode is memory-bound, so one target forward pass can verify k draft tokens for nearly the cost of generating one — turning latency into parallel verification. |
| 62 | Does speculative decoding change the output distribution? | No — with proper acceptance sampling it is lossless: output matches what the target model would have produced alone. |
| 63 | What determines the speedup? | The draft model's acceptance rate — how often its proposals survive verification. Higher acceptance → more tokens per target pass. |

---

## Day 19 — vLLM Introduction

| # | Q | A |
|---|---|---|
| 64 | Name three inference engines. | vLLM, TensorRT-LLM, SGLang. They wrap the model with batching, paging, and scheduling for production serving. |
| 65 | What is continuous (in-flight) batching? | Iteration-level scheduling: sequences join and leave the batch every decode step, so finished requests free slots immediately instead of waiting for the whole batch. |
| 66 | Static batching vs continuous batching? | Static waits for a fixed batch to all finish (GPU idles on stragglers). Continuous swaps sequences in/out each step, keeping the GPU full. |
| 67 | What two vLLM features most raise throughput? | PagedAttention (memory-efficient KV cache) and continuous batching (high GPU utilization). |
| 68 | What does `--concurrency` control in a benchmark? | How many requests are in flight at once — the primary knob for trading latency against throughput. |

---

## Day 20 — Consolidation: Scaling & Stacks

| # | Q | A |
|---|---|---|
| 69 | Order these by interconnect demand: data, tensor, pipeline parallelism. | Tensor (highest, per-layer all-reduce) > pipeline (stage-to-stage activations) > data (lowest, independent replicas). |
| 70 | Which techniques cut *latency* vs *memory* vs *throughput*? | Latency: speculative decoding, disaggregation. Memory: quantization, paging, MLA/GQA. Throughput: continuous batching, tensor parallelism. |
| 71 | A 70B model won't fit on one 80 GB GPU. What do you reach for first? | Tensor parallelism across GPUs on one node (NVLink), optionally plus weight quantization to reduce the shard sizes. |

---

## Day 21 — Latency vs Throughput

| # | Q | A |
|---|---|---|
| 72 | Define latency vs throughput for inference. | Latency: time for one request (TTFT, ITL). Throughput: total tokens/requests served per second across all users. They trade off. |
| 73 | The core latency–throughput tradeoff, in one line? | Bigger batches raise throughput but add queueing/compute delay per request, raising latency; smaller batches do the reverse. |
| 74 | What is perceived TPS and its formula? | Tokens/sec a single streaming user sees. perceived TPS ≈ 1000 / ITL(ms). |
| 75 | What do P50, P95, P99 mean? | Latency percentiles: P95 = 95% of requests are faster than this value. Tail percentiles (P95/P99) capture the bad-case UX. |
| 76 | Why optimize P99 for user-facing services? | Because the slowest 1% of requests are what frustrated users actually feel; a good median hides a bad tail. |
| 77 | Which metric answers "is the model fast?" for a chat app vs a batch job? | Chat: TTFT / ITL (latency). Batch summarization: total throughput (tokens/sec). |

---

## Day 22 — Production Deployment

| # | Q | A |
|---|---|---|
| 78 | Shared (serverless) vs dedicated inference? | Shared: public API, pay per token, zero ops, noisy neighbors. Dedicated: rented GPUs, pay per hour, full control, you own utilization. |
| 79 | When does dedicated beat shared economically? | Once sustained volume is high enough that per-hour GPU cost per token drops below the per-token API price — i.e. you can keep the GPU busy. |
| 80 | Why is autoscaling LLM serving hard? | Cold starts are slow (load tens of GB of weights) and GPUs are expensive to keep warm, so scaling to zero trades cost against first-request latency. |
| 81 | What is an SLO in this context? | A Service-Level Objective — a target such as "P95 TTFT < 500 ms" that the deployment must meet, driving batch-size and capacity choices. |
| 82 | Why report latency at a fixed concurrency? | Latency is meaningless without load; the same server is fast at concurrency 1 and slow at 100, so numbers must state the concurrency. |

---

## Day 23 — LLM Evaluation

| # | Q | A |
|---|---|---|
| 83 | Why is measuring inference speed not enough? | Speed can look great while quality quietly regresses (e.g. after quantization); you must evaluate output quality alongside latency/throughput. |
| 84 | What four categories should a structured eval cover? | Factual recall, math/reasoning, code generation, and refusal/safety. |
| 85 | Why must an eval include a refusal/safety category? | Aggressive optimization (esp. quantization) can erode guardrails; without a refusal category you systematically over-rate a broken model. |
| 86 | What is Goodhart's Law and why does it bite evals? | "When a measure becomes a target, it ceases to be a good measure" — models/teams overfit the benchmark, so it stops reflecting real quality. |
| 87 | What is constrained (structured) decoding? | Masking the logits so only tokens valid under a grammar or JSON schema can be sampled — guaranteeing structurally valid output. |
| 88 | What does "passed" mean for an eval prompt? | An expected *behavior*, not just an expected answer — the specific, checkable property the response must satisfy. |

---

## Day 24 — Inference Economics

| # | Q | A |
|---|---|---|
| 89 | What are the main drivers of inference cost? | GPU-hours (hardware × time) divided by tokens served — so utilization, batch efficiency, and model size dominate cost per token. |
| 90 | Why does higher utilization lower cost per token? | Fixed GPU rental is paid per hour regardless of load; packing more tokens into each GPU-hour spreads that cost over more output. |
| 91 | How does quantization affect cost? | Smaller weights/KV fit more concurrency per GPU and raise throughput, cutting GPU-hours per token — provided quality holds. |
| 92 | Cost lever with the biggest headline effect on $/token? | Right-sizing the model (smallest model that passes evals) — compute scales steeply with parameter count. |

---

## Day 25 — Consolidation: Phase 1 Synthesis

| # | Q | A |
|---|---|---|
| 93 | Trace a request end-to-end through the concepts. | Tokenize → prefill (compute-bound, builds KV cache, sets TTFT) → decode (memory-bound, streams tokens, sets ITL/TPS) → detokenize; batching + paging keep the GPU busy. |
| 94 | Give the one-line role of each: batching, caching, quantization, speculation, parallelism, disaggregation. | Batching: utilization. Caching (KV): avoid recompute. Quantization: shrink memory. Speculation: cut latency. Parallelism: fit/scale the model. Disaggregation: isolate prefill from decode. |
| 95 | A chat SLO of P95 TTFT < 300 ms is missed under load. Two levers? | Add prefill capacity / disaggregate prefill from decode, and cap batch size or add replicas to shorten the queue. |
| 96 | Why is "throughput per dollar" the metric that ties Phase 1 together? | Every technique ultimately moves tokens-per-GPU-hour; latency SLOs bound how far you can push batching, and quality evals bound how far you can push quantization. |

---

## Numerical-anchor cards (high-yield facts)

| # | Q | A |
|---|---|---|
| 97 | H100 HBM capacity and bandwidth? | 80 GB HBM3, ≈ 3.35 TB/s memory bandwidth. |
| 98 | Rough tokens-to-words and chars-per-token? | ~0.75 words per token; ~4 characters per token in English. |
| 99 | Bytes per value at FP16 / INT8 / INT4? | 2 / 1 / 0.5 bytes. |
| 100 | Perceived tokens/sec from a 20 ms ITL? | 1000 / 20 = 50 tokens/sec. |
| 101 | Which phase is compute-bound and which is memory-bound? | Prefill = compute-bound; decode = memory-bound. |
| 102 | Attention memory cost: naive vs FlashAttention? | Naive O(N²), FlashAttention O(N) HBM traffic (exact, not approximate). |
