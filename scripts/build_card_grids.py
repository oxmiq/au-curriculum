"""Generate card-grid HTML blocks for the au-curriculum catalog pages.

Sources of truth:
  * ``mkdocs.yml`` — the canonical nav structure (weeks + modules + paths).
  * ``docs/lessons/week-XX/index.md`` — the per-week overview page.
  * ``docs/curriculum.md``           — the top-level curriculum page.

This script writes (or rewrites) an auto-generated card-grid block bounded
by two HTML comment markers inside each target page:

    <!-- AUTO-GEN:CARD-GRID:START -->
    ...generated HTML...
    <!-- AUTO-GEN:CARD-GRID:END -->

If the markers are absent, the block is inserted at the first sensible spot
(after the leading blockquote(s) and before the first ``## `` heading).

Re-running is idempotent: the block is replaced wholesale on each run.

Card status pills are emitted as ``{status:week-XX/module-Y}`` tokens; the
Phase D mkdocs hook (``hooks/progress_badges.py``) substitutes them at build
time using ``docs/progress/summary.json``.

Usage::

    python scripts/build_card_grids.py            # rewrite all targets
    python scripts/build_card_grids.py --check    # exit 1 if drift detected
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
MKDOCS_YML = ROOT / "mkdocs.yml"
DOCS = ROOT / "docs"

START = "<!-- AUTO-GEN:CARD-GRID:START -->"
END = "<!-- AUTO-GEN:CARD-GRID:END -->"

WEEK_TITLE_RE = re.compile(r"^Week\s+(\d+)\s+—\s+(.+)$")


# ── parse the canonical structure out of mkdocs.yml ────────────────────────

def _load_mkdocs_nav() -> list:
    """Read mkdocs.yml as plain YAML.

    MkDocs uses a couple of custom YAML tags (e.g. ``!!python/name:``); they
    only appear in the ``markdown_extensions`` block, which we don't touch.
    A permissive Loader handles them by registering a passthrough.
    """
    class _Tolerant(yaml.SafeLoader):
        pass

    def _passthrough(loader, tag_suffix, node):  # noqa: ARG001
        return None

    yaml.add_multi_constructor("tag:yaml.org,2002:python/name:",
                               _passthrough, Loader=_Tolerant)
    yaml.add_multi_constructor("!!python/name:",
                               _passthrough, Loader=_Tolerant)

    with MKDOCS_YML.open("r", encoding="utf-8") as f:
        cfg = yaml.load(f, Loader=_Tolerant)
    return cfg["nav"]


def _extract_weeks(nav: list) -> list[dict]:
    """Return [{number, full_title, path, modules: [{day, title, path}]}, ...].

    The shape we expect under "Learn" is::

        - Learn:
            - Curriculum: curriculum.md
            - "Week 1 — Orientation & Foundations":
                - Overview: lessons/week-01/index.md
                - "Day 1 · Welcome & Context": lessons/week-01/module-1/index.md
                ...
    """
    learn = None
    for entry in nav:
        if isinstance(entry, dict) and "Learn" in entry:
            learn = entry["Learn"]
            break
    if not learn:
        raise SystemExit("could not find 'Learn' top-level tab in mkdocs.yml nav")

    weeks: list[dict] = []
    for entry in learn:
        if not isinstance(entry, dict):
            continue
        for label, children in entry.items():
            m = WEEK_TITLE_RE.match(label)
            if not m or not isinstance(children, list):
                continue
            number = int(m.group(1))
            subtitle = m.group(2).strip()
            week = {
                "number": number,
                "subtitle": subtitle,
                "full_title": label,
                "path": None,
                "modules": [],
            }
            for child in children:
                if not isinstance(child, dict):
                    continue
                for ck, cv in child.items():
                    if ck == "Overview":
                        week["path"] = cv
                    elif ck.startswith("Day "):
                        # "Day 7 · Meet the GPU"
                        day_num = int(ck.split()[1])
                        title = ck.split("·", 1)[1].strip() if "·" in ck else ck
                        week["modules"].append({
                            "day": day_num,
                            "title": title,
                            "path": cv,
                        })
            weeks.append(week)
    weeks.sort(key=lambda w: w["number"])
    return weeks


# ── card HTML generators ───────────────────────────────────────────────────

def _module_id_from_path(path: str) -> str:
    """``lessons/week-02/module-3/index.md`` → ``week-02/module-3``."""
    m = re.search(r"(week-\d{2}/module-\d+)", path)
    return m.group(1) if m else path


def _relative_from_week_index(target_path: str, week_number: int) -> str:
    """All week module paths start with ``lessons/week-XX/module-Y/index.md``;
    relative to ``lessons/week-XX/index.md`` the prefix is just ``module-Y/``.
    """
    prefix = f"lessons/week-{week_number:02d}/"
    if target_path.startswith(prefix):
        return target_path[len(prefix):]
    return target_path


def _module_card(week_number: int, mod: dict) -> str:
    href = _relative_from_week_index(mod["path"], week_number)
    module_id = _module_id_from_path(mod["path"])
    return (
        f'  <a class="ox-card" href="{href}" style="--i:{mod["day"]}">\n'
        f'    {{status:{module_id}}}\n'
        f'    <span class="ox-card__eyebrow">Day {mod["day"]}</span>\n'
        f'    <h3 class="ox-card__title">{mod["title"]}</h3>\n'
        f'    <span class="ox-card__cta">Open lesson →</span>\n'
        f'  </a>'
    )


def _week_module_grid(week: dict) -> str:
    cards = "\n".join(_module_card(week["number"], m) for m in week["modules"])
    return (
        f"{START}\n"
        f'<div class="ox-card-grid" markdown="0">\n'
        f"{cards}\n"
        f"</div>\n"
        f"{END}"
    )


def _week_card(week: dict) -> str:
    # The curriculum.md sits at docs/curriculum.md; its href to a week is
    # lessons/week-XX/.
    href = f"lessons/week-{week['number']:02d}/"
    module_count = len(week["modules"])
    return (
        f'  <a class="ox-card" href="{href}" style="--i:{week["number"]}">\n'
        f'    <span class="ox-card__eyebrow">Week {week["number"]:02d}</span>\n'
        f'    <h3 class="ox-card__title">{week["subtitle"]}</h3>\n'
        f'    <p class="ox-card__desc">{module_count} half-day sessions · '
        f'pre-read · concept · practice · Friday consolidation.</p>\n'
        f'    <span class="ox-card__cta">Open week →</span>\n'
        f'  </a>'
    )


def _curriculum_week_grid(weeks: list[dict]) -> str:
    cards = "\n".join(_week_card(w) for w in weeks)
    return (
        f"{START}\n"
        f'<div class="ox-card-grid" markdown="0">\n'
        f"{cards}\n"
        f"</div>\n"
        f"{END}"
    )


# ── file rewriter ──────────────────────────────────────────────────────────

def _insert_or_replace_block(text: str, block: str) -> str:
    """Replace an existing AUTO-GEN block, or insert one after the leading
    blockquote(s) of the file (and before the first ``## `` heading)."""
    if START in text and END in text:
        pattern = re.compile(re.escape(START) + r".*?" + re.escape(END),
                             flags=re.DOTALL)
        return pattern.sub(block, text, count=1)

    lines = text.splitlines(keepends=False)
    insert_at = None
    seen_h1 = False
    in_blockquote = False

    for i, line in enumerate(lines):
        if not seen_h1 and line.startswith("# "):
            seen_h1 = True
            continue
        if not seen_h1:
            continue
        # past H1 — find end of leading blockquote block(s) + blank gaps
        if line.startswith(">"):
            in_blockquote = True
            continue
        if in_blockquote and line.strip() == "":
            continue
        if line.startswith("## ") or line.startswith("---"):
            insert_at = i
            break
        # any other non-empty content: insert right before it
        if line.strip() and not line.startswith(">"):
            insert_at = i
            break

    if insert_at is None:
        # fallback: append at end
        return text.rstrip() + "\n\n" + block + "\n"

    head = "\n".join(lines[:insert_at]).rstrip()
    tail = "\n".join(lines[insert_at:]).lstrip("\n")
    return f"{head}\n\n{block}\n\n{tail}\n"


def _process_file(path: Path, block: str, check: bool) -> bool:
    """Returns True if the file already matched the desired block."""
    original = path.read_text(encoding="utf-8")
    updated = _insert_or_replace_block(original, block)
    if updated == original:
        return True
    if check:
        return False
    path.write_text(updated, encoding="utf-8")
    print(f"  wrote  {path.relative_to(ROOT)}")
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if any file would be modified")
    args = ap.parse_args()

    nav = _load_mkdocs_nav()
    weeks = _extract_weeks(nav)

    if not weeks:
        print("no weeks found — aborting", file=sys.stderr)
        return 2

    all_clean = True

    # 1. Per-week index pages.
    for week in weeks:
        target = DOCS / "lessons" / f"week-{week['number']:02d}" / "index.md"
        if not target.is_file():
            print(f"  miss   {target.relative_to(ROOT)} (skipped)")
            continue
        clean = _process_file(target, _week_module_grid(week), args.check)
        all_clean = all_clean and clean

    # 2. Top-level curriculum page.
    curriculum = DOCS / "curriculum.md"
    if curriculum.is_file():
        clean = _process_file(curriculum, _curriculum_week_grid(weeks), args.check)
        all_clean = all_clean and clean

    if args.check and not all_clean:
        print("drift detected — run `python scripts/build_card_grids.py`", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
