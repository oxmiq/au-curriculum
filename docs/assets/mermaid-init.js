// Loads Mermaid from the official CDN and initialises any <pre class="mermaid">
// blocks emitted by pymdownx.superfences. Pinned to a stable major to avoid
// breaking when upstream cuts a new release.
//
// If the CDN is blocked, the page degrades to plain text inside the <pre>;
// the rest of the page remains usable.

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
    "  securityLevel: 'loose'",  // needed for click handlers to navigate
    "});"
  ].join('\n');
  document.head.appendChild(s);
})();
