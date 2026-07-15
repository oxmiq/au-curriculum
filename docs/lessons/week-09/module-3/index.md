---
drift: |
  Originally Day 43 of the former Capsule wk9, named "Interactive Evaluation". Now Day 43
  of the new week (week-09/module-3), renamed "Interactive Chat" in the graph but scope
  is essentially identical. Source-material link paths bumped one level deeper.
---

# Day 43 · Interactive Chat (Quality Evaluation)

> **Concept of the day:** **throughput is not quality.** A fast config that produces worse answers is a worse config. Use the Capsule chat UI to probe quality *interactively*, both speed (TTFT/ITL felt as a human) and quality (correctness, refusals, hallucinations), alongside the benchmark numbers.<br>
> **Pre-reading:** <a href="../../../readings/capsule/#interactive-evaluation">Capsule Power-User Pre-Lecture Reading - Interactive Evaluation</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-9-model-evaluation-interactive-chat">Capsule Lab Guide</a> Module 9.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../../curriculum/">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 - Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 43 · Interactive Chat</span>
    {status:week-09/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity |
|---|---|
| Part 1 | Pre-Reading Review |
| Part 2 | Core Concepts: What Benchmarks Miss |
| Part 3 | Core Concepts: The 5-Prompt Eval Suite |
| Part 4 | Deep Dive: Latency You Measure vs Latency You Feel |
| Part 5 | Hands-On: Build Your Eval Suite |
| Part 6 | Hands-On: Evaluate Two Configs Side by Side |
| Part 7 | Wrap-up & Connection |

**Total: ~145 min**

---

## Part 1 - Pre-Reading Review

### Reading - Why this matters

It's painfully easy to optimize for the wrong thing. Quantize down to FP8 to hit a throughput target, ship it, watch the model hallucinate medical dosages or refuse benign requests; and now your "fast" config has cost a customer. Today: build the habit of **feeling** the model alongside benchmarking it.

### Exercise: Self-Check

Answer before reading on:

1. What does the chat UI measure that `report.json` cannot?
2. What's the difference between *latency you measure* and *latency you feel*?
3. Name three quality dimensions you can probe interactively.
4. Why is a 5–10 prompt eval suite enough to *catch regressions*: but not enough to *validate quality*?
5. What's the link to Week 6 Day 29 (eval-driven prompting)?

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m3-readiness" data-kind="readiness" data-draw="5" data-source="Capsule Power-User Pre-Lecture Reading + Lab Guide Module 9">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "What does `report.json` NOT capture that the Capsule chat UI can reveal?", "options": ["TTFT and ITL numbers", "GPU utilisation during inference", "Answer correctness, refusal behaviour, tone, and hallucinations", "Throughput in tokens per second"]},
  {"stem": "What is 'latency you feel' vs 'latency you measure'?", "options": ["They are the same thing: p99 latency", "'Latency you feel' is how a human experiences streaming (first word, smoothness); 'latency you measure' is p50/p99 numbers in report.json", "'Latency you measure' is GPU processing time; 'latency you feel' is network delay", "'Latency you feel' is only relevant for video streaming, not text"]},
  {"stem": "Why is a 5–10 prompt eval suite enough to CATCH regressions but not to VALIDATE quality?", "options": ["Because regressions are smaller than quality failures", "A small focused suite can flag if a config change broke something specific; validating general quality requires much broader coverage across topics, formats, and edge cases", "Because 10 is the maximum supported by the chat UI", "Because quality can only be validated by automated benchmarks"]},
  {"stem": "Which of these quality dimensions can you probe interactively in the Capsule chat UI?", "options": ["Only TTFT and token throughput", "Correctness, refusal behaviour, hallucinations, tone, and output format", "Only correctness and GPU memory usage", "Only refusals and safety filters"]},
  {"stem": "You optimize a model config for throughput; it's 30% faster but fails your eval suite on medical prompts. What does this tell you?", "options": ["The eval suite is wrong; throughput is the goal", "A fast config that produces worse answers is a worse config; throughput is not quality", "You should ignore the quality failure if throughput is the SLA metric", "The model needs more GPU memory"]},
  {"stem": "What is the connection between Day 43 (Interactive Chat) and Week 6 Day 29 (eval-driven prompting)?", "options": ["Day 29 introduced API calls; Day 43 introduces the chat UI", "Day 29 taught evaluating outputs to iterate on prompts; Day 43 applies the same evaluation habit to model configs: same skill, different target", "They are unrelated; one is about prompting, the other about infrastructure", "Day 44 replaces the techniques from Day 29"]},
  {"stem": "When evaluating two configs side by side in the Capsule chat UI, what is the minimum useful comparison?", "options": ["Run the same 5 prompts on both configs; compare TTFT felt + answer quality for each", "Run 100+ prompts and use automated scoring", "Compare only TTFT; if one feels faster, it's better", "Compare GPU utilisation from report.json"]},
  {"stem": "What does 'streaming smoothness' measure in the chat UI that benchmark numbers miss?", "options": ["The GPU temperature during inference", "Whether ITL is consistent enough to produce smooth token-by-token streaming without visible pauses", "How many tokens per second the model generates", "The network bandwidth between the GPU node and your laptop"]}
]
</script>
</div>

---

## Part 2 - Core Concepts: What Benchmarks Miss

### Reading - The benchmark vs chat comparison

| Dimension | Benchmark report | Chat UI |
|---|---|---|
| TTFT | p50 / p99 number | You *feel* it: how long until first word? |
| ITL | p50 / p99 number | You *see* it: does it stream smoothly? |
| Correctness | - | You judge it |
| Refusals | - | You probe edge cases |
| Tone / style | - | You feel it |
| Hallucinations | - | You spot them |
| Output format | - | You verify it |

The benchmark answers "is it fast?" The chat answers "is it any good?"

### Exercise: Benchmark Blind Spots

For each production scenario, identify what the benchmark report would NOT tell you:

1. A customer-facing code assistant that must refuse to generate malware.
2. A document summarizer that must correctly reference specific page numbers.
3. A chatbot that must match your brand's formal tone.
4. An agent tool-call parser that must return valid JSON every time.

---

## Part 3 - Core Concepts: The 5-Prompt Eval Suite

### Reading - Borrow from Week 6 Day 29

Keep a curated set of prompts you run against *every* config change:

1. **A simple correctness probe** - math, fact, code one-liner. Answer should be obvious.
2. **A refusal probe** - benign-but-edgy request the model shouldn't refuse.
3. **A safety probe** - clearly out-of-bounds request the model *should* refuse.
4. **A long-context probe** - give it a doc, ask a specific question deep in it.
5. **A format probe** - "return JSON with fields x, y, z." Verify schema.
6. **A reasoning probe** - multi-step word problem.
7. **A hallucination probe** - ask about something specific & verifiable.
8. **A tone probe** - ensure it stays in character / register.

Run all of them. Note pass/fail per prompt. Compare config A vs config B.

This isn't statistical validation; it's a **smoke test**. Enough to catch regressions, not enough to certify production quality (that needs Week 5 Day 23's full eval setup).

### Exercise: Write Your First Eval Prompt

Write one prompt for each of the 8 types above, targeting a "code assistant" use case. For each, write the criterion that defines pass/fail (1 sentence).

| Type | Prompt | Pass criterion |
|---|---|---|
| Correctness | | |
| Refusal probe | | |
| Safety probe | | |
| Long-context | | |
| Format | | |
| Reasoning | | |
| Hallucination | | |
| Tone | | |

---

## Part 4 - Deep Dive: Latency You Measure vs Latency You Feel

### Reading - The human perception table

| Measured | Felt |
|---|---|
| TTFT 380 ms | "feels snappy" |
| TTFT 1200 ms | "feels sluggish: am I sure I hit enter?" |
| ITL 20 ms (50 tok/s) | "comfortable reading pace" |
| ITL 50 ms (20 tok/s) | "I'm waiting on words" |
| ITL 8 ms (125 tok/s) | "too fast to read in real time: fine for tools, weird for chat" |

For human-facing chat, you want both TTFT < ~600 ms *and* ITL roughly matched to reading pace (~30–60 tokens/s). For agent / tool calls, push throughput as high as you can; no human is reading the stream.

### Reading - How to evaluate two configs side by side

1. Spin up config A in one Capsule chat tab.
2. Spin up config B in a second tab.
3. Run the same prompt suite through both.
4. For each prompt: which feels faster? Which is *correct*? Which is more helpful?
5. Tally. Write 3 sentences per config: speed, quality, recommended use.

### Exercise: Feel vs Measure

Your benchmark shows: Config A: TTFT p99 = 380 ms. Config B: TTFT p99 = 1150 ms.

1. Which would a human notice more: the difference in p99 or p50? Why?
2. For a streaming chat interface, at what ITL do you expect users to start complaining?
3. For an autonomous agent making 50 tool calls per task, does TTFT matter much? What does?

---

## Part 5 - Hands-On: Build Your Eval Suite

### Exercise: Finalize Your 8-Prompt Suite

1. Refine the table from Part 3; make sure every prompt is specific and the pass criterion is binary (pass/fail, not "looks good").
2. Write out each prompt in full, as you'd type it into a chat UI.
3. Share your suite with a partner. They should be able to run it without asking you any questions.

---

## Part 6 - Hands-On: Evaluate Two Configs Side by Side

### Exercise: Comparative Evaluation

1. Ensure two model configs are reachable (e.g. FP16 vs FP8 of the same model, or two concurrency settings from yesterday).
2. Run your 8-prompt suite against Config A in the chat UI. Record pass/fail per prompt.
3. Run the same suite against Config B. Record pass/fail per prompt.
4. Compare: where does Config B lose quality? Where does it keep up? Is the throughput win worth it?

Fill in:

| Prompt type | Config A result | Config B result | Winner |
|---|---|---|---|
| Correctness | | | |
| Refusal probe | | | |
| Safety probe | | | |
| Long-context | | | |
| Format | | | |
| Reasoning | | | |
| Hallucination | | | |
| Tone | | | |

Write your 3-sentence verdict per config and commit it alongside your Day 42 saturation curve.

---

## Part 7 - Wrap-up & Connection

### Self-check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-09-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 43 · Interactive Chat Evaluation">

<script type="application/json" class="ox-self-check__pool">
[
  {"stem": "Why is the benchmark report (TTFT, throughput) insufficient for config selection on its own?", "options": ["The benchmark report doesn't measure GPU utilization", "The benchmark report measures speed, not quality; a fast config that hallucinates or gives wrong answers fails in production regardless of its latency numbers", "The benchmark report only measures one concurrency level", "The benchmark report doesn't account for network latency"]},
  {"stem": "What is the human perception threshold for TTFT that separates 'feels instant' from 'noticeable delay'?", "options": ["< 50 ms is instant, 50-500 ms is acceptable, > 500 ms is noticeable", "< 200 ms feels responsive; > 500-700 ms starts feeling noticeably slow", "< 1 second is always acceptable for any interactive use case", "< 100 ms is instant; any TTFT above 100 ms is unacceptable"]},
  {"stem": "What makes a good evaluation prompt suite for an interactive eval?", "options": ["Use 100+ prompts to ensure statistical significance", "A small set (8-10) of diverse, representative prompts with clear binary pass/fail criteria defined before running; representativeness matters more than quantity", "Use only the 3 hardest prompts to stress-test the model", "Use prompts from the model's training set to avoid distributional shift"]},
  {"stem": "How do you separate quality from latency in your config comparison judgment?", "options": ["Use throughput numbers as a proxy for quality", "Run the same eval suite against each config independently, recording quality pass/fail per prompt separately from latency metrics; then compare both dimensions in your config table", "Higher latency configs always have better quality", "Quality and latency cannot be separated; you must choose one"]},
  {"stem": "What is ITL (Inter-Token Latency) and why does it matter for user experience?", "options": ["Inter-Token Latency is the time between words in a spoken response: only relevant for voice interfaces", "ITL is the time between consecutive output tokens during streaming; high ITL causes visible stutter or pause mid-response, degrading user experience even if TTFT is good", "ITL measures the latency of the tokenization step", "ITL is the total time to receive all tokens minus TTFT"]},
  {"stem": "For an autonomous agent making 50 tool calls per task, which metric matters most; and which matters least?", "options": ["Throughput (tok/s) matters most; no human reads the stream, so push it as high as you can; TTFT per call matters far less", "TTFT matters most; the agent feels every first-token delay the way a human does", "Streaming smoothness matters most; the agent needs a comfortable reading pace", "Tone and register matter most; the agent judges the style of each response"]},
  {"stem": "Your 5-prompt eval suite includes both a 'refusal probe' and a 'safety probe'. How do they differ?", "options": ["They are the same test run twice for reliability", "The refusal probe checks GPU limits; the safety probe checks memory pressure", "The refusal probe is a benign-but-edgy request the model should NOT refuse; the safety probe is a clearly out-of-bounds request the model SHOULD refuse", "The safety probe measures TTFT while the refusal probe measures ITL"]},
  {"stem": "Why is an 8-prompt interactive eval a 'smoke test' rather than a production-quality certification?", "options": ["Because 8 prompts is the maximum the chat UI supports", "Because smoke tests only measure latency, never correctness", "Because interactive evals cannot detect hallucinations", "It catches regressions on the specific capabilities you care about, but certifying general quality needs far broader coverage: the full eval setup from Week 5 Day 23"]}
]
</script>
</div>

### Connect forward

Tomorrow: **scheduling & MCP**: once you trust a config, automate the benchmark + eval. Also: Capsule's MCP surface, so an agent can run benchmarks for you.

### Pre-read for tomorrow (Day 44 · Scheduling & MCP)

- **Resource:** <a href="../../../readings/capsule/#scheduling-mcp">Capsule Power-User Pre-Lecture Reading - Scheduling & MCP</a>. Supplement: <a href="../../../readings/capsule/lab-guide/#module-10-scheduled-jobs-agents-and-the-reliability-toolkit">Capsule Lab Guide</a> Module 10.
- **Reflection questions:**
  1. Why schedule benchmarks instead of running them by hand?
  2. What does an MCP surface for Capsule unlock that the CLI alone doesn't?
  3. If your Week 6 agent project were to run nightly benchmarks, what tools would it need?

---

## Stuck?

Ask **oxtutor**; share which config performed better on which eval type, and it can help you explain the quality tradeoff in terms of model precision (Week 3 Day 14).
