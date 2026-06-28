# Question Pool Implementation Plan

> Created: 2026-06-27
> Purpose: Document the work required to add Readiness-check, Self-check, and Knowledge-check question pools to all applicable lessons.

---

## Executive Summary

| Feature | Current State | Required Work |
|---------|---------------|---------------|
| Q&A Wizard | Not implemented | Not in scope |
| Readiness-check pools | 4 of 51 modules (~8%) | Add to ~40 modules |
| Self-check pools | 5 of 51 modules (~10%) | Add to ~46 modules |
| Friday Knowledge-check | 7 of 10 weeks have questions | Create for weeks 6, 7, 10 |

---

## Implementation Pattern

All question pools use the same HTML + JSON pattern:

### Readiness-check Template

```markdown
### Readiness Check

Not gated; the score nudges you to re-read or to ask OxTutor before continuing.

<div class="ox-self-check" data-widget="self-check" data-id="WEEK-MODULE-readiness" data-kind="readiness" data-draw="5" data-source="PRE-READ TITLE">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0,
    "explain": "Explanation of correct answer"
  },
  ... more questions (minimum 5-10 recommended)
]
</script>
</div>
```

### Self-check Template

```markdown
### Self-Check

Not gated; the score nudges you to revisit specific sections or ask OxTutor before moving on.

<div class="ox-self-check" data-widget="self-check" data-id="WEEK-MODULE-wrapup" data-kind="wrap-up" data-draw="5" data-source="Day X · Lesson Title">
<script type="application/json" class="ox-self-check__pool">
[
  {
    "stem": "Question text",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0,
    "explain": "Explanation of correct answer"
  },
  ... more questions (minimum 5-10 recommended)
]
</script>
</div>
```

### Knowledge-check.html Template

See existing file at `docs/lessons/week-01/module-1/knowledge-check.html` for the full template.

---

## Phase 1: Fix Friday Knowledge-check.html Files (Week 6, 7, 10) ✅ COMPLETE

**Priority: HIGH** - These are blocking issues for Friday consolidation

| Week | File | Current State | Status |
|------|------|---------------|--------|
| week-06 | `docs/lessons/week-06/module-5/knowledge-check.html` | ✅ 20 questions | Done |
| week-07 | `docs/lessons/week-07/module-5/knowledge-check.html` | ✅ 15 questions | Done |
| week-10 | `docs/lessons/week-10/module-5/knowledge-check.html` | ✅ Intentional stub — `questions: []` by design | Capstone week has no canonical KC; only assessed artifact is the capstone deliverable (40% of grade) + Day 50 panel. File exists for progress-tooling slot detection only. |

---

## Phase 2: Add Readiness-check Pools

**Priority: MEDIUM** - Based on pre-read materials

Readiness-checks should be added to modules that have pre-reading assignments.

### Module List by Week

#### week-01 (4 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | None — first day | ❌ Skip | No pre-read |
| module-2 | MIT Missing Semester — Shell | ✅ Already exists | Verify questions |
| module-3 | Atlassian Git Tutorial | ✅ Already exists | Verify questions |
| module-4 | GPU Explained (YouTube) | ✅ Already exists | Verify questions |
| module-5 | Friday consolidation | ❌ Skip | No pre-read |

#### week-02 (4 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Chip Huyen — LLM Engineering | ❌ Missing | Add pool |
| module-2 | NVIDIA H100 GPU Datasheet | ❌ Missing | Add pool |
| module-3 | Horace He — Bandwidth | ❌ Missing | Add pool |
| module-4 | Horace He — Compute | ❌ Missing | Add pool |
| module-5 | Friday consolidation | ❌ Skip | No pre-read |

#### week-03 (4 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Databricks — Prefill/Decode | ❌ Missing | Add pool |
| module-2 | KV Caching Explained | ❌ Missing | Add pool |
| module-3 | FlashAttention + PagedAttention | ❌ Missing | Add pool |
| module-4 | Hugging Face — Quantization | ❌ Missing | Add pool |
| module-5 | Friday consolidation | ❌ Skip | No pre-read |

#### week-04 (3 modules need readiness-check - module-1 already exists)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Hugging Face — Tensor Parallel | ✅ Already exists | Verify questions |
| module-2 | Lilian Weng — PP + MoE | ❌ Missing | Add pool |
| module-3 | Lilian Weng — Spec Decoding | ❌ Missing | Add pool |
| module-4 | vLLM + Continuous Batching | ❌ Missing | Add pool |
| module-5 | Friday consolidation | ❌ Skip | No pre-read |

#### week-05 (4 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Anyscale — Latency/Throughput | ❌ Missing | Add pool |
| module-2 | Chip Huyen — Deploying ML | ❌ Missing | Add pool |
| module-3 | Hugging Face Evaluate + Eugene Yan | ❌ Missing | Add pool |
| module-4 | a16z — Economics of AI | ❌ Missing | Add pool |
| module-5 | Friday consolidation | ❌ Skip | No pre-read |

#### week-06 (5 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Prompt Engineering Pre-Lecture | ❌ Missing | Add pool |
| module-2 | Prompt Engineering (Roles) | ❌ Missing | Add pool |
| module-3 | AI Agents — Tools & MCP | ❌ Missing | Add pool |
| module-4 | AI Agents — Governance | ❌ Missing | Add pool |
| module-5 | AI Agents — Orchestration | ❌ Missing | Add pool |

#### week-07 (4 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | AI Agents Pre-Lecture + Case Studies | ❌ Missing | Add pool |
| module-2 | Capsule Power-User (Day 36) | ❌ Missing | Add pool |
| module-3 | Capsule Power-User (Day 36) | ❌ Missing | Add pool |
| module-4 | Capsule Power-User (Day 37) | ❌ Missing | Add pool |

#### week-08 (4 modules need readiness-check)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Capsule Power-User (Day 38) | ✅ Already exists | Verify questions |
| module-2 | Capsule Power-User (Day 39) | ✅ Already exists | Verify questions |
| module-3 | Capsule Power-User (Day 39) | ✅ Already exists | Verify questions |
| module-4 | Capsule Power-User (Day 40) | ✅ Added 2026-06-27 | Done |

#### week-09 (3 modules need readiness-check - verify pre-reads exist)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | Capsule Power-User (Day 41) | ✅ Added 2026-06-27 | Done |
| module-2 | none new | ❌ Skip | No pre-read ("builds on Day 42") |
| module-3 | Capsule Power-User (Day 43) | ✅ Added 2026-06-27 | Done |
| module-4 | Capsule Power-User (Day 44) | ✅ Added 2026-06-27 | Done |

#### week-10 (0 modules - capstone week)
| Module | Pre-read | Status | Action |
|--------|----------|--------|--------|
| module-1 | (none listed) | ❌ Skip | Verify |
| module-2 | (none listed) | ❌ Skip | Verify |
| module-3 | (none listed) | ❌ Skip | Verify |
| module-4 | (none listed) | ❌ Skip | Verify |

---

## Phase 3: Add Self-check Pools ✅ COMPLETE

**Priority: MEDIUM** - Based on lesson content

Self-checks should be added to ALL modules except Friday consolidation (module-5).

### Module List by Week

#### week-01
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Already exists | Verified |
| module-3 | ✅ Already exists | Verified |
| module-4 | ✅ Already exists | Verified |
| module-5 | ✅ Already exists | Verified |

#### week-02 (4 modules)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-03 (4 modules)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-04 (4 modules - module-1 exists)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Already exists | Verified |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-05 (4 modules)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-06 (5 modules + module-6)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |
| module-6 | ✅ Added | Done |

#### week-07 (4 modules)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-08 (4 modules)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-09 (4 modules)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ❌ Skip | Friday |

#### week-10 (4 modules + module-5)
| Module | Status | Action |
|--------|--------|--------|
| module-1 | ✅ Added | Done |
| module-2 | ✅ Added | Done |
| module-3 | ✅ Added | Done |
| module-4 | ✅ Added | Done |
| module-5 | ✅ Added | Done |

---

## Implementation Sequence

### Step 1: Fix Friday Knowledge-check.html Files ✅ COMPLETE
**Files:** week-06 (20 q), week-07 (15 q), week-10 (intentional stub — capstone week, no KC by design)

### Step 2: Add Readiness-check Pools (Weeks 2-5) ✅ COMPLETE
All of week-02/modules 1-4, week-03/modules 1-4, week-04/modules 2-4, week-05/modules 1-4 have readiness pools.

### Step 3: Add Readiness-check Pools (Weeks 6-9) ✅ COMPLETE
All of week-06/modules 1-5, week-07/modules 1-4, week-08/modules 1-4, week-09/modules 1, 3, 4 have readiness pools. week-09/module-2 correctly has no readiness check ("builds on Day 42", no new pre-read).

### Step 4: Add Self-check Pools (Weeks 2-5) ✅ COMPLETE
All of week-02/modules 1-4, week-03/modules 1-4, week-04/modules 2-4, week-05/modules 1-4 have self-check pools with stems > draw=5.

### Step 5: Add Self-check Pools (Weeks 6-10) ✅ COMPLETE
All modules complete including week-10/modules 1-5. All 44 self-check pools have stems > draw=5 (minimum 7 questions per pool, enabling C(7,5)=21+ unique draw combinations).

### Step 6: Add week-01/module-1 Readiness & Self-check ✅ COMPLETE
- Self-check: ✅ Added (7 questions, draw=5)
- Readiness: ✅ Correctly skipped — Phase 2 table explicitly designates module-1 "No pre-read / first day"

---

**Overall Implementation Status: ALL STEPS COMPLETE**

Post-completion quality audit (2026-06-28): All 44 self-check pools verified to have `stems > data-draw` to enable randomization. All Friday knowledge-check.html files for weeks 01-09 confirmed populated (15-20 questions each). Week-10 KC is an intentional stub by design.

---

## Question Authoring Guidelines

### Readiness-check Questions
- Based on the pre-reading material
- Test understanding of key concepts from the pre-read
- Should be answerable after completing the pre-read
- Minimum 5 questions recommended (data-draw="5")

### Self-check Questions
- Based on the lesson content (not pre-read)
- Test understanding of core concepts taught in the lesson
- Should be answerable after completing the lesson
- Minimum 5 questions recommended (data-draw="5")

### Question Format
```json
{
  "stem": "Question text (what is being asked)",
  "options": [
    "Option A (incorrect)",
    "Option B (correct)",
    "Option C (incorrect)",
    "Option D (incorrect)"
  ],
  "answer": 1,
  "explain": "Explanation of why the correct answer is right and why others are wrong"
}
```

### Best Practices
1. Each question should have exactly ONE correct answer
2. Distractors (wrong options) should be plausible
3. Explanation should reference specific parts of the source material
4. Question pool should have at least 5-10 questions to allow for variety (data-draw pulls random questions)

---

## Reference Files

### Existing Implementation
- `docs/lessons/week-01/module-2/index.md` - Has both Readiness-check and Self-check with full question pools
- `docs/lessons/week-01/module-1/knowledge-check.html` - Full HTML template for Friday knowledge check

### Files to Modify (Readiness-check)
The readiness-check section should be added after "## Part 1 — Pre-Reading Review" heading, replacing any existing stub.

### Files to Modify (Self-check)
The self-check section should be added at the end of Part 7 (Wrap-up & Connection), replacing any existing stub.

---

## Verification Commands

After implementing, verify with:

```bash
# Count Readiness-check sections
grep -c 'data-kind="readiness"' docs/lessons/*/module-*/index.md

# Count Self-check sections
grep -c 'data-kind="wrap-up"' docs/lessons/*/module-*/index.md

# Check Friday knowledge-check files
for f in docs/lessons/week-*/module-5/knowledge-check.html; do
  if grep -q "questions: \[\]" "$f"; then
    echo "STUB: $f"
  else
    echo "HAS QUESTIONS: $f"
  fi
done
```

---

## Notes

1. **Q&A Wizard**: Not implemented in current curriculum - not in scope
2. **Week-01/module-1**: Has no pre-read, so Readiness-check not applicable
3. **Friday consolidation (module-5)**: No Readiness-check needed (no pre-read), Self-check is in knowledge-check.html
4. **Week-10**: Verify if pre-reads exist before adding Readiness-check
5. **Question pools**: Must be authored per lesson - requires subject matter expertise

---

*End of Document*