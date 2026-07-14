# Day 40 (Fri) · Week 8 Consolidation

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 8 - Capsule: Connections &amp; Operations</a>
    <span class="sep">/</span>
    <span>Day 40 · Consolidation</span>
    {status:week-08/module-5}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## Self-Study Time Buckets

| Bucket | Activity |
|---|---|
| 🔵 Bucket 1 | Knowledge Check |
| 🟢 Bucket 2 | Self-Assessment Checklist |
| 🟡 Bucket 3 | Connection Drills |
| 🟠 Bucket 4 | Files & Storage Drills |
| 🔴 Bucket 5 | Known Quirks & Bug Report Drill |
| 🟣 Bucket 6 | Open Lab & Week 9 Preview |
| **Total** | |

---

## 🔵 Bucket 1: Knowledge Check

Take the **[canonical knowledge check](knowledge-check.md)**.

This covers: connecting to machines (`capsule term` / `capsule code` / `capsule exec`), files & storage mechanisms, streaming (architecture, hardware encoding, when to stream), and known quirks (triage tree, quirks table, bug-report rubric).

Aim for 80% before moving on. For any topic below 60%: revisit the specific day's lesson before the drill buckets.

---

## 🟢 Bucket 2: Self-Assessment Checklist

Without notes, answer each question. Write your answers before looking anything up.

**Can you...**

- [ ] Explain what `capsule term` does that raw SSH doesn't: name at least 3 differences?
- [ ] State the first command you run after `capsule term` and explain exactly why (what problem does it solve)?
- [ ] Name the three file-transfer mechanisms and give the correct scenario for each?
- [ ] Recite all 8 rows of the known-quirks table from memory: symptom and fix?
- [ ] Name all 8 fields of a proper bug report in order?
- [ ] Walk through the 4-step triage decision tree from memory?
- [ ] Explain what `capsule session endall` does and does NOT affect?
- [ ] Describe the hardware encoding pipeline: GPU → encoder → WebRTC → client?

For any unchecked item: write the answer out longhand, then return to the source lesson to verify.

---

## 🟡 Bucket 3: Connection Drills

Work through these exercises with your actual dev node. Each exercise tests a skill from Days 36–37.

**Drill 1 - tmux persistence:**

1. `capsule term <config-tag>` - connect to a dev node.
2. Start a new tmux session: `tmux new -s drill`
3. In a tmux pane, run a long command: `find / 2>/dev/null | wc -l`
4. Detach from tmux: `Ctrl+B, D`
5. Disconnect from capsule: type `exit`
6. Reconnect: `capsule term <config-tag>` → `tmux attach -t drill`
7. Confirm the `find` command is still running or has completed.

If the command was still running when you detached and reconnected, your tmux persistence is working correctly. This is the core of the "never lose work" discipline.

**Drill 2 - port forward test:**

1. On the remote node, start an HTTP server: `python3 -m http.server 8001 &`
2. In a second local terminal, open a session with a forwarded port: `capsule term <config-tag> --direct --options "-L 8001:localhost:8001"`
3. Open `http://localhost:8001` in your local browser. Confirm you see the remote directory listing.
4. Exit that capsule session. Confirm the tunnel drops (browser should fail to load).

**Drill 3 - triage decision tree:**

Speak the 4-step triage decision tree aloud, from memory:
- Step 1: ___
- Step 2: ___
- Step 3: ___
- Step 4: ___

For each step, say what failure mode it catches.

---

## 🟠 Bucket 4: Files & Storage Drills

**Drill 1 - scp round-trip:**

1. Create a 1 MB test file locally: `dd if=/dev/urandom of=/tmp/test1mb.bin bs=1024 count=1024`
2. Upload: `capsule scp upload /tmp/test1mb.bin <config-tag>:/tmp/test1mb.bin`
3. Download: `capsule scp download <config-tag>:/tmp/test1mb.bin /tmp/test1mb-downloaded.bin`
4. Verify checksums match: `md5sum /tmp/test1mb.bin /tmp/test1mb-downloaded.bin`

If checksums match, your scp workflow is working correctly.

**Drill 2 - OneDrive persistence:**

1. On the remote node, write a test file to your OneDrive-mounted directory: `echo "test content $(date)" > ~/OneDrive/capsule-drill-test.txt`
2. Disconnect from that node.
3. Connect to a *different* node in the same environment.
4. Read the file: `cat ~/OneDrive/capsule-drill-test.txt`
5. Confirm the content is identical.

This confirms your OneDrive mount is working as shared persistent storage across machines.

**Drill 3 - Storage mechanism selection:**

For each scenario, name the correct mechanism and explain why:

| Scenario | Correct mechanism | Why |
|---|---|---|
| 50 GB model checkpoint shared across 3 nodes | | |
| Your `.gitconfig` and shell aliases | | |
| Temporary intermediate results during a 1-hour job | | |
| Output you want to access from any machine permanently | | |

---

## 🔴 Bucket 5: Known Quirks & Bug Report Drill

**Drill 1 - Quirks recall:**

Cover the known-quirks table. From memory, name the fix for each of these 4 symptoms:

1. "My `capsule list` is showing a completely different set of machines."
2. "VS Code Remote-SSH is failing with config parsing errors."
3. "`capsule update` is failing even though I'm logged in."
4. "The browser auth flow didn't complete; it just hung."

Write the fix for each. Then check against the [Day 39 known-quirks table](../module-4/index.md).

**Drill 2 - Bug report:**

Write a complete bug report (all 8 fields) for the following scenario:

> "You ran `capsule term <config-tag>` at 14:32 UTC. The command printed 'connecting...' and then hung for 60 seconds, then exited with no error message. You are on a dev node with unique ID `NV-3060-04-1`. You tried `capsule session endall` before the connection attempt. Your env is `development`. Your customer is set correctly."

Fill in all 8 fields. For any field you can't fill in from the scenario description (e.g. `capsule --version`), write exactly what command you would run to get it.

After writing: apply the **specificity test**: could a support engineer reproduce your issue from this report without asking any follow-up questions? If not, identify which field is too vague.

---

## 🟣 Bucket 6: Open Lab & Week 9 Preview

**Catch up (if needed):**

- Complete any incomplete assignments from Days 36–39
- Retry any drill from Buckets 3–5 that you couldn't complete
- Ask **oxtutor** to quiz you on anything from this week

**Week 9 preview:**

Week 9 covers **Benchmarking & Reliability**: the most important operational track for the internship:

- Day 41: Your First Benchmark (`capsule benchmark`, InferenceMAX, the four backend options)
- Day 42: Reading Benchmark Results (latency/throughput tradeoffs, GPU efficiency metrics)
- Day 43: Reliability Engineering (failure modes in multi-step inference, SLA design)
- Day 44 (Fri): Week 9 Consolidation

Module 8 of the Lab Guide (Benchmarking) is the most important module for this track. Read it carefully before Monday.

---

## Pre-read for Monday (Week 9 · Day 41 · Your First Benchmark)

- **Resource:** <a href="../../../readings/capsule/#your-first-benchmark">Capsule Power-User Pre-Lecture Reading - Your First Benchmark</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-8-model-evaluation-benchmarking-the-inferencemax-path">Capsule Lab Guide</a> Module 8 (Benchmarking): budget the full 30 minutes.
- **Reflection questions:**
  1. What is **InferenceMAX** and what does it measure?
  2. What are the four backend options for `capsule benchmark`?
  3. What does `--concurrency` mean in the context of a benchmark run?

---

## Stuck?

Ask **oxtutor**; the [Day 39 known-quirks lesson](../module-4/index.md) is the single highest-leverage page for daily Capsule operation.
