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
> **Pre-reading:** Capsule Power User Lab Guide **Modules 1 + 2** (~35 min).

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
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-07/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | What you do | Time |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: The Three Layers | 25 min |
| Part 3 | Core Concepts: Installation Flow | 20 min |
| Part 4 | Deep Dive: What Each Layer Stores | 20 min |
| Part 5 | Hands-On: Install & Verify | 30 min |
| Part 6 | Hands-On: Architecture Diagram | 20 min |
| Part 7 | Wrap-up & Connection | 15 min |

## Part 1 — Pre-Reading Review · 15 min

> Read the Capsule Power User Lab Guide **Modules 1 + 2** (~35 min) before this lesson. Use this Part to consolidate what you read.

### Exercise: Self-Check

Answer these before you continue — they preview where you'll be uncertain:

1. Name the three layers of the Capsule architecture.
2. What's the difference between the **CLI**, the **control plane**, and the **node agent**?
3. Where does authentication live?
4. What does an **environment** contain?
5. After install, what's the first command you run to verify it works?

If you hesitated on any of these, flag it — the next three Parts will close those gaps.

## Part 2 — Core Concepts: The Three Layers · 25 min

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

## Part 3 — Core Concepts: Installation Flow · 20 min

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

## Part 4 — Deep Dive: What Each Layer Stores · 20 min

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

## Part 5 — Hands-On: Install & Verify · 30 min

### Exercise: Install Capsule on your laptop

(20 min) Install Capsule on your laptop. Verify with `capsule version` and `capsule whoami`.

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

(10 min) Run `capsule env list`. Identify which environments you have access to. Pick one as default with `capsule env use <env-name>`.

## Part 6 — Hands-On: Architecture Diagram · 20 min

### Exercise: Draw from memory

(15 min) Draw the 3-layer architecture on paper — no peeking. Label each layer with:

- Where it runs
- What it stores
- Who talks to it

Compare your drawing to the diagram in Part 2. Note every discrepancy.

### Exercise: Explore the Cheatsheet

(5 min) Read the Cheatsheet's "first 10 minutes" section. Familiarize with the command surface.

## Part 7 — Wrap-up & Connection · 15 min

**Before you finish, check each item:**

- [ ] I can run `capsule whoami` successfully.
- [ ] I can name the three layers of the Capsule architecture (CLI, control plane, node agent).
- [ ] I know what `~/.capsule/` stores and why the token is there.
- [ ] I know what an "environment" is and which one I'm in.
- [ ] I've resolved any install gotchas I encountered.

### Connect forward

Tomorrow: **environments and fleet discovery** — how to find what's available, what to ask for, and how to read the inventory.

### Pre-read for tomorrow (Day 37 · Environments & Fleet Discovery)

- **Resource:** Lab Guide **Module 3** (~15 min).
- **Reflection questions:**
  1. How do you list available machines in an environment?
  2. What fields tell you a machine is *available* vs *leased*?
  3. How is hardware diversity (NVIDIA H100, NVIDIA T4, Tenstorrent, Apple Silicon) surfaced in the inventory?

## Stuck?

Ask **oxtutor** — describe what you tried and what happened.
