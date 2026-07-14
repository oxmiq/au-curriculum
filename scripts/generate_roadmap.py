#!/usr/bin/env python3
"""Generate docs/roadmap.md (phase-banded sitemap) from docs/kb/graph.json.

The roadmap is the "front door" visualization: a three-level sitemap of
phase bands -> week cards -> per-day timeline. Structure, week titles, day
numbers and day titles all come from graph.json (the single source of truth);
phase grouping/labels/colours and the fixed page scaffolding (intro, overall
progress bar, status legend) live here as presentation config.

The day tiles carry ``data-module`` ids so ``docs/assets/roadmap-progress.js``
can overlay per-student progress at runtime (passed/in-progress, week + overall
bars, "next up"). Styling: ``.ox-roadmap`` / ``.ox-rmap-*`` in cards.css.

Run after editing graph.json to keep the roadmap in sync:

    python scripts/generate_roadmap.py            # rewrite docs/roadmap.md
    python scripts/generate_roadmap.py --check     # exit 1 if it would change
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRAPH = REPO / "docs" / "kb" / "graph.json"
OUT = REPO / "docs" / "roadmap.md"

# Phase display labels (override graph.json titles where the roadmap uses a
# shorter band name, e.g. the week-6 "Prompt Engineering + AI Agents" phase
# reads as just "AI Agents" on the band).
PHASE_LABELS = {
    "orientation": "Orientation",
    "inference":   "Inference Engineering",
    "agents":      "AI Agents",
    "bridge":      "Bridge",
    "capsule":     "Capsule Hands-On",
    "capstone":    "Capstone",
}

# Per-phase palette (design tokens; mirror the light/cream brand in cards.css).
# fill = header tint, line = accent/border, ink = heading + label text.
PHASE_COLORS = {
    "orientation": ("#EDF0F4", "#5A6577", "#26303F"),
    "inference":   ("#E4F3F5", "#0E7C8A", "#06363D"),
    "agents":      ("#F7EFDD", "#B8761E", "#4A3208"),
    "bridge":      ("#E9ECF7", "#5B6BA8", "#232C4D"),
    "capsule":     ("#E3F2E7", "#2E7D32", "#123D18"),
    "capstone":    ("#F8E5E9", "#C43E54", "#4A1420"),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def weeks_range(nums: list[int]) -> str:
    if len(nums) == 1:
        return f"Week {nums[0]}"
    return f"Weeks {nums[0]}–{nums[-1]}"   # en-dash range


def build() -> str:
    g = json.loads(GRAPH.read_text(encoding="utf-8"))
    weeks = g["weeks"]

    lines: list[str] = []
    a = lines.append

    # ---- header + intro ----
    a("# Roadmap")
    a("")
    a("The full 50-day path through the curriculum, grouped by phase and then "
      "by week. Each tile is a session; click to open the lesson. The last tile "
      "in every week (before the capstone) is the Friday consolidation, shown "
      "as a dashed node.")
    a("")
    a("If you want the narrative version with rationale, see "
      "[Curriculum](curriculum.md) and [Why this curriculum](rationale.md). To "
      "explore cross-phase prerequisites, how a later session builds on earlier "
      "ones outside its week, see the [Interactive Graph](kb/interactive-graph.md).")
    a("")

    # ---- overall progress bar (populated at runtime; hidden until data loads) ----
    a('<div class="ox-rmap-overall" hidden>')
    a('  <div class="ox-rmap-overall__pct">0%</div>')
    a('  <div class="ox-rmap-overall__meta">')
    a('    <span class="ox-rmap-overall__label">Overall progress · '
      '<span data-done>0</span>/<span data-total>50</span> sessions cleared</span>')
    a('    <span class="ox-rmap-track"><i></i></span>')
    a('  </div>')
    a('</div>')
    a("")

    # ---- status legend ----
    a('<div class="ox-rmap-legend" hidden>')
    a('  <span><i style="background:var(--ox-green)"></i>Passed</span>')
    a('  <span><i style="background:var(--ox-gold)"></i>In progress</span>')
    a('  <span><i style="background:var(--ox-surface);border-color:var(--ox-line-strong)"></i>Not started</span>')
    a('  <span><i style="background:var(--ox-surface);box-shadow:0 0 0 2px color-mix(in srgb,var(--ox-blood) 35%,transparent)"></i>Next up</span>')
    a('</div>')
    a("")

    # ---- sitemap: phase bands -> week cards -> day tiles ----
    a('<div class="ox-roadmap" markdown="0">')

    # group weeks into contiguous phase bands, preserving order
    bands: list[tuple[str, list[dict]]] = []
    for w in weeks:
        if bands and bands[-1][0] == w["phase"]:
            bands[-1][1].append(w)
        else:
            bands.append((w["phase"], [w]))

    day_counter = 0
    for phase, members in bands:
        fill, line, ink = PHASE_COLORS[phase]
        label = PHASE_LABELS.get(phase, phase)
        nums = [w["number"] for w in members]
        a(f'  <section class="ox-rmap-phase" style="--phase-fill:{fill};--phase-line:{line};--phase-ink:{ink}">')
        a('    <header class="ox-rmap-phase__head">')
        a('      <span class="ox-rmap-phase__swatch" aria-hidden="true"></span>')
        a(f'      <h2 class="ox-rmap-phase__name">{esc(label)}</h2>')
        a(f'      <span class="ox-rmap-phase__weeks">{weeks_range(nums)}</span>')
        a('    </header>')
        a(f'    <div class="ox-rmap-weeks" style="--cols:{len(members)}">')
        for w in members:
            a('      <section class="ox-rmap-week">')
            a('        <header class="ox-rmap-week__head">')
            a(f'          <span class="ox-rmap-week__num">Week {w["number"]:02d}</span>')
            a(f'          <h3 class="ox-rmap-week__title">{esc(w["title"])}</h3>')
            a('          <div class="ox-rmap-week__prog" hidden>')
            a('            <span class="ox-rmap-track"><i></i></span>')
            a('            <span class="ox-rmap-week__pct"></span>')
            a('          </div>')
            a('        </header>')
            a('        <ol class="ox-rmap-days">')
            for m in w["modules"]:
                day_counter += 1
                mid = m["id"]
                cls = "ox-rmap-day"
                if "Consolidation" in m["title"]:
                    cls += " is-consolidation"
                a(f'          <li><a class="{cls}" href="../lessons/{mid}/" '
                  f'data-module="{mid}"><span class="ox-rmap-day__n">{m["day"]:02d}</span>'
                  f'<span class="ox-rmap-day__t">{esc(m["title"])}</span></a></li>')
            a('        </ol>')
            a('      </section>')
        a('    </div>')
        a('  </section>')
    a('</div>')
    a("")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if docs/roadmap.md is out of sync with graph.json")
    args = ap.parse_args()

    new = build()
    current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    # compare ignoring line-ending differences
    if current.replace("\r\n", "\n") == new:
        if not args.check:
            print(f"{OUT.relative_to(REPO)} already up to date")
        return 0
    if args.check:
        print(f"drift: {OUT.relative_to(REPO)} differs from graph.json "
              f"— run `python scripts/generate_roadmap.py`", file=sys.stderr)
        return 1
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        f.write(new)
    print(f"wrote {OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
