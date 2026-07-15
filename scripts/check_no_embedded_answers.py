#!/usr/bin/env python3
"""Guard: no answer key may be embedded in a server-persisted lesson pool.

Task 5b, Phase B invariant. Readiness / wrap-up / knowledge-check pools
(`data-id` ending -readiness/-wrapup/-canonical) are graded server-side by the
grade-readiness Edge Function; their answers live only in the PRIVATE
au-cohort-tracker repo. This repo is forked publicly, so a pool here must carry
ONLY `stem` + `options` — never `answer` or `explain`.

Exits non-zero (fails CI) if any server pool contains `answer` or `explain`.
Formative, client-graded pools (any other id) are allowed to keep their answers.

    python scripts/check_no_embedded_answers.py
"""
from __future__ import annotations
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

POOL_RE = re.compile(
    r'(<div\s+class="ox-self-check"[^>]*>)\s*'
    r'<script[^>]*class="ox-self-check__pool"[^>]*>(.*?)</script>',
    re.S,
)
ID_RE = re.compile(r'data-id="([^"]+)"')
SERVER_RE = re.compile(r"-(readiness|wrapup|canonical)$")


def main() -> int:
    sources = (glob.glob(os.path.join(ROOT, "docs/lessons/week-*/module-*/index.md"))
               + glob.glob(os.path.join(ROOT, "docs/lessons/week-*/module-*/knowledge-check.md")))
    offenders = []
    for f in sorted(sources):
        text = open(f, encoding="utf-8").read()
        for m in POOL_RE.finditer(text):
            did = ID_RE.search(m.group(1))
            if not did or not SERVER_RE.search(did.group(1)):
                continue
            try:
                pool = json.loads(m.group(2).strip())
            except json.JSONDecodeError:
                offenders.append((os.path.relpath(f, ROOT), did.group(1), "unparseable pool JSON"))
                continue
            leaks = sum(1 for q in pool if isinstance(q, dict) and ("answer" in q or "explain" in q))
            if leaks:
                offenders.append((os.path.relpath(f, ROOT), did.group(1), f"{leaks} question(s) embed answer/explain"))

    if offenders:
        print("!! embedded answers found in server-persisted pools "
              "(answers belong in the private au-cohort-tracker repo):", file=sys.stderr)
        for path, cid, why in offenders:
            print(f"   - {path}  [{cid}]  {why}", file=sys.stderr)
        return 1
    print("OK: no server-persisted pool embeds answer/explain")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
