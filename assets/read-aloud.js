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
        if (token === generation) {
          onChunkStart(typeof chunk === 'string' ? null : chunk.element, index, typeof chunk === 'string' ? null : chunk.range);
        }
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
    var excluded = 'pre, script, style, nav, button, img, svg, [hidden], [aria-hidden="true"], .read-aloud, .chapter-outline, .heading-anchor, .chapter-nav-footer,.roadmap-return,.reader-breadcrumb,.reader-meta,.reading-width,.study-continuation,.revision-controls,details:not([open])';
    var NodeFilter = content.ownerDocument.defaultView.NodeFilter;
    var walker = content.ownerDocument.createTreeWalker(content, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent || !node.textContent.trim() || parent.closest(excluded)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var groups = [], previous = null, nodes = [];
    function normalizeNodes(sourceNodes) {
      var rawCharacters = [], positions = [];
      sourceNodes.forEach(function (node) {
        var value = node.textContent;
        for (var i = 0; i < value.length; i += 1) {
          rawCharacters.push(value[i]);
          positions.push({node: node, offset: i});
        }
      });
      var raw = rawCharacters.join('');
      var normalizedCharacters = [], locations = [], inWhitespace = false;
      for (var j = 0; j < raw.length; j += 1) {
        if (/\s/.test(raw[j])) {
          if (normalizedCharacters.length && !inWhitespace) { normalizedCharacters.push(' '); locations.push(positions[j]); }
          inWhitespace = true;
        } else {
          normalizedCharacters.push(raw[j]); locations.push(positions[j]); inWhitespace = false;
        }
      }
      if (inWhitespace) { normalizedCharacters.pop(); locations.pop(); }
      var text = normalizedCharacters.join('');
      return {text: text, locations: locations};
    }
    function splitWithOffsets(value) {
      var parts = [], start = 0;
      while (value.length - start > 240) {
        var cut = value.lastIndexOf(' ', start + 240);
        if (cut < start + 1) cut = start + 240;
        var end = cut;
        while (end > start && /\s/.test(value[end - 1])) end -= 1;
        if (end > start) parts.push({text: value.slice(start, end), start: start, end: end});
        start = cut;
        while (start < value.length && /\s/.test(value[start])) start += 1;
      }
      if (start < value.length) parts.push({text: value.slice(start), start: start, end: value.length});
      return parts;
    }
    function rangeForPart(document, locations, part) {
      var first = locations[part.start], last = locations[part.end - 1];
      if (!first || !last || !document.createRange) return null;
      var range = document.createRange();
      range.setStart(first.node, first.offset);
      range.setEnd(last.node, last.offset + 1);
      return range;
    }
    function save() {
      if (nodes.length) {
        var normalized = normalizeNodes(nodes);
        splitWithOffsets(normalized.text).forEach(function (part) {
          groups.push({text: part.text, element: previous, range: rangeForPart(content.ownerDocument, normalized.locations, part)});
        });
      }
    }
    while (walker.nextNode()) {
      var node = walker.currentNode;
      var block = node.parentElement.closest('h1,h2,h3,h4,h5,h6,p,li,td,th,blockquote');
      if (!block || !content.contains(block)) continue;
      if (previous !== block) {
        save();
        nodes = []; previous = block;
      }
      nodes.push(node);
    }
    save();
    return groups;
  }
  function mount() {
    var content = document.querySelector('.post-content');
    if (!content || content.querySelector('.read-aloud')) return;
    var state = root.StudyState;
    if (!state || (!state.isLearningPath(root.location.pathname) && !/\/REVISION\.html$/i.test(root.location.pathname))) return;
    var bar = document.createElement('section');
    bar.className = 'read-aloud'; bar.setAttribute('aria-label', 'Chapter read aloud');
    bar.innerHTML = '<span class="read-aloud-status" role="status" aria-live="polite">Read along at your own pace</span><div class="read-aloud-controls"><button type="button" data-read aria-label="Read aloud">Listen</button><button type="button" data-pause aria-label="Pause" hidden>Pause</button><button type="button" data-stop aria-label="Stop" hidden>Stop</button><select aria-label="Reading speed"><option value="0.5">0.5×</option><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></div>';
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
    function follow(element, _index, range) {
      if (!element || !content.contains(element)) { clearActive(); return; }
      if (activeElement !== element) clearActive();
      activeElement = element;
      element.setAttribute('data-read-aloud-active', 'true');
      document.dispatchEvent(new root.CustomEvent('study:narration', {detail: {element: element}}));
      var topMargin = 120;
      var bottomMargin = Math.min(120, root.innerHeight * 0.15);
      var reduced = root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var behavior = reduced ? 'auto' : 'smooth';
      var rects = range && range.getClientRects ? Array.from(range.getClientRects()).filter(function (rect) { return rect.height > 0; }) : [];
      if (rects.length) {
        var first = rects[0], last = rects[rects.length - 1];
        var visibleTop = topMargin, visibleBottom = root.innerHeight - bottomMargin;
        var delta = 0;
        if (last.bottom - first.top > visibleBottom - visibleTop) {
          var spokenCenter = (first.top + last.bottom) / 2;
          delta = spokenCenter - (visibleTop + visibleBottom) / 2;
        } else if (first.top < visibleTop) delta = first.top - visibleTop;
        else if (last.bottom > visibleBottom) delta = last.bottom - visibleBottom;
        if (delta) root.scrollBy({top: delta, behavior: behavior});
      } else {
        var rect = element.getBoundingClientRect();
        if (rect.top < topMargin || rect.bottom > root.innerHeight - bottomMargin) {
          element.scrollIntoView({block: 'start', behavior: behavior});
        }
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
