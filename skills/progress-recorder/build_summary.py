#!/usr/bin/env python3
"""Regenerate docs/progress/summary.json from the per-module progress records.

Source of truth  = one JSON per module at docs/progress/week-xx/module-y.json (§8).
Derived output   = docs/progress/summary.json — the single small file the graph
                   page and progress view read, so the renderer never crawls
                   every per-module file.

This is what oxtutor runs (via record_progress) after recording a result.
Totals come from kb/graph.json (the authoritative module list), so a week shows
the right denominator even before every module has a record. "Completed" = passed.

Run from anywhere:  python3 skills/progress-recorder/build_summary.py
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]          # skills/progress-recorder/ -> repo root
GRAPH = ROOT / "docs" / "kb" / "graph.json"
PROGRESS_DIR = ROOT / "docs" / "progress"
OUT = PROGRESS_DIR / "summary.json"


def main() -> None:
    if not GRAPH.exists():
        sys.exit(f"graph.json not found at {GRAPH}")
    graph = json.loads(GRAPH.read_text())

    # week id -> ordered list of its module ids (the authoritative denominator)
    week_modules = {w["id"]: [m["id"] for m in w["modules"]] for w in graph["weeks"]}

    # load every per-module record (week-*/module-*.json); summary.json sits at the
    # progress/ root so this glob never picks it up
    records: dict[str, dict] = {}
    for f in sorted(PROGRESS_DIR.glob("week-*/*.json")):
        try:
            rec = json.loads(f.read_text())
        except json.JSONDecodeError as e:
            print(f"  skip {f.name}: invalid JSON ({e})", file=sys.stderr)
            continue
        mid = rec.get("module")
        if not mid:
            print(f"  skip {f}: missing 'module' field", file=sys.stderr)
            continue
        entry = {"status": rec.get("status", "not_started")}
        if "canonical_knowledge_check" in rec:
            entry["canonical_knowledge_check"] = rec["canonical_knowledge_check"]
        records[mid] = entry

    # weekly + overall rollups
    weeks: dict[str, dict] = {}
    all_total = all_done = 0
    for wid, mids in week_modules.items():
        total = len(mids)
        done = sum(1 for mid in mids if records.get(mid, {}).get("status") == "passed")
        weeks[wid] = {
            "completed": done,
            "total": total,
            "percent": round(100 * done / total) if total else 0,
        }
        all_total += total
        all_done += done

    summary = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_note": "Derived by build_summary.py from per-module progress/*.json — do not hand-edit.",
        "modules": records,
        "weeks": weeks,
        "overall": {
            "completed": all_done,
            "total": all_total,
            "percent": round(100 * all_done / all_total) if all_total else 0,
        },
    }
    OUT.write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"wrote {OUT.relative_to(ROOT)} — overall {summary['overall']['percent']}% "
        f"({all_done}/{all_total} modules passed) from {len(records)} records"
    )


if __name__ == "__main__":
    main()
