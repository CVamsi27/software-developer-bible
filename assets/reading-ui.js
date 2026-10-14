/* A collapsible route through the chapter, built from its authored headings. */
document.addEventListener('DOMContentLoaded', function () {
  var menuInput = document.getElementById('nav-trigger');
  var menuToggle = document.querySelector('label[for="nav-trigger"]');
  var menuLinks = document.querySelector('.site-nav .trigger');
  if (menuInput && menuToggle && menuLinks) {
    menuLinks.id = menuLinks.id || 'site-navigation-links';
    menuToggle.setAttribute('role', 'button');
    menuToggle.setAttribute('tabindex', '0');
    menuToggle.setAttribute('aria-label', 'Toggle navigation');
    menuToggle.setAttribute('aria-controls', menuLinks.id);
    var updateMenuState = function () {
      menuToggle.setAttribute('aria-expanded', String(menuInput.checked));
    };
    menuInput.addEventListener('change', updateMenuState);
    menuToggle.addEventListener('keydown', function (event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        menuInput.click();
      }
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuInput.checked) {
        menuInput.checked = false;
        updateMenuState();
        menuToggle.focus();
      }
    });
    updateMenuState();
  }
  var sharedRoadmap = window.GermanyRoadmapReturn;
  if (sharedRoadmap) {
    document.querySelectorAll('.site-header a[href], .hero-actions a[href]').forEach(function (link) { link.href = sharedRoadmap.chapterWithContext(link.href, location.search); });
    window.__SDB_SEARCH_URL__ = sharedRoadmap.chapterWithContext(new URL(window.__SDB_SEARCH_URL__ || '/search.html', location.href).href, location.search);
  }
  var content = document.querySelector('.post-content');
  if (!content) return;
  var authoredTitle = content.querySelector('h1');
  var header = document.querySelector('.post-header');
  var inferredTitle = header && header.querySelector('.post-title');
  var normalizeInferredTitle = function (value) {
    var decoder = document.createElement('textarea');
    decoder.innerHTML = value.replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return decoder.value.trim().replace(/\s+/g, ' ');
  };
  if (authoredTitle && inferredTitle &&
      authoredTitle.textContent.trim().replace(/\s+/g, ' ') ===
        normalizeInferredTitle(inferredTitle.textContent)) {
    header.hidden = true;
  }
  var roadmap = window.GermanyRoadmapReturn;
  if (roadmap) content.querySelectorAll('a[href]').forEach(function (link) {
    link.href = roadmap.chapterWithContext(link.href, window.location.search);
  });
  var state = window.StudyState, paths = window.StudyPublishedPaths || [];
  var published = state && state.publishedPath(location.pathname, paths);
  var learning = published && state.isLearningPath(published);
  var revision = published && /\/REVISION\.html$/i.test(published);
  if (!learning && !revision) return;
  if (content.dataset.studyReader) return;
  content.dataset.studyReader = 'true';
  function headingText(element) {
    var copy = element.cloneNode(true);
    copy.querySelectorAll('.heading-anchor').forEach(function (anchor) { anchor.remove(); });
    return copy.textContent.trim();
  }
  var titleRow = content.querySelector('.chapter-title-row');
  if (!titleRow && authoredTitle) {
    titleRow = document.createElement('div'); titleRow.className = 'chapter-title-row'; authoredTitle.before(titleRow); titleRow.append(authoredTitle);
  }
  var badges = Array.from(content.children).filter(function (p) { return p.tagName === 'P' && (titleRow || authoredTitle) && (p.compareDocumentPosition(titleRow || authoredTitle) & Node.DOCUMENT_POSITION_FOLLOWING) && p.querySelector('img[src*="img.shields.io/badge/"]'); });
  var values = {};
  badges.forEach(function (p) { p.querySelectorAll('img').forEach(function (img) {
    var match = decodeURIComponent(img.src).match(/\/badge\/(section|category|read--time|role--priority)-(.+)-[^-]+$/);
    if (match) values[match[1]] = match[2].replace(/--/g, '-').replace(/_/g, ' ');
  }); });
  var meta = document.createElement('div'); meta.className = 'reader-meta';
  var line = document.createElement('span'); line.textContent = [values.section, values['role--priority'], values['read--time'] && values['read--time'] + ' read'].filter(Boolean).join(' · '); meta.append(line);
  if (badges.length) {
    var details = document.createElement('details'); details.className = 'chapter-details';
    var summary = document.createElement('summary'); summary.textContent = 'Chapter details'; details.append(summary);
    badges.forEach(function (p) { details.append(p); }); meta.append(details);
  }
  if (titleRow) titleRow.after(meta); else content.prepend(meta);
  var breadcrumb = document.createElement('nav'); breadcrumb.className = 'reader-breadcrumb'; breadcrumb.setAttribute('aria-label', 'Breadcrumb');
  var dirs = location.pathname.split('/').filter(Boolean); dirs.pop();
  var library = document.createElement('a'); library.href = '/INDEX.html'; library.textContent = 'Library'; breadcrumb.append(library);
  dirs.forEach(function (dir, index) {
    var target = '/' + dirs.slice(0, index + 1).join('/') + '/INDEX.html';
    if (!paths.includes(target)) return;
    var link = document.createElement('a'); link.href = target;
    link.textContent = index === 1 && values.section ? values.section : dir.replace(/^\d+(?:\.\d+)*-/, '').split('-').map(function (word) { return word === 'and' ? '&' : word.charAt(0).toUpperCase() + word.slice(1); }).join(' ');
    var separator = document.createElement('span'); separator.textContent = '/'; separator.setAttribute('aria-hidden', 'true'); breadcrumb.append(separator, link);
  });
  if (roadmap) {
    var back = document.createElement('a'); back.className = 'roadmap-return'; back.href = roadmap.roadmapReturnUrl(location.search);
    var hasContext = roadmap.context(location.search);
    back.textContent = hasContext ? 'Return to personal roadmap' : 'Personal roadmap';
    if (hasContext) breadcrumb.append(back); else content.append(back);
  }
  if (roadmap) breadcrumb.querySelectorAll('a[href]').forEach(function (link) { link.href = roadmap.chapterWithContext(link.href, location.search); });
  content.prepend(breadcrumb);
  if (learning) {
    var widthLabel = document.createElement('label'); widthLabel.className = 'reading-width'; widthLabel.append(document.createTextNode('Width '));
    var width = document.createElement('select'); width.setAttribute('aria-label', 'Reading width');
    ['Wide', 'Comfortable'].forEach(function (label) { var option = document.createElement('option'); option.value = label.toLowerCase(); option.textContent = label; width.append(option); });
    try { if (localStorage.getItem('sdb-reading-width') === 'comfortable') width.value = 'comfortable'; } catch (_) {}
    content.dataset.width = width.value;
    width.addEventListener('change', function () { content.dataset.width = width.value; try { localStorage.setItem('sdb-reading-width', width.value); } catch (_) {} });
    widthLabel.append(width);
    var toolbar = content.querySelector('.read-aloud');
    if (toolbar) toolbar.append(widthLabel); else if (titleRow) titleRow.append(widthLabel);
    var sourceLinks = Array.from(content.querySelectorAll('a[href]'));
    function available(link) { try { var url = new URL(link.href); return url.origin === location.origin && paths.includes(url.pathname); } catch (_) { return false; } }
    var next = sourceLinks.find(function (link) { return /^Next:/i.test(link.textContent.trim()) && available(link); });
    var review = sourceLinks.find(function (link) { return /\/REVISION\.html$/i.test(new URL(link.href).pathname) && available(link); });
    var summaryHeading = Array.from(content.querySelectorAll('h2')).find(function (h) { return headingText(h) === 'Summary'; });
    if (summaryHeading && (next || review)) {
      var continuation = document.createElement('nav'); continuation.className = 'study-continuation'; continuation.setAttribute('aria-label', 'Continue studying');
      if (review) { var revisionLink = document.createElement('a'); revisionLink.href = review.href; revisionLink.textContent = 'Review this category'; continuation.append(revisionLink); }
      if (next) { var nextLink = document.createElement('a'); nextLink.href = next.href; nextLink.textContent = next.textContent.trim(); continuation.append(nextLink); }
      var following = summaryHeading.nextElementSibling;
      while (following && !/^H[12]$/.test(following.tagName)) following = following.nextElementSibling;
      if (following) following.before(continuation); else content.append(continuation);
    }
  }
  content.querySelectorAll('div.highlighter-rouge').forEach(function (block) {
    if (block.querySelector('.code-caption')) return;
    var language = Array.from(block.classList).find(function (name) { return name.indexOf('language-') === 0; });
    if (!language) return;
    var names = {javascript: 'JavaScript', typescript: 'TypeScript', jsx: 'JSX', tsx: 'TSX', json: 'JSON', html: 'HTML', css: 'CSS', sql: 'SQL', plaintext: 'Plain text'};
    var value = language.slice(9), caption = document.createElement('span'); caption.className = 'code-caption';
    caption.textContent = names[value] || value.charAt(0).toUpperCase() + value.slice(1); block.prepend(caption);
  });
  var headings = Array.from(content.querySelectorAll('h2[id]'));
  if (!headings.length) return;
  var outline = document.createElement('details'); outline.className = 'chapter-outline';
  var outlineSummary = document.createElement('summary'); outlineSummary.textContent = 'On this page';
  var nav = document.createElement('nav'); nav.setAttribute('aria-label', 'Chapter sections');
  var list = document.createElement('ul');
  var links = headings.map(function (heading) {
    var item = document.createElement('li'), link = document.createElement('a');
    link.textContent = headingText(heading); link.href = '#' + heading.id;
    link.addEventListener('click', function () {
      heading.setAttribute('tabindex', '-1'); heading.focus({preventScroll: true});
      document.dispatchEvent(new CustomEvent('study:section', {detail: {heading: heading, deliberate: true}}));
    });
    item.append(link); list.append(item); return link;
  });
  nav.append(list); outline.append(outlineSummary, nav);
  var layout = document.createElement('div'); layout.className = 'reader-layout'; content.before(layout); layout.append(content, outline);
  var desktop = window.matchMedia('(min-width: 1200px)');
  function syncOutline() {
    if (desktop.matches) layout.append(outline); else meta.after(outline);
    outline.open = desktop.matches;
  }
  syncOutline(); if (desktop.addEventListener) desktop.addEventListener('change', syncOutline);
  var scheduled = false;
  function currentSection() {
    scheduled = false;
    var current = headings[0];
    headings.forEach(function (heading) { if (heading.getBoundingClientRect().top <= 150) current = heading; });
    links.forEach(function (link, index) { if (headings[index] === current) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    document.dispatchEvent(new CustomEvent('study:section', {detail: {heading: current, deliberate: false}}));
  }
  window.addEventListener('scroll', function () { if (!scheduled) { scheduled = true; requestAnimationFrame(currentSection); } }, {passive: true});
  currentSection();
});
