// Loads Mermaid from the official CDN and initialises any <pre class="mermaid">
// blocks emitted by pymdownx.superfences. Pinned to a stable major to avoid
// breaking when upstream cuts a new release.
//
// If the CDN is blocked, the page degrades to plain text inside the <pre>;
// the rest of the page remains usable.
//
// Theme: the site is a single cream + oxblood scheme (no dark mode), so we
// drive Mermaid with the `base` theme and OxBlood themeVariables rather than
// the stock 'default'/'dark' presets. This keeps diagram chrome (edges,
// clusters, titles, fonts) on-brand and — crucially — legible on the cream
// page. Per-node phase colours come from `classDef`s in the diagram source.
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
    "mermaid.initialize({",
    "  startOnLoad: true,",
    "  theme: 'base',",
    "  themeVariables: {",
    "    fontFamily: '\"Oxygen Mono\", \"Oxygen\", ui-monospace, monospace',",
    "    fontSize: '13px',",
    "    background: '#F5F0E4',",
    "    primaryColor: '#FFFFFF',",
    "    primaryBorderColor: '#8B0000',",
    "    primaryTextColor: '#1A1A1A',",
    "    secondaryColor: '#EDE8DC',",
    "    tertiaryColor: '#F5F0E4',",
    "    lineColor: '#A89E92',",
    "    textColor: '#1A1A1A',",
    "    mainBkg: '#FFFFFF',",
    "    nodeBorder: '#8B0000',",
    "    nodeTextColor: '#1A1A1A',",
    "    clusterBkg: '#EFEADD',",
    "    clusterBorder: '#D0C8BC',",
    "    titleColor: '#8B0000',",
    "    edgeLabelBackground: '#F5F0E4'",
    "  },",
    "  flowchart: { htmlLabels: true, useMaxWidth: true, padding: 10 },",
    "  securityLevel: 'antiscript'",  // strips <script> from labels; click directives still work
    "});"
  ].join('\n');
  document.head.appendChild(s);
})();
