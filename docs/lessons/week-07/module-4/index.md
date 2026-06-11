---
drift: |
  Originally Day 37 of the former Capsule wk8. Now sits as Day 35 of the new Bridge week
  (week-07/module-4), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 35 · Environments & Fleet Discovery

> **Concept of the day:** an **environment** is a fleet you can see; a **node** is a machine you can lease. `capsule env`, `capsule node list`, `capsule node show` are your three workhorse commands. Filter by capability — never by name when you can avoid it.
> **Pre-reading:** Lab Guide **Module 3** (~15 min).
> **Source:** [Lab Guide Module 3](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md).

---

## Why this matters

Half of "Capsule is broken" tickets are actually "I leased the wrong machine." Knowing what's in the fleet, what's available, and how to filter cleanly is the difference between productive and frustrating.

## Readiness check

1. List the three workhorse commands for fleet discovery.
2. What fields indicate a node is available?
3. How do you filter by GPU type, by status, by tag?
4. Why prefer *capability-based* selection over *name-based*?
5. What's a **lease** and when does it expire?

## Core concept

### The discovery commands

| Command | Use |
|---|---|
| `capsule env list` | Show all environments you have access to |
| `capsule env use <env>` | Set default environment for subsequent commands |
| `capsule node list` | All nodes in the current env (or `--env` flag) |
| `capsule node list --status available --gpu h100` | Filter |
| `capsule node show <node-id>` | Full detail on one node |

### Anatomy of a node listing

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

### Filtering — by capability, not name

**Don't:**
```
capsule node lease nv-h100-04-1
```

**Do:**
```
capsule node lease --gpu h100 --min-gpus 8 --tag nvlink --duration 4h
```

Why: hardware retires, names change, instances get rebuilt. Capability filters survive all of that. Plus you're explicit about what you actually need.

### Common filters

| Filter | Example |
|---|---|
| GPU class | `--gpu h100`, `--gpu a100`, `--gpu wormhole-n150` |
| Min count | `--min-gpus 4` |
| Tag | `--tag tp-ready`, `--tag bench` |
| Status | `--status available` |
| Free disk | `--min-disk 500g` |
| OS | `--os ubuntu-22` |

### Leases

A **lease** is a time-bounded reservation of a node:

```
capsule node lease --gpu h100 --min-gpus 8 --duration 2h --reason "week-9 benchmark"
```

- Default duration varies by env (often 2h).
- Renewable: `capsule lease extend --hours 2`.
- Released on expiry, manual release (`capsule lease release`), or shutdown.
- **Reason field is mandatory in production** envs — searchable in audit logs.

### Hardware diversity in one fleet

Capsule's value: heterogeneous hardware behind one UX. You'll see:

| Class | What |
|---|---|
| NVIDIA H100 / A100 | High-end LLM serving |
| NVIDIA T4 / L4 / 3060 | Smaller models, dev work |
| NVIDIA RTX 4090 / 5090 | High clock, consumer |
| Tenstorrent Wormhole n150 / Blackhole p150 | Non-NVIDIA accelerators |
| Apple M2 / M3 | Laptop-class for testing |

The Week 9 benchmark suite will sweep across multiple classes to compare cost/perf — discovery is the entry point.

### When discovery is healthy vs sick

| Sign | Likely cause |
|---|---|
| `node list` returns 0 nodes | Wrong env, or auth scope too narrow |
| All nodes `unhealthy` | Control plane / agent connectivity issue (escalate) |
| Same node leased to two people | Race in scheduler (file a bug — Day 40) |
| Node `available` but `lease` fails | Tag mismatch or quota |

## Practice (90 min)

1. (15 min) Run `capsule env list`, `capsule node list`. Identify available capacity by GPU class.
2. (20 min) Filter exercise: find every available 8×H100 node with NVLink in your env. Express as a single command.
3. (20 min) Lease a small dev node for 1 hour. Verify lease shows under your name. Release it.
4. (25 min) Pair: each person filters for a different hardware class. Discuss what's available and what's scarce.
5. (10 min) Write a one-line cheat: the `capsule node list` filter you'll use 90% of the time.

## Wrap-up

Cohort can find available capacity by capability in any environment they have access to.

## Connect forward

Tomorrow: **connecting** — once you have a lease, how to actually shell in, what the session looks like, the etiquette of multi-user nodes.

---

## Pre-read for tomorrow (Day 38 · Connecting to Machines)

- **Resource:** Lab Guide **Module 5** (~15 min).
- **Reflection questions:**
  1. What command connects you to a leased node?
  2. How does Capsule's connect differ from raw `ssh`?
  3. What state is preserved between connect sessions vs lost?
