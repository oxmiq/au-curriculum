/* embed-autosize.js
   ------------------------------------------------------------------
   The kb/*.md wrapper pages embed a self-contained visualization via
   <iframe class="ox-embed">. For document-flow views (marked
   data-embed="flow") we grow the iframe to its content's height so it
   scrolls as one with the host page — no inner scrollbar, no boxed
   "page-in-a-page" look. Same-origin, so we can read the framed doc.
   Full-window apps (data-embed="app") keep their CSS viewport height
   and are left alone. */
(function () {
  function measure(doc) {
    var b = doc.body, e = doc.documentElement;
    return Math.max(
      b ? b.scrollHeight : 0, b ? b.offsetHeight : 0,
      e ? e.scrollHeight : 0, e ? e.offsetHeight : 0
    );
  }

  function fit(iframe) {
    try {
      var doc = iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document);
      if (!doc || !doc.body) return;
      var h = measure(doc);
      if (h > 0) iframe.style.height = h + 'px';
    } catch (e) { /* cross-origin or not ready — leave CSS height */ }
  }

  function setup(iframe) {
    var refit = function () { fit(iframe); };
    var onReady = function () {
      refit();
      try {
        var doc = iframe.contentDocument;
        // re-fit when the framed content reflows (async render, image load)
        if (window.ResizeObserver && doc && doc.body) {
          new ResizeObserver(refit).observe(doc.body);
        }
        // …or when its own controls (view toggles, search) change layout
        if (doc) doc.addEventListener('click', function () { setTimeout(refit, 60); });
      } catch (e) { /* ignore */ }
      // a couple of trailing passes catch late layout settling
      setTimeout(refit, 150);
      setTimeout(refit, 500);
    };
    iframe.addEventListener('load', onReady);
    // already loaded (e.g. bfcache restore)
    try {
      if (iframe.contentDocument && iframe.contentDocument.readyState === 'complete') onReady();
    } catch (e) { /* ignore */ }
  }

  function init() {
    var frames = document.querySelectorAll('iframe.ox-embed[data-embed="flow"]');
    for (var i = 0; i < frames.length; i++) setup(frames[i]);
  }

  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);

  window.addEventListener('resize', function () {
    var frames = document.querySelectorAll('iframe.ox-embed[data-embed="flow"]');
    for (var i = 0; i < frames.length; i++) fit(frames[i]);
  });
})();
