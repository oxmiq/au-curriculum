#!/usr/bin/env python3
"""Walk docs/lessons/ and emit a single catalog.json describing the curriculum.

The catalog is the **filesystem's view** of the curriculum — it is intentionally
derived, never hand-edited. Commit it so reviewers can diff curriculum changes,
and so CI can verify the committed file matches the regenerated one.

Schema (v1):

    {
      "schema_version": 1,
      "generated_at": "<utc iso8601>",
      "module_count": <int>,
      "modules": [
        {
          "id": "module-NN",
          "title": "<H1 of index.md, or null>",
          "index": "docs/lessons/module-NN/index.md",
          "assignment": "docs/lessons/module-NN/assignment.md" | null,
          "quiz": "docs/lessons/module-NN/quiz.html" | null,
          "days": [
            { "id": "01", "slug": "<slug>", "title": "<H1>", "path": "..." },
            ...
          ],
          "source_material": [ "<relative path on disk>", ... ]
        },
        ...
      ]
    }

Usage:
    python3 scripts/build_catalog.py                # writes <repo>/catalog.json
    python3 scripts/build_catalog.py --stdout       # emit to stdout, write nothing
    python3 scripts/build_catalog.py --check        # exit 1 if regenerating
                                                    # would change the file on disk
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "docs" / "lessons"
CATALOG_PATH = REPO_ROOT / "catalog.json"

MODULE_NAME_RE = re.compile(r"^module-(\d{2})$")
DAY_FILE_RE = re.compile(r"^(0\d)-([a-z0-9][a-z0-9-]*)\.md$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SOURCE_LINK_RE = re.compile(r"\]\((\.\./\.\./\.\./planning/source-material/[^)]+)\)")


def extract_h1(file_path: Path) -> str | None:
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = H1_RE.search(text)
    return m.group(1).strip() if m else None


def relative_to_repo(p: Path) -> str:
    return str(p.relative_to(REPO_ROOT)).replace("\\", "/")


def collect_source_material(module_dir: Path) -> list[str]:
    seen: set[str] = set()
    for md_file in module_dir.glob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue
        for raw_link in SOURCE_LINK_RE.findall(text):
            decoded = unquote(raw_link)
            target = (md_file.parent / decoded).resolve()
            if target.exists():
                seen.add(relative_to_repo(target))
    return sorted(seen)


def build_module(module_dir: Path) -> dict | None:
    name = module_dir.name
    if not MODULE_NAME_RE.match(name):
        return None

    index_md = module_dir / "index.md"
    quiz = module_dir / "quiz.html"
    assignment = module_dir / "assignment.md"

    days: list[dict] = []
    for day_file in sorted(module_dir.iterdir()):
        m = DAY_FILE_RE.match(day_file.name)
        if not m:
            continue
        days.append(
            {
                "id": m.group(1),
                "slug": m.group(2),
                "title": extract_h1(day_file),
                "path": relative_to_repo(day_file),
            }
        )

    return {
        "id": name,
        "title": extract_h1(index_md) if index_md.exists() else None,
        "index": relative_to_repo(index_md) if index_md.exists() else None,
        "assignment": relative_to_repo(assignment) if assignment.exists() else None,
        "quiz": relative_to_repo(quiz) if quiz.exists() else None,
        "days": days,
        "source_material": collect_source_material(module_dir),
    }


def build_catalog() -> dict:
    modules: list[dict] = []
    if LESSONS_DIR.exists():
        for module_dir in sorted(p for p in LESSONS_DIR.iterdir() if p.is_dir()):
            entry = build_module(module_dir)
            if entry is not None:
                modules.append(entry)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "module_count": len(modules),
        "modules": modules,
    }


def serialize(catalog: dict) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def _strip_timestamp(text: str) -> str:
    """Strip the generated_at line so --check ignores wall-clock drift."""
    return re.sub(r'\s+"generated_at": "[^"]+",\n', "\n", text, count=1)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the curriculum catalog from disk")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout; do not touch catalog.json")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if catalog.json on disk differs from the regenerated catalog (ignoring generated_at)",
    )
    args = parser.parse_args()

    catalog = build_catalog()
    text = serialize(catalog)

    if args.stdout:
        sys.stdout.write(text)
        return 0

    if args.check:
        if not CATALOG_PATH.exists():
            print("catalog.json is missing; run `python3 scripts/build_catalog.py`", file=sys.stderr)
            return 1
        existing = CATALOG_PATH.read_text(encoding="utf-8")
        if _strip_timestamp(existing) != _strip_timestamp(text):
            print("catalog.json is out of date; run `python3 scripts/build_catalog.py`", file=sys.stderr)
            return 1
        return 0

    CATALOG_PATH.write_text(text, encoding="utf-8")
    print(f"wrote {relative_to_repo(CATALOG_PATH)} ({catalog['module_count']} module(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
