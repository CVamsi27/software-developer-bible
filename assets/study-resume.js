/* One deliberate reading position, local to this browser. Never auto-resume. */
document.addEventListener('DOMContentLoaded', function () {
  'use strict';
  if (!window.StudyState || !Array.isArray(window.StudyPublishedPaths)) return;
  var storage;
  try { storage = window.localStorage; } catch (_) { storage = null; }
  var store = window.StudyResumeStore || window.StudyState.createStore(storage, window.StudyPublishedPaths);
  window.StudyResumeStore = store;
  var card = document.querySelector('[data-study-resume]');
  if (card && !card.dataset.mounted) {
    card.dataset.mounted = 'true';
    var feedback = document.querySelector('.resume-feedback'), previous = null;
    var intro = document.querySelector('.home-intro'), headline = intro && intro.querySelector('h1');
    var firstVisitTitle = headline && headline.textContent;
    function render() {
      var record = store.read(); card.hidden = !record;
      document.body.classList.toggle('has-saved-position', Boolean(record));
      if (headline) headline.textContent = record ? 'Continue your study.' : firstVisitTitle;
      if (intro) intro.querySelector('p:not(.eyebrow)').hidden = Boolean(record);
      if (!record) return;
      card.querySelector('[data-resume-title]').textContent = record.title;
      card.querySelector('[data-resume-section]').textContent = record.section || 'Chapter start';
      card.querySelector('[data-resume-link]').href = record.path + '?resume=1';
    }
    card.querySelector('[data-clear-resume]').addEventListener('click', function () {
      previous = store.clear(); render(); feedback.hidden = false;
      feedback.querySelector('[role="status"]').textContent = 'Saved position cleared.';
      feedback.querySelector('button').focus();
    });
    feedback.querySelector('button').addEventListener('click', function () {
      if (previous) store.write(previous); previous = null; render(); feedback.hidden = true;
      if (!card.hidden) card.querySelector('[data-resume-link]').focus();
    });
    render();
  }
  var content = document.querySelector('.post-content');
  if (!content || !window.StudyState.isLearningPath(location.pathname) || !window.StudyPublishedPaths.includes(location.pathname) || content.dataset.resumeMounted) return;
  content.dataset.resumeMounted = 'true';
  var saved = store.read();
  if (new URLSearchParams(location.search).get('resume') === '1' && !location.hash && saved && saved.path === location.pathname) {
    var destination = saved.anchor ? document.getElementById(saved.anchor) : content.querySelector('h1');
    if (destination && content.contains(destination)) {
      destination.scrollIntoView({block: 'start', behavior: 'auto'});
      destination.setAttribute('tabindex', '-1'); destination.focus({preventScroll: true});
      if (saved.anchor) history.replaceState(null, '', location.pathname + location.search + '#' + encodeURIComponent(saved.anchor));
    } else {
      var notice = document.createElement('p'); notice.className = 'resume-feedback'; notice.setAttribute('role', 'status');
      notice.textContent = 'This chapter changed; opening from the beginning.'; content.prepend(notice);
      window.scrollTo({top: 0, left: 0, behavior: 'auto'});
    }
  }
  var intentUntil = 0, pending = null, timer;
  function intention(event) {
    if (event.type === 'keydown' && (!['ArrowDown','ArrowUp','PageDown','PageUp','Home','End',' '].includes(event.key) || event.target.closest('input,select,textarea,button,summary'))) return;
    intentUntil = Date.now() + 2500;
  }
  window.addEventListener('wheel', intention, {passive: true});
  window.addEventListener('touchmove', intention, {passive: true});
  document.addEventListener('keydown', intention);
  function text(element) { var clone = element.cloneNode(true); clone.querySelectorAll('.heading-anchor').forEach(function (a) { a.remove(); }); return clone.textContent.trim(); }
  function flush() { clearTimeout(timer); if (pending) { store.write(pending); pending = null; } }
  function save(heading) {
    var title = content.querySelector('h1');
    if (!title || !heading || !content.contains(heading)) return;
    pending = {version: 1, path: location.pathname, anchor: heading.id || '', title: text(title), section: text(heading), savedAt: Date.now()};
    clearTimeout(timer); timer = setTimeout(flush, 400);
  }
  document.addEventListener('study:section', function (event) {
    if (event.detail.deliberate || Date.now() < intentUntil) save(event.detail.heading);
  });
  document.addEventListener('study:narration', function (event) {
    var element = event.detail.element;
    var headings = Array.from(content.querySelectorAll('h2[id]'));
    var heading = headings[0];
    headings.forEach(function (candidate) { if (candidate === element || candidate.compareDocumentPosition(element) & Node.DOCUMENT_POSITION_FOLLOWING) heading = candidate; });
    save(heading);
  });
  window.addEventListener('pagehide', flush);
});
