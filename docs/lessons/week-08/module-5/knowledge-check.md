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
    "stem": "The three layers of Capsule architecture are:",
    "options": [
      "Frontend / Backend / DB",
      "CLI / Control plane / Node agent",
      "CPU / GPU / NIC",
      "Compile / Link / Run"
    ],
    "answer": 1,
    "explain": "CLI → control plane → node agent. Brokered, identity-aware."
  },
  {
    "stem": "After installing the CLI, the first command to verify install + identity is:",
    "options": [
      "capsule connect",
      "capsule whoami",
      "capsule node list",
      "ssh"
    ],
    "answer": 1,
    "explain": "<code>whoami</code> confirms the token works against the control plane."
  },
  {
    "stem": "An environment is best described as:",
    "options": [
      "A single GPU",
      "A logical grouping of nodes with policy + shared storage",
      "Your terminal",
      "A Kubernetes cluster"
    ],
    "answer": 1,
    "explain": "Per-site or per-class fleet of nodes."
  },
  {
    "stem": "Capability filtering (e.g. <code>--gpu h100 --min-gpus 8</code>) is preferred over name-based filtering because:",
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
    "stem": "A lease is:",
    "options": [
      "Permanent ownership",
      "Time-bounded reservation of a node",
      "A connection",
      "An environment"
    ],
    "answer": 1,
    "explain": "Renewable, releaseable, audited with a reason field."
  },
  {
    "stem": "<code>capsule connect</code> differs from raw SSH primarily by:",
    "options": [
      "Identity from CLI auth, brokered, audited, no key management",
      "Faster bytes",
      "Better colors",
      "Less secure"
    ],
    "answer": 0,
    "explain": "All four properties; key management overhead disappears."
  },
  {
    "stem": "First command after <code>capsule connect <node></code> should be:",
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
    "stem": "A 140 GB model checkpoint belongs in:",
    "options": [
      "Email",
      "Your home dir on the node",
      "Shared storage pool",
      "Git"
    ],
    "answer": 2,
    "explain": "Home is small + per-node; shared is large + visible to all nodes."
  },
  {
    "stem": "Streaming output (<code>capsule run --stream</code>) beats post-hoc log scraping because:",
    "options": [
      "You see live output and can abort early on obvious failures",
      "Faster GPU",
      "No reason",
      "Required by SOC2"
    ],
    "answer": 0,
    "explain": "Save GPU-hours by catching typo'd configs in 30 seconds."
  },
  {
    "stem": "Daily file workflow for a benchmark run is roughly:",
    "options": [
      "Email files to yourself",
      "lease → cp config → run --stream → storage get report → release",
      "Reboot node",
      "Use git only"
    ],
    "answer": 1,
    "explain": "Lease, push small config, stream the run, pull report, release."
  },
  {
    "stem": "<code>capsule connect</code> hangs forever — most likely cause:",
    "options": [
      "Capsule bug",
      "Corporate proxy mangling websockets; set HTTPS_PROXY",
      "Disk full",
      "Wrong env"
    ],
    "answer": 1,
    "explain": "Top install/connect quirk (Module 10)."
  },
  {
    "stem": "Mid-session your node goes <code>unhealthy</code> and connection drops. Your long-running benchmark in tmux is:",
    "options": [
      "Definitely lost",
      "Likely still running once the agent recovers; reattach with <code>tmux a</code>",
      "Sent to email",
      "Migrated automatically"
    ],
    "answer": 1,
    "explain": "Tmux survives transient agent restarts as long as the process wasn't killed."
  },
  {
    "stem": "Two users see the same node leased to both of them. Correct action:",
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
    "stem": "A good bug report contains at minimum:",
    "options": [
      "A complaint",
      "Reproduction steps, expected vs actual, logs, environment, hypothesis",
      "Just a screenshot",
      "The word <code>bug</code>"
    ],
    "answer": 1,
    "explain": "The five mandatory fields — anything less wastes the maintainer's time."
  },
  {
    "stem": "By Friday of Week 8 you can draw:",
    "options": [
      "Nothing",
      "The 3-layer Capsule architecture and map each layer to your Week 1–7 concepts",
      "Only NVIDIA chips",
      "A Kubernetes diagram"
    ],
    "answer": 1,
    "explain": "Goal of the week — operational fluency + architectural mental model."
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
