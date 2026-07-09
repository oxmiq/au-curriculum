# Day 49 · Analyze & Recommend

> **Concept of the day:** raw data does not persuade. **A comparison table + a cost calculation + a defended recommendation** persuade. Today: compile, calculate, conclude. Build the presentation around the **claim sentence** (see capstone deliverable).<br>
> **Source template:** [Day-48 Presentation Outline](../../../../planning/source-material/Capstone/Day-48-Presentation-Outline.md) (source filename is `Day-48-...` from upstream capstone-relative naming; this is program Day 49).

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 10 — Capstone Project</a>
    <span class="sep">/</span>
    <span>Day 49 · Analyze & Recommend</span>
    {status:week-10/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Analysis checklist at a glance

| Step | Activity |
|---|---|
| 1 | Compile comparison table + cost calculation |
| 2 | Write the claim sentence + recommendation |
| 3 | Build the 12-slide deck |
| 4 | Dry run with partner team (15 min talk + 10 min Q&A) |
| 5 | Revise based on dry-run feedback |

## Why this matters

The hiring signal isn't "did you run things on Capsule?" — it's **"can you defend a decision with evidence?"** Day 49 transforms yesterday's data into the story you'll tell on Day 50.

## Today's milestones

1. **Compile results into a comparison table** (template below).
2. **Calculate cost per request / per day / per month** for each config.
3. **Form the recommendation** — fill in the claim sentence.
4. **Identify the strongest counter-argument** — and have an answer ready for it.
5. **Build the 12-slide presentation** (outline below).
6. **Dry run with a partner team** — 15 min + 10 min Q&A. Take notes. Revise.

## The comparison table

Minimum columns:

| Config | TTFT p50 | TTFT p99 | Throughput (tok/s) | Quality (X/10 passes) | Cost ($/req) | Cost ($/month at projected load) |
|---|---|---|---|---|---|---|
| A — FP16, TP=1 | … | … | … | … | … | … |
| B — FP8, TP=1 | … | … | … | … | … | … |
| C — FP16, TP=2 | … | … | … | … | … | … |

The right answer is rarely the fastest or the cheapest — it's the one that **wins on the criteria you defined Monday**.

## The cost calculation

```
cost_per_request = (lease_$/hr ÷ 3600) × seconds_per_request
seconds_per_request = TTFT + (avg_output_tokens / throughput_per_request)

monthly_cost = cost_per_request × requests_per_day × 30
```

Show your work on a slide. Cite the lease rate from Capsule pricing or instructor sheet. Pessimistic assumptions beat optimistic ones — surprises in production hurt.

## The claim sentence (mandatory)

Every team's presentation lands here:

> "For use case **X**, deploy model **Y** at config **Z**, because **[evidence from benchmark]** shows **[metric]** at **[cost]**, with **[quality tradeoff]** that is **[acceptable / not]** because **[reasoning]**."

This is the entire deliverable in one sentence. The 12 slides exist to defend it.

## 12-slide outline

| # | Slide | Content |
|---|---|---|
| 1 | Title | Team, use case in one line |
| 2 | The user | Who needs this, what task, what success looks like |
| 3 | Why an LLM (vs not) | Justify the technology choice |
| 4 | Charter recap | Model + hardware + eval plan (1 slide) |
| 5 | Methodology | What you ran, how you measured |
| 6 | Comparison table | The full table |
| 7 | Latency story | Saturation curve + interpretation (Phase 1 vocabulary) |
| 8 | Quality story | Eval results + 1–2 illustrative example outputs |
| 9 | Cost story | The calculation + monthly projection |
| 10 | Recommendation | **The claim sentence**, large, on its own slide |
| 11 | Risks & limitations | What you didn't test, what could go wrong, what's gating production |
| 12 | What's next | If you had another week — what would you do? |

15 min + 10 min Q&A.

## Anticipate the Q&A

Three questions every panel will ask:

1. **"Why this model and not [bigger/smaller alternative]?"** — have the alternative's numbers ready or admit you didn't test it.
2. **"What's the failure mode in production?"** — at least one concrete answer (load spike, quality drift, cost overrun).
3. **"How would your recommendation change if [budget halves / quality bar rises / load 10×]?"** — show you understand the gradient.

If you can't answer all three, you're not done.

## Time budget for today

| Block | Minutes |
|---|---|
| Compile table + cost calc | 90 |
| Recommendation + claim sentence | 30 |
| Slide build | 120 |
| Dry run with partner team | 30 |
| Revise | 60 |

## Wrap-up

End of Day 49: each team has a polished 12-slide deck and can recite the claim sentence from memory. Day 50 is the show.

## Self-check before Day 50

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="week-10-m3-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day 49 · Analyze &amp; Recommend">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "What is the claim sentence format for a capstone recommendation?",
    "options": [
      "'Model X is the best choice because it is fast and accurate.'",
      "'For use case [specific task], deploy [model + config] because [3 data-backed reasons from your comparison table].'",
      "'Config A is better than config B across all metrics.'",
      "'We recommend GPU Y because it delivered the highest throughput in our tests.'"
    ],
    "answer": 1,
    "explain": "The lesson's claim sentence format: 'For use case X, deploy model Y at config Z, because [reason 1], [reason 2], [reason 3].' Each reason is a number from your table: 'meets TTFT < 800 ms P95 (charter criterion), passes 9/10 eval prompts, costs $0.003/req vs $0.011 for the FP16 baseline.' The claim sentence must be on slide 10 verbatim."
  },
  {
    "stem": "What are the required columns in the comparison table?",
    "options": [
      "Model, GPU, precision, test date",
      "TTFT p50, TTFT p99, throughput (tok/s), quality pass rate, cost per request, estimated monthly cost",
      "Concurrency, batch size, temperature, max tokens",
      "GPU memory, compute utilization, power consumption, temperature"
    ],
    "answer": 1,
    "explain": "The comparison table's required columns: TTFT p50 and p99 (latency percentiles from benchmark), throughput in tok/s (capacity), quality pass rate from eval suite, cost per request (lease$/hr ÷ 3600 × seconds/request), and estimated monthly cost at projected volume. This covers the SLO tripod: latency + quality + cost."
  },
  {
    "stem": "How is cost per request calculated from GPU lease cost?",
    "options": [
      "cost = model_size_GB × $/GB/hr",
      "cost = (lease $/hr) ÷ 3600 × (average request duration in seconds)",
      "cost = total monthly cost ÷ total requests per month",
      "cost = throughput (tok/s) ÷ (lease $/hr × 3600)"
    ],
    "answer": 1,
    "explain": "The formula from the lesson: cost/req = (lease $/hr ÷ 3600) × avg_seconds_per_request. If the GPU costs $2/hr and a request takes 1.5 seconds on average: $2/3600 × 1.5 = $0.00083/req. This lets you compare 'serve 1M requests at config A = $830' vs 'at config B = $1400' — a concrete economic argument for the recommendation."
  },
  {
    "stem": "What three questions should every capstone team anticipate from the review panel?",
    "options": [
      "Who is on the team, how long did it take, and what would you do differently?",
      "Why that model over the next-best alternative? What would break the recommendation? What would you measure next if given 2 more days?",
      "What GPU did you use, what was your TTFT, and what was your throughput?",
      "What is the project title, what is the use case, and what is the claim sentence?"
    ],
    "answer": 1,
    "explain": "The lesson's three predictable Q&A questions: (1) 'Why not model X instead of Y?' — requires knowing why your choice beats the runner-up on the specific criteria; (2) 'What assumption would break this recommendation?' — requires knowing your recommendation's weakest point; (3) 'What's next?' — requires a concrete follow-on experiment."
  },
  {
    "stem": "What does it mean that the winning config must win on the criteria defined in the charter, not just be fastest?",
    "options": [
      "The fastest config always wins by definition",
      "The recommendation is judged against the specific success criteria the team committed to on Day 47 — a config that is fastest but fails the quality threshold or costs 10× more doesn't win",
      "The criteria can be redefined on Day 49 if the data suggests different criteria",
      "Winning means all metrics are best — if one metric is worse, the config cannot be recommended"
    ],
    "answer": 1,
    "explain": "The charter defined success: 'P95 TTFT < 800 ms AND quality pass rate > 8/10 AND cost < $0.005/req.' The winning config is the one that satisfies all three criteria at the lowest cost. A config that is fastest (200 ms TTFT) but fails quality (5/10 prompts) doesn't win. A recommendation that rewrites its own success criteria isn't credible."
  },
  {
    "stem": "What is the purpose of slide 11 ('Risks & Limitations') in the 12-slide deck?",
    "options": [
      "To apologize for any shortcomings in the analysis",
      "To proactively acknowledge what wasn't tested, what could go wrong in production, and what is gating production deployment — demonstrating honest, defensible analysis",
      "To list the team members who weren't available to run certain configs",
      "To request more time or resources for a Phase 2"
    ],
    "answer": 1,
    "explain": "Slide 11 is intellectual honesty turned into a strength. 'We didn't test cold-start latency. We didn't test multi-tenant load. The gating issue for production is the SLA on the TURN relay.' Panel members respect this — it shows you know the limits of your data. A team that pretends their 4-day capstone is production-ready is less credible than one that names the gaps."
  },
  {
    "stem": "If your comparison table shows a latency-quality trade-off (config A is faster but config B passes more eval prompts), how do you make the recommendation?",
    "options": [
      "Always recommend the faster config — latency is always the primary concern",
      "Always recommend the higher-quality config — quality failures in production are worse than latency",
      "Return to the charter's success criteria: if the use case defined a quality threshold, config B wins if A fails it; if latency was the tighter constraint, A wins if B fails it",
      "Present both and refuse to make a recommendation without more data"
    ],
    "answer": 2,
    "explain": "The charter's success criteria are the tiebreaker. If the charter says 'P95 TTFT < 800 ms AND quality > 8/10', and config A has 400 ms TTFT but 6/10 quality (fails), while config B has 700 ms TTFT and 9/10 quality (passes), config B wins — it satisfies the charter. The recommendation must be derived from pre-committed criteria, not post-hoc preference."
  }
]
</script>
</div>

- [ ] The claim sentence is written and can be stated from memory
- [ ] Comparison table has all columns (TTFT p50/p99, throughput, quality, cost/req, cost/month)
- [ ] The three Q&A questions from "Anticipate the Q&A" section can be answered without hesitation
- [ ] Slides 5-10 tell a coherent story: methodology → data → recommendation

## Stuck?

Ask **oxtutor** to help you construct the cost calculation or to peer-review your claim sentence — it can check whether the sentence is defensible given your data.
