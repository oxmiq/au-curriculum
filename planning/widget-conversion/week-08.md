# Widget Conversion Plan — Week 08 (Days 37–40)

**Branch:** `feat/content-fortification`  
**Pre-reading source:** `planning/source-material/Capsule Power User/Capsule-Power-User-Lab-Guide.md`  
**Lab Guide modules used:** Module 5 (Day 37), Modules 6+7 (Day 38), Module 7 (Day 39), Module 10 (Day 40)  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Lab Guide module | data-source |
|--------|-----|-------|-----------------|-------------|
| module-1 | 37 | Connecting to Machines | Module 5 | `Capsule Power User Lab Guide Module 5` |
| module-2 | 38 | Files & Storage | Modules 6+7 | `Capsule Power User Lab Guide Modules 6+7` |
| module-3 | 39 | Streaming | Module 7 | `Capsule Power User Lab Guide Module 7` |
| module-4 | 40 | Known Quirks | Module 10 | `Capsule Power User Lab Guide Module 10` |

All four lessons have `## Part 1 — Pre-Reading Review`. No structural changes needed.

---

## module-1 — Day 37 · Connecting to Machines

**File:** `docs/lessons/week-08/module-1/index.md`  
**Pre-reading:** Lab Guide Module 5 — The Connect Command and Session Management  
**data-source label:** `Capsule Power User Lab Guide Module 5`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-08-m1-readiness` | `readiness` | `Capsule Power User Lab Guide Module 5` |
| Wrap-up | `week-08-m1-wrapup` | `wrap-up` | `Day 37 · Connecting to Machines` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: The Connect Command
- Part 3 — Core: Session State & What Persists
- Part 4 — Deep Dive: tmux for Reliable Sessions
- Part 5 — Hands-On: Connect Detach Reconnect
- Part 6 — Hands-On: Tunneling & Multi-User Etiquette
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 5)
Module 5 covers: `capsule connect`, what a session is, what persists across
disconnect/reconnect, tmux for session persistence, tunneling for port
forwarding, multi-user etiquette on shared nodes.

**Recall (6):**
1. What command connects to a Capsule machine?
2. What is a "session" in the context of `capsule connect`?
3. What persists between disconnect and reconnect on a Capsule machine?
4. What is tmux and why does the Lab Guide recommend it?
5. What is "port forwarding" in a Capsule connection?
6. What does "multi-user etiquette" mean when sharing a Capsule node?

**Apply (8):**
7. A user connects to a node, starts a training job, then disconnects — does the job continue?
8. Identify the command to reconnect to an existing session after network interruption
9. A user wants to run a Jupyter notebook accessible from their laptop — what Capsule feature helps?
10. Select the correct tmux command to create a new named session and detach from it
11. A GPU node has 3 concurrent users — identify the etiquette rule for starting a heavy compute job
12. Classify: closing the terminal vs `capsule disconnect` — which terminates the session?
13. A user's `capsule connect` fails with "no available lease" — identify the cause
14. Select the correct approach for a long-running job that must survive a laptop going to sleep

**Analyse (6):**
15. Why is tmux necessary for long-running jobs even when using Capsule session persistence?
16. Compare direct SSH with `capsule connect` — what does Capsule add to the session lifecycle?
17. A team of 5 shares a single H100 node — what coordination mechanism prevents resource contention?
18. Why does port forwarding enable a richer local development workflow on remote GPU nodes?
19. Compare detach/reattach patterns in tmux vs screen — what does the lesson recommend and why?
20. A user reports their training job "disappeared" after network loss — diagnose the failure

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: `capsule connect` mechanics, session state map (what persists:
processes, files, environment; what doesn't: terminal output), tmux session
workflow, connect-detach-reconnect exercise, tunneling setup, etiquette rules.

**Recall (6):**
1. What persists in a Capsule session after disconnect?
2. What does NOT persist (is lost) after disconnect?
3. What is the tmux command to detach from a session?
4. What is the `capsule connect --tunnel` flag used for?
5. Name two etiquette rules for shared GPU nodes
6. What does `capsule session list` show?

**Apply (8):**
7. Write the sequence of commands to: connect → start tmux → run training → detach → reconnect → reattach
8. A user wants to access port 8888 (Jupyter) from their laptop via Capsule — write the connect command with tunneling
9. Identify which session state component a team member must NOT rely on persisting
10. Given a shared 8-GPU node, identify the correct way to check current GPU utilisation before starting a job
11. Select the correct troubleshooting step when `capsule connect` hangs at "establishing connection"
12. A user's tmux session list is empty after reconnect — identify what went wrong
13. Apply etiquette rules: is it acceptable to run a 72-hour training job on a shared node without notifying teammates?
14. Identify the command to see active sessions on a Capsule node

**Analyse (6):**
15. Why does Capsule session persistence not replace the need for tmux for long-running jobs?
16. Compare the reliability of a local training job vs a remote Capsule session job — what risks differ?
17. A team's policy is "all jobs must run in tmux" — analyse why this policy exists
18. Why is port forwarding more secure than exposing the GPU node's port directly to the internet?
19. A team has 10 engineers sharing 2 GPU nodes — design an etiquette policy for fair use
20. Compare the session lifecycle of `capsule connect` vs a traditional SLURM job — what is different?

---

## module-2 — Day 38 · Files & Storage

**File:** `docs/lessons/week-08/module-2/index.md`  
**Pre-reading:** Lab Guide Modules 6+7 — File Transfer and Storage Scopes  
**data-source label:** `Capsule Power User Lab Guide Modules 6+7`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-08-m2-readiness` | `readiness` | `Capsule Power User Lab Guide Modules 6+7` |
| Wrap-up | `week-08-m2-wrapup` | `wrap-up` | `Day 38 · Files & Storage` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: Three Transfer Mechanisms (capsule cp, rsync, mounted storage)
- Part 3 — Core: Storage Scopes (local node vs shared storage vs persistent volumes)
- Part 4 — Deep Dive: Shared Storage Workflow
- Part 5 — Hands-On: Upload/Download Drill
- Part 6 — Hands-On: Streaming & Daily Rhythm
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Modules 6+7)
Modules 6+7 cover: three mechanisms for file transfer (`capsule cp`, rsync,
mounted storage), storage scope types (local/node-ephemeral, shared/team,
persistent volume), when to use each, daily rhythm for data management.

**Recall (6):**
1. What are the three file transfer mechanisms in Capsule?
2. What is the difference between local node storage and shared storage in Capsule?
3. What is a "persistent volume" in Capsule?
4. What does `capsule cp` do?
5. When should you use rsync instead of `capsule cp`?
6. What is "node-ephemeral" storage and what happens to it when a lease ends?

**Apply (8):**
7. A user wants to transfer a 50GB dataset to a GPU node before training — which mechanism?
8. Identify the correct storage scope for: results that must survive lease expiry
9. Two team members need to share a preprocessed dataset on the same Capsule fleet — which storage?
10. Select the correct rsync flag for incremental sync of a large directory
11. A user's trained model weights are stored in node-ephemeral storage — what happens at lease end?
12. Classify each storage type: node-ephemeral, shared storage, persistent volume — by: survives lease? shared across users?
13. Identify the correct `capsule cp` command syntax for uploading a local file to a node
14. A team's workflow requires checkpointing every 30 min — which storage type is most appropriate?

**Analyse (6):**
15. Why does using node-ephemeral storage for checkpoints create a data loss risk?
16. Compare `capsule cp` and rsync for a 200GB dataset — what trade-offs determine the choice?
17. A team stores all training outputs in shared storage — identify the naming convention problem
18. Why is a "daily rhythm" for data management important in a shared Capsule environment?
19. Compare persistent volumes and shared storage — when would you choose one over the other?
20. A user's training job outputs 1TB of data to node-ephemeral storage — identify the recovery plan if the lease expires

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: three mechanisms with use cases, storage scope comparison
table, shared storage workflow (mount, write, unmount), upload/download drill
exercise, daily rhythm checklist.

**Recall (6):**
1. Which transfer mechanism is best for large incremental syncs?
2. What is the `capsule cp` upload syntax?
3. What storage scope survives fleet restarts?
4. Name two naming convention rules for shared storage
5. What does the daily rhythm checklist in Part 6 include?
6. What is the maximum file size recommendation for `capsule cp` vs rsync?

**Apply (8):**
7. Upload a local `./data/` directory to `/workspace/data/` on node `gpu-01` — write the `capsule cp` command
8. An rsync command to sync `./results/` to `gpu-01:/shared/my-results/` incrementally — write it
9. Given a shared storage path `/shared/team/`, apply naming conventions for a new experiment
10. Identify which files belong in node-ephemeral vs persistent storage for a training workflow
11. Apply the daily rhythm checklist to a day's workflow: morning prep, during training, end of day cleanup
12. Select the correct storage type for: intermediate training artifacts, final model weights, shared datasets
13. A team member accidentally writes to `/shared/` without a namespace prefix — identify the impact
14. Calculate: daily rsync of 5GB delta at 100 MB/s — how long does the morning sync take?

**Analyse (6):**
15. Why does the three-scope storage model exist rather than a single unified storage?
16. Compare the I/O performance of node-ephemeral storage vs shared storage for training checkpoints
17. A team adopts a "everything in shared storage" policy — identify the performance and cost risks
18. Why do naming conventions matter more in shared storage than in single-user storage?
19. Compare Capsule's storage model to S3 + local SSD in a cloud training setup — what is analogous?
20. A team's daily rhythm breaks down under a deadline crunch — identify the data risks that accumulate

---

## module-3 — Day 39 · Streaming

**File:** `docs/lessons/week-08/module-3/index.md`  
**Pre-reading:** Lab Guide Module 7 — Desktop and App Streaming  
**data-source label:** `Capsule Power User Lab Guide Module 7`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-08-m3-readiness` | `readiness` | `Capsule Power User Lab Guide Module 7` |
| Wrap-up | `week-08-m3-wrapup` | `wrap-up` | `Day 39 · Streaming` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: Streaming Architecture (how Capsule streams desktop/apps)
- Part 3 — Core: When to Stream vs Terminal/Exec
- Part 4 — Hands-On: Launch Desktop Stream
- Part 5 — Hands-On: App Streaming & Containers
- Part 6 — Core: Network Sensitivity & Failure Modes
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 7)
Module 7 covers: what Capsule streaming is, how it differs from terminal access,
when you need it (GUI apps, graphical output), the stream command, container
streaming, network latency sensitivity, common streaming failure modes.

**Recall (6):**
1. What is Capsule streaming?
2. When is streaming needed vs terminal/SSH access?
3. What command launches a desktop stream in Capsule?
4. What is "container streaming" in Capsule?
5. What network condition most degrades streaming quality?
6. What is the recommended minimum bandwidth for a smooth Capsule desktop stream?

**Apply (8):**
7. A user needs to run a GUI-based tool on a GPU node — which Capsule access method?
8. Identify the command to launch a desktop stream on node `gpu-01`
9. A user's stream shows high latency on a 100 Mbps connection — identify the first diagnostic step
10. Select the correct use case for container streaming vs direct desktop streaming
11. A team member in a different country reports poor stream quality — identify the likely cause
12. Classify: training a model (no GUI needed) vs debugging with a visual profiler — stream or terminal?
13. Identify what happens to the stream when network drops for 5 seconds
14. Select the correct codec setting recommendation for a high-latency connection

**Analyse (6):**
15. Why does streaming add latency overhead that terminal access does not?
16. Compare the bandwidth requirements of desktop streaming vs a training job's GPU-to-CPU data transfer
17. A team uses streaming for all workflows including purely terminal tasks — what inefficiency does this create?
18. Why does streaming quality degrade non-linearly with network latency?
19. Compare Capsule streaming to VNC/RDP — what does Capsule's approach add?
20. A team reports that streaming works for 15 minutes then degrades — identify likely streaming failure modes

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: streaming architecture overview, stream vs terminal decision
matrix, launch desktop stream walkthrough, container streaming setup, network
sensitivity analysis and failure mode catalogue.

**Recall (6):**
1. Name two use cases where streaming is required vs terminal-only
2. What command launches an app stream (specific application) rather than full desktop?
3. What does the streaming codec affect in the user experience?
4. Name two streaming failure modes from Part 6
5. What is the latency threshold beyond which streaming becomes unusable?
6. What is the recommended approach when streaming is unavailable due to network issues?

**Apply (8):**
7. A user wants to stream a specific app (e.g., a visual debugger) rather than a full desktop — write the command
8. Given network latency = 150ms, classify: is this suitable for interactive streaming?
9. Identify the troubleshooting sequence when a stream connection is established but the image freezes
10. Select the correct fallback when streaming quality is too low for productive work
11. A container has a GUI app — identify the steps to stream it via Capsule
12. Apply the decision matrix to classify each workflow: bash script, Python training, visual profiler, model output viewer
13. A user reports "black screen" after stream launch — identify the first two diagnostic steps
14. Select the correct network diagnostic command to measure latency to the Capsule streaming endpoint

**Analyse (6):**
15. Why is interactive streaming latency-sensitive in a way that bulk file transfer is not?
16. Compare the user experience of 50ms vs 200ms round-trip latency for a streaming session
17. A team mandates "use streaming only when GUI is required" — analyse the impact on GPU node load
18. Why does container streaming add complexity vs direct desktop streaming?
19. Compare Capsule streaming and X11 forwarding — what does Capsule improve?
20. A team in Mumbai streams to US-West GPU nodes — identify the root problem and two solutions

---

## module-4 — Day 40 · Known Quirks

**File:** `docs/lessons/week-08/module-4/index.md`  
**Pre-reading:** Lab Guide Module 10 — Known Quirks and Troubleshooting  
**data-source label:** `Capsule Power User Lab Guide Module 10`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-08-m4-readiness` | `readiness` | `Capsule Power User Lab Guide Module 10` |
| Wrap-up | `week-08-m4-wrapup` | `wrap-up` | `Day 40 · Known Quirks` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: Triage Decision Tree
- Part 3 — Deep Dive: Known-Quirks Table
- Part 4 — Core: Bug-Report Rubric
- Part 5 — Hands-On: Reproduce Three Quirks
- Part 6 — Hands-On: File a Proper Bug Report
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 10)
Module 10 covers: the known quirks table (specific reproducible issues with
workarounds), the triage decision tree (is this a bug vs user error), the
bug-report rubric (reproduction steps, environment info, expected vs actual),
how to escalate issues.

**Recall (6):**
1. What is the "triage decision tree" in Lab Guide Module 10?
2. What are the three components of a good bug report per the Lab Guide?
3. Name two known quirks listed in the Lab Guide
4. What is the first triage question when something doesn't work?
5. What environment information is required in a bug report?
6. What is the escalation path when a workaround doesn't fix a known quirk?

**Apply (8):**
7. A user reports "capsule connect is slow" — apply the triage decision tree to classify it
8. Write a bug report for: `capsule list machines` returns empty list on a fleet with 10 nodes
9. Identify which known quirk applies when streaming works but audio is missing
10. Select the correct workaround for the "auth token refresh loop" known quirk
11. A user encounters an error not in the known-quirks table — what does the triage tree say?
12. Classify: "capsule cp fails for files >2GB" — known quirk or user error?
13. Identify what "reproduction steps" must include per the bug-report rubric
14. Select the correct first step when a known quirk's workaround fails

**Analyse (6):**
15. Why does a structured triage decision tree reduce time-to-resolution compared to free-form troubleshooting?
16. Compare a bug report with and without reproduction steps — which gets resolved faster and why?
17. A team has 10 engineers all hitting the same quirk but filing different bug reports — what coordination failure is this?
18. Why does the known-quirks table need to be a living document rather than a one-time reference?
19. Compare the value of a workaround vs a root-cause fix — when should each be prioritised?
20. A team never encounters known quirks because they only use basic features — identify the risk of this over time

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: triage decision tree walkthrough, known-quirks table deep
dive (at least 5 specific quirks with symptoms and workarounds), bug-report
rubric, reproduction exercise for three quirks, full bug report filing exercise.

**Recall (6):**
1. Draw (or describe) the triage decision tree from Part 2
2. Name three known quirks from the Part 3 table with their symptoms and workarounds
3. What are the six fields in the bug-report rubric?
4. What does "expected vs actual" mean in a bug report?
5. What information should the "environment" section of a bug report include?
6. What is the one question that separates "known quirk" from "new bug"?

**Apply (8):**
7. Apply the triage tree to: "capsule stream launches but desktop is black"
8. Write a complete bug report for one of the three quirks you reproduced in Part 5
9. Identify the correct workaround for the known quirk: "lease expires 10 minutes early"
10. Select the correct escalation action when the known-quirks table has no match
11. Given a minimal bug report (title only), identify what is missing per the rubric
12. A team uses a shared Slack channel to report bugs informally — identify what the rubric adds
13. Apply the quirk table to classify: "streaming disconnects every ~20 minutes on corporate Wi-Fi"
14. Identify the reproduction rate (100%/intermittent/rare) for each of the three reproduced quirks

**Analyse (6):**
15. Why is reproducing a quirk before filing a report more valuable than filing immediately?
16. Compare a team that keeps a private quirks log vs one that contributes to the Lab Guide — what diverges?
17. A bug is intermittent — apply the rubric to identify what additional information makes it useful
18. Why do structured bug reports reduce "noise" in the issue tracker compared to informal reports?
19. Compare the triage process for a new user vs an experienced user — where do mistakes occur?
20. A team encounters a critical quirk blocking a deadline — apply the triage tree and identify the fastest path to resolution

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Read Lab Guide Modules 5, 6, 7, 10 from `Capsule-Power-User-Lab-Guide.md`
- [ ] module-1 (Day 37): Lab Guide M5 readiness + connecting/sessions wrap-up
- [ ] module-2 (Day 38): Lab Guide M6+M7 readiness + files & storage wrap-up
- [ ] module-3 (Day 39): Lab Guide M7 readiness + streaming wrap-up
- [ ] module-4 (Day 40): Lab Guide M10 readiness + known quirks wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`
- [ ] After all 4 modules: `python3 scripts/audit_lessons.py` — 0 violations
