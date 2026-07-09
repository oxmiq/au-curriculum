---
drift: |
  Authored as a combined "Architecture + Installation" day (former wk8 day 36). New graph
  splits this into two consecutive modules: week-07/module-2 (Foundations) and
  week-07/module-3 (Installation). For now this lesson covers BOTH concepts in a single
  page; module-3 is a redirect stub pointing to the install sections below. Future
  authoring should extract the install flow into its own page.
---

# Day 33 · Capsule Foundations & Architecture

> **Concept of the day:** **Capsule** = orchestration platform for on-prem GPU fleets. CLI on your laptop talks to a **control plane**; the control plane manages **environments** (clusters of nodes); each node runs an **agent** that exposes machines. Install once, configure once, operate every day.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#day-36-capsule-architecture-installation">Capsule Power-User Pre-Lecture Reading — Day 36 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-1-capsule-foundations">Capsule Lab Guide</a> Modules 1 + 2.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 7 — Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <span>Day 33 · Capsule Foundations</span>
    {status:week-07/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | What you do |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: The Three Layers |
| Part 3 | Core Concepts: Installation Flow |
| Part 4 | Deep Dive: What Each Layer Stores |
| Part 5 | Hands-On: Install & Verify |
| Part 6 | Hands-On: Architecture Diagram |
| Part 7 | Wrap-up & Connection |

## Part 1 — Pre-Reading Review

> Read the Capsule Power User Lab Guide **Modules 1 + 2** before this lesson. Use this Part to consolidate what you read.

### Exercise: Self-Check

Answer these before you continue — they preview where you'll be uncertain:

1. Name the three layers of the Capsule architecture.
2. What's the difference between the **CLI**, the **control plane**, and the **node agent**?
3. Where does authentication live?
4. What does an **environment** contain?
5. After install, what's the first command you run to verify it works?

If you hesitated on any of these, flag it — the next three Parts will close those gaps.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m2-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the three layers of the Capsule architecture?",
    "options": [
      "Input, Processing, Output",
      "CLI, control plane, node agent",
      "Model, Tools, API",
      "Training, Testing, Deployment"
    ],
    "answer": 1,
    "explain": "The three layers of Capsule architecture are: (1) CLI — the command-line interface on your laptop, (2) control plane — the orchestration service that manages environments, (3) node agent — the software running on each GPU node that exposes machines."
  },
  {
    "stem": "What is the Capsule CLI?",
    "options": [
      "A web interface",
      "The command-line interface you run on your laptop to interact with Capsule",
      "A model training tool",
      "A type of GPU"
    ],
    "answer": 1,
    "explain": "The Capsule CLI is the command-line interface you run on your laptop. It's how you interact with Capsule — running commands, deploying models, managing environments. You type commands locally and they go to the control plane."
  },
  {
    "stem": "What is the Capsule control plane?",
    "options": [
      "A physical server",
      "The orchestration service that manages environments and coordinates node agents",
      "A type of LLM",
      "A monitoring dashboard"
    ],
    "answer": 1,
    "explain": "The control plane is the orchestration service that manages environments (clusters of nodes) and coordinates node agents. It's the central service that your CLI talks to over HTTPS."
  },
  {
    "stem": "What is a node agent in Capsule?",
    "options": [
      "A human operator",
      "Software running on each GPU node that exposes machines to the fleet",
      "A type of virtual machine",
      "A network switch"
    ],
    "answer": 1,
    "explain": "A node agent is software running on each GPU node that exposes machines to the fleet. It handles the actual model serving, execution, and reporting back to the control plane."
  },
  {
    "stem": "Where does authentication live in Capsule?",
    "options": [
      "In the node agent",
      "In the control plane (auth token-based)",
      "In the CLI only",
      "Authentication is not required"
    ],
    "answer": 1,
    "explain": "Authentication lives in the control plane. The CLI authenticates with an auth token when talking to the control plane. This provides secure access to the Capsule fleet."
  },
  {
    "stem": "What does an environment contain in Capsule?",
    "options": [
      "Only the CLI",
      "A cluster of nodes (GPU machines) managed together",
      "Just the control plane",
      "Only the user credentials"
    ],
    "answer": 1,
    "explain": "An environment is a cluster of nodes (GPU machines) managed together. It's a logical grouping of machines that you can deploy models to. You configure an environment once and deploy to all nodes in it."
  },
  {
    "stem": "After installing Capsule, what's the first command you run to verify it works?",
    "options": [
      "capsule deploy",
      "capsule status",
      "capsule init",
      "capsule login"
    ],
    "answer": 1,
    "explain": "After installing Capsule, the first command you run is 'capsule status' to verify the installation works and check the connection to the control plane."
  },
  {
    "stem": "What is the relationship between Capsule and on-prem GPU fleets?",
    "options": [
      "Capsule is a cloud service",
      "Capsule is an orchestration platform for on-prem GPU fleets",
      "Capsule is a model training framework",
      "Capsule is a type of GPU"
    ],
    "answer": 1,
    "explain": "Capsule is an orchestration platform for on-prem GPU fleets. It lets you manage your own GPU machines (on-premises or in your own cloud VPC) rather than using managed services. Install once, configure once, operate every day."
  }
]
</script>
</div>

## Part 2 — Core Concepts: The Three Layers

### Reading — Why this matters

This is Phase 3's foundation. Every benchmark in Week 9, every agent in Week 7's project — they all land on Capsule machines. If you don't have a clean mental model of the architecture, every "why won't this connect?" debug session will burn 30 minutes instead of 30 seconds.

### Reading — The three layers

```
┌───────────────────────────────────────┐
│ 1. Capsule CLI (your laptop)          │ ← you type here
└──────────────┬────────────────────────┘
               │ HTTPS + auth token
               ▼
┌───────────────────────────────────────┐
│ 2. Control plane (cloud-hosted)       │ ← state, scheduling, identity
│    - environments / inventory          │
│    - user identity                     │
│    - scheduling / leases               │
└──────────────┬────────────────────────┘
               │ secure channel
               ▼
┌───────────────────────────────────────┐
│ 3. Node agent (on each GPU machine)   │ ← actually runs your workload
│    - tunnel / SSH                      │
│    - file transfer                     │
│    - GPU access                        │
└───────────────────────────────────────┘
```

**Key insight:** you never SSH directly to a node. The CLI brokers everything through the control plane, which authenticates you, then opens a session via the node agent. This gives you identity, audit, and bookkeeping for free.

### Reading — Why this design

| Goal | Mechanism |
|---|---|
| Identity-aware access | CLI → control plane → node, never direct |
| Multi-tenant safety | Per-user / per-team environments + leases |
| Heterogeneous fleet | Environments group by hardware; users select by capability |
| Auditable operation | Every CLI action logs through control plane |

### Reading — What an environment contains

An **environment** is a logical grouping of nodes — usually one per geographic site or per hardware class:

- A list of nodes (machines).
- Per-node metadata: GPU type, model, status, leased-by.
- Per-environment policies: who can connect, what tools are pre-installed.
- A shared storage pool (covered Day 39).

Examples: `production`, `development`, `production-fre`, `production-tenstorrent` (mirroring the `capsule-ansible` inventory naming).

## Part 3 — Core Concepts: Installation Flow

### Reading — Installation flow (macOS + Linux)

1. Install the CLI: `brew install capsule` (or the equivalent for your platform).
2. Authenticate: `capsule login` — opens a browser, returns a token.
3. Verify: `capsule whoami` — confirms identity.
4. Configure default env: `capsule env use <env-name>`.

That's the happy path. On a fresh laptop it's ~5 minutes.

### Reading — Common install gotchas (Module 1 quirks)

| Symptom | Cause |
|---|---|
| `capsule: command not found` | PATH doesn't include install dir; restart shell |
| `capsule login` browser doesn't open | Headless terminal; use `--device-code` flow |
| `whoami` says unauthorized after login | Clock skew between laptop and control plane; sync NTP |
| SSH to a node hangs after `capsule connect` | Corporate proxy mangling websockets; need `HTTPS_PROXY` |

These are the four most-asked support questions. Memorize them.

## Part 4 — Deep Dive: What Each Layer Stores

### Reading — What a Capsule "install" actually does

| Component | Where it lives | What it stores |
|---|---|---|
| Binary | `/usr/local/bin/capsule` (or equivalent) | the CLI itself |
| Config dir | `~/.capsule/` | tokens, default env, cached env metadata |
| Token | `~/.capsule/credentials` | refresh + access tokens, encrypted at rest on macOS Keychain when available |

### Exercise: Trace the auth path

Draw the flow for `capsule connect nv-h100-04-1`:

1. The CLI reads your token from `~/.capsule/credentials`.
2. It calls the control plane over HTTPS with that token.
3. The control plane checks: is this user authorized to connect to this node?
4. The control plane tells the node agent to open a session.
5. The CLI receives the tunnel info and proxies your shell.

**Question:** at which step would a clock-skew problem manifest? At which step would a corporate proxy problem manifest? Write your answers before continuing.

## Part 5 — Hands-On: Install & Verify

### Exercise: Install Capsule on your laptop

 Install Capsule on your laptop. Verify with `capsule version` and `capsule whoami`.

Expected output:

```
$ capsule version
capsule v2.x.x ...
$ capsule whoami
user: alice@oxmiq.com
env: development
```

If you hit one of the four gotchas from Part 3, resolve it now. Pair up if needed.

### Exercise: Configure your default environment

 Run `capsule env list`. Identify which environments you have access to. Pick one as default with `capsule env use <env-name>`.

## Part 6 — Hands-On: Architecture Diagram

### Exercise: Draw from memory

 Draw the 3-layer architecture on paper — no peeking. Label each layer with:

- Where it runs
- What it stores
- Who talks to it

Compare your drawing to the diagram in Part 2. Note every discrepancy.

### Exercise: Explore the Cheatsheet

 Read the Cheatsheet's "first 10 minutes" section. Familiarize with the command surface.

## Part 7 — Wrap-up & Connection

**Before you finish, check each item:**

- [ ] I can run `capsule whoami` successfully.
- [ ] I can name the three layers of the Capsule architecture (CLI, control plane, node agent).
- [ ] I know what `~/.capsule/` stores and why the token is there.
- [ ] I know what an "environment" is and which one I'm in.
- [ ] I've resolved any install gotchas I encountered.

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 33 · Capsule Foundations &amp; Architecture">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the three layers of Capsule's architecture?",
    "options": [
      "Frontend, backend, database",
      "CLI (client), control plane (management), and node agent (machine-side)",
      "Authentication, orchestration, and execution",
      "User interface, API gateway, and compute cluster"
    ],
    "answer": 1,
    "explain": "Capsule has three layers: the CLI (your local tool for sending commands), the control plane (cloud service that authenticates, schedules, and manages fleet state), and the node agent (runs on each GPU machine, executes commands and reports status). Understanding this layering helps diagnose where failures occur."
  },
  {
    "stem": "What does `~/.capsule/` store and why is the token kept there?",
    "options": [
      "Model weights — because they need to be accessible from the CLI",
      "Auth token, config, and environment settings — the token is stored locally so you don't re-authenticate on every command",
      "Log files — so you can review past commands",
      "GPU firmware — to enable local hardware monitoring"
    ],
    "answer": 1,
    "explain": "`~/.capsule/` stores: the auth token (so you stay authenticated between CLI calls), your active config (environment, customer), and CLI state. The token must be kept confidential — it grants access to lease machines and run commands on behalf of your account."
  },
  {
    "stem": "What is an 'environment' in Capsule?",
    "options": [
      "A Python virtualenv for running model code",
      "A logical namespace that groups a set of machines under a customer's access scope, defining which fleet you can see and operate",
      "A GPU driver version that determines which models are compatible",
      "A container image used as the base for all workloads"
    ],
    "answer": 1,
    "explain": "An environment in Capsule is a logical grouping of machines under a specific customer or deployment context. Environments determine what fleet you can list and lease. `capsule env list` shows available environments; `capsule config customer set` switches which customer's environment you're operating in."
  },
  {
    "stem": "What does `capsule whoami` tell you?",
    "options": [
      "The current operating system user running the Capsule process",
      "Your authenticated identity (user email / identity provider) and the active environment/customer config",
      "The version of the Capsule CLI installed",
      "The GPU hardware specification of the machine you're connected to"
    ],
    "answer": 1,
    "explain": "`capsule whoami` verifies that your auth token is valid and shows your identity as seen by the control plane. It's the first diagnostic command after install or when experiencing auth issues. If it fails, authentication is broken."
  },
  {
    "stem": "What role does the control plane play in Capsule's architecture?",
    "options": [
      "It runs the model inference workloads",
      "It authenticates requests, manages fleet state and leases, routes commands to node agents, and enforces access control",
      "It stores model weights for download",
      "It provides the CLI interface to the user"
    ],
    "answer": 1,
    "explain": "The control plane is the central brain: it authenticates your CLI token, maintains the inventory of machines and their states (available, leased, unhealthy), routes your commands to the correct node agent, and enforces multi-tenant access control. It's the 'management layer' between your CLI and the physical machines."
  }
]
</script>
</div>

### Connect forward

Tomorrow: **environments and fleet discovery** — how to find what's available, what to ask for, and how to read the inventory.

### Pre-read for tomorrow (Day 37 · Environments & Fleet Discovery)

- **Resource:** <a href="../../../readings/capsule/#day-37-environments-fleet-discovery">Capsule Power-User Pre-Lecture Reading — Day 37 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-3-environments-customers-and-why-your-fleet-looks-wrong">Capsule Lab Guide</a> Module 3.
- **Reflection questions:**
  1. How do you list available machines in an environment?
  2. What fields tell you a machine is *available* vs *leased*?
  3. How is hardware diversity (NVIDIA H100, NVIDIA T4, Tenstorrent, Apple Silicon) surfaced in the inventory?

## Stuck?

Ask **oxtutor** — describe what you tried and what happened.
