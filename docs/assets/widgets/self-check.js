/* ============================================================
   ox-self-check  —  MCQ formative knowledge check
   ------------------------------------------------------------
   Mounts into:

     <div class="ox-self-check" data-widget="self-check"
          data-id="week-04-m1-readiness"
          data-kind="readiness"          (or "wrap-up")
          data-draw="5"                  (questions per attempt; default 5)
          data-lesson="Day 16 · Tensor Parallelism"   (optional override; falls back to <h1>)
          data-source="Reader 8"          (optional; for OxTutor nudge copy)
     >
       <script type="application/json" class="ox-self-check__pool">
       [
         {
           "stem": "What gets split across GPUs in tensor parallelism?",
           "options": [
             "LayerNorm parameters",
             "Q/K/V/output projection matrices",
             "Residual-stream activations",
             "Only the KV cache"
           ],
           "answer": 1,
           "explain": "TP splits dense weight matrices column-wise. LayerNorm and the residual stream stay replicated."
         },
         ...
       ]
       </script>
     </div>

   Behaviour
     - On hydrate: parse the JSON pool.
     - Random-draw `data-draw` questions (Fisher-Yates).
     - Shuffle option order per question; track where the correct answer landed.
     - Render N MCQ cards with radios + Submit button.
     - On submit: score deterministically, reveal explanations, lock inputs,
       show summary band (strong ≥80% / mixed 50-79% / low <50%) with
       coaching nudge + copy-able OxTutor prompt.
     - Retake → new random draw + shuffle, fresh attempt, history preserved.
     - Every attempt is appended to localStorage under
       `ox.selfcheck.<data-id>` for later wholistic assessment.
     - "Copy progress JSON" copies the full attempts payload for pasting
       into docs/progress/<module_id>.json.

   This widget never gates the lesson — the canonical end-of-week
   knowledge check is the only gate (per agents.md). This is formative.
   ============================================================ */

(function () {
  'use strict';

  // ----- storage ------------------------------------------------
  var STORAGE_VERSION = 1;

  function storageKey(id) { return 'ox.selfcheck.' + id; }

  function loadRecord(id) {
    try {
      var raw = localStorage.getItem(storageKey(id));
      if (!raw) return { version: STORAGE_VERSION, attempts: [] };
      var rec = JSON.parse(raw);
      if (!rec || rec.version !== STORAGE_VERSION || !Array.isArray(rec.attempts)) {
        return { version: STORAGE_VERSION, attempts: [] };
      }
      return rec;
    } catch (e) {
      return { version: STORAGE_VERSION, attempts: [] };
    }
  }

  function saveRecord(id, rec) {
    try {
      localStorage.setItem(storageKey(id), JSON.stringify(rec));
    } catch (e) { /* quota / private mode — ignore */ }
  }

  // ----- random utilities ---------------------------------------
  function shuffleInPlace(arr) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = arr[i]; arr[i] = arr[j]; arr[j] = tmp;
    }
    return arr;
  }

  function drawSample(pool, n) {
    var indices = pool.map(function (_, i) { return i; });
    shuffleInPlace(indices);
    return indices.slice(0, Math.min(n, indices.length));
  }

  // ----- DOM helpers --------------------------------------------
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === 'class') node.className = attrs[k];
        else if (k === 'html') node.innerHTML = attrs[k];
        else if (k === 'text') node.textContent = attrs[k];
        else if (k.indexOf('data-') === 0 || k === 'role' || k === 'aria-label') {
          node.setAttribute(k, attrs[k]);
        } else { node[k] = attrs[k]; }
      });
    }
    if (children) {
      children.forEach(function (c) {
        if (c == null) return;
        if (typeof c === 'string') node.appendChild(document.createTextNode(c));
        else node.appendChild(c);
      });
    }
    return node;
  }

  function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }

  // ----- pool parsing -------------------------------------------
  function parsePool(host) {
    var script = host.querySelector('script.ox-self-check__pool');
    if (!script) return [];
    try {
      var pool = JSON.parse(script.textContent || '[]');
      if (!Array.isArray(pool)) return [];
      // sanity-filter malformed entries
      return pool.filter(function (q) {
        return q && typeof q.stem === 'string'
          && Array.isArray(q.options) && q.options.length >= 2
          && typeof q.answer === 'number'
          && q.answer >= 0 && q.answer < q.options.length;
      });
    } catch (e) {
      console.warn('[ox-self-check] failed to parse pool for', host.dataset.id, e);
      return [];
    }
  }

  // ----- attempt state ------------------------------------------
  // For each rendered question we store:
  //   poolIdx       — original index into the pool
  //   optOrder      — permutation of option indices used at render time
  //   correctIdx    — where the correct answer lives AFTER shuffle
  //   chosenIdx     — what the learner picked (after shuffle); -1 if unanswered
  function buildAttempt(pool, drawN) {
    var sample = drawSample(pool, drawN);
    return sample.map(function (poolIdx) {
      var q = pool[poolIdx];
      var order = q.options.map(function (_, i) { return i; });
      shuffleInPlace(order);
      var correctIdx = order.indexOf(q.answer);
      return {
        poolIdx: poolIdx,
        optOrder: order,
        correctIdx: correctIdx,
        chosenIdx: -1
      };
    });
  }

  // ----- render -------------------------------------------------
  function lessonTitle(host) {
    if (host.dataset.lesson) return host.dataset.lesson;
    var h1 = document.querySelector('article h1, main h1, h1');
    return h1 ? (h1.textContent || '').trim() : 'this lesson';
  }

  function oxTutorPrompt(host, kind, band) {
    var title = lessonTitle(host);
    var source = host.dataset.source ? ' (' + host.dataset.source + ')' : '';
    if (kind === 'readiness') {
      if (band === 'low') {
        return 'Quiz me on the pre-reading for "' + title + '"' + source +
               ' — 5 fresh flash cards, one concept per card.';
      }
      return 'Re-explain the pre-reading for "' + title + '"' + source +
             ' in 3 short bullets per core concept.';
    }
    // wrap-up
    if (band === 'low') {
      return 'Quiz me on "' + title + '" — 5 fresh flash cards covering the points I missed.';
    }
    return 'Re-explain the key ideas of "' + title + '" in 3 short bullets each.';
  }

  function nudgeCopy(kind, band) {
    if (kind === 'readiness') {
      if (band === 'strong') return 'Ready — continue to the next section.';
      if (band === 'mixed') return 'Close, but not solid. Re-skim the pre-reading or ask OxTutor below, then retake.';
      return 'Not ready yet. Re-read the pre-reading and ask OxTutor below before retaking.';
    }
    // wrap-up
    if (band === 'strong') return 'Solid — you\u2019re ready for the next lesson.';
    if (band === 'mixed') return 'Revisit the Key Phrase and re-read the parts of this lesson the missed questions came from.';
    return 'Don\u2019t move on yet — re-read this lesson and ask OxTutor below before retaking.';
  }

  function band(score, total) {
    if (total === 0) return 'incomplete';
    var pct = score / total;
    if (pct >= 0.8) return 'strong';
    if (pct >= 0.5) return 'mixed';
    return 'low';
  }

  function renderQuestion(host, qState, qDisplayIdx, pool, locked) {
    var poolQ = pool[qState.poolIdx];
    var card = el('div', { class: 'ox-self-check__card' });
    card.appendChild(el('div', {
      class: 'ox-self-check__num',
      text: 'Q' + (qDisplayIdx + 1) + ' / ' + host.dataset._drawCount
    }));
    card.appendChild(el('div', {
      class: 'ox-self-check__q',
      html: poolQ.stem    // stems are author-trusted; allow inline code/em.
    }));

    var groupName = 'sc-' + host.dataset.id + '-' + qDisplayIdx;
    var optsList = el('div', { class: 'ox-self-check__opts', role: 'radiogroup' });

    qState.optOrder.forEach(function (originalOptIdx, shuffledPos) {
      var optId = groupName + '-o' + shuffledPos;
      var input = el('input', {
        type: 'radio',
        name: groupName,
        id: optId,
        class: 'ox-self-check__radio'
      });
      input.value = String(shuffledPos);
      if (locked) input.disabled = true;
      if (qState.chosenIdx === shuffledPos) input.checked = true;

      input.addEventListener('change', function () {
        qState.chosenIdx = shuffledPos;
        updateSubmitState(host);
      });

      var optClass = 'ox-self-check__opt';
      if (locked) {
        if (shuffledPos === qState.correctIdx) optClass += ' is-correct';
        else if (shuffledPos === qState.chosenIdx) optClass += ' is-wrong';
      }

      var label = el('label', {
        class: optClass,
        htmlFor: optId
      }, [
        input,
        el('span', { class: 'ox-self-check__opt-text', html: poolQ.options[originalOptIdx] })
      ]);

      if (locked) {
        var icon = '';
        if (shuffledPos === qState.correctIdx) icon = '\u2713';
        else if (shuffledPos === qState.chosenIdx) icon = '\u2717';
        if (icon) label.appendChild(el('span', { class: 'ox-self-check__opt-mark', text: icon }));
      }

      optsList.appendChild(label);
    });

    card.appendChild(optsList);

    if (locked && poolQ.explain) {
      var explainLabel = (qState.chosenIdx === qState.correctIdx) ? 'Why' : 'Why not';
      var explain = el('div', { class: 'ox-self-check__explain' }, [
        el('div', { class: 'ox-self-check__explain-label', text: explainLabel }),
        el('div', { class: 'ox-self-check__explain-body', html: poolQ.explain })
      ]);
      card.appendChild(explain);
    }

    return card;
  }

  function updateSubmitState(host) {
    var btn = host.querySelector('.ox-self-check__submit');
    if (!btn) return;
    var attempt = host._attempt;
    if (!attempt) return;
    var allAnswered = attempt.every(function (q) { return q.chosenIdx >= 0; });
    btn.disabled = !allAnswered;
    btn.textContent = allAnswered
      ? 'Submit answers'
      : ('Answer all ' + attempt.length + ' to submit');
  }

  function renderAll(host, pool) {
    var attempt = host._attempt;
    var locked = !!host._submitted;
    host.dataset._drawCount = String(attempt.length);

    var shell = el('div', { class: 'ox-self-check__shell' });

    attempt.forEach(function (qState, i) {
      shell.appendChild(renderQuestion(host, qState, i, pool, locked));
    });

    if (!locked) {
      var actions = el('div', { class: 'ox-self-check__actions' });
      var btn = el('button', {
        class: 'ox-self-check__submit',
        type: 'button'
      });
      btn.disabled = true;
      btn.textContent = 'Answer all ' + attempt.length + ' to submit';
      btn.addEventListener('click', function () { submitAttempt(host, pool); });
      actions.appendChild(btn);
      shell.appendChild(actions);
    } else {
      shell.appendChild(renderSummary(host, pool));
    }

    clear(host);
    // re-attach the pool script so later retakes/hydrates can still find it
    host.appendChild(host._poolScript);
    host.appendChild(shell);

    if (!locked) updateSubmitState(host);
  }

  function renderSummary(host, pool) {
    var attempt = host._attempt;
    var total = attempt.length;
    var score = attempt.reduce(function (s, q) {
      return s + (q.chosenIdx === q.correctIdx ? 1 : 0);
    }, 0);
    var kind = host.dataset.kind === 'wrap-up' ? 'wrap-up' : 'readiness';
    var b = band(score, total);

    var summary = el('div', { class: 'ox-self-check__summary', 'data-state': b });

    var head = el('div', { class: 'ox-self-check__score' }, [
      el('span', { class: 'ox-self-check__score-num', text: score + ' / ' + total }),
      el('span', {
        class: 'ox-self-check__score-meta',
        text: (b === 'strong' ? 'strong' : b === 'mixed' ? 'mixed' : 'needs more time')
      })
    ]);

    var retakeBtn = el('button', {
      class: 'ox-self-check__retake',
      type: 'button',
      text: 'Retake (new questions)'
    });
    retakeBtn.addEventListener('click', function () { retake(host, pool); });
    head.appendChild(retakeBtn);

    summary.appendChild(head);

    summary.appendChild(el('div', {
      class: 'ox-self-check__nudge',
      text: nudgeCopy(kind, b)
    }));

    if (b !== 'strong') {
      var prompt = oxTutorPrompt(host, kind, b);
      var promptWrap = el('div', { class: 'ox-self-check__prompt' }, [
        el('div', { class: 'ox-self-check__prompt-label', text: 'Ask OxTutor' }),
        el('code', { class: 'ox-self-check__prompt-body', text: prompt })
      ]);
      var copyBtn = el('button', {
        class: 'ox-self-check__copy',
        type: 'button',
        text: 'Copy prompt'
      });
      copyBtn.addEventListener('click', function () {
        copyText(prompt, copyBtn);
      });
      promptWrap.appendChild(copyBtn);
      summary.appendChild(promptWrap);
    }

    var rec = loadRecord(host.dataset.id);
    if (rec.attempts.length) {
      summary.appendChild(renderHistory(host, rec));
    }

    return summary;
  }

  function renderHistory(host, rec) {
    var details = el('details', { class: 'ox-self-check__history' });
    var summary = el('summary', {
      class: 'ox-self-check__history-summary',
      text: 'Attempt history (' + rec.attempts.length + ')'
    });
    details.appendChild(summary);
    var list = el('ol', { class: 'ox-self-check__history-list' });
    rec.attempts.slice().reverse().forEach(function (a) {
      var when = '';
      try { when = new Date(a.ts).toLocaleString(); } catch (e) { when = a.ts; }
      list.appendChild(el('li', {
        class: 'ox-self-check__history-item',
        text: a.score + ' / ' + a.total + '  ·  ' + when
      }));
    });
    details.appendChild(list);

    var actions = el('div', { class: 'ox-self-check__history-actions' });
    var copyJson = el('button', {
      class: 'ox-self-check__copy-json',
      type: 'button',
      text: 'Copy progress JSON'
    });
    copyJson.addEventListener('click', function () {
      copyText(JSON.stringify(rec, null, 2), copyJson);
    });
    actions.appendChild(copyJson);

    var clearBtn = el('button', {
      class: 'ox-self-check__clear',
      type: 'button',
      text: 'Clear history'
    });
    clearBtn.addEventListener('click', function () {
      if (!confirm('Clear all attempt history for this self-check?')) return;
      try { localStorage.removeItem(storageKey(host.dataset.id)); } catch (e) {}
      retake(host, host._pool);
    });
    actions.appendChild(clearBtn);
    details.appendChild(actions);

    return details;
  }

  function copyText(text, btn) {
    var original = btn.textContent;
    var done = function (ok) {
      btn.textContent = ok ? 'Copied' : 'Copy failed';
      setTimeout(function () { btn.textContent = original; }, 1400);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
    } else {
      try {
        var ta = document.createElement('textarea');
        ta.value = text; ta.setAttribute('readonly', '');
        ta.style.position = 'absolute'; ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.select(); document.execCommand('copy');
        document.body.removeChild(ta);
        done(true);
      } catch (e) { done(false); }
    }
  }

  function submitAttempt(host, pool) {
    var attempt = host._attempt;
    var total = attempt.length;
    var score = attempt.reduce(function (s, q) {
      return s + (q.chosenIdx === q.correctIdx ? 1 : 0);
    }, 0);

    var rec = loadRecord(host.dataset.id);
    rec.attempts.push({
      ts: new Date().toISOString(),
      draw: attempt.map(function (q) { return q.poolIdx; }),
      optOrder: attempt.map(function (q) { return q.optOrder.slice(); }),
      chosen: attempt.map(function (q) { return q.chosenIdx; }),
      correctIdx: attempt.map(function (q) { return q.correctIdx; }),
      score: score,
      total: total
    });
    saveRecord(host.dataset.id, rec);

    host._submitted = true;
    renderAll(host, pool);
  }

  function retake(host, pool) {
    var drawN = parseInt(host.dataset.draw || '5', 10);
    if (isNaN(drawN) || drawN < 1) drawN = 5;
    host._attempt = buildAttempt(pool, drawN);
    host._submitted = false;
    renderAll(host, pool);
  }

  // ----- hydration ----------------------------------------------
  function hydrate(host) {
    if (host.dataset.hydrated === 'true') return;
    var pool = parsePool(host);
    if (!pool.length) {
      host.dataset.hydrated = 'true';
      host.dataset.state = 'empty';
      clear(host);
      host.appendChild(el('div', {
        class: 'ox-self-check__empty',
        text: 'Self-check pool is empty.'
      }));
      return;
    }
    // detach pool script (we'll re-attach on every render so retakes survive)
    host._poolScript = host.querySelector('script.ox-self-check__pool');
    host._pool = pool;

    var drawN = parseInt(host.dataset.draw || '5', 10);
    if (isNaN(drawN) || drawN < 1) drawN = 5;
    host._attempt = buildAttempt(pool, drawN);
    host._submitted = false;
    host.dataset.hydrated = 'true';
    renderAll(host, pool);
  }

  function hydrateAll() {
    var hosts = document.querySelectorAll('.ox-self-check[data-widget="self-check"]');
    Array.prototype.forEach.call(hosts, hydrate);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrateAll);
  } else {
    hydrateAll();
  }
})();
