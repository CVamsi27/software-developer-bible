/* Chapter narration using the browser's speech service. */
(function (root) {
  'use strict';
  var VOICE_KEY = 'sdb-read-aloud-voice-v3';
  var SETTINGS_KEY = 'sdb-read-aloud-settings-v1';
  function splitWithOffsets(value) {
    var parts = [], start = 0;
    while (value.length - start > 240) {
      var sample = value.slice(start, start + 241);
      var endings = /[.!?]["'”’)]*(?=\s)/g, match, sentenceEnd = 0;
      while ((match = endings.exec(sample))) sentenceEnd = match.index + match[0].length;
      var cut = sentenceEnd >= 40 ? start + sentenceEnd : value.lastIndexOf(' ', start + 240);
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
  function splitText(text) {
    return splitWithOffsets(text.replace(/\s+/g, ' ').trim()).map(function (part) { return part.text; });
  }
  function rankVoices(voices) {
    var seen = Object.create(null);
    var novelty = /^(albert|bad news|bahh|bells|boing|bubbles|cellos|deranged|eddy|flo|fred|good news|grandma|grandpa|hysterical|jester|junior|kathy|organ|pipe organ|ralph|reed|rocko|sandy|shelley|trinoids|whisper|wobble|zarvox|superstar)(?:\b|$)/i;
    function score(voice) {
      var name = voice.name || '';
      return (/\bsamantha\b/i.test(name) ? 1000 : 0)
        + (/\bpremium\b/i.test(name) ? 300 : /\b(enhanced|natural|neural)\b/i.test(name) ? 200 : 0)
        + (voice.default ? 10 : 0);
    }
    return (voices || []).filter(function (voice) {
      if (!voice || !voice.voiceURI || voice.localService !== true || !/^en(?:-|_|$)/i.test(voice.lang || '') || novelty.test(voice.name || '') || seen[voice.voiceURI]) return false;
      seen[voice.voiceURI] = true;
      return true;
    }).sort(function (a, b) {
      var difference = score(b) - score(a);
      var aKey = [a.name, a.lang, a.voiceURI].join('|').toLowerCase();
      var bKey = [b.name, b.lang, b.voiceURI].join('|').toLowerCase();
      return difference || (aKey < bKey ? -1 : aKey > bKey ? 1 : 0);
    });
  }
  var wordSegmenter;
  function wordAt(text, index) {
    if (!Number.isInteger(index) || index < 0 || index >= text.length || /\s/.test(text[index])) return null;
    if (root.Intl && root.Intl.Segmenter) {
      if (!wordSegmenter) wordSegmenter = new root.Intl.Segmenter('en', {granularity: 'word'});
      var segments = wordSegmenter.segment(text);
      for (var segment of segments) {
        if (segment.isWordLike && segment.index <= index && segment.index + segment.segment.length > index) return {start: segment.index, end: segment.index + segment.segment.length};
      }
      return null;
    }
    var words = /[\p{L}\p{N}_]+(?:['’.-][\p{L}\p{N}_]+)*/gu, match;
    while ((match = words.exec(text))) {
      if (match.index <= index && match.index + match[0].length > index) return {start: match.index, end: match.index + match[0].length};
    }
    return null;
  }
  function createReader(synth, Utterance, update, onChunkStart, onWord) {
    var chunks = [], index = 0, offset = 0, generation = 0, state = 'idle', active = false, rate = 1, voice = null, doneState = 'idle';
    onChunkStart = onChunkStart || function () {};
    onWord = onWord || function () {};
    function emit(next) { state = next; update(next); }
    function cancelCurrent() {
      generation += 1; active = false;
      synth.cancel();
    }
    function reset() { cancelCurrent(); chunks = []; index = 0; offset = 0; }
    function stop() { reset(); emit('idle'); }
    function speakNext() {
      if (state !== 'reading' || active) return;
      if (index >= chunks.length) { active = false; emit(doneState); return; }
      var token = generation;
      var chunk = chunks[index];
      var text = typeof chunk === 'string' ? chunk : chunk.text;
      var startOffset = offset;
      var lastWordStart = -1;
      var utterance = new Utterance(text.slice(startOffset));
      utterance.rate = rate;
      // A selected voice carries its own language. Fall back to English for
      // the default system voice so the pronunciation stays predictable.
      utterance.lang = voice && voice.lang ? voice.lang : 'en-US';
      if (voice) utterance.voice = voice;
      active = true;
      utterance.onboundary = function (event) {
        if (token !== generation || (event.name && event.name !== 'word')) return;
        if (!Number.isInteger(event.charIndex) || event.charIndex < 0 || event.charIndex >= text.length - startOffset) return;
        // Engines may report separate boundaries for pieces of one visible word.
        var word = wordAt(text, startOffset + event.charIndex);
        if (!word || word.start <= lastWordStart) return;
        lastWordStart = offset = word.start;
        onWord(chunk, word.start, word.end);
      };
      utterance.onstart = function () {
        if (token !== generation) return;
        var range = typeof chunk === 'string' ? null : chunk.range;
        if (startOffset && chunk.rangeForOffsets) range = chunk.rangeForOffsets(startOffset, text.length);
        onChunkStart(typeof chunk === 'string' ? null : chunk.element, index, range);
      };
      utterance.onend = function () {
        if (token !== generation) return;
        generation += 1; active = false; index += 1; offset = 0; speakNext();
      };
      utterance.onerror = function () {
        if (token !== generation) return;
        cancelCurrent(); emit('error');
      };
      // Retain the current utterance until completion on browsers that require it.
      reader.utterance = utterance;
      try { synth.speak(utterance); } catch (_) { utterance.onerror(); }
    }
    function restartActive() {
      if (state !== 'reading' || !active) return;
      cancelCurrent(); synth.resume(); speakNext();
    }
    function pause() {
      if (state !== 'reading') return;
      cancelCurrent(); emit('paused');
    }
    function resume() {
      if (state !== 'paused') return;
      synth.resume(); emit('reading'); speakNext();
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
      pause: pause,
      togglePause: function () {
        if (state === 'reading') pause();
        else if (state === 'paused') resume();
      },
      setRate: function (value) {
        var numeric = Number(value);
        var next = Math.max(0.2, Math.min(2, Number.isFinite(numeric) && numeric > 0 ? numeric : 1));
        if (next === rate) return;
        rate = next; restartActive();
      },
      setVoice: function (value) {
        var next = value || null;
        if (voice === next) return;
        if (voice && next && voice.voiceURI === next.voiceURI && voice.lang === next.lang) { voice = next; return; }
        voice = next; restartActive();
      }
    };
    return reader;
  }
  // Source blocks form passages for navigation and optional study pauses.
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
        if (!parent || !node.textContent || parent.closest(excluded)) return NodeFilter.FILTER_REJECT;
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
          groups.push({text: part.text, element: previous, range: rangeForPart(content.ownerDocument, normalized.locations, part),
            rangeForOffsets: function (start, end) {
              if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end <= start || end > part.text.length) return null;
              return rangeForPart(content.ownerDocument, normalized.locations, {start: part.start + start, end: part.start + end});
            }});
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
  function createWordHighlighter(content) {
    var name = 'sdb-spoken-word', registry = root.CSS && root.CSS.highlights;
    var native = registry && typeof root.Highlight === 'function';
    var range = null, overlay = null, frame = null;
    function paint() {
      if (!range || !overlay) return;
      overlay.textContent = '';
      Array.from(range.getClientRects()).forEach(function (rect) {
        if (!rect.width || !rect.height) return;
        var box = document.createElement('span');
        box.className = 'read-aloud-word-box';
        box.style.left = rect.left + 'px'; box.style.top = rect.top + 'px';
        box.style.width = rect.width + 'px'; box.style.height = rect.height + 'px';
        overlay.append(box);
      });
    }
    function refresh() {
      if (native || !range || frame !== null) return;
      frame = root.requestAnimationFrame(function () { frame = null; paint(); });
    }
    if (!native) {
      root.addEventListener('scroll', refresh, true);
      root.addEventListener('resize', refresh);
      if (root.ResizeObserver) new root.ResizeObserver(refresh).observe(content);
    }
    return {
      show: function (next) {
        if (!next) return;
        range = next;
        if (native) { registry.set(name, new root.Highlight(range)); return; }
        if (!overlay) {
          overlay = document.createElement('div'); overlay.className = 'read-aloud-word-overlay';
          overlay.setAttribute('aria-hidden', 'true'); document.body.append(overlay);
        }
        paint();
      },
      clear: function () {
        range = null;
        if (native) registry.delete(name);
        if (overlay) overlay.textContent = '';
        if (frame !== null) { root.cancelAnimationFrame(frame); frame = null; }
      }
    };
  }
  function mount() {
    var content = document.querySelector('.post-content');
    if (!content || document.querySelector('.read-aloud')) return;
    var studyState = root.StudyState;
    var published = studyState && studyState.publishedPath(root.location.pathname, root.StudyPublishedPaths || []);
    if (!published || (!studyState.isLearningPath(published) && !/(?:\/REVISION|-interview-questions)\.html$/i.test(published))) return;
    function icon(paths) {
      return '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + paths + '</svg>';
    }
    var bar = document.createElement('section');
    bar.className = 'read-aloud';
    bar.setAttribute('aria-label', 'Chapter read aloud');
    bar.innerHTML = '<div class="read-aloud-settings" id="read-aloud-settings" hidden>'
      + '<div class="read-aloud-settings-heading"><strong>Make it sound right</strong><button type="button" data-close-settings aria-label="Close audio settings">' + icon('<path d="m6 6 12 12M6 18 18 6"/>') + '</button></div>'
      + '<div class="read-aloud-voice-row"><label class="read-aloud-field">Voice<select data-voice aria-label="Reading voice"></select></label>'
      + '<button type="button" data-preview aria-label="Preview voice">' + icon('<path d="m11 5-6 4H2v6h3l6 4zM15 8a6 6 0 0 1 0 8M18 5a10 10 0 0 1 0 14"/>') + '<span data-preview-label>Preview</span></button></div>'
      + '<p class="read-aloud-settings-note" data-voice-note>English device voices, with character voices hidden. Try a sample to choose.</p>'
      + '<div class="read-aloud-preferences"><label class="read-aloud-field">Speed<select data-speed aria-label="Reading speed"></select></label>'
      + '<label class="read-aloud-field">Playback<select data-mode aria-label="Playback mode"><option value="continuous">Continue through chapter</option><option value="paragraph">One passage at a time</option></select></label></div>'
      + '<label class="read-aloud-follow"><input type="checkbox" data-follow checked> Keep the spoken text in view</label></div>'
      + '<div class="read-aloud-summary"><div class="read-aloud-context"><div class="read-aloud-info"><span class="read-aloud-eyebrow">LISTEN TO THIS CHAPTER</span><strong class="read-aloud-title" data-title></strong><span class="read-aloud-status" role="status" aria-live="polite" aria-atomic="true">Ready when you are</span></div></div>'
      + '<div class="read-aloud-transport"><button type="button" class="read-aloud-icon" data-previous aria-label="Previous passage" title="Previous passage" disabled>' + icon('<path d="M5 5v14M19 5 8 12l11 7z"/>') + '</button>'
      + '<div class="read-aloud-primary"><button type="button" data-read aria-label="Read aloud">Listen</button><button type="button" data-pause aria-label="Pause" hidden>Pause</button></div>'
      + '<button type="button" class="read-aloud-icon" data-next aria-label="Next passage" title="Next passage" disabled>' + icon('<path d="M19 5v14M5 5l11 7-11 7z"/>') + '</button>'
      + '<button type="button" class="read-aloud-icon" data-stop aria-label="Stop" title="Stop" hidden>' + icon('<rect x="6" y="6" width="12" height="12" rx="2"/>') + '</button>'
      + '<button type="button" data-settings aria-label="Audio settings" title="Audio settings" aria-expanded="false" aria-controls="read-aloud-settings"><span data-rate>1.0×</span>' + icon('<path d="M4 7h9m4 0h3M4 17h3m4 0h9M13 4v6M7 14v6"/>') + '</button></div></div>'
      + '<div class="read-aloud-footer"><span class="read-aloud-hint" data-hint>Start here, or click a paragraph to choose.</span><span class="read-aloud-count" data-count></span></div>'
      + '<progress class="read-aloud-track" data-progress aria-label="Chapter listening progress" max="1" value="0"></progress>';
    document.body.append(bar);
    document.body.classList.add('has-read-aloud');
    var play = bar.querySelector('[data-read]'), pauseButton = bar.querySelector('[data-pause]');
    var previousButton = bar.querySelector('[data-previous]'), nextButton = bar.querySelector('[data-next]'), stopButton = bar.querySelector('[data-stop]');
    var status = bar.querySelector('[role="status"]'), hint = bar.querySelector('[data-hint]'), progress = bar.querySelector('[data-progress]'), count = bar.querySelector('[data-count]');
    var voiceSelect = bar.querySelector('[data-voice]'), speedSelect = bar.querySelector('[data-speed]'), modeSelect = bar.querySelector('[data-mode]'), followInput = bar.querySelector('[data-follow]');
    var settingsButton = bar.querySelector('[data-settings]'), settingsPanel = bar.querySelector('.read-aloud-settings'), previewButton = bar.querySelector('[data-preview]');
    var title = content.querySelector('h1');
    bar.querySelector('[data-title]').textContent = title ? title.textContent.trim() : 'Chapter audio';
    var arrowMedia = root.matchMedia && root.matchMedia('(max-width: 959px)');
    function placeArrow() {
      var arrow = document.querySelector('.back-to-top');
      if (!arrow) return;
      var parent = arrowMedia && arrowMedia.matches ? bar.querySelector('.read-aloud-context') : document.body;
      if (arrow.parentElement !== parent) parent.append(arrow);
      syncDock();
    }
    function syncDock() {
      if (!bar.offsetHeight) return;
      document.documentElement.style.setProperty('--read-aloud-height', bar.offsetHeight + 'px');
      var compactHeight = bar.querySelector('.read-aloud-summary').offsetHeight + bar.querySelector('.read-aloud-footer').offsetHeight + progress.offsetHeight;
      document.documentElement.style.setProperty('--read-aloud-compact-height', compactHeight + 'px');
    }
    placeArrow();
    document.addEventListener('DOMContentLoaded', placeArrow, {once: true});
    if (arrowMedia && arrowMedia.addEventListener) arrowMedia.addEventListener('change', placeArrow);
    else if (arrowMedia && arrowMedia.addListener) arrowMedia.addListener(placeArrow);
    function toggleSettings(open) {
      settingsPanel.hidden = !open;
      settingsButton.setAttribute('aria-expanded', String(open));
      syncDock();
    }
    settingsButton.addEventListener('click', function () { toggleSettings(settingsPanel.hidden); });
    bar.querySelector('[data-close-settings]').addEventListener('click', function () { toggleSettings(false); settingsButton.focus(); });
    bar.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && !settingsPanel.hidden) {
        event.preventDefault(); toggleSettings(false); settingsButton.focus();
      }
    });
    var speeds = [];
    for (var tenth = 2; tenth <= 20; tenth += 1) speeds.push(tenth / 10);
    speeds.push(0.75, 1.25);
    speeds.sort(function (a, b) { return a - b; }).forEach(function (speed) {
      var option = document.createElement('option');
      option.value = String(speed);
      option.textContent = (Number.isInteger(speed * 10) ? speed.toFixed(1) : String(speed)) + '×' + (speed === 1 ? ' · Normal' : '');
      speedSelect.append(option);
    });
    var preferences = {};
    try { preferences = JSON.parse(root.localStorage.getItem(SETTINGS_KEY) || '{}') || {}; } catch (_) {}
    if (typeof preferences !== 'object' || Array.isArray(preferences)) preferences = {};
    if (speeds.indexOf(Number(preferences.rate)) === -1) preferences.rate = 1;
    preferences.mode = preferences.mode === 'paragraph' ? 'paragraph' : 'continuous';
    preferences.follow = preferences.follow !== false;
    speedSelect.value = String(preferences.rate); modeSelect.value = preferences.mode; followInput.checked = preferences.follow;
    function savePreferences() {
      preferences = {rate: Number(speedSelect.value), mode: modeSelect.value, follow: followInput.checked};
      try { root.localStorage.setItem(SETTINGS_KEY, JSON.stringify(preferences)); } catch (_) {}
      var rate = Number(speedSelect.value);
      bar.querySelector('[data-rate]').textContent = (Number.isInteger(rate * 10) ? rate.toFixed(1) : String(rate)) + '×';
    }
    savePreferences();
    if (root.ResizeObserver) new root.ResizeObserver(syncDock).observe(bar);
    root.addEventListener('resize', syncDock);
    if (!root.speechSynthesis || !root.SpeechSynthesisUtterance) {
      [play, voiceSelect, speedSelect, modeSelect, followInput, previewButton].forEach(function (control) { control.disabled = true; });
      bar.dataset.state = 'unsupported'; status.textContent = 'Read aloud is unavailable in this browser.';
      hint.textContent = 'Try a browser that supports device speech.'; syncDock(); return;
    }
    var groups = groupChunks(extractChapter(content));
    var wordHighlighter = createWordHighlighter(content);
    var currentGroup = -1, selectedGroup = -1, activeBlock = null, selectedBlock = null;
    var lastState = 'idle', previewing = false, availableVoices = [], savedVoice = '', legacyVoice = '';
    try {
      savedVoice = root.localStorage.getItem(VOICE_KEY) || '';
      legacyVoice = root.localStorage.getItem('sdb-read-aloud-voice-v2') || '';
    } catch (_) {}
    function clearActive() {
      wordHighlighter.clear();
      if (activeBlock) activeBlock.removeAttribute('data-read-aloud-active');
      activeBlock = null;
    }
    function markActive(element) {
      if (!element || !content.contains(element)) { clearActive(); return; }
      if (activeBlock === element) return;
      if (activeBlock !== element) clearActive();
      activeBlock = element; element.setAttribute('data-read-aloud-active', 'true');
      document.dispatchEvent(new root.CustomEvent('study:narration', {detail: {element: element}}));
    }
    function clearSelected() {
      if (selectedBlock) selectedBlock.removeAttribute('data-read-aloud-selected');
      selectedBlock = null; selectedGroup = -1;
    }
    function selectParagraph(index) {
      var element = groups[index] && groups[index].element;
      if (!element || element.tagName !== 'P') return;
      clearSelected(); selectedGroup = index; selectedBlock = element;
      element.setAttribute('data-read-aloud-selected', 'true'); sync(lastState);
    }
    function follow(element, range, firstLineOnly) {
      if (!element || !content.contains(element)) { clearActive(); return; }
      markActive(element);
      if (!followInput.checked) return;
      var topMargin = Math.min(120, root.innerHeight * 0.2);
      var bottomMargin = bar.offsetHeight + 32;
      var visibleBottom = Math.max(topMargin + 40, root.innerHeight - bottomMargin);
      var reduced = root.matchMedia && root.matchMedia('(prefers-reduced-motion: reduce)').matches;
      var behavior = reduced ? 'auto' : 'smooth';
      var rects = range && range.getClientRects ? Array.from(range.getClientRects()).filter(function (rect) { return rect.height > 0; }) : [];
      if (rects.length) {
        var first = rects[0], last = firstLineOnly ? first : rects[rects.length - 1], delta = 0;
        if (last.bottom - first.top > visibleBottom - topMargin) delta = first.top - topMargin;
        else if (first.top < topMargin) delta = first.top - topMargin;
        else if (last.bottom > visibleBottom) delta = last.bottom - visibleBottom;
        if (delta) root.scrollBy({top: delta, behavior: behavior});
      } else {
        var rect = element.getBoundingClientRect();
        if (rect.top < topMargin || rect.bottom > visibleBottom) element.scrollIntoView({block: 'start', behavior: behavior});
      }
    }
    function stateMessage(next) {
      if (previewing) return lastState === 'paused' ? 'Previewing voice · chapter stays paused' : 'Previewing selected voice';
      if (!availableVoices.length) return 'No English device voice available.';
      if (!groups.length || next === 'empty') return 'No readable chapter text.';
      if (selectedGroup >= 0) return 'Paragraph selected · press Listen here';
      if (next === 'reading') return 'Reading · passage ' + (currentGroup + 1) + ' of ' + groups.length;
      if (next === 'paused') return 'Paused · resume when you’re ready';
      if (next === 'ready') return 'Passage finished · continue when ready';
      if (next === 'complete') return 'Chapter complete · nicely done';
      if (next === 'error') return 'Speech stopped · try again or choose another voice';
      return 'Ready · start from where you’re reading';
    }
    function sync(nextState) {
      lastState = nextState;
      var busy = nextState === 'reading' || nextState === 'paused';
      var positioned = currentGroup >= 0 && (busy || nextState === 'ready' || nextState === 'complete' || nextState === 'error');
      var focusWasAction = [play, pauseButton, previousButton, nextButton, stopButton].indexOf(document.activeElement) !== -1;
      var focused = document.activeElement;
      if (!positioned || nextState === 'complete' || nextState === 'error') clearActive();
      else if (nextState === 'ready') wordHighlighter.clear();
      bar.dataset.state = previewing ? 'preview' : !availableVoices.length ? 'no-voices' : nextState;
      play.hidden = busy && selectedGroup < 0;
      pauseButton.hidden = !busy || selectedGroup >= 0;
      play.disabled = !availableVoices.length || !groups.length;
      previousButton.disabled = !positioned || currentGroup <= 0 || !availableVoices.length;
      nextButton.disabled = !positioned || currentGroup >= groups.length - 1 || !availableVoices.length;
      stopButton.hidden = !positioned && !previewing;
      play.textContent = selectedGroup >= 0 ? 'Listen here' : nextState === 'ready' ? 'Continue' : nextState === 'complete' ? 'Listen again' : nextState === 'error' ? 'Try again' : 'Listen';
      play.setAttribute('aria-label', selectedGroup >= 0 ? 'Read selected paragraph' : nextState === 'ready' ? 'Continue listening' : nextState === 'complete' ? 'Listen again' : 'Read aloud');
      pauseButton.textContent = nextState === 'paused' ? 'Resume' : 'Pause';
      pauseButton.setAttribute('aria-label', nextState === 'paused' ? 'Resume' : 'Pause');
      pauseButton.dataset.paused = String(nextState === 'paused');
      previewButton.setAttribute('aria-label', previewing ? 'Stop voice preview' : 'Preview voice');
      bar.querySelector('[data-preview-label]').textContent = previewing ? 'Stop preview' : 'Preview';
      status.textContent = stateMessage(nextState);
      hint.textContent = !availableVoices.length ? 'Enable an English voice in your device’s speech settings, then reload.'
        : selectedGroup >= 0 ? 'Your selection starts the next listening passage.'
        : positioned ? (modeSelect.value === 'continuous' ? 'Continuous listening' : 'One passage at a time')
        : 'Start here, or click a paragraph to choose.';
      count.textContent = positioned ? (currentGroup + 1) + ' / ' + groups.length : '';
      progress.max = Math.max(1, groups.length);
      progress.value = nextState === 'complete' ? groups.length : nextState === 'ready' ? currentGroup + 1 : Math.max(0, currentGroup);
      if (focusWasAction && (focused.hidden || focused.disabled)) (busy && selectedGroup < 0 ? pauseButton : play).focus({preventScroll: true});
      syncDock();
    }
    var reader = createReader(root.speechSynthesis, root.SpeechSynthesisUtterance, function (next) {
      if (next === 'ready' && modeSelect.value === 'continuous' && selectedGroup < 0) { startAt(currentGroup + 1); return; }
      sync(next);
    }, function (element, _index, range) {
      wordHighlighter.clear(); follow(element, range, true);
    }, function (chunk, start, end) {
      if (!chunk.rangeForOffsets || !content.contains(chunk.element)) return;
      var range = chunk.rangeForOffsets(start, end);
      if (!range) return;
      follow(chunk.element, range); wordHighlighter.show(range);
    });
    var previewReader = createReader(root.speechSynthesis, root.SpeechSynthesisUtterance, function (next) {
      if (next === 'reading') return;
      previewing = false; sync(lastState);
      if (next === 'error') status.textContent = 'Preview could not play. Choose another device voice.';
    });
    reader.setRate(speedSelect.value); previewReader.setRate(speedSelect.value);
    function stopPreview() { if (previewing) previewReader.stop(); }
    function voiceByURI(uri) {
      return availableVoices.find(function (voice) { return voice.voiceURI === uri; }) || null;
    }
    function refreshVoices() {
      var list = [];
      try { list = Array.from(root.speechSynthesis.getVoices()); } catch (_) {}
      var selected = voiceSelect.value || savedVoice;
      availableVoices = rankVoices(list);
      voiceSelect.textContent = '';
      if (!availableVoices.length) {
        var unavailable = document.createElement('option');
        unavailable.value = ''; unavailable.textContent = 'No English device voices'; voiceSelect.append(unavailable);
        voiceSelect.disabled = true; previewButton.disabled = true;
        stopPreview();
        if (lastState === 'reading' || lastState === 'paused') reader.stop();
        sync(lastState); return;
      }
      var suggestions = document.createElement('optgroup'); suggestions.label = 'Suggested device voices';
      var others = document.createElement('optgroup'); others.label = 'Other installed English voices';
      var suggestedVoices = availableVoices.filter(function (voice) { return /\b(samantha|premium|enhanced|natural|neural)\b/i.test(voice.name || ''); }).slice(0, 5);
      if (!suggestedVoices.length) suggestedVoices = availableVoices.slice(0, 1);
      availableVoices.forEach(function (voice) {
        var option = document.createElement('option');
        option.value = voice.voiceURI; option.textContent = voice.name + ' · ' + voice.lang;
        (suggestedVoices.indexOf(voice) >= 0 ? suggestions : others).append(option);
      });
      voiceSelect.append(suggestions); if (others.children.length) voiceSelect.append(others);
      if (!selected && legacyVoice && suggestedVoices.some(function (voice) { return voice.voiceURI === legacyVoice; })) selected = legacyVoice;
      voiceSelect.value = voiceByURI(selected) ? selected : availableVoices[0].voiceURI;
      voiceSelect.disabled = false; previewButton.disabled = false;
      var chosen = voiceByURI(voiceSelect.value);
      reader.setVoice(chosen); previewReader.setVoice(chosen); sync(lastState);
    }
    function startAt(index) {
      if (index < 0 || index >= groups.length || !availableVoices.length) return;
      stopPreview(); wordHighlighter.clear(); clearSelected(); currentGroup = index;
      markActive(groups[index].element);
      reader.start(groups[index].chunks, {doneState: index === groups.length - 1 ? 'complete' : 'ready'});
    }
    play.addEventListener('click', function () {
      refreshVoices();
      if (selectedGroup >= 0) { startAt(selectedGroup); return; }
      if (lastState === 'ready') { startAt(currentGroup + 1); return; }
      if (lastState === 'error' && currentGroup >= 0) { startAt(currentGroup); return; }
      if (lastState === 'complete') { startAt(0); return; }
      groups = groupChunks(extractChapter(content));
      var atTop = (root.scrollY || root.pageYOffset || 0) <= 1;
      var readingLine = Math.max(96, Math.min(root.innerHeight * 0.28, 220));
      startAt(pickStartGroup(groups, atTop ? -1 : readingLine));
    });
    content.addEventListener('click', function (event) {
      var target = event.target;
      if (!target || !target.closest || target.closest('a,button,input,select,textarea,summary,[role="button"],[contenteditable="true"]')) return;
      if (root.getSelection && !root.getSelection().isCollapsed) return;
      var paragraph = target.closest('p');
      if (!paragraph || !content.contains(paragraph)) return;
      if (lastState === 'idle') groups = groupChunks(extractChapter(content));
      for (var index = 0; index < groups.length; index += 1) {
        if (groups[index].element === paragraph) { selectParagraph(index); return; }
      }
    });
    pauseButton.addEventListener('click', function () { stopPreview(); reader.togglePause(); });
    previousButton.addEventListener('click', function () { startAt(currentGroup - 1); });
    nextButton.addEventListener('click', function () { startAt(currentGroup + 1); });
    stopButton.addEventListener('click', function () { stopPreview(); currentGroup = -1; clearSelected(); reader.stop(); });
    speedSelect.addEventListener('change', function () {
      savePreferences(); reader.setRate(speedSelect.value); previewReader.setRate(speedSelect.value);
    });
    modeSelect.addEventListener('change', function () { savePreferences(); sync(lastState); });
    followInput.addEventListener('change', savePreferences);
    voiceSelect.addEventListener('change', function () {
      savedVoice = voiceSelect.value;
      try { root.localStorage.setItem(VOICE_KEY, savedVoice); } catch (_) {}
      reader.setVoice(voiceByURI(savedVoice)); previewReader.setVoice(voiceByURI(savedVoice));
    });
    previewButton.addEventListener('click', function () {
      if (previewing) { stopPreview(); return; }
      if (!voiceByURI(voiceSelect.value)) return;
      reader.pause(); previewing = true;
      previewReader.start(['This is a preview of your reading voice. Find a pace that feels right for you.']);
      sync(lastState);
    });
    if (root.speechSynthesis.addEventListener) root.speechSynthesis.addEventListener('voiceschanged', refreshVoices);
    else root.speechSynthesis.onvoiceschanged = refreshVoices;
    refreshVoices();
    function leave() { stopPreview(); reader.stop(); }
    root.addEventListener('pagehide', leave); root.addEventListener('beforeunload', leave);
    sync(lastState);
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = {splitText: splitText, createReader: createReader, groupChunks: groupChunks, pickStartGroup: pickStartGroup, rankVoices: rankVoices, wordAt: wordAt};
  else {
    root.SDBReadAloud = {extractChapter: extractChapter, groupChunks: groupChunks, pickStartGroup: pickStartGroup};
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount);
    else mount();
  }
})(typeof window !== 'undefined' ? window : globalThis);
