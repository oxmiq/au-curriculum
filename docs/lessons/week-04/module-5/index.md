# Day 20 (Fri) · Week 4 Consolidation

> **Goal of the day:** consolidate parallelism + speculative decoding + serving engines. No new content.

## What today is for

You've covered tensor parallelism, pipeline + expert parallelism, speculative decoding, and serving engines / continuous batching. Friday is the day to:

1. **Pass the knowledge check.** [Take the canonical knowledge check](knowledge-check.html) — parallelism (TP/PP/EP), speculation, batching, engines. Item bank: Problem Sets Day 19/20 ★.
2. **Submit the serving-system design assignment** — given 70B model, 8×H100, P99 < 500 ms, throughput 50 req/s → what config? Rubric: Worksheets Appendix C.
3. **Open-ended lab time.** Catch up; ask oxtutor to re-explain anything still fuzzy; generate extra practice.

## Self-check before Week 5

Week 4 turns Week 3's bottleneck knowledge into engineering decisions: *which* parallelism, *which* engine, *which* batching mode.

## Stuck?

Ask **oxtutor** to re-explain — the TP-vs-PP-vs-EP decision tree is the most-asked interview question of the entire program.
