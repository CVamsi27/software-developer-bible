/* Chapter narration using the browser's speech service. */
(function (root) {
  'use strict';
  function splitText(text) {
    var rest = text.replace(/\s+/g, ' ').trim();
    var parts = [];
    while (rest.length > 240) {
      var cut = rest.lastIndexOf(' ', 240);
      if (cut < 1) cut = 240;
      parts.push(rest.slice(0, cut).trim());
      rest = rest.slice(cut).trim();
    }
    if (rest) parts.push(rest);
    return parts;
  }
  function createReader(synth, Utterance, update, onChunkStart) {
    var chunks = [], index = 0, generation = 0, state = 'idle', active = false, rate = 1;
    onChunkStart = onChunkStart || function () {};
    function emit(next) { state = next; update(next); }
    function stop() {
      generation += 1; active = false; chunks = []; index = 0;
      synth.cancel(); emit('idle');
    }
    function speakNext() {
      if (state === 'paused' || active) return;
      if (index >= chunks.length) { emit('idle'); return; }
      var token = generation;
      var chunk = chunks[index];
      var text = typeof chunk === 'string' ? chunk : chunk.text;
      var utterance = new Utterance(text);
      utterance.rate = rate;
      utterance.lang = 'en-US';
      active = true;
      utterance.onstart = function () {
        if (token === generation) onChunkStart(typeof chunk === 'string' ? null : chunk.element, index);
      };
      utterance.onend = function () {
        if (token !== generation) return;
        active = false; index += 1; speakNext();
      };
      utterance.onerror = function () {
        if (token !== generation) return;
        generation += 1; active = false; synth.cancel(); emit('error');
      };
      // Retain the current utterance until completion on browsers that require it.
      reader.utterance = utterance;
      try { synth.speak(utterance); } catch (_) { utterance.onerror(); }
    }
    var reader = {
      start: function (parts) {
        stop(); chunks = parts;
        if (!chunks.length) { emit('empty'); return; }
        synth.resume(); emit('reading'); speakNext();
      },
      stop: stop,
      togglePause: function () {
        if (state === 'reading') { emit('paused'); synth.pause(); }
        else if (state === 'paused') { emit('reading'); synth.resume(); speakNext(); }
      },
      setRate: function (value) { rate = Math.max(0.5, Math.min(2, Number(value) || 1)); }
    };
    return reader;
  }
  function extractChapter(content) {
    var excluded = 'pre, script, style, nav, button, img, svg, [hidden], [aria-hidden="true"], .read-aloud, .chapter-outline, .heading-anchor, .chapter-nav-footer';
    var NodeFilter = content.ownerDocument.defaultView.NodeFilter;
    var walker = content.ownerDocument.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent || !node.textContent.trim() || parent.closest(excluded)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var groups = [], previous = null, text = '';
    function save() {
      if (text.trim()) {
        splitText(text).forEach(function (part) { groups.push({text: part, element: previous}); });
      }
    }
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var block = node.parentElement.closest('h1,h2,h3,h4,h5,h6,p,li,td,th,blockquote');
      if (!block || !content.contains(block)) continue;
      if (previous !== block) {
        save();
        text = ''; previous = block;
      }
      text += node.textContent;
    }
    save();
    return groups;
  }
  function mount() {
    var content = document.querySelector('.post-content');
    if (!content || content.querySelector('.read-aloud')) return;
    var bar = document.createElement('section');
    bar.className = 'read-aloud'; bar.setAttribute('aria-label', 'Chapter read aloud');
    bar.innerHTML = '<span class="read-aloud-status" role="status" aria-live="polite">Read along at your own pace</span><div class="read-aloud-controls"><button type="button" data-read aria-label="Read aloud">Read</button><button type="button" data-pause aria-label="Pause" hidden>Pause</button><button type="button" data-stop aria-label="Stop" hidden>Stop</button><select aria-label="Reading speed"><option value="0.5">0.5×</option><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></div>';
    var title = content.querySelector('h1');
    if (title && title.parentElement === content) {
      var row = document.createElement('div');
      row.className = 'chapter-title-row';
      title.before(row);
      row.append(title, bar);
    } else if (title) title.after(bar);
    else content.prepend(bar);
    var play = bar.querySelector('[data-read]'), pause = bar.querySelector('[data-pause]'), stop = bar.querySelector('[data-stop]'), status = bar.querySelector('[role="status"]');
    if (!root.speechSynthesis || !root.SpeechSynthesisUtterance) {
      play.disabled = true; bar.querySelector('select').disabled = true;
      status.textContent = 'Read aloud is unavailable in this browser.'; return;
    }
    var activeElement = null;
    function clearActive() {
      if (activeElement) activeElement.removeAttribute('data-read-aloud-active');
      activeElement = null;
    }
    function follow(element) {
      if (!element || !content.contains(element)) { clearActive(); return; }
      if (activeElement !== element) clearActive();
      activeElement = element;
      element.setAttribute('data-read-aloud-active', 'true');
      var rect = element.getBoundingClientRect();
      var topMargin = 120;
      var bottomMargin = Math.min(120, root.innerHeight * 0.15);
      if (rect.top < topMargin || rect.bottom > root.innerHeight - bottomMargin) {
        var reduced = root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches;
        element.scrollIntoView({block: 'start', behavior: reduced ? 'auto' : 'smooth'});
      }
    }
    var reader = createReader(root.speechSynthesis, root.SpeechSynthesisUtterance, function (state) {
      var busy = state === 'reading' || state === 'paused';
      if (!busy) clearActive();
      var moveFocus = busy ? document.activeElement === play : document.activeElement === pause || document.activeElement === stop;
      bar.dataset.state = state;
      play.hidden = busy; pause.hidden = !busy; stop.hidden = !busy;
      pause.disabled = !busy; stop.disabled = !busy;
      if (moveFocus) (busy ? pause : play).focus();
      pause.textContent = state === 'paused' ? 'Resume' : 'Pause';
      pause.setAttribute('aria-label', state === 'paused' ? 'Resume' : 'Pause');
      status.textContent = ({idle: 'Read along at your own pace', reading: 'Reading chapter', paused: 'Paused', error: 'Speech could not play. Try again or choose another browser.', empty: 'No readable chapter text.'})[state];
    }, follow);
    play.addEventListener('click', function () { reader.start(extractChapter(content)); });
    pause.addEventListener('click', reader.togglePause);
    stop.addEventListener('click', reader.stop);
    bar.querySelector('select').addEventListener('change', function (event) { reader.setRate(event.target.value); });
    root.addEventListener('pagehide', reader.stop);
    root.addEventListener('beforeunload', reader.stop);
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {splitText: splitText, createReader: createReader};
  else {
    root.SDBReadAloud = {extractChapter: extractChapter};
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
    else mount();
  }
})(typeof window !== 'undefined' ? window : globalThis);
