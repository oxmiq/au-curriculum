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
    <span class="sep">·</span>
    <span class="duration">Full-day milestone</span>
    {status:week-10/module-3}
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

---

## Analysis checklist at a glance

| Step | Activity | Time budget |
|---|---|---|
| 1 | Compile comparison table + cost calculation | 90 min |
| 2 | Write the claim sentence + recommendation | 30 min |
| 3 | Build the 12-slide deck | 120 min |
| 4 | Dry run with partner team (15 min talk + 10 min Q&A) | 30 min |
| 5 | Revise based on dry-run feedback | 60 min |

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

- [ ] The claim sentence is written and can be stated from memory
- [ ] Comparison table has all columns (TTFT p50/p99, throughput, quality, cost/req, cost/month)
- [ ] The three Q&A questions from "Anticipate the Q&A" section can be answered without hesitation
- [ ] Slides 5-10 tell a coherent story: methodology → data → recommendation

## Stuck?

Ask **oxtutor** to help you construct the cost calculation or to peer-review your claim sentence — it can check whether the sentence is defensible given your data.
