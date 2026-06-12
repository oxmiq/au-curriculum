# Capsule Power-User — Flashcards

*Spaced-repetition flashcards for Weeks 8–9. Format: `Q` on one side, `A` on the other. Use Anki, Mochi, or any SR tool — or just cover the answer column and self-test. ~55 cards organized by day, plus a "command-recall under time pressure" tier for the Day 45 sprint.*

---

## Day 36 — Architecture & Installation

| # | Q | A |
|---|---|---|
| 1 | What are the two connection paths in Capsule? | SshRTC (WebRTC-tunneled SSH, works through NAT/firewall) and `--direct` (raw TCP, lower latency, requires reachable endpoints). |
| 2 | Capsule's three-tier architecture? | `client → server → cloud`. Client = your CLI, server = orchestration plane, cloud = GPU fleet + identity (B2C). |
| 3 | Why does Capsule use browser-flow auth on first run? | OAuth via Azure B2C: user creds never touch the CLI, tokens are scoped and revocable, and re-auth happens through the IdP's standard UX. |
| 4 | First three commands to verify a working install? | `capsule --version`, `capsule auth login`, `capsule status`. |
| 5 | Headless / CI auth — what's the mechanism? | `export CAPSULE_AUTH_TOKEN=<token>` (token obtained via `capsule auth token` on a normal box). |

---

## Day 37 — Environments & Fleet Discovery

| # | Q | A |
|---|---|---|
| 6 | Name the four Capsule environments. | `prod` (internal), `public` (external/partner), `dev`, `demo`. |
| 7 | Which B2C tenant maps to `prod`? | `mihirainfra.b2c`. (`public` ↔ `oxcapsule.b2c`.) |
| 8 | Why does `capsule env set` force re-auth? | Each env uses a different B2C tenant with its own user registry — your `prod` identity literally doesn't exist in `public` without separate provisioning. |
| 9 | The "wrong machines in `capsule list`" — first command to check? | `capsule config customer show`. Customer context drives fleet selection. |
| 10 | Name three customer contexts. | `micc` (default), `modelhosting`, `oneplay`. (Also `cree8` and others.) |
| 11 | Filter expression for "Nvidia GPUs with ≥80 GB VRAM"? | `--filter "vendor=nvidia,vram>=80"` |
| 12 | What's special about `--filter` in PowerShell? | Must be quoted; `>` is redirection in PS so unquoted `vram>=80` breaks. Also use `capsule`, not `cap`. |

---

## Day 38 — Connecting to Machines

| # | Q | A |
|---|---|---|
| 13 | When to use `capsule term` vs `capsule exec`? | `term` for interactive shell (exploration). `exec` for one-off scripted commands (automation, CI). |
| 14 | Tag-routing vs unique-ID routing — when each? | Tag: "any L4 is fine" (parallel work, fungible boxes). Unique-ID (`-u`): "this specific box I set up state on." |
| 15 | Three editor connectors? | `capsule code` (VS Code Remote-SSH), `capsule cursor`, `capsule claude` (Claude Code Desktop). |
| 16 | When does `--direct` win? | When both endpoints are reachable (corporate net, on-prem, dev box) and you need lower latency for keystroke-sensitive work. |
| 17 | When does `--direct` *lose*? | Symmetric NAT or restrictive firewalls — falls back to nothing. Default to SshRTC on laptops in public networks. |
| 18 | Session-limit error — what to run? | `capsule status` to see what's open, then disconnect what you don't need. Limits exist to prevent fleet squatting. |

---

## Day 39 — Files, Storage & Streaming

| # | Q | A |
|---|---|---|
| 19 | Three ways to move files local↔remote? | OneDrive mount (persistent, cross-machine), `scp` (one-off), dotfile passthrough (config files on first connect). |
| 20 | When is OneDrive the right choice? | Files you'll want on the *next* machine too. Datasets ≤ a few GB, results, eval prompts. |
| 21 | When is `scp` the right choice? | One-off transfer; you won't need the file on other machines. |
| 22 | What does dotfile passthrough do? | Copies a curated set of dotfiles (`.vimrc`, `.zshrc`, `.gitconfig`, …) to the remote on first connect — your shell/editor feel like home immediately. |
| 23 | Why WebRTC for `capsule stream` instead of VNC/RDP? | End-to-end codec negotiation gives much higher frame rate for GPU content; same NAT/firewall traversal as SshRTC. |
| 24 | What does `capsule docker` save you from? | Wiring up `nvidia-container-toolkit` (or vendor equivalent) by hand. The container sees the GPU out of the box. |

---

## Day 40 — Reliability & Diagnostics

| # | Q | A |
|---|---|---|
| 25 | The one command to try first when *anything* about local state looks wrong? | `capsule cleanup`. Safe, idempotent, fixes ~half the "why is this weird" tickets. |
| 26 | The full diagnostic sequence? | `capsule cleanup` → `capsule status` → `capsule env show` → `capsule config customer show` → `capsule list --users` → if still wrong, file a bug. |
| 27 | Four required fields in a useful Capsule bug report? | (1) `capsule --version` (2) `capsule status` output (3) Exact command + flags (4) Full error + the moment it happened. |
| 28 | "I can connect but my VS Code remote crashes" — first hypothesis? | Mixed connection method on the same machine (e.g., earlier `--direct` cached the wrong host key). `capsule cleanup`, then retry. |

---

## Day 41 — Your First Benchmark

| # | Q | A |
|---|---|---|
| 29 | What does `--concurrency` control? | Number of *simultaneous in-flight requests* the benchmark client maintains against the server. Connects to continuous batching from Week 4. |
| 30 | What does `--tp` control? | Tensor parallelism — how the model's weights are sharded across GPUs. Only meaningful for models large enough to need multiple GPUs. |
| 31 | What does TTFT mean? | Time-To-First-Token: latency from request to the first output token. Chat-quality metric. |
| 32 | What does ITL mean? | Inter-Token Latency: gap between successive output tokens during decode. Drives perceived "streaming smoothness." |
| 33 | What does TPS mean? | Tokens-Per-Second: decode rate after the first token. Throughput metric. |
| 34 | What does "throughput" mean (req/sec)? | Completed requests per second across all concurrent in-flight requests. The right number for batch / API-server use cases. |
| 35 | Chat use case — which latency metric matters most? | TTFT P95 (and ITL for streaming smoothness). |
| 36 | Batch summarization — which metric matters most? | Sustained throughput (req/sec or total tokens/sec) at high concurrency. |

---

## Day 42 — Varying Parameters

| # | Q | A |
|---|---|---|
| 37 | The cardinal rule of parameter sweeps? | Vary one knob per run. Hold everything else constant. |
| 38 | Doubling concurrency — throughput goes? | Up, until the GPU saturates ("the knee"), then flat. |
| 39 | Doubling concurrency — P95 latency goes? | Up. Always. Throughput-vs-latency is a real tradeoff. |
| 40 | Doubling concurrency — TTFT P95 goes? | Up. New requests queue behind in-flight ones. |
| 41 | FP16 → FP8 quantization, naive expectation? | ~1.5–2× throughput, ~1.5–2× lower latency, small quality drop. *Verify with eval suite.* |
| 42 | FP8 → INT4 quantization, watch for? | Quality cliffs. Especially math, code, refusal correctness. Don't ship without a careful eval. |

---

## Day 43 — Interactive Evaluation

| # | Q | A |
|---|---|---|
| 43 | One concrete way speed-only benchmarks mislead? | A quantized model can keep TPS high while silently regressing on math or formatting. Eval suite catches it; benchmark alone doesn't. |
| 44 | The 4 categories a structured eval set should cover? | Factual recall, math/reasoning, code generation, refusal/safety. |
| 45 | Why must the eval include a refusal/safety prompt? | Quantized models often become *over-eager* and fail refusals that the FP16 baseline handled. Without this category, you systematically over-rate the quantized variant. |
| 46 | How many prompts is a "good enough" eval suite for the capstone? | 10 minimum. Each with a *machine-checkable* expected behavior. |

---

## Day 44 — Scheduling & MCP

| # | Q | A |
|---|---|---|
| 47 | Why not run a 4-hour benchmark in `capsule term`? | SSH session drops (laptop sleep, network hiccup, screen lock) kill the job. Use `capsule schedule` instead. |
| 48 | `capsule schedule` sub-commands? | `start`, `status`, `logs`, `cancel`. |
| 49 | What does `capsule mcp --output` produce? | An MCP manifest describing Capsule commands as agent-callable tools. |
| 50 | Which clients consume that manifest? | Claude Desktop, Cursor, VS Code Copilot, any MCP-aware agent. |
| 51 | Capsule + MCP = which agent-stack layer is the Capsule CLI? | The Action layer for a deployment agent. (Week 7 Day 32.) |

---

## Day 45 — End-to-End Sprint

| # | Q | A |
|---|---|---|
| 52 | The 4 phases of the timed sprint? | Find machine → benchmark → evaluate → record. |
| 53 | Target time for the full sprint? | 20 minutes. |
| 54 | What's the one "save your data" command you should not forget? | Commit results to git. (`capsule list` output, benchmark output, eval table — all goes in the team repo.) |
| 55 | Before logging off, what command? | `capsule cleanup`. Tomorrow-you will thank today-you. |

---

## Command-recall tier (for Day 45 sprint readiness)

You should be able to type these from memory, no Cheatsheet, in under 5 seconds each. If you can't, drill them.

| Goal | Command (you fill in) |
|---|---|
| List Nvidia H100s in JSON | `capsule list --filter "vendor=nvidia,vram>=80" --json` |
| Connect to specific machine by unique ID | `capsule term -u <unique-id>` |
| Run nvidia-smi non-interactively on first matching tag | `capsule exec <tag> -- nvidia-smi` |
| Open VS Code on a tagged machine via direct TCP | `capsule code <tag> --direct` |
| Submit a benchmark script to run server-side | `capsule schedule start --script ./eval.sh` |
| Emit the MCP manifest for an agent to consume | `capsule mcp --output > capsule-mcp.json` |
| Fix "everything looks weird" local state | `capsule cleanup` |
| Show identity + token expiry | `capsule status` |
| Switch to public env (re-auths) | `capsule env set public` |
| Switch customer context to model hosting fleet | `capsule config customer set modelhosting` |

---

## How to use these cards

- **Daily review** during Weeks 8–9. Aim for ≥90% recall by Day 45.
- **Sprint-prep night** (evening before Day 45): do *only* the Command-recall tier. Three passes. Then sleep.
- **If you got a quantization card wrong** (Q41, Q42, Q45) → re-read Module 9 of the Lab Guide. Don't try to fix the gap during the sprint.
