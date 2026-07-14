#!/usr/bin/env python3
"""Walk docs/lessons/ and emit a single catalog.json — week-XX/module-Y schema.

The catalog is derived from the filesystem and is committed so reviewers can
diff curriculum changes and so CI can verify it stays in sync.

Schema (v2):

    {
      "schema_version": 2,
      "generated_at": "<utc iso8601>",
      "week_count": 10,
      "module_count": 51,
      "weeks": [
        {
          "id": "week-01",
          "title": "<H1 of week overview index.md>",
          "overview": "docs/lessons/week-01/index.md",
          "modules": [
            {
              "id": "week-01/module-1",
              "title": "<H1 of module index.md>",
              "index": "docs/lessons/week-01/module-1/index.md",
              "assignment": ".../assignment.md" | null,
              "knowledge_check": ".../knowledge-check.md" | null,
              "supplementary": [ ".../supplementary-NN-slug.md", ... ],
              "source_material": [ "<relative on-disk path>", ... ]
            }, ...
          ]
        }, ...
      ]
    }

Usage:
    python3 scripts/build_catalog.py                # writes <repo>/catalog.json
    python3 scripts/build_catalog.py --stdout       # emit to stdout, write nothing
    python3 scripts/build_catalog.py --check        # exit 1 if regenerating would change the file
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

WEEK_NAME_RE = re.compile(r"^week-(\d{2})$")
MODULE_NAME_RE = re.compile(r"^module-([1-9])$")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
SUPPLEMENTARY_RE = re.compile(r"^supplementary-\d{2}-[a-z0-9-]+\.md$")
SOURCE_LINK_RE = re.compile(r"\]\((\.\./\.\./\.\./(?:\.\./)?planning/source-material/[^)]+)\)")


def extract_h1(file_path: Path):
    """First H1 in a markdown file, skipping YAML frontmatter."""
    try:
        text = file_path.read_text(encoding="utf-8")
    except OSError:
        return None
    body = text
    if body.startswith("---\n"):
        end = body.find("\n---\n", 4)
        if end != -1:
            body = body[end + 5 :]
    m = H1_RE.search(body)
    return m.group(1).strip() if m else None


def collect_source_links(text: str, parent: Path):
    found = []
    for link in SOURCE_LINK_RE.findall(text):
        target_rel = unquote(link)
        target = (parent / target_rel).resolve()
        try:
            rel_to_repo = target.relative_to(REPO_ROOT)
        except ValueError:
            continue
        found.append(rel_to_repo.as_posix())
    return sorted(set(found))


def relpath(p: Path):
    # as_posix() so paths are forward-slashed on every OS (stable across
    # Windows dev + Linux CI; the committed catalog uses "/").
    return p.relative_to(REPO_ROOT).as_posix()


def build_module(module_dir: Path):
    name = module_dir.name
    week_id = module_dir.parent.name
    mid = f"{week_id}/{name}"

    index_md = module_dir / "index.md"
    assignment_md = module_dir / "assignment.md"
    kc_md = module_dir / "knowledge-check.md"

    supplementary = []
    sources = set()

    if index_md.exists():
        try:
            text = index_md.read_text(encoding="utf-8")
            sources.update(collect_source_links(text, index_md.parent))
        except OSError:
            pass

    for sub in sorted(module_dir.iterdir()):
        if sub.is_file() and SUPPLEMENTARY_RE.match(sub.name):
            supplementary.append(relpath(sub))
            try:
                text = sub.read_text(encoding="utf-8")
                sources.update(collect_source_links(text, sub.parent))
            except OSError:
                pass

    if assignment_md.exists():
        try:
            text = assignment_md.read_text(encoding="utf-8")
            sources.update(collect_source_links(text, assignment_md.parent))
        except OSError:
            pass

    return {
        "id": mid,
        "title": extract_h1(index_md) if index_md.exists() else None,
        "index": relpath(index_md) if index_md.exists() else None,
        "assignment": relpath(assignment_md) if assignment_md.exists() else None,
        "knowledge_check": relpath(kc_md) if kc_md.exists() else None,
        "supplementary": supplementary,
        "source_material": sorted(sources),
    }


def build_week(week_dir: Path):
    name = week_dir.name
    overview = week_dir / "index.md"
    modules = []
    for sub in sorted(week_dir.iterdir()):
        if sub.is_dir() and MODULE_NAME_RE.match(sub.name):
            modules.append(build_module(sub))
    return {
        "id": name,
        "title": extract_h1(overview) if overview.exists() else None,
        "overview": relpath(overview) if overview.exists() else None,
        "modules": modules,
    }


def build_catalog():
    weeks = []
    for sub in sorted(LESSONS_DIR.iterdir()):
        if sub.is_dir() and WEEK_NAME_RE.match(sub.name):
            weeks.append(build_week(sub))
    module_count = sum(len(w["modules"]) for w in weeks)
    return {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "week_count": len(weeks),
        "module_count": module_count,
        "weeks": weeks,
    }


def emit(catalog, stdout: bool):
    data = json.dumps(catalog, indent=2) + "\n"
    if stdout:
        sys.stdout.write(data)
    else:
        CATALOG_PATH.write_text(data, encoding="utf-8")
        print(f"wrote {CATALOG_PATH.relative_to(REPO_ROOT)} — "
              f"{catalog['week_count']} weeks, {catalog['module_count']} modules")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build catalog.json from docs/lessons/")
    parser.add_argument("--stdout", action="store_true", help="Emit JSON to stdout, do not write")
    parser.add_argument("--check", action="store_true", help="Exit 1 if catalog.json would change")
    args = parser.parse_args()

    catalog = build_catalog()

    if args.check:
        new_text = json.dumps(catalog, indent=2) + "\n"
        # Strip generated_at for the comparison so a same-content rebuild doesn't fail.
        check_new = json.loads(new_text)
        check_new.pop("generated_at", None)
        if CATALOG_PATH.exists():
            existing = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
            existing.pop("generated_at", None)
        else:
            existing = None
        if existing != check_new:
            print("catalog.json is out of date; run `python3 scripts/build_catalog.py`",
                  file=sys.stderr)
            return 1
        print("catalog.json is up to date")
        return 0

    emit(catalog, args.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
