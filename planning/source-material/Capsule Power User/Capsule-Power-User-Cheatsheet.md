O X M I Q
Capsule — Power-User Cheat Sheet

V 1   ·   A 4   ·   R E L I A B I L I T Y   &   M O D E L   E V A L   T R A C K

D A I L Y   L O O P

capsule status → capsule env show → capsule config customer show → capsule list --users → capsule term <tag> →
work → capsule cleanup

0 1   —   A U T H   &   I D E N T I T Y

capsule auth login          # browser
capsule status              # identity
+ expiry
capsule auth logout
capsule auth storage        # OneDrive
OAuth
capsule auth token          # print
token

Browser flow falls back to manual token at
oxmiq.ai/oxcapsule/auth. Headless: export
CAPSULE_AUTH_TOKEN.

0 2   —   E N V I R O N M E N T

prod mihirainfra.b2c · internal prod
public oxcapsule.b2c · external/partner
dev dev / test
demo demonstrations
capsule env show
capsule env set public
capsule auth login          # always
re-auth

public & the others use different B2C tenants —
separate user registries. Switching env requires
fresh login.

0 3   —   C U S T O M E R   F L E E T

micc default main fleet
modelhosting model hosting GPUs
oneplay OnePlay partner machines
cree8 Cree8 partner machines
capsule config customer show
capsule config customer set modelhosting
capsule config customer unset       # env default

If capsule list looks wrong, this is the FIRST thing
to check.

0 4   —   L I S T I N G   &   F I L T E R I N G

capsule list                # by config
tag
capsule list --all          # unique
IDs
capsule list --users        # who is on
capsule list --json | jq .

--filter "vendor=nvidia,vram>=24"
keys vendor, gpu, os, vram, memory, cores, ci
vendors nvidia, tenstorrent, amd, intel
ci= true / false

PowerShell: use capsule (not cap) and quote the
filter — > is redirection in PS.

0 5   —   C O N N E C T   ( O N E   R O U T I N G
L A N G U A G E )

capsule term remote shell (default SshRTC)
capsule exec one-off command
capsule code VS Code Remote-SSH
capsule cursor Cursor Remote-SSH
capsule claude Claude Code Desktop

Shared flags: <tag> or -u <id>, --direct, --idle-timeout, --max-session-length, --turn. code/cursor also accept --repo owner/repo. term aliases: terminal, ssh, launch.

0 6   —   C O N N E C T I O N   R E C I P E S

capsule term <tag>
capsule term -u boostergold461
capsule term <tag> -e "nvidia-smi"

# port-forward (direct SSH)
capsule term <tag> --direct \
  --options "-L 3000:localhost:3000"

# bounded session
capsule term <tag> \
  --idle-timeout 2h \
  --max-session-length 8h

# IDE with repo clone
capsule code <tag> --repo owner/repo

0 7   —   F I L E S   &   S T O R A G E

capsule auth storage         # once, OAuth
ls ~/OneDrive                # auto-mounted

# SCP
capsule scp upload <tag> ./src /dst
capsule scp download <tag> /src ./dst
  + --direct, --options "-l 50000"

# Dotfile passthrough
capsule config files add .gitconfig
~/.gitconfig
capsule config files list
capsule config files remove .vimrc
capsule config files clear

# Custom mount
capsule config storage-mount-dir set /workspace/cloud
capsule config storage-mount-dir unset

0 8   —   S T R E A M   &   D O C K E R

capsule stream <tag>              # full desktop
capsule stream <tag> --app "blender"

capsule docker <tag>              # ubuntu:latest
capsule docker <tag> \
    --image pytorch/pytorch:latest \
    --memory 16
capsule docker <tag> \
    --image nvidia/cuda:12.0-devel \
    --command "python train.py" \
    --volume "/data:/data:ro;/workspace:/workspace"
capsule docker <tag> -- --gpus all   # passthrough

Hardware encoding: NVENC / VAAPI / VideoToolbox. Adaptive bitrate; clipboard sync both ways.

0 9   —   C O M F Y U I   &   C L A U D E   M C P

capsule comfy <tag>                # default :8188
capsule comfy <tag> --port 8190 \
    --data-dir ~/my-comfyui \
    --hf-token hf_xxx
capsule comfy <tag> --image my/comfyui:custom

# Open in browser at http://localhost:8188

# Capsule MCP for Claude Desktop/Code
capsule mcp                       # install
capsule mcp --uninstall
capsule mcp --output ./mcp.json   # inspect

1 0   —   C A P S U L E   A G E N T   ( P R E - G A )

export CAPSULE_AGENT_ENABLED=1
export OXMIQ_AGENT_API_BASE=http://127.0.0.1:8080/v1
export OXMIQ_AGENT_API_KEY=your-api-key
export OXMIQ_AGENT_MODEL=openai/capsule

capsule agent                                # chat
capsule agent -p "list nvidia >=16GB VRAM"   # one-shot
capsule agent -c "show me free GPUs"         # iterative

Requires uv installed (brew install uv) and a valid
OpenAI-compatible endpoint.

O X M I Q   ·   C A P S U L E   P O W E R - U S E R   ·   P A G E   1   O F   2

A R C H I T E C T I N G   A T O M S   T O   A G E N T S

O X M I Q
Capsule — Cheat Sheet (cont.)

E V A L   ·   S C H E D U L E   ·   T R I A G E

T R I A G E   L O O P   —   W H E N   S O M E T H I N G   I S   B R O K E N

reproduce → capture: --version, env, customer, cmd, timestamp, unique-id → capsule cleanup → retry →
--direct fallback → escalate with logs

1 1   —   B E N C H M A R K   ·   C O R E   F L A G S

1 4   —   S C H E D U L E   ( B A T C H   J O B S )

1 7   —   E N V   V A R S

capsule benchmark <tag> <model>

-c / --concurrency batch (default 4)
--isl / --osl in / out tokens (128 / 128)
-n / --num-prompts total reqs (c × 10)
--tp tensor-parallelism (1)
-q / --quant awq, gptq, fp8, int8, Q4_K_M,

Q5_K_M
-b / --backend vllm, llamacpp, mlx,

oxpython

--api-base/-key external endpoint, no

deploy

--no-upload skip dashboard upload
--idle/--max timeouts; always set for long

runs

1 2   —   B E N C H M A R K   R E C I P E S

# Standard 8B eval
capsule benchmark <tag> \
  meta-llama/Llama-3.1-8B-Instruct \
  -c 8 --isl 256 --osl 256 -n 40

# Multi-GPU
capsule benchmark <tag> <model> --tp 4

# Quantized comparison
capsule benchmark <tag> <model> --quant
awq
capsule benchmark <tag> <model> \
  --backend llamacpp --quant Q4_K_M

# Against existing endpoint
capsule benchmark --api-base http://localhost:8000 \
  --api-key test <model>

# Long-run safety
capsule benchmark <tag> <model> \
  --idle-timeout 4h --max-session-length 8h

1 3   —   C H A T   F L A G S

capsule chat <tag> <model>

-b / --backend override auto-detect
--temperature sampling (default 0.7)
--max-tokens output cap
--system-prompt prepended each turn
--agent aichat agent + MCP tools (oxsol)
--hf-token for gated HF models
--rm cleanup container on exit
--no-stream disable streaming
--client-name aichat client id (default

capsule)
--api-base/-key talk to existing server

capsule schedule start <tag> \
  --script ./train.sh --name "v2" \
  --timeout 8h --retry 3 \
  --env "EPOCHS=100" --env "LR=0.001" \
  --with-file ./model.py

# Target a named machine
capsule schedule start --machine-name
NV-4090-01 \
  --script ./benchmark.sh

# Monitor
capsule schedule status <tag> --me \
  --state running --show-start
capsule schedule status <tag> --user
x@example.com
capsule schedule logs <job-id> --tail
100

# Cancel
capsule schedule cancel <job-id>
capsule schedule cancel --all

Use for anything > 1 hour. Don't tie up GPUs on
idle terminals.

1 5   —   T R I A G E   C H E A T   C O D E S

Wrong machines env show + customer show
SshRTC fails cleanup → retry → --direct
VS Code remote err rm capsule-* in ~/.ssh/

config

macOS keychain "Always Allow" once
PS filter > use capsule, quote arg
Update fails close SshRTC sessions first
gh download 401 re-check GH_TOKEN

GH_TOKEN install / update (scopes: repo,

read:org, workflow, user)

CAPSULE_AUTH_TOKEN headless auth
CAPSULE_SSH_PRIVATE_KEY override SSH key
CAPSULE_SSH_PUBLIC_KEY override pub key
CAPSULE_DEFAULT_APP_CONFIG default app

config

CAPSULE_AGENT_ENABLED enable agent (pre-

GA)

HF_TOKEN gated HF models
OXMIQ_AGENT_API_BASE agent upstream URL
OXMIQ_AGENT_API_KEY agent API key
OXMIQ_AGENT_MODEL agent model name
HOMEBREW_GITHUB_API_TOKEN macOS install (=$GH_TOKEN)

1 8   —   A L I A S E S   &   I D I O M S

cap same as capsule (PS quirks with >)
terminal / ssh / launch aliases of term
<tag> pool name → any available
-u <id> specific physical machine
--direct bypass WebRTC, use TCP SSH
--turn url explicit WebRTC relay
--idle-timeout kill if idle for X
--max-session-length hard cap on session
--repo owner/r code & cursor only —

clones on connect

scopes

1 9   —   C O N F I G   F I L E S   &   P A T H S

Auth fails (browser) manual token at oxmiq.ai/oxcapsule/auth

~/OneDrive empty re-run capsule auth storage

Benchmark vanished check timeouts; logs; dashboard

1 6   —   D I A G N O S T I C S

capsule status                # auth + expiry
capsule env show              # current env
capsule config customer show  # current fleet
capsule cleanup               # tear down stale state
capsule --version             # build id (for bugs)
capsule --no-banner list      # clean output
capsule list --users          # who else is on
capsule list --json | jq .    # machine-readable

# Update
capsule update --check-only
capsule update
capsule update --pre-release

macOS ~/Library/Application Support/Capsule/
Windows %APPDATA%\capsule\
Linux ~/.config/capsule/
capsule.conf main configuration
capsule-customer.conf customer override
capsule_rsa(.pub) auto-generated SSH key
rclone.conf cloud storage config
config-files.json file passthrough mapping
capsule config banner show / hide
capsule config bashrc-override enable / disable

2 0   —   R E S O U R C E S

Bench dashboard oxcapsulebenchmark.z22.web.core.windows.net

Manual token oxmiq.ai/oxcapsule/auth
Install repo mihira-ai/ox.capsule
Brew tap mihira-ai/software-packages
Pre-release brew install capsule-pre
Update CLI capsule update [--pre-release]
Linux PATH ~/.local/capsule-cli/bin
Windows PATH C:\Program Files\Capsule-CLI\bin

Discord help #capsule-help

O X M I Q   ·   C A P S U L E   P O W E R - U S E R   ·   P A G E   2   O F   2

---

P A G E   3   —   N U M E R I C A L   A N C H O R S   &   T R I A G E

2 1   —   F L E E T   M A G N I T U D E S

Fleet total (mid-2026) ~200 machines
NVIDIA ~120 (3060/4090/5090/L40S/H100)
Tenstorrent ~40 (Wormhole n150, Blackhole p150)
AMD MI300 ~20
Apple Silicon ~20 (M2/M3 Ultra)
Routing matrix 4 env × 4 customer = 16 cells

If a config tag returns 0 hits, you have drifted env or customer.
If a config tag returns >25 hits, your filter is too broad.

2 2   —   L A T E N C Y   T A R G E T S

SshRTC keystroke echo (p50) <80 ms
Direct SSH keystroke echo (p50) <40 ms
capsule list (warm cache) <500 ms
capsule term attach <1 sec
capsule claude attach ~2 sec
capsule code (VS Code Remote) ~3 sec
Auth token TTL ~60 min

>80ms SshRTC sustained = check WebRTC peer setup, not network speed.

2 3   —   T H R O U G H P U T   T A R G E T S   ( H 1 0 0 ,   L L A M A   3 . 1   8 B )

Decode single-stream 1500-2500 tok/sec
Batched throughput 10K-30K tok/sec
TTFT (256-token prompt) <50 ms
Cost per M-tokens batched ~$0.05 ($2/H100-hr)

<800 tok/sec decode = thermal throttle / wrong driver / PCIe degradation.
Always report median + p95 over >=3 runs.

2 4   —   S T O R A G E   S C O P E S

/tmp ephemeral, gone on container restart
/home/$USER persistent volume, durable, machine-local
~/OneDrive durable + portable, slow (<5 MB/s sustained)
Local NVMe write >1 GB/s

OneDrive is sync, not backup. Deletions propagate. Do not use for hot benchmark output.

2 5   —   S T R E A M I N G   S U R F A C E S

Desktop streaming ~30 FPS, 5-15 Mbps, 1 encoder slot
App streaming ~60 FPS, 3-8 Mbps, 1 encoder slot
Container shell ~0 Mbps video, text only

For pytest or long CLI work: container shell. Desktop wastes bandwidth + GPU encoder.

2 6   —   S C H E D U L I N G   E C O N O M I C S

8-model sweep, serial ~6 hours
8-model sweep, --parallel 4 ~90 min
Cost @ $2/GPU-hr × 4 GPUs × 1.5 hr $12/sweep
Log retention default 7 days
Re-runs after retention loss not recoverable

Forgetting --parallel costs you 4.5 hours of wall-clock per sweep.

2 7   —   T R I A G E   D E C I S I O N   T R E E

User: "Capsule isn't working"
|
+-- capsule list works?
|   +-- 401/403 → token expired → capsule auth login
|   +-- timeout → check egress to *.capsule.oxmiq.io
|   +-- empty → wrong env or customer (check FIRST)
|
+-- Connect to box works?
|   +-- SshRTC hangs → try --direct
|   +-- both fail → box offline → check fleet dashboard
|   +-- slow (>80ms) → WebRTC peer setup
|
+-- Workload fails?
    +-- GPU 0% → CUDA/driver mismatch
    +-- thermal throttle → nvidia-smi -q -d TEMPERATURE
    +-- OOM → VRAM headroom vs model size
    +-- "data gone" → which storage scope? (see 24)

2 8   —   V E R B   S E L E C T I O N   M A T R I X

Task Verb
-----------------------------------------------
One-shot command (nvidia-smi) exec
Interactive shell term
Edit a Python file with autocomplete code or cursor
AI-assisted log analysis claude
Need port-forward / WebRTC failing term --direct

Default to the most specific verb. Don't reach for term when exec suffices.

2 9   —   C O M M O N   F A I L U R E   →   F I X

empty capsule list ............. wrong env/customer (90% of cases)
401 mid-session ................ token expired, re-login
SshRTC keystroke lag ........... try --direct; report WebRTC peer issue
benchmark variance >30% ........ thermal / noisy neighbor / wrong filter
"my data disappeared" .......... wrong storage scope (see 24)
schedule job logs missing ...... aged out past 7-day retention
brew install fails ............. corporate proxy / DNS / cert chain
capsule chat hallucinated text . unrelated to deployment; check model card

3 0   —   T H E   2 - M I N U T E   N E W - I N T E R N   T E S T

Can the candidate, in under 2 minutes:
[ ] Define config tag vs unique ID?
[ ] Define SshRTC vs Direct SSH?
[ ] Name 4 envs and 4 customers?
[ ] State the 3 storage scopes and their durability?
[ ] Walk the triage tree for "empty capsule list"?

If yes to all → power user. If no → revisit the relevant section.

O X M I Q   ·   C A P S U L E   P O W E R - U S E R   ·   P A G E   3   O F   3

