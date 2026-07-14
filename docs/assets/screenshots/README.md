# Screenshots

README screenshots. Referenced from the root [`README.md`](../../../README.md#screenshots):

- `roadmap.png` - the progress-aware Roadmap sitemap (Plan tab)
- `lesson.png` - a lesson page with the header + body
- `knowledge-check.png` - a weekly canonical knowledge check
- `concept-graph.png` - the Interactive Concept Graph (Plan tab)
- `oxtutor.png` - an oxtutor terminal session (pending: needs an enrolled Capsule login)

Captured at 1440x950 @2x. To refresh: build the site (`mkdocs build -d _shot/au-curriculum`),
serve it (`cd _shot && python -m http.server 8123`), and re-shoot with Playwright against
`/au-curriculum/{roadmap/, lessons/week-03/module-2/, lessons/week-03/module-5/knowledge-check/,
kb/interactive-graph/}`.
