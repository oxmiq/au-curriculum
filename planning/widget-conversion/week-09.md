# Widget Conversion Plan — Week 09 (Days 42–45)

**Branch:** `feat/content-fortification`  
**Pre-reading source:** `planning/source-material/Capsule Power User/Capsule-Power-User-Lab-Guide.md`  
**Lab Guide modules used:** Module 8 (Day 42), none new (Day 43 recalls Day 42), Module 9 (Day 44), Module 10 (Day 45)  
**Commit message pattern:**
`feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`

---

## Week overview

| Module | Day | Title | Pre-reading | data-source | Special |
|--------|-----|-------|-------------|-------------|---------|
| module-1 | 42 | Your First Benchmark | Lab Guide Module 8 | `Capsule Power User Lab Guide Module 8` | — |
| module-2 | 43 | Model Evaluation (Varying Parameters) | Day 42 content recall — no new reading | `Day 42 · Your First Benchmark` | Readiness tests Day 42 material |
| module-3 | 44 | Interactive Chat (Quality Evaluation) | Lab Guide Module 9 | `Capsule Power User Lab Guide Module 9` | — |
| module-4 | 45 | Scheduling & MCP | Lab Guide Module 10 | `Capsule Power User Lab Guide Module 10` | — |

**Note on module-2 (Day 43):** There is no new pre-reading for this lesson. The pre-reading section (Part 1 Readiness) tests whether students retained and can apply Day 42 content (benchmarking fundamentals). Use `data-source="Day 42 · Your First Benchmark"` and make the readiness questions recall+apply on Day 42 material. The widget is still labelled `data-kind="readiness"` because it gates entry to new content (varying parameters) by confirming Day 42 is solid.

All four lessons have `## Part 1 — Pre-Reading Review`. No structural changes needed.

---

## module-1 — Day 42 · Your First Benchmark

**File:** `docs/lessons/week-09/module-1/index.md`  
**Pre-reading:** Lab Guide Module 8 — Running Your First Benchmark  
**data-source label:** `Capsule Power User Lab Guide Module 8`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-09-m1-readiness` | `readiness` | `Capsule Power User Lab Guide Module 8` |
| Wrap-up | `week-09-m1-wrapup` | `wrap-up` | `Day 42 · Your First Benchmark` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: Benchmark Anatomy (what a Capsule benchmark measures and reports)
- Part 3 — Core: Reading the Report (output fields, units, what each means)
- Part 4 — Deep Dive: What One Benchmark Proves (and what it doesn't)
- Part 5 — Hands-On: Run First Benchmark
- Part 6 — Hands-On: Annotate & Defend
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 8)
Module 8 covers: what the Capsule benchmarking tool does, what the benchmark
measures (TTFT, ITL, throughput at a given concurrency), what the output report
contains, how to run the benchmark command.

**Recall (6):**
1. What does the Capsule benchmark tool measure?
2. Name three metrics that appear in a Capsule benchmark report
3. What is "concurrency" in the context of a benchmark?
4. What command runs the Capsule benchmark?
5. What is the default number of requests the benchmark sends?
6. What does "warm-up" mean in the benchmarking context?

**Apply (8):**
7. Identify what changes between a benchmark run at concurrency=1 and concurrency=8
8. A benchmark report shows TTFT p99=800ms — is this within a typical production SLO?
9. Select the correct interpretation of "throughput: 45 tokens/sec" in a benchmark report
10. Identify which benchmark parameter to change to simulate 10 simultaneous users
11. A benchmark warm-up phase is skipped — identify how this affects the results
12. Classify: benchmark TTFT vs measured TTFT for a single user — which is typically higher?
13. Identify what the "requests_sent" and "requests_failed" fields in the report indicate
14. Select the correct flag to run the benchmark against a non-default model endpoint

**Analyse (6):**
15. Why does a single-concurrency benchmark not predict multi-user production performance?
16. Compare a warm benchmark (GPU cache hot) vs cold benchmark — which reflects production better?
17. A benchmark shows excellent TTFT but poor throughput — what does this indicate about the system?
18. Why is p99 TTFT a more useful benchmark metric than mean TTFT?
19. A team runs a 30-second benchmark and a 5-minute benchmark on the same system — which is more reliable?
20. A benchmark is run at 2am on a shared node with no other users — identify the representativeness issue

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: benchmark anatomy (what it sends and measures), report field
glossary, "what a benchmark proves" analysis (one config at one concurrency),
hands-on benchmark run, annotate-and-defend exercise.

**Recall (6):**
1. Name all output fields in a Capsule benchmark report
2. What does "requests_per_second" measure in the report?
3. What is the benchmark's default prompt template?
4. What does "annotate and defend" mean in Part 6?
5. What limitation is stated in Part 4 about what one benchmark proves?
6. What flag changes the output token count in the benchmark?

**Apply (8):**
7. Run a benchmark at concurrency=4 for 60 seconds — write the command
8. Given a report: TTFT p50=120ms, p99=650ms — interpret the tail behaviour
9. Identify what "defend your numbers" means in the Part 6 exercise
10. A benchmark returns 0 failed requests — is this always good? Identify the edge case
11. Select the correct next step after a benchmark shows TTFT p99 > 1000ms
12. Identify what the benchmark does NOT measure (quality, accuracy, cost)
13. A team uses the benchmark output as their SLA — identify what is missing
14. Calculate: benchmark duration 120s, requests_sent=240, success_rate=95% — how many failed?

**Analyse (6):**
15. Why does a single benchmark run at one concurrency tell an incomplete performance story?
16. Compare benchmark results on an idle GPU node vs a fully-loaded node — what changes?
17. A team treats benchmark throughput as their production throughput — identify the assumption error
18. Why does the "defend your numbers" exercise prepare students for production performance reviews?
19. Compare a micro-benchmark (single operation) vs the Capsule end-to-end benchmark — what each reveals
20. A team's benchmark shows different results each run — identify three sources of variance

---

## module-2 — Day 43 · Model Evaluation (Varying Parameters)

**File:** `docs/lessons/week-09/module-2/index.md`  
**Pre-reading:** Day 42 content (no new Lab Guide reading — this lesson extends Day 42)  
**data-source label:** `Day 42 · Your First Benchmark`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-09-m2-readiness` | `readiness` | `Day 42 · Your First Benchmark` |
| Wrap-up | `week-09-m2-wrapup` | `wrap-up` | `Day 43 · Model Evaluation (Varying Parameters)` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
  (tests Day 42 recall — no new pre-reading)
- Part 2 — Core: The Sweep Template
- Part 3 — Core: Expected Shapes & Phase-1 Recall
- Part 4 — Deep Dive: Saturation Curves & Regimes
- Part 5 — Hands-On: Predict Then Run Sweep
- Part 6 — Hands-On: Reconcile Predictions
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Day 42 recall)
Day 42 covered: benchmark anatomy, running the command, reading the report,
what one benchmark proves. This readiness check confirms those fundamentals
are solid before introducing parameter sweeps.

**Recall (6):**
1. What are the three primary metrics in a Capsule benchmark report?
2. What does `--concurrency` control in the benchmark command?
3. What is TTFT and what does a high p99 value indicate?
4. What does "throughput" measure in the benchmark context?
5. What limitation of a single-concurrency benchmark was discussed in Day 42?
6. What does the "warm-up" phase of a benchmark accomplish?

**Apply (8):**
7. From Day 42: a benchmark at concurrency=1 shows TTFT p50=150ms — predict TTFT at concurrency=8
8. Identify which Day 42 benchmark flag to change for a parameter sweep over concurrency
9. Given Day 42's report format, identify which field tracks failed requests
10. Select the correct interpretation of p99 vs p50 gap from Day 42's lesson
11. From Day 42: what does a benchmark NOT measure that a quality eval would?
12. Identify the first step in a benchmark workflow (from Day 42's hands-on)
13. A team uses Day 42's benchmark results at concurrency=1 to size their production fleet — what is wrong?
14. Select the correct Day 42 takeaway: one benchmark run answers what question?

**Analyse (6):**
15. Why does Day 42 conclude that a single benchmark is "a starting point, not a verdict"?
16. Compare what Day 42 taught about benchmark design vs what Day 43 extends
17. A team runs Day 42's benchmark on day 1 and never again — identify the monitoring gap
18. From Day 42: why does p99 latency worsen faster than p50 as load increases?
19. Compare the information content of a single-point benchmark vs a sweep — what Day 43 extends
20. A team uses Day 42's warm benchmark data to predict cold-start production performance — identify the flaw

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: parameter sweep template (varying concurrency 1→16), expected
throughput and latency shapes (linear, saturation, degradation), saturation
curve analysis, predict-then-run exercise, reconcile predictions exercise.

**Recall (6):**
1. What is the "sweep template" introduced in Part 2?
2. What are the three regimes in a throughput-vs-concurrency curve?
3. What does "saturation" mean in a GPU serving context?
4. What does it mean to "predict then run" in Part 5?
5. What causes throughput to decline after saturation (the third regime)?
6. What does "reconcile predictions" mean in Part 6?

**Apply (8):**
7. Write a sweep plan: concurrency values 1, 2, 4, 8, 16, 32 — what data do you collect at each point?
8. Given a throughput curve that plateaus at concurrency=8 — identify the saturation point
9. Predict the shape of TTFT vs concurrency: sketch or describe the expected curve
10. Given measured data: concurrency=1 (50 tok/s), 4 (180 tok/s), 8 (340 tok/s), 16 (310 tok/s) — identify the saturation and decline
11. Identify what "regime 1 vs regime 2 vs regime 3" means in practical terms
12. A prediction overestimates throughput at high concurrency — identify which regime was misjudged
13. Select the correct interpretation when measured results are 30% below predicted at saturation
14. Calculate: at saturation, throughput=400 tok/s, concurrency=8 — what is per-user effective throughput?

**Analyse (6):**
15. Why does throughput increase then plateau then decline as concurrency increases?
16. Compare the value of predicting before running vs running then explaining — what skill does prediction build?
17. A team's sweep shows saturation at concurrency=4 — what does this reveal about the GPU's bottleneck?
18. Why does the reconcile step (comparing prediction to measurement) matter more than the measurement alone?
19. Compare the shape of a compute-bound system's sweep vs a memory-bound system's sweep
20. A team presents a throughput sweep to justify hardware spend — identify the three questions stakeholders will ask

---

## module-3 — Day 44 · Interactive Chat (Quality Evaluation)

**File:** `docs/lessons/week-09/module-3/index.md`  
**Pre-reading:** Lab Guide Module 9 — Interactive Chat and Quality Evaluation  
**data-source label:** `Capsule Power User Lab Guide Module 9`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-09-m3-readiness` | `readiness` | `Capsule Power User Lab Guide Module 9` |
| Wrap-up | `week-09-m3-wrapup` | `wrap-up` | `Day 44 · Interactive Chat (Quality Evaluation)` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: What Benchmarks Miss (quality, coherence, usefulness)
- Part 3 — Core: The 5-Prompt Eval Suite
- Part 4 — Deep Dive: Latency You Measure vs Latency You Feel
- Part 5 — Hands-On: Build Eval Suite
- Part 6 — Hands-On: Evaluate Two Configs
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 9)
Module 9 covers: how to use Capsule's interactive chat interface, what it
enables for manual quality evaluation, the concept of "felt latency" vs
measured latency, how to design a manual eval suite, comparing configs
qualitatively.

**Recall (6):**
1. What does Capsule's interactive chat interface allow a user to do?
2. What does a manual quality evaluation test that automated benchmarks don't?
3. What is "felt latency" and how does it differ from measured TTFT?
4. What is the "5-prompt eval suite" approach in Lab Guide Module 9?
5. What are the two configs typically compared in Module 9's evaluation exercise?
6. What is a "rubric" for manual quality evaluation?

**Apply (8):**
7. Identify three prompt types that a good 5-prompt eval suite should include for a code assistant
8. A benchmark shows TTFT=150ms but users report the response "feels slow" — which concept explains this?
9. Select the correct description of what "streaming quality" means in interactive chat
10. Given two configs: Config A (faster, shorter outputs) vs Config B (slower, more detailed) — how to evaluate?
11. Identify which quality dimension is hardest to measure with automated benchmarks
12. A team's eval suite has 5 identical prompts — identify the design flaw
13. Select the correct rubric dimension for evaluating "does the response follow the instruction"?
14. Classify: measuring TTFT with a stopwatch vs a benchmark tool — which is "felt latency"?

**Analyse (6):**
15. Why can a model with excellent benchmark scores fail a manual quality eval?
16. Compare automated benchmark evaluation and manual quality evaluation — what each is good for
17. A team uses only automated benchmarks for model comparison — what failure mode does this create?
18. Why does streaming affect "felt latency" in a way that batch generation doesn't?
19. Compare a 5-prompt suite evaluated by one person vs 5 people — what does the disagreement reveal?
20. A team's manual eval takes 4 hours per config — identify how to make it systematic and faster

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: what benchmarks miss (quality, coherence, instruction
following), 5-prompt suite design, felt latency vs measured latency analysis,
hands-on eval suite build, two-config comparison exercise.

**Recall (6):**
1. Name three quality dimensions that benchmarks miss
2. What are the five prompt categories recommended for an eval suite?
3. What is the "first token effect" in felt latency?
4. Name two rubric dimensions used in the Part 6 comparison exercise
5. What does "streaming affects felt latency" mean concretely?
6. What does the two-config comparison exercise produce as output?

**Apply (8):**
7. Design a 5-prompt eval suite for a "homework helper" chatbot — name the 5 prompts
8. A response streams slowly after a fast first token — classify: which latency metric explains the experience?
9. Given the rubric from Part 6, evaluate a provided sample response on all dimensions
10. Identify which eval suite prompt tests "instruction following"
11. Select the correct interpretation when Config A wins on 3 of 5 rubric dimensions but Config B wins on throughput
12. A team's eval shows Config A is better for simple queries, Config B for complex — what does this mean for deployment?
13. Apply the felt-latency analysis to: TTFT=200ms, ITL=150ms (slow stream) — what does the user experience?
14. Calculate: a 5-prompt suite takes 20 minutes per config, 5 evaluators, 3 configs — how long total?

**Analyse (6):**
15. Why is a 5-prompt eval suite enough to catch major quality regressions but not subtle ones?
16. Compare the eval suite approach for a research team vs a production team — what scales?
17. A team adds 50 prompts to their eval suite but only 1 evaluator — identify the new bottleneck
18. Why does "felt latency" matter for product retention even when measured latency is "good"?
19. Compare the two-config evaluation approach in this lesson with the quantitative sweep from Day 43
20. A team must choose between Config A (better quality, higher cost) and Config B (lower quality, half the cost) — what framework does this lesson provide for the decision?

---

## module-4 — Day 45 · Scheduling & MCP

**File:** `docs/lessons/week-09/module-4/index.md`  
**Pre-reading:** Lab Guide Module 10 — Scheduling and MCP Integration  
**data-source label:** `Capsule Power User Lab Guide Module 10`

### Widget IDs
| Widget | `data-id` | `data-kind` | `data-source` |
|--------|-----------|-------------|---------------|
| Readiness | `week-09-m4-readiness` | `readiness` | `Capsule Power User Lab Guide Module 10` |
| Wrap-up | `week-09-m4-wrapup` | `wrap-up` | `Day 45 · Scheduling & MCP` |

### Part structure
- Part 1 — Pre-Reading Review + Readiness Check (~15 min)
- Part 2 — Core: `capsule schedule` command
- Part 3 — Core: MCP for Capsule (Capsule as a tool source)
- Part 4 — Deep Dive: Phase 1+2+3 Composition (benchmarking → evaluation → scheduling)
- Part 5 — Hands-On: Create & Monitor Schedule
- Part 6 — Hands-On: Sketch Nightly Agent
- Part 7 — Wrap-up & Connection

### Readiness question outline (20 questions — Lab Guide Module 10 scheduling + MCP)
Module 10 covers: what `capsule schedule` does, how to create a recurring
benchmark or eval job, what MCP integration with Capsule enables, how an
agent could use Capsule tools.

**Recall (6):**
1. What does `capsule schedule` allow a user to do?
2. What is the cron syntax for "run every night at 2am"?
3. What does MCP integration with Capsule expose?
4. What is an "MCP server" in the context of Capsule?
5. What does `capsule schedule list` show?
6. What is the purpose of a "nightly benchmark agent" described in the Lab Guide?

**Apply (8):**
7. Write the `capsule schedule` command to run a benchmark nightly at 2am on node `gpu-01`
8. An MCP server exposes `capsule list machines` as a tool — what can an agent do with this?
9. Identify what a "nightly agent" needs: list machines, run benchmark, store results, notify team
10. Select the correct cron expression for "every Monday at 8am"
11. A schedule is created but the job never runs — identify the first troubleshooting step
12. Classify: using MCP to let Claude run `capsule connect` — which security concern applies?
13. Identify what the `capsule schedule logs` command shows
14. Select the correct MCP tool call to list available GPU nodes from an agent context

**Analyse (6):**
15. Why does automating nightly benchmarks catch performance regressions that manual checks miss?
16. Compare a cron job on the GPU node vs `capsule schedule` — what does Capsule's scheduler add?
17. A team exposes all Capsule CLI commands via MCP — identify the security risks
18. Why does Phase 1+2+3 composition (benchmark → eval → schedule) represent a complete workflow?
19. Compare a human-in-the-loop nightly review vs a fully automated scheduled benchmark — trade-offs?
20. A team's nightly benchmark agent sends alerts but nobody acts on them — identify the workflow failure

### Wrap-up question outline (20 questions — Parts 2–6)
Parts 2–6 cover: `capsule schedule` syntax and lifecycle, MCP Capsule
integration overview, Phase 1+2+3 composition diagram, create-and-monitor
schedule exercise, nightly agent sketch exercise.

**Recall (6):**
1. What is the `capsule schedule create` command syntax?
2. Name three Capsule CLI operations that an MCP server could expose as tools
3. What are the three phases in the Phase 1+2+3 composition?
4. What does the "notify team" step in a nightly agent require?
5. What does `capsule schedule delete <id>` do?
6. What does MCP enable that direct CLI scripting does not?

**Apply (8):**
7. Create a schedule to run a benchmark sweep (concurrency 1,4,8) every Sunday at midnight
8. Sketch a nightly agent workflow: list nodes → select best node → run benchmark → store results → send Slack notification
9. Given MCP tools: `capsule_list_machines`, `capsule_run_benchmark`, `capsule_get_results` — trace an agent invocation
10. Identify which part of the nightly agent requires an LLM step vs a deterministic step
11. Select the correct monitoring approach for a scheduled benchmark job
12. Apply Phase 1+2+3: a team has Phase 1 (benchmark) and Phase 3 (schedule) — what is Phase 2?
13. Identify what happens when a scheduled benchmark runs during a period of high fleet utilisation
14. A nightly agent's benchmark results vary wildly each night — identify three possible causes

**Analyse (6):**
15. Why is composing Phase 1+2+3 more powerful than running each phase in isolation?
16. Compare human-run benchmarks vs scheduled automated benchmarks — what bias does automation remove?
17. A team's MCP-powered agent has write access to Capsule — identify the least-privilege violation
18. Why is Phase 3 (scheduling) the last phase rather than the first — why does the order matter?
19. Compare the operational burden of a nightly benchmark agent vs a weekly manual benchmark — at 6-month scale
20. A team's final project integrates all three phases — identify the three most common integration failure points and their mitigations

---

## Execution checklist

- [ ] Read this file in full before starting
- [ ] Read `planning/widget-conversion/README.md` for JSON schema + quality rules
- [ ] Read Lab Guide Modules 8, 9, 10 from `Capsule-Power-User-Lab-Guide.md`
- [ ] module-1 (Day 42): Lab Guide M8 readiness + first benchmark wrap-up
- [ ] module-2 (Day 43): Day 42 recall readiness (test Day 42 content) + parameter sweep wrap-up
  - Note: `data-source="Day 42 · Your First Benchmark"` for readiness widget
- [ ] module-3 (Day 44): Lab Guide M9 readiness + quality evaluation wrap-up
- [ ] module-4 (Day 45): Lab Guide M10 readiness + scheduling & MCP wrap-up
- [ ] After each module: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"`
- [ ] After each module: commit with `feat(quiz): add readiness + wrap-up widgets to Day NN · <title>`
- [ ] After all 4 modules: `python3 scripts/audit_lessons.py` — 0 violations
- [ ] Push all commits: `git push origin feat/content-fortification`

---

## After all week plans complete

With all nine week plan files done, the next step is the **pilot execution**:
1. Open `docs/lessons/week-01/module-2/index.md`
2. Read `planning/widget-conversion/README.md` (JSON schema + HTML structure)
3. Read `planning/widget-conversion/week-01.md` (module-2 section)
4. Author 20 readiness questions (Shell/MIT Missing Semester source) in JSON
5. Author 20 wrap-up questions (Parts 2–5 content) in JSON
6. Insert both widget `<div>` blocks at the correct insertion points
7. Run `mkdocs build --strict` and `python3 scripts/audit_lessons.py`
8. Commit: `feat(quiz): add readiness + wrap-up widgets to Day 2 · Shell & Linux`
9. Present for user review before proceeding to week-01/module-3
