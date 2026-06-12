# Day 49 — Panel Presentation & Assessment Rubric

> **Outcome of the day:** every team presents to a panel (Oxmiq engineers + facilitators) and receives scored feedback.
> **Mindset:** this is a job-interview-quality presentation. Panels include engineers who may hire you.

---

## Schedule for Day 49

| Time | Activity |
|---|---|
| 0:00–0:30 | Final tech check. Presentation order announced. |
| 0:30–3:00 | Team presentations: 15 min talk + 10 min Q&A + 5 min panel deliberation. |
| 3:00–3:30 | Panel announces top finding(s), shares cross-team observations. |

A panel of 3–4 (mix of Oxmiq engineers and facilitators) scores each team independently using the rubric below, then averages.

---

## Rubric — 100 points total

### 1. Engineering reasoning (30 pts)

| Score | Descriptor |
|---|---|
| 27–30 | Charter constraints are explicit and quantified. One knob varied per experiment. Configurations chosen explained by *expected* tradeoff (not just "let's try stuff"). Negative results acknowledged. |
| 22–26 | Mostly disciplined. Maybe one configuration choice unexplained. Charter has minor gaps. |
| 16–21 | Several knobs varied per run; some results uninterpretable. Charter targets are vague. |
| 0–15 | Ad-hoc experimentation. No baseline. No coherent argument. |

### 2. Evidence quality (25 pts)

| Score | Descriptor |
|---|---|
| 23–25 | Baseline + sweep + eval suite all present. Numbers reproducible from committed repo. Cost math correct. Quality regressions surfaced and named. |
| 18–22 | All ingredients present, one or two small gaps (e.g., one sweep skipped, one cost number off). |
| 13–17 | Missing baseline OR missing eval OR missing cost. Single-data-point claims. |
| 0–12 | Anecdotal. "It seemed fast." No table. No reproducible numbers. |

### 3. Recommendation clarity (20 pts)

| Score | Descriptor |
|---|---|
| 18–20 | One sentence. Names use case, model, config, evidence, cost, quality tradeoff, and justification. Actionable tomorrow. |
| 14–17 | Recommendation present but missing one or two slots from the template. |
| 9–13 | Recommendation is vague ("FP8 is best"). Doesn't connect to use case. |
| 0–8 | No recommendation. Or contradictory recommendations across slides. |

### 4. Presentation quality (15 pts)

| Score | Descriptor |
|---|---|
| 13–15 | Within time. Every team member speaks. Slides have axis labels, units, readable fonts. Smooth transitions. |
| 10–12 | Within time but one or two rough patches. Slides mostly clean. |
| 6–9 | Overran time, OR one team member dominated, OR slides hard to read. |
| 0–5 | Significant overrun. Unreadable slides. Visible team coordination failure. |

### 5. Q&A handling (10 pts)

| Score | Descriptor |
|---|---|
| 9–10 | Answers grounded in their own data ("our benchmark showed X"). Honest about unknowns. Distinguishes "we didn't test" from "we tested and it failed." |
| 7–8 | Mostly grounded. One or two answers slipped into generalities. |
| 4–6 | Several "I think" answers when the data would have answered. |
| 0–3 | Defensive. Speculates beyond data. Won't admit unknowns. |

---

## Panel scoring sheet (one per panelist per team)

```markdown
# Team: <team-name>     Panelist: <name>

## Scores
- Engineering reasoning: __ / 30
- Evidence quality: __ / 25
- Recommendation clarity: __ / 20
- Presentation quality: __ / 15
- Q&A handling: __ / 10
- **Total: __ / 100**

## One-paragraph written feedback (required, will be shared with team)
*What was strongest? What's the one thing that would have moved this to the next tier?*

## Hiring-signal note (panelists from Oxmiq only; private)
*Did anyone on this team stand out as someone we should fast-track for an interview? Name + 1-sentence reason.*
```

---

## Peer feedback form (one per audience team, per presentation)

```markdown
# Audience team: <name>     Presenting team: <name>

- One thing I'll steal from your approach: ___
- One number from your slides I'd push back on: ___
- One question I wanted to ask but didn't: ___
```

Submit at end of day. Facilitators compile and share with presenters before Day 50.

---

## Common Q&A questions panels ask (prepare answers)

- "Why this model and not <larger / smaller / different family>?"
- "Why this engine (vLLM / SGLang / TRT-LLM)?"
- "What did you NOT test, and why?"
- "What would you change if your latency target halved?"
- "What would you change if your budget halved?"
- "Did quantization break anything subtle that your eval missed?"
- "How would this scale to 10× the load?"
- "What's the failure mode if the GPU goes down? What's your fallback?"
- "If I gave you another week, what would you do first?"

Practice answers in your dry-run on Day 48. Two-sentence answers beat two-minute monologues.

---

## End of Day 49

- [ ] All team presentations complete.
- [ ] Panel scores averaged and recorded.
- [ ] Peer feedback collected.
- [ ] Top 1–2 recommendations flagged for Oxmiq follow-up.
- [ ] Each team receives their panel feedback before Day 50 retrospective.
