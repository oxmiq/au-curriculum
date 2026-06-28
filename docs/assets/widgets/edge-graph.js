/* ============================================================
   Dependency Graph (edge graph) widget — Material-wrapped.
   Mounts into .edge-graph-page #edge-canvas / #legend / #edge-footer
   on kb/edge-graph.md.

   URL math: page served at /au-curriculum/kb/edge-graph/, so:
     - graph.json   → ../graph.json
     - summary.json → ../../progress/summary.json
     - lessons/...  → ../../<m.lesson>
   ============================================================ */
(function () {
  'use strict';

  if (!document.getElementById('edge-canvas')) return;

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

  const PAD = 34;
  const COL_W = 182;
  const ROW_H = 120;
  const NODE_W = 156;
  const NODE_H = 58;

  async function load() {
    let graph;
    let summary;
    try {
      [graph, summary] = await Promise.all([
        fetch(GRAPH_URL).then((r) => {
          if (!r.ok) throw new Error(GRAPH_URL);
          return r.json();
        }),
        fetch(SUMMARY_URL)
          .then((r) => (r.ok ? r.json() : { modules: {} }))
          .catch(() => ({ modules: {} })),
      ]);
    } catch (e) {
      document.getElementById('edge-canvas').innerHTML =
        '<div class="err">Couldn\'t load <code>' +
        esc(e.message) +
        '</code>. Serve over HTTP (mkdocs serve), not file://.</div>';
      return;
    }
    render(graph, summary);
  }

  const statusOf = (s, id) =>
    (s.modules && s.modules[id] && s.modules[id].status) || 'not_started';

  function render(graph, summary) {
    const pos = {};
    const nodes = [];
    let maxCols = 0;

    graph.weeks.forEach((w, wi) => {
      maxCols = Math.max(maxCols, w.modules.length);
      w.modules.forEach((m, mi) => {
        const col = wi % 2 === 0 ? mi : w.modules.length - 1 - mi;
        const x = PAD + col * COL_W;
        const y = PAD + wi * ROW_H;
        pos[m.id] = {
          x: x,
          y: y,
          cx: x + NODE_W / 2,
          cy: y + NODE_H / 2,
        };
        nodes.push(Object.assign({}, m, { phase: w.phase, week: w }));
      });
    });

    const passed = (id) => statusOf(summary, id) === 'passed';
    const prereqsMet = (m) => (m.prereqs || []).every(passed);
    const ordered = [].concat(nodes).sort((a, b) => (a.day || 0) - (b.day || 0));
    let nextId = null;
    for (const m of ordered) {
      if (statusOf(summary, m.id) !== 'passed' && prereqsMet(m)) {
        nextId = m.id;
        break;
      }
    }

    const W = PAD * 2 + (maxCols - 1) * COL_W + NODE_W;
    const H = PAD * 2 + (graph.weeks.length - 1) * ROW_H + NODE_H;

    let edges = '';
    nodes.forEach((m) => {
      (m.prereqs || []).forEach((pid) => {
        const a = pos[pid];
        const b = pos[m.id];
        if (!a || !b) return;
        const done = passed(pid) && passed(m.id);
        const dim =
          statusOf(summary, m.id) === 'not_started' && !prereqsMet(m);
        const midY = (a.cy + b.cy) / 2;
        const d =
          'M ' +
          a.cx +
          ' ' +
          a.cy +
          ' C ' +
          a.cx +
          ' ' +
          midY +
          ', ' +
          b.cx +
          ' ' +
          midY +
          ', ' +
          b.cx +
          ' ' +
          b.cy;
        const stroke = done ? 'var(--eg-edge-done)' : 'var(--eg-edge)';
        const op = dim ? 0.35 : done ? 0.95 : 0.7;
        edges +=
          '<path d="' +
          d +
          '" fill="none" stroke="' +
          stroke +
          '" stroke-width="' +
          (done ? 2 : 1.5) +
          '" opacity="' +
          op +
          '" marker-end="url(#arrow)"/>';
      });
    });

    let fos = '';
    nodes.forEach((m) => {
      const p = pos[m.id];
      const color = PHASE_COLOR[m.phase] || 'var(--eg-muted)';
      const st = statusOf(summary, m.id);
      const isNext = m.id === nextId;
      const locked = st === 'not_started' && !prereqsMet(m) && !isNext;
      let icon;
      let cls = 'node';
      if (st === 'passed') {
        icon = '<span class="st st-passed">✓</span>';
        cls += ' passed';
      } else if (st === 'in_progress') {
        icon = '<span class="st st-wip">◐</span>';
      } else if (isNext) {
        icon = '<span class="next-tag">next</span>';
        cls += ' next';
      } else {
        icon = '<span class="st"><i class="st-dot"></i></span>';
      }
      if (locked) cls += ' locked';
      const dayLbl = 'D' + (m.day != null ? m.day : '?');
      const body =
        '<div class="top"><span class="day">' +
        dayLbl +
        '</span>' +
        icon +
        '</div><div class="ttl">' +
        esc(m.title) +
        '</div>';
      const el = locked
        ? '<div class="' +
          cls +
          '" style="--phase:' +
          color +
          '" title="' +
          esc(m.title) +
          ' · locked">' +
          body +
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
          body +
          '</a>';
      fos +=
        '<foreignObject x="' +
        p.x +
        '" y="' +
        p.y +
        '" width="' +
        NODE_W +
        '" height="' +
        NODE_H +
        '">' +
        el +
        '</foreignObject>';
    });

    document.getElementById('edge-canvas').innerHTML =
      '<svg width="' +
      W +
      '" height="' +
      H +
      '" viewBox="0 0 ' +
      W +
      ' ' +
      H +
      '" xmlns="http://www.w3.org/2000/svg">' +
      '<defs>' +
      '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">' +
      '<path d="M0,0 L10,5 L0,10 z" fill="var(--eg-edge)"/>' +
      '</marker>' +
      '</defs>' +
      '<g>' +
      edges +
      '</g>' +
      fos +
      '</svg>';

    document.getElementById('legend').innerHTML =
      (graph.phases || [])
        .map(
          (p) =>
            '<span><i class="dot" style="background:' +
            (PHASE_COLOR[p.id] || 'var(--eg-muted)') +
            '"></i>' +
            esc(p.title) +
            '</span>'
        )
        .join('') +
      '<span><i class="dot" style="background:var(--eg-ok)"></i>Passed</span>' +
      '<span><i class="dot" style="background:var(--eg-wip)"></i>In progress</span>';

    document.getElementById('edge-footer').textContent =
      'fast-follow edge-graph · same graph.json + summary.json as the tree view · arrows point from a concept to what it unlocks';
  }

  load();
})();
