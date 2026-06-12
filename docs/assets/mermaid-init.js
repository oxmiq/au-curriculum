// Loads Mermaid from the official CDN and initialises any <pre class="mermaid">
// blocks emitted by pymdownx.superfences. Pinned to a stable major to avoid
// breaking when upstream cuts a new release.
//
// If the CDN is blocked, the page degrades to plain text inside the <pre>;
// the rest of the page remains usable.
//
// Security: `securityLevel: 'antiscript'` is the OWASP-aligned middle ground
// for our use case. It strips <script> tags from Mermaid node labels (closing
// the XSS vector flagged by Copilot review on PR #4) while still allowing the
// `click NODE "<href>"` directive used by docs/roadmap.md (20+ navigation
// handlers across the curriculum graph). Do NOT downgrade back to 'loose'
// without first removing every click handler in docs/**.

(function () {
  var s = document.createElement('script');
  s.type = 'module';
  s.textContent = [
    "import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.esm.min.mjs';",
    "const isDark = document.body && document.body.dataset && document.body.dataset.mdColorScheme === 'slate';",
    "mermaid.initialize({",
    "  startOnLoad: true,",
    "  theme: isDark ? 'dark' : 'default',",
    "  flowchart: { htmlLabels: true, useMaxWidth: true },",
    "  securityLevel: 'antiscript'",  // strips <script> from labels; click directives still work
    "});"
  ].join('\n');
  document.head.appendChild(s);
})();
