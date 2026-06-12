# Curriculum

> **Shape:** 10 weeks, half-days (4 hours / morning).
> **Cadence:** one concept per day, Friday is consolidation, afternoons are yours.
> **Outcome:** you can reason about how AI runs in production — and prove it end-to-end on real hardware.

## How a day runs

Every morning has the same shape:

| Block | Time | What happens |
|---|---|---|
| Pre-read | the evening before | 15–30 min of curated reading + 3 reflection questions |
| Readiness check | 0:00 – 0:20 | 5-question quiz on the pre-read; <3/5 pairs you with a buddy |
| Concept | 0:20 – 1:20 | one core idea — analogy first, then technical detail |
| Break | 1:20 – 1:30 | |
| Practice | 1:30 – 3:00 | guided exercise, then open-ended challenge; pair work encouraged |
| Wrap-up | 3:00 – 3:30 | students summarize, connect to what comes next |
| Office hours | 3:30 – 4:00 | optional, for clarifications or going deeper |

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

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 1 | Welcome & Context | — | What Oxmiq is; the GPU-cloud problem; the 10-week arc | Write "what I think Capsule does" in 3 sentences |
| 2 | Shell & Linux | MIT Missing Semester — shell (20 min) | Pipes, redirects, grep, awk, scripting | Parse `nvidia-smi` with grep/awk; 15-line bash monitor |
| 3 | Git Workflow | "Git in 15 minutes" (15 min) | Branch, commit (conventional), push, PR | Fork → change → PR → review a peer's PR |
| 4 | How Computers Run AI | 3Blue1Brown-style GPU video (15 min) | CPU vs GPU; matmul = parallelism; train vs serve | Draw the path of a prompt from keyboard to screen |
| 5 | **Consolidation** | — | No new content; open lab + Week 1 quiz | Readiness for Week 2 |

### Week 2 — Inference: GPU & Memory

Goal: build the hardware mental model.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 6 | Prompt → Token Pipeline | Inference vs training (15 min) | tokenize → embed → layers → logits → sample; one forward pass = one token | Trace a 5-word prompt on paper, annotated |
| 7 | Meet the GPU | H100 1-page spec (10 min) | SMs, Tensor Cores, HBM, L2; SM = factory floor, HBM = warehouse | Label a blank GPU diagram; match specs to 3 GPU models |
| 8 | The Memory Bottleneck | "Why bandwidth matters" (20 min) | HBM → L2 → SRAM hierarchy; data movement is the real cost | Time to read 16 GB from HBM at 3.35 TB/s — vs L2 |
| 9 | Compute- vs Memory-Bound | "Arithmetic intensity" (15 min) | Ops:byte ratio; roofline model; prefill = compute, decode = memory | Classify 5 workloads; sketch them on the roofline |
| 10 | **Consolidation** | — | Feynman teach-back: each team teaches one Day 6–9 concept to another | Quiz; assign KV-cache pre-read |

### Week 3 — Inference: Attention & KV Cache

Goal: the central resource-management problem of serving LLMs.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 11 | Prefill & Decode | Prefill-vs-decode explainer (15 min) | Prefill parallel, compute-bound (TTFT); decode sequential, memory-bound (TPS) | 1000-in / 500-out — sketch the timeline |
| 12 | The KV Cache | KV-cache blog with diagrams (20 min) | Grows linearly with context; can exceed weights at long context | Llama-3.1-8B KV at 4K / 32K / 128K — does it fit in 80 GB? |
| 13 | Flash- & Paged-Attention | FlashAttention blog + abstract (20 min) | FlashAttention: fuse one kernel, fewer HBM trips. PagedAttention: virtual memory for the KV cache | Draw memory access before vs after FlashAttention |
| 14 | Quantization | Quantization 101 (20 min) | Fewer bits → less data moved → faster decode; sensitivity ladder weights→activations→KV→attention | 8B model FP16 vs FP8 vs INT4 — memory and theoretical speedup |
| 15 | **Consolidation** | — | Memory-budget calculator mini-project | Pair presentations — one insight each |

### Week 4 — Inference: Scaling & Stacks

Goal: from one GPU to many; from theory to real software.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 16 | Tensor Parallelism | "How to split a model across GPUs" (20 min) | Split each layer; needs all-reduce; intra-node only; lowest latency | TP=2 and TP=4 for an 8B model — memory per GPU; when not to use TP |
| 17 | Pipeline & Expert Parallelism | Pipeline + MoE blog (20 min) | PP for multi-node (bubbles), EP for MoE throughput; TP latency, EP throughput, PP fallback | 8×H100: design parallelism for 70B dense vs 235B MoE |
| 18 | Speculative Decoding | Speculative decoding explainer (15 min) | Draft cheap → verify → N+1 tokens/step; helps when batch is low | If 4 of 5 draft tokens accept, what's the speedup? When does it fail? |
| 19 | Serving Engines | vLLM intro (15 min) | Continuous batching, disaggregation (xPyD), engine tradeoffs (vLLM / SGLang / TRT-LLM) | Pick engines for (a) broad HW, (b) MoE, (c) max-perf NVIDIA |
| 20 | **Consolidation** | — | Synthesis: design a serving system for 70B + 8×H100 + P99<500ms | Critique each other's designs |

### Week 5 — Inference: Metrics & Economics

Goal: measure what matters; operate in the real world; understand cost.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 21 | Metrics | Latency vs throughput (15 min) | TTFT, ITL, TPS, percentiles; throughput vs latency tension | Interpret a benchmark dump — write the story the numbers tell |
| 22 | Production Patterns | Deploying LLMs in production (20 min) | Containers, cold starts, autoscaling, canary (not blue-green), LoRA serving | Deployment for 99.9% uptime, ≤200ms P99, 3× spikes |
| 23 | Evaluation & Quality | How to evaluate LLMs (20 min) | Perplexity (coarse), task evals, quantization quality checks, Goodhart's Law | 10-prompt eval suite for a code assistant — what's a pass? |
| 24 | Cost & Economics | Inference cost newsletter (15 min) | $/M tokens, ~10× decline/year, reserved vs on-demand vs spot, $/completed-task | 100k DAU × 500 tokens — API vs dedicated 8×H100 |
| 25 | **Consolidation + Phase 1 Wrap** | — | Open-book problem set; team presentations of Week 4 designs | Reflection: most important thing learned in Phase 1 |

### Week 6 — Prompt Engineering

Goal: craft prompts that produce reliable, high-quality output from any LLM.

> Primary source: [Anthropic Prompt Engineering Interactive Tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) — 9 chapters + appendix.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 26 | Prompt Structure | Anthropic Ch 1 + 2 (20 min) | System + human turn; specificity beats vagueness | Rewrite 5 vague prompts; compare outputs |
| 27 | Roles, Data, Formatting | Anthropic Ch 3 + 4 + 5 (25 min) | Personas, XML data separation, output format, prefill | Build a JSON extractor: role + data + format spec |
| 28 | CoT & Few-Shot | Anthropic Ch 6 + 7 (20 min) | Step-by-step planning; showing beats telling | One CoT and one few-shot prompt for the same problem — compare |
| 29 | Hallucinations & Evals | Anthropic Ch 8 + 9 (25 min) | Citations, hedging, refusal; prompt evals | Full prompt for one industry case + 5-prompt eval suite |
| 30 | **Consolidation: Chaining & Tool Use** | Anthropic Appendix (15 min) | Decompose into chains; tool use via structured output; search & retrieval | 2-step chained prompt; run a prompt eval |

### Week 7 — AI Agents

Goal: how agents are built, how they connect to tools, how they fail.

> Primary sources: Student Guide (Modules 0–4) + [HuggingFace Agents Course](https://huggingface.co/learn/agents-course) Units 1–3.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 31 | The Agent Loop | Student Guide Module 0 (20 min) | ReAct: perceive → plan → act → observe; why now (MoE + FlashAttention made it cheap) | Agent loop for "deploy a model on a GPU machine" — tools? failure modes? |
| 32 | Tools & MCP | Module 2 (25 min) | MCP as universal tool standard; A2A for multi-agent; `capsule mcp` | MCP manifest for list-machines / deploy-model / check-status |
| 33 | Governance & Security | Module 3 (25 min) | Prompt injection (direct + indirect); blast radius; sandboxing; observability | 3 injection attacks against a deploy agent — then defenses |
| 34 | Orchestration & Multi-Agent | Module 4 (20 min) | Single vs multi; routing; long-horizon drift; workflow as control point | 3-agent system: responsibilities, routing, governance |
| 35 | **Consolidation: Case Studies** | Klarna + coding-agent cases (20 min) | What ships, what fails; integration: design a complete agent system | Post-mortem of a hypothetical failure; 15-min team presentations |

### Week 8 — Capsule: Foundations

Goal: Capsule installed, understood, and operationally fluent.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 36 | Architecture & Install | Lab Guide M1 + M2 (35 min) | Client → server → cloud; auth via Azure B2C; `capsule --version`, `capsule status` | Install + authenticate; draw architecture labelled by week |
| 37 | Environments & Fleet | Lab Guide M3 (15 min) | `capsule env`, `capsule config customer`, `capsule list` + filters | Switch envs; filter fleet by GPU/VRAM/vendor; `\| jq` exercises |
| 38 | Connecting to Machines | Lab Guide M5 (15 min) | `term`, `exec`, `code`, `cursor`, `claude`; SshRTC vs `--direct` | `term` + `nvidia-smi`; VS Code remote; compare `--direct` |
| 39 | Files, Storage, Streaming | Lab Guide M6 + M7 (30 min) | OneDrive mount; SCP; passthrough; `stream`; `docker` w/ GPU | SCP a file; stream a desktop; container with `nvidia-smi` |
| 40 | **Consolidation: Reliability** | Lab Guide M10 quirks (10 min) | `capsule cleanup`; diagnostic sequence; bug-report shape | Diagnose 3 instructor-simulated breakages; write proper reports |

### Week 9 — Capsule: Benchmarking

Goal: where Phase 1 becomes real.

| Day | Topic | Pre-read | Core concept | Practice |
|---|---|---|---|---|
| 41 | Your First Benchmark | Lab Guide M8 (20 min) | `capsule benchmark`; backends; params map to Phase 1 (concurrency = batching, tp = parallelism, quant = quantization) | Baseline Llama-3.1-8B; explain every metric in Phase 1 vocabulary |
| 42 | Varying Parameters | — | One variable at a time | Concurrency sweep 1→4→8→16; quantize and compare; plot |
| 43 | Interactive Evaluation | Lab Guide M9 (15 min) | `capsule chat`; structured eval (factual, math, code, refusal); spotting quant regressions | Chat FP16 vs quantized — same 5 prompts; is the speedup worth it? |
| 44 | Scheduling & MCP | Lab Guide M10 (15 min) | `capsule schedule`; `capsule mcp`; when to schedule vs interactive | `eval.sh` → submit → monitor → cancel; read the MCP manifest |
| 45 | **Consolidation** | — | Timed end-to-end loop: find → benchmark → evaluate → record (≤20 min) | Retrospective: what surprised you? |

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
