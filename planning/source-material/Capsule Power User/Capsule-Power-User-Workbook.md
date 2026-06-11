**OXMIQ**

**CAPSULE**

Power-User Workbook

*Reliability & Model Evaluation Track*

Student Name: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Cohort: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

Instructor: \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

# Preface — Why This Course Exists

Capsule is the operational backbone of GPU work at OXMIQ. Every benchmark, every model evaluation, every reliability investigation that touches our hardware fleet runs through it. As an intern on the Reliability & Model Evaluation track, your day-to-day will be: provisioning machines, running structured evaluations, triaging failures, and turning vague reports into reproducible incidents.

This workbook is the written companion to the ten-module Capsule curriculum. Each module mirrors a lecture and lab session. Use it three ways: read it ahead of the lecture, scribble in it during the lab, and keep it as a desk reference once the course ends.

By the time you finish, you should be able to install Capsule on a fresh laptop, route to the right environment and fleet, find an appropriate machine, run a benchmark, schedule a long job, debug a failure, and write up the result — all without supervision. That is the bar for being able to contribute meaningfully to reliability and model-eval work.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>Throughout the workbook you'll see callouts marked "Reliability lens." These are the failure modes most likely to show up in real incidents. Treat them as required reading.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

# Course Outline

| **Module** | **Title** | **Lab focus** |
|----|----|----|
| 1 | Capsule Foundations | Mental model |
| 2 | Installation & First Login | Get the CLI working |
| 3 | Environments & Customers | Routing to the right fleet |
| 4 | The Fleet: Listing & Filtering | Finding the right machine |
| 5 | Connecting to Machines | term / exec / code / cursor / claude |
| 6 | Files, Storage & OneDrive | Persistent data |
| 7 | Streaming & Containers | Desktop, app, docker |
| 8 | Benchmarking | InferenceMAX evaluation runs |
| 9 | Interactive Chat | Hands-on model probing |
| 10 | Scheduling & Reliability Toolkit | Long jobs and triage |

**MODULE 1**

**Capsule Foundations**

*Focus: Build the right mental model before you type a single command.*

## What Capsule is

Capsule is a remote development and application streaming platform. Your laptop is a thin client; the CPU, GPU, RAM, and disk live on remote machines. Capsule pipes shells, IDEs, full desktops, and individual applications back to you over the network.

## Two connection paths

| **Path** | **How it works** | **When to use it** |
|----|----|----|
| SshRTC (default) | SSH tunneled through a WebRTC peer connection. | Everyday work. NAT traversal handled for you. |
| Direct SSH (--direct) | Plain TCP SSH. | Port-forwarding, debugging WebRTC failures. |

## Two routing dimensions

Every Capsule session is parameterised by two things you should be able to recite in your sleep:

- Environment — backend deployment and B2C identity tenant. One of prod, public, dev, demo.

- Customer — which fleet inside an environment you index into. One of micc, modelhosting, oneplay, cree8.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>When a report comes in that 'Capsule isn't working,' the first four questions are: which environment, which customer, is the token expired, and is SshRTC failing? Most incidents resolve on the first three before you need to look at logs.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Self-check

1.  Explain SshRTC vs Direct SSH in your own words, with the trade-off.

2.  Capsule list looks wrong. Name the first two settings you check.

3.  A teammate gives you a unique ID. Which command confirms that ID exists in the fleet?

**\**

**MODULE 2**

**Installation & First Login**

*Focus: Get the CLI on your machine and authenticated.*

## Prerequisites

- GitHub Personal Access Token with scopes repo, read:org, workflow, user. Exported as GH_TOKEN.

- GitHub CLI (gh) on Windows/Linux.

- Homebrew on macOS.

- rclone (auto on macOS, manual elsewhere).

## macOS install

export HOMEBREW_GITHUB_API_TOKEN=\$GH_TOKEN\
brew tap mihira-ai/software-packages https://\$GH_TOKEN@github.com/mihira-ai/software-packages.git\
brew install capsule

## Windows install (Administrator PowerShell)

winget install --id GitHub.cli\
exit \# restart as Admin\
\$cliVersion=""\
\$capsulePath="C:\Program Files\Capsule-CLI"\
gh.exe release download \$cliVersion -R mihira-ai/ox.capsule \`\
-p "capsule-cli-\*-win-x64.tar.gz" --clobber -D "\$capsulePath\bin"\
winget install Rclone.Rclone

## Linux install

CAPSULE_PATH="\$HOME/.local/capsule-cli"\
mkdir -p "\$CAPSULE_PATH/bin"\
gh release download -R mihira-ai/ox.capsule \\\
-p "capsule-cli-\*-linux-x64.tar.gz" --clobber -D "\$CAPSULE_PATH/bin"\
tar -xzf "\$CAPSULE_PATH/bin/"\*linux-x64.tar.gz -C "\$CAPSULE_PATH"

## First login

capsule auth login \# browser flow; falls back to manual token\
capsule status \# confirm identity + expiry\
capsule auth storage \# one-time OneDrive consent

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>'Install is broken' almost always traces back to GH_TOKEN. Ask in order: is it set, do the scopes match, is HOMEBREW_GITHUB_API_TOKEN exported in the same shell (macOS), did the terminal get restarted after setting the system variable (Windows)?</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 3**

**Environments & Customers**

*Focus: Routing your CLI to the correct fleet.*

## The four environments

| **Environment** | **B2C tenant**           | **Typical use**       |
|-----------------|--------------------------|-----------------------|
| prod            | mihirainfra.b2clogin.com | Internal production   |
| public          | oxcapsule.b2clogin.com   | External / partner    |
| dev             | mihirainfra.b2clogin.com | Development / testing |
| demo            | mihirainfra.b2clogin.com | Demonstrations        |

public uses a different B2C tenant than the others — separate user registry, separate token. Switching environments requires a fresh capsule auth login.

## Switching

capsule env show\
capsule env set public\
capsule auth login \# always re-authenticate after env switch\
capsule config customer show\
capsule config customer set modelhosting\
capsule config customer unset

## Lab exercises

4.  Switch from your default env to public, re-auth, list machines.

5.  Switch back. Verify with capsule status.

6.  Override the customer to modelhosting; list; unset; re-list. Note what changed.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>If 'machine X disappeared,' check the customer override before everything else. It persists across sessions and gets set by setup scripts more often than people remember.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 4**

**The Fleet: Listing & Filtering**

*Focus: Find the right machine in seconds.*

## Config tag vs unique ID

- Config tag — a pool/class name. Scheduler hands you any available member.

- Unique ID — a specific physical machine. Always paired with -u / --unique.

## Listing

capsule list \# by config tag\
capsule list --all \# individual unique IDs\
capsule list --users \# who's logged in\
capsule list --json \# machine-readable

## Filtering — key=value grammar

capsule list --filter "vendor=nvidia"\
capsule list --filter "gpu=rtx"\
capsule list --filter "os=linux"\
capsule list --filter "vram\>=24"\
capsule list --filter "ci=true"\
capsule list --filter "vendor=nvidia,vram\>=24,memory\>=100"

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>PowerShell quirk</strong></p>
<p>The cap shortener interacts badly with &gt; in PowerShell (treated as redirection). Use capsule (full name) and quote the filter argument.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

## Lab exercises

7.  List every NVIDIA machine with at least 24 GB VRAM.

8.  List every Tenstorrent machine. Identify CI-flagged ones.

9.  Pipe --json into jq and count machines by vendor.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>capsule list --users is your sniff test before scheduling expensive work — never blow away someone else's session.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 5**

**Connecting to Machines**

*Focus: Five commands, one routing language.*

## The five session commands

| **Command**    | **Opens**                          |
|----------------|------------------------------------|
| capsule term   | Remote shell over SshRTC (default) |
| capsule exec   | Single command, then exit          |
| capsule code   | VS Code with Remote-SSH attached   |
| capsule cursor | Cursor with Remote-SSH attached    |
| capsule claude | Claude Code Desktop on the remote  |

All five accept the same routing flags: positional \<config-tag\>, -u \<unique-id\>, --direct, --idle-timeout, --max-session-length, --turn. code and cursor additionally accept --repo. claude does not.

## Examples

capsule term \<tag\>\
capsule term -u \<unique-id\> --idle-timeout 2h --max-session-length 8h\
capsule term \<tag\> -e "nvidia-smi"\
capsule term \<tag\> --direct --options "-L 3000:localhost:3000"\
capsule code \<tag\> --repo mihira-ai/your-experiment\
capsule claude \<tag\>

## Lab exercises

10. term into an NVIDIA box; run nvidia-smi and whoami.

11. Run nvidia-smi non-interactively via capsule exec.

12. Open the same machine in VS Code; verify the integrated terminal is remote.

13. Re-open with --direct; compare informally.

14. Open a session with --idle-timeout 30m --max-session-length 1h; note the message.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>Three habits to build: (1) cleanup + retry before --direct fallback; (2) always set timeouts for batch-like work; (3) don't leave stale capsule-&lt;id&gt; blocks in ~/.ssh/config — they break Remote-SSH cryptically.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 6**

**Files, Storage & OneDrive**

*Focus: Three ways to move bytes.*

## Three transfer mechanisms

| **Mechanism** | **When to use it** |
|----|----|
| OneDrive auto-mount | Files you want available on every machine you connect to. |
| capsule scp | One-off transfers, especially large blobs. |
| File passthrough | Small dotfiles copied at session start (.vimrc, .gitconfig). |

## OneDrive setup (once)

capsule auth storage \# browser OAuth, stores credentials locally\
\# every subsequent session auto-mounts ~/OneDrive\
ls ~/OneDrive \# OxCapsule contents\
cp model.safetensors ~/OneDrive/

## SCP

capsule scp upload \<tag\> ./model.onnx /workspace/models/\
capsule scp upload \<tag\> ./dataset/ /data/training/\
capsule scp download \<tag\> /workspace/output/results.csv ./\
capsule scp upload -u \<unique-id\> ./script.py /home/user/\
capsule scp upload \<tag\> ./large.tar.gz /data/ --options "-l 50000"

## File passthrough

capsule config files add .gitconfig ~/.gitconfig\
capsule config files list\
capsule config files remove .vimrc\
capsule config files clear

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>If ~/OneDrive is empty on the remote, the daemon couldn't mount it. Common causes: rclone missing locally, expired OneDrive OAuth, VFS cache from a prior session. Re-auth storage, reconnect.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 7**

**Streaming & Containers**

*Focus: Bring up GUIs and isolated environments.*

## Desktop & app streaming

capsule stream \<tag\>\
capsule stream -u \<unique-id\>\
capsule stream \<tag\> --app "blender"

- Hardware-encoded H.264/H.265/AV1 (NVENC / VAAPI / VideoToolbox).

- Audio forwarded, clipboard sync, adaptive bitrate.

- Keyboard, mouse, gamepad input.

## Docker

capsule docker \<tag\> \# ubuntu:latest, bash\
capsule docker \<tag\> --image pytorch/pytorch:latest --memory 16\
capsule docker \<tag\> --image nvidia/cuda:12.0-devel \\\
--command "python train.py" \\\
--volume "/data:/data:ro;/workspace:/workspace"\
capsule docker \<tag\> -- --gpus all

## Lab exercises

15. Stream a remote desktop. Test clipboard both ways.

16. Stream a single app (--app firefox or similar).

17. Launch ubuntu:latest; confirm nvidia-smi fails.

18. Re-launch with -- --gpus all; confirm nvidia-smi sees the GPU.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>WebRTC is bandwidth-sensitive. Video drops first, then audio, then input lag. Before blaming the encoder, confirm the user's downlink with a separate speed test.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 8**

**Benchmarking — the InferenceMAX path**

*Focus: Most important module for the reliability & eval track.*

## Backends

| **Backend** | **When to use it**                                 |
|-------------|----------------------------------------------------|
| vllm        | Default. NVIDIA, batched serving, paged attention. |
| llamacpp    | CPU-friendly, GGUF quantizations (Q4_K_M, Q5_K_M). |
| mlx         | Apple Silicon.                                     |
| oxpython    | OXMIQ Python runtime for in-house eval paths.      |

## Key knobs

| **Flag** | **Meaning** | **Default** |
|----|----|----|
| --concurrency / -c | max-num-seqs (batch size) | 4 |
| --input-length / --isl | Tokens per prompt | 128 |
| --output-length / --osl | Tokens generated per response | 128 |
| --num-prompts / -n | Total requests sent | concurrency × 10 |
| --tensor-parallelism / --tp | Split model across N GPUs | 1 |
| --quant / -q | Quantization (awq, gptq, fp8, int8, Q4_K_M, Q5_K_M) | — |
| --api-base / --api-key | Benchmark an existing endpoint without provisioning | — |

## Examples

capsule benchmark \<tag\> meta-llama/Llama-3.1-8B-Instruct\
capsule benchmark \<tag\> meta-llama/Llama-3.1-8B-Instruct \\\
--concurrency 8 --input-length 256 --output-length 256 --num-prompts 40\
capsule benchmark \<tag\> Qwen/Qwen2.5-7B-Instruct-GGUF \\\
--backend llamacpp --quant Q4_K_M\
capsule benchmark \<tag\> meta-llama/Llama-3.1-70B-Instruct --tp 4\
capsule benchmark --api-base http://localhost:8000 --api-key test \<model\>

Results dashboard:

[<u>https://oxcapsulebenchmark.z22.web.core.windows.net</u>](https://oxcapsulebenchmark.z22.web.core.windows.net)

## Lab exercises

19. Default benchmark on an 8B model on NVIDIA. Note throughput.

20. Re-run with concurrency 16 and num-prompts 160. Compare.

21. Run with --quant awq. Note quality eyeball + throughput.

22. Run with --tp 2 on a multi-GPU machine. Verify GPU usage with nvidia-smi.

23. Find both runs on the dashboard.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>Benchmarks are silent on the SSH channel — exactly the workload aggressive idle timeouts kill. Always pass --idle-timeout and --max-session-length longer than your expected run. For anything over an hour, prefer capsule schedule (Module 10).</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**MODULE 9**

**Interactive Chat**

*Focus: Hands-on model probing.*

## Basic chat

capsule chat \<tag\> meta-llama/Llama-3.1-8B-Instruct\
capsule chat \<tag\> \<model\> --temperature 0.3 --max-tokens 2048 \\\
--system-prompt "You are a helpful coding assistant."\
capsule chat \<tag\> Qwen/Qwen2.5-7B-Instruct-GGUF --backend llamacpp --quant Q4_K_M\
capsule chat \<tag\> \<model\> --agent oxsol \# tool calling\
capsule chat \<tag\> \<model\> --hf-token \$HF_TOKEN --tp 4 --rm

## Key flags

| **Flag**                     | **Purpose**                               |
|------------------------------|-------------------------------------------|
| --backend                    | Override auto-detected backend            |
| --temperature / --max-tokens | Sampling controls                         |
| --system-prompt              | Prepended to every turn                   |
| --agent                      | Enable aichat agent with MCP tool calling |
| --api-base / --api-key       | Skip deploy; talk to an existing endpoint |
| --hf-token                   | For gated models                          |
| --rm                         | Auto-cleanup container on exit            |
| --no-stream                  | Disable streaming                         |

## Lab exercises

24. Chat with a model; test prompt categories: factual, math, code, refusal probe, long-context.

25. Re-run with --temperature 0.1; compare consistency.

26. Spin up with --quant awq; rerun the prompts; note regressions.

27. Add --agent oxsol; try a multi-step task with tool calls.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Reliability lens</strong></p>
<p>When a customer says 'the model is broken,' reproduce on the same machine with capsule chat -u &lt;unique-id&gt; using their sampling settings. If it works for you, the issue is in their client, not the inference path.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**MODULE 10**

**Scheduling & Reliability Toolkit**

*Focus: Long jobs and triage.*

## Scheduled jobs

capsule schedule start \<tag\> --script ./train.sh --name "training-v2" --timeout 8h\
capsule schedule start \<tag\> --script ./train.sh --retry 3 --env "EPOCHS=100"\
capsule schedule start --machine-name NV-4090-01 --script ./benchmark.sh\
capsule schedule start \<tag\> --script ./run.sh --with-file ./model.py\
capsule schedule status \<tag\>\
capsule schedule status \<tag\> --me --state running --show-start\
capsule schedule cancel \<job-id\>\
capsule schedule cancel --all\
capsule schedule logs \<job-id\> --tail 100

## Agents & MCP

capsule mcp \# install Capsule MCP into Claude\
capsule mcp --uninstall\
capsule mcp --output ./mcp.json \# inspect without installing\
export CAPSULE_AGENT_ENABLED=1\
export OXMIQ_AGENT_API_BASE=http://127.0.0.1:8080/v1\
export OXMIQ_AGENT_API_KEY=your-key\
export OXMIQ_AGENT_MODEL=openai/capsule\
capsule agent -p "list nvidia machines with 16GB+ VRAM"\
capsule agent -c "show me free GPUs"

## Reliability toolkit

capsule status \# auth, identity, expiry\
capsule env show \# current environment\
capsule config customer show \# current fleet\
capsule cleanup \# tear down stale WebRTC + SSH state\
capsule --version \# CLI build (for bug reports)\
capsule --no-banner list \# clean output

## Known-quirks table — memorise this

<table>
<colgroup>
<col style="width: 42%" />
<col style="width: 57%" />
</colgroup>
<thead>
<tr>
<th><strong>Symptom</strong></th>
<th><strong>Fix</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Auth fails in browser flow</td>
<td>Manual token at https://oxmiq.ai/oxcapsule/auth</td>
</tr>
<tr>
<td>capsule list shows wrong machines</td>
<td>Check env show and config customer show</td>
</tr>
<tr>
<td>SshRTC won't connect</td>
<td>cleanup, retry, then --direct as fallback</td>
</tr>
<tr>
<td>VS Code Remote-SSH fails after a session</td>
<td>Remove capsule-&lt;id&gt; blocks from ~/.ssh/config</td>
</tr>
<tr>
<td>macOS Keychain prompts constantly</td>
<td>Click 'Always Allow' once</td>
</tr>
<tr>
<td>PowerShell filter with &gt; fails</td>
<td>Use capsule (not cap) and quote the argument</td>
</tr>
<tr>
<td>capsule update fails</td>
<td>Token valid; close all SshRTC sessions first</td>
</tr>
<tr>
<td>gh release download 401/403</td>
<td>Re-check GH_TOKEN scopes</td>
</tr>
<tr>
<td colspan="2"><p><strong>Reliability lens</strong></p>
<p>Triage shape: (1) reproduce yourself — no repro = incident not bug; (2) capture version, env, customer, command, timestamp, unique ID; (3) try cleanup + --direct before escalating; (4) default long work to capsule schedule.</p></td>
</tr>
</tbody>
</table>

**\**

**Capstone Lab — Bench-to-Dashboard Round Trip**

*Focus: End-to-end, without notes. Time yourself.*

28. From a fresh shell, confirm env is prod and customer is micc.

29. Find an NVIDIA machine with ≥24 GB VRAM that has no active users.

30. Open VS Code via SshRTC; confirm nvidia-smi from the integrated terminal.

31. From your laptop, upload prompts.txt to /workspace/ via SCP.

32. Run a benchmark on Llama-3.1-8B-Instruct with concurrency 8, ISL 256, OSL 256.

33. Re-run with --quant awq. Note the new throughput.

34. Find both runs on the dashboard.

35. Schedule the same benchmark as a background job, 1-hour timeout.

36. While it runs, open capsule chat against the same model and verify a few prompts.

37. Run capsule cleanup. Confirm via capsule list --users that you no longer hold the machine.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><p><strong>Target time</strong></p>
<p>Under 30 minutes once you've done it. Reliability work is mostly muscle memory.</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**\**

**Glossary**

*Focus: Speak the language.*

| **Term** | **Definition** |
|----|----|
| Config tag | Machine pool/class name. Scheduler hands you any available member. |
| Unique ID | Specific physical machine. Always paired with -u / --unique. |
| SshRTC | Capsule's WebRTC-based SSH data channel. Default connection method. |
| Direct SSH | Plain TCP SSH (--direct). Fallback and clean port-forwarding. |
| Environment | Backend deployment (prod, public, dev, demo). Determines B2C tenant. |
| Customer | Fleet selector inside an environment (micc, modelhosting, oneplay, cree8). |
| InferenceMAX | The benchmark suite invoked by capsule benchmark. |
| TURN | WebRTC relay used when peer-to-peer NAT traversal fails. |
| MCP | Model Context Protocol; how Claude Desktop/Code talks to Capsule as a tool. |

**\**

**Self-Assessment**

*Focus: Are you a power user yet?*

By the end of the course, all of the following should be true:

- Install, authenticate, and produce a benchmark run on a fresh laptop in under 15 minutes.

- Debug a 'Capsule isn't working' report by walking env → customer → auth → connection method aloud.

- Write a capsule schedule job that wraps a non-trivial eval and recover its logs after the fact.

- Explain in two minutes to a new intern: config tag vs unique ID, SshRTC vs Direct SSH.

If any of these still take you more than a minute of hesitation, revisit the relevant module.

---

# Appendix A — Per-Module Reliability Deep-Dives

The body of this workbook teaches you *how* to use Capsule. This appendix teaches you *what tends to break*, with the numbers you'll need to triage it. Each module gets a five-part block matching the structure used in the Inference Engineering and AI Agents tracks:

1. **Why this matters in reliability work** — the on-call moment this module unlocks.
2. **Worked numerical example(s)** — real fleet/network/time math.
3. **Common confusions / what it is NOT** — misconceptions seen in intern PRs and on-call handoffs.
4. **How this connects** — links to other modules and to the broader OXMIQ stack.
5. **Concept-graph anchors** — IDs from `docs/kb/concepts.json` to study alongside.

## A.1 — Capsule Foundations

**Why this matters.** Most 'Capsule is broken' tickets are routing or transport confusion, not actual breakage. If you carry the two-dimensional model (env × customer) and the two transport paths (SshRTC vs Direct SSH) in your head, you triage in 30 seconds instead of 30 minutes.

**Worked example.** A user reports `capsule list` returning an empty fleet. Walk the matrix: env (prod/public/dev/demo) × customer (micc/modelhosting/oneplay/cree8) = **16 cells**. They are almost certainly in the wrong cell. Ask them to print their current env+customer; in 9 of 10 cases the answer is `prod / modelhosting` when they meant `prod / micc` (or vice versa). Resolution time: **<2 minutes**.

**Common confusions.** It is NOT: a single fleet (it's 16+); a VPN (it's WebRTC over arbitrary networks); a cloud (the boxes are real hardware on the lab floor); a replacement for SSH (it *uses* SSH, then adds routing, identity, and a peer fabric).

**How this connects.** Module 3 (env/customer routing), Module 5 (transport), Module 10 (triage scripts). Connects upward to the broader OXMIQ stack: oxgate (identity), oxfactory (control plane), model-hosting (a customer fleet).

**Concept-graph anchors.** `capsule-fleet`, `capsule-routing`, `sshrtc-transport`.

## A.2 — Installation & First Login

**Why this matters.** The intern who can't install Capsule can't do reliability work. The intern who *can* install it on a stranger's laptop in 15 minutes is the one we trust on-call.

**Worked example.** Fresh MacBook (M-series), no Homebrew. Steps and target times: brew install (2 min) → `brew tap oxmiq/software-packages` (30 sec) → `brew install capsule` (90 sec) → `capsule login` opens browser, B2C device-code auth (60 sec) → `capsule list` returns first fleet (5 sec). **Total: ~5 min** clean path; **15 min** budget allows one retry on auth.

**Common confusions.** It is NOT: a `pip install` (it's a brew bottle / msi / deb). It does NOT cache credentials forever — tokens refresh every ~60 minutes; expired tokens manifest as `403` on `capsule list`, which interns mistake for fleet outages.

**How this connects.** Module 3 (after install, the next thing is env selection). Connects to the `software-packages` repo (bottle authoring) and `oxgate` (auth issuance).

**Concept-graph anchors.** `capsule-install`, `oxgate-auth`, `b2c-tenant`.

## A.3 — Environments & Customers

**Why this matters.** Most cross-team handoff bugs are an environment mismatch. A reliability engineer who can read a CLI command and tell you which env+customer it ran against is one who can reproduce any reported issue.

**Worked example.** 4 envs × 4 customers = **16 possible routing cells**. A bug report says "the model deployment failed." Without env+customer, you can't reproduce; with both, you can `capsule env prod && capsule customer modelhosting && capsule list` and have the fleet under your fingers in 10 seconds. Time saved on average ticket: **~20 minutes**.

**Common confusions.** Environments are NOT branches (they're parallel deployments). Customers are NOT tenants (they're fleet selectors within a single backend). `prod` is NOT the only production environment — `public` is also production, but for external customers.

**How this connects.** Module 4 (env+customer determines what `list` returns). Module 10 (env mismatch is the #1 triage misdirection).

**Concept-graph anchors.** `capsule-env`, `capsule-customer`, `b2c-tenant`.

## A.4 — The Fleet: Listing & Filtering

**Why this matters.** A reliability engineer who can't quickly filter the fleet wastes minutes per incident. With 200+ machines across env+customer combinations, raw `capsule list` is unusable without filters.

**Worked example.** OXMIQ's combined fleet in mid-2026 is roughly **200 machines**: ~120 NVIDIA (mix of 3060/4090/5090/L40S/H100), ~40 Tenstorrent (Wormhole n150 + Blackhole p150), ~20 AMD MI300, ~20 Apple Silicon (M2/M3 Ultra). A query like `capsule list --config nv-h100` should return **8–12 hits**; if it returns 0, you've drifted env or customer.

**Common confusions.** Config tag is NOT a hostname — it's a *pool*. Unique ID is NOT a config tag — it's a *box*. Asking the scheduler for a config tag = "any available H100"; asking for a unique ID = "*this* H100, even if it's offline."

**How this connects.** Module 5 (you connect to either a config tag or a unique ID). Module 8 (benchmarks target config tags to get fair pool-average numbers).

**Concept-graph anchors.** `capsule-fleet`, `config-tag`, `unique-id`.

## A.5 — Connecting to Machines

**Why this matters.** Five connection verbs (`term`, `exec`, `code`, `cursor`, `claude`) each have a use case. Picking the wrong one wastes 5 minutes per incident and confuses the model context for AI-assisted debugging.

**Worked example.** Triage a hung benchmark on `nv-h100-03-2`:
- `capsule term -u nv-h100-03-2` (~1 sec to attach) → `nvidia-smi` → see GPU at 0% utilization → likely user-side hang.
- `capsule exec -u nv-h100-03-2 -- nvidia-smi` (~0.5 sec) → same info, scriptable.
- `capsule code -u nv-h100-03-2` (~3 sec) → opens VS Code Remote, full IDE for editing the eval script.
- `capsule claude -u nv-h100-03-2` (~2 sec) → MCP-enabled Claude Code session for AI-assisted log analysis.

**Common confusions.** `term` is NOT the same as `ssh` — it goes over SshRTC by default. `--direct` is NOT a fallback for slow networks — it's a fallback for *broken WebRTC peer setup*. Latency target: SshRTC keystroke echo **<80ms p50** on a healthy network; Direct SSH **<40ms p50**.

**How this connects.** Module 6 (files), Module 7 (streaming), Module 9 (chat). The connection verb you pick determines what context the downstream AI tool sees.

**Concept-graph anchors.** `capsule-connect`, `sshrtc-transport`, `mcp-server`.

## A.6 — Files, Storage & OneDrive

**Why this matters.** Reliability incidents that involve "where did my data go?" are almost always a storage scope confusion. There are 3 scopes (ephemeral pod, persistent volume, OneDrive mount) and each has different durability.

**Worked example.** A user reports their eval results "disappeared." The triage tree: (a) `/tmp` → ephemeral, gone on container restart; (b) `/home/$USER` → persistent volume, durable across restarts but tied to *this machine*; (c) `~/OneDrive` → durable AND portable across machines, but writes are slower (target: **<5MB/s sustained** vs. local NVMe **>1GB/s**). Asking *which scope* before triaging saves ~20 minutes.

**Common confusions.** OneDrive is NOT a backup — it's a sync. Deletions propagate. The persistent volume is NOT shared across machines — same path, different data on different boxes.

**How this connects.** Module 8 (benchmark outputs default to persistent volume; you must opt in to OneDrive for cross-machine analysis). Module 10 (storage scope is a frequent triage step).

**Concept-graph anchors.** `capsule-storage`, `onedrive-mount`, `persistent-volume`.

## A.7 — Streaming & Containers

**Why this matters.** Desktop streaming, app streaming, and Docker each have a different latency/cost profile. Picking wrong burns either GPU time or network bandwidth.

**Worked example.** Desktop streaming runs a full Linux/Windows desktop at ~30 FPS, ~5-15 Mbps depending on content. App streaming runs a single application window at ~60 FPS, ~3-8 Mbps. Container shells use ~0 Mbps for the video path (text only). For an intern who just needs to run `pytest`, desktop streaming wastes **~10 Mbps × session-duration** of bandwidth and ~1 GPU encoder slot.

**Common confusions.** App streaming is NOT a remote desktop with one window — it has its own compositor. Docker on Capsule is NOT a sandbox in the security sense — it's a *packaging* mechanism; the host has full visibility.

**How this connects.** Module 5 (you can mix-and-match: stream a desktop AND open a `term` simultaneously). Connects to capsule-streamer (the underlying WebRTC streaming stack).

**Concept-graph anchors.** `capsule-streaming`, `webrtc-encoder`, `docker-runtime`.

## A.8 — Benchmarking

**Why this matters.** Benchmark numbers drive procurement decisions worth millions. A reliability engineer who can't read an InferenceMAX run sheet is a liability.

**Worked example.** `capsule benchmark --model llama3.1-8b --config nv-h100` on a healthy H100 should yield: **~1500-2500 tokens/sec** decode (single stream), **~10K-30K tokens/sec** batched, **<50ms TTFT** at 256-token prompt. If you see <800 tokens/sec decode, suspect: (a) thermal throttling, (b) wrong driver version, (c) PCIe link degradation. The cost-per-million-tokens math at $2/H100-hour: 2000 tok/sec × 3600 = 7.2M tok/hr → **$0.28 per M-tokens** at single-stream; batched: **$0.05 per M-tokens**.

**Common confusions.** A single benchmark run is NOT a measurement — it's a sample. Always run **≥3** for variance; report median and p95. The "throughput" number on the dashboard is NOT comparable across config tags — it's only comparable within a tag.

**How this connects.** Module 4 (you pick a config tag, not a unique ID, for fair pool-average numbers). Module 10 (anomalous benchmarks are a primary triage signal).

**Concept-graph anchors.** `inferencemax`, `benchmark-variance`, `gpu-throttling`.

## A.9 — Interactive Chat

**Why this matters.** Hands-on probing of a deployed model surfaces failure modes (refusals, format breaks, language drift) that batch evals miss.

**Worked example.** A model behaves well on a benchmark but a user reports "weird Korean text appearing." Reproduce via `capsule chat --model X` with the user's prompt: if you see the drift in 3 of 10 attempts (**30% reproduction rate**), it's a real bug, not a one-off. Time to first signal: **~2 min**, vs. **~2 hours** to construct a batch eval for the same insight.

**Common confusions.** Chat is NOT a benchmark — single-turn quality varies wildly. Chat is NOT logged automatically — copy interesting transcripts to your incident notes immediately.

**How this connects.** Module 8 (chat surfaces bugs; benchmarks quantify them). Connects to model-hosting (the deployment under test).

**Concept-graph anchors.** `interactive-eval`, `model-deployment`, `prompt-probing`.

## A.10 — Scheduling & Reliability Toolkit

**Why this matters.** Multi-hour evals can't be babysat. Knowing how to schedule, monitor, and post-mortem a scheduled run is the *defining* skill of the reliability-track intern.

**Worked example.** A 6-hour InferenceMAX sweep across 8 models. Per-model wall-clock: ~45 min. Serial: **6 hours**. Parallel across 4 GPUs: **~90 min** (8 models × 45 min ÷ 4 GPUs). Schedule submission: `capsule schedule submit --config nv-h100 --parallel 4 sweep.sh`. Cost: 4 GPUs × 1.5 hours × $2/hr = **$12 per sweep**. Lost wall-clock recovery if you forget `--parallel`: **4.5 hours**.

**Common confusions.** A scheduled job is NOT a service — it has a finite lifetime. Logs are NOT retained forever — pull them within **7 days** or they age out of the default retention.

**How this connects.** Every prior module. Scheduling is where Capsule shifts from interactive tool to production system.

**Concept-graph anchors.** `capsule-scheduler`, `parallel-execution`, `log-retention`.

---

# Appendix B — Numerical Anchors Cheat-Card

Memorize these. They are the numbers you'll be asked in week-1 stand-ups.

| Quantity | Value |
|---|---|
| Fleet size (mid-2026) | ~200 machines |
| Routing matrix | 4 envs × 4 customers = 16 cells |
| SshRTC keystroke echo (p50, healthy) | <80 ms |
| Direct SSH keystroke echo (p50) | <40 ms |
| H100 decode throughput (single stream, Llama-3.1-8B) | 1500-2500 tok/sec |
| H100 batched throughput (Llama-3.1-8B) | 10K-30K tok/sec |
| Per-M-token cost on H100 (batched) | ~$0.05 |
| OneDrive sustained write | <5 MB/s |
| Persistent volume (local NVMe) | >1 GB/s |
| Auth token TTL | ~60 min |
| Log retention default | 7 days |
| Minimum runs for variance reporting | ≥3 (median + p95) |

---

# Appendix C — Triage Decision Tree

Use this as your on-call cheat-sheet. Print and keep on your desk.

```
User reports: "Capsule isn't working"
│
├── Can they `capsule list`?
│   ├── No → Auth issue
│   │   ├── 401/403 → token expired → `capsule login` (TTL ~60 min)
│   │   ├── connection refused → check oxgate health
│   │   └── timeout → check user's network egress to *.capsule.oxmiq.io
│   │
│   └── Yes, but empty → Routing issue
│       ├── Wrong env → `capsule env <prod|public|dev|demo>`
│       └── Wrong customer → `capsule customer <micc|modelhosting|oneplay|cree8>`
│
├── Can they connect to a specific box?
│   ├── No, SshRTC hangs → try `--direct`; if that works → WebRTC peer fail
│   ├── No, both fail → box is offline → check fleet dashboard
│   └── Yes, but slow → check transport latency target (<80ms / <40ms)
│
└── Connected, but workload fails
    ├── GPU at 0% → app didn't see CUDA → driver/runtime mismatch
    ├── GPU throttling → thermal → check `nvidia-smi -q -d TEMPERATURE`
    ├── OOM → check VRAM headroom vs. model size
    └── "Disappeared" data → ask which storage scope (Module 6 tree)
```

---

# Appendix D — Concept-Graph Cross-Reference

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

These IDs are stable; consult `docs/kb/concepts.json` for prerequisite edges and longer definitions.
