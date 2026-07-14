#!/usr/bin/env python3
"""Build docs/kb/flashcards.json from the source-material flashcard files.

Each phase ships a `*-Flashcards.md` deck under planning/source-material/.
Every deck is authored as Markdown tables grouped by `## ` headings::

    ## Day 26 — Prompt Structure & Clarity

    | # | Q | A |
    |---|---|---|
    | 1 | What are the two structural slots…? | System prompt and user turn(s). |
    | 2 | …                                   | …                                 |

This script reads the four decks, extracts each `| n | question | answer |`
row into a `{q, a}` card, groups cards under the heading they fall beneath,
and writes a single `flashcards.json` the Reference-tab flashcards page renders.

Group labels are TOPIC-based: a leading `Day NN —` prefix on a heading is
stripped for display (the day number is kept only as an ordering hint). This
keeps the deck aligned with the curriculum's own day numbering instead of the
original stand-alone course numbering — the same principle behind the
topic-anchored pre-reads.

Usage::

    python scripts/build_flashcards.py            # write flashcards.json
    python scripts/build_flashcards.py --dry-run  # report only
    python scripts/build_flashcards.py --check     # exit 1 if output would change

Idempotent. Re-run whenever a deck changes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "kb" / "flashcards.json"
SOURCE_ROOT = REPO / "planning" / "source-material"

# Deck file -> metadata. Order here is the display order (curriculum order).
DECKS = [
    {
        "id": "inference",
        "title": "Inference Engineering",
        "phase": "inference",
        "file": "Inference Engineering/Inference_Engineering_Flashcards.md",
    },
    {
        "id": "prompting",
        "title": "Prompt Engineering",
        "phase": "prompting",
        "file": "Prompt Engineering/Prompt-Engineering-Flashcards.md",
    },
    {
        "id": "agents",
        "title": "AI Agents",
        "phase": "agents",
        "file": "AI Agents/AI Agents - Flashcards.md",
    },
    {
        "id": "capsule",
        "title": "Capsule Power-User",
        "phase": "capsule",
        "file": "Capsule Power User/Capsule-Power-User-Flashcards.md",
    },
]

# Headings that are prose, not card groups (skip even if they somehow parse).
SKIP_HEADINGS = re.compile(r"how to use these cards|self-test order", re.IGNORECASE)

# "Day 26 — Topic" / "Day 26 - Topic"  ->  (26, "Topic")
DAY_PREFIX = re.compile(r"^Day\s+(\d+)\s*[—–-]\s*(.+)$", re.IGNORECASE)
# "Appendix A — Numerical anchors" -> "Numerical anchors" (drop the appendix tag)
APPENDIX_PREFIX = re.compile(r"^Appendix\s+\w+\s*[—–-]\s*(.+)$", re.IGNORECASE)

# Header first-cell values that mark an index column (dropped from the card).
INDEX_MARKERS = {"", "#", "no", "no.", "n", "id", "card"}


def normalize_dashes(text: str) -> str:
    """House style: no em/en dashes. `a — b` -> `a - b`, `a–b` -> `a-b`."""
    return text.replace("—", "-").replace("–", "-")


def clean_cell(text: str) -> str:
    """Collapse whitespace, drop em/en dashes, unescape a literal `\\|`."""
    text = text.replace(r"\|", "|")
    text = normalize_dashes(text)
    return re.sub(r"\s+", " ", text).strip()


def split_row(line: str) -> list[str] | None:
    """A GitHub table row -> list of trimmed cell strings, or None if not a row."""
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s.strip("|")
    # Split on unescaped pipes only.
    cells = re.split(r"(?<!\\)\|", s)
    return [c.strip() for c in cells]


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells if c is not None) and bool(cells)


def next_nonempty(lines: list[str], i: int) -> str | None:
    for j in range(i + 1, len(lines)):
        if lines[j].strip():
            return lines[j]
    return None


def clean_heading(heading: str) -> tuple[str, int | None]:
    """(display title, day-or-None). Strips a `Day NN —` / `Appendix X —` tag."""
    m = DAY_PREFIX.match(heading)
    if m:
        return normalize_dashes(m.group(2).strip()), int(m.group(1))
    m = APPENDIX_PREFIX.match(heading)
    if m:
        return normalize_dashes(m.group(1).strip()), None
    return normalize_dashes(heading), None


def parse_row(cells: list[str], indexed: bool) -> tuple[str, str] | None:
    """Map a data row to (question, answer) using the table's column schema.

    `indexed` is decided from the header row: a leading index column (``#``,
    ``N1`` …) is dropped so Q=cell[1], A=cell[2:]; otherwise the table is a
    plain two-column Q/A (e.g. the command-recall ``Goal | Command`` tier) and
    Q=cell[0], A=cell[1:]. Trailing cells are rejoined so an answer that itself
    contained a pipe survives.
    """
    if indexed and len(cells) >= 3:
        q, a = clean_cell(cells[1]), clean_cell(" ".join(cells[2:]))
    elif len(cells) >= 2:
        q, a = clean_cell(cells[0]), clean_cell(" ".join(cells[1:]))
    else:
        return None
    return (q, a) if q and a else None


def parse_deck(path: Path) -> list[dict]:
    """Return [{title, day, cards:[{q,a}]}, ...] in document order.

    Every Markdown table under a heading (``#``/``##``/``###``) is a card group.
    The header row (the one directly above the ``|---|`` separator) both sets the
    column schema — whether a leading index column should be dropped — and is
    itself skipped. Prose sections (``How to use…``, self-test order) and any
    group that yields no cards are dropped.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    groups: list[dict] = []
    current: dict | None = None
    indexed = False          # current table's schema; reset when a table ends

    for i, line in enumerate(lines):
        h = re.match(r"^#{1,3}\s+(.+?)\s*$", line)
        if h:
            heading = h.group(1).strip()
            indexed = False
            if SKIP_HEADINGS.search(heading):
                current = None
                continue
            title, day = clean_heading(heading)
            current = {"title": title, "day": day, "cards": []}
            groups.append(current)
            continue

        cells = split_row(line)
        if not cells:                       # non-table line ends any open table
            indexed = False
            continue
        if is_separator(cells):
            continue
        if current is None:
            continue

        # A header row is the one directly above the |---| separator. Use it to
        # set the schema (index column present?) and then skip it.
        nxt = next_nonempty(lines, i)
        nxt_cells = split_row(nxt) if nxt else None
        if nxt_cells and is_separator(nxt_cells):
            first = (cells[0] or "").strip().lower()
            indexed = len(cells) >= 3 and first in INDEX_MARKERS
            continue

        card = parse_row(cells, indexed)
        if card:
            current["cards"].append({"q": card[0], "a": card[1]})

    return [g for g in groups if g["cards"]]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="report only; do not write")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if flashcards.json would change")
    args = ap.parse_args()

    decks_out: list[dict] = []
    total = 0
    for meta in DECKS:
        path = SOURCE_ROOT / meta["file"]
        if not path.exists():
            print(f"WARN  deck not found: {meta['file']}", file=sys.stderr)
            continue
        groups = parse_deck(path)
        count = sum(len(g["cards"]) for g in groups)
        total += count
        decks_out.append({
            "id": meta["id"],
            "title": meta["title"],
            "phase": meta["phase"],
            "card_count": count,
            "groups": groups,
        })
        print(f"  {meta['id']:10s} {count:4d} cards  ·  {len(groups)} groups")

    doc = {
        "$schema_version": 1,
        "total_cards": total,
        "decks": decks_out,
    }
    rendered = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"

    print(f"\ntotal cards: {total}")

    if args.check:
        existing = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if existing != rendered:
            print("drift detected — run `python scripts/build_flashcards.py`", file=sys.stderr)
            return 1
        print("up to date.")
        return 0

    if args.dry_run:
        print("[dry-run] no files written.")
        return 0

    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
