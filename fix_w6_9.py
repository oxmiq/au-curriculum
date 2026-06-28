#!/usr/bin/env python3
"""
fix_w6_9.py  — Week 5–9 pre-reading link repair
================================================
1. Creates docs/readings/ pages from the NON-GIT pre-lecture reading files
   (plus Student Guide / Lab Guide from planning/source-material/).
2. Updates lesson headers and end-of-day pre-read sections in weeks 5–9.
3. Adds a "Reading Guides" section to mkdocs.yml nav.

Run from the repo root:
    python3 fix_w6_9.py
"""

import os
import re

REPO = "/Users/shiva/Documents/vscode/oxmiq/projects/au-curriculum"
NONGT = "/Users/shiva/Documents/vscode/oxmiq/projects/NON-GIT/au-curriculum-planning/planning/source-material"
PLAN  = f"{REPO}/planning/source-material"

# ── helpers ────────────────────────────────────────────────────────────────────

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote  {os.path.relpath(path, REPO)}")

def patch(path, old, new, *, required=True):
    with open(path, encoding="utf-8") as f:
        content = f.read()
    if old not in content:
        if required:
            print(f"  WARN   string not found in {os.path.relpath(path, REPO)}: {old[:80]!r}")
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.replace(old, new, 1))
    return True

# Link helpers
def ext(url, text):
    """External link — opens in new tab."""
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'

def inn(path, text):
    """Internal link — same tab."""
    return f'<a href="{path}">{text}</a>'

# ── URL constants ──────────────────────────────────────────────────────────────

ANTHROPIC_TUTORIAL = "https://github.com/anthropics/prompt-eng-interactive-tutorial"
ANTHROPIC_MCP      = "https://www.anthropic.com/news/model-context-protocol"
MITRE_CVE          = "https://www.cve.org/CVERecord?id=CVE-2025-32711"
OWASP_LLM          = "https://owasp.org/www-project-top-10-for-large-language-model-applications/"
HF_AGENTS          = "https://huggingface.co/learn/agents-course/unit2/introduction"
KLARNA             = "https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/"
CLAUDE_CODE        = "https://www.anthropic.com/news/claude-code"

# Internal docs/readings/ paths (relative from any lesson file depth docs/lessons/week-XX/module-Y/)
PE_PAGE  = "../../../readings/prompt-engineering/"
AI_PAGE  = "../../../readings/ai-agents/"
CAP_PAGE = "../../../readings/capsule/"


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Create docs/readings/ pages
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 1: create docs/readings/ pages ──────────────────────────────────")

pe_preread  = read(f"{NONGT}/Prompt Engineering/Prompt-Engineering-Pre-Lecture-Reading.md")
ai_preread  = read(f"{NONGT}/AI Agents/AI Agents - Pre-Lecture Reading.md")
cap_preread = read(f"{NONGT}/Capsule Power User/Capsule-Power-User-Pre-Lecture-Reading.md")

pe_guide   = read(f"{PLAN}/Prompt Engineering/Prompt-Engineering-Student-Guide.md")
ai_guide   = read(f"{PLAN}/AI Agents/AI Agents - Student Guide.md")
cap_guide  = read(f"{PLAN}/Capsule Power User/Capsule-Power-User-Lab-Guide.md")

write(f"{REPO}/docs/readings/prompt-engineering/index.md",
      "---\ntitle: Prompt Engineering — Pre-Lecture Reading\n---\n\n" + pe_preread)

write(f"{REPO}/docs/readings/prompt-engineering/student-guide.md",
      "---\ntitle: Prompt Engineering — Student Guide\n---\n\n" + pe_guide)

write(f"{REPO}/docs/readings/ai-agents/index.md",
      "---\ntitle: AI Agents — Pre-Lecture Reading\n---\n\n" + ai_preread)

write(f"{REPO}/docs/readings/ai-agents/student-guide.md",
      "---\ntitle: AI Agents — Student Guide\n---\n\n" + ai_guide)

write(f"{REPO}/docs/readings/capsule/index.md",
      "---\ntitle: Capsule Power-User — Pre-Lecture Reading\n---\n\n" + cap_preread)

write(f"{REPO}/docs/readings/capsule/lab-guide.md",
      "---\ntitle: Capsule Power-User — Lab Guide\n---\n\n" + cap_guide)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Fix week-05/module-5 (pre-read for Day 26 at bottom)
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 2: week-05/module-5 ─────────────────────────────────────────────")

patch(
    f"{REPO}/docs/lessons/week-05/module-5/index.md",
    "- **Resource:** Prompt Engineering Student Guide, Modules 0–1 (~30 min)",
    (
        f"- **Resource:** {inn(PE_PAGE, 'Prompt Engineering Pre-Lecture Reading')} — "
        "work through the Day 26 and Day 27 primers before Monday (~25 min). "
        f"Supplement: {ext(ANTHROPIC_TUTORIAL, 'Anthropic Prompt Engineering Interactive Tutorial')}."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Fix week-06 headers + end-of-day sections
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 3: week-06 ──────────────────────────────────────────────────────")

L6 = lambda m: f"{REPO}/docs/lessons/week-06/{m}/index.md"

# ── module-1 (Day 26 · Prompt Structure & Clarity) ──────────────────────────
patch(L6("module-1"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Prompt%20Engineering/Prompt-Engineering-Pre-Lecture-Reading.md" target="_blank" rel="noopener">Anthropic Prompt Engineering Interactive Tutorial — Chapter 1 (Basic Prompt Structure) + Chapter 2 (Being Clear and Direct)</a> (~20 min).',
    (
        f'> **Pre-reading:** {inn(PE_PAGE, "Prompt Engineering Pre-Lecture Reading — Day 26 primer")} (~10 min). '
        f'Supplement: {ext(ANTHROPIC_TUTORIAL, "Anthropic Prompt Engineering Interactive Tutorial")} (Ch 1 + Ch 2, ~20 min).'
    ),
)
# end → pre-read for Day 27 (Roles, Data, Output Formatting)
patch(L6("module-1"),
    "- **Resource:** Anthropic tutorial **Ch 3 (Roles)** + **Ch 4 (Separating Data and Instructions)** + **Ch 5 (Output Formatting)** (~25 min).",
    (
        f"- **Resource:** {inn(PE_PAGE, 'Prompt Engineering Pre-Lecture Reading — Day 27 primer')} (~12 min). "
        f"Supplement: {ext(ANTHROPIC_TUTORIAL, 'Anthropic tutorial')} Ch 3 + Ch 4 + Ch 5 (~20 min)."
    ),
)

# ── module-2 (Day 27 · Agent Fundamentals — corrected to PE Day 27 primer) ──
patch(L6("module-2"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Pre-Lecture%20Reading.md" target="_blank" rel="noopener">AI Agents Student Guide — Module 0 (Why Now?)</a> (~20 min).',
    (
        f'> **Pre-reading:** {inn(PE_PAGE, "Prompt Engineering Pre-Lecture Reading — Day 27 primer (Roles, walls, and shapes)")} (~12 min). '
        f'Supplement: {ext(ANTHROPIC_TUTORIAL, "Anthropic tutorial")} Ch 3–5 (~20 min).'
    ),
)
# end → pre-read for Day 28 (Tools & MCP — AI Agents territory)
patch(L6("module-2"),
    "- **Resource:** Student Guide **Module 2 — Action Layer** + Anthropic MCP spec overview (~25 min).",
    (
        f"- **Resource:** {inn(AI_PAGE, 'AI Agents Pre-Lecture Reading — Tools & MCP section')} (~30 min). "
        f"Supplement: {ext(ANTHROPIC_MCP, 'Anthropic — Introducing the Model Context Protocol')} (5 min)."
    ),
)

# ── module-3 (Day 28 · Tools & Action Layer) ────────────────────────────────
patch(L6("module-3"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Pre-Lecture%20Reading.md" target="_blank" rel="noopener">AI Agents Student Guide — Module 2 (Action Layer)</a> + Anthropic MCP overview (~25 min).',
    (
        f'> **Pre-reading:** {inn(AI_PAGE, "AI Agents Pre-Lecture Reading — Tools & MCP section")} (~30 min). '
        f'Supplement: {ext(ANTHROPIC_MCP, "Anthropic — Introducing the Model Context Protocol")}.'
    ),
)
# end → pre-read for Day 29 (Governance & Security)
patch(L6("module-3"),
    "- **Resource:** Student Guide **Module 3 — Governance Layer** + Glossary entry on **EchoLeak** (~25 min).",
    (
        f"- **Resource:** {inn(AI_PAGE, 'AI Agents Pre-Lecture Reading — Governance & Security section')} (~35 min). "
        f"Supplement: {ext(MITRE_CVE, 'MITRE — CVE-2025-32711 (EchoLeak)')} + "
        f"{ext(OWASP_LLM, 'OWASP Top 10 for LLM Applications')} (scan LLM01 + LLM02, ~10 min)."
    ),
)

# ── module-4 (Day 29 · Governance) ──────────────────────────────────────────
patch(L6("module-4"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Pre-Lecture%20Reading.md" target="_blank" rel="noopener">AI Agents Student Guide — Module 3 (Governance Layer)</a> + Glossary "EchoLeak" (~25 min).',
    (
        f'> **Pre-reading:** {inn(AI_PAGE, "AI Agents Pre-Lecture Reading — Governance & Security section")} (~35 min). '
        f'Supplement: {ext(MITRE_CVE, "MITRE — CVE-2025-32711 (EchoLeak)")} + '
        f'{ext(OWASP_LLM, "OWASP LLM01 + LLM02")} (~10 min).'
    ),
)
# end → pre-read for Day 30 (Orchestration & Multi-Agent)
patch(L6("module-4"),
    "- **Resource:** Student Guide **Module 4 — Orchestration Layer** (~20 min).",
    (
        f"- **Resource:** {inn(AI_PAGE, 'AI Agents Pre-Lecture Reading — Orchestration & Multi-Agent section')} (~30 min). "
        f"Supplement: {ext(HF_AGENTS, 'HuggingFace Agents Course — Unit 2 intro (smolagents)')} (~10 min)."
    ),
)

# ── module-5 (Day 30 · Orchestration) ───────────────────────────────────────
patch(L6("module-5"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/AI%20Agents/AI%20Agents%20-%20Pre-Lecture%20Reading.md" target="_blank" rel="noopener">AI Agents Student Guide — Module 4 (Orchestration Layer)</a> (~20 min).',
    (
        f'> **Pre-reading:** {inn(AI_PAGE, "AI Agents Pre-Lecture Reading — Orchestration & Multi-Agent section")} (~30 min). '
        f'Supplement: {ext(HF_AGENTS, "HuggingFace Agents Course — Unit 2 intro")} (~10 min).'
    ),
)
# module-5 end → "Review your notes" (no external reading needed; leave as-is)

# ── module-6 (Day 31 · Consolidation) — end → pre-read for Day 32 ───────────
patch(L6("module-6"),
    "- **Resource:** Read one published case study about a production agent: Klarna AI assistant, Cursor, OxCode, or Claude Code. A blog post or conference talk works (~20 min).",
    (
        f"- **Resource:** {inn(AI_PAGE, 'AI Agents Pre-Lecture Reading — Day 35 section')} (~20 min). "
        f"Case studies: {ext(KLARNA, 'Klarna AI assistant')} or "
        f"{ext(CLAUDE_CODE, 'Anthropic — Claude Code')} (~20 min)."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Fix week-07 headers + end-of-day sections
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 4: week-07 ──────────────────────────────────────────────────────")

L7 = lambda m: f"{REPO}/docs/lessons/week-07/{m}/index.md"

# ── module-1 (Day 32 · Agent Case Studies) — pre-reading embedded in blockquote
patch(L7("module-1"),
    "**Pre-reading:** Klarna AI assistant blog post + one coding-agent case study (Claude Code or Cursor) (~20 min).",
    (
        f"**Pre-reading:** {inn(AI_PAGE, 'AI Agents Pre-Lecture Reading')} (~20 min). "
        f"Case studies: {ext(KLARNA, 'Klarna AI assistant')} or "
        f"{ext(CLAUDE_CODE, 'Anthropic — Claude Code')}."
    ),
)
# end → pre-read for Day 33 (Capsule Foundations)
patch(L7("module-1"),
    "- **Resource:** Capsule Power User Lab Guide **Modules 1 + 2** (~35 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 36 section')} (~40 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Modules 1 + 2."
    ),
)

# ── module-2 (Day 33 · Capsule Foundations) — standalone blockquote ──────────
patch(L7("module-2"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Modules 1 + 2</a> (~35 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 36 section")} (~40 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Modules 1 + 2.'
    ),
)
# end → pre-read for Environments & Fleet Discovery
patch(L7("module-2"),
    "- **Resource:** Lab Guide **Module 3** (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 37 section')} (~25 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 3."
    ),
)

# ── module-3 (Day 34 · Installation) — pre-reading embedded in blockquote ────
patch(L7("module-3"),
    "**Pre-reading:** Capsule Power User Lab Guide **Module 2** (~20 min).",
    (
        f"**Pre-reading:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 36 section')} (~40 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 2 (~15 min)."
    ),
)
# end → pre-read for Environments & Fleet Discovery
patch(L7("module-3"),
    "- **Resource:** Capsule Power User Lab Guide **Module 3** (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 37 section')} (~25 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 3."
    ),
)

# ── module-4 (Day 35 · Environments & Fleet Discovery) — standalone blockquote
patch(L7("module-4"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Module 3</a> (~15 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 37 section")} (~25 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Module 3.'
    ),
)
# end → pre-read for Connecting to Machines
patch(L7("module-4"),
    "- **Resource:** Lab Guide **Module 5** (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 38 section')} (~25 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 5."
    ),
)

# ── module-5 (Day 36 · Consolidation) — end → pre-read for Day 37 Connecting ─
patch(L7("module-5"),
    "- **Resource:** Capsule Power User Lab Guide **Module 5** (Connecting to Machines) (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 38 section')} (~25 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 5 (Connecting to Machines)."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Fix week-08 headers + end-of-day sections
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 5: week-08 ──────────────────────────────────────────────────────")

L8 = lambda m: f"{REPO}/docs/lessons/week-08/{m}/index.md"

# ── module-1 (Day 37 · Connecting to Machines) — standalone blockquote ───────
patch(L8("module-1"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Module 5</a> (~15 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 38 section")} (~25 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Module 5.'
    ),
)
# end → pre-read for Files & Storage
patch(L8("module-1"),
    "- **Resource:** Lab Guide **Modules 6 + 7** (~30 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 39 section')} (~40 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Modules 6 + 7."
    ),
)

# ── module-2 (Day 38 · Files & Storage) — standalone blockquote ──────────────
patch(L8("module-2"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Modules 6 + 7</a> (~30 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 39 section")} (~40 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Modules 6 + 7.'
    ),
)
# end → pre-read for Reliability & Diagnostics (Day 40)
patch(L8("module-2"),
    "- **Resource:** Lab Guide **Module 10 known-quirks table** + Glossary (~10 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 40 section')} (~15 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 10 known-quirks table + Glossary."
    ),
)

# ── module-3 (Day 39 · Streaming) — pre-reading embedded in blockquote ───────
patch(L8("module-3"),
    "**Pre-reading:** Capsule Power User Lab Guide **Module 7** (~15 min).",
    (
        f"**Pre-reading:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 39 section')} (~40 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 7 (~15 min)."
    ),
)
# end → pre-read for Known Quirks (Day 40)
patch(L8("module-3"),
    "- **Resource:** Capsule Power User Lab Guide **Module 10 (Known Quirks)** (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 40 section')} (~15 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 10 (Known Quirks)."
    ),
)

# ── module-4 (Day 40 · Known Quirks) — pre-reading embedded in blockquote ────
patch(L8("module-4"),
    "**Pre-reading:** Capsule Power User Lab Guide **Module 10 — Known Quirks** (~15 min).",
    (
        f"**Pre-reading:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 40 section')} (~15 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 10 — Known Quirks."
    ),
)
# module-4 end → Day 41 Consolidation (no external reading; leave as-is)

# ── module-5 (Day 41 · Consolidation) — end → pre-read for Day 42 Benchmark ──
patch(L8("module-5"),
    "- **Resource:** Capsule Power User Lab Guide **Module 8** (Benchmarking) (~30 min). This is the most important module for the reliability track — budget the full 30 minutes.",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 41 section')} (~30 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 8 (Benchmarking) — budget the full 30 minutes."
    ),
)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — Fix week-09 headers + end-of-day sections
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 6: week-09 ──────────────────────────────────────────────────────")

L9 = lambda m: f"{REPO}/docs/lessons/week-09/{m}/index.md"

# ── module-1 (Day 42 · Benchmarking) — standalone blockquote ─────────────────
patch(L9("module-1"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Module 8</a> (~20 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 41 section")} (~30 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Module 8.'
    ),
)
# module-1 end → "Re-skim Week 4 Day 16 + Day 14" (internal cross-reference; leave as-is)

# ── module-2 (Day 43 · Varying Parameters) — end → pre-read for Day 44 ───────
patch(L9("module-2"),
    "- **Resource:** Lab Guide **Module 9** (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 43 section')} (~20 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 9."
    ),
)

# ── module-3 (Day 44 · Interactive Chat) — standalone blockquote ─────────────
patch(L9("module-3"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Module 9</a> (~15 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 43 section")} (~20 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Module 9.'
    ),
)
# end → pre-read for Day 45 (Scheduling & MCP)
patch(L9("module-3"),
    "- **Resource:** Lab Guide **Module 10** (~15 min).",
    (
        f"- **Resource:** {inn(CAP_PAGE, 'Capsule Power-User Pre-Lecture Reading — Day 44 section')} (~25 min). "
        f"Supplement: {inn(CAP_PAGE + 'lab-guide/', 'Capsule Lab Guide')} Module 10."
    ),
)

# ── module-4 (Day 45 · Scheduling & MCP) — standalone blockquote ─────────────
patch(L9("module-4"),
    '> **Pre-reading:** <a href="../../../../planning/source-material/Capsule%20Power%20User/Capsule-Power-User-Lab-Guide.md" target="_blank" rel="noopener">Capsule Power User Lab Guide — Module 10</a> (~15 min).',
    (
        f'> **Pre-reading:** {inn(CAP_PAGE, "Capsule Power-User Pre-Lecture Reading — Day 44 section")} (~25 min). '
        f'Supplement: {inn(CAP_PAGE + "lab-guide/", "Capsule Lab Guide")} Module 10.'
    ),
)
# module-4 end → capstone prep (no changes needed)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — Update mkdocs.yml nav
# ══════════════════════════════════════════════════════════════════════════════

print("\n── Step 7: mkdocs.yml nav ────────────────────────────────────────────────")

MKDOCS = f"{REPO}/mkdocs.yml"
NAV_INSERTION_MARKER = "  - Plan:"

READINGS_NAV = """\
  - Reading Guides:
      - Prompt Engineering:
          - Pre-Lecture Reading: readings/prompt-engineering/index.md
          - Student Guide: readings/prompt-engineering/student-guide.md
      - AI Agents:
          - Pre-Lecture Reading: readings/ai-agents/index.md
          - Student Guide: readings/ai-agents/student-guide.md
      - "Capsule Power-User":
          - Pre-Lecture Reading: readings/capsule/index.md
          - Lab Guide: readings/capsule/lab-guide.md
"""

mkdocs_content = read(MKDOCS)
if "readings/prompt-engineering/index.md" in mkdocs_content:
    print("  nav already updated — skipping")
else:
    updated = mkdocs_content.replace(NAV_INSERTION_MARKER, READINGS_NAV + NAV_INSERTION_MARKER, 1)
    if updated == mkdocs_content:
        print(f"  WARN   insertion marker not found: {NAV_INSERTION_MARKER!r}")
    else:
        with open(MKDOCS, "w", encoding="utf-8") as f:
            f.write(updated)
        print("  wrote  mkdocs.yml")


print("\n✓ All done. Run `mkdocs build --strict` to verify.\n")
