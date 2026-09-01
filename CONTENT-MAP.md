# Content Map & Architecture

How the curriculum site is organized and how content flows from source files to
the rendered site. This is the maintainer's companion to
[CONTRIBUTING.md](CONTRIBUTING.md) (workflow) and
[LESSON_TEMPLATE.md](LESSON_TEMPLATE.md) (per-lesson shape).

- **Stack:** [MkDocs Material](https://squidfunk.github.io/mkdocs-material/), OxBlood brand (cream + oxblood, single light scheme).
- **Nav source of truth:** [`mkdocs.yml`](mkdocs.yml).
- **Content source of truth:** the `docs/` filesystem.
- **Guardrails:** `scripts/audit_lessons.py` (rules L001–L015) + `mkdocs build --strict` in CI.

At a glance: **~176 content pages** across 4 nav tabs, 10 weeks × 5 daily modules,
3 interactive knowledge-base pages, driven by build scripts and 1 build-time hook.

---

## 1. Navigation structure

The site presents four verb-style top tabs (`navigation.tabs`). Everything
below is declared in the `nav:` block of [`mkdocs.yml`](mkdocs.yml).

| Tab | Pages | Contents |
|-----|-------|----------|
| **🏠 Home** | 2 | `index.md` (Welcome), `rationale.md` (Why this curriculum) |
| **📚 Learn** | 61 | `curriculum.md` + 10 week overviews + 50 daily lessons |
| **🗺️ Plan** | 2 | `roadmap.md` (progress-aware sitemap) + Interactive Concept Graph |
| **📖 Reference** | 3 | Glossary, Concepts, Flashcards |

Progress is surfaced on the **Roadmap** itself (per-week + overall bars, a "next up" flag) and via status pills on lesson pages; there is no separate progress tab.

### The 10 weeks (3 phases)

| Phase | Weeks | Focus |
|-------|-------|-------|
| **Phase 1 - Inference Engineering** | 1–5 | Foundations, the GPU & memory, attention & KV cache, scaling & stacks, metrics & production |
| **Phase 2 - Prompt & Agents** | 6 | Prompt engineering, agent fundamentals, tools, governance, orchestration |
| **Phase 3 - Capsule** | 7–10 | Bridge → connections & operations → benchmarking & eval → capstone |

Each week folder is `docs/lessons/week-XX/` (`XX` zero-padded `01`–`10`) with a
`week-XX/index.md` overview plus five `module-Y/` folders (`Y` = `1`–`5`).

---

## 2. Anatomy of a day-module

Every one of the 50 daily lessons is a folder with three hand-authored files:

```
docs/lessons/week-XX/module-Y/
├── index.md            # the lesson page  (in nav)
├── assignment.md       # hands-on assignment  (linked from lesson, not in nav)
└── knowledge-check.md  # formative MCQ check  (linked from lesson, not in nav)
```

- The **weekly** knowledge check (`module-5/knowledge-check.md` for weeks 1–9) is
  the only check promoted into the sidebar as "Week N Knowledge Check".
- **Week 6 / module 1** additionally carries three `supplementary-*.md` deep-dives
  (roles & formatting, CoT / few-shot, hallucinations & evals).
- Each `index.md` opens with an auto-generated breadcrumb header (see §4).

New lessons must satisfy `scripts/audit_lessons.py`; see
[CONTRIBUTING.md § Authoring new lessons](CONTRIBUTING.md#authoring-new-lessons).

---

## 3. Content linked but not in the sidebar

These render but are reached from within lessons, not the nav tree. They're
declared under `not_in_nav:` in `mkdocs.yml` so `--strict` builds stay quiet.

| Content | Count | Location |
|---------|-------|----------|
| Assignments | 50 | `lessons/**/assignment.md` |
| Knowledge checks | 50 | `lessons/**/knowledge-check.md` (9 also surfaced weekly) |
| Supplementary deep-dives | 3 | `lessons/week-06/module-1/supplementary-*.md` |
| Readings & guides | 6 | `readings/{ai-agents,prompt-engineering,capsule}/` |

Each readings topic has an `index.md` plus a student- or lab-guide, and opens in
a new tab (via `assets/readings-newtab.js`).

---

## 4. How content is managed (the build pipeline)

The core rule: **edit sources of truth, never edit generated artifacts.**

```
   SOURCES OF TRUTH                 BUILD SCRIPTS                GENERATED ARTIFACTS
   (hand-authored)          (scripts/ + hooks/, run in CI)      (derived - don't edit)
   ─────────────────        ──────────────────────────────      ────────────────────────
   lessons/**/*.md      ──▶ build_catalog.py              ──▶   catalog.json
   source-material/     ──▶ build_glossary.py             ──▶   kb/glossary.json
     (5 *-Glossary.md)
   source-material/     ──▶ build_flashcards.py           ──▶   kb/flashcards.json
     (4 *-Flashcards.md)
   kb/graph.json        ──▶ generate_roadmap.py           ──▶   roadmap.md (sitemap)
   mkdocs.yml (nav)     ──▶ build_card_grids.py           ──▶   AUTO-GEN card grids
                            apply_lesson_header.py         ──▶   AUTO-GEN lesson headers
                            hooks/progress_badges.py       ──▶   {status:…} → status pills
                            audit_lessons.py (lint L001–L015)
```

### Sources of truth - edit these

- `docs/lessons/**/index.md`, `assignment.md`, `knowledge-check.md` - lesson content.
- `docs/kb/graph.json` - the hand-authored heart: ~98 concepts + prerequisite
  edges. Feeds the interactive concept graph **and** the roadmap.
- `planning/source-material/` - upstream study guides the lessons distill from
  and the glossary is built from (reference, not a primary edit target).
- `mkdocs.yml` - the canonical nav. Adding/reordering lessons means editing
  **both** the filesystem folder and this nav; the catalog check keeps them in sync.

### Generated artifacts - never hand-edit

| Artifact | Generated by | Notes |
|----------|--------------|-------|
| `catalog.json` (repo root) | `build_catalog.py` | Filesystem-derived week/module catalog; committed so CI can diff structure. |
| `docs/kb/glossary.json` | `build_glossary.py` | A–Z dictionary built from the 5 source-material glossaries. |
| `docs/kb/flashcards.json` | `build_flashcards.py` | Q/A decks built from the 4 source-material `*-Flashcards.md` files (has `--check`). Renders the Reference-tab Flashcards page. |
| `docs/roadmap.md` | `generate_roadmap.py` | Phase-banded sitemap derived from `kb/graph.json` (has `--check`). |
| In-page card grids | `build_card_grids.py` | Bounded by `<!-- AUTO-GEN:CARD-GRID:START/END -->` markers. |
| In-page lesson headers | `apply_lesson_header.py` | Bounded by `<!-- AUTO-GEN:LESSON-HEADER:START/END -->` markers. |
| Status pills | `hooks/progress_badges.py` | Build-time hook swaps `{status:week-XX/module-Y}` tokens. |

### Progress tracking

Progress has two sources, resolved by `docs/assets/progress-source.js`:

1. **Live (primary).** For a signed-in student it reads their own server-stored
   check attempts and derives per-module status, per-week and overall rollups.
   A module counts as cleared when its wrap-up — or the week's canonical check,
   on consolidation days that have no wrap-up — reaches 80%. Pre-reads move a
   module to *in progress* but never clear it.
2. **Committed (fallback).** `docs/progress/summary.json`, derived from the
   per-module files under `docs/progress/`. Used when there is no session, and
   by forks that record progress that way. It's a build artifact; don't hand-edit.

Both are emitted in the same shape, so the consumers are unchanged:
`docs/assets/roadmap-progress.js` (per-week + overall bars, next-up) and the
header progress pill. The `{status:...}` pills on lesson pages still come from
the build-time hook reading the committed files.

---

## 5. Data & knowledge-base layer

The interactive KB pages under `docs/kb/` are **self-contained HTML** (inline
`<style>` + `<script>`, served without Material chrome). To restyle one, edit
that `.html` file's inline styles directly: not the global stylesheets.

| KB page (`docs/kb/`) | Kind | Backing data |
|----------------------|------|--------------|
| `interactive-graph.html` | Plan | `graph.json` |
| `glossary.html` | Reference | `glossary.json` (generated) |
| `concepts.html` | Reference | `concepts.json`, `facts.json` |
| `flashcards.html` | Reference | `flashcards.json` (generated) |

Other committed data: `docs/kb/lesson-frontmatter.json` (per-lesson metadata).

---

## 6. Building & serving locally

```bash
python3 scripts/audit_lessons.py        # lint lesson invariants (L001–L015)
python3 scripts/build_catalog.py        # regenerate catalog.json (commit if changed)
mkdocs build --strict                   # the check CI runs
mkdocs serve                            # local preview — open the URL it prints (http://localhost:8000/au-curriculum/)
```

Regeneration order when editing the concept graph: edit `kb/graph.json` →
`generate_roadmap.py` → rebuild. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
full branch/PR flow and pre-PR checklist.
