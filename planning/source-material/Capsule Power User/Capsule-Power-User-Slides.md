<!-- Slide number: 1 -->

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)
CAPSULE
Power-User Curriculum
Reliability & Model Evaluation · Intern Track
10 modules · 2 days · Hands-on labs

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image1.jpg)

### Notes:

<!-- Slide number: 2 -->

CURRICULUM
Ten modules. One mental model.

MODULE

TITLE

LAB FOCUS

1

Capsule Foundations

Mental model

2

Installation & First Login

Get the CLI working

3

Environments & Customers

Routing to the right fleet

4

The Fleet: Listing & Filtering

Finding the right machine

5

Connecting to Machines

term · exec · code · cursor · claude

6

Files, Storage & OneDrive

Persistent data

7

Streaming & Containers

Desktop, app, docker

8

Benchmarking (InferenceMAX)

Model evaluation runs

9

Interactive Chat

Hands-on model probing

10

Scheduling & Reliability Toolkit

Long jobs and triage

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

2

### Notes:

<!-- Slide number: 3 -->

MODULE 1
CAPSULE FOUNDATIONS

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 4 -->

MODULE 1 · CONCEPT
What Capsule actually is
Your laptop is a thin client. The CPU, GPU, RAM, and disk live on remote machines. Capsule pipes shells, IDEs, and full desktops back to you.

SshRTC (default)
WebRTC peer connection carries SSH
No public-facing port required
NAT traversal handled for you
Use for: everyday work

Direct SSH (--direct)
Plain TCP SSH connection
Requires reachable SSH port
Cleaner port-forwarding
Use for: WebRTC fallback, port forwards

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

4

### Notes:

<!-- Slide number: 5 -->

MODULE 1 · ROUTING
Two dimensions decide which fleet you see

ENV

B2C TENANT

TYPICAL USE

prod

mihirainfra.b2clogin.com

Internal production

public

oxcapsule.b2clogin.com

External / partner

dev

mihirainfra.b2clogin.com

Development / testing

demo

mihirainfra.b2clogin.com

Demonstrations

RELIABILITY LENS
When a report says 'Capsule isn't working,' the first four questions are: which environment, which customer, is the token expired, is SshRTC failing? Most incidents resolve on the first three before you look at logs.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

5

### Notes:

<!-- Slide number: 6 -->

MODULE 2
INSTALLATION & FIRST LOGIN

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 7 -->

MODULE 2 · SETUP
Same moving parts on every OS

Prerequisites
GH_TOKEN with scopes: repo, read:org, workflow, user
gh CLI (Windows/Linux)
Homebrew (macOS)
rclone (auto on macOS)

Install paths
macOS: brew tap + brew install capsule
Windows: gh release download + tar -xzf
Linux: gh release download + tar -xzf
Verify: capsule --version

First-time auth
capsule auth login (browser flow)
Fallback: paste manual token at oxmiq.ai/oxcapsule/auth
capsule status : confirm identity & expiry
capsule auth storage : OneDrive consent

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

7

### Notes:

<!-- Slide number: 8 -->

MODULE 2 · LAB
macOS install (run this exact sequence)

export HOMEBREW_GITHUB_API_TOKEN=$GH_TOKEN
brew tap mihira-ai/software-packages \
  https://$GH_TOKEN@github.com/mihira-ai/software-packages.git
brew install capsule

capsule --version          # confirm install
capsule auth login         # browser-based
capsule status             # identity + expiry
capsule auth storage       # OneDrive OAuth

RELIABILITY LENS
'Install is broken' almost always traces to GH_TOKEN. Ask in order: is it set, do scopes match, is HOMEBREW_GITHUB_API_TOKEN in the same shell, was PowerShell restarted after the env var was set?

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

8

### Notes:

<!-- Slide number: 9 -->

MODULE 3
ENVIRONMENTS & CUSTOMERS

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 10 -->

MODULE 3 · ROUTING
Switching environments and customers

capsule env show
capsule env set public
capsule auth login           # always re-auth after env switch

capsule config customer show
capsule config customer set modelhosting
capsule config customer unset

RELIABILITY LENS
If 'machine X disappeared,' check the customer override before anything else. It persists across sessions and gets set by setup scripts more often than people remember. capsule config customer show is your first command.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

10

### Notes:

<!-- Slide number: 11 -->

MODULE 4
THE FLEET : LISTING & FILTERING

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 12 -->

MODULE 4 · LISTING
Config tag vs unique ID

Config tag
Pool / class name
Scheduler hands you any available member
Example: capsule term gpu-workstation-01

Unique ID
Specific physical machine
Always paired with -u / --unique
Example: capsule term -u boostergold461

capsule list                                    # by pool
capsule list --all                              # unique IDs
capsule list --filter "vendor=nvidia,vram>=24"
capsule list --filter "os=linux,cores>=64"
capsule list --users                            # who is logged in

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

12

### Notes:

<!-- Slide number: 13 -->

MODULE 5
CONNECTING TO MACHINES

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 14 -->

MODULE 5 · SESSIONS
Five commands, one routing language

COMMAND

OPENS

capsule term

Remote shell over SshRTC (aliases: terminal, ssh, launch)

capsule exec

Single command on the remote, then exit

capsule code

VS Code with Remote-SSH attached

capsule cursor

Cursor with Remote-SSH attached

capsule claude

Claude Code Desktop on the remote

SHARED FLAGS
Positional <config-tag> or -u <unique-id>. --direct bypasses WebRTC. --idle-timeout and --max-session-length bound the session. code and cursor also accept --repo. claude does not.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

14

### Notes:

<!-- Slide number: 15 -->

MODULE 5 · LAB
Connection drills

capsule term <tag>                              # interactive shell
capsule term <tag> -e "nvidia-smi"              # one-shot command
capsule code <tag> --repo mihira-ai/<repo>      # VS Code + repo clone
capsule term <tag> --direct \
    --options "-L 3000:localhost:3000"          # port-forward via direct
capsule term <tag> --idle-timeout 2h --max-session-length 8h

RELIABILITY LENS
Cleanup + retry before --direct fallback. Always set timeouts for batch-like work. Don't leave stale capsule-<id> blocks in ~/.ssh/config : they break Remote-SSH cryptically.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

15

### Notes:

<!-- Slide number: 16 -->

MODULE 6
FILES, STORAGE & ONEDRIVE

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 17 -->

MODULE 6 · DATA
Three ways to move bytes

OneDrive auto-mount
capsule auth storage : once
Auto-mounts ~/OneDrive on every session
Same folder on every machine
Best for: shared eval data

capsule scp
capsule scp upload <tag> src dst
capsule scp download <tag> src dst
Add --direct if SshRTC misbehaves
Best for: one-off large blobs

File passthrough
capsule config files add .gitconfig ~/.gitconfig
Copied at session start
Best for: small dotfiles

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

17

### Notes:

<!-- Slide number: 18 -->

MODULE 7
STREAMING & CONTAINERS

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 19 -->

MODULE 7 · STREAMING
Desktops, apps, and Docker

capsule stream <tag>                            # full desktop
capsule stream <tag> --app "blender"            # single app

capsule docker <tag> --image pytorch/pytorch:latest --memory 16
capsule docker <tag> --image nvidia/cuda:12.0-devel \
    --command "python train.py" \
    --volume "/data:/data:ro;/workspace:/workspace"
capsule docker <tag> -- --gpus all              # pass docker args

WEBRTC NOTE
Hardware encoding via NVENC / VAAPI / VideoToolbox. Bandwidth-sensitive: video drops first, then audio, then input lag. Before blaming the encoder for 'lag,' confirm the user's downlink with a separate speed test.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

19

### Notes:

<!-- Slide number: 20 -->

MODULE 8
BENCHMARKING : INFERENCEMAX

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 21 -->

MODULE 8 · BACKENDS
Pick the right inference backend

BACKEND

WHEN TO USE

vllm

Default. NVIDIA, batched serving, paged attention

llamacpp

CPU-friendly, GGUF quantizations (Q4_K_M, Q5_K_M)

mlx

Apple Silicon

oxpython

OXMIQ Python runtime for in-house eval paths

capsule benchmark <tag> meta-llama/Llama-3.1-8B-Instruct \
    --concurrency 8 --input-length 256 --output-length 256 \
    --num-prompts 40 --tensor-parallelism 1
capsule benchmark <tag> <model> --quant awq

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

21

### Notes:

<!-- Slide number: 22 -->

MODULE 8 · KNOBS
Read every flag like a dial

FLAG

MEANING

DEFAULT

--concurrency / -c

max-num-seqs (batch size)

4

--input-length / --isl

Tokens per prompt

128

--output-length / --osl

Tokens generated per response

128

--num-prompts / -n

Total requests sent

concurrency × 10

--tensor-parallelism / --tp

Split model across N GPUs

1

--quant / -q

awq, gptq, fp8, int8, Q4_K_M, Q5_K_M

--api-base / --api-key

Benchmark an existing endpoint

DASHBOARD
Results uploaded to oxcapsulebenchmark.z22.web.core.windows.net unless --no-upload is set. Use --idle-timeout and --max-session-length longer than your expected run.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

22

### Notes:

<!-- Slide number: 23 -->

MODULE 9
INTERACTIVE CHAT

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 24 -->

MODULE 9 · CHAT
Spin up, probe, tear down

capsule chat <tag> meta-llama/Llama-3.1-8B-Instruct

capsule chat <tag> <model> --temperature 0.3 --max-tokens 2048 \
    --system-prompt "You are a helpful coding assistant."

capsule chat <tag> <model> --hf-token $HF_TOKEN --tp 4 --rm

RELIABILITY LENS
When a customer says 'the model is broken,' reproduce on the same machine with capsule chat -u <unique-id> using their sampling settings. If it works for you, the issue is in their client config, not the inference path.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

24

### Notes:

<!-- Slide number: 25 -->

MODULE 10
SCHEDULING & RELIABILITY TOOLKIT

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 26 -->

MODULE 10 · SCHEDULING
Long jobs run unattended

capsule schedule start <tag> --script ./train.sh \
    --name "training-v2" --timeout 8h --retry 3

capsule schedule status <tag> --me --state running --show-start
capsule schedule logs <job-id> --tail 100
capsule schedule cancel <job-id>
capsule schedule cancel --all

WHEN TO REACH FOR IT
Anything longer than a coffee break. Benchmarks, evals, training. Don't tie up a GPU on an interactive session that no human will be looking at for hours.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

26

### Notes:

<!-- Slide number: 27 -->

MODULE 10 · TRIAGE
Known-quirks table : memorise this

SYMPTOM

FIX

Auth fails in browser flow

Manual token at oxmiq.ai/oxcapsule/auth

capsule list shows wrong machines

Check env show + config customer show

SshRTC won't connect

cleanup, retry, then --direct fallback

VS Code Remote-SSH fails after a session

Remove capsule-<id> blocks from ~/.ssh/config

macOS Keychain prompts every command

Click 'Always Allow' once

PowerShell filter with > fails

Use capsule (not cap) and quote the argument

capsule update fails

Token valid; close all SshRTC sessions first

gh release download 401/403

Re-check GH_TOKEN scopes

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

27

### Notes:

<!-- Slide number: 28 -->

MODULE 10 · TOOLKIT
Commands you'll run during every triage

capsule status                # auth, identity, expiry
capsule env show              # current environment
capsule config customer show  # current fleet
capsule cleanup               # tear down stale WebRTC + SSH state
capsule --version             # exact build for bug reports
capsule --no-banner list      # clean output for tickets

TRIAGE SHAPE
(1) Reproduce yourself : no repro = incident not bug. (2) Capture version, env, customer, command, timestamp, unique ID. (3) Try cleanup + --direct before escalating. (4) Default long work to capsule schedule.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

28

### Notes:

<!-- Slide number: 29 -->

MODULE C
CAPSTONE : BENCH-TO-DASHBOARD ROUND TRIP

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)

### Notes:

<!-- Slide number: 30 -->

CAPSTONE · END-TO-END
Under 30 minutes once you've done it
01.  Confirm env=prod, customer=micc
02.  Find NVIDIA machine ≥24 GB VRAM with no active users
03.  Open VS Code via SshRTC; verify nvidia-smi from integrated terminal
04.  Upload prompts.txt to /workspace/ via SCP
05.  Benchmark Llama-3.1-8B-Instruct, concurrency 8, ISL 256, OSL 256
06.  Re-run with --quant awq; compare throughput
07.  Find both runs on the dashboard
08.  Schedule the same benchmark with a 1-hour timeout
09.  Run capsule chat against the same model while the job runs
10.  capsule cleanup; verify with capsule list --users

TARGET
Under 30 minutes. Reliability work is mostly muscle memory.

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-dark.png](Image0.jpg)

ARCHITECTING ATOMS TO AGENTS

30

### Notes:

<!-- Slide number: 31 -->

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image0.jpg)
WELCOME TO THE TEAM
Architecting atoms to agents : one capsule at a time.
Questions: ask your instructor · #capsule-help on Discord

![/sessions/lucid-elegant-hopper/mnt/outputs/assets/logos/OXMIQ-logo-white.png](Image1.jpg)

---

# Instructor Appendix — Per-Module Delivery Kit

This appendix is for the person delivering the deck. The 31 slides above carry the content; this appendix carries the *room dynamics* — what to anchor in numbers, what to ask, how to budget time, and what tends to go wrong in front of live interns.

## How to use this appendix

For each module you'll find:
- **Numerical anchors** — 2-3 numbers to write on the board before you start.
- **Ask-the-room prompts** — 4 questions designed to surface the misconceptions worth correcting in-session.
- **Time budget** — minute-by-minute pacing within the module's 90-min slot.
- **Calibration notes** — what landed / didn't land in prior cohorts, and how to course-correct mid-flight.

Mid-module energy checks and a course-wide closing-discussion ladder follow at the end.

---

## Module 1 — Capsule Foundations

**Numerical anchors**
- **16** routing cells (4 env × 4 customer). Write the 4×4 grid on the board.
- **~200 machines** in the combined fleet (mid-2026).
- **2 transports**: SshRTC (default, <80ms keystroke echo) vs. Direct SSH (<40ms, fallback).

**Ask-the-room prompts**
1. *"How is Capsule different from SSH-ing to a lab machine?"* — surfaces the routing layer.
2. *"If your laptop's wifi drops, which transport will recover first?"* — SshRTC re-negotiates; Direct SSH drops the TCP.
3. *"You're shown an empty `capsule list`. What are the top 3 things you check?"* — env, customer, auth.
4. *"Why two transports and not one?"* — NAT traversal vs. clean port-forwarding.

**Time budget (90 min)**
- 0-10: framing + 4×4 grid on the board
- 10-30: lecture (slides 1-8)
- 30-50: worked-example walkthrough (a "what fleet am I on?" puzzle)
- 50-75: pair exercise from the Workbook
- 75-90: critical analysis + preview of Module 2

**Calibration notes**
- *Failure to land*: interns nod through the env×customer matrix but later confuse them. Fix: have them draw the grid in their notebook before slide 4.
- *Common derail*: someone asks about pricing. Defer to Module 10. Don't get pulled in.

---

## Module 2 — Installation & First Login

**Numerical anchors**
- **~5 minutes** clean-path install on a fresh MacBook (brew + tap + bottle + login + list).
- **~60 min** auth token TTL — expired tokens are the #1 "Capsule broke" non-bug.
- **3 OSes** supported: macOS (brew), Linux (deb), Windows (msi).

**Ask-the-room prompts**
1. *"What does `brew tap` actually do?"* — establishes the bottle-vs-source-build mental model.
2. *"Your `capsule list` returns 401 at 3pm. What was true at 2pm?"* — token TTL.
3. *"Why a browser-based device-code flow instead of password?"* — B2C, MFA, audit.
4. *"Install fails behind the lab proxy. What's the diagnostic order?"* — DNS → proxy → cert.

**Time budget (90 min)**
- 0-10: recap Module 1
- 10-25: install demo on a fresh box (live)
- 25-45: students install on their own laptops
- 45-65: troubleshooting clinic (deliberately break a few installs)
- 65-80: first benchmark together
- 80-90: synthesis + Module 3 preview

**Calibration notes**
- *Failure to land*: someone's corporate laptop blocks the brew tap. Have them pair with a neighbor; assign as homework.
- *Common derail*: package-manager religion ("why brew?"). Acknowledge once, move on.

---

## Module 3 — Environments & Customers

**Numerical anchors**
- **4 envs** × **4 customers** = **16 cells**.
- **20 min** average ticket time saved by leading triage with env+customer.
- **2 production envs**: `prod` (internal) and `public` (external customers).

**Ask-the-room prompts**
1. *"What's the difference between `prod` and `public`?"* — both are production.
2. *"A user says 'deploy failed.' What's your first question?"* — env+customer.
3. *"Why are customers not the same as B2C tenants?"* — fleet selectors vs. identity tenants.
4. *"Can the same physical machine appear under two customers?"* — no.

**Time budget (90 min)**
- 0-10: recap; surface env/customer matrix again
- 10-30: lecture (slides for Module 3)
- 30-50: routing puzzles (instructor reads a CLI command, students name env+customer)
- 50-75: lab — switch env+customer 5 times, confirm fleet changes
- 75-90: critical analysis + preview

**Calibration notes**
- *Failure to land*: interns set the env once and forget. Force them to re-state env+customer at the start of every CLI session.

---

## Module 4 — The Fleet: Listing & Filtering

**Numerical anchors**
- **~200 machines** combined; **~120 NVIDIA**, **~40 Tenstorrent**, **~20 AMD MI300**, **~20 Apple Silicon**.
- **8-12 hits** is the right magnitude for a narrow filter (e.g., `nv-h100`).
- **0 hits** = you've drifted env or customer.

**Ask-the-room prompts**
1. *"Config tag or unique ID for a benchmark?"* — config tag (pool average).
2. *"Config tag or unique ID for reproducing a bug?"* — unique ID (same box).
3. *"`capsule list --config nv-h100` returns 0. What happened?"* — env/customer drift.
4. *"Why do scheduler reservations matter even for `list`?"* — `--free` filter.

**Time budget (90 min)**
- 0-10: recap
- 10-25: lecture on config tag vs. unique ID
- 25-50: live filter walkthrough on the real fleet
- 50-75: lab — find specific hardware classes; identify "needle" machines
- 75-90: synthesis

**Calibration notes**
- *Common derail*: a config tag returns surprising hardware. Use it as a teaching moment about how the scheduler defines pools.

---

## Module 5 — Connecting to Machines

**Numerical anchors**
- **5 verbs**: `term`, `exec`, `code`, `cursor`, `claude`.
- **<80ms** SshRTC keystroke echo (target); **<40ms** Direct SSH.
- **~2 sec** attach time for an MCP-enabled `claude` session.

**Ask-the-room prompts**
1. *"Which verb for a one-shot `nvidia-smi`?"* — `exec`.
2. *"Which for editing a Python file with autocomplete?"* — `code` or `cursor`.
3. *"Which to debug a hung benchmark with AI assistance?"* — `claude`.
4. *"When do you reach for `--direct`?"* — WebRTC peer fail (not slow networks).

**Time budget (90 min)**
- 0-10: recap
- 10-25: lecture — 5-verb matrix
- 25-50: live demo of each verb on the same box
- 50-75: lab — students pair, pick the right verb for 5 scenarios
- 75-90: critical analysis

**Calibration notes**
- *Failure to land*: interns default to `term` for everything. Make them justify the verb choice in their notes.

---

## Module 6 — Files, Storage & OneDrive

**Numerical anchors**
- **3 storage scopes**: ephemeral (`/tmp`), persistent volume (`/home/$USER`), OneDrive (`~/OneDrive`).
- **>1 GB/s** local NVMe write; **<5 MB/s** OneDrive sustained.
- **7 days** default log retention.

**Ask-the-room prompts**
1. *"Where do your benchmark outputs land by default?"* — persistent volume.
2. *"You want to compare results across two boxes. Where do you write?"* — OneDrive.
3. *"You're done with a 50GB dataset. Which scope do you nuke first?"* — ephemeral if possible.
4. *"OneDrive is a backup. True or false?"* — false; it's a sync.

**Time budget (90 min)**
- 0-15: recap + storage-scope tree on the board
- 15-35: lecture
- 35-60: lab — write a file in each scope, observe behavior across restart and across machines
- 60-80: triage exercise — "where did my data go?"
- 80-90: synthesis

**Calibration notes**
- *Common derail*: someone deletes a OneDrive file and panics. Use as a teaching moment about sync semantics.

---

## Module 7 — Streaming & Containers

**Numerical anchors**
- **Desktop streaming**: ~30 FPS, 5-15 Mbps.
- **App streaming**: ~60 FPS, 3-8 Mbps.
- **Container shell**: ~0 Mbps video, text only.

**Ask-the-room prompts**
1. *"You need to run `pytest` for 30 min. What surface?"* — container shell, not desktop.
2. *"You need to demo a GUI app to a customer. What surface?"* — app streaming.
3. *"Docker on Capsule is a security sandbox. True or false?"* — false.
4. *"What does the encoder cost you?"* — ~1 GPU encoder slot per stream.

**Time budget (90 min)**
- 0-10: recap
- 10-30: lecture — 3 surfaces compared
- 30-55: lab — open each surface on the same box
- 55-80: cost-of-surface exercise — for 5 scenarios, pick + justify
- 80-90: synthesis

---

## Module 8 — Benchmarking

**Numerical anchors**
- **1500-2500 tok/sec** decode (Llama-3.1-8B, single stream, H100).
- **10K-30K tok/sec** batched throughput.
- **≥3 runs** required for variance reporting (median + p95).
- **~$0.05 per M-tokens** batched at $2/H100-hour.

**Ask-the-room prompts**
1. *"You see 800 tok/sec decode on an H100. What's wrong?"* — thermal / driver / PCIe.
2. *"Is one benchmark run a measurement?"* — no, it's a sample.
3. *"Why config tag, not unique ID, for benchmarks?"* — pool average, fair comparison.
4. *"What does TTFT capture that throughput misses?"* — first-token latency.

**Time budget (90 min)**
- 0-10: recap
- 10-30: lecture — InferenceMAX overview, what gets measured
- 30-60: lab — run a benchmark, read the output sheet
- 60-80: variance exercise — run 5×, compute median/p95
- 80-90: synthesis

**Calibration notes**
- *Failure to land*: interns report a single number. Make them report median + p95 always.

---

## Module 9 — Interactive Chat

**Numerical anchors**
- **~2 min** to first signal in interactive probing; **~2 hours** to construct a batch eval for the same insight.
- **30% reproduction rate** is the threshold above which a "weird behavior" is a real bug.
- **Manual log** — chat is not auto-archived.

**Ask-the-room prompts**
1. *"Chat surfaces a weird output. What's your N before you write a ticket?"* — at least 5-10 attempts.
2. *"When does chat beat a benchmark?"* — qualitative failure modes.
3. *"When does a benchmark beat chat?"* — anything you need to quantify or trend.
4. *"What do you do with an interesting transcript?"* — copy into incident notes immediately.

**Time budget (90 min)**
- 0-10: recap
- 10-25: lecture — chat as a probing tool
- 25-55: lab — chat with a deployed model, surface 2-3 failure modes
- 55-80: pair exercise — design a probing protocol for a real bug
- 80-90: synthesis

---

## Module 10 — Scheduling & Reliability Toolkit

**Numerical anchors**
- **6-hour serial → 90-min parallel** on a typical 8-model sweep with 4 GPUs.
- **$12 per sweep** at $2/GPU-hour × 4 GPUs × 1.5 hours.
- **7 days** log retention; pull within window.

**Ask-the-room prompts**
1. *"You forget `--parallel` on a 6-hour sweep. What's the cost?"* — 4.5 hours wall-clock.
2. *"A scheduled job is a service. True or false?"* — false; finite lifetime.
3. *"Logs aged out. What's recoverable?"* — only what's in OneDrive or persistent volume.
4. *"What's the first command in any triage?"* — `capsule list --users` to see who's on what.

**Time budget (90 min)**
- 0-15: recap + the full triage tree on the board
- 15-35: lecture — scheduling primitives + reliability tools
- 35-65: lab — schedule a real sweep
- 65-85: triage simulation — instructor injects a fault; students walk the tree
- 85-90: course closing

**Calibration notes**
- *Failure to land*: interns submit unmonitored jobs and lose work. Require them to print the recovery plan before submission.

---

## Mid-module energy checks

- **At minute 45 of every module**: ask "what's the single thing on these slides that would change your work tomorrow?" Five-second silence is OK.
- **Before any lab**: count hands for "I've done something like this before." If <30%, slow down. If >70%, skip the warm-up.
- **After a dense slide**: deliberately re-explain in a one-sentence summary, then ask "did that match what I just said?"

## Course-wide closing-discussion ladder

End the course (or each day) by walking up this ladder of questions:
1. *What's the one Capsule command you'll use this week?*
2. *What's the most common failure mode you expect to see in your team's work?*
3. *Where does Capsule end and the broader OXMIQ stack (oxgate, oxfactory, model-hosting) begin?*
4. *What would you redesign about Capsule if you owned it?*

Questions 1-2 are warm-up. Question 3 surfaces system thinking. Question 4 is the "are they a power user yet?" test — if they answer with a specific UX or reliability gap, they've internalized the course.

## Concept-graph cross-reference

| Module | Primary concept IDs |
|---|---|
| 1 — Foundations | `capsule-fleet`, `capsule-routing`, `sshrtc-transport` |
| 2 — Install | `capsule-install`, `oxgate-auth`, `b2c-tenant` |
| 3 — Env/Customer | `capsule-env`, `capsule-customer`, `b2c-tenant` |
| 4 — Fleet | `capsule-fleet`, `config-tag`, `unique-id` |
| 5 — Connect | `capsule-connect`, `sshrtc-transport`, `mcp-server` |
| 6 — Storage | `capsule-storage`, `onedrive-mount`, `persistent-volume` |
| 7 — Streaming | `capsule-streaming`, `webrtc-encoder`, `docker-runtime` |
| 8 — Benchmark | `inferencemax`, `benchmark-variance`, `gpu-throttling` |
| 9 — Chat | `interactive-eval`, `model-deployment`, `prompt-probing` |
| 10 — Schedule | `capsule-scheduler`, `parallel-execution`, `log-retention` |

### Notes: