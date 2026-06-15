# Day 20 (Fri) · Week 4 Consolidation

> **Goal of the day:** consolidate parallelism + speculative decoding + serving engines. No new content.

<!-- AUTO-GEN:LESSON-HEADER:START -->
<div class="ox-lesson-header" markdown="0">
  <div class="ox-lesson-header__crumbs">
    <a href="../../../">Home</a>
    <span class="sep">/</span>
    <a href="../../">Learn</a>
    <span class="sep">/</span>
    <a href="../">Week 4 — Scaling &amp; Stacks</a>
    <span class="sep">/</span>
    <span>Day 20 · Consolidation</span>
    <span class="sep">·</span>
    <span class="duration">Friday · review &amp; wrap</span>
    {status:week-04/module-5}
  </div>
  <div class="ox-lesson-header__cta">
    <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
    <a class="md-button md-button--primary" href="knowledge-check.html">Knowledge check</a>
    <a class="md-button" href="assignment.md">Assignment</a>
    <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
  </div>
</div>
<!-- AUTO-GEN:LESSON-HEADER:END -->

## What today is for

You've covered tensor parallelism, pipeline + expert parallelism, speculative decoding, and serving engines / continuous batching. Friday is the day to:

1. **Pass the knowledge check.** [Take the canonical knowledge check](knowledge-check.html) — parallelism (TP/PP/EP), speculation, batching, engines. Item bank: Problem Sets Day 19/20 ★.
2. **Submit the serving-system design assignment** — given 70B model, 8×H100, P99 < 500 ms, throughput 50 req/s → what config? Rubric: Worksheets Appendix C.
3. **Open-ended lab time.** Catch up; ask oxtutor to re-explain anything still fuzzy; generate extra practice.

## Self-check before Week 5

Week 4 turns Week 3's bottleneck knowledge into engineering decisions: *which* parallelism, *which* engine, *which* batching mode.

## Stuck?

Ask **oxtutor** to re-explain — the TP-vs-PP-vs-EP decision tree is the most-asked interview question of the entire program.
