"""Insert a standard lesson-header band at the top of every module page.

The header is an HTML block bounded by markers so the script is idempotent::

    <!-- AUTO-GEN:LESSON-HEADER:START -->
    <div class="ox-lesson-header" markdown="0">
      <div class="ox-lesson-header__crumbs">
        <a href="../../../">Home</a>
        <span class="sep">/</span>
        <a href="../../">Learn</a>
        <span class="sep">/</span>
        <a href="../">Week 2 — The GPU &amp; Memory</a>
        <span class="sep">/</span>
        <span>Day 7 · Meet the GPU</span>
        {status:week-02/module-2}
      </div>
      <div class="ox-lesson-header__cta">
        <a class="md-button" href="#pre-read-for-tomorrow">Pre-read</a>
        <a class="md-button md-button--primary" href="knowledge-check/">Knowledge check</a>
        <a class="md-button" href="assignment/">Assignment</a>
        <a class="md-button" href="https://github.com/oxmiq/au-curriculum/tree/main/planning/source-material/Inference%20Engineering">Source material</a>
      </div>
    </div>
    <!-- AUTO-GEN:LESSON-HEADER:END -->

Mapping of week → source-material folder name is canonical: when a week page
references a different folder we honour that mapping here.

Run::

    python scripts/apply_lesson_header.py            # update all 51 modules
    python scripts/apply_lesson_header.py --check    # exit 1 on drift
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

START = "<!-- AUTO-GEN:LESSON-HEADER:START -->"
END = "<!-- AUTO-GEN:LESSON-HEADER:END -->"

# Per-week source-material folder mapping (matches planning/source-material/).
# Multiple weeks can share a folder (e.g. Phase 1 weeks 2–5 all reference
# "Inference Engineering").
SOURCE_FOLDER_BY_WEEK = {
    1:  "Orientation",
    2:  "Inference Engineering",
    3:  "Inference Engineering",
    4:  "Inference Engineering",
    5:  "Inference Engineering",
    6:  "Prompt Engineering",          # Day 26 — combined-week's first half
    7:  "AI Agents",
    8:  "Capsule Power User",
    9:  "Capsule Power User",
    10: "Capstone",
}

# Approximate duration text per module. Friday (consolidation/wrap) sessions
# are typically lighter; Week 10 (capstone) days are full-day milestones.
def _duration_label(week: int, day_in_week: int, total_in_week: int) -> str:
    if week == 10:
        return "Full-day milestone"
    if day_in_week == total_in_week:
        return "Friday · review &amp; wrap"
    return "~3 hrs"

WEEK_TITLE_RE = re.compile(r"^Week\s+(\d+)\s+—\s+(.+)$")


# ── nav parsing ────────────────────────────────────────────────────────────

def _load_nav() -> list:
    class _Tolerant(yaml.SafeLoader):
        pass

    def _passthrough(loader, tag_suffix, node):  # noqa: ARG001
        return None

    yaml.add_multi_constructor("tag:yaml.org,2002:python/name:",
                               _passthrough, Loader=_Tolerant)
    yaml.add_multi_constructor("!!python/name:",
                               _passthrough, Loader=_Tolerant)

    return yaml.load(MKDOCS_YML.read_text(encoding="utf-8"), Loader=_Tolerant)["nav"]


def _extract_weeks(nav: list) -> list[dict]:
    for entry in nav:
        if isinstance(entry, dict) and "Learn" in entry:
            learn = entry["Learn"]
            break
    else:
        raise SystemExit("could not find 'Learn' tab in mkdocs.yml nav")

    weeks: list[dict] = []
    for entry in learn:
        if not isinstance(entry, dict):
            continue
        for label, children in entry.items():
            m = WEEK_TITLE_RE.match(label)
            if not m or not isinstance(children, list):
                continue
            number = int(m.group(1))
            week = {
                "number": number,
                "subtitle": m.group(2).strip(),
                "full_title": label,
                "modules": [],
            }
            for child in children:
                if not isinstance(child, dict):
                    continue
                for ck, cv in child.items():
                    if ck.startswith("Day "):
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


# ── header HTML ────────────────────────────────────────────────────────────

def _module_id_from_path(path: str) -> str:
    m = re.search(r"(week-(\d{2})/module-(\d+))", path)
    return m.group(1) if m else path


def _lesson_header_block(week: dict, module: dict, day_in_week: int,
                          total_in_week: int) -> str:
    week_num = week["number"]
    module_id = _module_id_from_path(module["path"])
    duration = _duration_label(week_num, day_in_week, total_in_week)
    week_title_escaped = week["full_title"].replace("&", "&amp;")
    full_module_label = f'Day {module["day"]} · {module["title"]}'
    source_folder = SOURCE_FOLDER_BY_WEEK.get(week_num)
    # URL-encode spaces in the source-material folder for the GitHub link.
    source_url = (
        f"https://github.com/oxmiq/au-curriculum/tree/main/"
        f"planning/source-material/"
        + (source_folder.replace(' ', '%20') if source_folder else "")
    )

    # Anchor for the "Pre-read" button: every module ends with a
    # "## Pre-read for tomorrow" section. Anchor slug is created by
    # toc; we use a robust fallback to the page top if the heading is
    # absent (handled by browsers — empty fragment scrolls to top).
    pre_read_anchor = "#pre-read-for-tomorrow"

    return (
        f"{START}\n"
        f'<div class="ox-lesson-header" markdown="0">\n'
        f'  <div class="ox-lesson-header__crumbs">\n'
        f'    <a href="../../../">Home</a>\n'
        f'    <span class="sep">/</span>\n'
        f'    <a href="../../">Learn</a>\n'
        f'    <span class="sep">/</span>\n'
        f'    <a href="../">{week_title_escaped}</a>\n'
        f'    <span class="sep">/</span>\n'
        f'    <span>{full_module_label}</span>\n'
        f'    {{status:{module_id}}}\n'
        f'  </div>\n'
        f'  <div class="ox-lesson-header__cta">\n'
        f'    <a class="md-button" href="{pre_read_anchor}">Pre-read</a>\n'
        f'    <a class="md-button md-button--primary" href="knowledge-check/">Knowledge check</a>\n'
        f'    <a class="md-button" href="assignment/">Assignment</a>\n'
        f'    <a class="md-button" href="{source_url}">Source material</a>\n'
        f'  </div>\n'
        f'</div>\n'
        f"{END}"
    )


# ── file rewriter ──────────────────────────────────────────────────────────

def _insert_or_replace(text: str, block: str) -> str:
    """Insert block immediately after the H1 (and any leading blockquote(s))."""
    if START in text and END in text:
        pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
        return pat.sub(block, text, count=1)

    lines = text.splitlines(keepends=False)
    # find end of H1 + leading blockquote(s)
    insert_at = None
    seen_h1 = False
    after_h1 = False
    in_bq = False
    for i, line in enumerate(lines):
        if not seen_h1:
            if line.startswith("# "):
                seen_h1 = True
                after_h1 = True
            continue
        if after_h1 and line.startswith(">"):
            in_bq = True
            continue
        if in_bq and line.strip() == "":
            # eat blank lines that may follow a blockquote
            continue
        # first non-blockquote, non-blank line: insert here
        if line.strip() == "" and not in_bq:
            continue
        insert_at = i
        break

    if insert_at is None:
        return text.rstrip() + "\n\n" + block + "\n"
    head = "\n".join(lines[:insert_at]).rstrip()
    tail = "\n".join(lines[insert_at:]).lstrip("\n")
    return f"{head}\n\n{block}\n\n{tail}\n"


def _process(path: Path, block: str, check: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = _insert_or_replace(original, block)
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

    weeks = _extract_weeks(_load_nav())
    all_clean = True
    for week in weeks:
        total = len(week["modules"])
        for idx, mod in enumerate(week["modules"], start=1):
            target = ROOT / "docs" / mod["path"]
            if not target.is_file():
                print(f"  miss   {target.relative_to(ROOT)} (skipped)")
                continue
            block = _lesson_header_block(week, mod, idx, total)
            clean = _process(target, block, args.check)
            all_clean = all_clean and clean

    if args.check and not all_clean:
        print("drift detected — run `python scripts/apply_lesson_header.py`",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
