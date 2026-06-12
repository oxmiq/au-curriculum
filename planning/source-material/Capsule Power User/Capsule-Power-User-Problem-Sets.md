# Capsule Power-User — Problem Sets

*Graded exercises for Weeks 8–9. Each day has 5 problems of increasing difficulty. Problems marked ★ are required; ☆ are stretch. Every problem requires running a real Capsule command against a real machine — no whiteboard-only answers.*

**Submission format:** one markdown file per problem set, with each problem's solution including (a) the exact command(s), (b) the raw output (or a screenshot if visual), (c) your analysis. Commit to your `practice/week-08/` or `practice/week-09/` folder.

---

## Problem Set 36 — Architecture & Installation

### Problem 36.1 ★ — The architecture map

Draw the Capsule `client → server → cloud` diagram. Annotate each tier with: (a) which Phase-1 concepts live there (KV cache, batching, quantization, etc.) — most will be in only one tier; (b) which auth boundary crosses what.

### Problem 36.2 ★ — Two-path verification

Connect to the same machine twice — once via SshRTC (default), once via `--direct`. Measure round-trip ping latency for both. Report the deltas. Identify the situation in which each is the right default.

### Problem 36.3 ★ — Headless auth

Set up a Capsule auth token (`capsule auth token`) and use `CAPSULE_AUTH_TOKEN=` to run `capsule list` from a clean shell with no browser available. Submit the command transcript. Explain why this is a *worse* default than browser flow but a *necessary* fallback.

### Problem 36.4 ☆ — Permission probe

Without breaking anything, find one Capsule command that returns an error when you don't hold a particular permission. Capture the error. Speculate on which side of the auth boundary the check fires (client / server / cloud).

### Problem 36.5 ☆ — Cross-platform install

Install Capsule on a second OS (Windows or Linux if you've been on macOS, vice-versa). Document any step that didn't "just work." File a doc-improvement issue (or PR) against the Capsule repo with your suggested fix.

---

## Problem Set 37 — Environments & Fleet Discovery

### Problem 37.1 ★ — Customer-context audit

Switch through `micc → modelhosting → oneplay → cree8`, running `capsule list` after each. Record the fleet size at each. Identify one machine that exists in more than one customer's fleet (if any), and one that's exclusive to a single customer.

### Problem 37.2 ★ — The filter battery

Write `capsule list --filter` invocations for each of these queries:
1. All Nvidia GPUs with ≥80 GB VRAM.
2. All Tenstorrent machines.
3. All CI machines.
4. All Linux machines with ≥64 GB system memory.
5. (Stretch) Combine: Nvidia + ≥24 GB VRAM + Linux.

Submit the commands and outputs for each.

### Problem 37.3 ★ — JSON + jq drill

Pipe `capsule list --json` through `jq` to produce: (a) a flat list of unique IDs only, (b) a count of machines grouped by GPU model, (c) the single machine with the highest VRAM. Submit your `jq` expressions.

### Problem 37.4 ☆ — The wrong-fleet ticket

Deliberately misconfigure: set customer to a fleet you don't usually use, then run `capsule list`. Pretend a teammate filed a "I see weird machines" ticket. Write the *minimal* diagnostic sequence (≤ 3 commands) that resolves it.

### Problem 37.5 ☆ — Re-auth justification

Write a 1-paragraph explanation suitable for a non-technical onboarding doc: "Why does Capsule make me log in again when I switch from `prod` to `public`?" Include the *security* answer and the *engineering* answer.

---

## Problem Set 38 — Connecting to Machines

### Problem 38.1 ★ — All five connectors

Connect to a single Capsule machine using each of `term`, `exec`, `code`, `cursor`, `claude`. Submit a one-line transcript for each (e.g., the prompt you saw, the command you ran). If you don't have one of the editors installed, install the open ones; for paid ones, document the install instructions you'd give a new hire.

### Problem 38.2 ★ — Tag vs unique-ID

Pick a config tag (e.g., `NV-3060-04-1`) with ≥3 machines behind it. Run `capsule exec <tag> -- hostname` three times. Are you on the same machine each time? Now do the same with `capsule exec -u <unique-id> -- hostname`. Report.

### Problem 38.3 ★ — `--direct` latency win

On the same machine: run `capsule exec <tag> -- echo hi` ten times with SshRTC, then ten times with `--direct`. Report the min/median/max of each. Argue which difference is "noise" and which is "signal."

### Problem 38.4 ☆ — Session-limit experiment

Deliberately exceed your session limit by opening parallel `capsule term` sessions. Capture the error. Run `capsule status` to see what's open. Disconnect what you don't need and recover.

### Problem 38.5 ☆ — The reproducibility bug

Tell a story (real or hypothetical, ≤ 200 words): an engineer ran a benchmark on Monday, got 220 TPS. Re-ran "the same benchmark" on Tuesday, got 180 TPS. The root cause was tag-vs-unique-ID routing. Reconstruct what happened. What's the fix?

---

## Problem Set 39 — Files, Storage & Streaming

### Problem 39.1 ★ — Three transfers, three paths

Move a 1 MB text file in *all three* ways: OneDrive mount, SCP, dotfile passthrough (for the last, treat it as moving a `.zshrc`). Time each. Submit the transfer commands and the timings. Note: dotfile passthrough only fires on first-connect — set up a fresh machine context if needed.

### Problem 39.2 ★ — Stream a real workload

Use `capsule stream` to open a desktop or app on a remote machine. Run something that's actually GPU-bound (a 3D viewer, a game launcher, or even `nvidia-smi -l 1` if no GUI tool is available). Report observed frame rate and one source of latency.

### Problem 39.3 ★ — Docker + GPU

Use `capsule docker` to launch a container that runs `nvidia-smi` and exits. Submit the command, the output, and the Dockerfile (if you wrote one). Confirm the container saw the same GPU as `nvidia-smi` on the host.

### Problem 39.4 ☆ — Storage decision matrix

Build a small table: rows = file types (research dataset, eval prompts, model weights, one-off log file, `.zshrc`), columns = transfer mechanisms. Fill in the *right* choice per cell and the *wrong but tempting* alternative.

### Problem 39.5 ☆ — WebRTC vs alternatives

In one paragraph: why does Capsule build SshRTC and `capsule stream` both on WebRTC instead of using OpenVPN + SSH + VNC? Cite one specific WebRTC capability (ICE traversal, codec negotiation, etc.) that explains the choice.

---

## Problem Set 40 — Reliability & Diagnostics (consolidation)

### Problem 40.1 ★ — The race

Facilitator simulates 3 breakages live in class. For each, write the diagnostic sequence you would run and the recovery step. Submit afterward with the actual root cause your team identified.

### Problem 40.2 ★ — Anatomy of a useful bug report

Write a *full* Capsule bug report for any anomaly you saw this week, real or simulated. Required fields: version, status output, exact reproducer, error text, frequency, what you already tried. Length target: 1 page.

### Problem 40.3 ★ — The cleanup question

Read `capsule cleanup`'s help text. Answer: what *exactly* does it touch on disk? What would still be wrong after running it? When is cleanup *not* the right first step?

### Problem 40.4 ☆ — Build a diagnostic script

Write a shell script `capsule-doctor.sh` that runs the full diagnostic sequence and prints a colored summary. Commit it. (Bonus: support `--json` for ingestion by an MCP-aware agent.)

### Problem 40.5 ☆ — Postmortem the simulation

Pick one of the 3 simulated breakages from 40.1. Write a 1-page postmortem with: timeline, root cause, contributing factors, what would have prevented it, and one Capsule design change that would have made it impossible.

---

## Problem Set 41 — Your First Benchmark

### Problem 41.1 ★ — Baseline benchmark

Run `capsule benchmark` on Llama-3.1-8B-Instruct at FP16, concurrency=1, on a 1×H100. Submit raw output and the four-row "key metrics" table (TTFT P50/P95, ITL P50/P95, TPS, throughput).

### Problem 41.2 ★ — Predict, then measure

*Before* running 41.1, write your prediction for TTFT P95 and TPS. Submit the prediction file timestamped before the benchmark run. Compute your error (% over/under). The act of predicting first is the rep that trains intuition.

### Problem 41.3 ★ — Explain every metric

For each metric in 41.1's output, write one sentence explaining what it measures using *Phase-1 vocabulary* (refer to Week 4). If a metric appears that isn't in your Week-4 notes, look it up and add it.

### Problem 41.4 ☆ — Benchmark variance

Re-run 41.1 three times back-to-back. Report the variance in each metric. Which is most variable? Speculate on the source of the variance.

### Problem 41.5 ☆ — Two backends

Run the same benchmark using two different `--backend` values (vLLM vs SGLang, or vLLM vs TRT-LLM if both are available). Report the deltas. Which backend "won" on which metric?

---

## Problem Set 42 — Varying Parameters

### Problem 42.1 ★ — Concurrency sweep

Run `capsule benchmark` at concurrencies 1, 2, 4, 8, 16, 32 (model + GPU held constant). Plot throughput vs concurrency on one axis, P95 TTFT on another. Identify "the knee."

### Problem 42.2 ★ — Quantization sweep

Same model, three quantizations: FP16 → FP8 → INT4. Same concurrency. Report TTFT, TPS, and a one-sentence quality verdict per quant (you'll do the proper eval Day 43).

### Problem 42.3 ★ — Multi-GPU (`--tp`)

If your model is large enough (try Llama-3.1-70B), run `--tp 1` vs `--tp 2` vs `--tp 4`. Report throughput per GPU (not just total). Is parallelism free or are you paying overhead?

### Problem 42.4 ☆ — One-variable discipline

Take a sweep table from a teammate. Identify any row where they accidentally varied two variables at once. Propose the additional rows needed to disentangle.

### Problem 42.5 ☆ — Cost-aware sweep

For your 42.1 sweep, compute $/1M output tokens at each concurrency level (use $2/H100-hr). Identify the concurrency that *minimizes cost per token*. Is it the same as the throughput-maximizing point? Explain.

---

## Problem Set 43 — Interactive Evaluation

### Problem 43.1 ★ — Five-prompt eval

Write 5 prompts covering: factual recall, math, code generation, formatting, refusal/safety. Each must have a *machine-checkable* expected behavior. Submit the prompts + criteria.

### Problem 43.2 ★ — FP16 vs FP8 chat

Run your 5-prompt eval against FP16 and FP8 of the same model via `capsule chat`. Score each. Report any prompt where the FP8 model failed but FP16 passed.

### Problem 43.3 ★ — Quantization-regression hunt

Find *one* prompt (yours or a teammate's) where INT4 silently regresses — i.e., it produces a plausible-sounding but wrong answer. Submit the prompt, both outputs, and the explanation of why benchmarking alone wouldn't have caught it.

### Problem 43.4 ☆ — Refusal-eval study

Run a refusal/safety prompt against three quantization tiers of the same model. Quantized models often become *over-eager*. Did yours? Quantify.

### Problem 43.5 ☆ — Eval-as-code

Convert your 5-prompt eval to a single shell script that runs each prompt, captures the output, and prints PASS/FAIL using `grep` or `jq`. Commit. (This is what `capsule schedule` will run for you Day 44.)

---

## Problem Set 44 — Scheduling & MCP

### Problem 44.1 ★ — Schedule the eval

Submit your 43.5 eval script via `capsule schedule start`. Monitor with `capsule schedule status` and `capsule schedule logs --tail`. Submit the resulting log + the final PASS/FAIL summary.

### Problem 44.2 ★ — Cancel-and-resume

Submit a deliberately long benchmark via `capsule schedule start`, monitor its progress for 60 seconds with `capsule schedule status` / `logs`, then `capsule schedule cancel <job-id>`. Verify resources are released. Re-submit with adjusted parameters. Submit timestamps + commands.

### Problem 44.3 ★ — MCP manifest

Run `capsule mcp --output > capsule-mcp.json`. Open the file. For each exposed tool, write a one-line description in your own words. Identify any tool whose description in the manifest is unclear enough that you would rewrite it.

### Problem 44.4 ☆ — Agent + Capsule

Connect a Claude Desktop / Cursor / VS Code Copilot client to your local `capsule mcp` server. Ask the agent to list machines, then to start a benchmark. Submit screenshots of the agent calling the tools. Reflect: what surprised you?

### Problem 44.5 ☆ — Governance overlay

For the agent in 44.4: what blast-radius reduction would you apply *before* letting it run unsupervised? Propose one filter (which tools to expose) and one observability control (how to audit calls). Reference Week 7 Day 33 vocabulary.

---

## Problem Set 45 — End-to-End Sprint

### Problem 45.1 ★ — The 20-minute sprint

Timed: find a machine → run a benchmark → run an eval → record results → commit. 20-minute cap. Submit your timing breakdown per phase. If you went over time, identify the phase that ate the most clock and propose the one-shot fix.

### Problem 45.2 ★ — Phase-by-phase reflection

For each of the 4 sprint phases, write the *one* command that ended up being most important. Argue why.

### Problem 45.3 ★ — Cross-phase lesson

In ≤ 200 words: what did the sprint teach you that the 9 days of structured labs did not? Be specific.

### Problem 45.4 ☆ — Document the sprint as a runbook

Convert your sprint into a copy-paste runbook a new intern could follow next year. Commit to `practice/runbooks/`.

### Problem 45.5 ☆ — Capstone preview

Pre-write the *one-sentence deliverable* template (from the Capstone Guide) for the use case you'd most want to do in Week 10. Don't fill in real numbers — fill in the structure. This is your pre-charter draft.

---

## Appendix — Per-set difficulty index

| Set | Easiest | Hardest | Required total |
|---|---|---|---|
| 36 | 36.1 | 36.5 | 3 ★ |
| 37 | 37.1 | 37.4 | 3 ★ |
| 38 | 38.1 | 38.5 | 3 ★ |
| 39 | 39.1 | 39.5 | 3 ★ |
| 40 | 40.3 | 40.5 | 3 ★ |
| 41 | 41.1 | 41.5 | 3 ★ |
| 42 | 42.1 | 42.5 | 3 ★ |
| 43 | 43.1 | 43.3 | 3 ★ |
| 44 | 44.1 | 44.5 | 3 ★ |
| 45 | 45.1 | 45.4 | 3 ★ |

Total required problems for the two-week phase: **30** (the ★ problems). Stretch problems are scored separately and feed the capstone "engineering reasoning" rubric.

---

## Appendix — Concept-graph IDs covered

| Problem set | Concept IDs |
|---|---|
| 36 | `capsule.auth.b2c`, `capsule.connect.sshrtc`, `capsule.connect.direct` |
| 37 | `capsule.fleet.env`, `capsule.fleet.customer` |
| 38 | `capsule.connect.tag_vs_uid`, `capsule.connect.sshrtc`, `capsule.connect.direct` |
| 39 | `capsule.storage.onedrive`, `capsule.stream.webrtc`, `capsule.container.docker` |
| 40 | `capsule.diag.daily_loop`, `capsule.diag.cleanup` |
| 41 | `capsule.bench.runner`, `inference.metrics.ttft`, `inference.metrics.tps` |
| 42 | `capsule.bench.runner`, `inference.batching.concurrency`, `inference.quant.fp8` |
| 43 | `capsule.eval.chat`, `eval.refusal`, `inference.quant.regression` |
| 44 | `capsule.ops.schedule`, `capsule.ops.mcp`, `agent.mcp` |
| 45 | (synthesis — all of the above) |
