/* Unit test for the submit-error classification in assets/widgets/self-check.js.
 *
 * Run:  node tests/self_check_errors.test.mjs
 *
 * Loads the real widget with minimal DOM stubs (same harness as
 * progress_source.test.mjs) and drives the exported classifySubmitError().
 *
 * The copy this pins exists because the old generic advice — "Not recorded
 * (grading failed (Failed to fetch)). Sign in and retry." — sent
 * already-signed-in students in circles during the 127.0.0.1 CORS outage:
 * a fetch TypeError means network/CORS, not "you are not signed in".
 */
import { readFileSync } from "node:fs";
import assert from "node:assert/strict";
import vm from "node:vm";

const src = readFileSync(new URL("../docs/assets/widgets/self-check.js", import.meta.url), "utf8");

const sandbox = {
  document: {
    currentScript: { src: "https://example.test/assets/widgets/self-check.js" },
    readyState: "loading",          // skips hydrateAll at load time
    addEventListener() {},
    querySelectorAll: () => [],
  },
  location: { href: "https://example.test/lessons/week-01/module-1/", origin: "https://example.test" },
  console,
};
sandbox.window = sandbox;
vm.createContext(sandbox);
vm.runInContext(src, sandbox);

const classify = sandbox.window.OX_SELF_CHECK.classifySubmitError;
assert.equal(typeof classify, "function", "classifySubmitError is exported for tests");
const kind = (err) => classify(err).kind;

// 1. Not signed in (submit while signed out).
assert.equal(kind(new Error("not signed in")), "auth");
console.log("  PASS  'not signed in' -> auth");

// 2. Expired session.
assert.equal(kind(new Error("grading failed (401)")), "auth");
assert.equal(kind(new Error("invalid session")), "auth");
console.log("  PASS  401 / invalid session -> auth");

// 3. Replay throttle.
assert.equal(kind(new Error("grading failed (429)")), "throttle");
assert.equal(kind(new Error("too soon — retry in a moment")), "throttle");
console.log("  PASS  429 / too soon -> throttle");

// 4. Retired check on a stale fork (answer key deleted server-side).
assert.equal(kind(new Error("grading failed (404)")), "gone");
console.log("  PASS  404 (retired check, stale fork) -> gone, with the git-pull fix");

// 5. Pool/draw drift (rejected submission).
assert.equal(kind(new Error("grading failed (400)")), "mismatch");
console.log("  PASS  400 (check/question mismatch) -> mismatch");

// 6. supabase-js could not load at all.
assert.equal(kind(new Error("storage unavailable")), "offline");
console.log("  PASS  'storage unavailable' -> offline");

// 7. Network / CORS — the outage signature — across browsers. fetch() throws
//    TypeError on network failure AND on CORS preflight denial; a failed
//    dynamic import is a TypeError too.
assert.equal(kind(new TypeError("Failed to fetch")), "network");                        // Chrome
assert.equal(kind(new TypeError("NetworkError when attempting to fetch resource.")), "network"); // Firefox
assert.equal(kind(new TypeError("Load failed")), "network");                            // Safari
assert.equal(kind(new TypeError("Failed to fetch dynamically imported module: https://esm.sh/@supabase/supabase-js@2")), "network");
console.log("  PASS  fetch TypeErrors (Chrome/Firefox/Safari + dynamic import) -> network");

// 8. The network hint must be actionable: name the origin the student is on,
//    the canonical local URL, and the one-address rule.
{
  const hint = classify(new TypeError("Failed to fetch")).hint;
  assert.ok(hint.includes("https://example.test"), "names the origin the student is on");
  assert.ok(hint.includes("http://localhost:8000/au-curriculum/"), "names the canonical local URL");
  assert.ok(/localhost, 127\.0\.0\.1/.test(hint), "explains the one-address rule");
  assert.ok(!/sign in/i.test(hint), "does not tell an already-signed-in student to sign in");
  console.log("  PASS  network hint names the origin, canonical URL and one-address rule");
}

// 9. Anything else keeps the original message for debuggability.
{
  const c = classify(new Error("grading failed (500)"));
  assert.equal(c.kind, "server");
  assert.ok(c.hint.includes("grading failed (500)"), "server errors keep the original message");
  console.log("  PASS  unknown server errors keep their message");
}

// 10. Strings (not just Error objects) classify identically.
assert.equal(kind("Failed to fetch"), "network");
assert.equal(kind("grading failed (404)"), "gone");
console.log("  PASS  bare strings classify the same as Errors");

// 11. 403 = ineligible. grade-readiness rejects a student whose GitHub primary
// email is no longer their college address, and sends an actionable message.
// The widget MUST show that message: paraphrasing it ("the grading service
// returned an error (403)") is what made the earlier CORS outage unfixable
// from the student's side.
{
  const serverMsg =
    "Your GitHub account's primary email is now someone@gmail.com. Progress is " +
    "only recorded for GitHub accounts whose primary email is your Andhra " +
    "University address (323506402103@andhrauniversity.edu.in). Open " +
    "github.com/settings/emails, set your college address as Primary, then " +
    "sign out and back in here and retake this check. Your previously " +
    "recorded attempts are safe.";
  const c = classify(new Error("grading failed (403) :: " + serverMsg));
  assert.equal(c.kind, "ineligible");
  assert.equal(c.hint, serverMsg, "the server's message is shown verbatim, not paraphrased");
  assert.ok(!/returned an error/.test(c.hint), "the generic server wording is not used");
  console.log("  PASS  403 shows the server's eligibility message verbatim");
}

// 12. A 403 with no parseable body still says something useful.
{
  const c = classify(new Error("grading failed (403)"));
  assert.equal(c.kind, "ineligible");
  assert.ok(/not eligible/i.test(c.hint), "falls back to a plain ineligibility hint");
  assert.ok(/mentor/i.test(c.hint), "tells them who to ask");
  console.log("  PASS  403 without a body still explains itself");
}

// 13. A server message on any other status is surfaced too, rather than the
// raw thrown string.
{
  const c = classify(new Error("grading failed (500) :: the grading service is restarting"));
  assert.equal(c.kind, "server");
  assert.ok(c.hint.startsWith("the grading service is restarting"),
    "the server's words lead the hint");
  console.log("  PASS  a server message on another status is surfaced");
}

console.log("\n=== self_check_errors: ALL ASSERTIONS PASSED ===");
