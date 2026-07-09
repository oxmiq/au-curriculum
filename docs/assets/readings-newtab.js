/* readings-newtab.js
   ------------------------------------------------------------
   Open links to the standalone reading / reference pages
   (docs/readings/**) in a NEW TAB, so pre-read material never
   pulls the student out of the lesson's navigation context.

   Progressive enhancement: without JS the links still work, they
   just open in the same tab. External http(s) links are skipped —
   the lesson markup already gives those target="_blank".
   ------------------------------------------------------------ */
(function () {
  'use strict';

  function mark(root) {
    var scope = root || document;
    var links = scope.querySelectorAll('a[href*="readings/"]');
    Array.prototype.forEach.call(links, function (a) {
      if (a.dataset.newtab) return;
      var href = a.getAttribute('href') || '';
      if (/^https?:\/\//i.test(href)) return; // external links already handled
      a.target = '_blank';
      a.rel = 'noopener';
      a.dataset.newtab = '1';
    });
  }

  // Material's instant navigation (if ever enabled) re-emits document$;
  // otherwise fall back to a one-shot DOMContentLoaded pass.
  if (window.document$ && typeof window.document$.subscribe === 'function') {
    window.document$.subscribe(function () { mark(document); });
  } else if (document.readyState !== 'loading') {
    mark(document);
  } else {
    document.addEventListener('DOMContentLoaded', function () { mark(document); });
  }
})();
