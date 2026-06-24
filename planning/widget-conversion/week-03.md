# Widget Conversion Plan — Week 03 (Days 11–14)

**Branch:** `feat/content-fortification`  
**Pre-reading source:** `planning/source-material/Inference Engineering/Inference_Engineering_Pre_Lecture_Reading.md`  
**Readers used:** Reader 4 (~lines 379–483) + Reader 6 (~lines 588–725) for Day 11; Reader 4 for Day 12; Reader 4 for Day 13; Reader 7 (~lines 726–852) for Day 14  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Readers |
|--------|-----|-------|---------|
| module-1 | 11 | Prefill and Decode | Reader 4 + Reader 6 (serving sections) |
| module-2 | 12 | The KV Cache | Reader 4 + Study Guide §A.2 |
| module-3 | 13 | FlashAttention & PagedAttention | Reader 4 |
| module-4 | 14 | Quantization | Reader 7 |

All four lessons have `## Part 1 — Pre-Reading Review` and `## Part 7 — Wrap-up & Connection`. No structural changes needed.

---

## module-1 — Day 11 · Prefill and Decode

**File:** `docs/lessons/week-03/module-1/index.md`  
**Pre-reading:** Reader 4 (attention math) + Reader 6 (serving sections)  
**data-source label:** `Reader 4 — Attention Math + Reader 6 — Software Stack for ML`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-03-m1-readiness` | `readiness` | `Reader 4 — Attention Math + Reader 6 — Software Stack for ML` |
| Wrap-up | `week-03-m1-wrapup` | `wrap-up` | `Day 11 · Prefill and Decode` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: Prefill (~20 min): parallel processing of all input tokens, compute-bound
- Part 3 — Core Concepts: Decode (~20 min): autoregressive, one token per step, memory-bound
- Part 4 — Visual Timeline (~15 min): time breakdown across phases, KV cache introduction
- Part 5 — Hands-On: Calculate (~30 min): TTFT and ITL calculations
- Part 7 — Wrap-up & Connection (~15 min)

### Readiness question outline (20 questions — Reader 4 + Reader 6 serving)
Reader 4 attention math covers QKV mechanics; Reader 6 serving section covers
the serving pipeline, continuous batching concept, what a serving engine does.

**Recall (6):**
1. What is the difference between the prefill and decode phases in LLM inference?
2. Why is prefill considered compute-bound?
3. Why is decode considered memory-bound?
4. What does the KV cache store and why?
5. What is TTFT in a serving system?
6. What is ITL (inter-token latency)?

**Apply (8):**
7. A user sends a 500-token prompt and expects a 200-token response — how many decode steps?
8. Given TTFT = 400ms and ITL = 30ms, calculate total generation time for 50 tokens
9. Identify which phase dominates total GPU time for long-context generation
10. Classify: "serving 32 concurrent users with the same model" — what infrastructure component handles concurrency?
11. Select the correct description of what changes in memory usage as tokens are generated
12. Given equal hardware, which takes more wall-clock time: prefilling 1000 tokens or decoding 1000 tokens?
13. Identify the phase that benefits most from GPU parallelism
14. A request has 100 input tokens and 1 output token — which phase dominates total latency?

**Analyse (6):**
15. Why can't prefill and decode be optimised with the same techniques?
16. A serving system reports low TTFT but high ITL — what does this tell you about the bottleneck?
17. Why does the KV cache grow linearly with the number of tokens generated?
18. Compare the memory access pattern of prefill vs decode — what makes them fundamentally different?
19. A team increases GPU memory by 2× — which phase benefits more: prefill or decode? Why?
20. Why does batching multiple requests together improve throughput more during prefill than decode?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: prefill compute profile (parallel matmul), decode memory profile
(sequential GEMV), visual timeline breakdown, KV cache concept introduction,
TTFT and ITL calculation with worked examples.

**Recall (6):**
1. What type of operation dominates prefill: GEMM or GEMV?
2. What type of operation dominates decode: GEMM or GEMV?
3. How does KV cache size grow with generated tokens?
4. What is the primary reason decode is slower per token than prefill?
5. Name the two metrics the lesson uses to characterise inference latency
6. What percentage of total generation time is decode for a typical chat workload?

**Apply (8):**
7. A 70B model on H100 (140 GB weights) — estimate prefill time given 3.35 TB/s HBM bandwidth
8. Decode ITL = 50ms per token; user expects 100 output tokens — calculate decode phase duration
9. Given a timeline diagram, identify which segment is TTFT and which is the decode phase
10. Select the correct formula for total generation time given TTFT, ITL, and output token count
11. A request prefills 2000 tokens — is this prefill likely compute-bound or memory-bound?
12. Identify what is stored per layer in the KV cache (keys and values for all previous tokens)
13. Given a batch of 8 requests in decode, explain why each request still needs separate KV state
14. Calculate TTFT for a request where prefill takes 200ms and model loading is already complete

**Analyse (6):**
15. Why does prefill latency scale linearly with input tokens but is not simply proportional to decode latency × N?
16. Compare the impact of doubling batch size on TTFT vs ITL
17. A team separates prefill and decode onto different hardware — what advantage does this offer?
18. Why is the KV cache the primary memory bottleneck for long-context inference, not model weights?
19. Given two models (7B and 70B) with the same max context, compare their KV cache sizes
20. A user reports that longer prompts feel "slower to start" — which metric is affected and why?

---

## module-2 — Day 12 · The KV Cache

**File:** `docs/lessons/week-03/module-2/index.md`  
**Pre-reading:** Reader 4 + Study Guide §A.2  
**data-source label:** `Reader 4 — KV Cache section + Study Guide §A.2`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-03-m2-readiness` | `readiness` | `Reader 4 — KV Cache section + Study Guide §A.2` |
| Wrap-up | `week-03-m2-wrapup` | `wrap-up` | `Day 12 · The KV Cache` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: Why KV Cache Exists (~20 min): re-computation cost, what we're caching
- Part 3 — Deep Dive: KV Cache Size Formula (~20 min): 2 × layers × heads × head_dim × seq_len × bytes_per_element
- Part 4 — Hands-On: Calculate KV Cache Size (~30 min): Llama-3-8B and 70B examples
- Part 5 — Hands-On: GQA Impact (~20 min): grouped-query attention reduces KV cache size
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — Reader 4 KV Cache + Study Guide §A.2)
Reader 4 and §A.2 cover: why re-computing keys and values is expensive, what
is stored in the KV cache, memory implications of long contexts.

**Recall (6):**
1. What would have to be recomputed at each decode step without the KV cache?
2. What is stored in the KV cache — per token? Per layer?
3. How does KV cache memory scale with sequence length?
4. What is GQA (Grouped-Query Attention) and how does it differ from MHA?
5. Why does a longer context window increase peak GPU memory requirements?
6. What is the KV cache formula's relationship to the number of layers?

**Apply (8):**
7. A model has 32 layers, 32 heads, head_dim=128, seq_len=4096, FP16 — calculate KV cache size
8. Given Llama-3-8B specs, estimate the KV cache for a 2048-token conversation
9. GQA with 8 KV heads vs MHA with 32 KV heads — what is the memory reduction factor?
10. Identify what happens to available GPU memory for new requests as a long conversation continues
11. Select the correct explanation for why KV cache grows during generation but model weights don't
12. A serving system supports max context 8K but runs out of GPU memory at 4K — identify the cause
13. Calculate the KV cache for 70B model (80 layers, 8 KV heads GQA, head_dim=128) at 4096 tokens, FP16
14. Identify which component of the KV cache formula contributes most to its memory footprint

**Analyse (6):**
15. Why is managing KV cache memory a key challenge for multi-user serving?
16. Compare the memory trade-off between increasing max context and supporting more concurrent users
17. Why did GQA become the standard for large models — what does it sacrifice vs what it gains?
18. A serving system runs out of memory during a long conversation — should it offload KV cache to CPU or truncate?
19. Explain how KV cache prefilling (prefix caching) can reduce compute cost for repeated system prompts
20. Why does quantising KV cache (FP8 instead of FP16) help more at long contexts than short ones?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: re-computation cost argument, KV cache formula derivation,
worked calculations for Llama-3-8B and 70B, GQA vs MHA impact calculation.

**Recall (6):**
1. Write the KV cache size formula
2. How many KV heads does Llama-3-8B use (GQA)?
3. What is head_dim in the KV cache formula?
4. How does the KV cache formula change for GQA vs MHA?
5. For Llama-3-70B at 4096 tokens FP16, what is the approximate KV cache size?
6. Why does prefilling a KV cache for repeated system prompts save compute?

**Apply (8):**
7. Llama-3-8B: 32 layers, 8 KV heads, head_dim=128, FP16, seq=8192 — calculate KV cache
8. A model has 40 layers, 40 MHA heads, head_dim=128, seq=4096, FP16 — calculate KV cache
9. Same model switches to GQA with 8 KV heads — recalculate KV cache size
10. Given GPU memory = 80 GB, model weights = 14 GB — how much context can a KV cache support?
11. Identify the bottleneck when a serving engine can only serve short requests despite GPU availability
12. Select the correct statement about why the KV cache doesn't grow with additional requests (per-request isolation)
13. Calculate the memory freed when reducing context from 8192 to 4096 for a given model
14. A 70B model uses GQA (8 KV heads) — compare its KV cache to the same model with MHA (64 KV heads)

**Analyse (6):**
15. Why does the KV cache formula scale O(n) with sequence length but attention scores scale O(n²)?
16. A team increases layers from 32 to 48 — how does this affect KV cache vs model weights proportionally?
17. Compare the trade-offs of FP8 KV quantisation vs reducing max context to save memory
18. Why is KV cache a harder memory management problem than model weight management in serving?
19. Explain why streaming prefill of a KV cache (for prefix caching) requires the cache to be immutable
20. Given equal GPU memory, compare a single-user 128K context vs 128 users × 1K context — which uses more KV cache?

---

## module-3 — Day 13 · FlashAttention & PagedAttention

**File:** `docs/lessons/week-03/module-3/index.md`  
**Pre-reading:** Reader 4 (FlashAttention blog summary + paper abstract)  
**data-source label:** `Reader 4 — FlashAttention & Memory-Efficient Attention`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-03-m3-readiness` | `readiness` | `Reader 4 — FlashAttention & Memory-Efficient Attention` |
| Wrap-up | `week-03-m3-wrapup` | `wrap-up` | `Day 13 · FlashAttention & PagedAttention` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: Naive Attention's Memory Problem (~20 min): O(n²) materialisation
- Part 3 — Deep Dive: FlashAttention Mechanics (~20 min): tiling, SRAM reuse, no materialisation
- Part 4 — Hands-On: Memory Traffic Calculation (~25 min): naive vs FlashAttention HBM bytes
- Part 5 — Core Concepts: PagedAttention (~20 min): virtual memory for KV cache
- Part 6 — Hands-On: Multi-User Throughput (~20 min): fragmentation vs paging
- Part 7 — Wrap-up & Connection (~5 min)

### Readiness question outline (20 questions — Reader 4 FlashAttention)
Reader 4 covers: why naive attention materialises the N×N matrix in HBM, what
tiling does, the IO complexity argument, what PagedAttention is at a high level.

**Recall (6):**
1. What does naive attention materialise in HBM that FlashAttention avoids?
2. What is "tiling" in the context of FlashAttention?
3. What is the HBM IO complexity of naive attention vs FlashAttention?
4. What problem does PagedAttention solve that FlashAttention does not?
5. What is SRAM on a GPU and how does its size compare to HBM?
6. What does "IO-bound" mean for the attention kernel?

**Apply (8):**
7. For seq_len=4096 in FP16, calculate the size of the naive attention score matrix
8. FlashAttention avoids storing the attention matrix — where are intermediate results kept?
9. Identify which attention implementation is more suitable for long-context inference: naive or Flash
10. A serving engine uses naive attention — at seq_len=32768, what is the attention matrix size?
11. Select the correct description of what PagedAttention enables that contiguous KV allocation does not
12. Given a GPU with 50 MB SRAM per SM, identify the maximum tile size for a FlashAttention pass
13. Classify: FlashAttention — is it memory-bound or compute-bound relative to naive attention?
14. Select the correct statement about FlashAttention's numerical equivalence to naive attention

**Analyse (6):**
15. Why does FlashAttention improve throughput even though it performs the same number of FLOPs as naive attention?
16. Compare the memory access pattern of FlashAttention vs naive attention — what changes at the hardware level?
17. PagedAttention reduces KV cache fragmentation — why does fragmentation matter for concurrent users?
18. Why does combining FlashAttention + PagedAttention give more than the sum of their individual benefits?
19. FlashAttention-2 vs FlashAttention-1 — what key improvement was made and why?
20. A team enables FlashAttention on their serving engine — which users benefit most: those with short or long contexts?

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: O(n²) materialisation problem, tiling mechanics, SRAM vs HBM
tradeoff, HBM bytes comparison (naive vs Flash), PagedAttention virtual memory
analogy, fragmentation cost and paging benefit.

**Recall (6):**
1. What is the HBM IO complexity of naive attention (reads + writes for score matrix)?
2. What is the HBM IO complexity of FlashAttention?
3. What does PagedAttention borrow its design from in OS virtual memory?
4. How does PagedAttention store KV blocks — contiguous or non-contiguous?
5. What is the approximate SRAM size per SM on an H100?
6. What does "IO-bound" mean for attention kernels?

**Apply (8):**
7. Naive attention at seq_len=8192, FP16: calculate attention matrix HBM bytes (read + write)
8. FlashAttention at same seq_len — explain why HBM bytes are O(n) not O(n²)
9. Given 10 concurrent users each with different context lengths — identify why contiguous KV allocation wastes memory
10. Select the correct analogy: PagedAttention is to KV cache as ___ is to RAM
11. Calculate the memory wasted by 30% fragmentation in a 40 GB KV cache pool
12. Identify which component of vLLM directly implements PagedAttention
13. A model serving engine reports 40% KV cache utilisation despite available memory — likely cause?
14. Select the correct description of what happens when a new token is generated in FlashAttention

**Analyse (6):**
15. Why does the O(n²) → O(n) HBM reduction matter more at 32K context than at 1K context?
16. Compare the performance of FlashAttention at batch=1 vs batch=32 — where is the gain larger?
17. Why did PagedAttention require changes to the CUDA kernel, not just data structure layout?
18. A serving system without PagedAttention rejects a request because a single large contiguous block is unavailable, despite enough total free memory — why?
19. Compare FlashAttention and KV quantisation as memory-saving strategies — what does each sacrifice?
20. Explain why enabling FlashAttention in a serving engine typically requires no change to model weights or inference results.

---

## module-4 — Day 14 · Quantization

**File:** `docs/lessons/week-03/module-4/index.md`  
**Pre-reading:** Reader 7 — Numerical precision and floating point (~lines 726–852)  
**data-source label:** `Reader 7 — Numerical Precision and Floating Point`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-03-m4-readiness` | `readiness` | `Reader 7 — Numerical Precision and Floating Point` |
| Wrap-up | `week-03-m4-wrapup` | `wrap-up` | `Day 14 · Quantization` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: The Precision Ladder (~20 min): FP32 → FP16 → BF16 → FP8 → INT8 → INT4
- Part 3 — Deep Dive: Float vs Int & Sensitivity Ladder (~20 min): weights vs activations vs KV cache
- Part 4 — Hands-On: Weight Memory Calculations (~20 min): size at each precision
- Part 5 — Hands-On: Decode Latency at Different Precisions (~25 min): bandwidth-limited latency
- Part 6 — Hands-On: Combined Memory Budget (~20 min): weights + KV cache at various precisions
- Part 7 — Wrap-up & Connection (~5 min)

### Readiness question outline (20 questions — Reader 7)
Reader 7 covers: floating point representation (sign, exponent, mantissa), FP32
vs FP16 vs BF16 differences, dynamic range vs precision, why lower precision
loses information, what quantisation is conceptually.

**Recall (6):**
1. How many bits does FP32 use for exponent and mantissa?
2. What is the key difference between FP16 and BF16?
3. What does "dynamic range" mean for a floating-point format?
4. What does quantisation do to a floating-point weight?
5. Why does BF16 preserve more of FP32's dynamic range than FP16?
6. What does INT8 represent — is it a floating-point or fixed-point format?

**Apply (8):**
7. A FP32 weight matrix is 20 GB — what is its size in FP16?
8. A model with 7B parameters in FP16 — calculate memory footprint
9. Given that INT8 uses 1 byte per weight, how does a 70B model fit in 70 GB?
10. Identify which format has the largest dynamic range: FP32, FP16, or BF16
11. Select the correct description of what "dequantisation" does at inference time
12. A hardware accelerator only supports INT8 — which precision ladder level is the user limited to?
13. Given that activations have higher variance than weights, classify which requires more dynamic range
14. Select the correct trade-off when moving from FP16 to INT4: what is gained and what is risked?

**Analyse (6):**
15. Why does INT4 quantisation risk more quality loss than INT8 even with the same technique?
16. Compare weight quantisation and activation quantisation — which is harder to do without quality loss?
17. Why is BF16 often preferred over FP16 for training but both are common for inference?
18. A model quantised to INT4 produces good perplexity but fails on task-specific evals — explain why perplexity can mislead
19. Why does quantisation of KV cache (as opposed to weights) have a different quality risk profile?
20. A team uses GPTQ (weight-only INT4) — what does "weight-only" mean for the inference pipeline?

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: precision ladder, float vs int distinction, sensitivity ladder
(weights < activations < KV cache), memory calculations at each precision, latency
calculations (bandwidth-limited), combined memory budget.

**Recall (6):**
1. List the precision ladder from highest to lowest precision as covered in the lesson
2. Which tensor type is most sensitive to quantisation loss: weights, activations, or KV cache?
3. What is the memory footprint of a 70B model in FP16? In INT8? In INT4?
4. What does the "sensitivity ladder" state about which quantisation is safest?
5. What is the formula for decode latency lower bound from weight reads?
6. What does AWQ/GPTQ quantise, and what is left in higher precision?

**Apply (8):**
7. 70B model in FP16 = 140 GB; at INT8 = 70 GB; calculate read time at 3.35 TB/s for each
8. Moving from FP16 to FP8 weights — what is the memory reduction factor?
9. Given combined memory budget (weights + KV cache), calculate how much is available for KV cache at FP16 on an 80 GB GPU
10. A 7B INT4 model (3.5 GB) fits on a 4 GB GPU — calculate decode latency lower bound at 3.35 TB/s
11. Classify each quantisation scheme: weight-only INT4, W8A8, FP8-everything — by sensitivity level
12. Given that activations change dynamically, identify why static quantisation of activations is harder than weights
13. Select the correct precision for "fastest inference with acceptable quality" for production serving
14. Calculate the memory reduction when quantising both weights AND KV cache from FP16 to INT8

**Analyse (6):**
15. Why does weight-only quantisation (leaving activations in FP16) strike a better quality–speed trade-off than W4A4?
16. Compare FP8 and INT8 for weight quantisation — what does each preserve and what does each sacrifice?
17. A 70B model at INT4 fits on one H100 (80 GB) — but quality drops on certain tasks. What is the correct next step?
18. Explain why quantisation benefits scale with decode latency but not prefill latency proportionally
19. A team observes that INT4 is 4× smaller than FP16 but only 2× faster — explain this gap
20. Why does the "sensitivity ladder" put KV cache as most sensitive to quantisation loss at long contexts?

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Locate Reader 4, 6, 7 sections in `Inference_Engineering_Pre_Lecture_Reading.md`
- [ ] module-1 (Day 11): Reader 4+6 readiness + prefill/decode wrap-up
- [ ] module-2 (Day 12): Reader 4 KV cache readiness + KV cache formula wrap-up
- [ ] module-3 (Day 13): Reader 4 FlashAttention readiness + Flash+Paged wrap-up
- [ ] module-4 (Day 14): Reader 7 readiness + quantisation wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`
- [ ] After all 4 modules: `python3 scripts/audit_lessons.py` — 0 violations
