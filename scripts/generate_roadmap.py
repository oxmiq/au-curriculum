#!/usr/bin/env python3
"""Generate docs/roadmap.md (Mermaid flowchart) from docs/kb/graph.json.

The roadmap is the neetcode-style "front door" visualization: every day-module
shown as a clickable node, colour-coded by phase, week-by-week. Run after
editing graph.json to keep them in sync.

Usage:
    python3 scripts/generate_roadmap.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GRAPH = REPO / "docs" / "kb" / "graph.json"
OUT = REPO / "docs" / "roadmap.md"

PHASE_LABELS = {
    "orientation": "Orientation",
    "inference": "Inference Engineering",
    "prompting": "Prompt Engineering",
    "agents": "AI Agents",
    "capsule": "Capsule Hands-On",
    "capstone": "Capstone",
}

# Mermaid classDef colours (chosen to be legible in both light and dark themes
# under Material for MkDocs). Stroke is darker than fill so labels stay sharp.
PHASE_STYLE = {
    "orientation": "fill:#1f2937,stroke:#7c8aa0,color:#e7e9ee",
    "inference":   "fill:#0e2a32,stroke:#22d3ee,color:#e7f7fb",
    "prompting":   "fill:#2a1e3d,stroke:#a78bfa,color:#efeaff",
    "agents":      "fill:#3b2d10,stroke:#fbbf24,color:#fdf3d4",
    "capsule":     "fill:#0f2f25,stroke:#34d399,color:#dff9ee",
    "capstone":    "fill:#3a1320,stroke:#fb7185,color:#ffe2e8",
}


def node_id(module_id: str) -> str:
    """Mermaid node id: alnum only (e.g., 'week-02/module-3' -> 'W02M3')."""
    m = re.match(r"week-(\d{2})/module-(\d+)", module_id)
    if not m:
        return re.sub(r"[^A-Za-z0-9]", "", module_id)
    return f"W{m.group(1)}M{m.group(2)}"


def lesson_url(lesson_path: str) -> str:
    """Convert 'lessons/module-01/01-welcome-and-context.md' to a site URL
    relative to /roadmap/. mkdocs use_directory_urls=true strips .md and
    appends '/'. quiz.html is a static asset, leave it.
    """
    if lesson_path.endswith(".md"):
        return "../" + lesson_path[:-3] + "/"
    return "../" + lesson_path


def main() -> None:
    g = json.loads(GRAPH.read_text())
    weeks = g["weeks"]
    by_id = {m["id"]: m for w in weeks for m in w["modules"]}
    week_of = {m["id"]: w["number"] for w in weeks for m in w["modules"]}
    day_of = {m["id"]: m["day"] for w in weeks for m in w["modules"]}

    lines: list[str] = []
    lines.append("# Roadmap")
    lines.append("")
    lines.append(
        "The full 50-day path through the curriculum. Each box is a session — "
        "click to open the lesson. Colour marks the phase. Solid arrows are "
        "the day-to-day sequence; dotted arrows are cross-phase prereqs "
        "(a later session that builds on an earlier one outside the immediate "
        "week)."
    )
    lines.append("")
    lines.append(
        "If you want the narrative version with rationale, see "
        "[Curriculum](curriculum.md) and [Why this curriculum](rationale.md). "
        "For the interactive explorable graph, see "
        "[Interactive Graph](kb/interactive-graph.html)."
    )
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    # Subgraph per week
    for w in weeks:
        title = f"Week {w['number']:02d} · {w['title']}"
        lines.append(f'  subgraph W{w["number"]:02d}["{title}"]')
        lines.append("    direction TB")
        prev_nid = None
        for m in w["modules"]:
            nid = node_id(m["id"])
            label = f"Day {m['day']:02d} · {m['title']}"
            # Mermaid: escape pipes/quotes by wrapping label in quotes
            label_safe = label.replace('"', "'")
            lines.append(f'    {nid}["{label_safe}"]')
            if prev_nid is not None:
                lines.append(f"    {prev_nid} --> {nid}")
            prev_nid = nid
        lines.append("  end")
    # Connect week last-day → next week first-day
    for w_prev, w_next in zip(weeks, weeks[1:]):
        last = node_id(w_prev["modules"][-1]["id"])
        first = node_id(w_next["modules"][0]["id"])
        lines.append(f"  {last} --> {first}")
    # Cross-phase / non-linear prereq edges (dotted)
    lines.append("  %% cross-phase shortcuts")
    for w in weeks:
        for m in w["modules"]:
            for p in m["prereqs"]:
                # Skip the trivial day-N → day-N+1 edge (already drawn by chain)
                if day_of[p] == m["day"] - 1:
                    continue
                src = node_id(p)
                dst = node_id(m["id"])
                lines.append(f"  {src} -.-> {dst}")
    # classDef per phase + assignment
    lines.append("")
    for phase_id, style in PHASE_STYLE.items():
        lines.append(f"  classDef {phase_id} {style};")
    for phase_id in PHASE_STYLE:
        members = [
            node_id(m["id"])
            for w in weeks
            for m in w["modules"]
            if w["phase"] == phase_id
        ]
        if members:
            lines.append(f"  class {','.join(members)} {phase_id};")
    # Click handlers
    lines.append("")
    for w in weeks:
        for m in w["modules"]:
            url = lesson_url(m["lesson"])
            tooltip = m["title"].replace('"', "'")
            lines.append(f'  click {node_id(m["id"])} "{url}" "{tooltip}"')
    lines.append("```")
    lines.append("")
    lines.append("## Legend")
    lines.append("")
    lines.append("| Colour | Phase | Weeks |")
    lines.append("|--------|-------|-------|")
    for p in g["phases"]:
        weeks_str = ", ".join(str(w) for w in p["weeks"])
        label = PHASE_LABELS.get(p["id"], p["title"])
        lines.append(f"| ▣ | {label} | Week {weeks_str} |")
    lines.append("")
    lines.append(
        "Day 05 of weeks 1–9 is the Friday quiz "
        "(`quiz.html` in each module folder). Day 50 closes the program."
    )
    lines.append("")

    OUT.write_text("\n".join(lines))
    print(f"wrote {OUT.relative_to(REPO)} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
