# How to access the platform - OxBlood build

How to view the material, depending on what you need.

---

## A · Quick look

There's no separate no-server demo in the student fork anymore. The standalone
`curriculum-map-demo.html` was retired when the Tree / Graph / Timeline views were
folded into the **Roadmap** and the **Interactive Concept Graph**. For a quick look,
run the live site (**B**): it's a two-command setup.

> The instructor **cohort-dashboard-demo.html** lives in the separate **`au-cohort-tracker`** repo (see **C**).

---

## B · The full live site - `mkdocs serve` (the real platform)

**Prereq:** Python 3.

1. Open Terminal and `cd` into the repo (escape the spaces, or drag the folder in):
   ```
   cd ".../graph2.0 downloads/au-curriculum"
   ```
2. **First time only** - create a virtual env and install MkDocs:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install mkdocs mkdocs-material
   ```
3. Serve it:
   ```
   mkdocs serve
   ```
   Open **http://127.0.0.1:8000**. The **Roadmap** (with live progress), the **Interactive Concept Graph**, the **Glossary**, and **Concepts** are in the top nav (Plan / Reference tabs).

> 🔁 **After re-extracting an updated zip:** restart the server (Ctrl-C, then `mkdocs serve`).
> Edits inside `docs/` hot-reload automatically, but `mkdocs.yml` and new fonts only load on a restart.

---

## C · The instructor cohort dashboard - its own repo (`au-cohort-tracker`)

The instructor tooling is **not in this repo**; it's a separate (private) repo, so it never
ships inside a student fork. From inside `au-cohort-tracker`:

1. Regenerate the cohort roll-up from the mock forks:
   ```
   python3 build_cohort.py --local mock-forks
   ```
2. Serve the repo root and open the dashboard:
   ```
   python3 -m http.server 8077
   ```
   → **http://localhost:8077/dashboard.html**

> Or just double-click `cohort-dashboard-demo.html` in that repo for a baked, no-server snapshot.

---

## How progress drives the roadmap (the git-as-database loop)

1. Edit a module record: `docs/progress/week-xx/module-y.json` → set `"status"` to `passed` / `in_progress`.
2. Regenerate the summary:
   ```
   python3 skills/progress-recorder/build_summary.py
   ```
   (rewrites `docs/progress/summary.json`)
3. The **Roadmap** reflects it: the overall and per-week progress bars fill, day tiles switch to passed / in-progress, and the **NEXT** flag moves to the next available session.

In production the **course agent** performs steps 1-2 automatically as students pass knowledge checks.
