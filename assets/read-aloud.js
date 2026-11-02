/* Chapter narration using the browser's speech service. */
(function (root) {
  'use strict';
  var VOICE_KEY = 'sdb-read-aloud-voice';
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
    var chunks = [], index = 0, generation = 0, state = 'idle', active = false, rate = 1, voice = null, doneState = 'idle';
    onChunkStart = onChunkStart || function () {};
    function emit(next) { state = next; update(next); }
    function reset() {
      generation += 1; active = false; chunks = []; index = 0;
      synth.cancel();
    }
    function stop() { reset(); emit('idle'); }
    function speakNext() {
      if (state === 'paused' || active) return;
      if (index >= chunks.length) { active = false; emit(doneState); return; }
      var token = generation;
      var chunk = chunks[index];
      var text = typeof chunk === 'string' ? chunk : chunk.text;
      var utterance = new Utterance(text);
      utterance.rate = rate;
      // A selected voice carries its own language. Fall back to English for
      // the default system voice so the pronunciation stays predictable.
      utterance.lang = voice && voice.lang ? voice.lang : 'en-US';
      if (voice) utterance.voice = voice;
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
      start: function (parts, options) {
        reset();
        chunks = parts || [];
        doneState = options && options.doneState || 'idle';
        if (!chunks.length) { emit('empty'); return; }
        synth.resume(); emit('reading'); speakNext();
      },
      stop: stop,
      togglePause: function () {
        if (state === 'reading') { emit('paused'); synth.pause(); }
        else if (state === 'paused') { emit('reading'); synth.resume(); speakNext(); }
      },
      setRate: function (value) { rate = Math.max(0.5, Math.min(2, Number(value) || 1)); },
      setVoice: function (value) { voice = value || null; }
    };
    return reader;
  }
  // A chapter is read one source block at a time so the listener can pause
  // between paragraphs instead of being carried through the whole page.
  function groupChunks(chunks) {
    var groups = [];
    (chunks || []).forEach(function (chunk) {
      var element = typeof chunk === 'string' ? null : chunk.element;
      var last = groups[groups.length - 1];
      if (!last || last.element !== element) groups.push({element: element, chunks: [chunk]});
      else last.chunks.push(chunk);
    });
    return groups;
  }
  // Pick the first readable block at or below the reading line. That makes a
  // scrolled chapter start where the reader is looking instead of at its title.
  function pickStartGroup(groups, topLine) {
    if (!groups || !groups.length) return -1;
    for (var index = 0; index < groups.length; index += 1) {
      var element = groups[index] && groups[index].element;
      if (!element || typeof element.getBoundingClientRect !== 'function') continue;
      if (element.getBoundingClientRect().bottom > topLine) return index;
    }
    return groups.length - 1;
  }
  function extractChapter(content) {
    var excluded = 'pre, script, style, nav, button, img, svg, [hidden], [aria-hidden="true"], .read-aloud, .chapter-outline, .heading-anchor, .chapter-nav-footer,.roadmap-return,.reader-breadcrumb,.reader-meta,.revision-controls,.code-line-numbers,.copy-feedback,details:not([open])';
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
    if (!content || document.querySelector('.read-aloud')) return;
    var state = root.StudyState;
    var published = state && state.publishedPath(root.location.pathname, root.StudyPublishedPaths || []);
    if (!published || (!state.isLearningPath(published) && !/\/REVISION\.html$/i.test(published))) return;
    var bar = document.createElement('section');
    bar.className = 'read-aloud'; bar.setAttribute('aria-label', 'Chapter read aloud');
    bar.innerHTML = '<span class="read-aloud-progress" aria-hidden="true" hidden></span><span class="read-aloud-status" role="status" aria-live="polite">Read along at your own pace</span><div class="read-aloud-controls"><button type="button" data-read aria-label="Read aloud" title="Click or tap a paragraph to choose where Listen starts">Listen</button><button type="button" data-pause aria-label="Pause" hidden>Pause</button><button type="button" data-next aria-label="Read the next paragraph" hidden>Next</button><button type="button" data-stop aria-label="Stop" hidden>Stop</button><label class="read-aloud-field">Voice <select data-voice aria-label="Reading voice"></select></label><label class="read-aloud-field">Speed <select data-speed aria-label="Reading speed"><option value="0.5">0.5×</option><option value="0.75">0.75×</option><option value="1" selected>1×</option><option value="1.25">1.25×</option><option value="1.5">1.5×</option><option value="2">2×</option></select></label></div>';
    document.body.append(bar);
    var topButton = document.querySelector('.back-to-top');
    var controls = bar.querySelector('.read-aloud-controls');
    if (topButton && controls) controls.append(topButton);
    document.body.classList.add('has-read-aloud');
    var play = bar.querySelector('[data-read]'), pause = bar.querySelector('[data-pause]'), nextButton = bar.querySelector('[data-next]'), stop = bar.querySelector('[data-stop]'), status = bar.querySelector('[role="status"]'), progress = bar.querySelector('.read-aloud-progress'), voiceSelect = bar.querySelector('[data-voice]'), speedSelect = bar.querySelector('[data-speed]');
    function syncDock() {
      if (!bar.offsetHeight) return;
      document.documentElement.style.setProperty('--read-aloud-height', bar.offsetHeight + 'px');
    }
    if (!root.speechSynthesis || !root.SpeechSynthesisUtterance) {
      play.disabled = true; voiceSelect.disabled = true; speedSelect.disabled = true;
      bar.dataset.state = 'unsupported';
      status.textContent = 'Read aloud is unavailable in this browser.';
      syncDock(); return;
    }
    var groups = groupChunks(extractChapter(content));
    var currentGroup = -1, selectedGroup = -1, activeBlock = null, selectedBlock = null;
    var savedVoice = '';
    try { savedVoice = root.localStorage.getItem(VOICE_KEY) || ''; } catch (_) {}
    function clearActive() {
      if (activeBlock) activeBlock.removeAttribute('data-read-aloud-active');
      activeBlock = null;
    }
    function markActive(element) {
      if (!element || !content.contains(element)) { clearActive(); return; }
      if (activeBlock !== element) clearActive();
      activeBlock = element;
      element.setAttribute('data-read-aloud-active', 'true');
      document.dispatchEvent(new root.CustomEvent('study:narration', {detail: {element: element}}));
    }
    function clearSelected() {
      if (selectedBlock) selectedBlock.removeAttribute('data-read-aloud-selected');
      selectedBlock = null;
      selectedGroup = -1;
    }
    function selectParagraph(index) {
      if (index < 0 || index >= groups.length) return;
      var element = groups[index].element;
      if (!element || element.tagName !== 'P') return;
      if (selectedBlock && selectedBlock !== element) selectedBlock.removeAttribute('data-read-aloud-selected');
      selectedGroup = index;
      selectedBlock = element;
      element.setAttribute('data-read-aloud-selected', 'true');
      play.hidden = false;
      play.textContent = 'Listen';
      play.setAttribute('aria-label', 'Read selected paragraph');
      status.textContent = 'Paragraph selected. Press Listen to start here.';
      syncDock();
    }
    function follow(element, _index, range) {
      if (!element || !content.contains(element)) { clearActive(); return; }
      markActive(element);
      var topMargin = 120;
      var bottomMargin = Math.min(root.innerHeight * 0.28, Math.max(112, bar.offsetHeight + 28));
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
    function stateMessage(next) {
      var place = currentGroup >= 0 ? 'paragraph ' + (currentGroup + 1) + ' of ' + groups.length : 'chapter';
      if (next === 'reading') return 'Reading ' + place + '.';
      if (next === 'paused') return 'Paused at ' + place + '.';
      if (next === 'ready') return 'Finished ' + place + '. Choose Next to continue.';
      if (next === 'complete') return 'Chapter complete. Choose Listen again to restart.';
      if (next === 'error') return 'Speech could not play. Try again or choose another browser.';
      if (next === 'empty') return 'No readable chapter text.';
      return 'Read along at your own pace';
    }
    var lastState = 'idle';
    function sync(nextState) {
      lastState = nextState;
      var busy = nextState === 'reading' || nextState === 'paused';
      var ready = nextState === 'ready';
      var finished = nextState === 'complete';
      var active = busy || ready || finished;
      var focusWasAction = [play, pause, nextButton, stop].indexOf(document.activeElement) !== -1;
      if (!active) clearActive();
      bar.dataset.state = nextState;
      play.hidden = (busy || ready) && selectedGroup < 0;
      pause.hidden = !busy;
      nextButton.hidden = !ready;
      stop.hidden = !(busy || ready || finished);
      play.textContent = finished && selectedGroup < 0 ? 'Listen again' : 'Listen';
      play.setAttribute('aria-label', selectedGroup >= 0 ? 'Read selected paragraph' : finished ? 'Listen again' : 'Read aloud');
      pause.textContent = nextState === 'paused' ? 'Resume' : 'Pause';
      pause.setAttribute('aria-label', nextState === 'paused' ? 'Resume' : 'Pause');
      var hasPosition = active && currentGroup >= 0 && currentGroup < groups.length;
      progress.hidden = !hasPosition;
      if (hasPosition) progress.textContent = (currentGroup + 1) + ' / ' + groups.length;
      status.textContent = stateMessage(nextState);
      if (focusWasAction) (busy ? pause : ready ? nextButton : play).focus();
      syncDock();
    }
    var reader = createReader(root.speechSynthesis, root.SpeechSynthesisUtterance, function (next) {
      sync(next);
    }, follow);
    function voiceByURI(uri) {
      for (var index = 0; index < availableVoices.length; index += 1) {
        if (availableVoices[index].voiceURI === uri) return availableVoices[index];
      }
      return null;
    }
    var availableVoices = [];
    function refreshVoices() {
      var list = [];
      try { list = root.speechSynthesis.getVoices ? Array.prototype.slice.call(root.speechSynthesis.getVoices()) : []; } catch (_) { list = []; }
      availableVoices = list.filter(function (voice) {
        return voice && voice.voiceURI && /^en(?:-|_|$)/i.test(voice.lang || '');
      }).sort(function (a, b) {
        return (a.name || '').localeCompare(b.name || '');
      }).slice(0, 5);
      var selected = voiceSelect.value || savedVoice;
      voiceSelect.textContent = '';
      if (!availableVoices.length) {
        var unavailable = document.createElement('option');
        unavailable.value = '';
        unavailable.textContent = 'No English voices available';
        unavailable.disabled = true;
        voiceSelect.append(unavailable);
        voiceSelect.value = '';
        voiceSelect.disabled = true;
        reader.setVoice(null);
        return;
      }
      availableVoices.forEach(function (voice) {
        var option = document.createElement('option');
        option.value = voice.voiceURI;
        option.textContent = voice.name + (voice.lang ? ' (' + voice.lang + ')' : '');
        voiceSelect.append(option);
      });
      voiceSelect.value = selected && voiceByURI(selected) ? selected : availableVoices[0].voiceURI;
      voiceSelect.disabled = false;
      reader.setVoice(voiceByURI(voiceSelect.value));
    }
    function startAt(index) {
      if (index < 0 || index >= groups.length) return;
      clearSelected();
      currentGroup = index;
      markActive(groups[index].element);
      reader.start(groups[index].chunks, {doneState: index === groups.length - 1 ? 'complete' : 'ready'});
    }
    play.addEventListener('click', function () {
      refreshVoices();
      if (selectedGroup >= 0) { startAt(selectedGroup); return; }
      // "Listen again" restarts at the chapter opening even when the last
      // paragraph left the viewport at the bottom of the page.
      if (lastState === 'complete') { startAt(0); return; }
      var atTop = (root.scrollY || root.pageYOffset || 0) <= 1;
      var readingLine = Math.max(96, Math.min(root.innerHeight * 0.28, 220));
      startAt(pickStartGroup(groups, atTop ? -1 : readingLine));
    });
    content.addEventListener('click', function (event) {
      var target = event.target;
      if (!target || !target.closest) return;
      if (target.closest('a, button, input, select, textarea, summary, [role="button"], [contenteditable="true"]')) return;
      var paragraph = target.closest('p');
      if (!paragraph || !content.contains(paragraph)) return;
      for (var index = 0; index < groups.length; index += 1) {
        if (groups[index].element === paragraph) {
          selectParagraph(index);
          return;
        }
      }
    });
    pause.addEventListener('click', reader.togglePause);
    nextButton.addEventListener('click', function () { startAt(currentGroup + 1); });
    stop.addEventListener('click', function () { currentGroup = -1; clearSelected(); reader.stop(); });
    speedSelect.addEventListener('change', function (event) { reader.setRate(event.target.value); });
    voiceSelect.addEventListener('change', function () {
      savedVoice = voiceSelect.value;
      try { root.localStorage.setItem(VOICE_KEY, savedVoice); } catch (_) {}
      reader.setVoice(voiceByURI(savedVoice));
    });
    if (root.speechSynthesis.addEventListener) root.speechSynthesis.addEventListener('voiceschanged', refreshVoices);
    else root.speechSynthesis.onvoiceschanged = refreshVoices;
    refreshVoices();
    if (!groups.length) { play.disabled = true; sync('empty'); }
    else sync('idle');
    if (root.ResizeObserver) new root.ResizeObserver(syncDock).observe(bar);
    root.addEventListener('resize', syncDock);
    root.addEventListener('pagehide', reader.stop);
    root.addEventListener('beforeunload', reader.stop);
    syncDock();
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {splitText: splitText, createReader: createReader, groupChunks: groupChunks, pickStartGroup: pickStartGroup};
  else {
    root.SDBReadAloud = {extractChapter: extractChapter, groupChunks: groupChunks, pickStartGroup: pickStartGroup};
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
    else mount();
  }
})(typeof window !== 'undefined' ? window : globalThis);
