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
    // A disclosure that stays open after a pointer moves elsewhere reads as
    // stuck; close it from anywhere outside the navigation.
    document.addEventListener('click', function (event) {
      if (!menuInput.checked || event.target.closest('.site-nav')) return;
      menuInput.checked = false;
      updateMenuState();
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
  [['section', values.section], ['priority', values['role--priority']], ['time', values['read--time'] && values['read--time'] + ' read']].forEach(function (entry) {
    if (!entry[1]) return;
    var token = document.createElement('span'); token.className = 'reader-meta-' + entry[0]; token.textContent = entry[1]; meta.append(token);
  });
  if (badges.length) {
    var details = document.createElement('details'); details.className = 'chapter-details';
    var summary = document.createElement('summary'); summary.textContent = 'Chapter details'; details.append(summary);
    badges.forEach(function (p) { details.append(p); }); meta.append(details);
  }
  if (titleRow) titleRow.after(meta); else content.prepend(meta);
  var breadcrumb = document.createElement('nav'); breadcrumb.className = 'reader-breadcrumb'; breadcrumb.setAttribute('aria-label', 'Breadcrumb');
  var dirs = location.pathname.split('/').filter(Boolean); dirs.pop();

  dirs.forEach(function (dir, index) {
    var target = '/' + dirs.slice(0, index + 1).join('/') + '/INDEX.html';
    if (!paths.includes(target)) return;
    var link = document.createElement('a'); link.href = target;
    link.textContent = index === 1 && values.section ? values.section : dir.replace(/^\d+(?:\.\d+)*-/, '').split('-').map(function (word) { return word === 'and' ? '&' : word.charAt(0).toUpperCase() + word.slice(1); }).join(' ');
    if (breadcrumb.children.length) { var separator = document.createElement('span'); separator.textContent = '/'; separator.setAttribute('aria-hidden', 'true'); breadcrumb.append(separator); } breadcrumb.append(link);
  });
  if (roadmap && roadmap.context(location.search)) {
    var back = document.createElement('a'); back.className = 'roadmap-return'; back.href = roadmap.roadmapReturnUrl(location.search);
    back.textContent = 'Return to personal roadmap';
    breadcrumb.append(back);
  }
  if (roadmap) breadcrumb.querySelectorAll('a[href]').forEach(function (link) { link.href = roadmap.chapterWithContext(link.href, location.search); });
  content.prepend(breadcrumb);
  if (learning) {
    var widthLabel = document.createElement('label'); widthLabel.className = 'reading-width'; widthLabel.append(document.createTextNode('Width '));
    var width = document.createElement('select'); width.setAttribute('aria-label', 'Reading width');
    ['Comfortable', 'Wide'].forEach(function (label) { var option = document.createElement('option'); option.value = label.toLowerCase(); option.textContent = label; width.append(option); });
    // Comfortable measure is the default; an explicit Wide choice sticks.
    try { if (localStorage.getItem('sdb-reading-width') === 'wide') width.value = 'wide'; } catch (_) {}
    content.dataset.width = width.value;
    width.addEventListener('change', function () { content.dataset.width = width.value; try { localStorage.setItem('sdb-reading-width', width.value); } catch (_) {} });
    widthLabel.append(width);
    var toolbar = content.querySelector('.read-aloud');
    if (toolbar) toolbar.append(widthLabel); else if (titleRow) titleRow.append(widthLabel);
    // Chapter navigation stays in its single authored home at the end of the
    // chapter. Mirroring the same Next/revision links after Summary duplicated
    // both controls and split one onward choice across two surfaces.
  }
  content.querySelectorAll('div.highlighter-rouge').forEach(function (block) {
    if (block.querySelector('.code-caption')) return;
    var language = Array.from(block.classList).find(function (name) { return name.indexOf('language-') === 0; });
    if (!language) return;
    var names = {javascript: 'JavaScript', typescript: 'TypeScript', jsx: 'JSX', tsx: 'TSX', json: 'JSON', html: 'HTML', css: 'CSS', sql: 'SQL', plaintext: 'Plain text'};
    var value = language.slice(9), caption = document.createElement('span'); caption.className = 'code-caption';
    var label = names[value] || value.charAt(0).toUpperCase() + value.slice(1);
    caption.textContent = label + ':'; block.prepend(caption);
    var code = block.querySelector('pre code');
    if (code) {
      var numbers = document.createElement('span'); numbers.className = 'code-line-numbers'; numbers.setAttribute('aria-hidden', 'true');
      var pre = block.querySelector('pre'); pre.setAttribute('tabindex', '0'); pre.setAttribute('role', 'region'); pre.setAttribute('aria-label', label + ' code');
      var count = code.textContent.replace(/\n$/, '').split('\n').length;
      numbers.textContent = Array.from({length: count}, function (_, index) { return index + 1; }).join('\n');
      block.querySelector('pre').before(numbers); block.classList.add('has-line-numbers');
    }
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
      if (!window.matchMedia('(min-width: 1200px)').matches) outline.open = false;
      heading.setAttribute('tabindex', '-1'); heading.focus({preventScroll: true});
      document.dispatchEvent(new CustomEvent('study:section', {detail: {heading: heading, deliberate: true}}));
    });
    item.append(link); list.append(item); return link;
  });
  nav.append(list); outline.append(outlineSummary, nav);
  var layout = document.createElement('div'); layout.className = 'reader-layout'; content.before(layout); layout.append(content, outline);
  var desktop = window.matchMedia('(min-width: 1200px)');
  outlineSummary.addEventListener('click', function (event) { if (desktop.matches) event.preventDefault(); });
  function syncOutline() {
    if (desktop.matches) layout.append(outline); else meta.after(outline);
    outline.open = desktop.matches;
    if (desktop.matches) outlineSummary.setAttribute('tabindex', '-1'); else outlineSummary.removeAttribute('tabindex');
  }
  syncOutline(); if (desktop.addEventListener) desktop.addEventListener('change', syncOutline);
  var scheduled = false;
  function currentSection() {
    scheduled = false;
    var current = headings[0];
    headings.forEach(function (heading) { if (heading.getBoundingClientRect().top <= 150) current = heading; });
    var pageHeight = document.documentElement.scrollHeight;
    if (pageHeight > window.innerHeight && window.scrollY + window.innerHeight >= pageHeight - 2) current = headings[headings.length - 1];
    links.forEach(function (link, index) { if (headings[index] === current) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    document.dispatchEvent(new CustomEvent('study:section', {detail: {heading: current, deliberate: false}}));
  }
  window.addEventListener('scroll', function () { if (!scheduled) { scheduled = true; requestAnimationFrame(currentSection); } }, {passive: true});
  currentSection();
});
