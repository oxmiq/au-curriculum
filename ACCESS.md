# How to access the platform — OxBlood build

Three ways to view things, depending on what you need.

---

## A · The clickable demos — no setup, just double-click

Best for **sharing or a quick look**. Each is a single self-contained file with the
data **baked in** — no server, no internet, no install. They live in `scratch/`.

1. **`scratch/curriculum-map-demo.html`** — double-click → opens in your browser.
   - Toggle **Tree | Graph** at the top to switch views.
   - Click a week to expand its sessions.
   - Deep-link straight to the graph with `curriculum-map-demo.html?view=graph`.

> The instructor **cohort-dashboard-demo.html** now lives in the separate **`au-cohort-tracker`** repo (see **C**).

> ⚠️ Demos are a **frozen snapshot** — they don't change as progress is recorded.
> For live, updating progress use the served site (**B**).

---

## B · The full live site — `mkdocs serve` (the real platform)

**Prereq:** Python 3.

1. Open Terminal and `cd` into the repo (escape the spaces, or drag the folder in):
   ```
   cd ".../graph2.0 downloads/au-curriculum"
   ```
2. **First time only** — create a virtual env and install MkDocs:
   ```
   python3 -m venv .venv
   source .venv/bin/activate
   pip install mkdocs mkdocs-material
   ```
3. Serve it:
   ```
   mkdocs serve
   ```
   Open **http://127.0.0.1:8000**. The **Curriculum Map**, **Dependency Graph**, and **My Progress** (timeline) are in the left nav.

> 🔁 **After re-extracting an updated zip:** restart the server (Ctrl-C, then `mkdocs serve`).
> Edits inside `docs/` hot-reload automatically, but `mkdocs.yml` and new fonts only load on a restart.

---

## C · The instructor cohort dashboard — its own repo (`au-cohort-tracker`)

The instructor tooling is **not in this repo** — it's a separate (private) repo, so it never
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

## How progress drives the map (the git-as-database loop)

1. Edit a module record: `docs/progress/week-xx/module-y.json` → set `"status"` to `passed` / `in_progress`.
2. Regenerate the summary:
   ```
   python3 skills/progress-recorder/build_summary.py
   ```
   (rewrites `docs/progress/summary.json`)
3. The served map reorganizes — `%` updates, the next module unlocks, the **NEXT** highlight moves.

In production the **course agent** performs step 1–2 automatically as students pass knowledge checks.
