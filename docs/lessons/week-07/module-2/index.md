---
drift: |
  Authored as a combined "Architecture + Installation" day (former wk8 day 36). New graph
  splits this into two consecutive modules: week-07/module-2 (Foundations) and
  week-07/module-3 (Installation). For now this lesson covers BOTH concepts in a single
  page; module-3 is a redirect stub pointing to the install sections below. Future
  authoring should extract the install flow into its own page.
---

# Day 33 · Capsule Foundations & Architecture

> **Concept of the day:** **Capsule** = orchestration platform for on-prem GPU fleets. CLI on your laptop talks to a **control plane**; the control plane manages **environments** (clusters of nodes); each node runs an **agent** that exposes machines. Install once, configure once, operate every day.
> **Pre-reading:** Capsule Power User Lab Guide **Modules 1 + 2** (~35 min).
> **Source:** [Lab Guide](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md) · [Cheatsheet](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Cheatsheet.md). The installation deep-dive in this lesson is *also* the source for the next module ([Day 34 · Installation](../module-3/index.md))​.

---

## Why this matters

This is Phase 3's foundation. Every benchmark in Week 9, every agent in Week 7's project — they all land on Capsule machines. If you don't have a clean mental model of the architecture, every "why won't this connect?" debug session will burn 30 minutes instead of 30 seconds.

## Readiness check

1. Name the three layers of the Capsule architecture.
2. What's the difference between the **CLI**, the **control plane**, and the **node agent**?
3. Where does authentication live?
4. What does an **environment** contain?
5. After install, what's the first command you run to verify it works?

## Core concept

### The three layers

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

### Installation flow (macOS + Linux)

1. Install the CLI: `brew install capsule` (or the equivalent for your platform).
2. Authenticate: `capsule login` — opens a browser, returns a token.
3. Verify: `capsule whoami` — confirms identity.
4. Configure default env: `capsule env use <env-name>`.

That's the happy path. On a fresh laptop it's ~5 minutes.

### What a Capsule "install" actually does

| Component | Where it lives | What it stores |
|---|---|---|
| Binary | `/usr/local/bin/capsule` (or equivalent) | the CLI itself |
| Config dir | `~/.capsule/` | tokens, default env, cached env metadata |
| Token | `~/.capsule/credentials` | refresh + access tokens, encrypted at rest on macOS Keychain when available |

### Common install gotchas (Module 1 quirks)

| Symptom | Cause |
|---|---|
| `capsule: command not found` | PATH doesn't include install dir; restart shell |
| `capsule login` browser doesn't open | Headless terminal; use `--device-code` flow |
| `whoami` says unauthorized after login | Clock skew between laptop and control plane; sync NTP |
| SSH to a node hangs after `capsule connect` | Corporate proxy mangling websockets; need `HTTPS_PROXY` |

These are the four most-asked support questions. Memorize them.

### What an environment contains

An **environment** is a logical grouping of nodes — usually one per geographic site or per hardware class:

- A list of nodes (machines).
- Per-node metadata: GPU type, model, status, leased-by.
- Per-environment policies: who can connect, what tools are pre-installed.
- A shared storage pool (covered Day 39).

Examples: `production`, `development`, `production-fre`, `production-tenstorrent` (mirroring the `capsule-ansible` inventory naming).

### Why this design

| Goal | Mechanism |
|---|---|
| Identity-aware access | CLI → control plane → node, never direct |
| Multi-tenant safety | Per-user / per-team environments + leases |
| Heterogeneous fleet | Environments group by hardware; users select by capability |
| Auditable operation | Every CLI action logs through control plane |

## Practice (90 min)

1. (20 min) Install Capsule on your laptop. Verify with `capsule version` and `capsule whoami`.
2. (15 min) Run `capsule env list`. Identify which environments you have access to. Pick one as default.
3. (15 min) Draw the 3-layer architecture from memory on paper. Label each layer with: where it runs, what it stores, who talks to it.
4. (25 min) Pair: walk a partner through your install. Hit at least one of the 4 common gotchas. Resolve.
5. (15 min) Read the Cheatsheet's "first 10 minutes" section. Familiarize with the command surface.

## Wrap-up

Every student can run `capsule whoami` successfully and name the environment they're in.

## Connect forward

Tomorrow: **environments and fleet discovery** — how to find what's available, what to ask for, and how to read the inventory.

---

## Pre-read for tomorrow (Day 37 · Environments & Fleet Discovery)

- **Resource:** Lab Guide **Module 3** (~15 min).
- **Reflection questions:**
  1. How do you list available machines in an environment?
  2. What fields tell you a machine is *available* vs *leased*?
  3. How is hardware diversity (NVIDIA H100, NVIDIA T4, Tenstorrent, Apple Silicon) surfaced in the inventory?
