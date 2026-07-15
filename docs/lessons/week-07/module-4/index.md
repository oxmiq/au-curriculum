---
drift: |
  Originally Day 37 of the former Capsule wk8. Now sits as Day 34 of the new Bridge week
  (week-07/module-4), unchanged in scope. Source-material link paths bumped one level deeper.
---

# Day 34 · Environments & Fleet Discovery

> **Concept of the day:** an **environment** is a backend deployment (`prod`/`public`/`dev`/`demo`); the **customer** selector scopes which fleet you see inside it; and `capsule list` is how you discover machines. `capsule env show`, `capsule config customer show`, and `capsule list` (with `--filter`, `--users`, `--json`, `--all`) are your workhorse commands. Filter by capability: never by name when you can avoid it.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#environments-fleet-discovery">Capsule Power-User Pre-Lecture Reading - Environments & Fleet Discovery</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-3-environments-customers-and-why-your-fleet-looks-wrong">Capsule Lab Guide</a> Module 3.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 7 - Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <span>Day 34 · Environments</span>
    {status:week-07/module-4}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | What you do |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: Environments & Discovery Commands |
| Part 3 | Core Concepts: Reading the Fleet Listing |
| Part 4 | Deep Dive: Capability-Based Filtering |
| Part 5 | Core Concepts: Sessions & Claiming Machines |
| Part 6 | Hands-On: Fleet Discovery Drills |
| Part 7 | Wrap-up & Connection |

## Part 1 - Pre-Reading Review

> Read Lab Guide **Module 3** before this lesson. Use this Part to consolidate what you read.

### Exercise: Self-Check

Answer these before you continue:

1. List the workhorse commands for fleet discovery (env, customer, list).
2. What does `capsule list --users` tell you before you claim a machine?
3. How do you filter the fleet by vendor, by VRAM, by GPU model?
4. Why prefer *capability-based* selection over *name-based*?
5. How do you target one specific physical machine instead of any-from-pool?

If you hesitated on any of these, flag it; Parts 2–5 will close those gaps.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m4-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 3">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What is an environment in Capsule?", "options": ["A cluster of GPU nodes you can deploy models across", "A backend deployment (prod, public, dev, demo) that determines the B2C tenant and API endpoint", "A single machine you have leased for a session", "A saved capsule list filter expression"]},
  {"stem": "Within one environment, which command changes the fleet of machines you actually see?", "options": ["capsule env set <name>", "capsule list --refresh", "capsule config customer set <name>", "capsule node list --env <name>"]},
  {"stem": "Why does switching environments with `capsule env set` require you to re-authenticate?", "options": ["Each environment uses a different B2C tenant, so your auth token is scoped per environment", "Switching environments re-indexes the fleet, which invalidates the session", "Any active leases expire the moment you change environments", "It resets the customer override back to the default"]},
  {"stem": "Which command lists the machines available to you in the current environment and customer fleet?", "options": ["capsule node list", "capsule fleets", "capsule machines --available", "capsule list"]},
  {"stem": "How do you list every NVIDIA machine with at least 24 GB of VRAM?", "options": ["capsule node list --gpus nvidia --vram 24", "capsule list --filter \"vendor=nvidia,vram>=24\"", "capsule list --gpu nvidia --min-vram 24", "capsule node show --vendor nvidia"]},
  {"stem": "How do you target one specific physical machine rather than any available machine from a pool?", "options": ["Use --gpus with the exact GPU model to pin the box", "A config tag always targets one specific machine; a pool needs --all", "Pass the config tag alone; the scheduler resolves it to a fixed machine", "Use its unique ID with -u/--unique (see unique IDs via capsule list --all)"]},
  {"stem": "`capsule list` is showing machines that don't belong to the fleet you expect. What do you check first?", "options": ["capsule env show and capsule config customer show", "capsule node show on each unexpected machine", "Run capsule list --refresh to rebuild the index", "capsule status --gpus to confirm hardware inventory"]},
  {"stem": "What does `capsule list --users` show, and why is it useful?", "options": ["The list of users permitted to lease each machine", "The lease_expires timestamp for every machine", "Which machines have active user sessions: a sniff test before claiming a machine", "Only the machines you personally have reserved"]}
]
</script>
</div>

## Part 2 - Core Concepts: Environments & Discovery Commands

### Reading - Why this matters

Half of "Capsule is broken" tickets are actually "I leased the wrong machine." Knowing what's in the fleet, what's available, and how to filter cleanly is the difference between productive and frustrating.

### Reading - The discovery commands

| Command | Use |
|---|---|
| `capsule env show` | Show your current environment |
| `capsule env set <env>` | Switch environment (then re-run `capsule auth login`) |
| `capsule config customer show` | Show the current customer fleet selector |
| `capsule config customer set <name>` | Switch which customer's fleet you see |
| `capsule list` | List machines in the current env + customer fleet, grouped by config tag |
| `capsule list --filter "vendor=nvidia,vram>=24"` | Filter by capability |
| `capsule list --users` | Show which machines have active user sessions |
| `capsule list --json` | Emit JSON for scripting / `jq` |
| `capsule list --all` | Reveal per-machine unique IDs |

### Reading - Hardware diversity in one fleet

Capsule's value: heterogeneous hardware behind one UX. You'll see:

| Class | What |
|---|---|
| NVIDIA H100 / A100 | High-end LLM serving |
| NVIDIA T4 / L4 / 3060 | Smaller models, dev work |
| NVIDIA RTX 4090 / 5090 | High clock, consumer |
| Tenstorrent Wormhole n150 / Blackhole p150 | Non-NVIDIA accelerators |
| Apple M2 / M3 | Laptop-class for testing |

The Week 9 benchmark suite will sweep across multiple classes to compare cost/perf; discovery is the entry point.

## Part 3 - Core Concepts: Reading the Fleet Listing

### Reading - Anatomy of a fleet listing

`capsule list` groups machines by **config tag** (a machine pool / class). A typical entry surfaces:

| Field | Example | Meaning |
|---|---|---|
| Config tag | `gpu-workstation-01` | The pool name you connect to; the scheduler hands you any available member |
| Machine specs | `H100 80GB ×8`, CPU, memory | Hardware, shown by `capsule list` |
| Active users | `alice@oxmiq.com` | Who is currently on the machine: shown with `capsule list --users` |
| Unique ID | `boostergold461` | A specific physical machine: shown with `capsule list --all`, targeted with `-u`/`--unique` |

Use `capsule list --json | jq` to pull any of these fields programmatically.

### Reading - When discovery is healthy vs sick

| Sign | Likely cause |
|---|---|
| `capsule list` returns 0 machines | Wrong environment or wrong customer selector: check `capsule env show` and `capsule config customer show` |
| The fleet looks like a different customer's | A stray `capsule config customer set`: run `capsule config customer unset` |
| A machine you expected is missing | Someone already has an active session on it (`capsule list --users`), or you're in the wrong env/customer |
| Auth errors on every command | Token expired or scoped to a different environment: re-run `capsule auth login` |

## Part 4 - Deep Dive: Capability-Based Filtering

### Reading - Filter by capability, not name

**Don't** hard-code a specific machine when any matching one will do:
```
capsule ssh boostergold461 --unique
```

**Do** describe the capability you need and let the fleet listing find it:
```
capsule list --filter "vendor=nvidia,vram>=24"
```

Why: hardware retires, names change, instances get rebuilt. Capability filters survive all of that. Plus you're explicit about what you actually need.

### Reading - The filter grammar

`--filter` takes a comma-separated list of `key=value` (or `key>=value`) terms, combined with AND semantics:

| Filter term | Example |
|---|---|
| Vendor | `vendor=nvidia` |
| VRAM (GB) | `vram>=24` |
| GPU model | `gpu=rtx` |
| System memory (GB) | `memory>=100` |
| OS | `os=linux` |
| CI-flagged | `ci=true` |
| Combined | `vendor=nvidia,vram>=24,memory>=100` |

> On PowerShell, `cap list --filter` with a `>` breaks, and an unquoted `>` redirects to a file on any OS; use `capsule list --filter "..."` with the whole argument quoted.

### Exercise: Write your personal filter

Write the `capsule list --filter` expression you'd use 90% of the time for your typical workload. Save it somewhere you can paste from quickly.

## Part 5 - Core Concepts: Sessions & Claiming Machines

### Reading - There is no "lease"

Capsule has **no reservation or lease system**. You don't reserve a machine ahead of time; you simply connect to it (`capsule term`, `code`, `cursor`, `exec`, `stream`), and it's yours to use while your session is open. That makes fleet etiquette your responsibility:

- **Check before you claim.** Run `capsule list --users` first. If a machine already has an active user, pick another one; never blow away someone else's work.
- **Manage your own tunnels.** `capsule session list` shows your active SshRTC data-channel tunnels; `capsule session end` closes a specific one (by unique id, port, or session id) and `capsule session endall` closes them all: without disturbing other sessions on your machine.
- **Clean up when done.** End sessions you're no longer using so the machine is free for the next person.

## Part 6 - Hands-On: Fleet Discovery Drills

### Exercise: Inventory the fleet

 Run `capsule env show` and `capsule config customer show`, then `capsule list`. Identify available capacity by GPU class. Use `capsule list --users` to note which machines already have active users.

### Exercise: Capability filter

 Filter exercise: find every NVIDIA machine with at least 24 GB VRAM in your fleet. Express it as a single command (`capsule list --filter "vendor=nvidia,vram>=24"`). Then:

1. Connect to one with `capsule term` (or target a specific box with `-u <unique-id>`).
2. Run `nvidia-smi` to confirm the hardware matches what you filtered for.
3. When done, close the tunnel with `capsule session end` (or `capsule session endall`).

### Exercise: Pair - hardware diversity

 Each person filters for a different hardware class. Compare what's available and what's scarce.

## Part 7 - Wrap-up & Connection

**Before you finish, check each item:**

- [ ] I can run `capsule list` (with `--users`, `--json`, `--all`) and read every field.
- [ ] I can find capacity by GPU class using a `--filter` capability expression.
- [ ] I know to check `capsule list --users` before claiming a machine.
- [ ] I understand why capability-based filtering is preferable to name-based.
- [ ] I know how to list and end my sessions (`capsule session list`/`end`/`endall`).

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-07-m4-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 34 · Environments &amp; Fleet Discovery">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "In `capsule list`, what is the difference between a config tag and a unique ID?", "options": ["A config tag names a machine pool/class (the scheduler gives you any available member); a unique ID identifies one specific physical machine, targeted with `-u`/`--unique`", "A config tag is a billing code; a unique ID is a GPU serial number", "They are two names for the same thing", "A config tag only works in prod; a unique ID only works in dev"]},
  {"stem": "Why is capability-based filtering preferable to name-based filtering when selecting a machine?", "options": ["Capability filters are faster to type", "Machine names change when hardware is replaced; capability filters (`capsule list --filter \"vendor=nvidia,vram>=24\"`) find any matching machine regardless of its specific name", "Capability filters work without authentication", "Name-based filters don't work in the production environment"]},
  {"stem": "Before you start heavy work on a machine, why run `capsule list --users`?", "options": ["To renew your reservation on the machine", "To see which machines already have active user sessions, so you don't disrupt someone else's work by claiming a busy machine", "To list which users are allowed to log in to each machine", "To display the billing owner of each machine"]},
  {"stem": "What command finds NVIDIA H100-class machines in your fleet?", "options": ["`capsule node list --status available --gpu H100`", "`capsule list --filter \"vendor=nvidia,gpu=h100\"`", "`capsule find gpu --type H100 --free`", "`capsule inventory search H100`"]},
  {"stem": "How do you see the unique ID of a specific physical machine and its full specs?", "options": ["`capsule node show <id>` prints a detail page per node", "`capsule list --all` reveals per-machine unique IDs; `capsule list --json` gives full machine specs for scripting", "`capsule inspect <id>` opens an interactive inspector", "`capsule describe machine <id>` returns YAML"]},
  {"stem": "You're in the right environment but `capsule list` shows a different customer's machines. Which command changes the fleet you see?", "options": ["`capsule env set <name>`", "`capsule list --refresh`", "`capsule config customer set <name>` (and `capsule config customer unset` to clear a stray override)", "`capsule node list --customer <name>`"]},
  {"stem": "Using the `--filter` grammar, how do you list NVIDIA machines with at least 24 GB VRAM AND at least 100 GB system memory?", "options": ["`capsule list --gpu nvidia --min-vram 24 --min-mem 100`", "`capsule node list --vendor nvidia --vram 24 --memory 100`", "`capsule filter vendor=nvidia vram=24 memory=100`", "`capsule list --filter \"vendor=nvidia,vram>=24,memory>=100\"`"]},
  {"stem": "Capsule has no lease/reservation system. How do you manage and clean up your connections when you're done?", "options": ["`capsule session list` shows your active SshRTC tunnels; `capsule session end` closes one (by unique id, port, or session id) and `capsule session endall` closes them all", "`capsule lease release` returns the machine to the pool", "`capsule disconnect --all` ends every reservation", "There is nothing to clean up; sessions expire on a timer"]},
  {"stem": "On PowerShell, `cap list --filter \"vram>=24\"` misbehaves because of the `>`. What is the fix?", "options": ["`>` is never allowed in a filter on any shell; use `=` only", "Use `capsule list --filter` (not the `cap` shortener) and keep the whole filter argument quoted", "Escape it as `\\>` and run it under cmd.exe", "Switch to name-based selection; filters don't work on Windows"]}
]
</script>
</div>

### Connect forward

Tomorrow: **connecting**: once you have a lease, how to actually shell in, what the session looks like, the etiquette of multi-user nodes.

### Pre-read for tomorrow (Day 38 · Connecting to Machines)

- **Resource:** <a href="../../../readings/capsule/#connecting-to-machines">Capsule Power-User Pre-Lecture Reading - Connecting to Machines</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-5-connecting-to-machines">Capsule Lab Guide</a> Module 5.
- **Reflection questions:**
  1. What command connects you to a leased node?
  2. How does Capsule's connect differ from raw `ssh`?
  3. What state is preserved between connect sessions vs lost?

## Stuck?

Ask **oxtutor**; describe what you tried and what happened.
