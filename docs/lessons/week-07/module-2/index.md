---
drift: |
  Authored as a combined "Architecture + Installation" day (former wk8 day 36). New graph
  splits this into two consecutive modules: week-07/module-2 (Foundations) and
  week-07/module-3 (Installation). For now this lesson covers BOTH concepts in a single
  page; module-3 is a redirect stub pointing to the install sections below. Future
  authoring should extract the install flow into its own page.
---

# Day 32 · Capsule Foundations & Architecture

> **Concept of the day:** **Capsule** = a remote development and application streaming platform for GPU fleets. You stay on your laptop; the CLI brokers a connection to a remote machine: by default over the **SshRTC data channel** (SSH tunnelled through WebRTC), or over **direct SSH** with `--direct`. What machines you *see* is governed by two routing dimensions: the **environment** (backend deployment: `prod`/`public`/`dev`/`demo`) and the **customer** fleet selector. Install once, configure once, operate every day.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#capsule-architecture-installation">Capsule Power-User Pre-Lecture Reading - Capsule Architecture & Installation</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-1-capsule-foundations">Capsule Lab Guide</a> Modules 1 + 2.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 7 - Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <span>Day 32 · Capsule Foundations</span>
    {status:week-07/module-2}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | What you do |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: How Capsule Connects You |
| Part 3 | Core Concepts: Installation Flow |
| Part 4 | Deep Dive: What the CLI Stores Locally |
| Part 5 | Hands-On: Install & Verify |
| Part 6 | Hands-On: Architecture Diagram |
| Part 7 | Wrap-up & Connection |

## Part 1 - Pre-Reading Review

> Read the Capsule Power User Lab Guide **Modules 1 + 2** before this lesson. Use this Part to consolidate what you read.

### Exercise: Self-Check

Answer these before you continue; they preview where you'll be uncertain:

1. Name the two connection paths Capsule can use to reach a machine.
2. What's the difference between an **environment** and a **customer**; which routing dimension does each control?
3. How does Capsule authenticate you, and where is the cached token stored?
4. What does switching to a different **environment** change, and why does it force a re-login?
5. After install, what's the first command you run to verify it works?

If you hesitated on any of these, flag it; the next three Parts will close those gaps.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m2-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What is Capsule?", "options": ["A managed cloud GPU rental marketplace", "A remote development and application streaming platform: you stay on your laptop while terminals, editors, and desktops run on remote hardware and are piped back over the network", "A Python library for quantizing model weights", "A Kubernetes distribution you install on your own cluster"]},
  {"stem": "Which connection method does `capsule term` use by default?", "options": ["The SshRTC data channel: SSH carried over a WebRTC peer connection, which reaches machines that have no public-facing port", "Direct TCP SSH to a publicly reachable port", "A plain HTTP REST call to the machine", "Telnet"]},
  {"stem": "How do you force a plain TCP SSH connection instead of the SshRTC (WebRTC) data channel?", "options": ["Run `capsule connect --tcp`", "Set the environment variable CAPSULE_TCP=1", "Add the `--direct` flag to the command", "There is no way; SshRTC is mandatory"]},
  {"stem": "How does Capsule authenticate you when you first log in?", "options": ["A static API key you paste into a config file", "A username and password stored in `~/.capsule/credentials`", "An SSH key exchanged directly with each node", "A browser-based Azure B2C login via `capsule auth login`, which caches an auth token (with a manual-token fallback for headless sessions)"]},
  {"stem": "What is an 'environment' in Capsule (e.g. prod, public, dev, demo)?", "options": ["A cluster of GPU nodes managed together as one unit", "A backend deployment that selects the endpoint and B2C tenant you authenticate against", "A Python virtualenv created on the remote machine", "A saved set of default benchmark parameters"]},
  {"stem": "`capsule list` looks empty or shows the wrong machines. What should you check first?", "options": ["The customer selector, with `capsule config customer show`", "The GPU driver version installed on each node", "Your local `~/.ssh/known_hosts` file", "The benchmark results dashboard"]},
  {"stem": "Where does the Capsule CLI store its configuration and SSH keys on macOS?", "options": ["In `~/.capsule/`", "In `/etc/capsule/`", "In `$HOME/Library/Application Support/Capsule/`", "In `/usr/local/share/capsule/`"]},
  {"stem": "You want any available machine from a pool in one case, and one specific physical box in another. How do you target each?", "options": ["Both always require the `--unique` flag", "Config tags need `--json`; unique IDs need `--users`", "You can only ever connect to the default machine", "Use a config tag for any-from-pool; use `-u`/`--unique <unique-id>` for a specific box"]}
]
</script>
</div>

## Part 2 - Core Concepts: How Capsule Connects You

### Reading - Why this matters

This is Phase 3's foundation. Every benchmark in Week 9, every agent in Week 7's project: they all land on Capsule machines. If you don't have a clean mental model of how the CLI reaches a machine and how the fleet you see is scoped, every "why won't this connect?" or "why can't I see my machine?" debug session will burn 30 minutes instead of 30 seconds.

### Reading - The shape: your laptop → the platform → remote machines

You stay on your laptop. The CPU, GPU, RAM, and disk live on a remote machine. Everything you type, terminals, VS Code, Cursor, full desktops, runs remotely and is piped back to you over the network. The CLI (`capsule`, or its shortcut `cap`) is the only piece that runs locally.

There are **two connection paths** underneath every connect command:

| Path | Flag | Tradeoff |
|---|---|---|
| **SshRTC data channel** (default) | *(none)* | SSH carried over a WebRTC peer connection. The remote never needs a publicly reachable port; NAT traversal "just works" most of the time. |
| **Direct SSH** | `--direct` | Plain TCP SSH. Needs a reachable SSH port. Faster and easier to debug; needed when WebRTC fails or for clean port-forwarding. |

`capsule term`, `capsule code`, and `capsule cursor` use SshRTC by default; add `--direct` to fall back to TCP SSH. (`capsule ssh` is the direct-SSH-by-default variant.)

### Reading - The two routing dimensions

The single biggest source of "Capsule is broken" tickets is not the connection path; it's *which fleet you are pointed at*. Two independent settings decide that:

| Dimension | Command | What it controls |
|---|---|---|
| **Environment** | `capsule env show` / `capsule env set <name>` | The backend deployment you talk to: `prod`, `public`, `dev`, or `demo`. Each selects a B2C tenant and API endpoint. |
| **Customer** | `capsule config customer show` / `set` / `unset` | The fleet selector *inside* an environment: `micc` (default), `modelhosting`, `oneplay`, `cree8`. It scopes which machines appear in `capsule list`. |

**Key insight:** an *environment* is a backend deployment, **not** a cluster of machines. Which machines you can see is chosen by the *customer* selector, layered on top of the environment. When `capsule list` looks empty or wrong, check `capsule env show` and `capsule config customer show` before anything else.

### Reading - Why this design

| Goal | Mechanism |
|---|---|
| Identity-aware access | Every command carries your Azure B2C token; the backend authorizes you |
| Reach machines behind NAT/firewalls | SshRTC data channel: no public port required on the remote |
| One UX over a heterogeneous fleet | `capsule list` groups machines by config tag; filter by capability |
| Isolated tenants | Environment (tenant/endpoint) × customer (fleet) scoping |

### Reading - Authentication

Capsule authenticates through **Azure B2C** (not GitHub). `capsule auth login` opens a browser to the B2C login page and caches the returned token locally. If no browser is available (headless/remote), it falls back to a manual token flow: it prints a URL (`https://oxmiq.ai/oxcapsule/auth`) and you paste back the token it gives you. For automation you can instead set `CAPSULE_AUTH_TOKEN`. Because the token is scoped to an environment, switching environments with `capsule env set` is followed by a fresh `capsule auth login`.

> A GitHub token (`GH_TOKEN`) is used only to *install and update* Capsule and to access private repos with `--repo`: never for runtime authentication. Don't confuse the two.

## Part 3 - Core Concepts: Installation Flow

### Reading - Installation flow (macOS + Linux)

1. Install the CLI: `brew install capsule` (or the equivalent for your platform).
2. Authenticate: `capsule auth login` - opens a browser for the Azure B2C flow, caches a token.
3. Verify: `capsule status` - confirms your identity and token expiry.
4. Select your environment: `capsule env set <env-name>`, then re-run `capsule auth login` (the token is scoped per environment).

That's the happy path. On a fresh laptop it's ~5 minutes. (Day 33 covers install in depth.)

### Reading - Common install gotchas

| Symptom | Cause |
|---|---|
| `capsule: command not found` | PATH doesn't include install dir; restart shell |
| `capsule auth login` browser doesn't open | Headless terminal; use the manual-token fallback (it prints a URL) or set `CAPSULE_AUTH_TOKEN` |
| `capsule status` says unauthorized after login | Wrong environment selected, or an expired/mismatched token; re-run `capsule auth login` for the right env |
| Connection hangs after `capsule term` | Corporate proxy mangling WebRTC; fall back to `--direct` or fix `HTTPS_PROXY` |

These are the most-asked support questions. Memorize them.

## Part 4 - Deep Dive: What the CLI Stores Locally

### Reading - What a Capsule "install" actually does

The CLI keeps its state in one OS-specific config directory; **there is no `~/.capsule/`**:

| Component | Where it lives | What it stores |
|---|---|---|
| Binary | `/usr/local/bin/capsule` (Intel) or `/opt/homebrew/bin/capsule` (Apple Silicon); on PATH | the CLI itself (invoked as `capsule` or `cap`) |
| Config dir (macOS) | `$HOME/Library/Application Support/Capsule/` | `capsule.conf`, the auto-generated `capsule_rsa`/`capsule_rsa.pub` SSH keypair, `rclone.conf` |
| Config dir (Windows) | `%APPDATA%\capsule` | same contents as above |

The cached Azure B2C auth token lives alongside this config (on macOS it can be held in the Keychain). Your SSH keypair is generated here automatically the first time you connect.

### Exercise: Trace a connection

Draw the flow for `capsule term <config-tag>`:

1. The CLI reads your cached Azure B2C token from the config directory.
2. It contacts the Capsule backend for the environment named by `capsule env show`, scoped to the fleet from `capsule config customer show`.
3. The backend authorizes you and resolves the config tag to an available machine.
4. An SshRTC (WebRTC) data channel is negotiated to that machine: no public port required.
5. The CLI proxies your shell over that channel. (Add `--direct` to use plain TCP SSH instead.)

**Question:** at which step would a wrong-customer setting manifest? At which step would a corporate proxy blocking WebRTC manifest? Write your answers before continuing.

## Part 5 - Hands-On: Install & Verify

### Exercise: Install Capsule on your laptop

 Install Capsule on your laptop. Verify with `capsule --version` and `capsule status`.

Expected output:

```
$ capsule --version
capsule version 1.x.x
$ capsule status
user: alice@oxmiq.com
env: prod
```

If you hit one of the gotchas from Part 3, resolve it now. Pair up if needed.

### Exercise: Select your environment

 Run `capsule env show` to see your current environment. Switch with `capsule env set <env-name>` (`prod`, `public`, `dev`, or `demo`) and re-run `capsule auth login`, since the token is scoped per environment.

## Part 6 - Hands-On: Architecture Diagram

### Exercise: Draw from memory

 Draw Capsule's connection model on paper: no peeking. Include:

- Your laptop (the CLI) and the remote machine
- The two connection paths (SshRTC by default, `--direct` fallback)
- The two routing dimensions (environment and customer) and what each controls

Compare your drawing to Part 2. Note every discrepancy.

### Exercise: Explore the Cheatsheet

 Read the Cheatsheet's "first 10 minutes" section. Familiarize with the command surface.

## Part 7 - Wrap-up & Connection

**Before you finish, check each item:**

- [ ] I can run `capsule status` successfully.
- [ ] I can name the two connection paths (SshRTC by default, direct SSH via `--direct`).
- [ ] I know what the config directory stores (config, SSH keypair, cached token) and where it lives on my OS.
- [ ] I know the difference between an "environment" and a "customer", and which one I'm in.
- [ ] I've resolved any install gotchas I encountered.

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m2-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 32 · Capsule Foundations &amp; Architecture">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What are the two connection paths Capsule can use to reach a remote machine?", "options": ["HTTP polling and gRPC streaming", "The SshRTC data channel (SSH over WebRTC, the default) and direct TCP SSH (via `--direct`)", "Telnet and rlogin", "A control-plane tunnel and a node-agent tunnel"]},
  {"stem": "Where does the Capsule CLI keep its local config and cached token, and why store the token locally?", "options": ["In `~/.capsule/`: because every CLI relies on a dotfile in the home directory", "In the OS config dir (macOS `$HOME/Library/Application Support/Capsule/`, Windows `%APPDATA%\\capsule`): the token is cached so you don't re-authenticate on every command", "In `/etc/capsule/`: so all users on the machine share one token", "Nowhere; the token is re-fetched from the server on every command"]},
  {"stem": "What is an 'environment' in Capsule (e.g. prod, public, dev, demo)?", "options": ["A Python virtualenv for running model code", "A backend deployment that selects the API endpoint and Azure B2C tenant you authenticate against: switched with `capsule env set`", "A cluster of GPU machines managed together as one unit", "A container image used as the base for all workloads"]},
  {"stem": "What does `capsule status` tell you?", "options": ["The current operating-system user running the Capsule process", "Your authenticated identity (user email) and token expiry, as seen by the Capsule backend", "The version of the Capsule CLI installed", "The GPU hardware specification of the machine you're connected to"]},
  {"stem": "`capsule list` is empty or shows the wrong machines. What should you check first, and why?", "options": ["The GPU driver version on each machine: a mismatch hides machines from the list", "Your environment (`capsule env show`) and customer selector (`capsule config customer show`): these two settings scope which fleet you see", "Your `~/.ssh/known_hosts` file: stale host keys hide machines", "The benchmark dashboard: the fleet list mirrors the last benchmark run"]},
  {"stem": "What is the difference between an 'environment' and a 'customer' in Capsule?", "options": ["The environment is the backend deployment (prod/public/dev/demo: endpoint + B2C tenant); the customer is the fleet selector inside it that scopes which machines appear in `capsule list`", "The environment is a cluster of GPU machines; the customer is the billing account", "They are two names for the same setting", "The environment picks a GPU vendor; the customer picks a region"]},
  {"stem": "`capsule term` won't connect through a corporate proxy that mangles WebRTC. How do you force a plain TCP SSH connection instead?", "options": ["Run `capsule connect --tcp`", "Set the environment variable `CAPSULE_TCP=1`", "Add the `--direct` flag (e.g. `capsule term <tag> --direct`)", "There is no fallback; SshRTC is mandatory"]},
  {"stem": "How does Capsule authenticate you at runtime, and what is GH_TOKEN used for?", "options": ["GitHub OAuth handles both runtime auth and machine access", "A static API key in capsule.conf; GH_TOKEN is unused", "SSH keys exchanged with each node; GH_TOKEN authorizes those keys", "Azure B2C via `capsule auth login` (browser flow, cached token, manual-token fallback for headless); GH_TOKEN is only for installing/updating Capsule and `--repo` access, never runtime auth"]},
  {"stem": "You run `capsule list` and see the wrong fleet. Which command changes which customer's machines you see?", "options": ["`capsule env set <name>`", "`capsule config customer set <name>` (and `capsule config customer show` / `unset` to inspect or clear it)", "`capsule list --refresh`", "`capsule node list --customer <name>`"]}
]
</script>
</div>

### Connect forward

Tomorrow: **environments and fleet discovery** - how to find what's available, what to ask for, and how to read the inventory.

### Pre-read for tomorrow (Day 36 · Environments & Fleet Discovery)

- **Resource:** <a href="../../../readings/capsule/#environments-fleet-discovery">Capsule Power-User Pre-Lecture Reading - Environments & Fleet Discovery</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-3-environments-customers-and-why-your-fleet-looks-wrong">Capsule Lab Guide</a> Module 3.
- **Reflection questions:**
  1. How do you list available machines in an environment?
  2. What fields tell you a machine is *available* vs *leased*?
  3. How is hardware diversity (NVIDIA H100, NVIDIA T4, Tenstorrent, Apple Silicon) surfaced in the inventory?

## Stuck?

Ask **oxtutor**; describe what you tried and what happened.
