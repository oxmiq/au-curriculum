/* Unit test for the module/week/overall rollup in assets/progress-source.js.
 *
 * Run:  node tests/progress_source.test.mjs
 *
 * Loads the real browser module with minimal DOM/window stubs and exercises the
 * exported _build() against the curriculum's actual check shape.
 */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
import vm from "node:vm";

const src = readFileSync(new URL("../docs/assets/progress-source.js", import.meta.url), "utf8");

const sandbox = {
  document: {
    currentScript: { src: "https://example.test/assets/progress-source.js" },
    dispatchEvent() {},
    getElementById: () => null,
  },
  localStorage: { getItem: () => null },
  fetch: () => Promise.resolve({ ok: false }),
  console,
  CustomEvent: class { constructor(t, o) { this.type = t; Object.assign(this, o); } },
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

const build = sandbox.window.OX_PROGRESS._build;
assert.equal(typeof build, "function", "_build is exported");

// Shape of a real week: 4 teaching days (readiness + wrapup) + a consolidation
// day whose only check is the week's canonical knowledge check.
const tax = [];
for (let m = 1; m <= 4; m++) {
  tax.push({ check_id: `week-01-m${m}-readiness`, week: 1, module: m, type: "readiness" });
  tax.push({ check_id: `week-01-m${m}-wrapup`,    week: 1, module: m, type: "wrapup" });
}
tax.push({ check_id: "week-01-m5-canonical", week: 1, module: 5, type: "canonical" });

function statuses(prog) {
  const s = build(tax, prog);
  return { s, m: (n) => s.modules[`week-01/module-${n}`].status };
}

// 1. No attempts at all.
{
  const { s, m } = statuses([]);
  assert.equal(m(1), "not_started");
  assert.equal(s.overall.completed, 0);
  assert.equal(s.overall.total, 5);
  assert.equal(s.overall.percent, 0);
  console.log("  PASS  no attempts -> everything not_started");
}

// 2. Pre-read alone must NOT clear a module, but does start it.
{
  const { m } = statuses([{ check_id: "week-01-m1-readiness", best_ratio: 1.0 }]);
  assert.equal(m(1), "in_progress", "a perfect pre-read is not mastery");
  console.log("  PASS  a perfect pre-read alone -> in_progress, not passed");
}

// 3. Wrap-up at/above the 80% band clears the module.
{
  const { m } = statuses([{ check_id: "week-01-m2-wrapup", best_ratio: 0.8 }]);
  assert.equal(m(2), "passed");
  console.log("  PASS  wrap-up at exactly 0.8 -> passed");
}

// 4. Just below the band does not.
{
  const { m } = statuses([{ check_id: "week-01-m2-wrapup", best_ratio: 0.79 }]);
  assert.equal(m(2), "in_progress");
  console.log("  PASS  wrap-up at 0.79 -> in_progress");
}

// 5. Consolidation day falls back to the canonical check.
{
  const { m } = statuses([{ check_id: "week-01-m5-canonical", best_ratio: 0.9 }]);
  assert.equal(m(5), "passed", "module-5 has no wrap-up; canonical is its mastery check");
  console.log("  PASS  consolidation day clears on the canonical check");
}

// 6. Week + overall rollups.
{
  const { s } = statuses([
    { check_id: "week-01-m1-wrapup",    best_ratio: 1.0 },
    { check_id: "week-01-m2-wrapup",    best_ratio: 0.85 },
    { check_id: "week-01-m3-readiness", best_ratio: 1.0 },   // started, not cleared
    { check_id: "week-01-m5-canonical", best_ratio: 0.95 },
  ]);
  assert.equal(s.weeks["week-01"].completed, 3);
  assert.equal(s.weeks["week-01"].total, 5);
  assert.equal(s.weeks["week-01"].percent, 60);
  assert.equal(s.overall.completed, 3);
  assert.equal(s.overall.percent, 60);
  assert.equal(s.modules["week-01/module-3"].status, "in_progress");
  assert.equal(s.modules["week-01/module-4"].status, "not_started");
  console.log("  PASS  week + overall rollups (3/5 = 60%)");
}

// 7. A null best_ratio (attempt row with no usable denominator) is not mastery.
{
  const { m } = statuses([{ check_id: "week-01-m1-wrapup", best_ratio: null }]);
  assert.equal(m(1), "not_started");
  console.log("  PASS  a null best_ratio does not count as an attempt");
}

// 8. Week 10 shape: wrap-up only, no canonical.
{
  const t10 = [{ check_id: "week-10-m1-wrapup", week: 10, module: 1, type: "wrapup" }];
  const s = build(t10, [{ check_id: "week-10-m1-wrapup", best_ratio: 0.9 }]);
  assert.equal(s.modules["week-10/module-1"].status, "passed");
  assert.equal(s.overall.total, 1);
  console.log("  PASS  week-10 (wrap-up only, no canonical) clears correctly");
}

// 9. A RETIRED wrap-up must not be the mastery check. Consolidation days carry
//    only the weekly canonical; the W1 D5 / W6 D30 wrap-ups were retired as
//    outliers, but their historical attempts still exist in check_taxonomy.
{
  const t = [
    { check_id: "week-01-m5-wrapup",    week: 1, module: 5, type: "wrapup",    retired: true },
    { check_id: "week-01-m5-canonical", week: 1, module: 5, type: "canonical", retired: false },
  ];
  // A past 0.9 on the retired wrap-up must NOT clear the module...
  let s = build(t, [{ check_id: "week-01-m5-wrapup", best_ratio: 0.9 }]);
  assert.equal(s.modules["week-01/module-5"].status, "in_progress",
    "a retired wrap-up cannot gate a module a student can no longer take");
  assert.equal(s.modules["week-01/module-5"].mastery_check, "week-01-m5-canonical");

  // ...the canonical does.
  s = build(t, [{ check_id: "week-01-m5-canonical", best_ratio: 0.9 }]);
  assert.equal(s.modules["week-01/module-5"].status, "passed");
  console.log("  PASS  a retired wrap-up is ignored; the canonical is the mastery check");
}

// 10. Absent `retired` (older taxonomy rows) must behave as live.
{
  const t = [{ check_id: "week-02-m1-wrapup", week: 2, module: 1, type: "wrapup" }];
  const s = build(t, [{ check_id: "week-02-m1-wrapup", best_ratio: 0.9 }]);
  assert.equal(s.modules["week-02/module-1"].status, "passed");
  console.log("  PASS  a taxonomy row without `retired` is treated as live");
}

console.log("\n=== progress_source: ALL ASSERTIONS PASSED ===");
