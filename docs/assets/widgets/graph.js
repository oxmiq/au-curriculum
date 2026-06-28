/* ============================================================
   Curriculum Map (tree) widget — Material-wrapped version.
   Mounts into .graph-page #graph-app on kb/graph.md.

   URL math: the page is served at /au-curriculum/kb/graph/, so:
     - graph.json   → ../graph.json
     - summary.json → ../../progress/summary.json
     - lessons/...  → ../../<m.lesson>
   ============================================================ */
(function () {
  'use strict';

  if (!document.getElementById('graph-app')) return;

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

  const statusOf = (summary, id) =>
    (summary.modules && summary.modules[id] && summary.modules[id].status) ||
    'not_started';

  async function load() {
    const app = document.getElementById('graph-app');
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
    const app = document.getElementById('graph-app');

    const all = [];
    graph.weeks.forEach((w) =>
      w.modules.forEach((m) => all.push(Object.assign({}, m, { week: w })))
    );
    all.sort((a, b) => (a.day || 0) - (b.day || 0));

    const passed = (id) => statusOf(summary, id) === 'passed';
    const prereqsMet = (m) => (m.prereqs || []).every(passed);
    let nextId = null;
    for (const m of all) {
      if (statusOf(summary, m.id) !== 'passed' && prereqsMet(m)) {
        nextId = m.id;
        break;
      }
    }

    const overall = summary.overall || {};
    const phaseTitle = {};
    (graph.phases || []).forEach((p) => {
      phaseTitle[p.id] = p.title;
    });

    let html =
      '<div class="overall">' +
      '<div class="pct">' +
      (overall.percent != null ? overall.percent + '%' : '—') +
      '</div>' +
      '<div class="bar-wrap">' +
      '<div class="label">overall progress · ' +
      (overall.completed != null ? overall.completed : 0) +
      '/' +
      (overall.total != null ? overall.total : all.length) +
      ' complete</div>' +
      '<div class="track"><div class="fill" style="width:' +
      (overall.percent || 0) +
      '%;background:var(--p-inference)"></div></div>' +
      '</div></div>' +
      '<div class="legend">' +
      (graph.phases || [])
        .map(
          (p) =>
            '<span><i class="dot" style="background:' +
            (PHASE_COLOR[p.id] || 'var(--g-muted)') +
            '"></i>' +
            esc(p.title) +
            '</span>'
        )
        .join('') +
      '<span><i class="dot" style="background:var(--g-ok)"></i>Passed</span>' +
      '<span><i class="dot" style="background:var(--g-wip)"></i>In progress</span>' +
      '</div>' +
      '<main>';

    graph.weeks.forEach((w, i) => {
      const color = PHASE_COLOR[w.phase] || 'var(--g-muted)';
      const wp = (summary.weeks && summary.weeks[w.id]) || {};
      const pct = wp.percent || 0;
      const open = pct > 0 && pct < 100 ? 'open' : '';

      const mods = w.modules
        .map((m) => {
          const st = statusOf(summary, m.id);
          const isNext = m.id === nextId;
          const locked =
            st === 'not_started' && !prereqsMet(m) && !isNext;
          let icon;
          if (st === 'passed') {
            icon = '<span class="status st-passed">✓</span>';
          } else if (st === 'in_progress') {
            icon = '<span class="status st-wip">◐</span>';
          } else {
            icon = '<span class="status"><i class="st-dot"></i></span>';
          }

          const tag =
            m.type && m.type !== 'concept'
              ? '<span class="tag">' + esc(m.type) + '</span>'
              : isNext
              ? '<span class="next-flag">next ▸</span>'
              : '';

          const cls =
            'mod' + (isNext ? ' next' : '') + (locked ? ' locked' : '');
          const tagEl = locked ? '<span class="tag">locked</span>' : tag;
          const inner =
            icon +
            '<span class="day">D' +
            (m.day != null ? m.day : '?') +
            '</span>' +
            '<span class="mod-title">' +
            esc(m.title) +
            '</span>' +
            tagEl;
          return locked
            ? '<div class="' +
                cls +
                '" style="--phase:' +
                color +
                '">' +
                inner +
                '</div>'
            : '<a class="' +
                cls +
                '" style="--phase:' +
                color +
                '" href="' +
                esc(lessonHref(m)) +
                '">' +
                inner +
                '</a>';
        })
        .join('');

      html +=
        '<details class="week" ' +
        open +
        ' style="--phase:' +
        color +
        ';animation-delay:' +
        i * 45 +
        'ms">' +
        '<summary>' +
        '<span class="wk-num">WK ' +
        String(w.number).padStart(2, '0') +
        '</span>' +
        '<span>' +
        '<span class="wk-title">' +
        esc(w.title) +
        '</span>' +
        '<span class="wk-theme"> · ' +
        esc(phaseTitle[w.phase] || '') +
        '</span>' +
        '</span>' +
        '<span class="wk-right">' +
        '<span class="track"><span class="fill" style="width:' +
        pct +
        '%;background:' +
        color +
        '"></span></span>' +
        '<span class="wk-pct">' +
        pct +
        '%</span>' +
        '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 6l6 6-6 6"/></svg>' +
        '</span>' +
        '</summary>' +
        '<div class="modules">' +
        mods +
        '</div>' +
        '</details>';
    });

    html +=
      '</main>' +
      '<footer class="graph-foot">collapsible tree · reads graph.json + summary.json · the edge-graph view is the fast-follow on the same data</footer>';

    app.innerHTML = html;
  }

  load();
})();
