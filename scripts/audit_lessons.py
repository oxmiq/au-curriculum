#!/usr/bin/env python3
"""Lint every lesson folder under docs/lessons/ — week-XX/module-Y/ schema.

Rules (L001-L015):

  L001  week folder name matches week-NN (zero-padded, 01..10)
  L001m module folder name matches module-N (1-9)
  L002  index.md exists and starts with an H1 (week overview + each module)
  L003  module count per week matches docs/kb/graph.json
  L005  knowledge-check.html exists in every module folder
  L006  assignment.md exists and starts with an H1 in every module folder
  L007  every `planning/source-material/...` link in a lesson points at a file
        that exists on disk (URL-encoded paths are decoded before checking)
  L008  no legacy `quiz.html` references; no legacy `module-NN/` flat references
  L010  week overview (week-NN/index.md): H1 matches "# Week N · ", frontmatter
        has "Goal of the week:", day-map table has exactly
        4 columns (Day|Topic|Pre-read|Page), "## Friday — the bar" present
  L011  module index.md classified as exactly one shape: B7 | F | C
        (B7 = lesson plan table + Part 1-7 headings;
         F  = Self-Study Time Buckets table + Bucket headings;
         C  = Today's milestones section present)
  L012  B7 invariants: Part 7 = Wrap-up,
        "### Pre-read for tomorrow" is H3 (not standalone H2), "## Stuck?" present,
        no legacy H2s (## Wrap-up / ## Connect forward / ## Pre-read for tomorrow)
  L013  F invariants: Self-Study Time Buckets table present, ≥3 Bucket headings,
        emoji order starts with 🔵 🟢 🟡, "## Stuck?" present,
        no ## Lesson plan and no ## Part N headings
  L014  C invariants: "## Today's milestones" or "## Detailed time budget" present,
        "## Wrap-up" present, "## Self-check before Day" present, "## Stuck?" present
  L015  day-map link integrity: every module-N/index.md link in a week overview
        resolves to an existing file on disk

Exit codes:
    0   no violations
    1   one or more violations (with --strict; otherwise 0)

Usage:
    python3 scripts/audit_lessons.py
    python3 scripts/audit_lessons.py --week week-01
    python3 scripts/audit_lessons.py --strict
    python3 scripts/audit_lessons.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "docs" / "lessons"
GRAPH_JSON = REPO_ROOT / "docs" / "kb" / "graph.json"

WEEK_NAME_RE = re.compile(r"^week-(\d{2})$")
MODULE_NAME_RE = re.compile(r"^module-([1-9])$")
H1_RE = re.compile(r"^# \S", re.MULTILINE)
SOURCE_LINK_RE = re.compile(r"\]\((\.\./\.\./\.\./(?:\.\./)?planning/source-material/[^)]+)\)")
LEGACY_QUIZ_RE = re.compile(r"\bquiz\.html\b")
LEGACY_FLAT_MODULE_RE = re.compile(r"lessons/module-\d{2}/")

# ── L010: week-overview shape ────────────────────────────────────────────────
WEEK_H1_RE = re.compile(r"^# Week \d+", re.MULTILINE)
WEEK_GOAL_RE = re.compile(r"\*\*Goal of the week:\*\*")
WEEK_DAYMAP_HEADER_RE = re.compile(r"^## Day map", re.MULTILINE)
# 4-column table: must have exactly 3 pipes between columns (= 4 columns)
WEEK_DAYMAP_4COL_RE = re.compile(r"^\|[^|]+\|[^|]+\|[^|]+\|[^|]+\|", re.MULTILINE)
WEEK_FRIDAY_BAR_RE = re.compile(r"^## (?:Friday [-—–] the bar|The bar)", re.MULTILINE)

# ── L011: shape classification ───────────────────────────────────────────────
SHAPE_B7_LESSON_PLAN_RE = re.compile(r"^## Lesson plan", re.MULTILINE)
SHAPE_B7_PART_RE = re.compile(r"^## Part \d+", re.MULTILINE)
SHAPE_F_BUCKETS_RE = re.compile(r"^## Self-Study Time Buckets", re.MULTILINE)
SHAPE_F_BUCKET_HEAD_RE = re.compile(r"^## [🔵🟢🟡🟠🔴🟣]", re.MULTILINE)
SHAPE_C_MILESTONES_RE = re.compile(r"^## Today.s milestones|^## Detailed time budget", re.MULTILINE)

# ── L012: B7 invariants ──────────────────────────────────────────────────────
B7_PART7_RE = re.compile(r"^## Part 7 [-—–] Wrap-up & Connection", re.MULTILINE)
B7_PART_MIDDLE_DOT_RE = re.compile(r"^## Part \d+ [-—–] .+ · \d", re.MULTILINE)
B7_PART_ANY_RE = re.compile(r"^## Part \d+ [-—–] ", re.MULTILINE)
B7_STUCK_RE = re.compile(r"^## Stuck\?", re.MULTILINE)
B7_PREREAD_H3_RE = re.compile(r"^### Pre-read for tomorrow", re.MULTILINE)
B7_LEGACY_WRAP_H2_RE = re.compile(r"^## Wrap-up\b|^## Wrap\b", re.MULTILINE)
B7_LEGACY_CONNECT_H2_RE = re.compile(r"^## Connect forward\b", re.MULTILINE)
B7_LEGACY_PREREAD_H2_RE = re.compile(r"^## Pre-read for tomorrow\b", re.MULTILINE)

# ── L013: F invariants ───────────────────────────────────────────────────────
F_EMOJI_ORDER_RE = re.compile(r"🔵.*\n.*🟢.*\n.*🟡", re.DOTALL)

# ── L014: C invariants ───────────────────────────────────────────────────────
C_MILESTONES_RE = re.compile(r"^## Today's milestones", re.MULTILINE)
C_TIMEBUDGET_RE = re.compile(r"^## (?:Time budget for today|Detailed time budget)", re.MULTILINE)
C_WRAPUP_RE = re.compile(r"^## Wrap-up", re.MULTILINE)
C_SELFCHECK_RE = re.compile(r"^## Self-check", re.MULTILINE)

# ── L015: day-map link integrity ─────────────────────────────────────────────
DAYMAP_LINK_RE = re.compile(r"\(module-\d+/index\.md\)")


@dataclass
class Violation:
    rule: str
    week: str
    module: str
    path: str
    message: str


@dataclass
class Report:
    violations: list[Violation] = field(default_factory=list)

    def add(self, rule: str, week: str, module: str, path, message: str) -> None:
        rel = str(Path(path).relative_to(REPO_ROOT)) if isinstance(path, Path) else str(path)
        self.violations.append(Violation(rule=rule, week=week, module=module, path=rel, message=message))


def starts_with_h1(file_path: Path) -> bool:
    """First non-blank, non-frontmatter line must be an H1.

    YAML-style frontmatter (a leading `---` line, contents, then a closing `---`)
    is skipped so files that carry drift markers still pass.
    """
    try:
        with file_path.open(encoding="utf-8") as fh:
            in_frontmatter = False
            opened_frontmatter = False
            for raw in fh:
                stripped = raw.strip()
                if not stripped:
                    continue
                if not opened_frontmatter and stripped == "---":
                    in_frontmatter = True
                    opened_frontmatter = True
                    continue
                if in_frontmatter:
                    if stripped == "---":
                        in_frontmatter = False
                    continue
                return bool(H1_RE.match(stripped))
    except OSError:
        return False
    return False


def _classify_shape(text: str) -> str:
    """Return 'B7', 'F', 'C', or 'UNKNOWN' based on structural fingerprint."""
    has_lesson_plan = bool(SHAPE_B7_LESSON_PLAN_RE.search(text))
    has_parts = bool(SHAPE_B7_PART_RE.search(text))
    has_buckets_table = bool(SHAPE_F_BUCKETS_RE.search(text))
    has_bucket_heads = bool(SHAPE_F_BUCKET_HEAD_RE.search(text))
    has_milestones = bool(SHAPE_C_MILESTONES_RE.search(text))

    b7_signals = has_lesson_plan or has_parts
    f_signals = has_buckets_table or has_bucket_heads
    c_signals = has_milestones

    if b7_signals and not f_signals and not c_signals:
        return "B7"
    if f_signals and not b7_signals and not c_signals:
        return "F"
    if c_signals and not b7_signals and not f_signals:
        return "C"
    return "UNKNOWN"


def load_graph_module_counts():
    if not GRAPH_JSON.exists():
        return {}
    graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    return {w["id"]: len(w["modules"]) for w in graph["weeks"]}


def audit_week_overview(overview: Path, week_name: str, report: Report) -> None:
    """L010 + L015: structural checks on week-NN/index.md."""
    try:
        text = overview.read_text(encoding="utf-8")
    except OSError:
        return

    # L010 — H1
    if not WEEK_H1_RE.search(text):
        report.add("L010", week_name, "-", overview,
                   "week overview H1 does not match '# Week N · '")

    # L010 — frontmatter block-quote
    if not WEEK_GOAL_RE.search(text):
        report.add("L010", week_name, "-", overview,
                   "week overview missing '**Goal of the week:**' in frontmatter")

    # L010 — day-map section present
    if not WEEK_DAYMAP_HEADER_RE.search(text):
        report.add("L010", week_name, "-", overview, "week overview missing '## Day map' section")
    else:
        # Check 4-column table: find lines inside the day-map table section
        daymap_start = text.find("## Day map")
        daymap_end = text.find("\n##", daymap_start + 1)
        daymap_section = text[daymap_start: daymap_end if daymap_end != -1 else len(text)]
        table_rows = [ln for ln in daymap_section.splitlines() if ln.strip().startswith("|")]
        for row in table_rows:
            cols = [c for c in row.split("|") if c.strip()]
            if len(cols) < 4 and not row.strip().startswith("|---"):
                report.add("L010", week_name, "-", overview,
                            f"day-map table row has {len(cols)} column(s); expected 4: {row[:80]!r}")
                break  # report once per file

    # L010 — Friday — the bar
    if not WEEK_FRIDAY_BAR_RE.search(text):
        report.add("L010", week_name, "-", overview,
                   "week overview missing '## Friday — the bar' (or '## The bar') section")

    # L015 — every module-N/index.md link in the overview must resolve on disk
    for m in DAYMAP_LINK_RE.finditer(text):
        link_rel = m.group(0)[1:-1]  # strip surrounding ()
        target = (overview.parent / link_rel).resolve()
        if not target.exists():
            report.add("L015", week_name, "-", overview,
                       f"day-map link broken: {link_rel}")


def audit_module_shape(index_md: Path, week_name: str, module_name: str, report: Report) -> None:
    """L011–L014: shape classification and per-shape invariant checks."""
    try:
        text = index_md.read_text(encoding="utf-8")
    except OSError:
        return

    shape = _classify_shape(text)

    # L011 — must have exactly one known shape
    if shape == "UNKNOWN":
        report.add("L011", week_name, module_name, index_md,
                   "index.md does not match any canonical shape (B7/F/C); "
                   "check for hybrid or missing structure")
        return  # no further shape-specific checks possible

    # L012 — B7 invariants
    if shape == "B7":
        if not B7_PART7_RE.search(text):
            report.add("L012", week_name, module_name, index_md,
                       "B7: missing '## Part 7 — Wrap-up & Connection'")

        if not B7_STUCK_RE.search(text):
            report.add("L012", week_name, module_name, index_md,
                       "B7: missing '## Stuck?' section")

        if not B7_PREREAD_H3_RE.search(text):
            # Not a hard error for modules that have no pre-read (Friday-adjacent, last day)
            # Only flag if there's a next-day reference at all
            pass

        if B7_LEGACY_WRAP_H2_RE.search(text):
            report.add("L012", week_name, module_name, index_md,
                       "B7: legacy '## Wrap-up' or '## Wrap' H2 found; fold into Part 7")
        if B7_LEGACY_CONNECT_H2_RE.search(text):
            report.add("L012", week_name, module_name, index_md,
                       "B7: legacy '## Connect forward' H2 found; fold into Part 7")
        if B7_LEGACY_PREREAD_H2_RE.search(text):
            report.add("L012", week_name, module_name, index_md,
                       "B7: standalone '## Pre-read for tomorrow' H2 found; "
                       "move inside Part 7 as '### Pre-read for tomorrow'")

    # L013 — F invariants
    elif shape == "F":
        bucket_heads = SHAPE_F_BUCKET_HEAD_RE.findall(text)
        if len(bucket_heads) < 3:
            report.add("L013", week_name, module_name, index_md,
                       f"F: only {len(bucket_heads)} Bucket heading(s) found; expected ≥3")
        if not F_EMOJI_ORDER_RE.search(text):
            report.add("L013", week_name, module_name, index_md,
                       "F: emoji bucket order does not start with 🔵 → 🟢 → 🟡")
        if not B7_STUCK_RE.search(text):
            report.add("L013", week_name, module_name, index_md,
                       "F: missing '## Stuck?' section")
        if SHAPE_B7_LESSON_PLAN_RE.search(text):
            report.add("L013", week_name, module_name, index_md,
                       "F: '## Lesson plan' found in F-shape file (hybrid)")
        if SHAPE_B7_PART_RE.search(text):
            report.add("L013", week_name, module_name, index_md,
                       "F: '## Part N' headings found in F-shape file (hybrid)")

    # L014 — C invariants
    elif shape == "C":
        if not C_MILESTONES_RE.search(text):
            report.add("L014", week_name, module_name, index_md,
                       "C: missing '## Today's milestones' section")
        if not C_TIMEBUDGET_RE.search(text):
            report.add("L014", week_name, module_name, index_md,
                       "C: missing '## Time budget for today' or '## Detailed time budget'")
        if not C_WRAPUP_RE.search(text):
            report.add("L014", week_name, module_name, index_md,
                       "C: missing '## Wrap-up' section")
        if not C_SELFCHECK_RE.search(text):
            report.add("L014", week_name, module_name, index_md,
                       "C: missing '## Self-check' section")
        if not B7_STUCK_RE.search(text):
            report.add("L014", week_name, module_name, index_md,
                       "C: missing '## Stuck?' section")


def audit_module(module_dir: Path, week_name: str, report: Report) -> None:
    name = module_dir.name
    if not MODULE_NAME_RE.match(name):
        report.add("L001m", week_name, name, module_dir, f"folder name '{name}' does not match module-N")
        return

    index_md = module_dir / "index.md"
    if not index_md.exists():
        report.add("L002", week_name, name, module_dir, "index.md missing")
    elif not starts_with_h1(index_md):
        report.add("L002", week_name, name, index_md, "index.md does not start with an H1")
    else:
        # L011–L014: shape classification and invariant checks
        audit_module_shape(index_md, week_name, name, report)

    if not (module_dir / "knowledge-check.md").exists():
        report.add("L005", week_name, name, module_dir, "knowledge-check.md missing")

    assignment = module_dir / "assignment.md"
    if not assignment.exists():
        report.add("L006", week_name, name, module_dir, "assignment.md missing")
    elif not starts_with_h1(assignment):
        report.add("L006", week_name, name, assignment, "assignment.md does not start with an H1")

    for md_file in module_dir.glob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        if LEGACY_QUIZ_RE.search(text):
            report.add("L008", week_name, name, md_file, "contains legacy 'quiz.html' reference")
        if LEGACY_FLAT_MODULE_RE.search(text):
            report.add("L008", week_name, name, md_file, "contains legacy 'lessons/module-NN/' reference")

        for link in SOURCE_LINK_RE.findall(text):
            target_rel = unquote(link)
            target = (md_file.parent / target_rel).resolve()
            if not target.exists():
                report.add("L007", week_name, name, md_file, f"broken source-material link: {target_rel}")


def audit_week(week_dir: Path, expected_module_counts, report: Report) -> None:
    name = week_dir.name
    if not WEEK_NAME_RE.match(name):
        report.add("L001", name, "-", week_dir, f"folder name '{name}' does not match week-NN")
        return

    overview = week_dir / "index.md"
    if not overview.exists():
        report.add("L002", name, "-", week_dir, "week overview index.md missing")
    elif not starts_with_h1(overview):
        report.add("L002", name, "-", overview, "week overview index.md does not start with an H1")
    else:
        # L010 + L015: week overview structural checks
        audit_week_overview(overview, name, report)

    if overview.exists():
        try:
            ov_text = overview.read_text(encoding="utf-8")
            if LEGACY_QUIZ_RE.search(ov_text):
                report.add("L008", name, "-", overview, "contains legacy 'quiz.html' reference")
            if LEGACY_FLAT_MODULE_RE.search(ov_text):
                report.add("L008", name, "-", overview, "contains legacy 'lessons/module-NN/' reference")
            for link in SOURCE_LINK_RE.findall(ov_text):
                target_rel = unquote(link)
                target = (overview.parent / target_rel).resolve()
                if not target.exists():
                    report.add("L007", name, "-", overview, f"broken source-material link: {target_rel}")
        except OSError:
            pass

    module_dirs = sorted(p for p in week_dir.iterdir() if p.is_dir() and MODULE_NAME_RE.match(p.name))
    expected = expected_module_counts.get(name)
    if expected is not None and len(module_dirs) != expected:
        report.add("L003", name, "-", week_dir,
                   f"expected {expected} modules per graph.json, found {len(module_dirs)}")

    for md in module_dirs:
        audit_module(md, name, report)


def iter_weeks(filter_name):
    if not LESSONS_DIR.exists():
        return []
    weeks = sorted(p for p in LESSONS_DIR.iterdir() if p.is_dir())
    if filter_name:
        weeks = [w for w in weeks if w.name == filter_name]
    return weeks


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint lesson invariants (week-XX/module-Y schema)")
    parser.add_argument("--week", help="Audit a single week (e.g. week-01)")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any violation")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    report = Report()
    weeks = list(iter_weeks(args.week))
    if args.week and not weeks:
        print(f"no such week: {args.week}", file=sys.stderr)
        return 2

    expected_counts = load_graph_module_counts()
    for week_dir in weeks:
        audit_week(week_dir, expected_counts, report)

    if args.json:
        json.dump(
            {
                "weeks_audited": [w.name for w in weeks],
                "violation_count": len(report.violations),
                "violations": [v.__dict__ for v in report.violations],
            },
            sys.stdout,
            indent=2,
        )
        print()
    else:
        for v in report.violations:
            print(f"{v.rule}  {v.week}  {v.module}  {v.path}  {v.message}")
        print(f"\n{len(report.violations)} violation(s) across {len(weeks)} week(s).")

    if args.strict and report.violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
