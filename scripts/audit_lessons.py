#!/usr/bin/env python3
"""Lint every lesson folder under docs/lessons/ — week-XX/module-Y/ schema.

Rules (L001-L008):

  L001  week folder name matches week-NN (zero-padded, 01..10)
  L001m module folder name matches module-N (1-9)
  L002  index.md exists and starts with an H1 (week overview + each module)
  L003  module count per week matches docs/kb/graph.json
  L005  knowledge-check.html exists in every module folder
  L006  assignment.md exists and starts with an H1 in every module folder
  L007  every `planning/source-material/...` link in a lesson points at a file
        that exists on disk (URL-encoded paths are decoded before checking)
  L008  no legacy `quiz.html` references; no legacy `module-NN/` flat references

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


def load_graph_module_counts():
    if not GRAPH_JSON.exists():
        return {}
    graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    return {w["id"]: len(w["modules"]) for w in graph["weeks"]}


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

    if not (module_dir / "knowledge-check.html").exists():
        report.add("L005", week_name, name, module_dir, "knowledge-check.html missing")

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
