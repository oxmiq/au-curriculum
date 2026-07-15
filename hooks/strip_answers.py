"""au-curriculum answer-secrecy hook (task 5b, Phase A).

Strips the ``answer`` (correct option index) and ``explain`` fields out of every
*server-persisted* ``ox-self-check`` pool at build time, so the **published site**
never ships the answer key. The authored markdown on disk is untouched — this
only rewrites the in-memory page content MkDocs renders.

Server-persisted checks are those whose ``data-id`` ends in ``-readiness``,
``-wrapup`` or ``-canonical`` — exactly the ids for which ``self-check.js`` grades
via the ``grade-readiness`` Edge Function and reveals feedback from the server
response. Formative checks with any other id keep their local answers (they are
graded client-side and never leave the browser).

Note (defense-in-depth): once Phase B lands, the lesson *source* no longer
contains answers for server checks, so this hook usually finds nothing to strip.
It stays as a safety net: if an author reintroduces an ``answer``/``explain`` into
a server pool, the published site still won't leak it. The companion
``scripts/check_no_embedded_answers.py`` fails CI so the source gets fixed too.

Registered in mkdocs.yml via ``hooks:`` alongside git_identity.py.
"""
from __future__ import annotations

import json
import re

# Capture: (div open tag)(script open tag)(JSON body)(script close). The div tag
# carries data-id; the script body is the authored pool JSON.
_POOL_RE = re.compile(
    r'(<div\s+class="ox-self-check"[^>]*>)\s*'
    r'(<script[^>]*class="ox-self-check__pool"[^>]*>)'
    r'(.*?)'
    r'(</script>)',
    re.S,
)
_ID_RE = re.compile(r'data-id="([^"]+)"')
# Must match self-check.js `serverEnabled()` exactly.
_SERVER_ID_RE = re.compile(r'-(readiness|wrapup|canonical)$')


def _strip_pool(json_text: str) -> str | None:
    """Return the pool JSON with answer/explain removed, or None if unchanged
    (or unparseable — leave the original untouched in that case)."""
    try:
        pool = json.loads(json_text.strip())
    except json.JSONDecodeError:
        return None
    if not isinstance(pool, list):
        return None
    changed = False
    for q in pool:
        if isinstance(q, dict):
            if q.pop("answer", None) is not None:
                changed = True
            if q.pop("explain", None) is not None:
                changed = True
    if not changed:
        return None
    # Compact, valid JSON; keep non-ASCII (×, —, …) intact for the browser parser.
    return json.dumps(pool, ensure_ascii=False, separators=(",", ":"))


def on_page_markdown(markdown, **_kwargs):  # type: ignore[no-untyped-def]
    def repl(m: "re.Match[str]") -> str:
        div_open, script_open, body, script_close = m.group(1), m.group(2), m.group(3), m.group(4)
        did = _ID_RE.search(div_open)
        if not did or not _SERVER_ID_RE.search(did.group(1)):
            return m.group(0)  # not server-persisted → leave answers in place
        stripped = _strip_pool(body)
        if stripped is None:
            return m.group(0)
        return f"{div_open}\n{script_open}{stripped}{script_close}"

    if "ox-self-check__pool" not in markdown:
        return markdown
    return _POOL_RE.sub(repl, markdown)
