# Day 36 (Fri) · Week 7 Consolidation

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 7 — Bridge: Theory Meets Tooling</a>
    <span class="sep">/</span>
    <span>Day 36 · Consolidation</span>
    {status:week-07/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Self-Study Time Buckets

| Bucket | Activity |
|---|---|
| 🔵 Bucket 1 | Knowledge Check |
| 🟢 Bucket 2 | Self-Assessment: 5-Layer Map |
| 🟡 Bucket 3 | Case Studies Review |
| 🟠 Bucket 4 | Capsule Architecture Drill |
| 🔴 Bucket 5 | Installation & Fleet Drill |
| 🟣 Bucket 6 | Open Lab & Week 8 Preview |
| **Total** | |

---

## 🔵 Bucket 1: Knowledge Check

Take the **[canonical knowledge check](knowledge-check.md)**.

This covers: agent case studies (Klarna, Claude Code, research agents), Capsule architecture (3-layer model), installation flow, authentication tokens, environments, and fleet discovery.

Aim for 80% before moving on. If you score below 70%, revisit the specific day's lesson before proceeding.

---

## 🟢 Bucket 2: Self-Assessment — 5-Layer Map

Without notes, answer each question. Score yourself honestly.

**Can you...**

- [ ] Name and define all 5 agent layers (Intelligence / Action / Governance / Orchestration / Economics) in one sentence each?
- [ ] Give a concrete example of each layer from one of the three case studies?
- [ ] Draw Capsule's 3-layer architecture (CLI → control plane → node agents) and label what each layer stores and what protocol connects adjacent layers?
- [ ] State the correct routing for your internship fleet: what environment name and customer value do you use?
- [ ] Name the 4 most common install failure modes and their fixes — recited from memory without looking at notes?

For any item you couldn't answer: write the answer out longhand (not just look it up — write it). Writing activates recall more than reading.

---

## 🟡 Bucket 3: Case Studies Review

For each of the three case studies from Day 32 (Klarna / Claude Code + Cursor / SemiAnalysis research), answer from memory:

**Klarna:**

1. What orchestration pattern did it use? (single / planner-worker / supervisor)
2. What was the key governance control? (specific, not "human review in general")
3. What was the dominant failure mode and which layer did it belong to?
4. What was the per-task cost advantage vs human agents?

**Claude Code / Cursor:**

1. What orchestration pattern?
2. What makes coding agents' environment different from customer-service agents?
3. Name three failure modes. Which layer does each belong to?

**SemiAnalysis Research Agent:**

1. What orchestration pattern?
2. What was the throughput improvement (companies screened per month)?
3. Why is the Action layer often the bottleneck for research agents, not the Intelligence layer?

Write your answers, then check against the [Day 32 lesson](../module-1/index.md).

---

## 🟠 Bucket 4: Capsule Architecture Drill

**Draw from memory:**

Draw the 3-layer Capsule architecture diagram:

```
[ CLI / client ]
        ↕  (what protocol?)
[ Control Plane ]
        ↕  (what protocol?)
[ Node Agents ]
```

For each layer, label:
- Where does it run? (user's laptop / cloud / remote machine)
- What does it store?
- What is the single most common failure mode for that layer?

**Architecture questions (answer without notes):**

1. When you run `capsule list`, which layer responds? What does it query?
2. When you run `capsule term <config-tag>`, which layers are involved in establishing the connection?
3. If the control plane is down, what can you do? What can you not do?
4. What is the relationship between a `config-tag`, a `node`, and a `machine` in Capsule's vocabulary?
5. Why does Capsule use WebRTC (SshRTC) instead of plain SSH for connections?

---

## 🔴 Bucket 5: Installation & Fleet Drill

Answer each question precisely. No notes.

1. What are the exact four GH_TOKEN scopes required for the Capsule install?
2. After `capsule auth login` succeeds, where are tokens stored on macOS? What format?
3. The access token TTL is ~60 minutes. What happens automatically when it expires? What requires you to take action?
4. Run the command: `capsule list --filter "vendor=nvidia,vram>=24"`. What does this return? If it returns nothing, name two things to check first.
5. Your colleague says "capsule status shows valid but all commands return unauthorized." What is the most likely cause? What is the diagnostic command?
6. Walk through the install verification sequence from memory: 5 commands in order, starting from `capsule --version`.

**Live drill:**

1. Run `capsule status` right now. Is your token still valid?
2. Run `capsule list` — how many machines are visible?
3. Run `capsule env show` — confirm you're in the right environment.
4. Run `capsule config customer show` — confirm the correct customer value.

If any of the above fails, treat it as a gotcha reproduction exercise and fix it using only your memory of the gotcha table.

---

## 🟣 Bucket 6: Open Lab & Week 8 Preview

**Catch up (if needed):**

- Complete any incomplete assignments from Days 32–35
- Revisit any case study you couldn't answer fully in Bucket 3
- Ask **oxtutor** to quiz you on anything from this week

**Week 8 preview:**

Week 8 covers the **operational** Capsule skills:

- Day 37: Connecting to machines (`capsule term`, `capsule code`, tmux discipline)
- Day 38: Files & storage (`capsule scp`, OneDrive mounts, storage patterns)
- Day 39: Streaming (`capsule stream`, hardware encoding, when to stream vs terminal)
- Day 40: Known quirks (the full triage decision tree, the known-quirks table, bug reports)
- Day 41 (Fri): Week 8 consolidation

These are the skills you will use every single day of the internship.

---

## Pre-read for Monday (Week 8 · Day 37 · Connecting to Machines)

- **Resource:** <a href="../../../readings/capsule/#day-38-connecting-to-machines">Capsule Power-User Pre-Lecture Reading — Day 38 section</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-5-connecting-to-machines">Capsule Lab Guide</a> Module 5 (Connecting to Machines).
- **Reflection questions:**
  1. What is the difference between `capsule term`, `capsule code`, and `capsule exec`?
  2. What does `--idle-timeout` do and when would you set it?
  3. Why is starting a tmux session immediately after connecting considered mandatory discipline?

---

## Stuck?

Ask **oxtutor** — the [Day 32 case studies lesson](../module-1/index.md) and the [Day 33 architecture lesson](../module-2/index.md) are the two highest-leverage pages of this week.
