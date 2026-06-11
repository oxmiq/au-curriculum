#!/usr/bin/env python3
"""Build docs/kb/glossary.json from the source-material glossary files.

The glossary is a separate surface from the interactive concept graph:
- The graph (kb/interactive-graph.html) shows the curated CONCEPTUAL map:
  ~98 ideas with hand-authored prereq edges. Dense, structured, navigable.
- The glossary (kb/glossary.html) is the alphabetical DICTIONARY: every term
  defined in any source-material glossary, sorted A-Z, with cross-links
  inferred from definition text.

This script reads the 5 source-material glossary files, normalises each term
to a kebab-case id, extracts the first paragraph as the definition, infers
"see also" cross-links by detecting other glossary terms mentioned in the
definition body, and writes a single glossary.json the page renders from.

It does NOT touch concepts.json. Glossary terms and curated concepts are
kept deliberately separate.

Usage:
    python3 scripts/build_glossary.py            # write glossary.json
    python3 scripts/build_glossary.py --dry-run  # report only

Idempotent. Run any time glossary source files change.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GLOSSARY_OUT = REPO / "docs" / "kb" / "glossary.json"
CONCEPTS = REPO / "docs" / "kb" / "concepts.json"
SOURCE_ROOT = REPO / "planning" / "source-material"

# Glossary file -> phase id. Each glossary's terms inherit that phase.
GLOSSARIES = {
    "Inference Engineering/Inference_Engineering_Glossary.md": "inference",
    "Prompt Engineering/Prompt-Engineering-Glossary.md":        "prompting",
    "AI Agents/AI Agents - Glossary.md":                        "agents",
    "Capsule Power User/Capsule-Power-User-Glossary.md":        "capsule",
    "Capsule Power User/Capsule-Power-User-Flashcards.md":      "capsule",
}

PHASE_TITLES = {
    "foundations": "Foundations",
    "inference":   "Inference",
    "prompting":   "Prompting",
    "agents":      "Agents",
    "capsule":     "Capsule",
    "capstone":    "Capstone",
}

# Two header styles seen across glossaries: `### Term` and `**Term**`.
H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
BOLD_RE = re.compile(r"^\*\*([^*\n]+)\*\*\s*$", re.MULTILINE)

# Headers/junk that should not become terms.
APPENDIX_RE = re.compile(r"^[A-Z]\.\d+\s*[—–-]")  # "B.10 — FlashAttention"
ALL_CAPS_LETTER_RE = re.compile(r"^[A-Z]\s*$")    # alphabet markers "A", "B", ...
COMPOUND_HINTS = (",", " vs.", " vs ", " / ")

# Words too generic to use as cross-link triggers, even though they are
# legitimate glossary entries on their own. Allowed as TERMS, blocked as
# substring triggers in other terms' definitions.
LINK_TRIGGER_BLOCKLIST = {
    "agent", "agents", "model", "models", "data", "react",
    "token", "tokens", "attention", "inference", "tool", "tools",
    "task", "tasks", "user", "system", "role", "chat", "memory",
    "context", "prompt", "prompts", "loop", "decode", "prefill",
    "batch", "completion", "delimiter", "eval", "evals",
    "session", "environment", "stream", "streaming", "node", "nodes",
    "card", "cards", "vendor", "name", "see", "also", "field",
}


def slugify(term: str) -> str:
    """kebab-case id. Strips trailing parenthetical, lowercases."""
    term = re.sub(r"\s*\([^)]*\)\s*$", "", term)
    term = term.strip("`* \t")
    term = term.replace("\u2013", "-").replace("\u2014", "-")
    s = re.sub(r"[^a-z0-9]+", "-", term.lower()).strip("-")
    return s


def is_junk_term(term: str, slug: str) -> tuple[bool, str]:
    if not slug or len(slug) < 2:
        return True, "too short"
    if APPENDIX_RE.match(term.strip()):
        return True, "appendix header"
    if ALL_CAPS_LETTER_RE.match(term.strip()):
        return True, "section letter"
    if term.startswith(("--", "-")):
        return True, "CLI flag"
    if term.startswith("`") and term.endswith("`"):
        inner = term.strip("`")
        if "/" in inner or inner.startswith("-") or " " in inner.strip():
            return True, "command literal"
    if "/" in term and not term[0].isalpha():
        return True, "looks like a path"
    if any(h in term for h in COMPOUND_HINTS):
        return True, "compound multi-concept title"
    if slug.isdigit():
        return True, "numeric"
    if slug.startswith(("b-", "a-", "c-")) and len(slug) > 3 and slug[2].isdigit():
        return True, "appendix-like slug"
    return False, ""


def parse_glossary(path: Path) -> list[tuple[str, str]]:
    """Return [(term, first-paragraph-definition), ...] in source order.

    Handles both `### Term` and `**Term**` heading styles. Strips a leading
    `**Field:** ...` line if present (used in some glossaries).
    """
    text = path.read_text(encoding="utf-8")
    matches: list[tuple[int, str]] = []
    for m in H3_RE.finditer(text):
        matches.append((m.start(), m.group(1).strip()))
    for m in BOLD_RE.finditer(text):
        matches.append((m.start(), m.group(1).strip()))
    matches.sort()
    out: list[tuple[str, str]] = []
    for i, (start, term) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        body = text[start:end]
        body = re.sub(r"^.*?\n", "", body, count=1)
        body = re.sub(r"^\*\*Field:\*\*\s*", "", body.strip(), count=1)
        para = re.split(r"\n\s*\n", body.strip(), maxsplit=1)[0]
        para = re.sub(r"\s+", " ", para).strip()
        if not para:
            continue
        out.append((term, para))
    return out


def build_cross_link_triggers(terms_by_slug: dict) -> list[tuple[re.Pattern, str]]:
    """Build a list of (compiled-regex, target-slug) used to detect mentions
    of glossary terms inside other glossary definitions.

    Conservative: only multi-word titles or titles ≥ 9 chars qualify as
    triggers, and the blocklist suppresses generic words.
    """
    triggers: list[tuple[re.Pattern, str]] = []
    for slug, entry in terms_by_slug.items():
        title = entry["term"]
        title_low = title.lower()
        if title_low in LINK_TRIGGER_BLOCKLIST:
            continue
        if " " in title or len(title) >= 9:
            triggers.append(
                (re.compile(r"\b" + re.escape(title) + r"\b", re.IGNORECASE), slug)
            )
        id_spaced = slug.replace("-", " ")
        if " " in id_spaced and id_spaced not in LINK_TRIGGER_BLOCKLIST and len(id_spaced) >= 6:
            triggers.append(
                (re.compile(r"\b" + re.escape(id_spaced) + r"\b", re.IGNORECASE), slug)
            )
    return triggers


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="report only; do not write")
    args = ap.parse_args()

    # terms_by_slug: slug -> { term, slug, phase, definition, sources: [...] }
    terms_by_slug: dict[str, dict] = {}
    duplicates: list[tuple[str, str, str]] = []  # (slug, existing source, new source)
    skipped: list[tuple[str, str, str]] = []      # (term, reason, source)

    for rel_path, phase in GLOSSARIES.items():
        path = SOURCE_ROOT / rel_path
        if not path.exists():
            print(f"WARN  glossary not found: {rel_path}", file=sys.stderr)
            continue
        for term, definition in parse_glossary(path):
            slug = slugify(term)
            skip, reason = is_junk_term(term, slug)
            if skip:
                skipped.append((term, reason, rel_path))
                continue
            if slug in terms_by_slug:
                existing = terms_by_slug[slug]
                if rel_path not in existing["sources"]:
                    existing["sources"].append(rel_path)
                # If the new definition is much longer, prefer it.
                if len(definition) > len(existing["definition"]) * 1.4:
                    existing["definition"] = definition
                duplicates.append((slug, existing["sources"][0], rel_path))
            else:
                terms_by_slug[slug] = {
                    "slug": slug,
                    "term": term,
                    "phase": phase,
                    "definition": definition,
                    "sources": [rel_path],
                    "see_also": [],         # filled by cross-link pass
                    "concept_link": None,   # filled if a curated concept shares the slug
                }

    # Mark glossary terms whose slug matches a curated concept id, so the
    # page can offer a "see in concept graph" deep-link.
    if CONCEPTS.exists():
        try:
            curated = json.loads(CONCEPTS.read_text(encoding="utf-8"))
            curated_ids = {c["id"] for c in curated.get("concepts", [])}
            for slug, entry in terms_by_slug.items():
                if slug in curated_ids:
                    entry["concept_link"] = slug
        except Exception as e:
            print(f"WARN  could not parse concepts.json: {e}", file=sys.stderr)

    # Cross-link inference: for each definition, detect mentions of other
    # glossary terms and record them under `see_also`.
    triggers = build_cross_link_triggers(terms_by_slug)
    total_links = 0
    for slug, entry in terms_by_slug.items():
        hits: set[str] = set()
        text = entry["definition"]
        for pattern, target in triggers:
            if target == slug:
                continue
            if pattern.search(text):
                hits.add(target)
        if hits:
            entry["see_also"] = sorted(hits)
            total_links += len(hits)

    # Build the output document.
    terms_sorted = sorted(terms_by_slug.values(), key=lambda x: x["term"].lower())
    phases = sorted({e["phase"] for e in terms_sorted})

    doc = {
        "$schema_version": 1,
        "phases": [{"id": p, "title": PHASE_TITLES.get(p, p)} for p in phases],
        "terms": terms_sorted,
    }

    # --- Report ---
    per_phase = defaultdict(int)
    for e in terms_sorted:
        per_phase[e["phase"]] += 1
    print(f"glossary terms: {len(terms_sorted)}")
    for ph, n in sorted(per_phase.items()):
        print(f"  {ph:12s} {n}")
    print()
    print(f"cross-links inferred (see-also entries): {total_links}")
    linked_to_concepts = sum(1 for e in terms_sorted if e["concept_link"])
    print(f"terms that also appear as curated concepts: {linked_to_concepts}")
    print()
    skipped_counts = defaultdict(int)
    for _, r, _ in skipped:
        skipped_counts[r] += 1
    print(f"terms skipped by junk filter: {len(skipped)}")
    for r, n in sorted(skipped_counts.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {r}")

    if args.dry_run:
        print("\n[dry-run] no files written.")
        return 0

    GLOSSARY_OUT.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {GLOSSARY_OUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
