# Widget Conversion Plan — Week 07 (Days 32–35)

**Branch:** `feat/content-fortification`  
**Pre-reading source:** `planning/source-material/Capsule Power User/Capsule-Power-User-Lab-Guide.md`  
**External source (module-1):** Klarna AI blog + coding-agent case study — no repo file. Author readiness questions from the lesson body's case study summaries.  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Pre-reading | data-source |
|--------|-----|-------|-------------|-------------|
| module-1 | 32 | Agent Case Studies | Klarna blog + coding-agent case study (no repo file — use lesson body) | `Klarna AI Blog + Coding Agent Case Studies` |
| module-2 | 33 | Capsule Foundations & Architecture | Lab Guide Modules 1+2 | `Capsule Power User Lab Guide Modules 1+2` |
| module-3 | 34 | Installation | Lab Guide Module 2 | `Capsule Power User Lab Guide Module 2` |
| module-4 | 35 | Environments & Fleet Discovery | Lab Guide Module 3 | `Capsule Power User Lab Guide Module 3` |

**Special note for module-1 (Day 32):** There is no pre-reading file in the repo for the Klarna AI blog or the coding-agent case study. Author readiness questions based on the lesson body (Parts 2–4 cover the case studies in detail). Use `data-source="Klarna AI Blog + Coding Agent Case Studies"` and note in the lesson comment that readers should have read the case study summaries provided in class.

**Special note for modules 2 and 4:** These lessons may have `## Part 1 — Pre-Reading Review` present but with static checkbox items instead of a `### Self-check` widget heading. The widget insertion replaces those static checkbox blocks entirely.

---

## module-1 — Day 32 · Agent Case Studies

**File:** `docs/lessons/week-07/module-1/index.md`  
**Pre-reading:** Klarna AI blog + coding-agent case studies (summarised in lesson body)  
**data-source label:** `Klarna AI Blog + Coding Agent Case Studies`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-07-m1-readiness` | `readiness` | `Klarna AI Blog + Coding Agent Case Studies` |
| Wrap-up | `week-07-m1-wrapup` | `wrap-up` | `Day 32 · Agent Case Studies` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Case Study: Klarna (customer service agent)
- Part 3 — Case Study: Coding Agents (Claude Code, Cursor)
- Part 4 — Case Study: Research Agents
- Part 5 — Hands-On: 5-Layer Stack Mapping
- Part 6 — Hands-On: Failure Mode Analysis
- Part 7 — Wrap-up & Connection

**Note:** Readiness questions test the pre-reading summaries that students read before class. Since there is no repo file, questions should be based on what the lesson summary text in Part 1 says the pre-reading covers. Verify against the actual lesson file before authoring.

### Readiness question outline (20 questions — case study summaries from pre-reading)
Source: The lesson body's pre-reading summary (Part 1 context paragraphs) describes
the Klarna agent deployment results, the coding agent category (Claude Code, Cursor,
Copilot), and research agent case studies. Questions test that content.

**Recall (6):**
1. What task did Klarna's AI agent replace, and what was the reported result?
2. What is the primary workflow of a coding agent like Claude Code?
3. What distinguishes a "research agent" from a "coding agent"?
4. Name two commercial coding agent products mentioned in the pre-reading
5. What metric did Klarna use to demonstrate their agent's business impact?
6. What is the "5-layer stack" framework introduced for analysing agent systems?

**Apply (8):**
7. The Klarna agent handles customer queries — classify which agent loop steps are used
8. A coding agent is asked to "add authentication to this function" — trace the first three loop steps
9. Classify a research agent that reads papers and generates a synthesis — which tools does it need?
10. Identify which layer in the 5-layer stack would handle "tool access control" for the Klarna agent
11. Select the correct description of what made Klarna's agent deployment technically feasible in 2024
12. Given the coding agent case study, identify the human-in-the-loop checkpoints
13. A research agent fails on a complex synthesis — identify the most likely failure point in the loop
14. Apply the 5-layer stack to a hypothetical "code review agent" — label each layer

**Analyse (6):**
15. Why did the Klarna deployment succeed when earlier chatbot deployments failed?
16. Compare coding agents and research agents on: autonomy level, error tolerance, and human oversight
17. What does the Klarna case study reveal about the "build vs buy" decision for agent infrastructure?
18. Why do coding agents require both generation and execution capabilities?
19. Compare the reliability requirements for a Klarna-scale customer service agent vs a coding assistant
20. A research agent produces a plausible but factually wrong synthesis — identify the root cause and mitigation

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: Klarna case study details, coding agent architecture, research
agent patterns, 5-layer stack mapping exercise, failure mode analysis.

**Recall (6):**
1. What were Klarna's reported metrics for their AI agent deployment?
2. Name the three layers that a coding agent uses (LLM, code execution, file system)
3. What is the 5-layer stack?
4. Name one common failure mode identified in the coding agent case study
5. What does a research agent's "synthesis" step require that simpler agents don't?
6. What is "human-in-the-loop" and where did it appear in the case studies?

**Apply (8):**
7. Map the Klarna agent to the 5-layer stack: LLM layer, memory layer, action layer, governance layer, integration layer
8. A coding agent fails to write tests — identify which stack layer is missing
9. Given a research agent architecture, identify the memory layer's role for a 50-paper synthesis
10. Select the correct failure mode when a coding agent has no execution environment
11. Apply failure mode analysis to the Klarna agent: identify three points where it could fail
12. Classify: "coding agent writes code but cannot run it to verify" — what is the architectural gap?
13. A team builds a research agent with no citation tracking — identify the governance failure
14. Select the correct human oversight level for a Klarna-style customer service agent in production

**Analyse (6):**
15. Why do all three case study agents rely on the same underlying agent loop despite different domains?
16. Compare the stack layers that are unique to coding agents vs research agents
17. What does the success of coding agents suggest about the importance of execution feedback in the loop?
18. Why is the Klarna case study more relevant for an "agent ROI" argument than a research agent case?
19. Compare the failure modes of tool-heavy agents vs purely generative agents using the case studies
20. A team is pitching an agent product — using the case studies, identify the two most persuasive ROI metrics

---

## module-2 — Day 33 · Capsule Foundations & Architecture

**File:** `docs/lessons/week-07/module-2/index.md`  
**Pre-reading:** Capsule Power User Lab Guide Modules 1+2  
**data-source label:** `Capsule Power User Lab Guide Modules 1+2`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-07-m2-readiness` | `readiness` | `Capsule Power User Lab Guide Modules 1+2` |
| Wrap-up | `week-07-m2-wrapup` | `wrap-up` | `Day 33 · Capsule Foundations & Architecture` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
  (may currently have static checkboxes — replace with widget)
- Part 2 — Core: Three Layers (CLI, Control Plane, Machine Layer)
- Part 3 — Core: Installation Flow
- Part 4 — Deep Dive: What Each Layer Stores
- Part 5 — Hands-On: Install & Verify
- Part 6 — Hands-On: Architecture Diagram
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Modules 1+2)
Modules 1+2 cover: what Capsule is (remote GPU access platform), the three-layer
architecture (CLI on laptop, control plane in cloud, machine layer on GPU nodes),
what each layer does, the authentication flow, what the CLI installs.

**Recall (6):**
1. What are the three layers of Capsule's architecture?
2. What does the Capsule CLI install on the user's laptop?
3. What is the "control plane" in Capsule's architecture?
4. What is the "machine layer" in Capsule?
5. What authentication method does Capsule use for the CLI?
6. What is Capsule's primary purpose — what problem does it solve?

**Apply (8):**
7. A user runs `capsule connect gpu-node-01` — which layer handles the routing?
8. Identify where user credentials are stored after `capsule auth login`
9. The CLI is installed on laptop A but not laptop B — identify what works and what doesn't on each
10. Select the correct description of what the control plane manages
11. A GPU node is unreachable — identify which layer reported this and which handles failover
12. Classify each component: `~/.capsule/`, control plane API, GPU node agent — which layer?
13. A user clears `~/.capsule/` — identify what needs to be reconfigured
14. Select the correct answer: which layer assigns GPU node leases?

**Analyse (6):**
15. Why does Capsule use a three-layer architecture instead of direct laptop-to-GPU connections?
16. Compare a direct SSH connection vs a Capsule connection — what does Capsule add and at what cost?
17. The control plane is unavailable — which Capsule operations still work and which don't?
18. Why is separating CLI from control plane important for scaling to thousands of users?
19. Compare Capsule's architecture to a VPN — what is similar and what is different?
20. A team runs Capsule for 50 engineers — at what layer does capacity planning occur?

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: three-layer architecture deep dive, installation steps and what
each creates, what the control plane stores per user, hands-on install and
verify exercise, architecture diagram exercise.

**Recall (6):**
1. Name the three Capsule layers and their locations (laptop / cloud / GPU node)
2. What does `capsule auth login` create in `~/.capsule/`?
3. What does the control plane store per user?
4. What does the machine layer's agent do continuously?
5. After a successful install, what is the command to verify the CLI works?
6. Which layer is responsible for node discovery?

**Apply (8):**
7. Draw (or describe) the data flow when a user runs `capsule list machines`
8. A user changes laptop — which Capsule components need re-setup?
9. The control plane goes down for 5 minutes — identify which operations fail and which continue
10. Identify the install verification steps the lesson prescribes
11. Select the correct description of what the architecture diagram exercise should produce
12. A new GPU node is added to the fleet — which layer registers it and how?
13. Classify: `capsule config set region=us-west` — which layer does this configure?
14. Identify what happens when `~/.capsule/auth.token` expires

**Analyse (6):**
15. Why does the three-layer architecture make Capsule more resilient than a two-layer (CLI + GPU) design?
16. Compare the security implications of token storage in `~/.capsule/` vs OS keychain
17. A team moves their control plane to a new region — what changes for users?
18. Why does Capsule's control plane need to be highly available even when GPUs are available?
19. Compare on-premise Capsule vs cloud Capsule deployments on the control plane architecture
20. The machine layer agent crashes on a node — what happens to active sessions and how does Capsule recover?

---

## module-3 — Day 34 · Installation

**File:** `docs/lessons/week-07/module-3/index.md`  
**Pre-reading:** Capsule Power User Lab Guide Module 2  
**data-source label:** `Capsule Power User Lab Guide Module 2`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-07-m3-readiness` | `readiness` | `Capsule Power User Lab Guide Module 2` |
| Wrap-up | `week-07-m3-wrapup` | `wrap-up` | `Day 34 · Installation` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: What the Install Actually Does
- Part 3 — Core: Authentication Flow
- Part 4 — Hands-On: Install on Laptop
- Part 5 — Core: Four Common Gotchas
- Part 6 — Hands-On: Gotcha Reproduction Lab
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 2)
Module 2 covers: CLI installation steps, what each step does, the authentication
flow (browser OAuth → token), the four common gotchas (wrong Python version,
PATH issues, corporate proxy, expired token).

**Recall (6):**
1. What package manager is used to install the Capsule CLI?
2. What does `capsule auth login` open in the user's browser?
3. What is stored in `~/.capsule/` after a successful install?
4. What is "Gotcha 1" in the Lab Guide's common installation issues?
5. What Python version does Capsule CLI require?
6. What does the Lab Guide say to check first when `capsule` is not found after install?

**Apply (8):**
7. A user runs `capsule` and gets "command not found" — identify the first troubleshooting step
8. After `pip install capsule-cli`, the command works in one terminal but not another — identify the cause
9. A corporate proxy blocks the OAuth callback URL — identify which gotcha this is and the fix
10. A user's auth token expires — identify the symptom and resolution
11. Classify: running `capsule auth login` on a headless server — will it work? What is the alternative?
12. Select the correct Python version check command and minimum version
13. A user installs Capsule in a venv but calls `capsule` from outside the venv — identify the issue
14. Identify the verification command that confirms a successful installation + authentication

**Analyse (6):**
15. Why does PATH configuration cause more installation failures than the actual package install step?
16. Compare installation on macOS vs Linux — what differences does the Lab Guide mention?
17. A team deploys Capsule for 30 new engineers — which two gotchas will they encounter most often?
18. Why does the corporate proxy gotcha require a different fix than just setting `HTTP_PROXY`?
19. Compare the security implications of storing the auth token in a plain file vs using OS keychain
20. A user reinstalls Capsule on a new laptop — identify what they must redo vs what transfers

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: install steps and what each creates, OAuth authentication
flow walkthrough, hands-on install exercise, four gotchas with symptoms and
fixes, gotcha reproduction lab.

**Recall (6):**
1. List the three install steps in order: install CLI → ___ → ___
2. What is the OAuth callback URL pattern used by Capsule auth?
3. Name the four gotchas from Part 5
4. What file does a successful auth write, and where?
5. What command verifies that auth succeeded?
6. What is the recommended fix for the "expired token" gotcha?

**Apply (8):**
7. Walk through the authentication flow from `capsule auth login` to ready-to-use CLI
8. Reproduce Gotcha 2 (PATH issue) on a fresh install — what commands show the problem?
9. Identify the correct fix for each gotcha: PATH, Python version, proxy, expired token
10. Select the verification checklist from the Lab Guide (4 steps post-install)
11. A user's `capsule list machines` returns "authentication required" despite previous login — gotcha?
12. Identify what the `--no-browser` flag does for `capsule auth login`
13. Calculate: if 20% of a 30-person team hit each of the 4 gotchas, how many total issues are expected?
14. Select the correct command to refresh an expired token

**Analyse (6):**
15. Why is token expiry a common production issue and how should teams manage it at scale?
16. Compare manual installation vs automated onboarding script for a 30-person team
17. A team documents that "it just works" after install — which gotchas are they underestimating?
18. Why does the proxy gotcha require a different approach on corporate vs home networks?
19. Compare the installation troubleshooting process for a developer vs a non-technical user
20. A team creates an internal installation guide — identify the top 3 things it must include based on this lesson

---

## module-4 — Day 35 · Environments & Fleet Discovery

**File:** `docs/lessons/week-07/module-4/index.md`  
**Pre-reading:** Capsule Power User Lab Guide Module 3  
**data-source label:** `Capsule Power User Lab Guide Module 3`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-07-m4-readiness` | `readiness` | `Capsule Power User Lab Guide Module 3` |
| Wrap-up | `week-07-m4-wrapup` | `wrap-up` | `Day 35 · Environments & Fleet Discovery` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
  (may currently have static checkboxes — replace with widget)
- Part 2 — Core: Environments & Discovery Commands
- Part 3 — Core: Node Anatomy & Status Fields
- Part 4 — Deep Dive: Capability-Based Filtering
- Part 5 — Core: Leases
- Part 6 — Hands-On: Fleet Discovery Drills
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 3)
Module 3 covers: what an "environment" is in Capsule, `capsule list machines`,
node status fields (available/leased/offline), GPU type and capability fields,
filtering syntax, what a "lease" is.

**Recall (6):**
1. What is a "Capsule environment"?
2. What command lists available machines in a Capsule environment?
3. What are the three node status values?
4. What does a "lease" mean in Capsule?
5. What CLI flag filters machines by GPU type?
6. What does the "available" status mean for a Capsule node?

**Apply (8):**
7. Run `capsule list machines --gpu-type h100` — what does this return?
8. A node shows status "leased" — can you connect to it? What does this mean?
9. Identify the command to list only available machines with 80GB VRAM
10. Select the correct interpretation of a node's `capabilities.gpu.memory_gb` field
11. A team needs an H100 node for 4 hours — identify the correct Capsule operation
12. Classify: a node in "offline" state — is it temporarily unavailable or permanently removed?
13. Given 5 nodes in an environment, 2 leased and 1 offline — how many are available?
14. Select the correct command to request a specific node by unique_id

**Analyse (6):**
15. Why does Capsule use leases rather than simple on/off reservations?
16. Compare a capability-based filter vs a name-based filter for fleet discovery — which is more robust?
17. A team frequently can't find available H100 nodes — what does this indicate about fleet utilisation?
18. Why is it important to filter by capability rather than by node name in a fleet of heterogeneous hardware?
19. Compare the fleet discovery experience in Capsule vs traditional SSH-based cluster access
20. A team's automation script uses hardcoded node names — identify the risk and the correct approach

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: environment concept, `capsule list machines` output fields,
node status states and transitions, capability fields and filtering, lease
mechanics, fleet discovery drill exercises.

**Recall (6):**
1. List the fields in a `capsule list machines` output row
2. What does node status transition from "available" to "leased" require?
3. What is the lease duration default in Capsule?
4. What does `--status available` filter for in `capsule list machines`?
5. Name three capability fields that can be used for filtering
6. What command extends an existing lease?

**Apply (8):**
7. Write the `capsule list machines` command to find available A100 nodes with ≥40GB VRAM
8. A lease expires — what happens to the active session?
9. Given a fleet discovery output, identify the correct node for a 70B FP16 inference task (needs ≥140GB VRAM)
10. Select the correct command to list all nodes regardless of status
11. A team's script should always pick the least-loaded available node — identify the filter approach
12. Identify what `capsule lease extend --node gpu-01 --duration 2h` does
13. Classify: filtering by `capabilities.gpu.type=a100` vs `name=gpu-node-07` — which is capability-based?
14. Calculate: 10-node fleet, 30% leased, 10% offline — how many nodes are available?

**Analyse (6):**
15. Why does Capsule expose capability fields rather than just listing GPU model names?
16. Compare fleet discovery in a homogeneous cluster (all same GPU) vs heterogeneous fleet
17. A team's automation always requests the same node by name — what failure scenario does this create?
18. Why does lease management matter more for shared fleets than for dedicated single-user GPUs?
19. Compare the fleet discovery UX of `capsule list machines` vs a web dashboard — trade-offs?
20. A team runs out of available H100 nodes during a deadline crunch — identify three actions they can take

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Read Lab Guide Modules 1, 2, 3 from `Capsule-Power-User-Lab-Guide.md`
- [ ] module-1 (Day 32): Verify lesson body contains case study summaries for readiness Qs
- [ ] module-1: readiness from lesson body + case study wrap-up
- [ ] module-2 (Day 33): Check for static checkbox block in Part 1 → replace with widget
- [ ] module-2: Lab Guide M1+M2 readiness + architecture wrap-up
- [ ] module-3 (Day 34): Lab Guide M2 readiness + installation wrap-up
- [ ] module-4 (Day 35): Check for static checkbox block in Part 1 → replace with widget
- [ ] module-4: Lab Guide M3 readiness + fleet discovery wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`
- [ ] After all 4 modules: `python3 scripts/audit_lessons.py` — 0 violations
