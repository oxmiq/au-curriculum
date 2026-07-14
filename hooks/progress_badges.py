"""au-curriculum progress hook.

Two responsibilities, both at build time:

1. Substitute ``{status:week-XX/module-Y}`` tokens that appear in any
   Markdown page with a styled HTML pill::

       <span class="status-pill status-passed">Passed</span>
       <span class="status-pill status-in-progress">In progress</span>
       <span class="status-pill status-not-started">Not started</span>

   State is read from ``docs/progress/summary.json`` (committed) and
   per-module records under ``docs/progress/<module_id>.json`` (per-student;
   may be absent on a fresh clone — that's the ``not-started`` case).

2. Expose the overall progress rollup to the Jinja header partial via
   ``config.extra.progress``. The custom header (``overrides/partials/header.html``)
   reads ``extra.progress.overall.{completed,total,percent}`` to render the
   status pill on every page without any client-side JS.

The hook is registered in ``mkdocs.yml`` via ``hooks:`` (MkDocs >= 1.4),
so no plugin package is required.

State legend (3-state, matches plan):
  passed       — module's ``status`` field in its per-module JSON == "passed"
  in-progress  — per-module JSON exists, status != "passed"
  not-started  — per-module JSON missing (or status == "not_started")
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

log = logging.getLogger("mkdocs.plugins.progress_badges")

# Tokens look like {status:week-02/module-3}. Matches verbatim in Markdown.
_TOKEN_RE = re.compile(r"\{status:(week-\d{2}/module-\d+)\}")

# Pretty labels for the 3 states.
_LABELS = {
    "passed":      "Passed",
    "in-progress": "In progress",
    "not-started": "Not started",
}


def _status_for_module(progress_dir: Path, module_id: str) -> str:
    """Resolve the 3-state status for ``week-XX/module-Y`` from per-module JSON.

    A missing per-module file is the common case on a fresh student clone;
    treat it as ``not-started`` rather than logging a warning.
    """
    per_module = progress_dir / f"{module_id}.json"
    if not per_module.is_file():
        return "not-started"
    try:
        data = json.loads(per_module.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log.warning("progress_badges: cannot read %s (%s) — treating as not-started",
                    per_module, exc)
        return "not-started"
    raw = (data.get("status") or "").strip().lower().replace("_", "-")
    if raw == "passed":
        return "passed"
    if raw in {"in-progress", "started"}:
        return "in-progress"
    # Any other value (incl. "not-started" or unset) => not started.
    return "not-started"


def _render_pill(state: str) -> str:
    label = _LABELS[state]
    return (
        f'<span class="status-pill status-{state}" '
        f'data-status="{state}" '
        f'title="{label}">{label}</span>'
    )


# ── MkDocs hook callbacks ──────────────────────────────────────────────────

def on_config(config, **_kwargs):  # type: ignore[no-untyped-def]
    """Read summary.json once per build and expose it via ``config.extra``.

    Also writes ``docs/assets/status.json`` so a future client-side enhancer
    (or external tooling) can fetch the same data without re-parsing.
    """
    docs_dir = Path(config["docs_dir"])
    summary_path = docs_dir / "progress" / "summary.json"

    summary: dict[str, Any]
    if summary_path.is_file():
        try:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            log.warning("progress_badges: cannot parse %s (%s)", summary_path, exc)
            summary = {}
    else:
        summary = {}

    # Defaults so the header template never blows up on missing keys.
    summary.setdefault("overall", {"completed": 0, "total": 50, "percent": 0})
    summary.setdefault("weeks", {})
    summary.setdefault("modules", {})

    extra = config.setdefault("extra", {}) or {}
    extra["progress"] = summary
    config["extra"] = extra

    # Mirror to docs/assets/status.json for any future client-side reader.
    # Guard: only write when content changes — avoids triggering mkdocs serve's
    # file-watcher (which watches docs/) and causing an infinite rebuild loop.
    assets_dir = docs_dir / "assets"
    try:
        assets_dir.mkdir(parents=True, exist_ok=True)
        new_content = json.dumps(summary, indent=2, sort_keys=True)
        status_path = assets_dir / "status.json"
        if not status_path.is_file() or status_path.read_text(encoding="utf-8") != new_content:
            status_path.write_text(new_content, encoding="utf-8")
    except OSError as exc:
        log.warning("progress_badges: cannot write status.json (%s)", exc)

    return config


def on_page_markdown(markdown: str, *, page, config, files, **_kwargs):  # type: ignore[no-untyped-def]
    """Replace ``{status:week-XX/module-Y}`` tokens with HTML pills."""
    if "{status:" not in markdown:
        return markdown

    progress_dir = Path(config["docs_dir"]) / "progress"

    def repl(match: re.Match[str]) -> str:
        module_id = match.group(1)
        state = _status_for_module(progress_dir, module_id)
        return _render_pill(state)

    return _TOKEN_RE.sub(repl, markdown)
