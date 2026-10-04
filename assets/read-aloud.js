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
  function createReader(synth, Utterance, update) {
    var chunks = [], index = 0, generation = 0, state = 'idle', active = false, rate = 1;
    function emit(next) { state = next; update(next); }
    function stop() {
      generation += 1; active = false; chunks = []; index = 0;
      synth.cancel(); emit('idle');
    }
    function speakNext() {
      if (state === 'paused' || active) return;
      if (index >= chunks.length) { emit('idle'); return; }
      var token = generation;
      var utterance = new Utterance(chunks[index]);
      utterance.rate = rate;
      utterance.lang = 'en-US';
      active = true;
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
    var copy = content.cloneNode(true);
    copy.querySelectorAll('pre, script, style, nav, button, img, svg, [hidden], [aria-hidden="true"], .read-aloud, .heading-anchor, .chapter-nav-footer').forEach(function (node) { node.remove(); });
    var walker = content.ownerDocument.createTreeWalker(copy, 4);
    var groups = [], previous = null, text = '';
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var block = node.parentElement.closest('h1,h2,h3,h4,h5,h6,p,li,td,th,blockquote');
      if (!block || !node.textContent.trim()) continue;
      if (previous !== block) {
        if (text.trim()) groups.push(text.trim());
        text = ''; previous = block;
      }
      text += node.textContent;
    }
    if (text.trim()) groups.push(text.trim());
    return groups.flatMap(splitText);
  }
  function mount() {
    var content = document.querySelector('.post-content');
    if (!content || content.querySelector('.read-aloud')) return;
    var bar = document.createElement('section');
    bar.className = 'read-aloud'; bar.setAttribute('aria-label', 'Chapter read aloud');
    bar.innerHTML = '<div class="read-aloud-copy"><span class="read-aloud-title">Listen to this chapter</span><span role="status" aria-live="polite">Read along at your own pace</span></div><div class="read-aloud-controls"><button type="button" data-read>Read aloud</button><button type="button" data-pause hidden>Pause</button><button type="button" data-stop hidden>Stop</button><label class="read-aloud-speed">Speed <select aria-label="Reading speed"><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label></div>';
    var title = content.querySelector('h1');
    if (title) title.after(bar); else content.prepend(bar);
    var play = bar.querySelector('[data-read]'), pause = bar.querySelector('[data-pause]'), stop = bar.querySelector('[data-stop]'), status = bar.querySelector('[role="status"]');
    if (!root.speechSynthesis || !root.SpeechSynthesisUtterance) {
      play.disabled = true; bar.querySelector('select').disabled = true;
      status.textContent = 'Read aloud is unavailable in this browser.'; return;
    }
    var reader = createReader(root.speechSynthesis, root.SpeechSynthesisUtterance, function (state) {
      var busy = state === 'reading' || state === 'paused';
      var moveFocus = busy ? document.activeElement === play : document.activeElement === pause || document.activeElement === stop;
      bar.dataset.state = state;
      play.hidden = busy; pause.hidden = !busy; stop.hidden = !busy;
      pause.disabled = !busy; stop.disabled = !busy;
      if (moveFocus) (busy ? pause : play).focus();
      pause.textContent = state === 'paused' ? 'Resume' : 'Pause';
      status.textContent = ({idle: 'Read along at your own pace', reading: 'Reading chapter', paused: 'Paused', error: 'Speech could not play. Try again or choose another browser.', empty: 'No readable chapter text.'})[state];
    });
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
