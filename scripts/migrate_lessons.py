#!/usr/bin/env python3
"""One-shot migration script: normalize B7 lesson files.

Transforms applied to every module-N/index.md classified as B7 shape:

  T1  Fold standalone `## Pre-read for tomorrow` H2 → H3 inside Part 7
      (removes the preceding `---` separator that separated it from Part 7)

  T2  Add `## Stuck?` block at end of file if missing

  T3  Rename `## Part 6 — Wrap-up & Connection` → `## Part 7 — Wrap-up & Connection`
      when only 6 parts exist (B6 case); update Lesson plan table row accordingly.
      Also updates table column headers to canonical form (What you do | Time).

  T4  Rename any final Part N heading containing "Wrap-up" / "Open Lab" / "Close"
      to `## Part 7 — Wrap-up & Connection · X min` when the file has 7 parts
      and the Part 7 heading doesn't match the canonical form.

Safety:
  - Creates a .bak backup of every file it modifies.
  - Prints a summary of changes.
  - Dry-run mode (--dry-run) shows diffs without writing.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "docs" / "lessons"
MODULE_NAME_RE = re.compile(r"^module-([1-9])$")

# Shape classification
SHAPE_B7_LP = re.compile(r"^## Lesson plan", re.MULTILINE)
SHAPE_B7_PART = re.compile(r"^## Part \d+", re.MULTILINE)
SHAPE_F_BUCKETS = re.compile(r"^## Self-Study Time Buckets", re.MULTILINE)
SHAPE_F_BUCKET_H = re.compile(r"^## [🔵🟢🟡🟠🔴🟣]", re.MULTILINE)
SHAPE_C = re.compile(r"^## Today.s milestones|^## Detailed time budget|^## Time budget for today", re.MULTILINE)

PART_ANY_RE = re.compile(r"^## Part (\d+) — (.+?)(?:\s*·\s*\d+\s*min)?$", re.MULTILINE)
PART7_CANONICAL = re.compile(r"^## Part 7 — Wrap-up & Connection", re.MULTILINE)
STUCK_RE = re.compile(r"^## Stuck\?", re.MULTILINE)
PREREAD_H2_RE = re.compile(r"^## Pre-read for tomorrow\b", re.MULTILINE)
PREREAD_H3_RE = re.compile(r"^### Pre-read for tomorrow\b", re.MULTILINE)
LEGACY_WRAP_H2 = re.compile(r"^## Wrap-up\b|^## Wrap\b", re.MULTILINE)
LEGACY_CONNECT_H2 = re.compile(r"^## Connect forward\b", re.MULTILINE)

STUCK_BLOCK = "\n---\n\n## Stuck?\n\nAsk **oxtutor** — share your exact question, the concept or command that isn't\nclicking, and which week/module you are on.\n"


def classify(text: str) -> str:
    b7 = bool(SHAPE_B7_LP.search(text)) or bool(SHAPE_B7_PART.search(text))
    f = bool(SHAPE_F_BUCKETS.search(text)) or bool(SHAPE_F_BUCKET_H.search(text))
    c = bool(SHAPE_C.search(text))
    if b7 and not f and not c:
        return "B7"
    if f and not b7 and not c:
        return "F"
    if c and not b7 and not f:
        return "C"
    return "UNKNOWN"


def count_parts(text: str) -> int:
    return len(PART_ANY_RE.findall(text))


def fold_preread_h2(text: str) -> tuple[str, bool]:
    """T1: convert standalone ## Pre-read H2 → H3 inside Part 7."""
    # Pattern: optional whitespace + --- + blank line(s) + ## Pre-read for tomorrow
    pattern = re.compile(
        r"(\n+---\n+)(## Pre-read for tomorrow\b)",
        re.MULTILINE,
    )
    new_text, n = pattern.subn(r"\n\n### Pre-read for tomorrow", text)
    return new_text, n > 0


def add_stuck(text: str) -> tuple[str, bool]:
    """T2: append ## Stuck? if missing."""
    if STUCK_RE.search(text):
        return text, False
    # Strip trailing whitespace/newlines then append
    new_text = text.rstrip() + "\n" + STUCK_BLOCK
    return new_text, True


def rename_part6_to_part7(text: str) -> tuple[str, bool]:
    """T3: rename any Part 6 heading to Part 7 — Wrap-up & Connection; update table."""
    parts = count_parts(text)
    if parts != 6:
        return text, False

    # Match any Part 6 heading (regardless of the topic name)
    part6_any_re = re.compile(
        r"^## Part 6 — (.+?)(\s*·\s*\d+\s*min)?$",
        re.MULTILINE,
    )
    m = part6_any_re.search(text)
    if not m:
        return text, False

    old_heading = m.group(0)
    # Preserve time annotation if present, default to 10 min
    time_part = m.group(2) if m.group(2) else f" · 10 min"
    new_heading = f"## Part 7 — Wrap-up & Connection{time_part}"
    new_text = text.replace(old_heading, new_heading, 1)

    # Update lesson plan table row: "| Part 6 | ... |" -> "| 7 | ... |"
    table_p6_re = re.compile(r"(\|\s*)Part\s*6(\s*\|)", re.MULTILINE)
    new_text, _ = table_p6_re.subn(r"\g<1>7\g<2>", new_text)

    return new_text, True


def rename_part7_heading(text: str) -> tuple[str, bool]:
    """T4: rename misnamed Part 7 heading (wrong title text) to canonical."""
    if PART7_CANONICAL.search(text):
        return text, False  # already correct
    parts = count_parts(text)
    if parts < 7:
        return text, False

    # Find Part 7 heading with wrong name
    part7_wrong_re = re.compile(
        r"^## Part 7 — (?!Wrap-up & Connection)(.+?)(\s*·\s*\d+\s*min)?$",
        re.MULTILINE,
    )
    m = part7_wrong_re.search(text)
    if not m:
        return text, False

    old_heading = m.group(0)
    time_part = m.group(2) if m.group(2) else " · 10 min"
    new_heading = f"## Part 7 — Wrap-up & Connection{time_part}"
    new_text = text.replace(old_heading, new_heading, 1)

    # Update table row similarly
    table_p7_re = re.compile(
        r"(\|\s*)(?:Part\s*)?7(\s*\|[^\n]*(?:Wrap-up|Open Lab|Close|Pre-read)[^\n]*\|)",
        re.MULTILINE,
    )
    new_text, _ = table_p7_re.subn(r"\g<1>7\g<2>", new_text)

    return new_text, True


def normalize_lesson_plan_table(text: str) -> tuple[str, bool]:
    """Normalize lesson plan table header row to canonical column names."""
    # Old: | Part | Activity Type | Duration |
    # New: | Part | What you do | Time |
    old_header = re.compile(
        r"(\| Part \|)\s*Activity Type\s*(\|)\s*Duration\s*(\|)",
        re.MULTILINE,
    )
    new_text, n = old_header.subn(r"\1 What you do \2 Time \3", text)
    return new_text, n > 0


def migrate_file(path: Path, dry_run: bool = False) -> list[str]:
    """Apply all transforms to a single file. Returns list of changes made."""
    text = path.read_text(encoding="utf-8")
    shape = classify(text)

    if shape != "B7":
        return []

    changes = []
    current = text

    # T1: fold standalone ## Pre-read H2
    current, changed = fold_preread_h2(current)
    if changed:
        changes.append("T1: folded ## Pre-read for tomorrow H2 → H3 inside Part 7")

    # T3: rename Part 6 Wrap-up → Part 7
    current, changed = rename_part6_to_part7(current)
    if changed:
        changes.append("T3: renamed Part 6 Wrap-up & Connection → Part 7")

    # T4: rename misnamed Part 7 heading
    current, changed = rename_part7_heading(current)
    if changed:
        changes.append("T4: renamed Part 7 heading to canonical 'Wrap-up & Connection'")

    # Normalize lesson plan table
    current, changed = normalize_lesson_plan_table(current)
    if changed:
        changes.append("Tx: normalized lesson plan table header (Activity Type→What you do, Duration→Time)")

    # T2: add ## Stuck? (do last so it's always at end)
    current, changed = add_stuck(current)
    if changed:
        changes.append("T2: added ## Stuck? block")

    if current == text:
        return []

    if not dry_run:
        shutil.copy2(path, path.with_suffix(".md.bak"))
        path.write_text(current, encoding="utf-8")

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate B7 lesson files to canonical format")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing files")
    parser.add_argument("--week", help="Process a single week (e.g. week-01)")
    args = parser.parse_args()

    total_files = 0
    total_changes = 0

    weeks = sorted(LESSONS_DIR.iterdir()) if LESSONS_DIR.exists() else []
    if args.week:
        weeks = [w for w in weeks if w.name == args.week]

    for week_dir in weeks:
        if not week_dir.is_dir():
            continue
        for mod_dir in sorted(week_dir.iterdir()):
            if not mod_dir.is_dir() or not MODULE_NAME_RE.match(mod_dir.name):
                continue
            index = mod_dir / "index.md"
            if not index.exists():
                continue

            changes = migrate_file(index, dry_run=args.dry_run)
            if changes:
                total_files += 1
                total_changes += len(changes)
                prefix = "[DRY-RUN] " if args.dry_run else ""
                print(f"\n{prefix}{index.relative_to(REPO_ROOT)}")
                for c in changes:
                    print(f"  • {c}")

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}Done: {total_files} file(s) modified, {total_changes} transform(s) applied.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
