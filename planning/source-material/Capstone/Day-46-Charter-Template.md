# Day 46 — Project Charter Template

> **Outcome of the day:** an approved one-page charter that your team commits to executing for the rest of the week.
> **Submission:** commit to your team's `capstone/<team-name>/charter.md`. Facilitator review by 3:00 PM.

---

## Schedule for Day 46

| Time | Activity |
|---|---|
| 0:00–0:30 | Form teams (2–3 people). Pick a use case (or propose one). |
| 0:30–1:30 | Draft the charter using the template below. |
| 1:30–2:00 | Peer review: trade charters with another team, leave comments. |
| 2:00–2:45 | Revise. Get facilitator sign-off. |
| 2:45–3:30 | Lab time: confirm Capsule access, list machines, do a dry-run benchmark on defaults. |

If your charter isn't signed off by 3:00 PM, you owe an hour of catch-up tonight.

---

## Charter template (copy into `capstone/<team-name>/charter.md`)

```markdown
# Capstone Charter — <team-name>

## Team
- Member 1 — role (e.g., "benchmarking lead")
- Member 2 — role (e.g., "evaluation lead")
- Member 3 — role (e.g., "presentation lead")

## Use case
*One paragraph. What does the system do? Who uses it? When?*

## Target shape (the constraints you're optimizing against)
- **Latency target:** P95 TTFT ≤ ___ ms (and / or P95 end-to-end ≤ ___ s)
- **Throughput target:** ≥ ___ tokens/sec, OR ≥ ___ req/sec at concurrency ___
- **Quality bar:** ___ (define what "good enough" means — name a measurable test)
- **Cost target:** ≤ $___ per 1M output tokens, OR ≤ $___ per 1K requests

## Candidate configurations to test (be explicit; you'll narrow on Day 47)
| # | Model | Quantization | GPU(s) | Parallelism | Concurrency |
|---|---|---|---|---|---|
| A | Llama-3.1-8B-Instruct | FP16 | 1×H100 | TP=1 | 1, 4, 16 |
| B | Llama-3.1-8B-Instruct | FP8 | 1×H100 | TP=1 | 1, 4, 16 |
| C | … | … | … | … | … |

(Aim for 3–5 candidate configurations. More than 5 = you'll run out of time. Fewer than 3 = you can't compare.)

## Evaluation plan
- **Benchmark tool:** `capsule benchmark` with backend ___ (vLLM / SGLang / TRT-LLM)
- **Eval prompts:** 10 prompts in `eval/prompts.json`. Categories: ___
- **Quality criterion per prompt:** ___ (e.g., "factually correct", "code compiles", "JSON parses")
- **How quantization regressions get caught:** ___ (e.g., "all 10 prompts re-run; manual diff vs. FP16 baseline")

## Risks
- *List 2–3 things that could derail your week. For each, write a mitigation.*

## Definition of done
- [ ] All candidate configs benchmarked at ≥3 concurrency levels.
- [ ] Eval suite run against FP16 baseline + all quantized variants.
- [ ] Comparison table built.
- [ ] Cost numbers computed.
- [ ] One-sentence recommendation written.
- [ ] 15-min slide deck rehearsed at least once.

## Sign-off
- Team approval: ___
- Facilitator approval (signature/initials): ___
- Date: ___
```

---

## Common charter pitfalls (facilitators will catch these)

| Pitfall | Why it kills the week | Fix |
|---|---|---|
| "Make it fast" as a target | Unmeasurable; you can't fail or pass | Name a number (P95 ≤ X ms) |
| 10 candidate configurations | Won't finish; can't compare | 3–5 maximum |
| Eval = "the model gives good answers" | Unverifiable | Define a per-prompt machine-checkable criterion |
| Single concurrency level | Won't surface throughput-vs-latency tradeoff | Always sweep at least 3 (1, 4, 16) |
| No FP16 baseline | Can't quantify quantization regression | Always include FP16 as the reference row |
| No cost math | The recommendation isn't actionable | Use Capsule's machine $/hr × runtime, or token-rate-based cost |

---

## Lab time (last 45 min of Day 46)

By end of session, every team must have:

1. ✅ Confirmed `capsule status` works for every member.
2. ✅ Run `capsule list` and identified ≥1 candidate machine for each configuration.
3. ✅ Dry-run `capsule benchmark` on default parameters for one of your configurations. Verified you get output. (You're not interpreting it yet — that's Day 47.)
4. ✅ Created `capstone/<team-name>/` folder in the practice repo with `charter.md` committed and pushed.

If any of the four is incomplete, escalate to facilitator before leaving. Don't wake up Day 47 still trying to reach the machine.
