<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 8 - Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <a href="../">Day 40 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-08/module-5}
  </div>
</div>

# Week 8 Knowledge Check

**Week 8 · Capsule Foundations & Operations.** 31-question bank · **15 drawn per attempt** · aim for **strong (≥ 80%)**. This check is
formative, it never blocks you, but it's the week's bar. Answer the drawn questions,
then submit to reveal explanations and your score band.

<div class="ox-self-check" data-widget="self-check" data-id="week-08-m5-canonical" data-kind="wrap-up" data-draw="15" data-lesson="Week 8 · Capsule Foundations &amp; Operations" data-source="Canonical knowledge check">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Capsule offers two connection paths to a remote machine. They are:",
    "options": [
      "Frontend / Backend / DB",
      "SshRTC (WebRTC data channel, default) and Direct SSH (--direct)",
      "CPU / GPU / NIC",
      "Compile / Link / Run"
    ],
    "answer": 1,
    "explain": "SshRTC tunnels SSH over a WebRTC data channel (default, no public port needed); Direct SSH (--direct) is traditional TCP SSH used as a fallback or for clean port-forwarding."
  },
  {
    "stem": "In the triage tree, the command that confirms your auth is valid and shows your identity + token expiry is:",
    "options": [
      "capsule connect",
      "capsule status",
      "capsule node list",
      "ssh"
    ],
    "answer": 1,
    "explain": "Step 1 of the triage tree is <code>capsule status</code>; it reports your identity and token expiry, the fastest confirmation that auth is valid. (capsule connect and capsule node list are not real Capsule commands.)"
  },
  {
    "stem": "In Capsule, an 'environment' (prod, public, dev, demo) is best described as:",
    "options": [
      "A single GPU",
      "Your terminal",
      "A Kubernetes cluster",
      "A backend deployment that sets the Azure B2C tenant and API endpoint"
    ],
    "answer": 3,
    "explain": "An environment selects the backend deployment and its Azure B2C tenant/endpoint. The auth token is scoped per environment, so capsule env set is followed by a fresh capsule auth login. Set with capsule env set, inspect with capsule env show."
  },
  {
    "stem": "Capability filtering (e.g. <code>capsule list --filter \"vendor=nvidia,vram>=24\"</code>) is preferred over name-based filtering because:",
    "options": [
      "Faster typing",
      "It survives hardware churn and states the real requirement explicitly",
      "Required by Capsule",
      "Naming is broken"
    ],
    "answer": 1,
    "explain": "Machine names churn as hardware is added, retired, or renamed; a capability filter (vendor, VRAM, etc.) describes the real requirement, so the same command keeps returning the right machines across hardware changes. Always quote the filter so the shell doesn't mangle the '>' (see the Windows PowerShell quirk)."
  },
  {
    "stem": "You have several SshRTC tunnels open and want to close just ONE without disturbing the others. Which command targets a single tunnel?",
    "options": [
      "capsule session endall",
      "capsule cleanup --all",
      "capsule session end (by --unique-id, --port, or --session-id)",
      "capsule session kill Noble"
    ],
    "answer": 2,
    "explain": "capsule session end closes a single tunnel identified by its unique id, local port, or 32-char session id; capsule session endall closes them all at once, and capsule session list enumerates them. There is no capsule cleanup or capsule session kill."
  },
  {
    "stem": "<code>capsule term</code> (SshRTC) differs from raw SSH primarily by:",
    "options": [
      "Identity comes from your CLI auth; the connection is brokered over WebRTC with no manual key management",
      "Faster bytes",
      "Better colors",
      "Less secure"
    ],
    "answer": 0,
    "explain": "capsule term uses your Capsule auth identity and tunnels SSH over a WebRTC data channel: no public port and no manual SSH key management (Capsule auto-generates and manages the keys). Raw SSH gives you none of that."
  },
  {
    "stem": "The first thing to run after you open a remote shell with <code>capsule term &lt;config-tag&gt;</code> should be:",
    "options": [
      "rm -rf /",
      "nvidia-smi",
      "tmux a || tmux new -s work",
      "sudo apt update"
    ],
    "answer": 2,
    "explain": "Network connections drop: VPN timeouts, laptop sleep, ISP hiccups. Starting inside tmux (tmux a || tmux new -s work) keeps a long job alive on the node so a dropped connection never kills it; reconnect and run tmux a to reattach."
  },
  {
    "stem": "A 140 GB model checkpoint you need available on every machine belongs in:",
    "options": [
      "Email",
      "Your per-machine home directory",
      "The auto-mounted OneDrive folder (~/OneDrive)",
      "Git"
    ],
    "answer": 2,
    "explain": "~/OneDrive (set up once with capsule auth storage) auto-mounts on every machine you connect to, so a large shared checkpoint lives there. A home directory is per-machine and not visible elsewhere; Git and email are wrong for large binaries."
  },
  {
    "stem": "Watching a run's output live with <code>capsule exec &lt;tag&gt; \"./run.sh\"</code> beats scraping a log after the fact because:",
    "options": [
      "You see output as it streams back and can abort early on an obvious failure",
      "Faster GPU",
      "No reason",
      "Required by SOC2"
    ],
    "answer": 0,
    "explain": "capsule exec runs the command and returns its output to your terminal as it comes back, so you can catch a typo'd config in 30 seconds and Ctrl-C: saving GPU-hours instead of discovering the failure in a log after a 4-hour run finished."
  },
  {
    "stem": "The documented daily file workflow for a benchmark run is roughly:",
    "options": [
      "Email files to yourself",
      "capsule list --filter → capsule scp upload config → capsule exec \"./run.sh\" → capsule scp download report → capsule session end",
      "Reboot the machine",
      "Use git only"
    ],
    "answer": 1,
    "explain": "Find a machine with capsule list --filter, push the config with capsule scp upload, run it with capsule exec (watch stdout live), pull results with capsule scp download, then close the tunnel with capsule session end. All five are real USAGE.md commands."
  },
  {
    "stem": "<code>capsule term</code> (SshRTC) hangs forever on connect; a likely cause is:",
    "options": [
      "A restrictive network/proxy is blocking the WebRTC negotiation",
      "Capsule bug",
      "Disk full",
      "Wrong env"
    ],
    "answer": 0,
    "explain": "SshRTC negotiates a WebRTC peer connection, which hostile networks or proxies can block. Recovery: capsule session endall, retry, then fall back to --direct."
  },
  {
    "stem": "Your connection drops mid-session, but your long-running benchmark is inside tmux. It is:",
    "options": [
      "Definitely lost",
      "Likely still running on the remote; reconnect and reattach with <code>tmux a</code>",
      "Sent to email",
      "Migrated automatically"
    ],
    "answer": 1,
    "explain": "tmux keeps the process alive on the remote machine across a dropped connection, as long as the process itself wasn't killed. Reconnect with capsule term and run tmux a to reattach."
  },
  {
    "stem": "After a Capsule session ends, VS Code Remote-SSH starts throwing config errors. The known-quirks fix is:",
    "options": [
      "Reinstall the Remote-SSH extension",
      "Run capsule auth login again",
      "Clear the macOS Keychain",
      "Remove the stale <code>capsule-&lt;uniqueId&gt;</code> blocks from ~/.ssh/config"
    ],
    "answer": 3,
    "explain": "Old sessions leave stale capsule-<uniqueId> blocks in ~/.ssh/config, and VS Code Remote-SSH picks up those entries and fails. Remove the blocks manually; USAGE.md gives the same advice when switching between --direct and SshRTC connections."
  },
  {
    "stem": "A good Capsule bug report contains at minimum how many required fields, and which set?",
    "options": [
      "A complaint",
      "Just a screenshot",
      "The word <code>bug</code>",
      "Six fields: capsule --version, env show, config customer show, the exact failing command, the timestamp, and the machine's unique ID"
    ],
    "answer": 3,
    "explain": "The bug-report rubric has exactly 6 required fields: capsule --version, capsule env show, capsule config customer show, the exact failing command (with full output), the timestamp, and the machine's unique ID (from capsule list --all, not the display name). Missing any one gets the report sent back."
  },
  {
    "stem": "By Friday of Week 8 you can draw:",
    "options": [
      "Nothing",
      "Capsule's connection model (SshRTC vs Direct SSH) and env × customer routing, mapped to your Week 1–7 concepts",
      "Only NVIDIA chips",
      "A Kubernetes diagram"
    ],
    "answer": 1,
    "explain": "Goal of the week - operational fluency: the two connection paths, environment/customer routing, and the connect verbs, mapped onto earlier concepts."
  },
  {
    "stem": "To run a single command like <code>nvidia-smi</code> on a remote machine and get its output back WITHOUT opening an interactive shell, use:",
    "options": [
      "capsule term <tag>",
      "capsule stream <tag>",
      "capsule exec <tag> \"nvidia-smi\"",
      "capsule ssh <tag> --options \"-L 8080:localhost:8080\""
    ],
    "answer": 2,
    "explain": "capsule exec <tag> \"<command>\" runs one command on the remote, returns its output, then exits: ideal for scripted checks. capsule term opens a full interactive shell, capsule stream opens a WebRTC desktop, and the ssh --options form is for port-forwarding."
  },
  {
    "stem": "You launched a vLLM server on the node's port 8000 and want to reach it from your laptop. Which command sets up the tunnel?",
    "options": [
      "capsule port-forward <tag> 8000",
      "capsule tunnel open --to localhost:8000",
      "capsule stream <tag> --app vllm",
      "capsule ssh <tag> --options \"-L 8000:localhost:8000\""
    ],
    "answer": 3,
    "explain": "Port-forwarding rides on a direct SSH connection: capsule ssh <tag> --options \"-L 8000:localhost:8000\" makes the node's 8000 reachable at your local 8000. There is no capsule port-forward or capsule tunnel command."
  },
  {
    "stem": "You write benchmark output to <code>/tmp</code> on a node, disconnect, then reconnect later. What likely happened to it?",
    "options": [
      "/tmp is ephemeral; it may be gone after a restart/cleanup; keep results in $HOME or ~/OneDrive",
      "It synced to every other machine automatically",
      "It moved to ~/OneDrive automatically",
      "Nothing persists; $HOME is also wiped every session"
    ],
    "answer": 0,
    "explain": "/tmp is ephemeral and disappears on restart/cleanup. $HOME survives a reconnect but is node-local (not visible on other machines). Only ~/OneDrive follows you across machines, so anything you want to keep or reuse elsewhere goes there."
  },
  {
    "stem": "Which two commands open a remote IDE attached to the machine over Remote-SSH?",
    "options": [
      "capsule term and capsule ssh",
      "capsule exec and capsule stream",
      "capsule code (VS Code) and capsule cursor (Cursor)",
      "capsule env and capsule session"
    ],
    "answer": 2,
    "explain": "capsule code opens VS Code and capsule cursor opens Cursor, each with Remote-SSH attached to the machine. Both default to the SshRTC data channel; add --direct if you need --repo functionality."
  },
  {
    "stem": "How does <code>capsule scp upload</code> differ from the <code>~/OneDrive</code> mount?",
    "options": [
      "scp upload is a one-off copy to one machine's local disk; ~/OneDrive auto-mounts the SAME folder on every machine you connect to",
      "They are identical; both just copy files",
      "scp upload is only for small files; ~/OneDrive only for large ones",
      "Both push to a cluster-wide /shared/ pool via capsule storage put"
    ],
    "answer": 0,
    "explain": "capsule scp upload <tag> <src> <dest> is a one-off transfer whose copy lives only on that one machine. ~/OneDrive is your cloud-synced OxCapsule folder that auto-mounts at the same path everywhere after a one-time capsule auth storage. There is no capsule storage put or /shared/ pool in Capsule."
  },
  {
    "stem": "Before <code>~/OneDrive</code> will auto-mount on your sessions, the one-time step required is:",
    "options": [
      "Create a pool with capsule storage init",
      "capsule config files add OneDrive",
      "Run capsule auth storage and complete the OneDrive consent flow",
      "Nothing: OneDrive is always mounted by default"
    ],
    "answer": 2,
    "explain": "capsule auth storage runs the OneDrive OAuth/consent flow once and writes rclone.conf; after that your OxCapsule folder auto-mounts at ~/OneDrive on every term/code/cursor/stream session. There is no capsule storage init and no /shared/ pool."
  },
  {
    "stem": "You want your <code>.gitconfig</code> copied to the remote home directory automatically on every connect. The mechanism is:",
    "options": [
      "File passthrough: capsule config files add .gitconfig ~/.gitconfig",
      "capsule scp upload it by hand on every connect",
      "capsule storage put ~/.gitconfig /shared/dotfiles/",
      "Put it in a cluster-wide /shared/ pool"
    ],
    "answer": 0,
    "explain": "File passthrough handles small dotfiles: register them with capsule config files add (manage with config files list/remove); mappings live in config-files.json and are copied to the remote home on every term/code connect. There is no capsule storage put or /shared/ pool."
  },
  {
    "stem": "What does <code>capsule stream</code> do, and what is its platform limitation?",
    "options": [
      "Streams a command's stdout to your terminal; Linux only",
      "Opens a hardware-encoded WebRTC pixel stream of the remote desktop (or one app with --app); Windows and Mac only",
      "Uploads files continuously; available on all platforms",
      "Streams benchmark logs to the dashboard; NVIDIA machines only"
    ],
    "answer": 1,
    "explain": "capsule stream opens a hardware-encoded WebRTC pixel stream of the remote desktop (or a single app with --app) for GUI work like ComfyUI or Blender. Per USAGE.md it is available only on Windows and Mac and needs a machine that can pixel stream. It is NOT stdout streaming; that's capsule exec."
  },
  {
    "stem": "During an open 1080p stream, <code>nvidia-smi</code> shows encoder activity. Why doesn't this meaningfully slow a training job on the same GPU?",
    "options": [
      "nvidia-smi misreports streaming utilization",
      "NVENC is dedicated encoder silicon, separate from the CUDA / Tensor compute cores",
      "Streaming auto-throttles to 0% whenever compute is busy",
      "The stream runs on the CPU, not the GPU"
    ],
    "answer": 1,
    "explain": "Modern NVIDIA GPUs have a dedicated NVENC hardware encoder separate from the CUDA and Tensor cores. Encoder activity appears in nvidia-smi but does not consume the compute resources your training/inference uses; even a 1080p/60fps stream costs a running job <1% throughput."
  },
  {
    "stem": "For which task should you reach for <code>capsule stream</code> rather than <code>capsule term</code>/<code>exec</code>?",
    "options": [
      "Running an unattended overnight benchmark and collecting the loss curve",
      "Pulling a report.json back to your laptop",
      "Executing a one-off nvidia-smi check",
      "Interactively using ComfyUI with visual feedback on the remote GPU"
    ],
    "answer": 3,
    "explain": "The decision key: does the task require a human to see and interact with a GUI? ComfyUI with visual feedback → yes → stream. Unattended benchmarks, file transfers, and one-off CLI checks are all text/CLI work → capsule term or capsule exec, which are lower overhead and more reliable."
  },
  {
    "stem": "Inside <code>capsule docker &lt;tag&gt;</code>, <code>nvidia-smi</code> reports no NVIDIA devices. How do you get GPU access in the container?",
    "options": [
      "GPU access is impossible from a Capsule container",
      "Run capsule auth login first",
      "Relaunch with capsule docker <tag> -- --gpus all",
      "Add --turn to the command"
    ],
    "answer": 2,
    "explain": "By default capsule docker gives an Ubuntu container with no GPU access. Relaunch with capsule docker <tag> -- --gpus all; the -- passes the --gpus all Docker flag through the Capsule CLI to the container runtime, and nvidia-smi then shows the GPU."
  },
  {
    "stem": "Capsule streaming connects peer-to-peer by default. When does it fall back to a TURN relay, and what's the tradeoff?",
    "options": [
      "When direct P2P is blocked (corporate firewall / symmetric NAT): the relay guarantees connectivity but adds latency (~100–200ms vs ~20–50ms local)",
      "Never: Capsule streaming is always peer-to-peer",
      "When the GPU is busy, it relays to save compute",
      "On every connection, purely to encrypt the stream"
    ],
    "answer": 0,
    "explain": "WebRTC tries direct P2P first (best latency). If a firewall or symmetric NAT blocks the direct path, it falls back to a TURN relay, which guarantees connectivity but adds a relay hop. You can force relay with --turn for testing or force direct with --no-turn when diagnosing input lag."
  },
  {
    "stem": "The Week 8 triage decision tree runs, in order:",
    "options": [
      "reboot → reinstall → contact support → escalate",
      "read logs → check GPU → check storage → check network",
      "check hardware → check drivers → check CUDA → retry",
      "capsule status → env show + config customer show → session endall → --direct + collect logs"
    ],
    "answer": 3,
    "explain": "The tree: (1) capsule status verifies auth/identity/token; (2) capsule env show + capsule config customer show confirm the right environment and customer; (3) capsule session endall clears stale SshRTC tunnel state before you retry; (4) if it still fails, retry with --direct and capture the command, output, version, env, and customer to escalate."
  },
  {
    "stem": "<code>capsule session endall</code> does NOT affect:",
    "options": [
      "The active SshRTC tunnels open on your machine",
      "Your local port and tunnel state",
      "Processes and files on the remote machine, and other users' sessions",
      "The list of tunnels shown by capsule session list"
    ],
    "answer": 2,
    "explain": "capsule session endall closes every active SshRTC data-channel tunnel on YOUR machine at once. It does not kill remote processes, delete remote files, or disturb other users' sessions: which is why it's safe as a first diagnostic step; you won't lose remote work (a job inside tmux keeps running)."
  },
  {
    "stem": "<code>capsule list</code> suddenly shows completely different machines than yesterday. The two commands to check FIRST are:",
    "options": [
      "capsule status and capsule auth login",
      "capsule --version and capsule update",
      "capsule env show and capsule config customer show",
      "capsule session endall and capsule list --json"
    ],
    "answer": 2,
    "explain": "Known-quirks row 2: 'capsule list shows wrong machines' is fixed by checking capsule env show and capsule config customer show; one is pointed at the wrong environment or customer fleet. Both settings persist across sessions, so a single accidental switch explains why 'everything stopped working.'"
  },
  {
    "stem": "On Windows PowerShell, <code>capsule list --filter</code> with an unquoted <code>&gt;</code> (e.g. vram&gt;=24) fails or silently creates a file. The fix is:",
    "options": [
      "Run it with sudo",
      "Use capsule (not the cap shortcut) and quote the whole filter: capsule list --filter \"vram>=24\"",
      "Switch to the demo environment first",
      "Add the --direct flag"
    ],
    "answer": 1,
    "explain": "PowerShell interprets an unquoted '>' as output redirection, and the cap shortener compounds the problem. Use the full capsule command and quote the entire filter argument so the shell passes it through instead of creating a file."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Back to today's lesson__

    [Day 40 · Consolidation](index.md)

-   __Back to the week__

    [Week 8 - Capsule: Connections &amp; Operations overview](../index.md)

-   __Continue the curriculum__

    [Day 41 · Benchmarking](../../week-09/module-1/index.md)

</div>
