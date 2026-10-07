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
  var content = document.querySelector('.post-content');
  if (!content) return;
  var authoredTitle = content.querySelector('h1');
  var header = document.querySelector('.post-header');
  var inferredTitle = header && header.querySelector('.post-title');
  if (authoredTitle && inferredTitle &&
      authoredTitle.textContent.trim() === inferredTitle.textContent.trim()) {
    header.hidden = true;
  }
  if (content.querySelector('.chapter-outline')) return;
  var headings = Array.from(content.querySelectorAll('h2[id]'));
  if (headings.length < 4) return;
  var outline = document.createElement('details');
  outline.className = 'chapter-outline';
  var summary = document.createElement('summary');
  summary.textContent = 'In this chapter';
  var nav = document.createElement('nav');
  nav.setAttribute('aria-label', 'Chapter sections');
  var list = document.createElement('ul');
  headings.forEach(function (heading) {
    var copy = heading.cloneNode(true);
    copy.querySelectorAll('.heading-anchor').forEach(function (a) { a.remove(); });
    var item = document.createElement('li'), link = document.createElement('a');
    link.textContent = copy.textContent.trim();
    link.href = '#' + heading.id;
    link.addEventListener('click', function () {
      heading.setAttribute('tabindex', '-1');
      heading.focus({preventScroll: true});
    });
    item.append(link); list.append(item);
  });
  nav.append(list); outline.append(summary, nav);
  var titleRow = content.querySelector('.chapter-title-row');
  var player = content.querySelector('.read-aloud');
  var title = content.querySelector('h1');
  if (titleRow) titleRow.after(outline);
  else if (player) player.after(outline);
  else if (title) title.after(outline);
  else content.prepend(outline);
});
