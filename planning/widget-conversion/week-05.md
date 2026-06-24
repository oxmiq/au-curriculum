# Widget Conversion Plan — Week 05 (Days 21–24)

**Branch:** `feat/content-fortification`  
**Pre-reading source:** `planning/source-material/Inference Engineering/Inference_Engineering_Pre_Lecture_Reading.md`  
**Reader used:** Reader 10 (~lines 1053–1232) for all four modules  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## CRITICAL: Part 1 restructure required for all four lessons

All four week-05 lessons currently lack `## Part 1 — Pre-Reading Review + Readiness Check`.
They begin directly with a core-content Part 1 (e.g., "Why Metrics Matter"). Before inserting
any widget, each lesson needs the following structural change:

1. **Prepend** a new `## Part 1 — Pre-Reading Review + Readiness Check · 15 min` section
   (containing only the readiness widget — no other content)
2. **Renumber** all existing Part headings: old Part 1 → Part 2, old Part 2 → Part 3, …,
   old Part N → Part N+1. Part 7 (Wrap-up) will move up by one accordingly.
3. **Update** the lesson-plan table at the top of the lesson to reflect the new part numbers
   and add the Pre-Reading Review row.

Do this restructure first, then insert both widgets.

### Original → new Part numbering table

| Lesson | Old Part 1 title | Old last Part | After restructure |
|--------|-----------------|--------------|-------------------|
| module-1 | Why Metrics Matter | Part 5 + Part 7 | Parts 2–6 + Part 7 (was 5) = Parts 1–7 |
| module-2 | Why Production Matters | Part 5 + Part 7 | Parts 2–6 + Part 7 |
| module-3 | Why Evaluation Matters | Part 5 + Part 7 | Parts 2–6 + Part 7 |
| module-4 | The Cost Formula | Part 5 + Part 7 | Parts 2–6 + Part 7 |

After renumbering, all four lessons will have the standard B7 shape:
Part 1 (readiness) + Parts 2–6 (content) + Part 7 (wrap-up).

---

## Week overview

| Module | Day | Title | Reader 10 sections | data-source |
|--------|-----|-------|--------------------|-------------|
| module-1 | 21 | Metrics That Matter | TTFT, ITL, throughput, percentiles | `Reader 10 — Distributed Systems for Production` |
| module-2 | 22 | Production Patterns | Load balancing, scaling, deployment patterns | `Reader 10 — Distributed Systems for Production` |
| module-3 | 23 | Evaluation & Quality | Eval pipelines, quality metrics, regression | `Reader 10 — Distributed Systems for Production` |
| module-4 | 24 | Cost & Economics | $/token, GPU utilisation, ROI | `Reader 10 — Distributed Systems for Production` |

---

## module-1 — Day 21 · Metrics That Matter

**File:** `docs/lessons/week-05/module-1/index.md`  
**Pre-reading:** Reader 10 — production metrics sections  
**data-source label:** `Reader 10 — Distributed Systems for Production`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-05-m1-readiness` | `readiness` | `Reader 10 — Distributed Systems for Production` |
| Wrap-up | `week-05-m1-wrapup` | `wrap-up` | `Day 21 · Metrics That Matter` |

### Part structure (after restructure)
- **Part 1 (NEW)** — Pre-Reading Review + Readiness Check (~15 min)
- **Part 2** (was Part 1) — Why Metrics Matter
- **Part 3** (was Part 2) — Deep Dive: Metric Vocabulary (TTFT, ITL, throughput, p50/p99)
- **Part 4** (was Part 3) — Percentile Calculations
- **Part 5** (was Part 4) — Latency vs Throughput Tradeoff
- **Part 6** (was Part 5) — Discussion: Goodhart Traps
- **Part 7** — Wrap-up & Connection (unchanged number)

### Readiness question outline (20 questions — Reader 10 metrics section)
Reader 10 covers: what production metrics matter for LLM serving, TTFT/ITL
definitions, percentile statistics (p50/p95/p99), the difference between latency
and throughput, why average is misleading.

**Recall (6):**
1. What does TTFT measure in an LLM serving system?
2. What does ITL (inter-token latency) measure?
3. What is throughput in the context of LLM serving?
4. What does p99 latency mean?
5. Why is average latency a misleading metric for production systems?
6. What is the "Goodhart's Law" problem as it applies to AI system metrics?

**Apply (8):**
7. A system reports TTFT p99=500ms and TTFT mean=80ms — what does this gap indicate?
8. ITL p50=20ms, p99=200ms: a user wants <100ms response — what SLO should they target?
9. Given TTFT=300ms and ITL=25ms, calculate total response time for a 40-token output
10. A serving system processes 100 requests/minute — is this a latency or throughput metric?
11. Identify which metric is most relevant for a streaming chat interface: TTFT or throughput
12. Select the correct reason why p99 is more actionable than mean for production SLOs
13. A team improves mean TTFT but p99 TTFT worsens — what has happened in the tail?
14. Classify: "tokens per second" — is this a latency or throughput metric?

**Analyse (6):**
15. Why is optimising for throughput sometimes in tension with optimising for latency?
16. Compare the user experience impact of high TTFT vs high ITL for a streaming chat product
17. A team chooses to measure p50 TTFT as their SLO — what class of users are they ignoring?
18. Why does Goodhart's Law apply when teams optimise directly for their measured metric?
19. Compare a batch processing use case vs an interactive chat use case — which metrics matter most?
20. A system serves both real-time chat and async summarisation — should they share a single SLO?

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: why metrics matter argument, TTFT/ITL/throughput vocabulary,
percentile calculation exercises, latency vs throughput trade-off diagram,
Goodhart traps discussion.

**Recall (6):**
1. Define TTFT and ITL in your own words
2. What is the formula for total response time given TTFT, ITL, and output tokens?
3. What does "throughput" measure that latency does not?
4. What percentile is recommended for production SLOs in this lesson?
5. Give one example of a Goodhart trap in LLM serving
6. What is the latency-throughput trade-off illustrated in Part 5?

**Apply (8):**
7. System A: TTFT p99=150ms, ITL p99=30ms. System B: TTFT p99=80ms, ITL p99=60ms. 20-token response — which feels faster to user?
8. Calculate p99 response time for a 100-token output with TTFT p99=200ms, ITL p99=25ms
9. A team increases batch size — TTFT worsens, ITL improves. Explain the trade-off
10. Given a Goodhart trap example from Part 6, identify the perverse incentive
11. Select the metric most relevant for billing a per-token API service
12. Identify which metric worsens first as concurrent users increase: TTFT or ITL?
13. Calculate: 1000 tokens/second throughput across 50 concurrent users — what is per-user ITL?
14. Select the correct statement about why p50 and p99 diverge under load

**Analyse (6):**
15. Why do latency and throughput trade off against each other in a serving system?
16. A team uses token throughput as their headline metric — what failure modes does this hide?
17. Compare real-time streaming vs batch generation — which needs a tighter TTFT SLO?
18. Explain why a Goodhart trap in serving metrics leads to poor product outcomes
19. Why does p99 latency worsen faster than p50 latency as the system approaches capacity?
20. A team's TTFT p99 is excellent but users complain the experience feels slow — what metric is likely the culprit?

---

## module-2 — Day 22 · Production Patterns

**File:** `docs/lessons/week-05/module-2/index.md`  
**Pre-reading:** Reader 10 — production patterns and scaling  
**data-source label:** `Reader 10 — Distributed Systems for Production`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-05-m2-readiness` | `readiness` | `Reader 10 — Distributed Systems for Production` |
| Wrap-up | `week-05-m2-wrapup` | `wrap-up` | `Day 22 · Production Patterns` |

### Part structure (after restructure)
- **Part 1 (NEW)** — Pre-Reading Review + Readiness Check (~15 min)
- **Part 2** (was Part 1) — Why Production Matters
- **Part 3** (was Part 2) — Deep Dive: Load Balancing for LLMs
- **Part 4** (was Part 3) — Core: Scaling Patterns (horizontal + vertical)
- **Part 5** (was Part 4) — Hands-On: Deployment Pattern Selection
- **Part 6** (was Part 5) — Case Study: Production Incident
- **Part 7** — Wrap-up & Connection

### Readiness question outline (20 questions — Reader 10 production patterns)
Reader 10 covers: why production serving differs from research, load balancing
strategies, horizontal vs vertical scaling, availability patterns, deployment
models (dedicated vs shared GPU).

**Recall (6):**
1. What is "load balancing" in an LLM serving context?
2. What is the difference between horizontal and vertical scaling?
3. What is an availability zone in cloud infrastructure?
4. What is a "dedicated" vs "shared" GPU deployment pattern?
5. What does "autoscaling" mean for an LLM serving cluster?
6. What problem does load balancing solve when multiple serving instances exist?

**Apply (8):**
7. A serving cluster has 3 nodes; one goes down — what must load balancing guarantee?
8. Identify which scaling type is limited by the maximum GPU available: horizontal or vertical
9. A team deploys one 8-GPU node vs eight 1-GPU nodes — identify the trade-offs
10. Select the correct load balancing strategy when requests have variable-length KV caches
11. A cloud LLM service reports 99.9% availability — how many minutes of downtime per year?
12. Classify: "adding more GPU nodes behind a load balancer" — horizontal or vertical scaling?
13. Given a serving system with p99 TTFT = 800ms at peak, identify the most likely production cause
14. Select the correct reason why LLM-aware load balancing differs from standard HTTP load balancing

**Analyse (6):**
15. Why is standard round-robin load balancing suboptimal for LLM serving?
16. Compare dedicated GPU deployment vs shared multi-tenant deployment on cost and performance
17. A production incident trace shows 3× latency spike every 5 minutes — identify likely causes
18. Why does horizontal scaling work better for stateless serving than for stateful applications?
19. Compare rolling deployment vs blue-green deployment for a model version update
20. A team reduces their GPU count by 30% to cut costs — at what utilisation level does this hurt SLOs?

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: production requirements, load balancing strategies for LLMs
(KV-cache-aware routing), horizontal vs vertical scaling, deployment patterns,
case study analysis of a production incident.

**Recall (6):**
1. What is "KV-cache-aware" load balancing?
2. Name two load balancing strategies covered in Part 3
3. When does vertical scaling hit its practical ceiling?
4. What is the primary advantage of a dedicated GPU deployment?
5. What is the primary advantage of a shared GPU deployment?
6. In the production incident case study, what was the root cause?

**Apply (8):**
7. A load balancer routes all long-context requests to node-1 and short requests to node-2 — what problem does this create?
8. Given 10 serving nodes, the team adds 5 more — throughput increases by only 30%. Explain why.
9. Select the correct load balancing strategy for prefix-caching to work across requests
10. Identify the monitoring metric that would have caught the production incident early
11. A team switches from vertical to horizontal scaling — what new failure mode is introduced?
12. Calculate: 10 GPUs each handling 100 req/min → 15 GPUs. If requests grow by 60%, do SLOs hold?
13. Select the correct response to a sudden 5× traffic spike: autoscale or shed load?
14. Identify what "warm standby" means in a serving deployment

**Analyse (6):**
15. Why is LLM-aware load balancing an open research problem while HTTP load balancing is solved?
16. Compare blue-green and canary deployment strategies for a model update
17. A team's autoscaling is too slow — 3-minute scale-up time causes SLO violations during traffic spikes. What is the fix?
18. Why does prefix caching create "stickiness" that conflicts with standard load balancing?
19. A team running at 80% GPU utilisation adds 25% more traffic — at what point do SLOs break?
20. Compare the operational cost of running a 24/7 dedicated serving cluster vs a serverless GPU API

---

## module-3 — Day 23 · Evaluation & Quality

**File:** `docs/lessons/week-05/module-3/index.md`  
**Pre-reading:** Reader 10 — evaluation and quality sections  
**data-source label:** `Reader 10 — Distributed Systems for Production`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-05-m3-readiness` | `readiness` | `Reader 10 — Distributed Systems for Production` |
| Wrap-up | `week-05-m3-wrapup` | `wrap-up` | `Day 23 · Evaluation & Quality` |

### Part structure (after restructure)
- **Part 1 (NEW)** — Pre-Reading Review + Readiness Check (~15 min)
- **Part 2** (was Part 1) — Why Evaluation Matters
- **Part 3** (was Part 2) — Deep Dive: Benchmark vs Production Quality
- **Part 4** (was Part 3) — Core: Eval Pipeline Design
- **Part 5** (was Part 4) — Hands-On: Build a Mini Eval Suite
- **Part 6** (was Part 5) — Deep Dive: Regression Testing & Regressions
- **Part 7** — Wrap-up & Connection

### Readiness question outline (20 questions — Reader 10 evaluation section)
Reader 10 covers: why offline benchmarks can mislead, what an eval pipeline
is, types of quality metrics (automated vs human), regression testing concept,
distribution shift.

**Recall (6):**
1. What is the difference between an offline benchmark and a production eval?
2. What is "MMLU" and what does it measure?
3. What is a "regression" in the context of model evaluation?
4. What is "LLM-as-judge" evaluation?
5. Why do offline benchmarks often overstate production quality?
6. What is "distribution shift" between a benchmark and production traffic?

**Apply (8):**
7. A model scores 85% on MMLU but users report poor quality — identify the likely cause
8. A team switches model versions; old eval suite passes but production users complain — what's missing?
9. Identify which evaluation approach catches regressions fastest: daily benchmark runs or A/B testing
10. Select the correct description of "task-specific eval" vs "general benchmark"
11. A team uses LLM-as-judge for their eval pipeline — identify one failure mode of this approach
12. Given a production eval suite with 100 test cases, identify what "regression detection" checks
13. Classify: MMLU, HumanEval, MT-Bench — which is most relevant for a coding assistant product?
14. Select the correct reason why production quality drifts even when the model is unchanged

**Analyse (6):**
15. Why is an eval suite that matches production distribution more valuable than a standardised benchmark?
16. Compare human evaluation and automated (LLM-as-judge) evaluation on cost, speed, and reliability
17. A model improves TTFT by 30% but LLM-as-judge score drops 5% — how should the team prioritise?
18. Why does distribution shift cause offline evals to become less accurate predictors over time?
19. A team uses the same eval set for 6 months — explain why "eval set contamination" is a risk
20. Compare the risk of under-evaluating vs over-evaluating quality when deploying model updates

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: offline vs production eval distinction, benchmark limitations,
eval pipeline design (test set + judge + reporting), mini eval suite exercise,
regression testing workflow.

**Recall (6):**
1. What are the three components of an eval pipeline per this lesson?
2. What is "eval set contamination"?
3. What is the recommended minimum eval suite size for a production serving system?
4. Name two automated quality metrics covered in this lesson
5. What is the difference between regression and degradation in model quality?
6. What does "golden set" mean in the context of regression testing?

**Apply (8):**
7. Design a 5-prompt eval suite for a code generation assistant (identify the 5 test categories)
8. A team uses p95 latency AND LLM-as-judge score as dual SLOs — identify the advantage
9. Select the correct cadence for re-running a regression suite: per commit, weekly, or monthly?
10. Given a golden set of 50 test cases, a new model scores 48/50 but old scored 50/50 — should this block deployment?
11. Identify what "soft fail" vs "hard fail" means in an eval pipeline
12. A team adds 20 new test cases from recent production failures — what type of eval improvement is this?
13. Select the correct description of why "eval-driven development" helps avoid quality regressions
14. Calculate: LLM-as-judge rates 45/50 responses as "good" — what is the pass rate and does it meet a 90% SLO?

**Analyse (6):**
15. Why is a task-specific eval suite more valuable than MMLU for a domain-specific product?
16. Compare the cost and latency of LLM-as-judge vs human evaluation for continuous monitoring
17. A team discovers their eval suite was "optimised against" by the model — what went wrong?
18. Why should regression tests include examples of recent failures, not just original passing cases?
19. A team runs evals on 1% of production traffic — what risks does this introduce vs a golden set?
20. Compare the evaluation needs of a research deployment vs a customer-facing production system

---

## module-4 — Day 24 · Cost & Economics

**File:** `docs/lessons/week-05/module-4/index.md`  
**Pre-reading:** Reader 10 — cost and economics of LLM deployment  
**data-source label:** `Reader 10 — Distributed Systems for Production`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-05-m4-readiness` | `readiness` | `Reader 10 — Distributed Systems for Production` |
| Wrap-up | `week-05-m4-wrapup` | `wrap-up` | `Day 24 · Cost & Economics` |

### Part structure (after restructure)
- **Part 1 (NEW)** — Pre-Reading Review + Readiness Check (~15 min)
- **Part 2** (was Part 1) — The Cost Formula
- **Part 3** (was Part 2) — Deep Dive: Utilisation & Efficiency
- **Part 4** (was Part 3) — Hands-On: Cost per Token Calculation
- **Part 5** (was Part 4) — Hands-On: ROI Analysis
- **Part 6** (was Part 5) — Discussion: Build vs Buy
- **Part 7** — Wrap-up & Connection

### Readiness question outline (20 questions — Reader 10 cost section)
Reader 10 covers: how to calculate $/token, GPU utilisation impact on cost,
the build-vs-buy decision, API vs self-hosting trade-offs, hidden costs of
production deployment.

**Recall (6):**
1. What is the formula for cost per token in a self-hosted deployment?
2. What is "GPU utilisation" and what does 100% utilisation mean?
3. What are the three main cost components in a self-hosted serving deployment?
4. What is "MFU" (model FLOP utilisation)?
5. Why does API pricing (per-token) appear more expensive than self-hosting at scale?
6. At what request volume does self-hosting typically break even with API pricing?

**Apply (8):**
7. GPU costs $3/hr, 40 requests/hr, each generating 200 tokens — calculate $/1K tokens
8. GPU utilisation improves from 40% to 80% — what happens to $/token?
9. A team uses a cloud API at $0.002/1K tokens vs self-hosting at $0.0005/1K at 1M tokens/day — calculate monthly savings
10. Identify which cost component grows with traffic: GPU rent, model size, or software licensing?
11. Select the correct description of "hidden costs" that self-hosting teams often underestimate
12. Given utilisation=60%, GPU cost=$2/hr, output=500 tokens/hr — calculate cost per token
13. Classify: engineering time to maintain a self-hosted serving stack — is this counted in $/token?
14. Select the correct break-even analysis approach for the build-vs-buy decision

**Analyse (6):**
15. Why does low GPU utilisation make self-hosting more expensive than the raw hardware cost suggests?
16. Compare the risk profile of API pricing vs self-hosting for a startup vs an enterprise
17. A team achieves 3× better throughput through optimisation — how does this affect $/token?
18. Why is "total cost of ownership" (TCO) a better metric than "GPU rent cost" for the build/buy decision?
19. A team's product fails financially despite good technical performance — what economic analysis was missing?
20. Compare the cost structure of a batch processing workload vs a real-time chat workload on the same hardware

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: cost formula (GPU cost / (tokens/hr × utilisation)), utilisation
efficiency analysis, cost-per-token calculations, ROI analysis exercise,
build-vs-buy decision framework.

**Recall (6):**
1. What is the cost-per-token formula?
2. What is the "break-even volume" in the build-vs-buy framework?
3. What does improving GPU utilisation from 50% to 80% do to $/token?
4. Name two "hidden costs" of self-hosting discussed in Part 6
5. At what monthly token volume did the lesson's worked example show self-hosting breaking even?
6. What is the ROI formula per this lesson?

**Apply (8):**
7. GPU = $4/hr, throughput = 2000 tokens/min at 70% utilisation — calculate $/1K tokens
8. A team reduces serving cost by 40% via quantisation — if monthly API spend was $50K, what is the new cost?
9. Calculate ROI for a $200K/yr serving investment that saves $350K/yr in API costs
10. Identify the correct break-even point for a 100M tokens/month workload at API price=$0.003 vs self-hosting cost=$0.0008/1K
11. Given GPU utilisation doubles (from 30% to 60%), calculate the $/token improvement
12. Select the correct classification: if a model update doubles quality but costs 3× more — how to analyse?
13. A team runs at 20% GPU utilisation — identify the correct action to improve cost efficiency
14. Given a startup's API bill of $15K/month, identify at what monthly volume self-hosting at $0.0005/1K tokens becomes cheaper

**Analyse (6):**
15. Why does utilisation have a multiplicative effect on cost efficiency?
16. Compare the cost sensitivity of a chatbot (low tokens/response) vs a summarisation service (high tokens/response)
17. A team achieves 2× throughput through continuous batching — what happens to $/token and $/GPU-hr?
18. Why is the build-vs-buy decision path-dependent (i.e., it depends on where you are now, not just future cost)?
19. Compare the economic risk of over-provisioning GPUs vs under-provisioning GPUs for a production service
20. A team's product is technically successful but economically unviable at the current token volume — what are the three paths forward?

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Confirm Reader 10 line range in `Inference_Engineering_Pre_Lecture_Reading.md`
- [ ] For EACH module: perform Part-1 restructure FIRST, then insert widgets
  - [ ] Prepend `## Part 1 — Pre-Reading Review + Readiness Check · 15 min`
  - [ ] Renumber old Part 1 → 2, Part 2 → 3, …, Part 5 → 6 (Part 7 stays Part 7)
  - [ ] Update lesson-plan table at top of file
- [ ] module-1 (Day 21): Reader 10 readiness + metrics wrap-up
- [ ] module-2 (Day 22): Reader 10 readiness + production patterns wrap-up
- [ ] module-3 (Day 23): Reader 10 readiness + evaluation wrap-up
- [ ] module-4 (Day 24): Reader 10 readiness + cost/economics wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`
- [ ] After all 4 modules: `python3 scripts/audit_lessons.py` — 0 violations
