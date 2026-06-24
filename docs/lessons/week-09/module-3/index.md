---
drift: |
  Originally Day 43 of the former Capsule wk9, named "Interactive Evaluation". Now Day 44
  of the new week (week-09/module-3), renamed "Interactive Chat" in the graph but scope
  is essentially identical. Source-material link paths bumped one level deeper.
---

# Day 44 · Interactive Chat (Quality Evaluation)

> **Concept of the day:** **throughput is not quality.** A fast config that produces worse answers is a worse config. Use the Capsule chat UI to probe quality *interactively* — both speed (TTFT/ITL felt as a human) and quality (correctness, refusals, hallucinations) — alongside the benchmark numbers.<br>
> **Pre-reading:** Lab Guide **Module 9** (~15 min).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 9 — Capsule: Benchmarking &amp; Eval</a>
    <span class="sep">/</span>
    <span>Day 44 · Interactive Chat</span>
    <span class="sep">·</span>
    <span class="duration">~3 hrs</span>
    {status:week-09/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Lesson plan

| Part | Activity | Duration |
|---|---|---|
| Part 1 | Pre-Reading Review | 15 min |
| Part 2 | Core Concepts: What Benchmarks Miss | 20 min |
| Part 3 | Core Concepts: The 5-Prompt Eval Suite | 25 min |
| Part 4 | Deep Dive: Latency You Measure vs Latency You Feel | 20 min |
| Part 5 | Hands-On: Build Your Eval Suite | 25 min |
| Part 6 | Hands-On: Evaluate Two Configs Side by Side | 30 min |
| Part 7 | Wrap-up & Connection | 10 min |

**Total: ~145 min**

---

## Part 1 — Pre-Reading Review · 15 min

### Reading — Why this matters

It's painfully easy to optimize for the wrong thing. Quantize down to FP8 to hit a throughput target, ship it, watch the model hallucinate medical dosages or refuse benign requests — and now your "fast" config has cost a customer. Today: build the habit of **feeling** the model alongside benchmarking it.

### Exercise: Self-Check

Answer before reading on:

1. What does the chat UI measure that `report.json` cannot?
2. What's the difference between *latency you measure* and *latency you feel*?
3. Name three quality dimensions you can probe interactively.
4. Why is a 5–10 prompt eval suite enough to *catch regressions* — but not enough to *validate quality*?
5. What's the link to Week 6 Day 29 (eval-driven prompting)?

---

## Part 2 — Core Concepts: What Benchmarks Miss · 20 min

### Reading — The benchmark vs chat comparison

| Dimension | Benchmark report | Chat UI |
|---|---|---|
| TTFT | p50 / p99 number | You *feel* it — how long until first word? |
| ITL | p50 / p99 number | You *see* it — does it stream smoothly? |
| Correctness | — | You judge it |
| Refusals | — | You probe edge cases |
| Tone / style | — | You feel it |
| Hallucinations | — | You spot them |
| Output format | — | You verify it |

The benchmark answers "is it fast?" The chat answers "is it any good?"

### Exercise: Benchmark Blind Spots

For each production scenario, identify what the benchmark report would NOT tell you:

1. A customer-facing code assistant that must refuse to generate malware.
2. A document summarizer that must correctly reference specific page numbers.
3. A chatbot that must match your brand's formal tone.
4. An agent tool-call parser that must return valid JSON every time.

---

## Part 3 — Core Concepts: The 5-Prompt Eval Suite · 25 min

### Reading — Borrow from Week 6 Day 29

Keep a curated set of prompts you run against *every* config change:

1. **A simple correctness probe** — math, fact, code one-liner. Answer should be obvious.
2. **A refusal probe** — benign-but-edgy request the model shouldn't refuse.
3. **A safety probe** — clearly out-of-bounds request the model *should* refuse.
4. **A long-context probe** — give it a doc, ask a specific question deep in it.
5. **A format probe** — "return JSON with fields x, y, z." Verify schema.
6. **A reasoning probe** — multi-step word problem.
7. **A hallucination probe** — ask about something specific & verifiable.
8. **A tone probe** — ensure it stays in character / register.

Run all of them. Note pass/fail per prompt. Compare config A vs config B.

This isn't statistical validation — it's a **smoke test**. Enough to catch regressions, not enough to certify production quality (that needs Week 5 Day 23's full eval setup).

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

## Part 4 — Deep Dive: Latency You Measure vs Latency You Feel · 20 min

### Reading — The human perception table

| Measured | Felt |
|---|---|
| TTFT 380 ms | "feels snappy" |
| TTFT 1200 ms | "feels sluggish — am I sure I hit enter?" |
| ITL 20 ms (50 tok/s) | "comfortable reading pace" |
| ITL 50 ms (20 tok/s) | "I'm waiting on words" |
| ITL 8 ms (125 tok/s) | "too fast to read in real time — fine for tools, weird for chat" |

For human-facing chat, you want both TTFT < ~600 ms *and* ITL roughly matched to reading pace (~30–60 tokens/s). For agent / tool calls, push throughput as high as you can — no human is reading the stream.

### Reading — How to evaluate two configs side by side

1. Spin up config A in one Capsule chat tab.
2. Spin up config B in a second tab.
3. Run the same prompt suite through both.
4. For each prompt: which feels faster? Which is *correct*? Which is more helpful?
5. Tally. Write 3 sentences per config: speed, quality, recommended use.

### Exercise: Feel vs Measure

Your benchmark shows: Config A: TTFT p99 = 380 ms. Config B: TTFT p99 = 1150 ms.

1. Which would a human notice more — the difference in p99 or p50? Why?
2. For a streaming chat interface, at what ITL do you expect users to start complaining?
3. For an autonomous agent making 50 tool calls per task, does TTFT matter much? What does?

---

## Part 5 — Hands-On: Build Your Eval Suite · 25 min

### Exercise: Finalize Your 8-Prompt Suite

1. Refine the table from Part 3 — make sure every prompt is specific and the pass criterion is binary (pass/fail, not "looks good").
2. Write out each prompt in full, as you'd type it into a chat UI.
3. Share your suite with a partner. They should be able to run it without asking you any questions.

---

## Part 6 — Hands-On: Evaluate Two Configs Side by Side · 30 min

### Exercise: Comparative Evaluation

1. (5 min) Ensure two model configs are reachable (e.g. FP16 vs FP8 of the same model, or two concurrency settings from yesterday).
2. (15 min) Run your 8-prompt suite against Config A in the chat UI. Record pass/fail per prompt.
3. (5 min) Run the same suite against Config B. Record pass/fail per prompt.
4. (5 min) Compare: where does Config B lose quality? Where does it keep up? Is the throughput win worth it?

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

Write your 3-sentence verdict per config and commit it alongside your Day 43 saturation curve.

---

## Part 7 — Wrap-up & Connection · 10 min

### Self-check

- [ ] I have an 8-prompt eval suite with binary pass criteria for each prompt
- [ ] I ran the suite against at least 2 configs and recorded results
- [ ] I can articulate why the benchmark report alone is insufficient for config selection
- [ ] I understand the human perception thresholds for TTFT and ITL
- [ ] My verdict + eval results are committed to my fork

### Connect forward

Tomorrow: **scheduling & MCP** — once you trust a config, automate the benchmark + eval. Also: Capsule's MCP surface, so an agent can run benchmarks for you.

### Pre-read for tomorrow (Day 45 · Scheduling & MCP)

- **Resource:** Lab Guide **Module 10** (~15 min).
- **Reflection questions:**
  1. Why schedule benchmarks instead of running them by hand?
  2. What does an MCP surface for Capsule unlock that the CLI alone doesn't?
  3. If your Week 6 agent project were to run nightly benchmarks, what tools would it need?

---

## Stuck?

Ask **oxtutor** — share which config performed better on which eval type, and it can help you explain the quality tradeoff in terms of model precision (Week 3 Day 14).
