#!/usr/bin/env python3
"""Lint every lesson folder under docs/lessons/.

Rules (L001-L008):

  L001  module folder name matches module-NN (zero-padded, 01..99)
  L002  index.md exists and starts with an H1
  L003  exactly four day files matching 0[1-4]-<slug>.md
        (module-10 is exempt: capstone has 5 day files 01..05)
  L004  each day file starts with an H1
  L005  quiz.html exists (exempt: module-10 capstone)
  L006  assignment.md exists and starts with an H1
  L007  every `planning/source-material/...` link in a lesson points at a file
        that exists on disk (URL-encoded paths are decoded before checking)
  L008  no legacy `../../../../planning/source-material/` (4-up form from the
        planning repo's week-NN/module-1/ shape)

Exit codes:
    0   no violations
    1   one or more violations (with --strict; otherwise 0)

Usage:
    python3 scripts/audit_lessons.py
    python3 scripts/audit_lessons.py --module module-01
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

MODULE_NAME_RE = re.compile(r"^module-(\d{2})$")
DAY_FILE_RE = re.compile(r"^(0[1-9])-[a-z0-9][a-z0-9-]*\.md$")
H1_RE = re.compile(r"^# \S", re.MULTILINE)
SOURCE_LINK_RE = re.compile(r"\]\((\.\./\.\./\.\./planning/source-material/[^)]+)\)")
LEGACY_SOURCE_LINK_RE = re.compile(r"\.\./\.\./\.\./\.\./planning/source-material/")

# Modules whose day-file count differs from the default of four.
DAY_FILE_OVERRIDES: dict[str, int] = {
    "module-10": 5,
}

# Modules that intentionally ship without a canonical quiz (project-only weeks).
QUIZ_EXEMPT: set[str] = {"module-10"}


@dataclass
class Violation:
    rule: str
    module: str
    path: str
    message: str


@dataclass
class Report:
    violations: list[Violation] = field(default_factory=list)

    def add(self, rule: str, module: str, path: Path | str, message: str) -> None:
        rel = str(Path(path).relative_to(REPO_ROOT)) if isinstance(path, Path) else str(path)
        self.violations.append(Violation(rule=rule, module=module, path=rel, message=message))


def starts_with_h1(file_path: Path) -> bool:
    try:
        with file_path.open(encoding="utf-8") as fh:
            for line in fh:
                stripped = line.strip()
                if not stripped:
                    continue
                return bool(H1_RE.match(stripped))
    except OSError:
        return False
    return False


def audit_module(module_dir: Path, report: Report) -> None:
    name = module_dir.name

    # L001
    match = MODULE_NAME_RE.match(name)
    if not match:
        report.add("L001", name, module_dir, f"folder name '{name}' does not match module-NN")
        return  # later rules assume the canonical shape

    # L002
    index_md = module_dir / "index.md"
    if not index_md.exists():
        report.add("L002", name, module_dir, "index.md missing")
    elif not starts_with_h1(index_md):
        report.add("L002", name, index_md, "index.md does not start with an H1")

    # L003
    expected_count = DAY_FILE_OVERRIDES.get(name, 4)
    day_files = sorted(p for p in module_dir.iterdir() if DAY_FILE_RE.match(p.name))
    if len(day_files) != expected_count:
        report.add(
            "L003",
            name,
            module_dir,
            f"expected {expected_count} day files matching 0[1-{expected_count}]-<slug>.md, found {len(day_files)}",
        )

    # L004
    for day_file in day_files:
        if not starts_with_h1(day_file):
            report.add("L004", name, day_file, "day file does not start with an H1")

    # L005
    if name not in QUIZ_EXEMPT and not (module_dir / "quiz.html").exists():
        report.add("L005", name, module_dir, "quiz.html missing")

    # L006
    assignment = module_dir / "assignment.md"
    if not assignment.exists():
        report.add("L006", name, module_dir, "assignment.md missing")
    elif not starts_with_h1(assignment):
        report.add("L006", name, assignment, "assignment.md does not start with an H1")

    # L007 + L008 — scan every .md in the module
    for md_file in module_dir.glob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue

        # L008 first (cheap regex), so legacy paths are flagged before being checked.
        if LEGACY_SOURCE_LINK_RE.search(text):
            report.add(
                "L008",
                name,
                md_file,
                "contains legacy 4-up '../../../../planning/source-material/' link",
            )

        # L007
        for link in SOURCE_LINK_RE.findall(text):
            target_rel = unquote(link)
            target = (md_file.parent / target_rel).resolve()
            if not target.exists():
                report.add(
                    "L007",
                    name,
                    md_file,
                    f"broken source-material link: {target_rel}",
                )


def iter_modules(filter_name: str | None) -> Iterable[Path]:
    if not LESSONS_DIR.exists():
        return []
    modules = sorted(p for p in LESSONS_DIR.iterdir() if p.is_dir())
    if filter_name:
        modules = [m for m in modules if m.name == filter_name]
    return modules


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint lesson invariants")
    parser.add_argument("--module", help="Audit a single module (e.g. module-01)")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on any violation")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    report = Report()
    modules = list(iter_modules(args.module))
    if args.module and not modules:
        print(f"no such module: {args.module}", file=sys.stderr)
        return 2

    for module_dir in modules:
        audit_module(module_dir, report)

    if args.json:
        json.dump(
            {
                "modules_audited": [m.name for m in modules],
                "violation_count": len(report.violations),
                "violations": [v.__dict__ for v in report.violations],
            },
            sys.stdout,
            indent=2,
        )
        print()
    else:
        for v in report.violations:
            print(f"{v.rule}  {v.module}  {v.path}  {v.message}")
        print(
            f"\n{len(report.violations)} violation(s) across {len(modules)} module(s).",
            file=sys.stderr,
        )

    if args.strict and report.violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
