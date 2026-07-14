/* identity-check.js
 * ------------------------------------------------------------------
 * Nudge students to use the SAME GitHub account for (a) forking/cloning this
 * repo and (b) signing in to record progress (Supabase GitHub OAuth).
 *
 * The fork owner is baked into the header at build time (data-git-user on
 * #ox-header-user, from hooks/git_identity.py). The signed-in GitHub username
 * is read from the Supabase session persisted in localStorage. If both are
 * known and they differ, show a dismissible banner. No mismatch, not signed
 * in, or no fork identity -> nothing shown. Dismissal is remembered per
 * (fork-user, signed-in-user) pair so it re-nudges only if the pairing changes.
 */
(function () {
  var el = document.getElementById("ox-header-user");
  var cfg = window.OX_SUPABASE;
  if (!el || !cfg || !cfg.url) return;

  var gitUser = (el.getAttribute("data-git-user") || "").trim().toLowerCase();
  if (!gitUser) return; // no fork identity to compare against

  var ref = (cfg.url.match(/^https?:\/\/([^.]+)\./) || [])[1];
  if (!ref) return;

  var supaUser = "";
  try {
    var raw = localStorage.getItem("sb-" + ref + "-auth-token");
    if (!raw) return; // not signed in -> nothing to compare yet
    var obj = JSON.parse(raw);
    var user = obj && (obj.user ||
      (obj.currentSession && obj.currentSession.user) ||
      (obj.session && obj.session.user));
    var meta = (user && user.user_metadata) || {};
    supaUser = (meta.user_name || meta.preferred_username || "").trim().toLowerCase();
  } catch (e) {
    return;
  }
  if (!supaUser || supaUser === gitUser) return; // unknown or matches -> no nudge

  var key = "ox-identity-nudge-dismissed:" + gitUser + "|" + supaUser;
  try { if (localStorage.getItem(key)) return; } catch (e) { /* ignore */ }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  var bar = document.createElement("div");
  bar.className = "ox-identity-nudge";
  bar.setAttribute("role", "alert");
  bar.innerHTML =
    '<div class="ox-identity-nudge__body">' +
      '<span class="ox-identity-nudge__msg">Heads up: this fork belongs to GitHub user <b>' +
      esc(gitUser) + '</b>, but you are signed in to record progress as <b>' + esc(supaUser) +
      '</b>. To keep your attempts attached to your fork, sign out and sign back in as <b>' +
      esc(gitUser) + '</b>.</span>' +
      '<div class="ox-identity-nudge__actions">' +
        '<button class="ox-identity-nudge__btn" type="button" data-act="signout">Sign out</button>' +
        '<a class="ox-identity-nudge__link" href="https://github.com/settings/applications" ' +
          'target="_blank" rel="noopener">Switch GitHub account &#8599;</a>' +
      '</div>' +
      '<span class="ox-identity-nudge__hint">After signing out, also sign out of GitHub (or revoke ' +
      'access there) first &mdash; otherwise GitHub will just sign you back in as <b>' + esc(supaUser) +
      '</b>.</span>' +
    '</div>' +
    '<button class="ox-identity-nudge__x" type="button" aria-label="Dismiss">&times;</button>';

  // Sign out = clear the Supabase session persisted for this project, then reload.
  // (Works on any page, offline; the GitHub-side switch is what actually changes account.)
  bar.querySelector('[data-act="signout"]').addEventListener("click", function () {
    try {
      Object.keys(localStorage).forEach(function (k) {
        if (k.indexOf("sb-" + ref + "-") === 0) localStorage.removeItem(k);
      });
    } catch (e) { /* ignore */ }
    location.reload();
  });
  bar.querySelector(".ox-identity-nudge__x").addEventListener("click", function () {
    bar.remove();
    try { localStorage.setItem(key, "1"); } catch (e) { /* ignore */ }
  });

  document.body.appendChild(bar);
})();
