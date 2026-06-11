---
drift: |
  Originally Day 43 of the former Capsule wk9, named "Interactive Evaluation". Now Day 44
  of the new week (week-09/module-3), renamed "Interactive Chat" in the graph but scope
  is essentially identical. Source-material link paths bumped one level deeper.
---

# Day 44 · Interactive Chat (Quality Evaluation)

> **Concept of the day:** **throughput is not quality.** A fast config that produces worse answers is a worse config. Use the Capsule chat UI to probe quality *interactively* — both speed (TTFT/ITL felt as a human) and quality (correctness, refusals, hallucinations) — alongside the benchmark numbers.
> **Pre-reading:** Lab Guide **Module 9** (~15 min).
> **Source:** [Lab Guide Module 9](../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md).

---

## Why this matters

It's painfully easy to optimize for the wrong thing. Quantize down to FP8 to hit a throughput target, ship it, watch the model hallucinate medical dosages or refuse benign requests — and now your "fast" config has cost a customer. Today: build the habit of **feeling** the model alongside benchmarking it.

## Readiness check

1. What does the chat UI measure that `report.json` cannot?
2. What's the difference between *latency you measure* and *latency you feel*?
3. Name three quality dimensions you can probe interactively.
4. Why is a 5–10 prompt eval suite enough to *catch regressions* — but not enough to *validate quality*?
5. What's the link to Week 6 (eval-driven prompting)?

## Core concept

### What the chat UI gives you

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

### A 5–10 prompt eval suite

Borrow directly from Week 6 Day 29. Keep a curated set of prompts you run against *every* config change:

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

### Latency you measure vs latency you feel

| Measured | Felt |
|---|---|
| TTFT 380 ms | "feels snappy" |
| TTFT 1200 ms | "feels sluggish — am I sure I hit enter?" |
| ITL 20 ms (50 tok/s) | "comfortable reading pace" |
| ITL 50 ms (20 tok/s) | "I'm waiting on words" |
| ITL 8 ms (125 tok/s) | "too fast to read in real time — fine for tools, weird for chat" |

For human-facing chat, you want both TTFT < ~600 ms *and* ITL roughly matched to reading pace (~30–60 tokens/s). For agent / tool calls, push throughput as high as you can — no human is reading the stream.

### How to evaluate two configs side by side

1. Spin up config A in one Capsule chat tab.
2. Spin up config B in a second tab.
3. Run the same prompt suite through both.
4. For each prompt: which feels faster? Which is *correct*? Which is more helpful?
5. Tally. Write 3 sentences per config: speed, quality, recommended use.

### Link to Week 6

This day **is** Week 6 Day 29 (eval-driven prompting) applied to the *config* axis instead of the *prompt* axis. The discipline is the same: write the suite first, measure against it.

## Practice (90 min)

1. (10 min) Lease a node, ensure two model configs are reachable (e.g. FP16 vs FP8 of the same model).
2. (25 min) Build (or pull from Week 6 Day 29) your 5–10 prompt eval suite. Write each prompt + the criterion that defines pass/fail.
3. (30 min) Run the suite against both configs in the chat UI. Record pass/fail per prompt per config.
4. (15 min) Compare: where does FP8 lose quality? Where does it keep up? Is the throughput win worth it?
5. (10 min) Write your 3-sentence verdict per config and commit it next to yesterday's saturation curve.

## Wrap-up

Cohort has both numbers (Day 41–42) and felt quality (Day 43) for at least one config comparison.

## Connect forward

Tomorrow: **scheduling & MCP** — once you trust a config, automate the benchmark + eval. Also: Capsule's MCP surface, so an agent (Week 7!) can run benchmarks for you.

---

## Pre-read for tomorrow (Day 44 · Scheduling & MCP)

- **Resource:** Lab Guide **Module 10** (~15 min).
- **Reflection questions:**
  1. Why schedule benchmarks instead of running them by hand?
  2. What does an MCP surface for Capsule unlock that the CLI alone doesn't?
  3. If your Week 7 agent project were to run nightly benchmarks, what tools would it need?
