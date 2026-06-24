# Widget Conversion Plan — Week 04 (Days 17–19)

**Branch:** `feat/content-fortification`  
**Note:** Day 16 (module-1 · Tensor Parallelism) is the **reference implementation** — already complete. Do NOT modify it.  
**Pre-reading source:** `planning/source-material/Inference Engineering/Inference_Engineering_Pre_Lecture_Reading.md`  
**Readers used:** Reader 8 (~lines 853–956) for Day 17; Reader 6 (~lines 588–725) for Days 18–19  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Readers | Notes |
|--------|-----|-------|---------|-------|
| module-1 | 16 | Tensor Parallelism | Reader 8 | **REFERENCE — skip** |
| module-2 | 17 | Pipeline & Expert Parallelism | Reader 8 | |
| module-3 | 18 | Speculative Decoding | Reader 6 | |
| module-4 | 19 | Serving Engines & Continuous Batching | Reader 6 | |

All three target lessons already have `## Part 1 — Pre-Reading Review + Readiness Check` and `## Part 7 — Wrap-up & Connection`. No structural changes needed.

---

## module-2 — Day 17 · Pipeline & Expert Parallelism

**File:** `docs/lessons/week-04/module-2/index.md`  
**Pre-reading:** Reader 8 — Parallel computing primer + Mixtral MoE architecture summary  
**data-source label:** `Reader 8 — Parallel Computing Primer`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-04-m2-readiness` | `readiness` | `Reader 8 — Parallel Computing Primer` |
| Wrap-up | `week-04-m2-wrapup` | `wrap-up` | `Day 17 · Pipeline & Expert Parallelism` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core Concept: Pipeline Parallelism (~20 min): depth-wise sharding, microbatches, bubbles
- Part 3 — Deep Dive: Bubbles & TP vs PP (~15 min): bubble fraction, interleaved scheduling
- Part 4 — Core Concept: Expert Parallelism (~20 min): MoE routing, expert sharding, all-to-all
- Part 5 — Hands-On: Config Design (~30 min): choose parallelism strategy for given hardware
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — Reader 8: parallel computing + MoE)
Reader 8 covers: why parallelism is needed beyond a single node, pipeline
parallelism concept (depth-wise), Mixture-of-Experts architecture, expert
routing, all-to-all communication.

**Recall (6):**
1. What does "pipeline parallelism" split — the model's width or depth?
2. What is a "pipeline bubble" in the context of PP?
3. What is a Mixture-of-Experts (MoE) model?
4. What is the "top-k" routing in a MoE model?
5. What communication primitive does Expert Parallelism use to route tokens to experts?
6. When does pipeline parallelism become necessary vs tensor parallelism?

**Apply (8):**
7. A 400B parameter model needs to run across 4 nodes of 8 H100s each — which parallelism dimension spans nodes?
8. Given a 4-stage pipeline and a microbatch of 8, calculate the pipeline bubble fraction
9. A MoE model has 8 experts with top-2 routing — what fraction of experts process each token?
10. Identify which parallelism dimension creates all-to-all communication: TP, PP, or EP?
11. Select the correct analogy for pipeline parallelism: assembly line or forking a process?
12. Given pipeline stages 1–4 each taking 10ms, with no microbatching, what is the bubble fraction?
13. Classify: reducing pipeline bubble by increasing microbatch count — what does this sacrifice?
14. A MoE layer has 64 experts; only 2 are active per token — what is the computation sparsity?

**Analyse (6):**
15. Why is PP preferred over TP for cross-node parallelism?
16. Compare pipeline parallelism and tensor parallelism in terms of communication overhead per layer
17. A team uses PP=4, TP=8 — at what point does cross-node communication become the bottleneck?
18. Why does EP require all-to-all communication rather than the all-reduce used by TP?
19. Compare MoE and dense models on a per-token compute basis — what changes and what stays the same?
20. Why does microbatching reduce the pipeline bubble, and what is the theoretical minimum bubble fraction?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: pipeline stages + microbatches, bubble fraction formula,
interleaved scheduling, MoE routing mechanics, EP all-to-all cost, config
design exercise.

**Recall (6):**
1. What is the bubble fraction formula for pipeline parallelism?
2. What does interleaved pipeline scheduling do to reduce bubbles?
3. Name the two types of communication in a hybrid TP+PP+EP setup
4. What is the "capacity factor" in MoE routing?
5. What happens when a MoE expert receives more tokens than its capacity?
6. In what scenario does PP outperform TP for serving a given model?

**Apply (8):**
7. PP=4 stages, 16 microbatches — calculate bubble fraction
8. PP=4 stages, 4 microbatches — calculate bubble fraction; compare to above
9. Interleaved scheduling with 2 chunks per stage — what is the new bubble fraction formula?
10. A MoE model has 16 experts, top-2 routing, capacity_factor=1.2 — calculate max tokens per expert
11. Given TP=8 within node + PP=4 across nodes, calculate total GPUs used
12. Select the correct hardware topology for a TP=8, PP=4 deployment on 4 nodes of 8 GPUs each
13. Classify: EP all-to-all communication — is it more expensive than TP all-reduce per layer?
14. A team has budget for 2 nodes of 8 H100s; model needs 4 nodes with PP=4. What config fits in 2 nodes?

**Analyse (6):**
15. Compare the latency impact of TP vs PP on a single request (not aggregate throughput)
16. A pipeline with low bubble fraction still shows poor GPU utilisation — what else could cause this?
17. Why do large-scale production deployments typically use TP within node + PP across nodes?
18. Compare an 8×70B dense serving config with a 1×Mixtral-8×7B MoE config — compute per token?
19. Why does expert load imbalance in MoE harm throughput even when average utilisation looks good?
20. A team switches from TP=8 to PP=8 for a 70B model — what trade-off are they accepting?

---

## module-3 — Day 18 · Speculative Decoding

**File:** `docs/lessons/week-04/module-3/index.md`  
**Pre-reading:** Reader 6 — Software stack for ML (speculative decoding section, ~lines 588–725)  
**data-source label:** `Reader 6 — Software Stack for ML`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-04-m3-readiness` | `readiness` | `Reader 6 — Software Stack for ML` |
| Wrap-up | `week-04-m3-wrapup` | `wrap-up` | `Day 18 · Speculative Decoding` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core Concept: The Wasted-Compute Problem (~15 min): decode underutilises GPU compute
- Part 3 — Core Concept: The Speculative Trick (~20 min): draft model + verifier, accept/reject
- Part 4 — Deep Dive: Why It's Faster + Bit-Exactness (~15 min): parallel verification, mathematical guarantee
- Part 5 — Hands-On: Calculations + Tradeoffs (~30 min): mean accepted tokens (α), expected speedup
- Part 7 — Wrap-up & Connection (~15 min)

### Readiness question outline (20 questions — Reader 6 speculative decoding section)
Reader 6 covers: why decode underutilises GPU, the concept of speculative
execution, draft model and verifier, acceptance rate definition, bit-exactness
guarantee.

**Recall (6):**
1. Why is standard autoregressive decode considered "wasteful" of GPU compute?
2. What is a "draft model" in speculative decoding?
3. What does the verifier (large model) do in one forward pass during speculative decoding?
4. What is the acceptance rate (α) in speculative decoding?
5. What guarantee does speculative decoding provide about output distribution?
6. What is the role of the "bonus token" in the rejection sampling algorithm?

**Apply (8):**
7. A draft model proposes 5 tokens; all are accepted — how many verifier forward passes were needed?
8. Given α=0.8 and k=5 draft tokens, calculate the expected number of accepted tokens per step
9. Identify which model must be larger: the draft model or the verifier
10. Select the correct description of what happens when a draft token is rejected
11. A team uses speculative decoding with k=4 — what is the worst-case scenario per verifier pass?
12. Given expected speedup formula, calculate speedup for α=0.7, k=5, verification overhead=1.2×
13. Classify: speculative decoding — does it change the probability distribution of outputs?
14. Select the correct hardware requirement for speculative decoding: same GPU, more GPUs, or less GPU?

**Analyse (6):**
15. Why does speculative decoding help more for memory-bound decode than for prefill?
16. Compare speculative decoding and batching as throughput-improvement strategies — what does each sacrifice?
17. A team uses a draft model that is 10× smaller — what is the trade-off in terms of quality and speed?
18. Why is bit-exactness (identical distribution guarantee) important for production deployments?
19. Speculative decoding has higher speedup on greedy decoding than sampling — explain why
20. A team tries speculative decoding but observes no speedup — what are the two most likely causes?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: GPU underutilisation in decode, draft model proposal loop,
verifier accept/reject mechanics, bit-exactness proof, α formula, expected
speedup calculation, practical tradeoffs.

**Recall (6):**
1. What is the formula for expected accepted tokens per speculative step?
2. What does "bit-exact" mean in the context of speculative decoding's output?
3. What is the minimum number of verifier forward passes per speculative step?
4. When is the bonus token generated?
5. What determines how many draft tokens (k) to use in practice?
6. Under what condition does speculative decoding degrade to standard autoregressive decode?

**Apply (8):**
7. α=0.9, k=4: calculate expected accepted tokens per step
8. α=0.6, k=5: calculate expected accepted tokens per step
9. Compare: standard decode (1 token/pass) vs speculative with α=0.8, k=5 — expected throughput ratio
10. A draft model proposes ["the", "cat", "sat"]; verifier accepts "the", rejects "cat" — what is output?
11. Given overhead of 1.1× per verifier pass and α=0.85, k=5 — calculate net speedup
12. Select the correct reason why speculative decoding is more effective for longer output sequences
13. Identify the maximum possible speedup with perfect acceptance rate (α=1.0) and k draft tokens
14. A team increases k from 4 to 8 but α drops from 0.85 to 0.70 — calculate whether this helps

**Analyse (6):**
15. Why does speculative decoding work best with greedy decoding (temperature=0)?
16. Compare the memory requirements of speculative decoding vs standard decoding — what additional overhead exists?
17. A team notices speculative decoding speedup drops from 2.5× to 1.3× as batch size increases — explain why
18. Why does the draft model need to be "aligned" with the verifier for high acceptance rates?
19. Compare speculative decoding and continuous batching as serving optimisations — are they complementary or competing?
20. A team's draft model has α=0.95 for English but α=0.40 for code — explain this gap and its implications

---

## module-4 — Day 19 · Serving Engines & Continuous Batching

**File:** `docs/lessons/week-04/module-4/index.md`  
**Pre-reading:** Reader 6 — Software stack for ML (continuous batching + vLLM, ~lines 588–725)  
**data-source label:** `Reader 6 — Software Stack for ML`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-04-m4-readiness` | `readiness` | `Reader 6 — Software Stack for ML` |
| Wrap-up | `week-04-m4-wrapup` | `wrap-up` | `Day 19 · Serving Engines & Continuous Batching` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core Concept: Static vs Continuous Batching (~20 min): head-of-line blocking, iteration-level scheduling
- Part 3 — Deep Dive: Why This Needs PagedAttention (~15 min): dynamic KV allocation
- Part 4 — Core Concept: Serving Engines Comparison (~20 min): vLLM, TGI, TensorRT-LLM, SGLang
- Part 5 — Hands-On: Engine Selection + vLLM Quickstart (~30 min)
- Part 7 — Wrap-up & Connection (~10 min)

### Readiness question outline (20 questions — Reader 6 serving engine section)
Reader 6 covers: what a serving engine is, static batching limitations,
continuous batching concept, PagedAttention dependency, overview of major
engines (vLLM, TGI).

**Recall (6):**
1. What is "static batching" and what problem does it create for LLM serving?
2. What is "continuous batching" (also called iteration-level batching)?
3. What is "head-of-line blocking" in static batching?
4. Why does continuous batching require PagedAttention?
5. Name two open-source LLM serving engines that implement continuous batching
6. What is the primary metric that continuous batching improves over static batching?

**Apply (8):**
7. Static batching with 8 requests: one request finishes in 10ms, others take 100ms — what is the GPU idle time percentage?
8. Continuous batching: request A finishes early — when can a new request join the batch?
9. Identify the component of a serving engine that schedules which requests run in each iteration
10. Select the correct description of what vLLM's PagedAttention enables that static KV allocation does not
11. A team uses static batching and observes 40% GPU underutilisation — likely cause?
12. Given 16 concurrent requests with variable lengths, classify which batching strategy keeps GPU busy
13. Identify what "iteration-level scheduling" means in terms of when decisions are made
14. Select the correct statement about continuous batching and request isolation (KV cache independence)

**Analyse (6):**
15. Why does continuous batching improve throughput by 5–10× over static batching in practice?
16. Compare vLLM and TensorRT-LLM on the trade-off between ease of deployment and raw performance
17. Why does continuous batching require the serving engine to manage KV memory dynamically?
18. A team switches from static to continuous batching — what changes about their GPU memory management?
19. Compare head-of-line blocking in LLM serving vs HTTP request queuing — what makes LLM serving worse?
20. Why is continuous batching the default in modern serving engines rather than an optional feature?

### Wrap-up question outline (20 questions — Parts 2–5)
Parts 2–5 cover: static vs continuous batching mechanics, head-of-line blocking
analysis, PagedAttention dependency, serving engine comparison table
(vLLM/TGI/TRT-LLM/SGLang), engine selection criteria, vLLM quickstart.

**Recall (6):**
1. What does "iteration-level scheduling" mean in continuous batching?
2. Which serving engine is described as "easiest to get started with"?
3. Which engine has the highest raw performance but most complex deployment?
4. What does vLLM use to manage KV cache memory dynamically?
5. What are the two primary criteria for choosing a serving engine per this lesson?
6. What is the throughput improvement range cited for continuous vs static batching?

**Apply (8):**
7. A team needs to serve an open-source 70B model with minimal setup — which engine does the lesson recommend?
8. A team needs maximum throughput for a high-volume production deployment — which engine?
9. Given the engine comparison table, identify which engine supports the most hardware backends
10. Select the correct vLLM launch command for a Llama model with tensor parallelism tp=4
11. Identify what happens in vLLM when the KV cache pool is exhausted (all pages occupied)
12. A team observes that adding more concurrent users beyond 32 does not improve throughput — explain
13. Select the correct description of how continuous batching handles a request that finishes mid-batch
14. Given a latency SLO of <200ms TTFT, identify which batching strategy risks violating it and why

**Analyse (6):**
15. Why does switching from static to continuous batching require no model weight changes?
16. Compare the operator overhead of managing a static batch vs a dynamic batch in continuous batching
17. A team benchmarks vLLM and TGI on the same hardware — vLLM is faster but uses 2× more GPU memory. Explain.
18. Why is continuous batching less beneficial for very short outputs (e.g., classification) than for long generations?
19. Compare the serving engine selection decision for a research team vs a production team — what differs?
20. A team reports that enabling continuous batching increased p99 latency while improving mean throughput — explain this trade-off.

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Note: module-1 (Day 16) is the reference — do NOT modify
- [ ] Locate Reader 8 and Reader 6 sections in `Inference_Engineering_Pre_Lecture_Reading.md`
- [ ] module-2 (Day 17): Reader 8 readiness + PP/EP wrap-up
- [ ] module-3 (Day 18): Reader 6 readiness + speculative decoding wrap-up
- [ ] module-4 (Day 19): Reader 6 readiness + serving engines wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`
- [ ] After all 3 modules: `python3 scripts/audit_lessons.py` — 0 violations
