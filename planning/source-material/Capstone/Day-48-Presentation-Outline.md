# Day 48 — Analyze, Recommend & Build the Deck

> **Outcome of the day:** comparison tables, cost numbers, one-sentence recommendation, and a rehearsed 15-min slide deck.
> **Mindset:** you're not writing a research paper. You're writing a memo a manager will act on tomorrow.

---

## Schedule for Day 48

| Time | Activity |
|---|---|
| 0:00–0:30 | Standup. Each team summarizes yesterday's data in 60 seconds. |
| 0:30–1:30 | Build the comparison tables. Compute costs. Pick the winner. |
| 1:30–2:30 | Build the slide deck using the outline below. |
| 2:30–3:00 | Dry-run the talk in front of one other team. Get feedback. |
| 3:00–3:30 | Revise. Commit final deck + recommendation. |

---

## Step 1 — Build the comparison table (30 min)

One row per configuration. Required columns:

| # | Config | TTFT P95 (ms) | TPS | Throughput (req/s) | Eval pass / 10 | $/1M output tokens | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Llama-3.1-8B FP16 1×H100 c=16 | | | | | | baseline |
| 2 | Llama-3.1-8B FP8 1×H100 c=16 | | | | | | |
| ... | | | | | | | |

**Cost formula:**

$$\text{cost per 1M output tokens} = \frac{\text{\$/hr of GPU(s)}}{\text{TPS} \times 3600} \times 10^6$$

Worked example: 1×H100 at $2/hr, 214 TPS sustained ⇒ $2 / (214 × 3600) × 10⁶ = **$2.60 per 1M output tokens**.

If your team is serving requests (not just tokens), also compute **$/1K requests** at your concurrency level. Manager-friendly number.

---

## Step 2 — Pick the winner (15 min)

Lay your charter's target shape over the table. Cross out any row that fails a hard constraint. Of the survivors, pick the cheapest (or the fastest, if cost ties).

If **no row survives all constraints**, that is a legitimate finding. Your recommendation becomes: *"None of the tested configurations meet [constraint X]. Closest is [config Y], which misses by [Z]. To meet the constraint we'd need to [option A or B]."* Honest negative results are valuable.

---

## Step 3 — Write the one-sentence recommendation (10 min)

Fill in the template:

> *"For [use case], deploy [model] at [config], because [benchmark evidence] shows [metric] at [cost], with [quality tradeoff] that is [acceptable / not] because [reasoning]."*

Rules:
- Every bracketed slot must contain a real number from your table.
- The "quality tradeoff" slot must reference your eval-suite result, not vibes.
- The "acceptable / not" justification must reference the use case's tolerance.

Bad: *"FP8 is good because it's faster and almost as accurate."*

Good: *"For a customer-support chatbot serving 5K queries/hour at P95 ≤ 800 ms, deploy Llama-3.1-8B-Instruct at FP8 on 1×H100 with continuous batching (concurrency=16), because Capsule benchmarks show 214 tokens/sec with P95 TTFT of 480 ms at $2.60 per 1M output tokens, with a 1.8-point drop on our 20-prompt eval suite that is acceptable because the failures are formatting-only, not factual."*

---

## Step 4 — Slide deck outline (15 slides, ~60 sec each)

| Slide | Content | Owner |
|---|---|---|
| 1 | Title — team, project name, one-sentence pitch | Presentation lead |
| 2 | The use case (one paragraph + target shape table) | Use-case owner |
| 3 | Method — candidate configs, what we varied, what we held constant | Benchmarking lead |
| 4 | Setup — model, hardware, engine, eval prompts (one table) | Benchmarking lead |
| 5 | Results table — full comparison matrix | Benchmarking lead |
| 6 | TTFT chart — bar chart, candidates side-by-side | Benchmarking lead |
| 7 | TPS / throughput chart — same | Benchmarking lead |
| 8 | Eval-suite results — pass rate per config + notable regressions | Evaluation lead |
| 9 | Cost chart — $/1M output tokens per config | Evaluation lead |
| 10 | The winner — config + why it won | Whole team |
| 11 | The recommendation — the one sentence, large font, centered | Whole team |
| 12 | What surprised us — 2–3 bullets | Whole team |
| 13 | What we'd do with another week — 2–3 bullets | Whole team |
| 14 | Connect back — which Weeks 1–9 concepts mattered most | Whole team |
| 15 | Thanks + Q&A | Whole team |

Notes:
- Every chart must have axis labels and units. No bare numbers.
- No screenshots of terminal output (illegible). Re-tabulate.
- Use one font + one accent color. Don't theme.

---

## Step 5 — Dry-run (30 min, in front of another team)

1. Set a 15-minute timer. Present start-to-finish. Don't stop.
2. The other team writes down: (a) which slide confused them, (b) one number they don't believe, (c) one question they want to ask in Q&A.
3. Swap. You give them the same feedback.
4. Revise the slides that confused. Re-rehearse the parts that ran long.

Teams that skip the dry-run reliably overrun. Don't be that team.

---

## End-of-day commits

- [ ] `slides/<team-name>.pdf` and source (Keynote / Google Slides export / Markdown)
- [ ] `recommendation.md` — the one-sentence recommendation + the comparison table
- [ ] `cost-analysis.md` — the cost math worked out
- [ ] Conventional-commit message: `feat(capstone): day 48 analysis + recommendation + deck`

---

## Common Day 48 pitfalls

| Pitfall | Fix |
|---|---|
| "We'll let the data speak for itself" | Data never speaks. Write the recommendation. |
| Picking the fastest config without checking the eval | Fast + wrong = useless. Always check eval first. |
| Cost computed at wrong concurrency | Use sustained throughput at the target concurrency, not peak. |
| Slides full of bullets, no numbers | Replace bullets with the table. Numbers persuade. |
| One person owns the presentation | Every team member presents at least one slide. The panel will ask each member a question. |
| Skipping the dry-run | You'll overrun and lose the Q&A buffer. |
