/* progress-source.js — the single source of student progress for the whole site.
 * ---------------------------------------------------------------------------
 * Background: the roadmap ticks, the per-week bars and the header pill were all
 * written against `docs/progress/summary.json` plus per-module records at
 * `docs/progress/week-XX/module-Y.json`. Those per-module records are produced
 * only by the `progress-recorder` skill (an agent writing into a student's fork),
 * so in practice none exist: summary.json is all zeros and every progress
 * surface on the site read 0/50 · 0% forever, no matter how much work a student
 * had actually done.
 *
 * Meanwhile every check a student takes IS recorded — server-side, append-only,
 * in Supabase, via the grade-readiness function. Nothing connected the two.
 * This module is that connection.
 *
 * It resolves `window.OX_PROGRESS.ready` with a summary in EXACTLY the shape
 * summary.json uses, so existing consumers need no rewrite:
 *
 *   { version, source: "live"|"static", modules: {"week-01/module-1": {...}},
 *     weeks: {"week-01": {completed,total,percent}},
 *     overall: {completed,total,percent} }
 *
 * Sources, in order of preference:
 *   1. LIVE — the signed-in student's own attempts, read from `readiness_progress`
 *      (a security_invoker view: RLS returns only their own rows) joined against
 *      the public `check_taxonomy`. This is authoritative.
 *   2. STATIC — docs/progress/summary.json, for signed-out visitors and for
 *      forks that record progress the committed-JSON way. Also the fallback
 *      whenever the network or the session is unavailable.
 *
 * What counts as "passed": a module is cleared when its MASTERY check reaches
 * the widget's own "strong" band (>= 80%). The mastery check is the module's
 * wrap-up, or the week's canonical knowledge check for consolidation days that
 * have no wrap-up. Pre-read (readiness) checks deliberately do NOT count toward
 * completion — they gate preparation, not mastery — but attempting one does
 * move a module to "in progress".
 */
(function () {
  "use strict";

  var PASS_THRESHOLD = 0.8;   // matches self-check.js band(): >= 0.8 is "strong"
  var TOTAL_MODULES_FALLBACK = 50;

  // Site root, derived from this script's own URL (the site has no <base> and
  // pages sit at varying depths, so relative paths alone are not enough).
  var ROOT = (function () {
    var s = document.currentScript && document.currentScript.src;
    return s ? s.replace(/assets\/progress-source\.js.*$/, "") : "";
  })();

  function emptySummary(source) {
    return { version: "1.0", source: source, modules: {}, weeks: {},
             overall: { completed: 0, total: TOTAL_MODULES_FALLBACK, percent: 0 } };
  }

  // ── static fallback ───────────────────────────────────────────────────────
  function loadStatic() {
    return fetch(ROOT + "progress/summary.json")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        if (!j) return emptySummary("static");
        j.source = "static";
        return j;
      })
      .catch(function () { return emptySummary("static"); });
  }

  // ── is there a session worth loading supabase-js for? ─────────────────────
  // Cheap localStorage probe first: no session means no import, no network.
  function hasStoredSession(cfg) {
    try {
      var ref = (cfg.url.match(/^https?:\/\/([^.]+)\./) || [])[1];
      if (!ref) return false;
      return !!localStorage.getItem("sb-" + ref + "-auth-token");
    } catch (e) { return false; }
  }

  // ── live ──────────────────────────────────────────────────────────────────
  function loadLive(cfg) {
    return import("https://esm.sh/@supabase/supabase-js@2")
      .then(function (m) {
        var sb = m.createClient(cfg.url, cfg.key);
        // getUser() lets supabase-js refresh an expired token before we query.
        return sb.auth.getUser().then(function (r) {
          if (!r || !r.data || !r.data.user) return null;
          return Promise.all([
            // select("*") rather than naming columns: check_taxonomy is 85 tiny
            // rows, and `retired` only exists from migration 0015. Naming it
            // against an older schema would error the whole query and silently
            // drop us back to static progress; with "*" the field is simply
            // absent and every check reads as live.
            sb.from("check_taxonomy").select("*"),
            sb.from("readiness_progress").select("check_id,best_ratio"),
          ]);
        });
      })
      .then(function (res) {
        if (!res) return null;
        var tax = (res[0] && res[0].data) || [];
        var prog = (res[1] && res[1].data) || [];
        if (!tax.length) return null;
        return build(tax, prog);
      })
      .catch(function (e) {
        console.warn("[ox-progress] live progress unavailable", e);
        return null;
      });
  }

  function moduleId(week, module) {
    return "week-" + String(week).padStart(2, "0") + "/module-" + module;
  }

  function build(tax, prog) {
    var bestBy = {};
    prog.forEach(function (p) {
      var v = p.best_ratio == null ? null : Number(p.best_ratio);
      if (v != null && !isNaN(v)) bestBy[p.check_id] = v;
    });

    // Group every known check by the module it belongs to.
    var byModule = {};
    tax.forEach(function (t) {
      if (t.week == null || t.module == null) return;
      var id = moduleId(t.week, t.module);
      (byModule[id] = byModule[id] || []).push(t);
    });

    var modules = {}, weeks = {};
    Object.keys(byModule).forEach(function (id) {
      var checks = byModule[id];
      // Mastery check: the wrap-up, else the canonical (consolidation days).
      // Retired checks are excluded — they may still hold immutable history, but
      // a student cannot take one today, so a module must not be gated on it.
      // Consolidation days carry only the weekly canonical by design; the two
      // wrap-ups that used to sit on W1 D5 and W6 D30 were retired as outliers.
      var live = checks.filter(function (c) { return !c.retired; });
      var mastery = live.filter(function (c) { return c.type === "wrapup"; })[0]
                 || live.filter(function (c) { return c.type === "canonical"; })[0]
                 || null;
      var masteryBest = mastery && bestBy[mastery.check_id] != null
        ? bestBy[mastery.check_id] : null;
      var attempted = checks.some(function (c) { return bestBy[c.check_id] != null; });

      // Underscore form: matches build_summary.py's records, roadmap-progress.js's
      // default, and the .ox-rmap-day[data-status="in_progress"] CSS selector.
      var status = "not_started";
      if (masteryBest != null && masteryBest >= PASS_THRESHOLD) status = "passed";
      else if (attempted) status = "in_progress";

      modules[id] = {
        status: status,
        best: masteryBest,
        mastery_check: mastery ? mastery.check_id : null,
        checks_attempted: checks.filter(function (c) { return bestBy[c.check_id] != null; }).length,
        checks_total: checks.length,
      };

      var wid = id.split("/")[0];
      weeks[wid] = weeks[wid] || { completed: 0, total: 0, percent: 0 };
      weeks[wid].total += 1;
      if (status === "passed") weeks[wid].completed += 1;
    });

    var done = 0, total = 0;
    Object.keys(weeks).forEach(function (w) {
      var x = weeks[w];
      x.percent = x.total ? Math.round((100 * x.completed) / x.total) : 0;
      done += x.completed; total += x.total;
    });
    if (!total) total = TOTAL_MODULES_FALLBACK;

    return {
      version: "1.0",
      source: "live",
      modules: modules,
      weeks: weeks,
      overall: { completed: done, total: total,
                 percent: total ? Math.round((100 * done) / total) : 0 },
    };
  }

  // ── header pill ───────────────────────────────────────────────────────────
  function paintPill(summary) {
    var pill = document.getElementById("ox-progress-pill");
    if (!pill) return;

    if (summary.source !== "live") {
      // Signed out we genuinely do not know: "0/50 · 0%" would assert that the
      // student has done nothing, which is a different claim from "unknown".
      pill.textContent = "Sign in to track progress";
      pill.className = "ox-progress-pill status-pill status-not-started";
      pill.title = "Sign in on any knowledge check to record and see your progress";
      return;
    }
    var o = summary.overall || {};
    var pct = o.percent || 0;
    pill.textContent = (o.completed || 0) + "/" + (o.total || 0) + " · " + pct + "%";
    pill.className = "ox-progress-pill status-pill " +
      (pct >= 100 ? "status-passed" : pct > 0 ? "status-in-progress" : "status-not-started");
    pill.title = "Sessions cleared (wrap-up or weekly check at " +
      Math.round(PASS_THRESHOLD * 100) + "% or better)";
    pill.setAttribute("data-pct", pct);
    pill.setAttribute("data-done", o.completed || 0);
    pill.setAttribute("data-total", o.total || 0);
  }

  // ── resolve ───────────────────────────────────────────────────────────────
  var cfg = (typeof window !== "undefined" && window.OX_SUPABASE) || null;

  // Publish the namespace BEFORE the promise can settle, so a consumer that
  // reads window.OX_PROGRESS.summary from the event handler always finds it.
  window.OX_PROGRESS = { ready: null, summary: null,
                         PASS_THRESHOLD: PASS_THRESHOLD,
                         _build: build };   // _build is exposed for tests

  window.OX_PROGRESS.ready = ((!cfg || !hasStoredSession(cfg))
    ? loadStatic()
    : loadLive(cfg).then(function (live) { return live || loadStatic(); })
  ).then(function (summary) {
    summary = summary || emptySummary("static");
    window.OX_PROGRESS.summary = summary;
    try { paintPill(summary); } catch (e) { /* never block consumers */ }
    document.dispatchEvent(new CustomEvent("ox-progress", { detail: summary }));
    return summary;
  });
})();
