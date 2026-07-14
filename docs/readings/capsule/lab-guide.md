---
title: Capsule Power-User - Lab Guide
---

# Capsule Power-User Lab Guide

**Course:** Becoming a Capsule Power User
**Audience:** OXMIQ Student Interns (Reliability & Model Evaluation track)
**Duration:** 2 days (10 modules × ~45 min lecture + ~45 min lab)
**Prereqs:** Comfortable with a Unix shell, SSH, basic Python, and Git. No prior Capsule experience required.

---

## How to use this guide

Every module has the same shape:

1. **Concept**: what the feature is and why it exists.
2. **Demo**: commands the instructor will run live.
3. **Lab**: exercises you run yourself, with checkpoints.
4. **Stretch**: optional deeper exploration. Do these if you finish early or after class.
5. **Reliability lens**: what failure modes to watch for. This is the part that matters most for your internship.

Throughout, `<config-tag>` is a machine pool name (e.g. `gpu-workstation-01`) and `<unique-id>` is a specific machine (e.g. `boostergold461`). Run `capsule list` to see the pools you have access to; run `capsule list --all` to see unique IDs.

---

## Module 1 - Capsule Foundations

### Concept

Capsule is a remote development and application streaming platform. You stay on your laptop; the CPU, GPU, RAM, and disk live somewhere else. Everything you type, terminals, VS Code, Cursor, Claude Code, full desktops, ComfyUI, runs on remote hardware and is piped back to you over the network.

There are two connection paths underneath every command:

- **SshRTC data channel** (default). A WebRTC peer connection carries SSH traffic. The remote machine never needs a publicly reachable port. NAT traversal "just works" most of the time.
- **Direct SSH** (`--direct` flag). Normal TCP SSH. The remote must have a reachable SSH port. Faster and easier to debug; needed when WebRTC fails or when you want to use SSH features like port-forwarding cleanly.

Capsule is deployed across four **environments** and several **customer fleets**:

| Environment | B2C tenant                  | Typical use                  |
|-------------|-----------------------------|------------------------------|
| `prod`      | `mihirainfra.b2clogin.com`  | Internal production fleet    |
| `public`    | `oxcapsule.b2clogin.com`    | External / partner access    |
| `dev`       | `mihirainfra.b2clogin.com`  | Development / testing        |
| `demo`      | `mihirainfra.b2clogin.com`  | Demos                        |

Customer fleets inside an environment: `micc` (default), `modelhosting`, `oneplay`, `cree8`.

Two facts worth memorising right now, because every confused support ticket eventually traces back to one of them:

1. **`public` and the others use different B2C tenants.** Your account in `prod` is not your account in `public`. Switching environments is followed by re-authenticating.
2. **Customer changes the fleet you see.** If `capsule list` looks empty or wrong, the first thing to check is `capsule config customer show`.

### Demo (instructor)

```bash
capsule --version
capsule env show
capsule config customer show
capsule list | head
```

### Lab

No tools to install yet. On paper or in your notes:

1. Explain SshRTC vs Direct SSH to your bench partner in your own words. What's the trade-off?
2. You see machines in `capsule list` that don't look like the production fleet. Name the two settings you'd inspect first.
3. A teammate emails you a unique ID `boostergold461`. What command lists machines so you can confirm that ID exists?

**Checkpoint:** You can explain to a non-Capsule engineer what the platform does in two sentences, and you know the names of the two routing dimensions (environment, customer).

### Reliability lens

Most "Capsule is broken" reports are really one of: (a) wrong environment, (b) wrong customer, (c) expired token, (d) SshRTC negotiating against a hostile network. Internalising those four candidates is half the job.

---

## Module 2 - Installation & First Login

### Concept

Install methods are OS-specific but the moving parts are the same: a CLI binary on your PATH, a GitHub PAT to fetch releases, `rclone` for cloud storage, and a one-time browser login that mints a Capsule auth token.

The PAT (`GH_TOKEN`) needs scopes `repo`, `read:org`, `workflow`, `user`. The token is used during installation and updates only: not at runtime.

### Demo

```bash
# macOS
export HOMEBREW_GITHUB_API_TOKEN=$GH_TOKEN
brew tap mihira-ai/software-packages https://$GH_TOKEN@github.com/mihira-ai/software-packages.git
brew install capsule

# Verify
capsule --version
capsule auth login
capsule status
```

### Lab

1. Install Capsule on your laptop using the instructions for your OS.
   - macOS: Homebrew tap + `brew install capsule`.
   - Windows: PowerShell as Administrator, `winget install --id GitHub.cli`, then download via `gh release download`. Don't forget `winget install Rclone.Rclone`.
   - Linux: install `gh`, then `gh release download -R mihira-ai/ox.capsule`.
2. Run `capsule --version`. Note the version on a sticky note; you'll need it when filing bugs.
3. Run `capsule auth login`. Complete the browser flow.
4. Run `capsule status`. Confirm your user name, display name, and token expiry.
5. Run `capsule auth storage` and complete the OneDrive consent flow.

**Checkpoint:** `capsule status` shows your identity and a non-empty expiry. You can list at least one machine: `capsule list | head`.

### Stretch

- Set `CAPSULE_AUTH_TOKEN` from a fresh login and run a command in a shell that has no browser session. This is how headless CI uses Capsule.
- Read the install scripts in this guide and identify, line by line, where rclone gets installed and why.

### Reliability lens

When a colleague says "install is broken", ask in this order: (1) Is `GH_TOKEN` set? (2) Do the token scopes match? (3) For macOS, is `HOMEBREW_GITHUB_API_TOKEN` exported in the *same* shell that's running `brew`? (4) For Windows, was the PowerShell restarted after the system env var was set?

---

## Module 3 - Environments, Customers, and Why Your Fleet Looks Wrong

### Concept

`capsule env set <name>` switches the backend endpoint and B2C tenant. `capsule config customer set <name>` switches which customer's fleet you're indexing into. Both persist across sessions. The auth token is **scoped to an environment**, so switching env requires a fresh `capsule auth login`.

### Demo

```bash
capsule env show
capsule env set public
capsule auth login              # required after env switch
capsule list
capsule config customer set modelhosting
capsule list
capsule config customer unset   # back to env default
capsule env set prod
capsule auth login
```

### Lab

1. Switch from your default environment to `public`, re-authenticate, and run `capsule list`. Note how the fleet changed.
2. Switch back to `prod` (or whichever is your primary). Re-auth. Verify with `capsule status`.
3. Set the customer to `modelhosting` and `capsule list` again. Observe which machines appear or disappear. Then `capsule config customer unset`.

**Checkpoint:** You can move between two environments and two customer overrides without help, and you can predict which fleet you'll see before running `capsule list`.

### Reliability lens

A common silent failure: a user reports "machine X disappeared". Nine times out of ten they accidentally switched customers (or someone wrote a setup script that did). `capsule config customer show` is always the first command in that conversation.

---

## Module 4 - The Fleet: Listing & Filtering Machines

### Concept

`capsule list` groups available machines by **config tag** (machine pool / class). When you ask for a config tag, the scheduler hands you any available machine from that pool. When you need a specific physical box, use `--all` to see **unique IDs** and target with `-u`/`--unique`.

Filters use a `key=value` (or `key>=value`) comma-separated grammar with AND semantics.

### Demo

```bash
capsule list
capsule list --all
capsule list --users
capsule list --json | jq '.[0]'

capsule list --filter "vendor=nvidia"
capsule list --filter "gpu=rtx"
capsule list --filter "os=linux"
capsule list --filter "vram>=24"
capsule list --filter "ci=true"
capsule list --filter "vendor=nvidia,vram>=24,memory>=100"
```

### Lab

1. List every NVIDIA machine with at least 24 GB of VRAM.
2. List every Tenstorrent machine. Note any that are CI-flagged.
3. Pipe `--json` into `jq` and count machines by vendor.
4. On Windows only: try the same filter using `cap` and notice when `>` fails in PowerShell. Switch to `capsule` and quote the argument.

**Checkpoint:** You can construct any filter expression on the fly and explain why `cap` shorthand breaks in PowerShell with `>` (PowerShell interprets it as redirection).

### Stretch

Write a small script (Python, Bash, your call) that consumes `capsule list --json` and prints a leaderboard of the top 5 machines by free VRAM. This kind of tooling is exactly what reliability work looks like.

### Reliability lens

`capsule list --users` is your fastest sniff test before scheduling expensive work; never blow away someone else's session by claiming a machine that already has an active user.

---

## Module 5 - Connecting to Machines

### Concept

There are five commands that all open some form of session on a remote machine:

| Command          | What it opens                       |
|------------------|-------------------------------------|
| `capsule term`   | A shell (SSH over WebRTC by default)|
| `capsule exec`   | One-off remote command, then exit   |
| `capsule code`   | VS Code with Remote-SSH attached    |
| `capsule cursor` | Cursor with Remote-SSH attached     |
| `capsule claude` | Claude Code Desktop on the remote   |

All five accept the same routing flags:
- positional `<config-tag>` for any-from-pool, or `-u <unique-id>` for a specific box;
- `--direct` to bypass WebRTC and go straight to TCP SSH;
- `--idle-timeout` and `--max-session-length` to bound the session;
- `--turn` for an explicit TURN relay when peer-to-peer fails.

`capsule code` and `capsule cursor` also accept `--repo owner/repository` to clone a repo at session start. `capsule claude` does not.

### Demo

```bash
capsule term <config-tag>
capsule term -u <unique-id> --idle-timeout 2h --max-session-length 8h
capsule term <config-tag> -e "nvidia-smi"
capsule term <config-tag> --direct
capsule term <config-tag> --direct --options "-L 3000:localhost:3000"

capsule exec <config-tag> "df -h"
capsule code <config-tag> --repo mihira-ai/your-experiment
capsule claude <config-tag>
```

### Lab

1. Open a terminal on any NVIDIA machine with `capsule term`. Run `nvidia-smi` and `whoami`.
2. Run the same `nvidia-smi` non-interactively with `capsule exec <tag> "nvidia-smi"`.
3. Open VS Code on the same machine with `capsule code <tag>`. Confirm the integrated terminal is on the remote.
4. Open VS Code again, this time with `--direct`. Compare the connection latency informally.
5. Re-open the terminal session with `--idle-timeout 30m --max-session-length 1h`. Note the message describing the limits.

**Checkpoint:** You can choose between `term`, `exec`, `code`, and `claude` for a given workflow and justify the choice.

### Stretch

- Run `capsule term <tag> --direct --options "-L 9090:localhost:9090"` and start `python -m http.server 9090` on the remote. Visit `http://localhost:9090` locally. Convince yourself why `--direct` makes port-forwarding tractable.
- Read the `--turn` flag docs. When would you supply a custom TURN server, and what does that imply about your network?

### Reliability lens

Three rules:

1. If SshRTC negotiation fails, retry once after `capsule session endall`. If it fails again, fall through to `--direct` and report the original failure with logs.
2. Always supply `--idle-timeout` and `--max-session-length` for batch-like work (benchmarks, long evals). Otherwise an idle terminal can pin a GPU for hours.
3. Don't leave stale `capsule-<uniqueId>` entries in your local `~/.ssh/config`. They cause cryptic Remote-SSH failures in VS Code.

---

## Module 6 - Files, Storage, and the OneDrive Mount

### Concept

Three orthogonal ways to move bytes between your laptop and a remote box:

1. **Auto-mounted OneDrive (`~/OneDrive`)**: fastest path for files you want to share across multiple machines. Set up once with `capsule auth storage`; every subsequent `capsule term`/`code`/`cursor`/`claude`/`stream` auto-mounts your `OxCapsule` OneDrive folder.
2. **SCP**: for one-off transfers, especially large blobs. `capsule scp upload` and `capsule scp download` understand both `<config-tag>` (any pool member) and `-u <unique-id>` (specific box). Add `--direct` if SshRTC is misbehaving.
3. **File passthrough**: small dotfiles you want copied at session start (`.vimrc`, `.gitconfig`). Configured locally with `capsule config files add`.

### Demo

```bash
capsule auth storage           # one-time OneDrive OAuth

capsule term <tag>
# Inside the session:
ls ~/OneDrive
cp model.safetensors ~/OneDrive/

# From your laptop:
capsule scp upload <tag> ./data/ /workspace/data/
capsule scp download <tag> /workspace/output/results.csv ./results/

capsule config files add .gitconfig ~/.gitconfig
capsule config files list
capsule config storage-mount-dir set /workspace/cloud
```

### Lab

1. Run `capsule auth storage` if you haven't yet. Connect to any machine and verify `ls ~/OneDrive` shows your `OxCapsule` folder.
2. Drop a `hello.txt` into `~/OneDrive` from machine A. Disconnect, connect to machine B, confirm the file is there.
3. Upload a small dataset to a remote machine with `capsule scp upload`. Then download a file back.
4. Add your `.gitconfig` to the file passthrough list. Reconnect and confirm `git config --global --list` reads it on the remote.
5. Override the storage mount to `/workspace/cloud` and reconnect. Confirm the mount moved. Then `unset` it.

**Checkpoint:** You know when to reach for each of the three transfer mechanisms, and you understand that the OneDrive mount is the same folder no matter which machine you're on.

### Reliability lens

If `~/OneDrive` is empty on the remote, the daemon couldn't mount it. Common causes: `rclone` missing locally, expired OneDrive OAuth, or VFS cache fighting with a previous session. Recovery: `capsule auth storage` again, then reconnect.

---

## Module 7 - Streaming & Containers

### Concept

`capsule stream <config-tag>` opens a hardware-encoded WebRTC stream of the remote desktop (or a single app with `--app <name>`). Use it for ComfyUI, Blender, browser-based debugging on the remote, or any GUI work. Hardware encoders used: NVENC (NVIDIA), VAAPI (Intel/AMD on Linux), VideoToolbox (Apple Silicon).

`capsule docker <config-tag>` launches a container on the remote and drops you into it. The defaults are `ubuntu:latest` with `bash`. Use `--image`, `--memory`, `--command`, `--volume`, and `-- <docker-args>` for everything else.

### Demo

```bash
capsule stream <config-tag>
capsule stream <config-tag> --app "blender"

capsule docker <config-tag> --image pytorch/pytorch:latest --memory 16
capsule docker <config-tag> --image nvidia/cuda:12.0-devel \
    --command "python train.py" \
    --volume "/data:/data:ro;/workspace:/workspace"
capsule docker <config-tag> -- --gpus all
```

### Lab

1. Stream a remote desktop. Verify clipboard sync by copying text both directions.
2. Stop the stream, then `capsule stream <tag> --app firefox` (or any app installed on the remote).
3. Launch an Ubuntu container on a remote machine. Inside, `nvidia-smi` should fail (no GPU exposed).
4. Re-launch with `-- --gpus all` and confirm `nvidia-smi` now sees the GPU.

**Checkpoint:** You can pick between `stream` (GUI) and `term` (CLI) based on the task, and you can expose a GPU into a container.

### Reliability lens

WebRTC streaming is bandwidth-sensitive. On a flaky network the first thing to drop is the video bitrate, then audio, then input. If users report "input lag", confirm their downlink with a separate speed test before assuming the encoder is at fault.

---

## Module 8 - Model Evaluation: Benchmarking (the InferenceMAX path)

> This is the most important module for the reliability & model evaluation track. Spend extra time here.

### Concept

`capsule benchmark <config-tag> <model>` provisions an inference server on the remote and drives it with InferenceMAX. The output is throughput, latency percentiles, and cost-per-token metrics, all uploaded to the Capsule benchmark dashboard unless you pass `--no-upload`.

Four backends are supported, each with different sweet spots:

| Backend     | When to choose it                                                |
|-------------|------------------------------------------------------------------|
| `vllm`      | Default. Best for NVIDIA, batched serving, paged-attention.      |
| `llamacpp`  | CPU-friendly, GGUF quantizations (`Q4_K_M`, `Q5_K_M`).            |
| `mlx`       | Apple Silicon.                                                   |
| `oxpython`  | OXMIQ Python runtime; use for in-house evaluation paths.         |

Key knobs and what they mean:

- `--concurrency` (`-c`): max-num-seqs. How many requests the server batches at once.
- `--input-length` / `--isl`: tokens per prompt.
- `--output-length` / `--osl`: tokens generated per response.
- `--num-prompts` (`-n`): total requests sent. Defaults to `concurrency × 10`.
- `--tensor-parallelism` / `--tp`: split the model across N GPUs.
- `--quant` / `-q`: quantization scheme (`awq`, `gptq`, `fp8`, `int8`, `Q4_K_M`, `Q5_K_M`).
- `--api-base` + `--api-key`: skip provisioning entirely and benchmark an OpenAI-compatible endpoint you already have.

### Demo

```bash
# Default vllm bench on an NVIDIA machine
capsule benchmark <tag> meta-llama/Llama-3.1-8B-Instruct

# Realistic eval workload
capsule benchmark <tag> meta-llama/Llama-3.1-8B-Instruct \
    --concurrency 8 --input-length 256 --output-length 256 --num-prompts 40

# Quantized model on llamacpp
capsule benchmark <tag> Qwen/Qwen2.5-7B-Instruct-GGUF \
    --backend llamacpp --quant Q4_K_M

# Multi-GPU tensor parallel
capsule benchmark <tag> meta-llama/Llama-3.1-70B-Instruct --tp 4

# Against an external endpoint, no machine deploy
capsule benchmark --api-base http://localhost:8000 --api-key test meta-llama/Llama-3.1-8B-Instruct

# Long run, suppress upload while iterating
capsule benchmark <tag> <model> --idle-timeout 4h --max-session-length 8h --no-upload
```

### Lab

1. Run a default benchmark on an 8B model on an NVIDIA box. Note the throughput in tokens/sec.
2. Re-run with `--concurrency 16` and `--num-prompts 160`. Compare throughput and latency.
3. Run the same model with `--quant awq`. Compare quality (eyeball a chat output) and throughput.
4. Run on a multi-GPU machine with `--tp 2`. Confirm the server actually used both GPUs (peek at `nvidia-smi` during the run from a second terminal).
5. Open the dashboard at `https://oxcapsulebenchmark.z22.web.core.windows.net` and find your runs.

**Checkpoint:** Given a hardware target and a model, you can pick a backend, set `tp` and concurrency reasonably, and explain what your numbers mean.

### Stretch

- Pick two models of similar size from different families (e.g. Llama-3.1-8B vs Qwen2.5-7B) and produce a small comparison table on the same hardware with identical concurrency, ISL, and OSL.
- Drive `capsule benchmark --api-base` against `capsule chat`'s server (Module 9). Confirm the numbers from the two paths match.

### Reliability lens

Benchmarks are long-running and silent on the SSH channel; that's exactly the kind of session that gets killed by an aggressive idle timeout. Always pass `--idle-timeout` and `--max-session-length` longer than your expected run, and prefer `capsule schedule` (Module 10) for anything over an hour. If a benchmark "vanishes", check session logs first, the dashboard second, and only blame the model last.

---

## Module 9 - Model Evaluation: Interactive Chat

### Concept

`capsule chat <config-tag> <model>` provisions the same inference stack as `benchmark`, but drops you into an `aichat` session for hands-on probing. Backend auto-detects from the GPU; everything else is overridable.

This is your go-to tool for: prompt regression spot-checks, sanity-checking quantization, fuzzing system prompts, and verifying that a benchmark's outputs are actually intelligible (a 0-token-output server has fantastic latency).

### Demo

```bash
capsule chat <tag> meta-llama/Llama-3.1-8B-Instruct

# With sampling controls and a system prompt
capsule chat <tag> <model> --temperature 0.3 --max-tokens 2048 \
    --system-prompt "You are a helpful coding assistant."

# GGUF model on llamacpp
capsule chat <tag> Qwen/Qwen2.5-7B-Instruct-GGUF --backend llamacpp --quant Q4_K_M

# Tool-calling agent
capsule chat <tag> <model> --agent oxsol

# Against external endpoint
capsule chat --api-base http://localhost:8000 --api-key mykey <model>

# Gated model with HF token, auto-cleanup container on exit
capsule chat <tag> meta-llama/Llama-3.1-70B-Instruct --hf-token $HF_TOKEN --tp 4 --rm
```

### Lab

1. Chat with an 8B model. Test five prompts: a simple factual question, a math word problem, a Python function ask, a refusal probe ("how do I make X?"), and a long-context request.
2. Re-run with `--temperature 0.1` and the same prompts. Compare consistency of outputs.
3. Spin up the same model with `--quant awq` and rerun the prompts. Note any quality regressions.
4. Use `--agent oxsol` to give the model tool-calling. Try a multi-step task.

**Checkpoint:** You can deploy a model and run a structured prompt regression in under five minutes.

### Reliability lens

A useful trick during incident response: when a customer reports "model is broken", reproduce on the same machine with `capsule chat -u <unique-id> <model>` and the customer's reported sampling settings. If it works for you, the issue is likely in their client or sampling config, not in inference.

---

## Module 10 - Scheduled Jobs, Agents, and the Reliability Toolkit

### Concept: scheduled jobs

`capsule schedule` is the right tool for any compute that runs longer than a coffee break:

- `schedule start <tag> --script ./train.sh` queues a job. It runs without you holding an SSH session open.
- `--name`, `--timeout`, `--retry`, `--env`, `--with-file`, `--machine-name` shape what runs and where.
- `schedule status <tag>` lists jobs; filter by `--me`, `--user`, `--state pending|running|completed|failed`; add `--show-start` for ETA on queued work.
- `schedule cancel <job-id>` or `schedule cancel --all`.
- `schedule logs <job-id>` (with optional `--tail`) for output.

### Concept: agents & MCP

- `capsule mcp` installs a Model Context Protocol server config into Claude Desktop / Claude Code so the assistant can drive Capsule on your behalf. `--uninstall` to remove, `--output` to dump the config without installing.
- `capsule agent` (gated by `CAPSULE_AGENT_ENABLED=1`) is a pre-GA natural-language fleet-management agent. Wire it to an OpenAI-compatible endpoint and talk to your fleet.

### Concept: the reliability toolkit

These are the commands you'll reach for most often in a triage session:

```bash
capsule status                    # auth, identity, expiry
capsule env show                  # current environment
capsule config customer show      # current customer fleet
capsule session endall                   # tear down stale WebRTC + SSH state
capsule --version                 # exact CLI build for bug reports
capsule --no-banner list          # clean output for logs / pasting in tickets
```

And the known-quirks list every intern should memorise:

| Symptom                                  | Fix                                                                          |
|------------------------------------------|------------------------------------------------------------------------------|
| Auth fails in browser flow               | The CLI falls back to a manual token at `https://oxmiq.ai/oxcapsule/auth`.   |
| `capsule list` shows wrong machines      | Check `env show` and `config customer show` before anything else.            |
| SshRTC won't connect                     | `capsule session endall`, retry, then `--direct` as fallback. Capture logs.         |
| VS Code Remote-SSH errors after a session| Remove `capsule-<uniqueId>` blocks from `~/.ssh/config`.                     |
| macOS Keychain prompts every command     | Click "Always Allow" once.                                                   |
| Windows PowerShell filter with `>` fails | Use `capsule` (not `cap`) and quote the whole filter argument.               |
| `capsule update` fails                   | Auth token must be valid; close all SshRTC sessions before retrying.         |
| `gh release download` 401/403            | Re-check `GH_TOKEN` scopes (`repo`, `read:org`, `workflow`, `user`).         |

### Demo

```bash
capsule schedule start <tag> --script ./eval.sh --name "llama-eval-v3" --timeout 4h
capsule schedule status <tag> --me --state running
capsule schedule logs <job-id> --tail 100
capsule schedule cancel <job-id>

capsule mcp                       # install Capsule MCP for Claude
capsule mcp --output ./mcp.json   # inspect config without installing

capsule session endall
capsule --version
```

### Lab

1. Write a tiny `eval.sh` that runs `capsule benchmark` against an external `--api-base` and prints the result. Submit it with `capsule schedule start`, then watch `schedule status` and `schedule logs --tail`.
2. Cancel the job you just submitted.
3. Run `capsule mcp --output ./mcp.json` and read the file. Identify, by name, which Capsule actions the MCP exposes to Claude.
4. Run `capsule session endall`. Re-list machines. Confirm nothing visibly changed for you (`cleanup` is mostly cleanup of *state*, not visible fleet objects).
5. Reproduce one entry from the known-quirks table on purpose (e.g. set the wrong customer) and follow the recovery recipe.

**Checkpoint:** You can run, monitor, and cancel a scheduled job. You can navigate the troubleshooting table from memory.

### Stretch

- Configure `capsule agent` against a local OpenAI-compatible server (or a `capsule chat` deployment) and ask it questions about your fleet.
- File a (sandboxed) bug report against the project that includes: `capsule --version`, `env show`, `config customer show`, the exact failing command, and the relevant logs. This is the report format your team will love you for.

### Reliability lens

You are now equipped to be the first responder. The shape of a good triage:

1. Reproduce yourself. If you can't reproduce, you don't have a bug yet; you have an incident.
2. Capture `capsule --version`, `env show`, `config customer show`, the exact command, the timestamp, and the unique ID of the machine (`capsule list --all`).
3. Try `cleanup` then `--direct` before escalating.
4. Default to scheduled jobs for anything long-running. Don't tie up a GPU on an interactive session that no human will be looking at for hours.

---

## Capstone Lab - Bench-to-Dashboard Round Trip

Do this end-to-end without notes. Time yourself.

1. From a fresh shell, confirm your environment is `prod` and customer is `micc`.
2. Find any NVIDIA machine with at least 24 GB VRAM that nobody else is using.
3. Open VS Code on that machine via SshRTC. Confirm `nvidia-smi` from the integrated terminal.
4. From your laptop, upload a small `prompts.txt` file to `/workspace/` on that machine via SCP.
5. Run a benchmark on `meta-llama/Llama-3.1-8B-Instruct` with concurrency 8, ISL 256, OSL 256. Note the throughput.
6. Re-run with `--quant awq`. Note the new throughput.
7. Open the benchmark dashboard and find both runs.
8. Schedule the same benchmark as a background job with a 1-hour timeout.
9. While the scheduled job runs, open `capsule chat` against the same model and verify a few prompts qualitatively.
10. After everything completes, run `capsule session endall`. Run `capsule list --users` and confirm you are no longer holding the machine.

Target time: under 30 minutes once you've done it once. Reliability work is mostly muscle memory.

---

## Glossary

- **Config tag**: a machine pool/class name; the scheduler hands you any available machine in that pool.
- **Unique ID**: a specific physical machine; always requires `-u`/`--unique`.
- **SshRTC**: Capsule's WebRTC-based SSH data channel. Default connection method.
- **Direct SSH**: traditional TCP SSH (`--direct`). Useful as a fallback or for clean port-forwarding.
- **Environment**: backend deployment (`prod`, `public`, `dev`, `demo`). Determines B2C tenant and endpoint.
- **Customer**: fleet selector inside an environment (`micc`, `modelhosting`, `oneplay`, `cree8`).
- **InferenceMAX**: the benchmark suite invoked by `capsule benchmark`.
- **TURN**: a WebRTC relay used when peer-to-peer NAT traversal fails.
- **MCP**: Model Context Protocol; how Claude Desktop/Code talks to Capsule as a tool.

---

## Self-assessment

If, by the end of the course, all of the following are true, you've passed:

- You can install, authenticate, and produce a benchmark run on a fresh laptop in under 15 minutes.
- You can debug a "Capsule isn't working" report by walking through env, customer, auth, and connection-method as a checklist, out loud, without hesitating.
- You can write a `capsule schedule` job that wraps a non-trivial eval and recover its logs after the fact.
- You can explain to a new intern, in two minutes, the difference between a config tag and a unique ID, and the difference between SshRTC and Direct SSH.

Welcome to the team.

---

# Appendix A - Lab Extensions & Reliability Drills

The labs above teach you the happy path. This appendix teaches you the *unhappy* path: the situations you'll actually be paid to handle. Each section pairs an extension lab (more depth on a module's topic) with a reliability drill (a fault to inject and triage).

## How to use this appendix

- **Extension labs (E.x)**: deepen a single module. Budget ~30 min each.
- **Reliability drills (R.x)**: instructor-led fault injection; pairs work through the triage decision tree. Budget ~20 min each.
- **Mastery checklist** at the end: 9 items. Hit them all and you're calibrated.

---

## E.1 - Routing-matrix sweep (Modules 1, 3)

**Goal**: walk all 16 cells of the env × customer matrix and observe what each one returns.

1. Script a loop: for env in {prod, public, dev, demo}, for customer in {micc, modelhosting, oneplay, cree8}, call `capsule env set $env && capsule auth login && capsule config customer set $customer && capsule list | wc -l`.
2. Record the result count for each cell in a 4×4 table.
3. Identify the **3 cells** where you have access. Note which envs require a separate re-auth.
4. Submit the table to your instructor.

**Expected outcome**: ~3-5 cells populated for an intern; everywhere else returns empty or 403.

## E.2 - Install on a stranger's laptop (Module 2)

**Goal**: prove you can hit the 15-minute install bar on hardware you don't control.

1. Pair with another intern. Use *their* laptop, not yours.
2. Start a stopwatch.
3. Install from scratch: brew/dpkg/msi → tap → bottle → login → `capsule list` returning a real fleet.
4. Stop the stopwatch.
5. Record the elapsed time and any obstacles (corporate proxy, DNS, missing CLI tools).

**Target**: <15 min. **Outcome**: if you exceed 20 min, write a one-paragraph postmortem on what slowed you down.

## E.3 - Filter speed-run (Module 4)

**Goal**: build muscle memory for fleet filtering.

1. For each of these targets, write the *single* `capsule list` command that returns it:
   - All H100 machines with no active users.
   - All Tenstorrent Blackhole machines.
   - All Apple Silicon machines.
   - A specific known unique ID.
   - Any GPU with ≥40 GB VRAM.
2. Time yourself. Target: <10 sec per command including typing.

## E.4 - Five verbs on one box (Module 5)

**Goal**: feel the difference between the connection verbs.

1. Pick a single unique ID. Open it 5 ways in 5 terminal panes:
   - `capsule term -u <id>`
   - `capsule exec -u <id> -- htop`
   - `capsule code -u <id>`
   - `capsule cursor -u <id>`
   - `capsule claude -u <id>`
2. Time each attach. Compare against the targets (term <1s, exec <0.5s, code ~3s, cursor ~3s, claude ~2s).
3. In each surface, run `nvidia-smi`. Note the user experience differences.

## E.5 - Storage scope experiment (Module 6)

**Goal**: internalize the 3-scope durability model.

1. On a single machine, write the same 100MB file to `/tmp/test.bin`, `~/test.bin`, and `~/OneDrive/test.bin`.
2. Time each write. Record the throughput.
3. Restart the container (or `capsule session endall` and reconnect).
4. Confirm `/tmp/test.bin` is gone; `~/test.bin` survives; `~/OneDrive/test.bin` is also visible from a *second* machine.
5. Delete `~/OneDrive/test.bin` from machine A; confirm it disappears from machine B within ~60 sec.

**Outcome**: a one-paragraph rule for "where do my outputs go?" that you can recite.

## E.6 - Benchmark variance study (Module 8)

**Goal**: see why one number is not a measurement.

1. Pick a single H100 unique ID. Run `capsule benchmark --model llama3.1-8b --config nv-h100` **5 times back-to-back**.
2. Record decode tok/sec for each run.
3. Compute median, p95, and (max − min) / median.
4. If variance is >10%, identify the cause: thermal warm-up, noisy neighbor, or measurement artifact.
5. Add a 60-second warm-up before each run; repeat. Does variance drop?

**Target**: <5% variance with proper warm-up. **Outcome**: a one-line "how I report a benchmark number" rule.

## E.7 - Schedule + recover (Module 10)

**Goal**: prove you can lose nothing on a long job.

1. Write a `sweep.sh` that runs 4 benchmarks taking ~10 min each.
2. Submit it with `capsule schedule start --script ./sweep.sh --config nv-h100 --timeout 1h`.
3. Note the job ID. **Close your laptop.** Walk away for 45 min.
4. Reopen. Find the job. Pull its logs.
5. Verify the outputs landed in OneDrive (not just persistent volume).

**Outcome**: a job you can hand off to a teammate without loss.

---

## R.1 - Empty list triage (Module 3)

Instructor sets a student's env+customer to a cell they don't have access to. Student must:
- Recognize the empty list.
- Walk the triage tree out loud (env? customer? auth?).
- Resolve in <2 min.

## R.2 - Token expiry mid-session (Module 2)

Instructor lets a student work normally for 60+ min, then has them run a command. They get 401/403. Student must:
- Recognize the auth failure (not a fleet failure).
- Re-authenticate.
- Resume without re-doing prior work.

## R.3 - SshRTC stall (Module 5)

Instructor simulates a degraded WebRTC connection (or asks student to work over hotspot). Student must:
- Notice keystroke echo >80ms.
- Fall back to `--direct`.
- Confirm responsiveness improves.
- File the WebRTC peer issue (don't just work around it).

## R.4 - Disappeared data (Module 6)

Instructor has student write benchmark output to `/tmp`, then cleanup. Student reports "data disappeared." Student must:
- Identify the scope (ephemeral).
- Explain why it's gone.
- Re-run with a durable scope.

## R.5 - Thermal-throttled benchmark (Module 8)

Instructor preloads a machine with a heavy workload, then has student benchmark on it. Student must:
- See decode tok/sec well below the 1500-2500 band.
- Check `nvidia-smi -q -d TEMPERATURE`.
- Diagnose throttle vs. driver vs. PCIe.
- Either wait or pick a different machine.

## R.6 - Forgotten --parallel (Module 10)

Instructor has student submit an 8-model sweep without `--parallel`. After 30 min, student checks ETA: it's 5.5 hours, not 90 min. Student must:
- Kill the job.
- Resubmit with `--parallel 4`.
- Compute the cost difference and report it.

---

## Mastery checklist

Self-grade after the labs and drills. You're calibrated when **all 9** are true:

- [ ] I can name and recite the 16 routing cells without hesitation.
- [ ] I can install Capsule on a fresh laptop in <15 min.
- [ ] I can write the right `capsule list` filter for any hardware class in <10 sec.
- [ ] I can pick the right connection verb in <5 sec for any task.
- [ ] I can predict whether a given file path is ephemeral, persistent, or synced.
- [ ] I have run >=3 benchmarks and reported median + p95.
- [ ] I have scheduled, walked away, and recovered logs from a multi-hour job.
- [ ] I can walk the triage decision tree from memory.
- [ ] I can compute the cost of a sweep at $2/H100-hour and the savings from `--parallel`.

If any are false, return to the matching module's lab and the matching drill.

---

# Appendix B - Numerical Anchors

These are the numbers you must carry in your head. They are the same anchors used in the Workbook (Appendix B) and Cheatsheet (Page 3).

| Quantity | Value |
|---|---|
| Fleet size (mid-2026) | ~200 machines |
| Routing matrix | 4 envs × 4 customers = 16 cells |
| SshRTC keystroke echo (p50, healthy) | <80 ms |
| Direct SSH keystroke echo (p50) | <40 ms |
| H100 decode (single, Llama-3.1-8B) | 1500-2500 tok/sec |
| H100 batched | 10K-30K tok/sec |
| Per-M-token cost on H100 (batched) | ~$0.05 |
| OneDrive sustained write | <5 MB/s |
| Local NVMe write | >1 GB/s |
| Auth token TTL | ~60 min |
| Log retention default | 7 days |
| Min runs for variance reporting | ≥3 (median + p95) |
| 8-model sweep serial → parallel | 6 hr → 90 min |
| Sweep cost @ $2/GPU-hr × 4 GPUs | $12 |

---

# Appendix C - Concept-Graph Cross-Reference

| Module | Primary concept IDs |
|---|---|
| 1 - Foundations | `capsule-fleet`, `capsule-routing`, `sshrtc-transport` |
| 2 - Install | `capsule-install`, `oxgate-auth`, `b2c-tenant` |
| 3 - Env/Customer | `capsule-env`, `capsule-customer`, `b2c-tenant` |
| 4 - Fleet | `capsule-fleet`, `config-tag`, `unique-id` |
| 5 - Connect | `capsule-connect`, `sshrtc-transport`, `mcp-server` |
| 6 - Storage | `capsule-storage`, `onedrive-mount`, `persistent-volume` |
| 7 - Streaming | `capsule-streaming`, `webrtc-encoder`, `docker-runtime` |
| 8 - Benchmark | `inferencemax`, `benchmark-variance`, `gpu-throttling` |
| 9 - Chat | `interactive-eval`, `model-deployment`, `prompt-probing` |
| 10 - Schedule | `capsule-scheduler`, `parallel-execution`, `log-retention` |
