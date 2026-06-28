/* ============================================================
   batch-tradeoff.js — flagship interactive playground
   ------------------------------------------------------------
   Mounts into any `<div class="ox-playground" data-widget="batch-tradeoff">`
   and renders an interactive latency-vs-throughput frontier with a
   batch-size slider. Vanilla JS + inline SVG, no framework.

   Toy serving model (illustrative, not benchmarked):
     prefill_ms       = 50
     itl_ms(batch)    = 20 + 0.5 * (batch - 1)
     output_tokens    = 100
     per_req_ms(b)    = prefill_ms + output_tokens * itl_ms(b)
     throughput_tps(b)= b * (1000 / itl_ms(b))

   Reads color tokens off :root via getComputedStyle so the widget
   re-themes correctly when the user toggles light/dark.
   ============================================================ */

(function () {
  "use strict";

  const SELECTOR = '.ox-playground[data-widget="batch-tradeoff"]';
  const BATCH_MIN = 1;
  const BATCH_MAX = 32;
  const PREFILL_MS = 50;
  const OUTPUT_TOKENS = 100;
  const ITL_BASE_MS = 20;
  const ITL_PER_BATCH_MS = 0.5;

  // ---- tiny SVG helper ---------------------------------------
  const SVG_NS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs) {
    const el = document.createElementNS(SVG_NS, tag);
    if (attrs) {
      for (const k in attrs) el.setAttribute(k, attrs[k]);
    }
    return el;
  }

  // ---- model -------------------------------------------------
  function itl(batch)        { return ITL_BASE_MS + ITL_PER_BATCH_MS * (batch - 1); }
  function perReqMs(batch)   { return PREFILL_MS + OUTPUT_TOKENS * itl(batch); }
  function throughput(batch) { return batch * (1000 / itl(batch)); }

  // ---- pull --ox-* tokens from CSS so colors track the theme
  function tokens(root) {
    const s = getComputedStyle(root);
    return {
      bg:      s.getPropertyValue("--ox-bg").trim()         || "#F6F1E6",
      surface: s.getPropertyValue("--ox-surface").trim()    || "#FBF7EE",
      ink:     s.getPropertyValue("--ox-ink").trim()        || "#1E1A16",
      body:    s.getPropertyValue("--ox-body").trim()       || "#3E342B",
      muted:   s.getPropertyValue("--ox-muted").trim()      || "#6E5F52",
      line:    s.getPropertyValue("--ox-line-strong").trim()|| "rgba(0,0,0,.2)",
      accent:  s.getPropertyValue("--ox-accent").trim()     || "#7A1F2B",
      amber:   s.getPropertyValue("--ox-amber").trim()      || "#C97A3A",
      teal:    s.getPropertyValue("--ox-teal").trim()       || "#2F6B68",
      mint:    s.getPropertyValue("--ox-mint").trim()       || "#4F8A6F",
    };
  }

  // ---- formatting --------------------------------------------
  function fmtMs(v)  { return v >= 1000 ? (v / 1000).toFixed(2) + " s" : Math.round(v) + " ms"; }
  function fmtTps(v) { return v >= 1000 ? (v / 1000).toFixed(2) + "k" : Math.round(v).toString(); }

  // ---- main builder ------------------------------------------
  function build(host) {
    const body = host.querySelector(".ox-playground__body");
    if (!body) return;
    body.innerHTML = "";   // clear loading state

    // wrapper
    const root = document.createElement("div");
    root.className = "bt-root";
    body.appendChild(root);

    // -- numeric readout strip ---------------------------------
    const readout = document.createElement("div");
    readout.className = "bt-readout";
    readout.innerHTML = `
      <div class="bt-metric bt-metric--latency">
        <span class="bt-metric__label">Per-request P50 latency</span>
        <span class="bt-metric__value" data-bt="latency">—</span>
      </div>
      <div class="bt-metric bt-metric--throughput">
        <span class="bt-metric__label">System throughput</span>
        <span class="bt-metric__value" data-bt="throughput">— <span class="bt-metric__unit">tok/s</span></span>
      </div>
      <div class="bt-metric bt-metric--util">
        <span class="bt-metric__label">Decode step (ITL)</span>
        <span class="bt-metric__value" data-bt="itl">— <span class="bt-metric__unit">ms/tok</span></span>
      </div>
    `;
    root.appendChild(readout);

    // -- chart area --------------------------------------------
    const chart = document.createElement("div");
    chart.className = "bt-chart";
    root.appendChild(chart);

    // The chart redraws on theme toggle; build it once and update.
    // viewBox is fixed; CSS makes it responsive.
    const W = 560, H = 220;
    const padL = 56, padR = 16, padT = 18, padB = 38;
    const plotW = W - padL - padR;
    const plotH = H - padT - padB;

    const root_svg = svg("svg", {
      viewBox: `0 0 ${W} ${H}`,
      role: "img",
      "aria-label": "Latency vs throughput Pareto frontier"
    });
    chart.appendChild(root_svg);

    // sample 32 batch sizes for the curve
    const samples = [];
    for (let b = BATCH_MIN; b <= BATCH_MAX; b++) {
      samples.push({ b, lat: perReqMs(b), tps: throughput(b) });
    }
    const latMin = samples[0].lat;
    const latMax = samples[samples.length - 1].lat;
    const tpsMin = 0;
    const tpsMax = samples[samples.length - 1].tps;
    const xOf = (lat) => padL + ((lat - latMin) / (latMax - latMin)) * plotW;
    const yOf = (tps) => padT + plotH - ((tps - tpsMin) / (tpsMax - tpsMin)) * plotH;

    // built dynamically inside redraw() so colors track the theme
    let redraw;

    function paint() {
      const t = tokens(document.body);
      root_svg.replaceChildren();

      // axes
      root_svg.appendChild(svg("line", {
        x1: padL, y1: padT + plotH, x2: padL + plotW, y2: padT + plotH,
        stroke: t.line, "stroke-width": 1
      }));
      root_svg.appendChild(svg("line", {
        x1: padL, y1: padT, x2: padL, y2: padT + plotH,
        stroke: t.line, "stroke-width": 1
      }));

      // axis ticks/labels — sparse
      const xTicks = [latMin, (latMin + latMax) / 2, latMax];
      xTicks.forEach((v) => {
        const x = xOf(v);
        root_svg.appendChild(svg("line", {
          x1: x, y1: padT + plotH, x2: x, y2: padT + plotH + 4,
          stroke: t.muted, "stroke-width": 1
        }));
        const lbl = svg("text", {
          x, y: padT + plotH + 18, "text-anchor": "middle",
          fill: t.muted, "font-family": "var(--ox-font-mono)",
          "font-size": 10, "letter-spacing": ".08em"
        });
        lbl.textContent = fmtMs(v);
        root_svg.appendChild(lbl);
      });

      const yTicks = [0, tpsMax / 2, tpsMax];
      yTicks.forEach((v) => {
        const y = yOf(v);
        root_svg.appendChild(svg("line", {
          x1: padL - 4, y1: y, x2: padL, y2: y,
          stroke: t.muted, "stroke-width": 1
        }));
        const lbl = svg("text", {
          x: padL - 8, y: y + 4, "text-anchor": "end",
          fill: t.muted, "font-family": "var(--ox-font-mono)",
          "font-size": 10, "letter-spacing": ".08em"
        });
        lbl.textContent = fmtTps(v);
        root_svg.appendChild(lbl);
      });

      // axis titles
      const xTitle = svg("text", {
        x: padL + plotW / 2, y: H - 6, "text-anchor": "middle",
        fill: t.muted, "font-family": "var(--ox-font-mono)",
        "font-size": 10, "letter-spacing": ".14em"
      });
      xTitle.textContent = "PER-REQUEST LATENCY →";
      root_svg.appendChild(xTitle);

      const yTitle = svg("text", {
        x: 14, y: padT + plotH / 2,
        fill: t.muted, "font-family": "var(--ox-font-mono)",
        "font-size": 10, "letter-spacing": ".14em",
        transform: `rotate(-90 14 ${padT + plotH / 2})`,
        "text-anchor": "middle"
      });
      yTitle.textContent = "THROUGHPUT (TOK/S) →";
      root_svg.appendChild(yTitle);

      // the frontier curve
      let d = "";
      samples.forEach((s, i) => {
        d += (i === 0 ? "M" : "L") + xOf(s.lat) + "," + yOf(s.tps);
      });
      root_svg.appendChild(svg("path", {
        d, fill: "none", stroke: t.accent, "stroke-width": 2,
        "stroke-linecap": "round", "stroke-linejoin": "round", opacity: ".75"
      }));

      // sample dots
      samples.forEach((s) => {
        root_svg.appendChild(svg("circle", {
          cx: xOf(s.lat), cy: yOf(s.tps), r: 2.5,
          fill: t.bg, stroke: t.accent, "stroke-width": 1
        }));
      });

      // the current operating point (filled below by redraw)
      const dot = svg("circle", {
        cx: xOf(samples[0].lat), cy: yOf(samples[0].tps),
        r: 7, fill: t.amber, stroke: t.ink, "stroke-width": 1.5,
        "data-bt": "dot", style: "transition: cx .15s ease, cy .15s ease"
      });
      root_svg.appendChild(dot);

      // crosshair guides (faint)
      const vGuide = svg("line", {
        "data-bt": "vguide",
        x1: 0, y1: padT, x2: 0, y2: padT + plotH,
        stroke: t.muted, "stroke-width": 1, "stroke-dasharray": "2 3", opacity: .35
      });
      const hGuide = svg("line", {
        "data-bt": "hguide",
        x1: padL, y1: 0, x2: padL + plotW, y2: 0,
        stroke: t.muted, "stroke-width": 1, "stroke-dasharray": "2 3", opacity: .35
      });
      root_svg.appendChild(vGuide);
      root_svg.appendChild(hGuide);

      // metric value colors track theme
      const valLat = readout.querySelector('[data-bt="latency"]');
      const valTps = readout.querySelector('[data-bt="throughput"]');
      const valItl = readout.querySelector('[data-bt="itl"]');
      if (valLat) valLat.style.color = t.amber;
      if (valTps) valTps.style.color = t.teal;
      if (valItl) valItl.style.color = t.ink;

      redraw = function (b) {
        const s = samples[b - BATCH_MIN];
        if (!s) return;
        dot.setAttribute("cx", xOf(s.lat));
        dot.setAttribute("cy", yOf(s.tps));
        vGuide.setAttribute("x1", xOf(s.lat));
        vGuide.setAttribute("x2", xOf(s.lat));
        hGuide.setAttribute("y1", yOf(s.tps));
        hGuide.setAttribute("y2", yOf(s.tps));
        if (valLat) valLat.textContent = fmtMs(s.lat);
        if (valTps) {
          valTps.innerHTML = fmtTps(s.tps) +
            ' <span class="bt-metric__unit">tok/s</span>';
        }
        if (valItl) {
          valItl.innerHTML = itl(b).toFixed(1) +
            ' <span class="bt-metric__unit">ms/tok</span>';
        }
      };
    }

    paint();

    // -- slider + summary --------------------------------------
    const controls = document.createElement("div");
    controls.className = "bt-controls";
    controls.innerHTML = `
      <label class="bt-slider-label">
        <span class="bt-slider-label__title">Batch size</span>
        <span class="bt-slider-label__value" data-bt="batch">1</span>
      </label>
      <input type="range"
             class="bt-slider"
             min="${BATCH_MIN}" max="${BATCH_MAX}" step="1" value="1"
             aria-label="Batch size">
      <div class="bt-scale">
        <span>${BATCH_MIN}</span>
        <span>${Math.round((BATCH_MIN + BATCH_MAX) / 2)}</span>
        <span>${BATCH_MAX}</span>
      </div>
      <p class="bt-note">
        Latency climbs gently because each decode step does more work; throughput
        climbs sharply at first, then flattens once the decode step lengthens enough
        to cancel the per-batch gain. <strong>The frontier is real — picking a point on it is the engineering job.</strong>
      </p>
    `;
    root.appendChild(controls);

    const slider = controls.querySelector(".bt-slider");
    const batchVal = controls.querySelector('[data-bt="batch"]');
    function update(b) {
      batchVal.textContent = b;
      redraw(b);
    }
    slider.addEventListener("input", (e) => update(parseInt(e.target.value, 10)));

    update(1);

    // re-paint on theme toggle (Material toggles data-md-color-scheme on <body>)
    const observer = new MutationObserver(() => {
      paint();
      update(parseInt(slider.value, 10));
    });
    observer.observe(document.body, { attributes: true, attributeFilter: ["data-md-color-scheme"] });

    host.setAttribute("data-hydrated", "true");
  }

  // ---- inject widget-specific CSS once -----------------------
  function injectStyles() {
    if (document.getElementById("bt-styles")) return;
    const s = document.createElement("style");
    s.id = "bt-styles";
    s.textContent = `
      .bt-root { display: flex; flex-direction: column; gap: 1rem; }
      .bt-readout {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
        gap: .8rem 1.5rem;
        padding-bottom: .4rem;
        border-bottom: 1px solid var(--ox-line);
      }
      .bt-metric { display: flex; flex-direction: column; gap: .15rem; }
      .bt-metric__label {
        font-family: var(--ox-font-mono);
        font-size: .7rem;
        font-weight: 600;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: var(--ox-muted);
      }
      .bt-metric__value {
        font-family: var(--ox-font-display);
        font-size: 1.7rem;
        font-weight: 600;
        line-height: 1;
        letter-spacing: -.02em;
        font-variant-numeric: tabular-nums;
      }
      .bt-metric__unit {
        font-family: var(--ox-font-mono);
        font-size: .75rem;
        font-weight: 600;
        letter-spacing: .04em;
        color: var(--ox-muted);
        margin-left: .15em;
      }

      .bt-chart svg { display: block; width: 100%; height: auto; }

      .bt-controls {
        display: flex; flex-direction: column; gap: .35rem;
        padding-top: .5rem;
        border-top: 1px solid var(--ox-line);
      }
      .bt-slider-label {
        display: flex; align-items: baseline; justify-content: space-between;
        font-family: var(--ox-font-mono);
        font-size: .74rem;
        font-weight: 600;
        letter-spacing: .12em;
        text-transform: uppercase;
        color: var(--ox-muted);
      }
      .bt-slider-label__value {
        font-family: var(--ox-font-display);
        font-size: 1.4rem;
        font-weight: 600;
        font-variant-numeric: tabular-nums;
        color: var(--ox-accent);
        letter-spacing: -.01em;
      }
      .bt-slider {
        appearance: none;
        -webkit-appearance: none;
        width: 100%;
        height: 4px;
        background: var(--ox-line-strong);
        border-radius: 2px;
        outline: none;
        margin: .35rem 0 .15rem;
        cursor: pointer;
      }
      .bt-slider::-webkit-slider-thumb {
        appearance: none;
        -webkit-appearance: none;
        width: 18px; height: 18px;
        border-radius: 50%;
        background: var(--ox-accent);
        border: 2px solid var(--ox-bg);
        box-shadow: 0 0 0 1px var(--ox-accent);
        cursor: grab;
        transition: transform .15s ease;
      }
      .bt-slider::-webkit-slider-thumb:active { transform: scale(1.15); cursor: grabbing; }
      .bt-slider::-moz-range-thumb {
        width: 18px; height: 18px;
        border-radius: 50%;
        background: var(--ox-accent);
        border: 2px solid var(--ox-bg);
        box-shadow: 0 0 0 1px var(--ox-accent);
        cursor: grab;
      }
      .bt-slider:focus-visible::-webkit-slider-thumb {
        box-shadow: 0 0 0 1px var(--ox-accent), 0 0 0 4px var(--ox-accent-soft);
      }

      .bt-scale {
        display: flex; justify-content: space-between;
        font-family: var(--ox-font-mono);
        font-size: .65rem;
        letter-spacing: .08em;
        color: var(--ox-muted);
      }
      .bt-note {
        margin: .5rem 0 0;
        font-size: .82rem;
        line-height: 1.5;
        color: var(--ox-body);
      }
      .bt-note strong { color: var(--ox-ink); font-weight: 600; }

      @media (prefers-reduced-motion: reduce) {
        [data-bt="dot"] { transition: none !important; }
      }
    `;
    document.head.appendChild(s);
  }

  // ---- bootstrap ---------------------------------------------
  function init() {
    injectStyles();
    document.querySelectorAll(SELECTOR).forEach(build);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
