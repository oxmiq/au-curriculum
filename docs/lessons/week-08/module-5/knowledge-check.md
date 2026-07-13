<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../">Learn</a>
    <span class="sep">/</span>
    <a href="../../">Week 8 — Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <a href="../">Day 40 · Consolidation</a>
    <span class="sep">/</span>
    <span>Knowledge Check</span>
    {status:week-08/module-5}
  </div>
</div>

# Week 8 Knowledge Check

**Week 8 · Capsule Foundations & Operations.** 15 questions · aim for **strong (≥ 80%)**. This check is
formative — it never blocks you — but it's the week's bar. Answer all questions,
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
    "stem": "After installing the CLI, the command that confirms your install works and shows your identity + token expiry is:",
    "options": [
      "capsule connect",
      "capsule status",
      "capsule node list",
      "ssh"
    ],
    "answer": 1,
    "explain": "<code>capsule status</code> reports your user name, display name, and token expiry — the fastest confirmation that auth works. <code>capsule --version</code> confirms the binary is installed. (capsule connect and capsule node list are not real commands.)"
  },
  {
    "stem": "In Capsule, an 'environment' (prod, public, dev, demo) is best described as:",
    "options": [
      "A single GPU",
      "A backend deployment that sets the Azure B2C tenant and API endpoint",
      "Your terminal",
      "A Kubernetes cluster"
    ],
    "answer": 1,
    "explain": "An environment selects the backend deployment and its Azure B2C tenant/endpoint. The auth token is scoped per environment, so capsule env set is followed by a fresh capsule auth login. Set with capsule env set, inspect with capsule env show."
  },
  {
    "stem": "Capability filtering (e.g. <code>capsule list --filter \"vendor=nvidia,vram>=24\"</code>) is preferred over name-based filtering because:",
    "options": [
      "Faster typing",
      "Survives hardware churn and is explicit about real requirements",
      "Required by Capsule",
      "Naming is broken"
    ],
    "answer": 1,
    "explain": "Names change; capabilities are stable."
  },
  {
    "stem": "To bound how long a session can hold a machine, you use:",
    "options": [
      "Permanent ownership",
      "The --idle-timeout and --max-session-length flags",
      "A raw SSH keepalive",
      "An environment"
    ],
    "answer": 1,
    "explain": "Connection commands accept --idle-timeout and --max-session-length so an idle terminal does not pin a GPU. Inspect and close active tunnels with capsule session list / capsule session end."
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
    "explain": "capsule term uses your Capsule auth identity and tunnels SSH over a WebRTC data channel — no public port and no manual SSH key management (Capsule auto-generates and manages the keys). Raw SSH gives you none of that."
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
    "explain": "Survive network blips; never lose long runs."
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
    "stem": "Watching a run's output live (via <code>capsule exec</code> or <code>capsule schedule logs --tail</code>) beats scraping logs after the fact because:",
    "options": [
      "You see live output and can abort early on obvious failures",
      "Faster GPU",
      "No reason",
      "Required by SOC2"
    ],
    "answer": 0,
    "explain": "Live output lets you catch a typo'd config in 30 seconds and abort, saving GPU-hours instead of discovering the failure in a log after the run finished."
  },
  {
    "stem": "Daily file workflow for a benchmark run is roughly:",
    "options": [
      "Email files to yourself",
      "capsule list --filter → capsule scp upload config → capsule benchmark → capsule scp download report → capsule session end",
      "Reboot the machine",
      "Use git only"
    ],
    "answer": 1,
    "explain": "Find a machine with capsule list --filter, push the config with capsule scp upload, run capsule benchmark, pull results with capsule scp download, then close the tunnel with capsule session end."
  },
  {
    "stem": "<code>capsule term</code> (SshRTC) hangs forever on connect — a likely cause is:",
    "options": [
      "Capsule bug",
      "A restrictive network/proxy is blocking the WebRTC negotiation",
      "Disk full",
      "Wrong env"
    ],
    "answer": 1,
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
    "stem": "Two users are handed the same machine by the scheduler. Correct action:",
    "options": [
      "Ignore",
      "File a bug report — scheduler race",
      "Reboot the node",
      "Yell"
    ],
    "answer": 1,
    "explain": "Day 40: actionable bug with reproduction + logs."
  },
  {
    "stem": "A good Capsule bug report contains at minimum:",
    "options": [
      "A complaint",
      "capsule --version, env show, config customer show, the exact failing command, the timestamp, and the machine's unique ID",
      "Just a screenshot",
      "The word <code>bug</code>"
    ],
    "answer": 1,
    "explain": "The six things an Oxmiq engineer needs: capsule --version, capsule env show, capsule config customer show, the exact failing command, the timestamp, and the machine's unique ID (capsule list --all). Anything less wastes the maintainer's time."
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
    "explain": "Goal of the week — operational fluency: the two connection paths, environment/customer routing, and the connect/benchmark verbs, mapped onto earlier concepts."
  }
]
</script>
</div>

## What next

<div class="grid cards" markdown>

-   __Record your result__

    Use **Retake** and **Copy progress JSON** in the check above to log the attempt in `docs/progress/`.

-   __Back to today's lesson__

    [Day 40 · Consolidation](index.md)

-   __Back to the week__

    [Week 8 — Capsule: Connections &amp; Operations overview](../index.md)

-   __Continue the curriculum__

    [Day 41 · Benchmarking](../../week-09/module-1/index.md)

</div>
