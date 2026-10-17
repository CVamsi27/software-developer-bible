/*
 * Color theme — the single owner of the `sdb-theme` preference.
 *
 * Every page loads this file: Jekyll pages through `_includes/head-custom.html`
 * and the generated search page through `scripts/gen_master_index.py`. The key,
 * the pre-paint application and the toggle wiring exist here and nowhere else;
 * `scripts/check_verify_wiring.py` (rule 13) fails the build if the key appears
 * in any other source file. Comments in the two consumers explain the wiring —
 * they must not restate this logic.
 *
 * Loaded without `defer`/`async` from `<head>` so a stored choice is applied
 * before the first paint (no flash of the wrong palette), and the toggle is
 * wired on DOMContentLoaded.
 */
(function () {
  var savedTheme;
  try { savedTheme = localStorage.getItem("sdb-theme"); } catch (_) {}
  if (savedTheme === "dark" || savedTheme === "light") {
    document.documentElement.setAttribute("data-theme", savedTheme);
  }
})();

document.addEventListener("DOMContentLoaded", function () {
  // The search page ships a #theme-btn in its markup; Jekyll pages have no
  // button, so one is created and placed beside the site navigation.
  var themeBtn = document.getElementById("theme-btn");
  var created = false;
  if (!themeBtn) {
    themeBtn = document.createElement("button");
    themeBtn.className = "theme-toggle-btn";
    themeBtn.type = "button";
    themeBtn.setAttribute("aria-label", "Toggle color theme");
    themeBtn.setAttribute("title", "Toggle dark/light mode");
    created = true;
  }

  var updateThemeColorMeta = function (theme) {
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute("content", theme === "dark" ? "#0d1720" : "#f8fafc");
    }
  };

  var updateThemeIcon = function (theme) {
    themeBtn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    themeBtn.setAttribute("title", themeBtn.getAttribute("aria-label"));
    if (theme === "dark") {
      themeBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>';
    } else {
      themeBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>';
    }
  };

  var getCurrentEffectiveTheme = function () {
    var explicit = document.documentElement.getAttribute("data-theme");
    if (explicit) return explicit;
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  };

  var initialTheme = getCurrentEffectiveTheme();
  updateThemeIcon(initialTheme);
  updateThemeColorMeta(initialTheme);

  var systemTheme = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)");
  if (systemTheme && systemTheme.addEventListener) {
    systemTheme.addEventListener("change", function () {
      if (document.documentElement.hasAttribute("data-theme")) return;
      var effective = getCurrentEffectiveTheme();
      updateThemeIcon(effective);
      updateThemeColorMeta(effective);
    });
  }

  themeBtn.addEventListener("click", function () {
    var current = getCurrentEffectiveTheme();
    var next = current === "dark" ? "light" : "dark";
    document.documentElement.setAttribute("data-theme", next);
    updateThemeIcon(next);
    updateThemeColorMeta(next);
    try { localStorage.setItem("sdb-theme", next); } catch (_) {}
  });

  if (!created) return;
  var siteNav = document.querySelector(".site-nav");
  var headerWrapper = document.querySelector(".site-header .wrapper");
  var headerSearch = headerWrapper && headerWrapper.querySelector(".header-search");
  var phoneHeader = window.matchMedia && window.matchMedia("(max-width: 700px)");
  var placeThemeButton = function () {
    var hadFocus = document.activeElement === themeBtn;
    var brand = headerWrapper && headerWrapper.querySelector(".site-title");
    if (headerSearch) {
      var sibling = phoneHeader && phoneHeader.matches && brand ? brand : headerSearch;
      sibling.insertAdjacentElement("afterend", themeBtn);
    } else if (siteNav && siteNav.parentNode) {
      siteNav.insertAdjacentElement("afterend", themeBtn);
    } else if (headerWrapper) {
      headerWrapper.appendChild(themeBtn);
    }
    if (hadFocus) themeBtn.focus({preventScroll: true});
  };
  placeThemeButton();
  if (phoneHeader && phoneHeader.addEventListener) phoneHeader.addEventListener("change", placeThemeButton);
});
