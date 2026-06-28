/* ============================================================
   column-toggles.js — collapse / expand for the two side
   columns (primary nav on the left, TOC on the right).
   ------------------------------------------------------------
   Injects into each visible sidebar:
     - a chevron <button class="ox-col-toggle">
     - a vertical <div class="ox-rail-label"> ("NAVIGATION" /
       "CONTENTS") — shown only while the column is collapsed
     - a <div class="ox-col-dot"> that tracks the active
       section while the column is collapsed
   Click toggles a class on <body> (ox-nav-collapsed /
   ox-toc-collapsed) — all visual chrome lives in
   stylesheets/columns.css. State is persisted per-user via
   localStorage and restored on the next page load.

   The dot uses position: fixed and is repositioned on scroll
   / resize so it always sits in the visible portion of the
   rail (the sticky sidebar's full content height can be many
   viewports tall, which would push an absolutely-positioned
   marker off-screen). It anchors against the inner edge of
   the rail (right edge of the left rail, left edge of the
   right rail) so it never sits behind the centered label.

   Bails on viewports where Material doesn't render permanent
   side columns (< 76.25em — drawer breakpoint).
   ============================================================ */
(function () {
  'use strict';

  const BREAKPOINT_PX = 76.25 * 16;
  const LS_NAV = 'ox.col.nav.collapsed';
  const LS_TOC = 'ox.col.toc.collapsed';

  const COLLAPSED = '1';
  const EXPANDED  = '0';

  const CHEVRON = {
    // Each toggle shows "what clicking will do", so a collapsed
    // column shows the open chevron and vice versa.
    nav: { expanded: '\u25C2', collapsed: '\u25B8' }, // ◂ / ▸
    toc: { expanded: '\u25B8', collapsed: '\u25C2' }, // ▸ / ◂
  };

  const LABEL = {
    nav: 'Navigation',
    toc: 'Contents',
  };

  function isDesktop() {
    return window.innerWidth >= BREAKPOINT_PX;
  }

  function sidebarFor(kind) {
    return document.querySelector(
      kind === 'nav' ? '.md-sidebar--primary' : '.md-sidebar--secondary'
    );
  }

  function bodyClassFor(kind) {
    return kind === 'nav' ? 'ox-nav-collapsed' : 'ox-toc-collapsed';
  }

  // ---- state restore ------------------------------------------

  function applyStoredState() {
    try {
      if (localStorage.getItem(LS_NAV) === COLLAPSED) {
        document.body.classList.add('ox-nav-collapsed');
      }
      if (localStorage.getItem(LS_TOC) === COLLAPSED) {
        document.body.classList.add('ox-toc-collapsed');
      }
    } catch (_) { /* private mode etc. — ignore */ }
  }

  // ---- chevron toggle -----------------------------------------

  function makeToggle(kind, sidebar) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ox-col-toggle';
    btn.setAttribute('aria-label',
      kind === 'nav'
        ? 'Toggle navigation column'
        : 'Toggle table of contents column'
    );
    refreshToggle(btn, kind);
    btn.addEventListener('click', () => {
      const cls = bodyClassFor(kind);
      const storeKey = kind === 'nav' ? LS_NAV : LS_TOC;
      const nowCollapsed = !document.body.classList.contains(cls);
      document.body.classList.toggle(cls, nowCollapsed);
      try {
        localStorage.setItem(storeKey, nowCollapsed ? COLLAPSED : EXPANDED);
      } catch (_) { /* ignore storage failures */ }
      refreshToggle(btn, kind);
      requestAnimationFrame(() => updateRailDot(kind));
    });
    sidebar.appendChild(btn);
    return btn;
  }

  function refreshToggle(btn, kind) {
    const collapsed = document.body.classList.contains(bodyClassFor(kind));
    btn.textContent = collapsed
      ? CHEVRON[kind].collapsed
      : CHEVRON[kind].expanded;
    btn.dataset.state = collapsed ? 'collapsed' : 'expanded';
    btn.title = collapsed
      ? (kind === 'nav' ? 'Expand navigation' : 'Expand contents')
      : (kind === 'nav' ? 'Collapse navigation' : 'Collapse contents');
  }

  // ---- vertical rail label ------------------------------------
  // Lives on <body> (not the sidebar) so position: fixed truly
  // anchors to the viewport — Material applies transforms on
  // ancestors which would otherwise re-anchor a fixed child.

  function getOrMakeLabel(kind) {
    const cls = 'ox-rail-label--' + kind;
    let label = document.body.querySelector('.' + cls);
    if (!label) {
      label = document.createElement('div');
      label.className = 'ox-rail-label ' + cls;
      label.textContent = LABEL[kind];
      document.body.appendChild(label);
    }
    return label;
  }

  // ---- active-position dot ------------------------------------
  // Same body-anchored trick as the label, for the same reason.

  function getOrMakeDot(kind) {
    const cls = 'ox-col-dot--' + kind;
    let dot = document.body.querySelector('.' + cls);
    if (!dot) {
      dot = document.createElement('div');
      dot.className = 'ox-col-dot ' + cls;
      document.body.appendChild(dot);
    }
    return dot;
  }

  // Left rail: which top-level item in the primary nav contains
  // the current page's active link? Returns a [0..1] ratio or
  // null when nothing can be determined.
  function computeNavActiveRatio(sidebar) {
    const list = sidebar.querySelector('.md-nav--primary > .md-nav__list');
    if (!list) return null;
    const items = Array.from(list.children)
      .filter((el) => el.classList.contains('md-nav__item'));
    if (!items.length) return null;
    const active = sidebar.querySelector('.md-nav__link--active');
    if (!active) return null;
    const idx = items.findIndex((it) => it.contains(active));
    if (idx < 0) return null;
    return (idx + 0.5) / items.length;
  }

  // Right rail: which heading is the user currently reading?
  // "Most recently scrolled past" h2/h3 in the main content.
  function computeTocActiveRatio() {
    const headings = document.querySelectorAll(
      '.md-content :is(h2, h3)[id]'
    );
    if (!headings.length) return null;
    const cutoff = window.innerHeight * 0.3;
    let activeIdx = 0;
    for (let i = 0; i < headings.length; i++) {
      const rect = headings[i].getBoundingClientRect();
      if (rect.top <= cutoff) activeIdx = i;
      else break;
    }
    return (activeIdx + 0.5) / headings.length;
  }

  function updateRailDot(kind) {
    const sidebar = sidebarFor(kind);
    if (!sidebar) return;
    if (!document.body.classList.contains(bodyClassFor(kind))) return;
    const rect = sidebar.getBoundingClientRect();

    // Derive the rail's vertical extent from the viewport, not
    // from the sidebar element: when collapsed, the sidebar's
    // own bounding box can shrink to near zero (children are
    // visibility:hidden and the absolutely-positioned toggle
    // contributes no height), which would otherwise pin the
    // label to the top of the page.
    const header = document.querySelector('.md-header');
    const tabs   = document.querySelector('.md-tabs');
    const headerH = (header ? header.getBoundingClientRect().height : 0)
                  + (tabs   ? tabs.getBoundingClientRect().height   : 0);
    const padTop = headerH + 32;
    const padBot = 24;
    const top    = padTop;
    const bottom = window.innerHeight - padBot;
    const available = Math.max(bottom - top, 0);
    const midY = top + available / 2;

    // --- vertical label: centered on the viewport-visible
    // portion of the rail.
    const label = getOrMakeLabel(kind);
    label.style.top  = midY + 'px';
    label.style.left = (rect.left + rect.width / 2) + 'px';

    // --- active-position dot
    const dot = getOrMakeDot(kind);
    const ratio = kind === 'nav'
      ? computeNavActiveRatio(sidebar)
      : computeTocActiveRatio();
    if (ratio == null) {
      dot.style.display = 'none';
      return;
    }
    // Anchor against the inner edge of the rail so it never
    // sits behind the centered vertical label.
    const innerInset = 6;
    const x = kind === 'nav'
      ? rect.right - innerInset
      : rect.left + innerInset;
    dot.style.display = '';
    dot.style.top = (top + available * ratio) + 'px';
    dot.style.left = x + 'px';
  }

  let rafPending = false;
  function scheduleRailUpdate() {
    if (rafPending) return;
    rafPending = true;
    requestAnimationFrame(() => {
      rafPending = false;
      updateRailDot('nav');
      updateRailDot('toc');
    });
  }

  // ---- mount --------------------------------------------------

  function mount() {
    if (!isDesktop()) return;
    ['nav', 'toc'].forEach((kind) => {
      const sidebar = sidebarFor(kind);
      if (!sidebar) return;
      if (!sidebar.querySelector('.ox-col-toggle')) {
        sidebar.style.position = sidebar.style.position || 'sticky';
        makeToggle(kind, sidebar);
      }
      // Re-position label / dot after the sidebar width
      // transition completes so they snap to the final rail
      // geometry rather than the mid-animation position.
      if (!sidebar.dataset.oxTransitionBound) {
        sidebar.addEventListener('transitionend', (e) => {
          if (e.propertyName === 'width') scheduleRailUpdate();
        });
        sidebar.dataset.oxTransitionBound = '1';
      }
      // Prime the label + dot DOM nodes (lives on <body>).
      getOrMakeLabel(kind);
      getOrMakeDot(kind);
    });
    scheduleRailUpdate();
  }

  applyStoredState();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
  window.addEventListener('scroll', scheduleRailUpdate, { passive: true });
  window.addEventListener('resize', scheduleRailUpdate, { passive: true });

  // Material's instant-nav can re-render the sidebar; re-mount.
  const mo = new MutationObserver(() => {
    ['nav', 'toc'].forEach((kind) => {
      const sidebar = sidebarFor(kind);
      if (sidebar && !sidebar.querySelector('.ox-col-toggle')) mount();
    });
  });
  mo.observe(document.body, { childList: true, subtree: false });
})();
