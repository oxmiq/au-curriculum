# Curriculum

!!! note "Shape"
    10 weeks, half-days (Approx 3 hours)

!!! note "Cadence"
    one concept per day, Friday is consolidation

!!! note "Outcome"
    you can reason about how AI runs in production — and prove it end-to-end on real hardware

<!-- AUTO-GEN:CARD-GRID:START -->
<div class="ox-card-grid" markdown="0">
  <a class="ox-card" href="../lessons/week-01/" style="--i:1">
    <span class="ox-card__eyebrow">Week 01</span>
    <h3 class="ox-card__title">Orientation & Foundations</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-02/" style="--i:2">
    <span class="ox-card__eyebrow">Week 02</span>
    <h3 class="ox-card__title">The GPU & Memory</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>  
  <a class="ox-card" href="../lessons/week-03/" style="--i:3">
    <span class="ox-card__eyebrow">Week 03</span>
    <h3 class="ox-card__title">Attention & KV Cache</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-04/" style="--i:4">
    <span class="ox-card__eyebrow">Week 04</span>
    <h3 class="ox-card__title">Scaling & Stacks</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-05/" style="--i:5">
    <span class="ox-card__eyebrow">Week 05</span>
    <h3 class="ox-card__title">Metrics & Production</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-06/" style="--i:6">
    <span class="ox-card__eyebrow">Week 06</span>
    <h3 class="ox-card__title">Prompt Engineering + AI Agents</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-07/" style="--i:7">
    <span class="ox-card__eyebrow">Week 07</span>
    <h3 class="ox-card__title">Bridge: Theory Meets Tooling</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-08/" style="--i:8">
    <span class="ox-card__eyebrow">Week 08</span>
    <h3 class="ox-card__title">Capsule: Connections & Operations</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-09/" style="--i:9">
    <span class="ox-card__eyebrow">Week 09</span>
    <h3 class="ox-card__title">Capsule: Benchmarking & Eval</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
  <a class="ox-card" href="../lessons/week-10/" style="--i:10">
    <span class="ox-card__eyebrow">Week 10</span>
    <h3 class="ox-card__title">Capstone Project</h3>
    <span class="ox-card__cta">Open week →</span>
  </a>
</div>
<!-- AUTO-GEN:CARD-GRID:END -->

## How a day runs

Every day has the same shape:

| Block | What happens |
|---|---|
| Pre-read | curated reading + 3 reflection questions |
| Readiness check | 5-question quiz on the pre-read; <3/5 pairs you with a buddy |
| Concept | one core idea — analogy first, then technical detail |
| Practice | guided exercise, then open-ended challenge; pair work encouraged |
| Wrap-up | students summarize, connect to what comes next |

Fridays carry no new concepts — quiz, review, catch-up, and the week's assignment.

## Phases

| Weeks | Phase | Why it sits here |
|---|---|---|
| 1 | Orientation & Foundations | level-set tooling and GPU intuition before anything else |
| 2 – 5 | Inference Engineering | the gap nobody else teaches; four weeks because each layer needs the one before it |
| 6 | Prompt Engineering | the bridge from inference behaviour to agent behaviour |
| 7 | AI Agents | application context — why latency, governance, and reliability matter |
| 8 – 9 | Capsule | platform where everything learned becomes a working system |
| 10 | Capstone | independent end-to-end demonstration |

## Day-by-day map

### Week 1 — Orientation & Foundations

Goal: everyone arrives at the same starting line.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 1 | Welcome & Context | What Oxmiq is; the GPU-cloud problem; the 10-week arc | Write "what I think Capsule does" in 3 sentences |
| 2 | Shell & Linux | Pipes, redirects, grep, awk, scripting | Parse `nvidia-smi` with grep/awk; 15-line bash monitor |
| 3 | Git Workflow | Branch, commit (conventional), push, PR | Fork → change → PR → review a peer's PR |
| 4 | How Computers Run AI | CPU vs GPU; matmul = parallelism; train vs serve | Draw the path of a prompt from keyboard to screen |
| 5 | **Consolidation** | No new content; open lab + Week 1 quiz | Readiness for Week 2 |

### Week 2 — Inference: GPU & Memory

Goal: build the hardware mental model.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 6 | Prompt → Token Pipeline | tokenize → embed → layers → logits → sample; one forward pass = one token | Trace a 5-word prompt on paper, annotated |
| 7 | Meet the GPU | SMs, Tensor Cores, HBM, L2; SM = factory floor, HBM = warehouse | Label a blank GPU diagram; match specs to 3 GPU models |
| 8 | The Memory Bottleneck | HBM → L2 → SRAM hierarchy; data movement is the real cost | Time to read 16 GB from HBM at 3.35 TB/s — vs L2 |
| 9 | Compute- vs Memory-Bound | Ops:byte ratio; roofline model; prefill = compute, decode = memory | Classify 5 workloads; sketch them on the roofline |
| 10 | **Consolidation** | Feynman teach-back: each team teaches one Day 6–9 concept to another | Quiz; assign KV-cache pre-read |

### Week 3 — Inference: Attention & KV Cache

Goal: the central resource-management problem of serving LLMs.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 11 | Prefill & Decode | Prefill parallel, compute-bound (TTFT); decode sequential, memory-bound (TPS) | 1000-in / 500-out — sketch the timeline |
| 12 | The KV Cache | Grows linearly with context; can exceed weights at long context | Llama-3.1-8B KV at 4K / 32K / 128K — does it fit in 80 GB? |
| 13 | Flash- & Paged-Attention | FlashAttention: fuse one kernel, fewer HBM trips. PagedAttention: virtual memory for the KV cache | Draw memory access before vs after FlashAttention |
| 14 | Quantization | Fewer bits → less data moved → faster decode; sensitivity ladder weights→activations→KV→attention | 8B model FP16 vs FP8 vs INT4 — memory and theoretical speedup |
| 15 | **Consolidation** | Memory-budget calculator mini-project | Pair presentations — one insight each |

### Week 4 — Inference: Scaling & Stacks

Goal: from one GPU to many; from theory to real software.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 16 | Tensor Parallelism | Split each layer; needs all-reduce; intra-node only; lowest latency | TP=2 and TP=4 for an 8B model — memory per GPU; when not to use TP |
| 17 | Pipeline & Expert Parallelism | PP for multi-node (bubbles), EP for MoE throughput; TP latency, EP throughput, PP fallback | 8×H100: design parallelism for 70B dense vs 235B MoE |
| 18 | Speculative Decoding | Draft cheap → verify → N+1 tokens/step; helps when batch is low | If 4 of 5 draft tokens accept, what's the speedup? When does it fail? |
| 19 | Serving Engines | Continuous batching, disaggregation (xPyD), engine tradeoffs (vLLM / SGLang / TRT-LLM) | Pick engines for (a) broad HW, (b) MoE, (c) max-perf NVIDIA |
| 20 | **Consolidation** | Synthesis: design a serving system for 70B + 8×H100 + P99<500ms | Critique each other's designs |

### Week 5 — Inference: Metrics & Economics

Goal: measure what matters; operate in the real world; understand cost.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 21 | Metrics | TTFT, ITL, TPS, percentiles; throughput vs latency tension | Interpret a benchmark dump — write the story the numbers tell |
| 22 | Production Patterns | Containers, cold starts, autoscaling, canary (not blue-green), LoRA serving | Deployment for 99.9% uptime, ≤200ms P99, 3× spikes |
| 23 | Evaluation & Quality | Perplexity (coarse), task evals, quantization quality checks, Goodhart's Law | 10-prompt eval suite for a code assistant — what's a pass? |
| 24 | Cost & Economics | $/M tokens, ~10× decline/year, reserved vs on-demand vs spot, $/completed-task | 100k DAU × 500 tokens — API vs dedicated 8×H100 |
| 25 | **Consolidation + Phase 1 Wrap** | Open-book problem set; team presentations of Week 4 designs | Reflection: most important thing learned in Phase 1 |

### Week 6 — Prompt Engineering

Goal: craft prompts that produce reliable, high-quality output from any LLM.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 26 | Prompt Structure | System + human turn; specificity beats vagueness | Rewrite 5 vague prompts; compare outputs |
| 27 | Roles, Data, Formatting | Personas, XML data separation, output format, prefill | Build a JSON extractor: role + data + format spec |
| 28 | CoT & Few-Shot | Step-by-step planning; showing beats telling | One CoT and one few-shot prompt for the same problem — compare |
| 29 | Hallucinations & Evals | Citations, hedging, refusal; prompt evals | Full prompt for one industry case + 5-prompt eval suite |
| 30 | **Consolidation: Chaining & Tool Use** | Decompose into chains; tool use via structured output; search & retrieval | 2-step chained prompt; run a prompt eval |

### Week 7 — AI Agents

Goal: how agents are built, how they connect to tools, how they fail.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 31 | The Agent Loop | ReAct: perceive → plan → act → observe; why now (MoE + FlashAttention made it cheap) | Agent loop for "deploy a model on a GPU machine" — tools? failure modes? |
| 32 | Tools & MCP | MCP as universal tool standard; A2A for multi-agent; `capsule mcp` | MCP manifest for list-machines / deploy-model / check-status |
| 33 | Governance & Security | Prompt injection (direct + indirect); blast radius; sandboxing; observability | 3 injection attacks against a deploy agent — then defenses |
| 34 | Orchestration & Multi-Agent | Single vs multi; routing; long-horizon drift; workflow as control point | 3-agent system: responsibilities, routing, governance |
| 35 | **Consolidation: Case Studies** | What ships, what fails; integration: design a complete agent system | Post-mortem of a hypothetical failure; 15-min team presentations |

### Week 8 — Capsule: Foundations

Goal: Capsule installed, understood, and operationally fluent.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 36 | Architecture & Install | Client → server → cloud; auth via Azure B2C; `capsule --version`, `capsule status` | Install + authenticate; draw architecture labelled by week |
| 37 | Environments & Fleet | `capsule env`, `capsule config customer`, `capsule list` + filters | Switch envs; filter fleet by GPU/VRAM/vendor; `\| jq` exercises |
| 38 | Connecting to Machines | `term`, `exec`, `code`, `cursor`, `claude`; SshRTC vs `--direct` | `term` + `nvidia-smi`; VS Code remote; compare `--direct` |
| 39 | Files, Storage, Streaming | OneDrive mount; SCP; passthrough; `stream`; `docker` w/ GPU | SCP a file; stream a desktop; container with `nvidia-smi` |
| 40 | **Consolidation: Reliability** | `capsule cleanup`; diagnostic sequence; bug-report shape | Diagnose 3 instructor-simulated breakages; write proper reports |

### Week 9 — Capsule: Benchmarking

Goal: where Phase 1 becomes real.

| Day | Topic | Core concept | Practice |
|---|---|---|---|
| 41 | Your First Benchmark | `capsule benchmark`; backends; params map to Phase 1 (concurrency = batching, tp = parallelism, quant = quantization) | Baseline Llama-3.1-8B; explain every metric in Phase 1 vocabulary |
| 42 | Varying Parameters | One variable at a time | Concurrency sweep 1→4→8→16; quantize and compare; plot |
| 43 | Interactive Evaluation | `capsule chat`; structured eval (factual, math, code, refusal); spotting quant regressions | Chat FP16 vs quantized — same 5 prompts; is the speedup worth it? |
| 44 | Scheduling & MCP | `capsule schedule`; `capsule mcp`; when to schedule vs interactive | `eval.sh` → submit → monitor → cancel; read the MCP manifest |
| 45 | **Consolidation** | Timed end-to-end loop: find → benchmark → evaluate → record (≤20 min) | Retrospective: what surprised you? |

### Week 10 — Capstone

Goal: independently demonstrate everything learned.

| Day | Topic | What happens |
|---|---|---|
| 46 | Kickoff & Planning | Form 2–3-person teams; pick use case; choose model + hardware + quant; design eval plan; peer review |
| 47 | Execute | Deploy on Capsule; run benchmarks across configs; interactive evaluation; document everything |
| 48 | Analyze & Recommend | Compile comparison tables; compute costs; form a justified recommendation; build the deck |
| 49 | Present | 15 min per team + 10 min Q&A; peer feedback; panel assessment |
| 50 | Close | 1:1 feedback; Oxmiq hiring path or portfolio guidance; retrospective |

**Deliverable shape:** *"For use case X, deploy model Y at config Z, because [benchmark evidence] shows [metric] at [cost], with [quality tradeoff] that is [acceptable / not] because [reasoning]."*

## Assessment

Cumulative, low-pressure. No surprise exams. No memorization tests.

| Component | Weight | When |
|---|---|---|
| Daily readiness checks | 10% | every day · diagnostic, pass/fail |
| Weekly consolidation exercises | 20% | Fridays · open-ended, collaborative |
| Phase 1 problem set | 15% | Day 25 · open-book, reasoning-focused |
| Prompt Engineering eval suite | 5% | Day 30 · author + run a prompt eval |
| Phase 2 agent design | 10% | Day 35 · team presentation |
| Capstone | 40% | Week 10 · end-to-end demonstration |

## Pacing rules

1. One concept per day. If it can't fit one session, it becomes two days.
2. Pre-reading is mandatory but short. 15–30 min. It levels the room.
3. The readiness check is diagnostic, not punitive — buddy pairing, not embarrassment.
4. Fridays are sacred. No new content. Practice, review, breathe.
5. Afternoons are free. Learning needs space.
6. Every session connects backwards ("remember when we learned X? That's why Y works").
7. Practice is longer than lecture. 90 min vs 60. Doing > listening.
8. Pair work over solo. Explaining something to someone else is the deepest form of learning it.

For the *why* behind these choices, see [Why this curriculum](rationale.md).
