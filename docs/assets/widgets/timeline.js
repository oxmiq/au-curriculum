/* ============================================================
   My Progress timeline widget — Material-wrapped version.
   Renders into .timeline-page #timeline-app on kb/timeline.md.

   URL math: the page is served at /au-curriculum/kb/timeline/
   (Material directory URLs), so:
     - graph.json     → ../graph.json
     - summary.json   → ../../progress/summary.json
     - lesson links   → ../../<m.lesson>
   ============================================================ */
(function () {
  'use strict';

  // Page guard — bail on any page that isn't kb/timeline.md
  if (!document.getElementById('timeline-app')) return;

  const GRAPH_URL   = '../graph.json';
  const SUMMARY_URL = '../../progress/summary.json';
  const LESSON_BASE = '../../';

  const PHASE_COLOR = {
    orientation: 'var(--p-orientation)',
    inference:   'var(--p-inference)',
    agents:      'var(--p-agents)',
    bridge:      'var(--p-bridge)',
    capsule:     'var(--p-capsule)',
    capstone:    'var(--p-capstone)',
  };

  const esc = (s) =>
    String(s).replace(/[&<>"]/g, (c) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
    }[c]));

  const lessonHref = (m) =>
    LESSON_BASE + String(m.lesson || '').replace(/index\.md$/, '');

  const statusOf = (s, id) =>
    (s.modules && s.modules[id] && s.modules[id].status) || 'not_started';

  async function load() {
    const app = document.getElementById('timeline-app');
    let graph;
    let summary;
    try {
      [graph, summary] = await Promise.all([
        fetch(GRAPH_URL).then((r) => {
          if (!r.ok) throw new Error(GRAPH_URL);
          return r.json();
        }),
        fetch(SUMMARY_URL)
          .then((r) => (r.ok ? r.json() : { modules: {}, weeks: {}, overall: {} }))
          .catch(() => ({ modules: {}, weeks: {}, overall: {} })),
      ]);
    } catch (e) {
      app.innerHTML =
        '<div class="err">Couldn\'t load <code>' +
        esc(e.message) +
        '</code>. Served by <code>mkdocs serve</code> — open over HTTP, not file://.</div>';
      return;
    }
    render(graph, summary);
  }

  function render(graph, summary) {
    const all = [];
    graph.weeks.forEach((w) =>
      w.modules.forEach((m) => all.push(Object.assign({}, m, { week: w })))
    );
    all.sort((a, b) => (a.day || 0) - (b.day || 0));

    const passed = (id) => statusOf(summary, id) === 'passed';
    const prereqsMet = (m) => (m.prereqs || []).every(passed);

    let next = null;
    for (const m of all) {
      if (statusOf(summary, m.id) !== 'passed' && prereqsMet(m)) {
        next = m;
        break;
      }
    }

    const o = summary.overall || {};
    const weeksDone = Object.values(summary.weeks || {}).filter(
      (w) => w.percent === 100
    ).length;
    const phaseTitle = {};
    (graph.phases || []).forEach((p) => {
      phaseTitle[p.id] = p.title;
    });

    const stats =
      '<div class="stats">' +
      '<div class="stat"><div class="n">' +
      (o.percent != null ? o.percent : 0) +
      '<small>%</small></div><div class="l">Overall</div></div>' +
      '<div class="stat"><div class="n">' +
      (o.completed != null ? o.completed : 0) +
      '<small> / ' +
      (o.total != null ? o.total : all.length) +
      '</small></div><div class="l">Sessions passed</div></div>' +
      '<div class="stat"><div class="n">' +
      weeksDone +
      '<small> / ' +
      graph.weeks.length +
      '</small></div><div class="l">Weeks complete</div></div>' +
      '<div class="stat now"><div class="n">' +
      (next
        ? '<span class="d">D' + next.day + '</span>' + esc(next.title)
        : '✓ all done') +
      '</div><div class="l">Up next</div></div>' +
      '</div>';

    const legend =
      '<div class="legend">' +
      '<span><i class="swatch" style="background:color-mix(in srgb,var(--t-next) 12%,var(--t-bg-sunk));border-color:var(--t-next)"></i>Next</span>' +
      '<span><i class="swatch" style="background:color-mix(in srgb,var(--t-ok) 16%,var(--t-bg-sunk));border-color:color-mix(in srgb,var(--t-ok) 45%,transparent)"></i>Passed</span>' +
      '<span><i class="swatch" style="background:color-mix(in srgb,var(--t-wip) 16%,var(--t-bg-sunk));border-color:color-mix(in srgb,var(--t-wip) 55%,transparent)"></i>In progress</span>' +
      '<span><i class="swatch" style="background:var(--t-bg-sunk)"></i>Available</span>' +
      '<span><i class="swatch" style="background:var(--t-bg-sunk);opacity:.45"></i>Locked</span>' +
      '</div>';

    const rows = graph.weeks
      .map((w) => {
        const color = PHASE_COLOR[w.phase] || 'var(--t-muted)';
        const pct =
          ((summary.weeks && summary.weeks[w.id]) || {}).percent || 0;
        const cells = w.modules
          .map((m) => {
            const st = statusOf(summary, m.id);
            const isNext = next && m.id === next.id;
            const locked =
              st === 'not_started' && !prereqsMet(m) && !isNext;
            let cls = 'cell';
            let g = '';
            if (st === 'passed') {
              cls += ' passed';
              g = '<span class="g">✓</span>';
            } else if (st === 'in_progress') {
              cls += ' wip';
              g = '<span class="g">◐</span>';
            } else if (isNext) {
              cls += ' next';
              g = '<span class="nextflag">next ▸</span>';
            } else if (locked) {
              cls += ' locked';
              g = '<span class="g" style="color:var(--t-faint)">•</span>';
            } else {
              g = '<span class="g" style="color:var(--t-faint)">○</span>';
            }
            const inner =
              '<div class="d">D' +
              (m.day != null ? m.day : '?') +
              '</div><div class="nm">' +
              esc(m.title) +
              '</div>' +
              g;
            return locked
              ? '<div class="' +
                  cls +
                  '" style="--phase:' +
                  color +
                  '" title="' +
                  esc(m.title) +
                  ' · locked">' +
                  inner +
                  '</div>'
              : '<a class="' +
                  cls +
                  '" style="--phase:' +
                  color +
                  '" href="' +
                  esc(lessonHref(m)) +
                  '" title="' +
                  esc(m.title) +
                  '">' +
                  inner +
                  '</a>';
          })
          .join('');
        return (
          '<div class="wk" style="--phase:' +
          color +
          '">' +
          '<div class="wk-meta">' +
          '<div class="num">WK ' +
          String(w.number).padStart(2, '0') +
          ' · ' +
          esc(phaseTitle[w.phase] || '') +
          '</div>' +
          '<div class="ttl">' +
          esc(w.title) +
          '</div>' +
          '<div class="mini"><i style="width:' +
          pct +
          '%"></i></div>' +
          '</div>' +
          '<div class="cells">' +
          cells +
          '</div>' +
          '</div>'
        );
      })
      .join('');

    document.getElementById('timeline-app').innerHTML =
      stats +
      legend +
      '<div class="timeline">' +
      rows +
      '</div>' +
      '<footer class="timeline-foot">your personal timeline · reads the same graph.json + summary.json as the map · cleared / current / locked derive from your progress</footer>';
  }

  load();
})();
