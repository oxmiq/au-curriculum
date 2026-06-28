---
drift: |
  Originally Day 37 of the former Capsule wk8. Now sits as Day 35 of the new Bridge week
  (week-07/module-4), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 35 · Environments & Fleet Discovery

> **Concept of the day:** an **environment** is a fleet you can see; a **node** is a machine you can lease. `capsule env`, `capsule node list`, `capsule node show` are your three workhorse commands. Filter by capability — never by name when you can avoid it.<br>
> **Pre-reading:** <a href="../../../readings/capsule/">Capsule Power-User Pre-Lecture Reading — Day 37 section</a> (~25 min). Supplement: <a href="../../../readings/capsule/lab-guide/">Capsule Lab Guide</a> Module 3.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 7 — Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <span>Day 35 · Environments</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-07/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | What you do | Time |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: Environments & Discovery Commands | 20 min |
| Part 3 | Core Concepts: Node Anatomy & Status Fields | 20 min |
| Part 4 | Deep Dive: Capability-Based Filtering | 20 min |
| Part 5 | Core Concepts: Leases | 15 min |
| Part 6 | Hands-On: Fleet Discovery Drills | 40 min |
| Part 7 | Wrap-up & Connection | 10 min |

## Part 1 — Pre-Reading Review · 15 min

> Read Lab Guide **Module 3** (~15 min) before this lesson. Use this Part to consolidate what you read.

### Exercise: Self-Check

Answer these before you continue:

1. List the three workhorse commands for fleet discovery.
2. What fields indicate a node is available?
3. How do you filter by GPU type, by status, by tag?
4. Why prefer *capability-based* selection over *name-based*?
5. What's a **lease** and when does it expire?

If you hesitated on any of these, flag it — Parts 2–5 will close those gaps.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m4-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 3">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What are the three workhorse commands for fleet discovery in Capsule?",
    "options": [
      "capsule deploy, capsule status, capsule list",
      "capsule env, capsule node list, capsule node show",
      "capsule nodes, capsule fleets, capsule machines",
      "capsule get, capsule show, capsule info"
    ],
    "answer": 1,
    "explain": "The three workhorse commands are: (1) capsule env — list available environments, (2) capsule node list — list nodes in an environment, (3) capsule node show — get detailed info on a specific node."
  },
  {
    "stem": "Which fields indicate a node is available in Capsule?",
    "options": [
      "The node name",
      "status=available and lease_expires is in the future (or null)",
      "The GPU model",
      "The IP address"
    ],
    "answer": 1,
    "explain": "A node is available when its status is 'available' and lease_expires is either null (no active lease) or is in the future. If lease_expires is in the past, the node is currently leased."
  },
  {
    "stem": "How do you filter nodes by GPU type in Capsule?",
    "options": [
      "By node name",
      "Using --gpus flag or capability filters",
      "Using --gpu-model flag",
      "By IP address"
    ],
    "answer": 1,
    "explain": "You filter nodes by GPU type using --gpus flag or capability filters (e.g., --gpus H100). This is preferred over filtering by name because it ensures you get nodes with the capabilities you need."
  },
  {
    "stem": "Why should you prefer capability-based selection over name-based selection?",
    "options": [
      "Capability-based selection is faster",
      "Name-based selection doesn't work; capability-based ensures you get nodes with the required capabilities regardless of specific machine names",
      "Capability-based is shorter to type",
      "They are the same"
    ],
    "answer": 1,
    "explain": "Capability-based selection (filtering by GPU type, memory, etc.) is preferred over name-based because it ensures you get nodes with the required capabilities regardless of specific machine names. This is more robust and portable."
  },
  {
    "stem": "What is a lease in Capsule and when does it expire?",
    "options": [
      "A lease is a reservation that expires at a specific timestamp or when released",
      "A lease is a purchase agreement",
      "A lease never expires",
      "A lease is only for new users"
    ],
    "answer": 0,
    "explain": "A lease is a reservation of a node. It expires at a specific timestamp (the lease_expires field) or when explicitly released. When a lease expires, the node becomes available for others to claim."
  },
  {
    "stem": "What does 'capsule node show' command do?",
    "options": [
      "Lists all available nodes",
      "Shows detailed information about a specific node including status, capabilities, and lease info",
      "Shows the node IP address only",
      "Deletes a node"
    ],
    "answer": 1,
    "explain": "'capsule node show' displays detailed information about a specific node, including its status, capabilities (GPU type, memory), current lease information, and other metadata."
  },
  {
    "stem": "What is an environment in Capsule?",
    "options": [
      "A single node",
      "A fleet (cluster) of nodes that you can see and deploy to",
      "A programming language",
      "A type of GPU"
    ],
    "answer": 1,
    "explain": "An environment is a fleet — a cluster of nodes that you can see and deploy to. It's a logical grouping of machines managed together. You configure an environment once and can deploy models to all nodes in it."
  },
  {
    "stem": "How do you filter nodes by status in Capsule?",
    "options": [
      "Using --status flag",
      "Using status filters in the node list command",
      "By looking at the node name",
      "Status filtering is not supported"
    ],
    "answer": 1,
    "explain": "You filter nodes by status using status filters in the node list command (e.g., --available, --leased). Common statuses include 'available' (ready to lease) and 'leased' (currently in use)."
  }
]
</script>
</div>

## Part 2 — Core Concepts: Environments & Discovery Commands · 20 min

### Reading — Why this matters

Half of "Capsule is broken" tickets are actually "I leased the wrong machine." Knowing what's in the fleet, what's available, and how to filter cleanly is the difference between productive and frustrating.

### Reading — The discovery commands

| Command | Use |
|---|---|
| `capsule env list` | Show all environments you have access to |
| `capsule env use <env>` | Set default environment for subsequent commands |
| `capsule node list` | All nodes in the current env (or `--env` flag) |
| `capsule node list --status available --gpu h100` | Filter |
| `capsule node show <node-id>` | Full detail on one node |

### Reading — Hardware diversity in one fleet

Capsule's value: heterogeneous hardware behind one UX. You'll see:

| Class | What |
|---|---|
| NVIDIA H100 / A100 | High-end LLM serving |
| NVIDIA T4 / L4 / 3060 | Smaller models, dev work |
| NVIDIA RTX 4090 / 5090 | High clock, consumer |
| Tenstorrent Wormhole n150 / Blackhole p150 | Non-NVIDIA accelerators |
| Apple M2 / M3 | Laptop-class for testing |

The Week 9 benchmark suite will sweep across multiple classes to compare cost/perf — discovery is the entry point.

## Part 3 — Core Concepts: Node Anatomy & Status Fields · 20 min

### Reading — Anatomy of a node listing

A typical `capsule node list` row:

| Field | Example | Meaning |
|---|---|---|
| ID | `nv-h100-01-1` | Unique identifier (env-prefix-class-NN-instance) |
| GPU | `H100 80GB ×8` | Hardware |
| Status | `available` / `leased` / `unhealthy` / `draining` | Lease state |
| Leased by | `alice@oxmiq.com` | Owner (if any) |
| Until | `2025-09-15 18:00 UTC` | Lease expiry |
| Tags | `tp-ready, nvlink, ubuntu-22` | Capabilities |

The naming convention echoes `capsule-ansible` inventory: `nv-h100-04-1` = NVIDIA, H100-class, group 04, instance 1.

### Reading — When discovery is healthy vs sick

| Sign | Likely cause |
|---|---|
| `node list` returns 0 nodes | Wrong env, or auth scope too narrow |
| All nodes `unhealthy` | Control plane / agent connectivity issue (escalate) |
| Same node leased to two people | Race in scheduler (file a bug — Day 40) |
| Node `available` but `lease` fails | Tag mismatch or quota |

## Part 4 — Deep Dive: Capability-Based Filtering · 20 min

### Reading — Filter by capability, not name

**Don't:**
```
capsule node lease nv-h100-04-1
```

**Do:**
```
capsule node lease --gpu h100 --min-gpus 8 --tag nvlink --duration 4h
```

Why: hardware retires, names change, instances get rebuilt. Capability filters survive all of that. Plus you're explicit about what you actually need.

### Reading — Common filters

| Filter | Example |
|---|---|
| GPU class | `--gpu h100`, `--gpu a100`, `--gpu wormhole-n150` |
| Min count | `--min-gpus 4` |
| Tag | `--tag tp-ready`, `--tag bench` |
| Status | `--status available` |
| Free disk | `--min-disk 500g` |
| OS | `--os ubuntu-22` |

### Exercise: Write your personal filter

Write the `capsule node list` filter you'd use 90% of the time for your typical workload. Save it somewhere you can paste from quickly.

## Part 5 — Core Concepts: Leases · 15 min

### Reading — Leases

A **lease** is a time-bounded reservation of a node:

```
capsule node lease --gpu h100 --min-gpus 8 --duration 2h --reason "week-9 benchmark"
```

- Default duration varies by env (often 2h).
- Renewable: `capsule lease extend --hours 2`.
- Released on expiry, manual release (`capsule lease release`), or shutdown.
- **Reason field is mandatory in production** envs — searchable in audit logs.

## Part 6 — Hands-On: Fleet Discovery Drills · 40 min

### Exercise: Inventory the fleet

(15 min) Run `capsule env list`, then `capsule node list`. Identify available capacity by GPU class. Note which classes are available vs fully leased.

### Exercise: Capability filter

(20 min) Filter exercise: find every available 8×H100 node with NVLink in your env. Express as a single command. Then:

1. Lease a small dev node for 1 hour.
2. Verify the lease shows under your name (`capsule node show <id>`).
3. Release it (`capsule lease release`).

### Exercise: Pair — hardware diversity

(5 min) Each person filters for a different hardware class. Compare what's available and what's scarce.

## Part 7 — Wrap-up & Connection · 10 min

**Before you finish, check each item:**

- [ ] I can run `capsule node list` and read every field in the output.
- [ ] I can find available capacity by GPU class using a capability filter.
- [ ] I know the difference between `available`, `leased`, `unhealthy`, and `draining` status.
- [ ] I understand why capability-based filtering is preferable to name-based.
- [ ] I know what a lease is and how to release one.

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 35 · Environments &amp; Fleet Discovery">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the difference between `available`, `leased`, and `draining` node status in Capsule?",
    "options": [
      "available = idle, leased = in use by you, draining = being prepared for maintenance and will not accept new leases",
      "available = online, leased = offline, draining = rebooting",
      "available = GPU free, leased = CPU in use, draining = network disconnected",
      "All three statuses mean the same thing on different hardware generations"
    ],
    "answer": 0,
    "explain": "Node statuses: available = the node is ready and can be leased; leased = currently allocated to a user (could be you or someone else); draining = the node is being gracefully emptied for maintenance and won't accept new leases but existing ones continue; unhealthy = the node has a fault and is not usable."
  },
  {
    "stem": "Why is capability-based filtering preferable to name-based filtering when selecting a node?",
    "options": [
      "Capability filters are faster to type",
      "Name-based filters require knowing exact machine names which change; capability filters (GPU type, memory, features) find any compatible machine regardless of its specific name",
      "Capability filters work without authentication",
      "Name-based filters don't work in the production environment"
    ],
    "answer": 1,
    "explain": "Machine names are internal identifiers that change when machines are replaced. Capability filters — e.g., `--gpu-type H100 --gpu-memory 80GB` — find any machine meeting your requirements. This makes scripts and workflows portable: they work on any matching machine, not just a specific named one."
  },
  {
    "stem": "What is a lease in Capsule, and what does releasing it do?",
    "options": [
      "A lease is a model license — releasing it makes the model available to other users",
      "A lease is a time-limited exclusive reservation of a node — releasing it returns the node to the available pool for others to use",
      "A lease is a billing commitment — releasing it stops charges",
      "A lease is a connection session — releasing it disconnects your terminal"
    ],
    "answer": 1,
    "explain": "A lease is an exclusive reservation: while you hold it, the node is not available to others. Releasing (`capsule lease release`) returns it to `available` status. Good etiquette: release leases promptly when your work is done — GPU time is a shared, expensive resource."
  },
  {
    "stem": "What command would you use to find available H100 nodes in Capsule?",
    "options": [
      "`capsule node list --status available --gpu H100`",
      "`capsule find gpu --type H100 --free`",
      "`capsule inventory search H100`",
      "`capsule machines --filter=h100`"
    ],
    "answer": 0,
    "explain": "The standard pattern is `capsule node list` with status and GPU-type filters. Exact flag syntax varies by CLI version, but the concept is: filter on `--status available` to exclude leased/unhealthy nodes, and a GPU class filter to find H100s specifically. Refer to `capsule node list --help` for current flag names."
  },
  {
    "stem": "What does `capsule node show <id>` display?",
    "options": [
      "The list of all leases held by the node's current user",
      "Detailed information about a specific node: hardware specs, status, current leaseholder, uptime, and capability tags",
      "The command history run on that node",
      "The network route between your workstation and the node"
    ],
    "answer": 1,
    "explain": "`capsule node show <id>` gives full detail on a single node: its hardware (GPU type, count, memory), current status (available/leased/unhealthy), who holds the current lease, how long it's been running, and its capability tags. Useful for verifying you're leasing the right hardware before committing."
  }
]
</script>
</div>

### Connect forward

Tomorrow: **connecting** — once you have a lease, how to actually shell in, what the session looks like, the etiquette of multi-user nodes.

### Pre-read for tomorrow (Day 38 · Connecting to Machines)

- **Resource:** <a href="../../../readings/capsule/">Capsule Power-User Pre-Lecture Reading — Day 38 section</a> (~25 min). Supplement: <a href="../../../readings/capsule/lab-guide/">Capsule Lab Guide</a> Module 5.
- **Reflection questions:**
  1. What command connects you to a leased node?
  2. How does Capsule's connect differ from raw `ssh`?
  3. What state is preserved between connect sessions vs lost?

## Stuck?

Ask **oxtutor** — describe what you tried and what happened.
