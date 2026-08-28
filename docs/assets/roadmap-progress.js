/* roadmap-progress.js — overlays student progress onto the roadmap sitemap.
 *
 * Progress comes from assets/progress-source.js (window.OX_PROGRESS.ready),
 * which resolves the signed-in student's LIVE Supabase attempts where possible
 * and falls back to the committed progress/summary.json otherwise. This file
 * used to fetch summary.json directly, which meant the roadmap only ever showed
 * the committed record — in practice all zeros, since nothing writes the
 * per-module JSON automatically.
 *
 *   window.OX_PROGRESS.ready  — per-module status + weekly / overall rollups
 *   kb/graph.json             — module prereqs (for "next up")
 *
 * Pure progressive enhancement: the static roadmap (structure + lesson links)
 * works with JS off or if either source fails. Only when progress resolves do
 * the status ticks, week bars, overall bar, legend and next-up state appear.
 */
(function () {
  "use strict";

  var root = document.querySelector(".ox-roadmap");
  if (!root) return; // only on the roadmap page

  // Relative to the roadmap page (served at <base>/roadmap/).
  var GRAPH_URL = "../kb/graph.json";

  function statusOf(summary, id) {
    return (
      (summary.modules && summary.modules[id] && summary.modules[id].status) ||
      "not_started"
    );
  }

  function getJSON(url) {
    return fetch(url)
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }

  var progress = (window.OX_PROGRESS && window.OX_PROGRESS.ready) || Promise.resolve(null);
  Promise.all([progress, getJSON(GRAPH_URL)]).then(function (res) {
    var summary = res[0];
    if (!summary) return; // no progress data → leave the static roadmap untouched
    decorate(summary, res[1]);
  });

  function decorate(summary, graph) {
    var days = root.querySelectorAll(".ox-rmap-day[data-module]");

    // 1) per-day status
    days.forEach(function (a) {
      a.setAttribute("data-status", statusOf(summary, a.getAttribute("data-module")));
    });

    // 2) "next up" — the first not-passed module whose prereqs are all met.
    // (We intentionally do NOT gate/lock later sessions: graph.json's prereqs
    // are a near-linear chain, so locking would dim ~every upcoming tile and
    // block navigation on what is also the site's primary catalog.)
    if (graph && graph.weeks) {
      var all = [];
      graph.weeks.forEach(function (w) {
        (w.modules || []).forEach(function (m) { all.push(m); });
      });
      all.sort(function (a, b) { return (a.day || 0) - (b.day || 0); });

      var passed = function (id) { return statusOf(summary, id) === "passed"; };
      var prereqsMet = function (m) { return (m.prereqs || []).every(passed); };

      var nextId = null;
      for (var i = 0; i < all.length; i++) {
        if (!passed(all[i].id) && prereqsMet(all[i])) { nextId = all[i].id; break; }
      }
      if (nextId) {
        var a = root.querySelector('.ox-rmap-day[data-module="' + nextId + '"]');
        if (a) {
          a.classList.add("is-next");
          var t = a.querySelector(".ox-rmap-day__t");
          if (t && !t.querySelector(".ox-rmap-day__next")) {
            var flag = document.createElement("span");
            flag.className = "ox-rmap-day__next";
            flag.textContent = "next ▸";
            t.appendChild(flag);
          }
        }
      }
    }

    // 3) per-week progress bars
    var weeks = summary.weeks || {};
    root.querySelectorAll(".ox-rmap-week").forEach(function (card) {
      var first = card.querySelector(".ox-rmap-day[data-module]");
      if (!first) return;
      var wid = first.getAttribute("data-module").split("/")[0]; // week-XX
      var wp = weeks[wid];
      if (!wp) return;
      var prog = card.querySelector(".ox-rmap-week__prog");
      if (!prog) return;
      prog.hidden = false;
      setWidth(prog, wp.percent || 0);
      var pct = prog.querySelector(".ox-rmap-week__pct");
      if (pct) pct.textContent = (wp.percent || 0) + "%";
    });

    // 4) overall summary + legend
    var overall = summary.overall || {};
    var box = document.querySelector(".ox-rmap-overall");
    if (box) {
      box.hidden = false;
      setText(box, ".ox-rmap-overall__pct", (overall.percent || 0) + "%");
      setText(box, "[data-done]", overall.completed || 0);
      setText(box, "[data-total]", overall.total || days.length);
      setWidth(box, overall.percent || 0);
    }
    var legend = document.querySelector(".ox-rmap-legend");
    if (legend) legend.hidden = false;
  }

  function setWidth(scope, percent) {
    var fill = scope.querySelector(".ox-rmap-track > i");
    if (fill) fill.style.width = percent + "%";
  }
  function setText(scope, sel, value) {
    var el = scope.querySelector(sel);
    if (el) el.textContent = value;
  }
})();
