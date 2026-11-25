  document.addEventListener("DOMContentLoaded", function() {
    // Ensure main content has ID for skip link
    var mainContent = document.querySelector('.post-content, .page-content, .search-main');
    if (mainContent && !mainContent.id) {
      mainContent.id = 'main-content';
    }

    // 1. Reading progress indicator
    var progressBar = document.createElement("div");
    progressBar.className = "reading-progress-bar";
    document.body.appendChild(progressBar);

    var updateProgress = function() {
      var winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      var scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      progressBar.style.width = scrolled + "%";
    };
    window.addEventListener("scroll", updateProgress, { passive: true });

    // 2. Back to top button
    var btt = document.createElement("button");
    btt.className = "back-to-top";
    btt.setAttribute("aria-label", "Back to top");
    btt.setAttribute("title", "Back to top");
    btt.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"></path><path d="m5 12 7-7 7 7"></path></svg>';
    document.body.appendChild(btt);

    window.addEventListener("scroll", function() {
      var scrollPos = document.documentElement.scrollTop || document.body.scrollTop;
      if (scrollPos > 350) {
        btt.classList.add("visible");
      } else {
        btt.classList.remove("visible");
      }
    }, { passive: true });

    btt.addEventListener("click", function() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // 3. Responsive table container wrapper. A shell keeps the edge fade
    // outside the scrolling surface; the wrapper itself is the keyboard-
    // focusable scroll region only while the table actually overflows.
    var tables = document.querySelectorAll(".post-content table, .page-content table");
    var markTableOverflow = function(shell, wrapper) {
      var max = wrapper.scrollWidth - wrapper.clientWidth;
      var scrollable = max > 4;
      shell.classList.toggle("is-scrollable", scrollable);
      shell.classList.toggle("at-start", wrapper.scrollLeft <= 2);
      shell.classList.toggle("at-end", !scrollable || wrapper.scrollLeft >= max - 2);
      if (scrollable) {
        wrapper.setAttribute("tabindex", "0");
        wrapper.setAttribute("role", "region");
        wrapper.setAttribute("aria-label", "Table, scroll horizontally for more columns");
      } else {
        wrapper.removeAttribute("tabindex");
        wrapper.removeAttribute("role");
        wrapper.removeAttribute("aria-label");
      }
    };
    tables.forEach(function(table) {
      if (table.parentElement.classList.contains("table-scroll-wrapper")) return;
      var wrapper = document.createElement("div");
      wrapper.className = "table-scroll-wrapper";
      var shell = document.createElement("div");
      shell.className = "table-scroll-shell";
      table.parentNode.insertBefore(shell, table);
      shell.appendChild(wrapper);
      wrapper.appendChild(table);
      var fade = document.createElement("span");
      fade.className = "table-scroll-fade";
      fade.setAttribute("aria-hidden", "true");
      shell.appendChild(fade);
      var update = function() { markTableOverflow(shell, wrapper); };
      wrapper.addEventListener("scroll", update, { passive: true });
      window.addEventListener("resize", update, { passive: true });
      requestAnimationFrame(update);
    });

    // 4. Code block copy buttons — quiet circular icon actions (copy → check);
    // the live-region feedback span stays for assistive tech.
    var codeContainers = document.querySelectorAll("div.highlighter-rouge, pre.highlight");
    var copyIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="11" height="12" rx="2.5"></rect><path d="M5 15V5.5A2.5 2.5 0 0 1 7.5 3H16"></path></svg>';
    var copiedIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m4 12.5 5 5L20 6.5"></path></svg>';
    var languageNames = {
      javascript: 'JavaScript', typescript: 'TypeScript', jsx: 'JSX', tsx: 'TSX',
      json: 'JSON', html: 'HTML', css: 'CSS', sql: 'SQL', python: 'Python',
      bash: 'Bash', shell: 'Shell', sh: 'Shell', go: 'Go', rust: 'Rust',
      java: 'Java', cpp: 'C++', c: 'C', ruby: 'Ruby', php: 'PHP',
      swift: 'Swift', kotlin: 'Kotlin', dart: 'Dart', yaml: 'YAML',
      markdown: 'Markdown', dockerfile: 'Dockerfile', text: 'Plain text',
      plaintext: 'Plain text'
    };
    codeContainers.forEach(function(container) {
      if (container.tagName === "PRE" && container.closest("div.highlighter-rouge")) return;
      var pre = container.tagName === "PRE" ? container : container.querySelector("pre");
      if (!pre || container.querySelector(".copy-code-btn")) return;

      if (!container.querySelector('.code-caption')) {
        var language = Array.from(container.classList).find(function (name) { return name.indexOf('language-') === 0; });
        if (language) {
          var value = language.slice(9);
          var label = languageNames[value] || value.charAt(0).toUpperCase() + value.slice(1);
          var caption = document.createElement('span');
          caption.className = 'code-caption';
          caption.textContent = label + ':';
          container.prepend(caption);
        }
      }

      var btn = document.createElement("button");
      btn.className = "copy-code-btn";
      btn.type = "button";
      btn.setAttribute("aria-label", "Copy code");
      btn.innerHTML = copyIcon;
      var feedback = document.createElement("span");
      feedback.className = "copy-feedback";
      feedback.setAttribute("role", "status");
      feedback.setAttribute("aria-live", "polite");

      btn.addEventListener("click", function() {
        feedback.textContent = "";
        var code = pre.querySelector("code") || pre;
        var text = code.innerText || code.textContent;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function() {
            btn.innerHTML = copiedIcon;
            btn.setAttribute("aria-label", "Code copied");
            btn.classList.add("copied");
            feedback.textContent = "Code copied to clipboard.";
            feedback.classList.add("visible");
            setTimeout(function() {
              btn.innerHTML = copyIcon;
              btn.setAttribute("aria-label", "Copy code");
              btn.classList.remove("copied");
              feedback.classList.remove("visible");
            }, 2000);
          }).catch(function() {
            btn.setAttribute("aria-label", "Copy failed");
            feedback.textContent = "Copy failed. Select the code and copy it manually.";
            feedback.classList.add("visible");
          });
        } else {
          feedback.textContent = "Clipboard access is unavailable. Select the code and copy it manually.";
          feedback.classList.add("visible");
        }
      });

      container.appendChild(btn);
      container.appendChild(feedback);

      // Show a quiet right-edge fade only while the code is wider than the
      // reading column. It disappears at the end so the cue never lies.
      if (container.tagName !== "PRE") {
        var syncCodeOverflow = function() {
          var max = pre.scrollWidth - pre.clientWidth;
          var scrollable = max > 4;
          container.classList.toggle("is-scrollable", scrollable);
          container.classList.toggle("is-at-end", !scrollable || pre.scrollLeft >= max - 2);
        };
        pre.addEventListener("scroll", syncCodeOverflow, { passive: true });
        window.addEventListener("resize", syncCodeOverflow, { passive: true });
        requestAnimationFrame(syncCodeOverflow);
      }
    });

    // 5. GitHub Alert / Callout transform (> [!NOTE], > [!TIP], etc.)
    var alertMeta = {
      NOTE: { title: "Note", icon: "", cls: "alert-note" },
      TIP: { title: "Tip", icon: "", cls: "alert-tip" },
      IMPORTANT: { title: "Important", icon: "", cls: "alert-important" },
      WARNING: { title: "Warning", icon: "", cls: "alert-warning" },
      CAUTION: { title: "Caution", icon: "", cls: "alert-caution" }
    };

    var blockquotes = document.querySelectorAll("blockquote");
    blockquotes.forEach(function(bq) {
      var firstP = bq.querySelector("p");
      if (!firstP) return;
      var rawHtml = firstP.innerHTML.trim();
      var match = rawHtml.match(/^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\s*<br\s*\/?>|\s*\n|\s+)?([\s\S]*)$/i);
      if (match) {
        var alertType = match[1].toUpperCase();
        var info = alertMeta[alertType];
        if (info) {
          bq.classList.add("markdown-alert", info.cls);
          var header = document.createElement("div");
          header.className = "alert-title";
          header.innerHTML = '<span class="alert-icon">' + info.icon + '</span> ' + info.title;
          firstP.innerHTML = match[2];
          bq.insertBefore(header, firstP);
        }
      }
    });

    // 6. Chapter bottom pagination styling
    var contentParas = document.querySelectorAll(".post-content p, .page-content p");
    contentParas.forEach(function(p) {
      var text = p.textContent.trim();
      if ((text.indexOf("Previous:") !== -1 || text.indexOf("Next:") !== -1) &&
          (text.indexOf("Index") !== -1 || text.indexOf("Back to Index") !== -1)) {
        p.classList.add("chapter-nav-footer");
        // The inline dot is a text node; in a wrapping flex row it becomes an
        // orphaned flex item. Make it one element the narrow layout can hide.
        Array.prototype.slice.call(p.childNodes).forEach(function(node) {
          if (node.nodeType !== 3 || node.textContent.indexOf("·") === -1) return;
          var parts = node.textContent.split("·");
          var fragment = document.createDocumentFragment();
          parts.forEach(function(part, index) {
            if (index) {
              var separator = document.createElement("span");
              separator.className = "chapter-nav-separator";
              separator.setAttribute("aria-hidden", "true");
              separator.textContent = "·";
              fragment.appendChild(separator);
            }
            fragment.appendChild(document.createTextNode(part));
          });
          p.replaceChild(fragment, node);
        });
      }
    });

    // 7. Toast notification helper
    var showToast = function(msg) {
      var toast = document.querySelector(".sdb-toast");
      if (!toast) {
        toast = document.createElement("div");
        toast.className = "sdb-toast";
        document.body.appendChild(toast);
      }
      toast.textContent = msg;
      toast.classList.add("show");
      if (window._toastTimeout) clearTimeout(window._toastTimeout);
      window._toastTimeout = setTimeout(function() {
        toast.classList.remove("show");
      }, 2200);
    };

    // 8. Heading anchor permalinks (#) with copy on click
    var headings = document.querySelectorAll(".post-content h2, .post-content h3, .post-content h4, .page-content h2, .page-content h3, .page-content h4");
    headings.forEach(function(h) {
      if (!h.id) {
        h.id = h.textContent.trim().toLowerCase()
          .replace(/[^\w\s-]/g, "")
          .replace(/\s+/g, "-");
      }
      if (!h.id || h.querySelector(".heading-anchor")) return;
      var headingName = h.textContent.trim();
      if (!h.hasAttribute("aria-label") && !h.hasAttribute("aria-labelledby")) h.setAttribute("aria-label", headingName);
      var anchor = document.createElement("a");
      anchor.className = "heading-anchor";
      anchor.href = "#" + h.id;
      anchor.setAttribute("aria-label", "Permalink to " + headingName);
      anchor.title = "Copy link to this section";
      anchor.innerHTML = "#";
      anchor.addEventListener("click", function(e) {
        e.preventDefault();
        var url = window.location.origin + window.location.pathname + "#" + h.id;
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(url).then(function() {
            showToast("Copied section link to clipboard");
          });
        }
        try {
          history.pushState(null, "", "#" + h.id);
        } catch (err) {}
        h.scrollIntoView({ behavior: "smooth" });
      });
      h.insertBefore(anchor, h.firstChild);
    });

    // 9. Search navigation badge & global keyboard shortcut (Cmd+K / Ctrl+K / '/')
    var searchLinks = document.querySelectorAll('.site-nav a[href*="search"]');
    searchLinks.forEach(function(link) {
      if (!link.querySelector(".search-shortcut-badge")) {
        var badge = document.createElement("span");
        badge.className = "search-shortcut-badge";
        badge.textContent = "⌘K";
        link.appendChild(badge);
      }
    });

    document.addEventListener("keydown", function(e) {
      var target = e.target;
      var isInput = target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable);
      if (isInput) return;

      var isCmdK = (e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K");
      var isSlash = e.key === "/" && !e.metaKey && !e.ctrlKey && !e.altKey;
      if (isCmdK || isSlash) {
        e.preventDefault();
        var headerSearch = document.getElementById("header-topic");
        var currentPath = window.location.pathname;
        if (/\/search(?:\.html)?$/.test(currentPath)) {
          var searchInput = document.getElementById("q");
          if (searchInput) {
            searchInput.focus();
            searchInput.select();
          }
        } else if (headerSearch) {
          headerSearch.focus();
          headerSearch.select();
        } else {
          var targetUrl = window.__SDB_SEARCH_URL__ || "/search.html";
          window.location.href = targetUrl;
        }
      }
    });
  });
