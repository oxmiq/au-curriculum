// ============================================================
// Glossary flipbook — vanilla JS, no framework.
// Loaded globally via extra_javascript; the IIFE early-returns
// on any page that lacks #book so it's safe everywhere.
// Search-mode toggling is scoped to the .glossary-page wrapper
// rather than document.body for the same reason.
// ============================================================

(async function () {
  if (!document.getElementById('book')) return;

  // ---------- constants ----------
  const ALL_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const PHASE_LABELS = {
    foundations: 'Foundations', inference: 'Inference', prompting: 'Prompting',
    agents: 'Agents', capsule: 'Capsule', capstone: 'Capstone'
  };
  // Pagination tunables. These used to be hard-coded for a 620×960 book
  // with 44px padding; the layout has since grown to 820×1280 / 56px
  // padding, so we derive them from the live DOM each time we paginate
  // (see paginateTerms / buildContentSpreads below).
  const PAGE_PADDING_PX = 56;   // matches .term-page padding in glossary.css
  const PAGE_HEAD_PX    = 70;   // .term-page .head (h2 + bottom-border + margin)
  const PAGE_FOOT_PX    = 36;   // .term-page .foot (text + top-border + padding)
  const PAGE_GUTTER_PX  = 4;    // safety so the last card never clips the foot rule

  const FALLBACK_FACTS = [
    { text: 'GPT-3 was 175B parameters; LLaMA 3 8B punches well above that weight class thanks to better data and training recipes.', tag: 'LLM history' },
    { text: 'NVIDIA H100 ships with 80GB of HBM3 and ~3.35 TB/s of memory bandwidth — the bottleneck most inference workloads run into.', tag: 'GPU' },
    { text: 'FlashAttention turned attention from O(N²) memory to O(N) IO without changing the math — a rare free lunch.', tag: 'Inference' }
  ];

  // ---------- state ----------
  let TERMS = [];
  let FACTS = FALLBACK_FACTS;
  let CONTENT_SPREADS = [];     // canonical spreads when not searching
  let SPREADS = [];             // active spreads (= CONTENT_SPREADS, or search-mode spreads)
  let TERM_TO_SPREAD = {};      // slug -> spread index in CONTENT_SPREADS
  let LETTER_TO_SPREAD = {};    // letter -> first spread index in CONTENT_SPREADS
  let current = 0;
  let isFlipping = false;
  let inSearch = false;
  let lastBookWidth = 0;

  const $  = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));

  // ---------- helpers ----------
  function escapeHTML(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, c => (
      { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
    ));
  }
  function debounce(fn, ms) {
    let t;
    return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
  }
  function firstLetter(term) {
    const cleaned = (term || '').replace(/^[`*_'"(\[\s]+/, '');
    const c = (cleaned[0] || '').toUpperCase();
    return /[A-Z]/.test(c) ? c : '?';
  }
  function termLabel(slug) {
    const t = TERMS.find(x => x.slug === slug);
    return t ? t.term : slug;
  }
  function pickFact(letter) {
    if (!FACTS.length) return { text: '', tag: '' };
    const seed = ((letter.charCodeAt(0) - 65) * 13 + 7) % FACTS.length;
    const f = FACTS[seed];
    return { text: f.text || '', tag: f.tag || f.category || '' };
  }

  // ---------- card / page renderers ----------
  function renderTermCard(t) {
    const seeAlso = (t.see_also || []).map(s =>
      `<a href="?term=${encodeURIComponent(s)}" data-term="${escapeHTML(s)}">${escapeHTML(termLabel(s))}</a>`
    ).join('');
    const meta = seeAlso ? `<div class="meta">${seeAlso}</div>` : '';
    const ptag = PHASE_LABELS[t.phase] || t.phase || '';
    return (
      `<div class="term" data-phase="${escapeHTML(t.phase || '')}">
         <h3>${escapeHTML(t.term)}</h3>
         <span class="ptag">${escapeHTML(ptag)}</span>
         <p class="def">${escapeHTML(t.definition)}</p>
         ${meta}
       </div>`
    );
  }

  function renderCoverPage() {
    const total = TERMS.length;
    const letters = Object.keys(LETTER_TO_SPREAD).length;
    return `<div class="cover-page">
      <div class="cover-eyebrow">Oxmiq — AU Internship</div>
      <h1 class="cover-title">Glossary</h1>
      <p class="cover-sub">A book of terms — across foundations, inference, prompting, agents, and Capsule.</p>
      <div class="cover-stats">
        ${total} terms<br>
        ${letters} of 26 letters<br>
        — A telephone directory of ideas —
      </div>
      <div class="cover-cta">▸ Click cover to open</div>
    </div>`;
  }

  function renderBackPage() {
    const total = TERMS.length;
    const contentPages = CONTENT_SPREADS.reduce((n, s) => {
      if (s.left && s.left.kind !== 'cover' && s.left.kind !== 'back' && s.left.kind !== 'blank') n++;
      if (s.right && s.right.kind !== 'cover' && s.right.kind !== 'back' && s.right.kind !== 'blank') n++;
      return n;
    }, 0);
    return `<div class="back-page">
      <div class="cover-eyebrow">— Fin —</div>
      <h1 class="cover-title">The End</h1>
      <p class="cover-sub">You've reached the back of the book.</p>
      <div class="cover-stats">
        ${total} terms · ${contentPages} pages<br>
        Built from five source glossaries:<br>
        Inference Engineering · Prompt Engineering<br>
        AI Agents · Capsule Power User · Flashcards
      </div>
      <div class="cover-cta">‹ Flip back to begin</div>
    </div>`;
  }

  function renderDropCapPage(page) {
    const L = page.letter;
    const fact = pickFact(L);
    return `<div class="drop-cap-page">
      <div class="drop">${L}</div>
      <div class="count">${page.totalTerms} term${page.totalTerms === 1 ? '' : 's'} starting with ${L}</div>
      <div class="divider"></div>
      <p class="fact">${escapeHTML(fact.text)}</p>
      <div><span class="fact-tag">${escapeHTML(fact.tag)}</span></div>
      <div class="foot">— Glossary —</div>
    </div>`;
  }

  function renderTermPage(page) {
    // Header just shows the letter (the bottom-bar position handles spread N/M).
    // For continuation pages (chunks after the first) a small "cont." tag sits
    // next to the letter so the reader knows the section is still A, even on
    // a left page that lacks the drop-cap.
    const cont = page.part > 1
      ? ` <span style="font-weight:400;color:var(--book-ink-soft);font-size:12px;font-family:var(--mono);letter-spacing:.1em;text-transform:lowercase;">cont.</span>`
      : '';
    const pageno = page.part === 1
      ? `${page.terms.length} term${page.terms.length === 1 ? '' : 's'} on this page`
      : '';
    const header = `<div class="head"><h2>${page.letter}${cont}</h2><span class="pageno">${pageno}</span></div>`;
    return `<div class="term-page">
      ${header}
      ${page.terms.map(renderTermCard).join('')}
      <div class="foot">— ${page.letter} —</div>
    </div>`;
  }

  function renderBlankPage(page) {
    return `<div class="blank-page">
      <div class="ornament">❦</div>
      <div class="ornament-sub">end of ${escapeHTML(page.letter || '')}</div>
    </div>`;
  }

  function renderSearchListPage(page) {
    // page.hits is an array of all matches; we paginate the LINK LIST itself
    // into one or more pages identical-format-wise to other left pages, so
    // even very long result sets fit without scrolling.
    const list = page.hits.map((t, i) => {
      const num = (page.startIndex + i + 1).toString().padStart(2, '0');
      const ptag = PHASE_LABELS[t.phase] || t.phase || '';
      return `<li><a class="hit" data-term="${escapeHTML(t.slug)}" data-phase="${escapeHTML(t.phase || '')}" href="?term=${encodeURIComponent(t.slug)}">
        <span class="num">${num}.</span>
        <span class="name">${escapeHTML(t.term)}</span>
        <span class="phase">${escapeHTML(ptag)}</span>
      </a></li>`;
    }).join('');
    return `<div class="search-list-page">
      <div class="head">
        <div class="label">Search results</div>
        <h2 class="q">"${escapeHTML(page.query)}"</h2>
        <div class="count">${page.totalCount} match${page.totalCount === 1 ? '' : 'es'} · click a term to jump to its page</div>
      </div>
      <ol>${list}</ol>
      <div class="foot">List · page ${page.part} of ${page.totalParts}</div>
    </div>`;
  }

  function renderPage(page) {
    if (!page) return '';
    switch (page.kind) {
      case 'cover':       return renderCoverPage();
      case 'back':        return renderBackPage();
      case 'drop-cap':    return renderDropCapPage(page);
      case 'terms':       return renderTermPage(page);
      case 'blank':       return renderBlankPage(page);
      case 'search-list': return renderSearchListPage(page);
      case 'search-terms':return renderTermPage(page); // same look as a normal term page
      default:            return '';
    }
  }

  // ---------- pagination ----------
  function pageUsableHeight() {
    const book = $('#book');
    const bookH = (book && book.getBoundingClientRect().height) || 820;
    return bookH - (PAGE_PADDING_PX * 2) - PAGE_HEAD_PX - PAGE_FOOT_PX - PAGE_GUTTER_PX;
  }

  function paginateTerms(terms, measureWidth, usablePx) {
    const limit = usablePx || pageUsableHeight();
    const measure = $('#measure');
    measure.style.width = measureWidth + 'px';
    measure.innerHTML = terms.map(renderTermCard).join('');
    const cards = Array.from(measure.children);
    const chunks = [];
    let start = 0, h = 0;
    for (let i = 0; i < cards.length; i++) {
      const hi = cards[i].getBoundingClientRect().height + 14; // 14 = .term margin-bottom
      if (h + hi > limit && i > start) {
        chunks.push(terms.slice(start, i));
        start = i; h = hi;
      } else {
        h += hi;
      }
    }
    if (start < terms.length) chunks.push(terms.slice(start));
    measure.innerHTML = '';
    return chunks;
  }

  // Build pages then group into spreads. Rules:
  //   - Cover is page 0 (right side of spread 0; left of spread 0 is null/hidden).
  //   - For each letter (alphabetical order):
  //       drop-cap page → left of a fresh spread
  //       chunk-1 → right of that same spread
  //       chunk-2 → left of next spread, chunk-3 → right, ...
  //       if leftover odd, add a blank page so next letter starts on a left.
  //   - Back is the last page (left side of final spread; right is null/hidden).
  function buildContentSpreads(terms) {
    const byLetter = {};
    for (const t of terms) {
      const L = firstLetter(t.term);
      if (!ALL_LETTERS.includes(L)) continue;
      (byLetter[L] = byLetter[L] || []).push(t);
    }
    for (const L of Object.keys(byLetter)) {
      byLetter[L].sort((a, b) => {
        const an = (a.term || '').replace(/^[`*_'"(\[\s]+/, '').toLowerCase();
        const bn = (b.term || '').replace(/^[`*_'"(\[\s]+/, '').toLowerCase();
        return an.localeCompare(bn);
      });
    }

    const bookWidth = $('#book').getBoundingClientRect().width || 960;
    const pageWidth = bookWidth / 2;
    const measureWidth = pageWidth - PAGE_PADDING_PX * 2;

    // Build flat page list first.
    const pages = [];

    // Cover spread: pages[0] is the right-of-spread-0 placeholder; left of
    // spread 0 is intentionally null (book is closed).
    // We model spreads explicitly rather than via the page array index because
    // of the cover/back asymmetry.

    const spreads = [{ kind: 'cover', left: null, right: { kind: 'cover' } }];

    LETTER_TO_SPREAD = {};
    TERM_TO_SPREAD = {};

    for (const L of ALL_LETTERS) {
      const list = byLetter[L];
      if (!list || !list.length) continue;
      const chunks = paginateTerms(list, measureWidth);
      // total pages for this letter = drop-cap(1) + chunks.length terms-pages
      const dropCap = {
        kind: 'drop-cap',
        letter: L,
        totalTerms: list.length
      };
      const termsPages = chunks.map((c, i) => ({
        kind: 'terms',
        letter: L,
        terms: c,
        part: i + 1,
        totalParts: chunks.length
      }));

      const firstSpreadIdx = spreads.length;
      LETTER_TO_SPREAD[L] = firstSpreadIdx;
      // First spread of letter: LEFT = drop-cap, RIGHT = chunk-1.
      spreads.push({
        kind: 'content',
        letter: L,
        left: dropCap,
        right: termsPages[0] || null
      });
      // Record where each term lives.
      if (termsPages[0]) {
        for (const t of termsPages[0].terms) TERM_TO_SPREAD[t.slug] = firstSpreadIdx;
      }
      // Subsequent term pages flow into LEFT/RIGHT pairs.
      let rest = termsPages.slice(1);
      while (rest.length) {
        const leftPage = rest.shift();
        const rightPage = rest.shift() || null;
        const sIdx = spreads.length;
        spreads.push({
          kind: 'content',
          letter: L,
          left: leftPage,
          right: rightPage
        });
        if (leftPage)  for (const t of leftPage.terms)  TERM_TO_SPREAD[t.slug] = sIdx;
        if (rightPage) for (const t of rightPage.terms) TERM_TO_SPREAD[t.slug] = sIdx;
      }
      // If the last spread's RIGHT is null (odd number of term pages after
      // the drop-cap), fill with a blank end-of-section page so the next
      // letter still begins on a LEFT page.
      const last = spreads[spreads.length - 1];
      if (last.kind === 'content' && last.right === null) {
        last.right = { kind: 'blank', letter: L };
      }
    }

    spreads.push({ kind: 'back', left: { kind: 'back' }, right: null });
    return spreads;
  }

  // ---------- main render ----------
  function renderSpread(idx) {
    const spread = SPREADS[idx];
    const book = $('#book');
    const left = $('#leftPage');
    const right = $('#rightPage');

    book.classList.remove('closed-cover', 'closed-back');
    if (spread.kind === 'cover') {
      book.classList.add('closed-cover');
      left.innerHTML = '';
      right.innerHTML = renderPage(spread.right);
    } else if (spread.kind === 'back') {
      book.classList.add('closed-back');
      left.innerHTML = renderPage(spread.left);
      right.innerHTML = '';
    } else {
      left.innerHTML  = renderPage(spread.left);
      right.innerHTML = renderPage(spread.right);
    }

    // Active tab (track current letter)
    $$('.tab').forEach(t => t.classList.remove('active'));
    const L = currentLetter(spread);
    if (L) {
      const tab = document.querySelector(`.tab[data-letter="${L}"]`);
      if (tab) tab.classList.add('active');
    }

    left.classList.toggle('flippable',  idx > 0);
    right.classList.toggle('flippable', idx < SPREADS.length - 1);
  }

  function currentLetter(spread) {
    if (!spread) return null;
    if (spread.left && spread.left.letter)  return spread.left.letter;
    if (spread.right && spread.right.letter) return spread.right.letter;
    return null;
  }

  function updateControls() {
    const spread = SPREADS[current];
    $('#prevBtn').disabled = current === 0;
    $('#nextBtn').disabled = current === SPREADS.length - 1;
    let label;
    if (spread.kind === 'cover')          label = 'Cover';
    else if (spread.kind === 'back')      label = 'The End';
    else if (spread.kind === 'search-results') {
      label = spread.totalParts > 1
        ? `Search · ${spread.part}/${spread.totalParts}`
        : `Search · ${spread.totalCount || 0} match${spread.totalCount === 1 ? '' : 'es'}`;
    } else {
      // content spread — compute letter + spread index within that letter
      const L = currentLetter(spread);
      if (L) {
        // count how many spreads belong to this letter and which index we're at
        const start = LETTER_TO_SPREAD[L];
        let end = SPREADS.length - 1;
        for (let i = start + 1; i < SPREADS.length; i++) {
          const s = SPREADS[i];
          if (currentLetter(s) !== L) { end = i - 1; break; }
        }
        const total = end - start + 1;
        const idxIn = current - start + 1;
        label = total > 1 ? `${L} · ${idxIn}/${total}` : L;
      } else {
        label = `${current + 1} / ${SPREADS.length}`;
      }
    }
    $('#pos').textContent = label;
  }

  function pushHistory() {
    const spread = SPREADS[current];
    let url = location.pathname;
    if (spread.kind !== 'cover' && spread.kind !== 'back' && spread.kind !== 'search-results') {
      const L = currentLetter(spread);
      if (L) url += `?letter=${L}`;
    }
    history.replaceState(null, '', url);
  }

  // ---------- flip animation ----------
  function flip(direction, targetIdxOverride) {
    if (isFlipping) return;
    const target = targetIdxOverride !== undefined
      ? targetIdxOverride
      : (direction === 'fwd' ? current + 1 : current - 1);
    if (target < 0 || target >= SPREADS.length || target === current) return;

    isFlipping = true;
    const book = $('#book');
    const currentSpread = SPREADS[current];
    const nextSpread = SPREADS[target];

    // 1) Drop closed-* classes for the duration of the flip so both halves
    //    of the book are visible while the page actually turns.
    const wasClosedCover = book.classList.contains('closed-cover');
    const wasClosedBack  = book.classList.contains('closed-back');
    book.classList.remove('closed-cover', 'closed-back');

    // Make sure the underlying page (the one NOT being flipped) holds the
    // correct destination content so it shows after the flipper rotates.
    const left  = $('#leftPage');
    const right = $('#rightPage');
    if (direction === 'fwd') {
      // Right page is the one turning; the underlying right will show next.right.
      right.innerHTML = renderPage(nextSpread.right);
      // The left page should show what the user came from until the flipper
      // settles; at cleanup we update it to nextSpread.left.
      if (wasClosedCover) {
        // We were at cover (left was hidden). Reveal a blank parchment now
        // so the flipper has something to rotate against — actually we
        // want the cover's "inside" face. Just show the current left content
        // (which was empty) — that's fine; the flipper covers the right half.
        left.innerHTML = '';
      }
    } else {
      // Left page is turning; the underlying left will show next.left.
      left.innerHTML = renderPage(nextSpread.left);
      if (wasClosedBack) right.innerHTML = '';
    }

    const flipper = document.createElement('div');
    flipper.className = `flipper ${direction}`;
    const front = document.createElement('div');
    front.className = 'flip-face front';
    const back = document.createElement('div');
    back.className = 'flip-face back';

    if (direction === 'fwd') {
      // Page turning is the RIGHT page. Front face = what was on the right;
      // back face = the new left page that's revealed.
      front.innerHTML = renderPage(currentSpread.right);
      back.innerHTML  = renderPage(nextSpread.left);
    } else {
      // Page turning is the LEFT page. Front face = what was on the left;
      // back face = the new right page that's revealed.
      front.innerHTML = renderPage(currentSpread.left);
      back.innerHTML  = renderPage(nextSpread.right);
    }

    flipper.appendChild(front);
    flipper.appendChild(back);
    book.appendChild(flipper);

    void flipper.offsetWidth;
    requestAnimationFrame(() => flipper.classList.add('go'));

    const cleanup = () => {
      current = target;
      // Final paint
      if (direction === 'fwd') {
        left.innerHTML = renderPage(nextSpread.left);
      } else {
        right.innerHTML = renderPage(nextSpread.right);
      }
      // Re-apply closed state for cover/back
      book.classList.remove('closed-cover', 'closed-back');
      if (nextSpread.kind === 'cover') {
        book.classList.add('closed-cover');
        left.innerHTML = '';
      } else if (nextSpread.kind === 'back') {
        book.classList.add('closed-back');
        right.innerHTML = '';
      }
      if (flipper.parentNode) flipper.parentNode.removeChild(flipper);

      // Re-apply flippable cursors + active tab
      $$('.tab').forEach(t => t.classList.remove('active'));
      const L = currentLetter(nextSpread);
      if (L) {
        const tab = document.querySelector(`.tab[data-letter="${L}"]`);
        if (tab) tab.classList.add('active');
      }
      left.classList.toggle('flippable',  current > 0);
      right.classList.toggle('flippable', current < SPREADS.length - 1);
      isFlipping = false;
      updateControls();
      pushHistory();
    };

    flipper.addEventListener('transitionend', (e) => {
      if (e.propertyName !== 'transform') return;
      cleanup();
    }, { once: true });

    // Safety in case transitionend doesn't fire (page hidden, etc.)
    setTimeout(() => { if (isFlipping) cleanup(); }, 1300);
  }

  function jumpToSpread(idx) {
    if (idx === current || isFlipping) return;
    flip(idx > current ? 'fwd' : 'bwd', idx);
  }

  function jumpToLetter(L) {
    const idx = LETTER_TO_SPREAD[L];
    if (idx === undefined) return;
    jumpToSpread(idx);
  }

  function openToTerm(slug) {
    if (inSearch) clearSearch();
    const idx = TERM_TO_SPREAD[slug];
    if (idx === undefined) return;
    jumpToSpread(idx);
  }

  // ---------- tabs ----------
  function renderTabs() {
    const tabsEl = $('#tabs');
    tabsEl.innerHTML = ALL_LETTERS.map(L => {
      const hasContent = LETTER_TO_SPREAD[L] !== undefined;
      return `<button class="tab ${hasContent ? '' : 'empty'}" data-letter="${L}"
                ${hasContent ? '' : 'disabled'} aria-label="Letter ${L}">${L}</button>`;
    }).join('');
  }

  // ---------- search ----------
  function runSearch(query) {
    const q = query.toLowerCase();
    const matches = TERMS.filter(t =>
      (t.term && t.term.toLowerCase().includes(q)) ||
      (t.definition && t.definition.toLowerCase().includes(q))
    );

    const bookWidth = $('#book').getBoundingClientRect().width || 960;
    const measureWidth = (bookWidth / 2) - PAGE_PADDING_PX * 2;

    if (!matches.length) {
      const noResult = [{
        kind: 'search-results',
        query, totalCount: 0, part: 1, totalParts: 1,
        left: { kind: 'search-list', query, hits: [], totalCount: 0, startIndex: 0, part: 1, totalParts: 1 },
        right: { kind: 'blank', letter: '' }
      }];
      SPREADS = noResult;
      current = 0;
      inSearch = true;
      document.querySelector('.glossary-page').classList.add('search-mode');
      renderSpread(0);
      updateControls();
      return;
    }

    // Paginate the TERM CARDS first (right side, density-bound).
    const cardChunks = paginateTerms(matches, measureWidth);
    // The LINK LIST on the left mirrors the card chunks 1:1 so every spread
    // shows the same slice of hits on both sides — left page always lists
    // exactly the terms whose cards appear on the facing right page.
    const total = cardChunks.length;
    let startIndex = 0;
    const spreads = [];
    for (let i = 0; i < total; i++) {
      const chunk = cardChunks[i];
      const leftPage = {
        kind: 'search-list',
        query,
        hits: chunk,
        totalCount: matches.length,
        startIndex,
        part: i + 1,
        totalParts: total
      };
      const rightPage = {
        kind: 'search-terms',
        letter: 'Results',
        terms: chunk,
        part: i + 1,
        totalParts: total
      };
      startIndex += chunk.length;
      spreads.push({
        kind: 'search-results',
        query,
        totalCount: matches.length,
        part: i + 1,
        totalParts: total,
        left: leftPage,
        right: rightPage
      });
    }

    inSearch = true;
    document.querySelector('.glossary-page').classList.add('search-mode');
    SPREADS = spreads;
    current = 0;
    renderSpread(0);
    updateControls();
  }

  function clearSearch() {
    if (!inSearch) return;
    inSearch = false;
    document.querySelector('.glossary-page').classList.remove('search-mode');
    $('#search').value = '';
    SPREADS = CONTENT_SPREADS;
    current = 0;
    renderSpread(0);
    updateControls();
  }

  // ---------- event wiring ----------
  function wireEvents() {
    $('#prevBtn').addEventListener('click', () => flip('bwd'));
    $('#nextBtn').addEventListener('click', () => flip('fwd'));

    $('#leftPage').addEventListener('click', (e) => {
      if (e.target.closest('a, button')) return;
      if (current > 0) flip('bwd');
    });
    $('#rightPage').addEventListener('click', (e) => {
      if (e.target.closest('a, button')) return;
      if (current < SPREADS.length - 1) flip('fwd');
    });

    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        if (e.key === 'Escape' && inSearch) {
          e.preventDefault();
          clearSearch();
        }
        return;
      }
      if (e.key === 'ArrowLeft')  { e.preventDefault(); flip('bwd'); }
      if (e.key === 'ArrowRight') { e.preventDefault(); flip('fwd'); }
      if (e.key === 'Home')       { e.preventDefault(); jumpToSpread(0); }
      if (e.key === 'End')        { e.preventDefault(); jumpToSpread(SPREADS.length - 1); }
      if (e.key === 'Escape' && inSearch) { clearSearch(); }
    });

    $('#tabs').addEventListener('click', (e) => {
      const t = e.target.closest('.tab');
      if (t && !t.disabled) {
        if (inSearch) clearSearch();
        jumpToLetter(t.dataset.letter);
      }
    });

    $('#search').addEventListener('input', debounce((e) => {
      const q = e.target.value.trim();
      if (q.length >= 2) runSearch(q);
      else if (inSearch) clearSearch();
    }, 220));

    // Term-jump link delegation (works for both search-list hits and
    // see-also references inside term cards).
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[data-term]');
      if (!a) return;
      e.preventDefault();
      e.stopPropagation();
      openToTerm(a.dataset.term);
    });

    window.addEventListener('resize', debounce(() => {
      const newWidth = $('#book').getBoundingClientRect().width;
      if (Math.abs(newWidth - lastBookWidth) < 8) return;
      lastBookWidth = newWidth;
      const wasLetter = currentLetter(SPREADS[current]);
      const wasSearch = inSearch;
      const searchQuery = wasSearch ? $('#search').value : null;
      CONTENT_SPREADS = buildContentSpreads(TERMS);
      if (wasSearch && searchQuery) {
        runSearch(searchQuery);
      } else {
        SPREADS = CONTENT_SPREADS;
        if (wasLetter && LETTER_TO_SPREAD[wasLetter] !== undefined) {
          current = LETTER_TO_SPREAD[wasLetter];
        } else {
          current = Math.min(current, SPREADS.length - 1);
        }
        renderSpread(current);
        updateControls();
      }
    }, 250));
  }

  // ---------- init ----------
  async function init() {
    // Both data files live alongside the old kb/glossary.html, which is
    // kb/glossary.json and kb/facts.json. With Material's use_directory_urls
    // this page is served at kb/glossary/, so we go up one level.
    try {
      const r = await fetch('../glossary.json', { cache: 'no-cache' });
      const d = await r.json();
      TERMS = d.terms || [];
    } catch (e) {
      console.error('Failed to load glossary.json', e);
      TERMS = [];
    }
    try {
      const r = await fetch('../facts.json', { cache: 'no-cache' });
      const d = await r.json();
      FACTS = (d.facts && d.facts.length) ? d.facts : FALLBACK_FACTS;
    } catch (e) {
      FACTS = FALLBACK_FACTS;
    }

    CONTENT_SPREADS = buildContentSpreads(TERMS);
    SPREADS = CONTENT_SPREADS;
    lastBookWidth = $('#book').getBoundingClientRect().width;

    renderTabs();
    renderSpread(0);
    updateControls();
    wireEvents();

    const params = new URLSearchParams(location.search);
    if (params.get('term')) {
      setTimeout(() => openToTerm(params.get('term')), 100);
    } else if (params.get('letter')) {
      const L = params.get('letter').toUpperCase();
      setTimeout(() => jumpToLetter(L), 100);
    }
  }

  // Wait for layout to settle so we measure cards at the real page width.
  requestAnimationFrame(() =>
    requestAnimationFrame(() =>
      init().catch(e => console.error('Glossary init failed:', e))
    )
  );
})();
