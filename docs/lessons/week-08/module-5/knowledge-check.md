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
  {"stem": "Capsule offers two connection paths to a remote machine. They are:", "options": ["Frontend / Backend / DB", "SshRTC (WebRTC data channel, default) and Direct SSH (--direct)", "CPU / GPU / NIC", "Compile / Link / Run"]},
  {"stem": "In the triage tree, the command that confirms your auth is valid and shows your identity + token expiry is:", "options": ["capsule connect", "capsule status", "capsule node list", "ssh"]},
  {"stem": "In Capsule, an 'environment' (prod, public, dev, demo) is best described as:", "options": ["A single GPU", "Your terminal", "A Kubernetes cluster", "A backend deployment that sets the Azure B2C tenant and API endpoint"]},
  {"stem": "Capability filtering (e.g. <code>capsule list --filter \"vendor=nvidia,vram>=24\"</code>) is preferred over name-based filtering because:", "options": ["Faster typing", "It survives hardware churn and states the real requirement explicitly", "Required by Capsule", "Naming is broken"]},
  {"stem": "You have several SshRTC tunnels open and want to close just ONE without disturbing the others. Which command targets a single tunnel?", "options": ["capsule session endall", "capsule cleanup --all", "capsule session end (by --unique-id, --port, or --session-id)", "capsule session kill Noble"]},
  {"stem": "<code>capsule term</code> (SshRTC) differs from raw SSH primarily by:", "options": ["Identity comes from your CLI auth; the connection is brokered over WebRTC with no manual key management", "Faster bytes", "Better colors", "Less secure"]},
  {"stem": "The first thing to run after you open a remote shell with <code>capsule term &lt;config-tag&gt;</code> should be:", "options": ["rm -rf /", "nvidia-smi", "tmux a || tmux new -s work", "sudo apt update"]},
  {"stem": "A 140 GB model checkpoint you need available on every machine belongs in:", "options": ["Email", "Your per-machine home directory", "The auto-mounted OneDrive folder (~/OneDrive)", "Git"]},
  {"stem": "Watching a run's output live with <code>capsule exec &lt;tag&gt; \"./run.sh\"</code> beats scraping a log after the fact because:", "options": ["You see output as it streams back and can abort early on an obvious failure", "Faster GPU", "No reason", "Required by SOC2"]},
  {"stem": "The documented daily file workflow for a benchmark run is roughly:", "options": ["Email files to yourself", "capsule list --filter → capsule scp upload config → capsule exec \"./run.sh\" → capsule scp download report → capsule session end", "Reboot the machine", "Use git only"]},
  {"stem": "<code>capsule term</code> (SshRTC) hangs forever on connect; a likely cause is:", "options": ["A restrictive network/proxy is blocking the WebRTC negotiation", "Capsule bug", "Disk full", "Wrong env"]},
  {"stem": "Your connection drops mid-session, but your long-running benchmark is inside tmux. It is:", "options": ["Definitely lost", "Likely still running on the remote; reconnect and reattach with <code>tmux a</code>", "Sent to email", "Migrated automatically"]},
  {"stem": "After a Capsule session ends, VS Code Remote-SSH starts throwing config errors. The known-quirks fix is:", "options": ["Reinstall the Remote-SSH extension", "Run capsule auth login again", "Clear the macOS Keychain", "Remove the stale <code>capsule-&lt;uniqueId&gt;</code> blocks from ~/.ssh/config"]},
  {"stem": "A good Capsule bug report contains at minimum how many required fields, and which set?", "options": ["A complaint", "Just a screenshot", "The word <code>bug</code>", "Six fields: capsule --version, env show, config customer show, the exact failing command, the timestamp, and the machine's unique ID"]},
  {"stem": "By Friday of Week 8 you can draw:", "options": ["Nothing", "Capsule's connection model (SshRTC vs Direct SSH) and env × customer routing, mapped to your Week 1–7 concepts", "Only NVIDIA chips", "A Kubernetes diagram"]},
  {"stem": "To run a single command like <code>nvidia-smi</code> on a remote machine and get its output back WITHOUT opening an interactive shell, use:", "options": ["capsule term <tag>", "capsule stream <tag>", "capsule exec <tag> \"nvidia-smi\"", "capsule ssh <tag> --options \"-L 8080:localhost:8080\""]},
  {"stem": "You launched a vLLM server on the node's port 8000 and want to reach it from your laptop. Which command sets up the tunnel?", "options": ["capsule port-forward <tag> 8000", "capsule tunnel open --to localhost:8000", "capsule stream <tag> --app vllm", "capsule ssh <tag> --options \"-L 8000:localhost:8000\""]},
  {"stem": "You write benchmark output to <code>/tmp</code> on a node, disconnect, then reconnect later. What likely happened to it?", "options": ["/tmp is ephemeral; it may be gone after a restart/cleanup; keep results in $HOME or ~/OneDrive", "It synced to every other machine automatically", "It moved to ~/OneDrive automatically", "Nothing persists; $HOME is also wiped every session"]},
  {"stem": "Which two commands open a remote IDE attached to the machine over Remote-SSH?", "options": ["capsule term and capsule ssh", "capsule exec and capsule stream", "capsule code (VS Code) and capsule cursor (Cursor)", "capsule env and capsule session"]},
  {"stem": "How does <code>capsule scp upload</code> differ from the <code>~/OneDrive</code> mount?", "options": ["scp upload is a one-off copy to one machine's local disk; ~/OneDrive auto-mounts the SAME folder on every machine you connect to", "They are identical; both just copy files", "scp upload is only for small files; ~/OneDrive only for large ones", "Both push to a cluster-wide /shared/ pool via capsule storage put"]},
  {"stem": "Before <code>~/OneDrive</code> will auto-mount on your sessions, the one-time step required is:", "options": ["Create a pool with capsule storage init", "capsule config files add OneDrive", "Run capsule auth storage and complete the OneDrive consent flow", "Nothing: OneDrive is always mounted by default"]},
  {"stem": "You want your <code>.gitconfig</code> copied to the remote home directory automatically on every connect. The mechanism is:", "options": ["File passthrough: capsule config files add .gitconfig ~/.gitconfig", "capsule scp upload it by hand on every connect", "capsule storage put ~/.gitconfig /shared/dotfiles/", "Put it in a cluster-wide /shared/ pool"]},
  {"stem": "What does <code>capsule stream</code> do, and what is its platform limitation?", "options": ["Streams a command's stdout to your terminal; Linux only", "Opens a hardware-encoded WebRTC pixel stream of the remote desktop (or one app with --app); Windows and Mac only", "Uploads files continuously; available on all platforms", "Streams benchmark logs to the dashboard; NVIDIA machines only"]},
  {"stem": "During an open 1080p stream, <code>nvidia-smi</code> shows encoder activity. Why doesn't this meaningfully slow a training job on the same GPU?", "options": ["nvidia-smi misreports streaming utilization", "NVENC is dedicated encoder silicon, separate from the CUDA / Tensor compute cores", "Streaming auto-throttles to 0% whenever compute is busy", "The stream runs on the CPU, not the GPU"]},
  {"stem": "For which task should you reach for <code>capsule stream</code> rather than <code>capsule term</code>/<code>exec</code>?", "options": ["Running an unattended overnight benchmark and collecting the loss curve", "Pulling a report.json back to your laptop", "Executing a one-off nvidia-smi check", "Interactively using ComfyUI with visual feedback on the remote GPU"]},
  {"stem": "Inside <code>capsule docker &lt;tag&gt;</code>, <code>nvidia-smi</code> reports no NVIDIA devices. How do you get GPU access in the container?", "options": ["GPU access is impossible from a Capsule container", "Run capsule auth login first", "Relaunch with capsule docker <tag> -- --gpus all", "Add --turn to the command"]},
  {"stem": "Capsule streaming connects peer-to-peer by default. When does it fall back to a TURN relay, and what's the tradeoff?", "options": ["When direct P2P is blocked (corporate firewall / symmetric NAT): the relay guarantees connectivity but adds latency (~100–200ms vs ~20–50ms local)", "Never: Capsule streaming is always peer-to-peer", "When the GPU is busy, it relays to save compute", "On every connection, purely to encrypt the stream"]},
  {"stem": "The Week 8 triage decision tree runs, in order:", "options": ["reboot → reinstall → contact support → escalate", "read logs → check GPU → check storage → check network", "check hardware → check drivers → check CUDA → retry", "capsule status → env show + config customer show → session endall → --direct + collect logs"]},
  {"stem": "<code>capsule session endall</code> does NOT affect:", "options": ["The active SshRTC tunnels open on your machine", "Your local port and tunnel state", "Processes and files on the remote machine, and other users' sessions", "The list of tunnels shown by capsule session list"]},
  {"stem": "<code>capsule list</code> suddenly shows completely different machines than yesterday. The two commands to check FIRST are:", "options": ["capsule status and capsule auth login", "capsule --version and capsule update", "capsule env show and capsule config customer show", "capsule session endall and capsule list --json"]},
  {"stem": "On Windows PowerShell, <code>capsule list --filter</code> with an unquoted <code>&gt;</code> (e.g. vram&gt;=24) fails or silently creates a file. The fix is:", "options": ["Run it with sudo", "Use capsule (not the cap shortcut) and quote the whole filter: capsule list --filter \"vram>=24\"", "Switch to the demo environment first", "Add the --direct flag"]}
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
