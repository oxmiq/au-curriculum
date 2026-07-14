---
title: Capsule Power-User - Pre-Lecture Reading
---

# Capsule Power-User - Pre-Lecture Reading

> **The Capsule Power-User practicum.** Required reading + three reflection questions per section, due in writing at the start-of-day readiness check.
>
> The sections below are listed in teaching order and span the Capsule phase (Weeks 7-9). Each day's lesson links you to the exact section it needs, so read to the link rather than by a fixed day number. This phase is the *practicum* of the program: by the end you will have driven a real GPU fleet from the command line, not as a tourist but at the level expected of a junior engineer joining Oxmiq. Every reflection question is designed to surface the gap between "I read the page" and "I can operate the tool under time pressure." Take them seriously.

---

## Capsule Architecture & Installation

**Pre-reading (≈ 40 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 1 "Foundations"** (20 min) and **Module 2 "Installation"** (15 min).
- [`capsule --help`](https://github.com/oxmiq/capsule) output: scan the top-level command list (5 min). You don't need to install yet; just read the surface area.

**Reflection questions:**

1. The Lab Guide names *two distinct connection paths* in Capsule. Name them and, in one sentence each, say what tradeoff each represents (latency, firewall posture, NAT traversal, etc.).
2. Capsule's architecture is `client → server → cloud`. Map each Phase-1 concept you remember (KV cache, continuous batching, quantization, MoE, FlashAttention) onto **which tier** it lives in. (Hint: most live in one specific tier.)
3. Capsule authenticates via Azure B2C with browser-flow + token caching. Why is interactive browser auth on the first run *better* security than an API key passed by environment variable, even though the latter is "simpler"?

---

## Environments & Fleet Discovery

**Pre-reading (≈ 25 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 3 "Environments"** (15 min).
- *Capsule-Power-User-Cheatsheet.md*, sections on `capsule env` and `capsule list` (10 min: skim).

**Reflection questions:**

1. Switching environments (`capsule env set`) forces re-authentication. *Why*: what is the threat model that this design defends against? (One sentence; think "what would happen if it *didn't* force re-auth.")
2. The two diagnostic facts that resolve 90% of "I see the wrong machines" tickets are the **tenant** and the **customer context**. In your own words, what's the difference between them, and which command surfaces each?
3. Write the exact `capsule list` invocation that would return *only* H100 machines with ≥80 GB VRAM in JSON, ready to pipe into `jq`. (You can guess the flag names; you'll verify against the tool next session.)

---

## Connecting to Machines

**Pre-reading (≈ 25 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 5 "Connecting"** (15 min).
- *Capsule-Power-User-Cheatsheet.md*, the table of the 5 connect commands: `term`, `exec`, `code`, `cursor`, `claude` (10 min).

**Reflection questions:**

1. `capsule term` and `capsule exec` look superficially similar. State the *one* rule that tells you which to use, and give one example task best suited to each.
2. Routing-by-config-tag vs routing-by-`-u <unique-id>`: which one is appropriate for "I want any L4 machine," and which for "I want *this specific* L4 machine I've been working on all morning"? Why does the distinction matter for reproducibility?
3. `--direct` skips the SshRTC overlay. When is the latency win worth giving up the firewall/NAT-traversal benefit, and when is it not? Name one situation each.

---

## Files, Storage & Streaming

**Pre-reading (≈ 40 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 6 "Files"** (15 min) and **Module 7 "Streaming"** (15 min).
- *Capsule-Power-User-Cheatsheet.md*, file-transfer table (10 min).

**Reflection questions:**

1. The three file-movement paths are: OneDrive mount, SCP, and dotfile passthrough. For each, give one concrete scenario where it is the *correct* choice and the other two would be wrong.
2. `capsule stream` opens a WebRTC desktop or app stream. Why WebRTC specifically: what advantage does it have over plain VNC or RDP for a GPU-heavy workload?
3. `capsule docker` exposes the GPU into a container with the correct toolkit pre-wired. What's one thing this saves you from having to set up by hand? (If you've never set up `nvidia-container-toolkit`, that's the point.)

---

## Consolidation: Reliability & Diagnostics

**Pre-reading (≈ 15 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 10's known-quirks table** (10 min).
- *Capsule-Power-User-Cheatsheet.md*, "Diagnostic sequence" panel (5 min).

**Reflection questions:**

1. Your `capsule list` shows machines that *shouldn't* be there. What's the first command you run, and why is it that one rather than `capsule status` or `--refresh`?
2. From the known-quirks table, pick the one failure mode that surprised you most. In one sentence, what's the recovery? In one more, why does it happen?
3. What makes a Capsule bug report *useful* to an Oxmiq engineer vs *useless*? List the pieces of information you'd always include.

---

## Your First Benchmark

**Pre-reading (≈ 30 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 8 "Benchmarking"** (20 min).
- Re-skim your own notes from **Week 4 (Inference Engineering - serving)**: specifically TTFT, ITL, TPS, throughput definitions (10 min). The Capsule benchmark output uses these exact terms.

**Reflection questions:**

1. `--concurrency` and `--tp` are two of the most important benchmark flags. Using *Phase 1 vocabulary*, explain what each one controls under the hood. (If you find yourself writing "the number of concurrent things," go back to your Week 4 notes.)
2. The benchmark output reports TTFT P95, ITL P95, and TPS. A product manager asks "is the model fast?": which of the three is the right answer, and why does the right answer depend on whether the use case is *chat* or *batch summarization*?
3. Before you run the benchmark next session, write down your *prediction* for Llama-3.1-8B FP16 on 1×H100 at concurrency=1: TTFT P95 (ms), TPS. The act of predicting first is what trains intuition. We'll compare predictions to reality in class.

---

## Varying Parameters

**Pre-reading (≈ 15 min):**
- No new reading. Re-read your first-benchmark output and your prediction notes (15 min).
- Optional: skim [vLLM concurrency notes](https://docs.vllm.ai/en/latest/serving/performance.html) for the "knee" intuition.

**Reflection questions:**

1. The scientific method rule: *one variable at a time*. Write down the three variables you'll sweep this week (concurrency, quantization, parallelism). For each sweep, what's the *one* thing that varies and what are the *several* things you hold constant?
2. If you double concurrency, what should happen to throughput, P95 latency, and TTFT P95? Answer with direction (up / down / flat) and rough magnitude. We'll check your predictions against actual data.
3. Quantization gives you a free speedup *if* quality holds. What's the *one* check that tells you whether quality held? (You practised this in the Prompt Engineering week; recall it.)

---

## Interactive Evaluation

**Pre-reading (≈ 20 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 9 "Chat"** (15 min).
- Your own prompt-eval notes from the Prompt Engineering week (5 min: re-read what "structured eval" meant).

**Reflection questions:**

1. Why is benchmarking *speed alone* insufficient? Give one concrete way speed can look great and quality can be quietly broken.
2. Structured eval should hit four categories: factual recall, math, code generation, and refusal/safety. Why does an evaluation suite *without* a refusal category systematically over-rate quantized models?
3. Write the 5 prompts you'll use next session against both FP16 and quantized variants. Each prompt should have an *expected behavior* (not just an expected answer): what does "passed" mean for that prompt?

---

## Scheduling & MCP

**Pre-reading (≈ 25 min):**
- *Capsule-Power-User-Lab-Guide.md*, **Module 10 "Scheduling"** (15 min).
- *AI Agents - Student Guide*, **Module 2 "Action Layer"**: re-read the MCP section (10 min). The same protocol you studied in the AI Agents week is what `capsule mcp` implements.

**Reflection questions:**

1. Why is running a 4-hour benchmark in an interactive terminal a recipe for losing the results? Name two failure modes and the `capsule schedule` feature that prevents each.
2. `capsule mcp --output` emits a tool manifest. Which AI assistants can consume that manifest today, and what does the assistant *do* with it: connect each step of the data flow.
3. Looking back at the agent loop you sketched in the AI Agents week, write down *which Capsule commands* would be the Action-layer tools for that agent. (This is exactly the integration you'll demo in the end-of-phase sprint.)

---

## Consolidation: End-to-End Sprint

**Pre-reading (≈ 10 min):**
- No new reading. Review your Cheatsheet for 10 minutes. You will use it as your only reference during the timed exercise.

**Reflection questions:**

1. The timed sprint: find machine → benchmark → evaluate → record, in 20 minutes. Write down the *exact sequence of commands* you plan to run, in order. You'll execute this in class; be ready.
2. Of all the commands in this phase, which surprised you most by how much you actually use it? Which one did you expect to need but rarely did?
3. Looking back across the whole program so far, name the *one* concept whose meaning shifted most for you between the day you first heard it and today. (Be ready to share with the cohort; these are the moments worth marking.)

---

## How facilitators score your reflections

Same 4-tier rubric as the AI Agents Pre-Lecture Reading:

| Tier | What facilitators see |
|---|---|
| Excellent | Answer references a specific Capsule command, output number, or earlier-week artifact. Shows you connected Phase 1/2 vocabulary to the tool. |
| Proficient | Correct and complete. No connections to earlier weeks. |
| Developing | Partially correct. Confuses two adjacent commands (e.g., `term` vs `exec`). |
| Below | Skipped, or generic "Capsule does X" answer with no specifics. |

The bar for Excellent in this phase is that you sound like an engineer reasoning about a real tool: because you are.
