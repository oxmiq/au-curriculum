"""au-curriculum git-identity hook.

Exposes the local clone's fork owner + committer email to the header via
``config.extra.git_identity`` = ``{"user": <github-username>, "email": <email>}``.

The site is built locally in each student's fork/clone (``mkdocs serve``), so
this reads *their own* git identity at build time: the header can show
"<github-username> / <email>" with no sign-in and no network. The username is
the owner of the ``origin`` remote (i.e. the fork owner on GitHub); the email is
``git config user.email``. Everything degrades to empty strings if git / the
remote / the email is unavailable (e.g. a bare CI checkout), in which case the
header simply shows whatever is present (or nothing).

Registered in mkdocs.yml via ``hooks:`` alongside progress_badges.py.
"""
from __future__ import annotations

import re
import subprocess


def _git(*args: str) -> str:
    try:
        r = subprocess.run(["git", *args], capture_output=True, text=True, timeout=5)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def _owner_from_remote(url: str) -> str:
    """Owner = the path segment before the repo name, for any remote form:
    https://github.com/<owner>/<repo>(.git) · git@github.com:<owner>/<repo>(.git)
    · git@<ssh-alias>:<owner>/<repo>(.git).
    """
    m = re.search(r"[:/]([^/:]+)/[^/:]+?(?:\.git)?/?$", url or "")
    return m.group(1) if m else ""


def on_config(config, **_kwargs):  # type: ignore[no-untyped-def]
    email = _git("config", "user.email")
    # prefer the fork owner from origin; fall back to the configured name
    user = _owner_from_remote(_git("remote", "get-url", "origin")) or _git("config", "user.name")

    extra = config.setdefault("extra", {}) or {}
    extra["git_identity"] = {"user": user, "email": email}
    config["extra"] = extra
    return config
