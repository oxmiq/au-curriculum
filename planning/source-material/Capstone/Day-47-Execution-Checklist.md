# Day 47 — Execution Checklist

> **Outcome of the day:** raw benchmark results + raw eval-suite results for every candidate configuration. No analysis yet — that's Day 48.
> **Mindset:** you are an engineer running a scientific experiment. Vary one knob at a time. Record everything.

---

## Schedule for Day 47

| Time | Activity |
|---|---|
| 0:00–0:30 | Standup: each team states today's plan in one sentence. Facilitator surfaces blockers. |
| 0:30–2:30 | Execute. Benchmarks + evals. Document as you go. |
| 2:30–3:00 | Mid-day checkpoint: each team has at least one full row of results. If not, escalate. |
| 3:00–3:30 | Wrap-up: commit all raw results to repo. End-of-day standup. |
| (Evening, optional) | If a long benchmark is queued via `capsule schedule`, let it run overnight. |

---

## Execution checklist (in order)

### 1. Baseline first (always)

- [ ] Run the **FP16 baseline** for your primary model at concurrency = 1. This is your reference row.
- [ ] Record: TTFT (P50/P95), ITL (P50/P95), TPS, throughput at concurrency 1.
- [ ] Run the eval suite (10 prompts) against this baseline. Save outputs.

If you don't have a baseline, every other number you collect is uninterpretable.

### 2. Sweep concurrency on the baseline

- [ ] Run the same FP16 baseline at concurrency 4, 8, 16 (or whatever your charter listed).
- [ ] Record the same metrics at each level.
- [ ] Note: throughput should rise; P95 latency should rise; at some point you'll see the throughput plateau and latency keep rising — that's your knee.

### 3. Now vary one knob at a time

In this order:

- [ ] **Quantization sweep** (FP16 → FP8 → INT4): same model, same GPU, same concurrency.
- [ ] **Hardware sweep** (e.g., 1×H100 → 1×L4 → 1×T4): same model, same quantization, same concurrency.
- [ ] **Parallelism sweep** (if applicable: TP=1 → TP=2 → TP=4): only meaningful for larger models.
- [ ] **Batching engine sweep** (vLLM vs SGLang vs TRT-LLM): if your charter included one, do it last — most variance.

Never vary two knobs in the same run. You'll never know which one moved the metric.

### 4. Eval suite per configuration

For every quantization variant, re-run the 10-prompt eval suite. Save outputs in `eval/results/<config-name>/`.

- [ ] Pass/fail per prompt, per config — recorded in a table.
- [ ] At least one "negative" prompt where the correct answer is a refusal or "I don't know." (Prevents over-eager configs from gaming the score.)
- [ ] Manual diff between FP16 baseline output and quantized output for at least 3 prompts — note any *meaning* changes, not just wording.

### 5. Cost math (raw inputs, not analyzed yet)

For each configuration, record:

- [ ] GPU(s) used (e.g., 1×H100)
- [ ] Hourly cost (Capsule pricing, or facilitator-provided $/hr)
- [ ] Sustained throughput (tokens/sec) at your target concurrency
- [ ] Total tokens generated during benchmark (Capsule reports this)
- [ ] Wall-clock time of benchmark

This lets Day 48 compute $/1M tokens cleanly.

---

## Recording template (per configuration)

Copy this block for each row in your candidate matrix. Commit to `capstone/<team-name>/results/<config-name>.md`.

```markdown
# Config: <name> (e.g., "llama-3.1-8b-fp8-1xh100-conc16")

## Setup
- Model: Llama-3.1-8B-Instruct
- Quantization: FP8
- Hardware: 1×H100
- Parallelism: TP=1
- Engine: vLLM 0.6.x
- Concurrency: 16
- Capsule machine unique-id: <copy from `capsule list`>
- Date / time of run: ___

## Benchmark output (paste raw output)
```
<paste `capsule benchmark` output verbatim>
```

## Key metrics
| Metric | Value |
|---|---|
| TTFT P50 / P95 | ___ ms / ___ ms |
| ITL P50 / P95 | ___ ms / ___ ms |
| TPS (decode) | ___ tokens/sec |
| Throughput | ___ req/sec |
| Total tokens generated | ___ |
| Wall-clock | ___ sec |

## Eval suite results
| # | Prompt | Expected | Got | Pass? | Notes |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ✓/✗ | |
| ... | | | | | |
| 10 | ... | ... | ... | ✓/✗ | |

Pass rate: ___ / 10

## Cost
- $/hr for this hardware: $___
- Throughput: ___ tokens/sec
- Cost per 1M output tokens: $___ (computed Day 48)

## Surprises / notes
*Anything that didn't go as expected. Crashes, weird outputs, "oh that's faster than I thought," etc.*
```

---

## Mid-day checkpoint (2:30 PM)

By 2:30 PM every team must have:

- [ ] FP16 baseline row complete (benchmark + eval).
- [ ] At least one quantization variant row complete.
- [ ] All results committed and pushed.

If not: facilitator triages. Most common rescue is "you're varying too many things at once — pick one knob."

---

## End-of-day standup (3:00 PM)

Each team gives a 2-minute update:

1. Number of configurations completed (out of planned).
2. One surprise from today's data.
3. One blocker for tomorrow, if any.

The facilitator will note which teams need a Day 48 morning unblock.

---

## Common Day 47 pitfalls

| Pitfall | Symptom | Fix |
|---|---|---|
| Varying multiple knobs per run | Can't explain why numbers changed | One knob per row. Use the recording template. |
| No baseline | "Is FP8 faster?" — faster than what? | Always run FP16 first. |
| Benchmark too short | High-variance numbers | Each benchmark ≥ 60s of sustained load, or ≥ 500 requests. |
| Eval prompts overlap too much | All configs pass everything; can't distinguish | Make eval prompts hit different failure modes. |
| Forgot to record machine ID | Can't re-run if you need to | Capsule machine unique-id in every result file. |
| Long benchmark in interactive terminal | SSH drops; you lose results | Use `capsule schedule` for anything > 30 min. |

---

## End of Day 47: definition of done

- [ ] ≥3 candidate configurations have full rows (benchmark + eval).
- [ ] All raw outputs committed to the repo.
- [ ] One end-of-day commit with a conventional-commit message: `feat(capstone): day 47 raw benchmark + eval results`.
- [ ] Team Slack / chat update with one-line status.
