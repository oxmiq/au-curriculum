# Widget Conversion — Canonical Pattern & Quality Rules

This directory contains per-week execution plans for converting every B7
Mon–Thu lesson from static `### Self-check` checkbox lists to the canonical
**interactive `ox-self-check` widget pattern** established in
`docs/lessons/week-04/module-1/index.md` (Day 16 · Tensor Parallelism).

---

## Directory structure

```
planning/widget-conversion/
├── README.md          ← you are here (canonical pattern + quality rules)
├── week-01.md         ← Day 1–4 execution plan
├── week-02.md         ← Day 6–9
├── week-03.md         ← Day 11–14
├── week-04.md         ← Day 17–19  (Day 16 = reference; already done)
├── week-05.md         ← Day 21–24  (requires Part-1 restructure)
├── week-06.md         ← Day 26–29
├── week-07.md         ← Day 32–35
├── week-08.md         ← Day 37–40
└── week-09.md         ← Day 42–45
```

---

## Canonical HTML structure

Each lesson receives **two** widget blocks. Copy this structure verbatim,
substituting the placeholders.

### Readiness widget (inside `## Part 1 — Pre-Reading Review + Readiness Check`)

```markdown
### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="WEEK-MODULE-readiness" data-kind="readiness" data-draw="5" data-source="SOURCE_LABEL">
<script type="application/json" class="ox-self-check__pool">
[
  { "stem": "...", "options": ["A", "B", "C", "D"], "answer": N, "explain": "..." },
  ...
]
</script>
</div>
```

### Wrap-up widget (inside `## Part 7 — Wrap-up & Connection`)

```markdown
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="WEEK-MODULE-wrapup" data-kind="wrap-up" data-draw="5" data-source="SOURCE_LABEL">
<script type="application/json" class="ox-self-check__pool">
[
  { "stem": "...", "options": ["A", "B", "C", "D"], "answer": N, "explain": "..." },
  ...
]
</script>
</div>
```

### `data-id` convention

| Slot | Format | Example |
|------|--------|---------|
| Readiness | `week-WW-mM-readiness` | `week-01-m2-readiness` |
| Wrap-up | `week-WW-mM-wrapup` | `week-01-m2-wrapup` |

### `data-source` convention

Use the bolded label from the lesson's pre-reading frontmatter. Examples:

| Lesson | `data-source` |
|--------|---------------|
| Day 2 | `MIT Missing Semester — Shell chapter` |
| Day 11 | `Reader 4 — Attention Math + Reader 6 — Serving` |
| Day 26 | `Anthropic Prompt Engineering Tutorial Ch1+Ch2` |
| Day 33 | `Capsule Power User Lab Guide Modules 1+2` |

---

## JSON schema (per question object)

```json
{
  "stem":    "<string — question text; may use HTML <code>, <em>, <strong>>",
  "options": ["<string>", "<string>", "<string>", "<string>"],
  "answer":  <integer 0–3, index into options[]>,
  "explain": "<string — 1–3 sentences referencing specific Part or concept>"
}
```

**Rules:**
- `options` must contain **exactly 4** entries.
- `answer` is **0-indexed** (first option = 0).
- JSON must be valid — no trailing commas, no unescaped quotes inside strings.
  Use `\u2019` for curly apostrophe, `<code>` for monospace, etc.
- Pool size: **20 questions** per widget. `data-draw="5"` draws 5 at random
  per attempt, so 20 items gives meaningful variety across attempts.

---

## Question quality bar

### Tone
- **Neutral, precise, slightly terse.** Identical to a well-written exam
  question. No em-dash banter, no casual hedges ("sort of", "basically").
- **Technical vocabulary throughout.** Use the lesson's exact terms: don't
  paraphrase "HBM" as "memory" or "TTFT" as "response time".
- Stems may reference the lesson by Part: *"Per Part 3 of this lesson…"* or
  *"The lesson calls this the 'roofline model'. According to Part 2…"*.

### Difficulty distribution (per 20-question pool)
| Level | Count | Description |
|-------|-------|-------------|
| Recall | 6 | Direct definition or fact stated in the reading/lesson |
| Apply | 8 | Apply a formula, classify a scenario, or identify the correct rule |
| Analyse | 6 | Compare two concepts, identify a failure mode, or reason about a tradeoff |

Mix the levels throughout the pool — do **not** cluster all recall questions
at the top.

### Distractor style
- **Three plausible distractors** per question. Each distractor should be
  wrong in a specific, identifiable way (not obviously absurd).
- **Common distractor patterns:**
  - A closely related but distinct concept (e.g., "pipeline parallelism"
    when the correct answer is "tensor parallelism")
  - A number that is off by a factor (2×, ÷2) from the correct value
  - A statement that is true in a different context than the question asks
  - The inverse of the correct answer
- **Avoid:** distractors that are obviously nonsensical, too long relative to
  the correct answer, or that accidentally make the correct answer obvious by
  elimination.

### Explain field
- Must reference **where** in the lesson the concept appears: *"From Part 3's
  memory-hierarchy table…"*, *"Per the roofline diagram in Part 2…"*, *"The
  pre-reading (Reader 5) defines this as…"*.
- Length: 1–3 sentences. Not a re-statement of the stem — explain *why* the
  correct answer is correct and what makes the distractors wrong.
- May include a brief formula reminder: *"140 GB ÷ 8 GPUs = 17.5 GB."*

### Readiness vs wrap-up distinction
| Widget | Tests | Source material |
|--------|-------|-----------------|
| Readiness | **Pre-reading** content only — concepts, definitions, and facts the student was expected to absorb before class | The cited Reader / Lab Guide module / external article |
| Wrap-up | **Lesson body** content — everything taught in Parts 2–6 of that day, including exercises and worked examples | The lesson's own `## Part 2` through `## Part 6` sections |

Do **not** mix these. A readiness question that tests lesson content (not in
the pre-reading) or a wrap-up question that only tests the pre-reading title
is a defect.

---

## Per-week workflow (for the agent executing a week plan)

1. **Read this README** in full.
2. **Read the week plan file** (`week-NN.md`) for the lesson being converted.
3. **Read the lesson file** in full (`docs/lessons/week-NN/module-M/index.md`).
4. **Read the pre-reading source file** if it is in the repo
   (e.g., `planning/source-material/Inference Engineering/
   Inference_Engineering_Pre_Lecture_Reading.md` — locate the relevant Reader
   section by line number from the week plan).
5. **Author 20 readiness questions** from the pre-reading source. Verify:
   - Each question maps to a specific passage in the pre-reading.
   - No question requires lesson content that hasn't been read yet.
6. **Author 20 wrap-up questions** from the lesson body (Parts 2–6). Verify:
   - Each question maps to a specific Part of that lesson.
   - No question repeats a readiness question verbatim.
7. **Insert widgets** using `replace_string_in_file`:
   - Readiness widget: replace `### Readiness Check\n\nNot gated…` block
     (the existing prose) with the full widget div.
   - Wrap-up widget: replace the `### Self-Check` / `### Self-check` block
     (the checkbox list) with the full widget div.
8. **Remove** the now-orphaned static `### Self-Check` checkbox block (if
   it was not already replaced in step 7).
9. **Validate**: `mkdocs build --strict 2>&1 | grep -E "^(WARNING|ERROR)"` —
   must return empty. Malformed JSON in a `<script>` tag will produce a
   build warning.
10. **Commit** after each lesson (not each week) so diffs stay reviewable:
    `git commit -m "feat(quiz): add readiness + wrap-up widgets to Day NN · <title>"`

---

## Pre-reading source map

| Weeks | Subject | Source file (relative to repo root) |
|-------|---------|--------------------------------------|
| 1 | Orientation | `planning/source-material/Orientation/Pre-Lecture-Reading.md` |
| 1 (m2) | Shell | External: MIT Missing Semester (lesson body summary is authoritative) |
| 1 (m3) | Git | External: Atlassian Git Tutorial (lesson body summary is authoritative) |
| 1 (m4) | GPU Primer | Facilitator video (no URL); use lesson body summary for readiness Qs |
| 2–5 | Inference Engineering | `planning/source-material/Inference Engineering/Inference_Engineering_Pre_Lecture_Reading.md` |
| 6 (m1) | Prompt Engineering | `planning/source-material/Prompt Engineering/Prompt-Engineering-Pre-Lecture-Reading.md` |
| 6 (m2–m4) | AI Agents | `planning/source-material/AI Agents/AI Agents - Pre-Lecture Reading.md` (Student Guide modules) |
| 7–9 | Capsule Power User | `planning/source-material/Capsule Power User/Capsule-Power-User-Lab-Guide.md` |

### Inference Engineering Reader line numbers

| Reader | Lines in Pre_Lecture_Reading.md | Used by |
|--------|---------------------------------|---------|
| Reader 1 — AI in production | ~63–166 | Day 6 (week-02/m1) |
| Reader 4 — Complexity, memory, attention | ~379–483 | Day 9 (w02/m4), Day 11 (w03/m1), Day 12 (w03/m2), Day 13 (w03/m3) |
| Reader 5 — Computer architecture | ~484–587 | Day 7 (w02/m2), Day 8 (w02/m3) |
| Reader 6 — Software stack for ML | ~588–725 | Day 11 (w03/m1), Day 18 (w04/m3), Day 19 (w04/m4) |
| Reader 7 — Numerical precision | ~726–852 | Day 14 (w03/m4) |
| Reader 8 — Parallel computing | ~853–956 | Day 16 (w04/m1 — reference), Day 17 (w04/m2) |
| Reader 10 — Distributed systems for production | ~1053–1232 | Day 21–24 (week-05) |

---

## Special cases

### week-01/module-1 (Day 1 · Welcome & Context)
No pre-reading — **Self-Check widget only** (no Readiness widget). The
`## Part 1` heading is not a Pre-Reading Review; leave it unchanged. Add
only the wrap-up widget inside `## Part 7`.

### week-05/module-1 through module-4 (Days 21–24)
These lessons do **not** have `## Part 1 — Pre-Reading Review + Readiness
Check`. Their existing Part 1 is a content part. Before adding widgets,
restructure each file:
1. Prepend a new `## Part 1 — Pre-Reading Review + Readiness Check · 15 min`
   section (with `### Before You Start` + `### Readiness Check` + widget).
2. Renumber existing Parts 1–6/7 → 2–7/8 throughout the file, including
   the lesson-plan table.
The week-05 plan file documents the exact renumbering for each lesson.

### week-09/module-2 (Day 43 — no new pre-reading)
Pre-reading is "none new — builds on Day 42 + recalls Week 3–4". The
Readiness widget should test **Day 42 content** (benchmark anatomy, report
fields, artifact conventions) rather than an external source. Set
`data-source="Day 42 · Your First Benchmark"`.

---

## Ambiguities resolved

| Ambiguity | Resolution |
|-----------|------------|
| Reader N files — accessible? | Yes — all in `planning/source-material/Inference Engineering/Inference_Engineering_Pre_Lecture_Reading.md`. Line ranges in table above. |
| week-01/m4 facilitator video — no URL | Author readiness questions from the lesson's own Part 2–5 GPU content (the lesson re-teaches the video). |
| week-09/m2 no pre-reading | Use Day 42 lesson content as readiness source; set `data-source="Day 42 · Your First Benchmark"`. |
| week-05 Part 1 not Pre-Reading Review | Prepend new Part 1 + renumber (see Special Cases above and week-05.md). |
| week-06/m1 supplementary files (02, 03, 04) | These supplement the main Day 26 lesson but are not tested in readiness/wrap-up widgets for Day 26. |
| AI Agents Student Guide modules — accessible? | Yes — `planning/source-material/AI Agents/AI Agents - Student Guide.md` and `AI Agents - Pre-Lecture Reading.md`. |
| Capsule Lab Guide modules — accessible? | Yes — `planning/source-material/Capsule Power User/Capsule-Power-User-Lab-Guide.md`. |
