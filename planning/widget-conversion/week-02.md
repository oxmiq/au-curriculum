# Widget Conversion Plan — Week 02 (Days 6–9)

**Branch:** `feat/content-fortification`  
**Pre-reading source:** `planning/source-material/Inference Engineering/Inference_Engineering_Pre_Lecture_Reading.md`  
**Readers used:** Reader 1 (~lines 63–166), Reader 5 (~lines 484–587), Reader 5 memory section + Study Guide §A.3 (Day 8), Reader 4 (~lines 379–483) + Study Guide §A.5 (Day 9)  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Readers |
|--------|-----|-------|---------|
| module-1 | 6 | What Happens When You Send a Prompt | Reader 1 |
| module-2 | 7 | Meet the GPU | Reader 5 (architecture) |
| module-3 | 8 | Memory Is the Bottleneck | Reader 5 (memory) + Study Guide §A.3 |
| module-4 | 9 | Compute-Bound vs Memory-Bound | Reader 4 + Study Guide §A.5 |

All four lessons have `## Part 1 — Pre-Reading Review` and `## Part 7 — Wrap-up & Connection`. No structural changes needed.

---

## module-1 — Day 6 · What Happens When You Send a Prompt

**File:** `docs/lessons/week-02/module-1/index.md`  
**Pre-reading:** Reader 1 — AI in production (lines ~63–166 of Pre_Lecture_Reading.md)  
**data-source label:** `Reader 1 — AI in production`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-02-m1-readiness` | `readiness` | `Reader 1 — AI in production` |
| Wrap-up | `week-02-m1-wrapup` | `wrap-up` | `Day 6 · What Happens When You Send a Prompt` |

### Part structure
- Part 1 — Pre-Reading Review (~15 min)
- Part 2 — Core Concepts: Inference Pipeline (~20 min): tokenise → embed → prefill → decode → detokenise
- Part 3 — Deep Dive: Prefill vs Decode (~20 min): compute characteristics, time budget
- Part 4 — Worked Example Analysis (~25 min): trace a real prompt through all stages
- Part 5 — Hands-On: Trace the Pipeline (~30 min): trace exercise with timing estimates
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — Reader 1)
Reader 1 covers: what LLM inference is, why it's expensive, the basic token pipeline,
why companies care about latency and cost, what a "serving system" is, the
difference between hosted API and self-hosted inference.

**Recall (6):**
1. What is "inference" in the context of a large language model?
2. What does tokenisation produce from a text string?
3. Why is LLM inference computationally expensive relative to, say, web serving?
4. What is the difference between a model "in training" and a model "in serving"?
5. What metric does an LLM serving system typically optimise first?
6. What is meant by a "serving system" in the context of production AI?

**Apply (8):**
7. A company serves 1 million requests per day — identify the primary cost driver
8. Given a latency requirement of <2s TTFT, classify this as latency-sensitive or throughput-sensitive
9. Identify which component of the inference stack is responsible for tokenisation
10. A request with 100 input tokens and 500 output tokens — which phase dominates GPU time?
11. Select the correct definition of "batch inference" vs "online inference"
12. Given a deployment scenario, identify whether hosted API or self-hosted is more cost-effective
13. Classify each inference stage (tokenise, prefill, decode, detokenise) as CPU-bound or GPU-bound
14. Select the correct description of what happens at each step when a user sends a chat message

**Analyse (6):**
15. Why does increasing model size disproportionately increase serving cost vs training cost?
16. Compare the latency profile of a 7B vs 70B model at the same hardware; what changes?
17. A company reports "99th percentile latency"; why is p99 more useful than mean latency?
18. Why does the inference serving problem differ from a typical database query serving problem?
19. What is the business implication of a model that is 2× slower but 10% more accurate?
20. Why do GPU prices for inference differ from GPU prices for training, and what drives that?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: the 5-stage inference pipeline in detail, the prefill/decode
distinction, compute profiles of each stage, tracing a prompt end-to-end with
timing estimates, TTFT and ITL definitions.

**Recall (6):**
1. What does the embedding layer produce from input token IDs?
2. What is TTFT (Time to First Token)?
3. What is ITL (Inter-Token Latency)?
4. Which phase processes all input tokens in parallel?
5. Which phase produces one token per forward pass?
6. What does "autoregressive" mean in the context of decode?

**Apply (8):**
7. A prompt has 200 input tokens and produces 400 output tokens — how many decode steps occur?
8. Given a TTFT of 300ms and ITL of 50ms, calculate the total generation time for 20 tokens
9. Identify which stage's output feeds directly into the embedding layer
10. Map each pipeline stage to its primary resource consumer (CPU / GPU compute / GPU memory BW)
11. Given a timing trace, identify which stage is the bottleneck
12. Select the correct description of what the KV cache stores (introduced conceptually here)
13. A user reports "first token is slow but subsequent tokens are fast" — which stage is the bottleneck?
14. Identify the correct order of the five inference pipeline stages

**Analyse (6):**
15. Why is prefill latency roughly proportional to input token count, but decode latency is not?
16. Compare "streaming" response delivery vs "wait for complete response" from a UX perspective — what does this imply about which metric matters more?
17. Why does the decode phase re-read the model weights for every token generated?
18. A team optimises TTFT but ignores ITL — in what user-facing scenario is this a mistake?
19. Why is the inference pipeline a DAG (directed acyclic graph) rather than a loop — except for decode?
20. Given two serving configs with identical throughput but different TTFT, which is preferable for an interactive chatbot and why?

---

## module-2 — Day 7 · Meet the GPU

**File:** `docs/lessons/week-02/module-2/index.md`  
**Pre-reading:** Reader 5 — Computer architecture primer (~lines 484–587) + H100 1-page spec  
**data-source label:** `Reader 5 — Computer architecture primer`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-02-m2-readiness` | `readiness` | `Reader 5 — Computer architecture primer` |
| Wrap-up | `week-02-m2-wrapup` | `wrap-up` | `Day 7 · Meet the GPU` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: GPU Anatomy (~25 min): SM, CUDA cores, HBM, PCIe, NVLink
- Part 3 — The Mental Model (~15 min): "wide and shallow" vs "narrow and deep"
- Part 4 — GPU Classes Comparison (~20 min): T4, A100, H100, 3090 — latency vs cost
- Part 5 — Hands-On: Calculate Bandwidth (~30 min): roofline teaser, memory bandwidth exercises
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — Reader 5)
Reader 5 covers: CPU architecture basics, memory hierarchy (registers, L1/L2/L3,
DRAM), GPU vs CPU core model, SIMD / SIMT execution, HBM, PCIe bandwidth limits.

**Recall (6):**
1. What does SIMT stand for and how does it differ from SIMD?
2. What is a Streaming Multiprocessor (SM)?
3. What is the memory hierarchy from fastest to slowest on a GPU?
4. What limits GPU-to-CPU data transfer speed?
5. What is HBM and why is it used on data-center GPUs instead of GDDR?
6. What does "memory bandwidth" measure — what moves, how fast?

**Apply (8):**
7. A GPU has 80 streaming multiprocessors each with 128 CUDA cores — how many CUDA cores total?
8. Given HBM bandwidth of 2 TB/s, how many GB can the GPU read in 1 millisecond?
9. Classify: reading model weights from HBM — which memory hierarchy level does this use?
10. A task needs to pass 50 GB of data from CPU to GPU — which interconnect determines throughput?
11. Select the correct description of "warp" in GPU execution
12. Given two GPUs with equal FLOPS but different HBM bandwidth, which is better for memory-bound workloads?
13. Identify what happens to GPU utilisation when all CUDA cores are waiting on HBM reads
14. Select the correct reason why CPUs cannot match GPU throughput for matrix multiplication

**Analyse (6):**
15. Why does HBM sit on the same package as the GPU die rather than on a separate DIMM?
16. Compare CPU cache hierarchy vs GPU memory hierarchy — what is the key design trade-off?
17. Why does the "wide and shallow" description fit GPUs and "narrow and deep" fit CPUs?
18. A team's model is FLOPS-limited but they upgrade to a GPU with 2× more HBM — impact?
19. Why is NVLink used between GPUs rather than PCIe for multi-GPU inference?
20. What makes the H100 significantly faster than the A100 for transformer inference specifically?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: SM anatomy, warp scheduling, HBM specs, NVLink, PCIe limits,
the mental model, GPU class comparison table (T4/A100/H100), bandwidth calculation.

**Recall (6):**
1. What are the three key specs the lesson says to memorise for the H100?
2. What is the H100's HBM bandwidth in TB/s?
3. What is PCIe Gen5 bandwidth in GB/s (approximate)?
4. What is NVLink 4 bandwidth in GB/s between two H100 GPUs?
5. What does "SM occupancy" measure?
6. Which GPU class is described as "the workhorse of cloud inference"?

**Apply (8):**
7. Given the H100 HBM bandwidth, calculate how long it takes to read 140 GB of model weights
8. Select the correct GPU class for latency-sensitive inference where cost is secondary
9. Given a memory-bandwidth-bound workload, estimate the speedup when doubling HBM bandwidth
10. Identify the bottleneck when GPU FLOPS are under-utilised but HBM reads are maxed out
11. A 70B FP16 model requires 140 GB — which GPU(s) from the comparison table can host it?
12. Calculate total CUDA cores given: 132 SMs × 128 cores/SM
13. Select the correct interpretation: "PCIe Gen5 limits CPU↔GPU transfer to ~64 GB/s"
14. Given two workloads (matrix multiply vs RNN with complex control flow), classify which suits GPU better

**Analyse (6):**
15. Why is NVLink bandwidth more than 10× PCIe — what physical property enables this?
16. A team measures 20% GPU utilisation on a transformer workload — what are the two most likely causes?
17. Compare the H100 SXM and H100 PCIe variants — when does the SXM variant matter for LLM serving?
18. Why does the lesson list "HBM bandwidth" as more important than FLOPS for LLM inference?
19. Given identical FLOPS, why does an H100 outperform an A100 for FP8 transformer ops?
20. A student says "more CUDA cores = faster inference" — what is wrong with this statement?

---

## module-3 — Day 8 · Memory Is the Bottleneck

**File:** `docs/lessons/week-02/module-3/index.md`  
**Pre-reading:** Reader 5 (memory section, ~lines 540–587) + Study Guide §A.3  
**data-source label:** `Reader 5 — Memory section + Study Guide §A.3`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-02-m3-readiness` | `readiness` | `Reader 5 — Memory section + Study Guide §A.3` |
| Wrap-up | `week-02-m3-wrapup` | `wrap-up` | `Day 8 · Memory Is the Bottleneck` |

### Part structure
- Part 1 — Pre-Reading Review (~15 min)
- Part 2 — Core Concepts: Memory Hierarchy (~20 min): registers → shared mem → L2 → HBM
- Part 3 — Deep Dive: Arithmetic Intensity (~25 min): FLOPs/byte, roofline preview
- Part 4 — Worked Example Analysis (~20 min): calculate arithmetic intensity for GEMM
- Part 5 — Hands-On: Calculate (~25 min): LLM weight-read calculations
- Part 7 — Wrap-up & Connection (~15 min)

### Readiness question outline (20 questions — Reader 5 memory section)
Reader 5 memory section covers: memory bandwidth vs compute throughput, why
bandwidth often limits AI workloads, the concept of arithmetic intensity, HBM
capacity and bandwidth characteristics.

**Recall (6):**
1. What is "arithmetic intensity" and what unit is it measured in?
2. Why is memory bandwidth often the binding constraint on GPU performance?
3. What does "memory-bound" mean for a GPU kernel?
4. How is HBM bandwidth different from DRAM bandwidth in a CPU?
5. What is the relationship between model precision (FP16 vs FP32) and memory footprint?
6. What does "memory footprint" mean for a neural network weight matrix?

**Apply (8):**
7. A kernel does 2 FLOPs per byte loaded — is it memory-bound or compute-bound on an H100?
8. Calculate the arithmetic intensity of a simple vector addition (1 FLOP, 2 bytes)
9. Given HBM bandwidth of 3.35 TB/s, how many FP16 parameters can be read per second?
10. A weight matrix is 4 GB in FP16 — how long to read it fully at 3.35 TB/s?
11. Identify which operation has higher arithmetic intensity: matrix multiply or element-wise ReLU
12. Select the correct reason why LLM decode is memory-bound rather than compute-bound
13. Given a roofline chart, identify whether a workload is in the "roofline" or "ceiling" regime
14. A team doubles HBM capacity but not bandwidth — what bottleneck do they solve? What remains?

**Analyse (6):**
15. Why is arithmetic intensity a more useful metric than raw FLOPS when analysing LLM bottlenecks?
16. Compare the memory behaviour of prefill vs decode — why does decode have lower arithmetic intensity?
17. A compute-bound workload moves to a GPU with 2× FLOPS but same memory BW — expected speedup?
18. Why does quantising from FP16 to INT8 improve throughput beyond just halving memory size?
19. What changes when you increase batch size in terms of arithmetic intensity?
20. A team observes that their workload is memory-bound at batch=1 but compute-bound at batch=64 — explain why.

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: full memory hierarchy, arithmetic intensity formula and
calculation, roofline model (preview), GEMM vs decode intensity comparison,
LLM weight-read latency calculations.

**Recall (6):**
1. What is the formula for arithmetic intensity?
2. List the GPU memory hierarchy from fastest/smallest to slowest/largest
3. What is the ridge point on a roofline plot?
4. What is the approximate arithmetic intensity of a matrix-vector multiply (GEMV)?
5. How much HBM does an H100 have?
6. What does "memory-bound kernel" mean in terms of where time is spent?

**Apply (8):**
7. GEMM with M=4096, K=4096, N=4096 in FP16 — estimate arithmetic intensity
8. Given: HBM BW = 3.35 TB/s; weight matrix = 70 GB — calculate read time in ms
9. A weight read takes 52ms on an H100 — is this consistent with the given bandwidth?
10. Classify each operation: element-wise sigmoid, large matmul, layer normalisation — memory-bound or compute-bound?
11. Select the correct interpretation of "roofline" for a given AI kernel
12. Given two kernels with arithmetic intensities of 5 FLOP/byte and 200 FLOP/byte on H100, classify each
13. Calculate how many weights an H100 can load in 10 ms at full bandwidth
14. Identify what arithmetic intensity tells you that FLOPS alone does not

**Analyse (6):**
15. Why does increasing batch size improve arithmetic intensity for matmul?
16. A team switches from FP32 to FP16 — explain the impact on arithmetic intensity and throughput
17. Compare the decode phase arithmetic intensity with GEMM — why is decode so much lower?
18. Why do modern LLM serving engines spend effort fusing kernels (combining operations)?
19. Given that HBM bandwidth is fixed, what is the only way to improve throughput on a memory-bound workload?
20. A student says "quantising to INT8 doubles throughput because it halves memory" — what is the correct nuance?

---

## module-4 — Day 9 · Compute-Bound vs Memory-Bound

**File:** `docs/lessons/week-02/module-4/index.md`  
**Pre-reading:** Reader 4 (complexity, memory, attention math, ~lines 379–483) + Study Guide §A.5 roofline subsection  
**data-source label:** `Reader 4 — Complexity, memory, attention math`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-02-m4-readiness` | `readiness` | `Reader 4 — Complexity, memory, attention math` |
| Wrap-up | `week-02-m4-wrapup` | `wrap-up` | `Day 9 · Compute-Bound vs Memory-Bound` |

### Part structure
- Part 1 — Pre-Reading Review (~10 min)
- Part 2 — Core Concepts: Roofline Model (~25 min): roofline axes, ridge point, regimes
- Part 3 — Deep Dive: Ridge Points (~15 min): H100 ridge point calculation
- Part 4 — Deep Dive: Where Kernels Sit (~20 min): GEMM, GEMV, attention, softmax
- Part 5 — Hands-On: Calculate (~25 min): place kernels on the roofline
- Part 7 — Wrap-up & Connection (~15 min)

### Readiness question outline (20 questions — Reader 4)
Reader 4 covers: O(n) vs O(n²) complexity, why attention is O(n²) in sequence
length, the concept of memory access patterns, basic attention math (QKV,
softmax), and why matrix multiplication dominates transformer compute.

**Recall (6):**
1. What is the time complexity of naive self-attention with respect to sequence length?
2. What do Q, K, V represent in the attention mechanism?
3. What operation produces the attention scores from Q and K?
4. What does the softmax function do to the attention scores?
5. What is the complexity of a matrix multiplication (GEMM) with matrices of size M×K and K×N?
6. Why is attention O(n²) in memory, not just compute?

**Apply (8):**
7. Sequence length doubles from 1K to 2K tokens — how does naive attention cost change?
8. Given attention scores of shape [seq_len, seq_len], calculate the memory required for seq_len=4096 in FP16
9. Identify which transformer operation has the highest arithmetic intensity: GEMM or softmax
10. Select the correct QKV attention formula from four candidates
11. Given matrices A (1024×512) and B (512×2048), calculate the number of multiply-accumulate operations
12. Classify: computing softmax over a 4096-length vector — memory-bound or compute-bound?
13. Which part of the transformer contributes most to O(n²) scaling with sequence length?
14. Select the correct description of why attention is more expensive at long contexts

**Analyse (6):**
15. Why does the O(n²) attention complexity matter more for inference than training?
16. Compare the memory complexity of storing KV states vs the attention scores — which grows faster with context?
17. A team increases context length from 4K to 32K — by what factor does naive attention memory usage grow?
18. Why do transformer models use multi-head attention rather than single-head attention?
19. What is the relationship between head dimension and the compute cost of a single attention head?
20. Why does the transformer architecture scale better than RNNs for long sequences in terms of parallelisability?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: roofline model axes (FLOPS/byte vs FLOPS), ridge point,
memory-bound vs compute-bound classification, kernel placement (GEMM, GEMV,
attention, softmax, layer norm), H100 roofline parameters.

**Recall (6):**
1. What are the two axes of the roofline plot?
2. What is the "ridge point" on a roofline chart?
3. Which regime is above and to the right of the ridge point?
4. What is the H100's peak FP16 FLOPS (approximate)?
5. What is the H100's memory bandwidth in TB/s?
6. Calculate the H100 ridge point (peak FLOPS ÷ peak bandwidth)?

**Apply (8):**
7. A kernel has arithmetic intensity 15 FLOP/byte — classify it on the H100 roofline
8. GEMM with large matrices has intensity ~200 FLOP/byte — compute-bound or memory-bound?
9. GEMV (matrix-vector multiply, as in decode) has intensity ~2 FLOP/byte — classify
10. Layer normalisation has intensity ~1 FLOP/byte — classify
11. Given ridge point = X FLOP/byte, identify which of three kernels (intensities 5, 50, 500) are memory-bound
12. Calculate the maximum achievable throughput for a memory-bound kernel at 0.5 FLOP/byte on H100
13. Select the correct roofline regime for FlashAttention (fused tiling reduces memory traffic)
14. A team fuses two memory-bound kernels into one — how does this affect arithmetic intensity?

**Analyse (6):**
15. Why is the roofline model useful for predicting the speedup limit of a hardware upgrade?
16. A compute-bound workload moves to a GPU with 2× HBM bandwidth but same FLOPS — impact?
17. Explain why decode is permanently in the memory-bound regime regardless of batch size (at batch=1)
18. Why does increasing batch size eventually push a workload from memory-bound to compute-bound?
19. A team claims their new kernel is "2× faster" — what additional information is needed to verify this on the roofline?
20. Compare the roofline positions of prefill (large batch, long seq) vs decode (batch=1) for the same model.

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Read Reader 1, 5, 4 sections in `Inference_Engineering_Pre_Lecture_Reading.md`
- [ ] module-1 (Day 6): Reader 1 readiness + pipeline wrap-up
- [ ] module-2 (Day 7): Reader 5 architecture readiness + GPU anatomy wrap-up
- [ ] module-3 (Day 8): Reader 5 memory readiness + arithmetic intensity wrap-up
- [ ] module-4 (Day 9): Reader 4 readiness + roofline wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day N · <title>`
- [ ] After all 4 modules: `python3 scripts/audit_lessons.py` — 0 violations
