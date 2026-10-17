<!-- section: HTML/CSS | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-HTML/CSS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../docs/topic-importance.md)

# HTML/CSS — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## HTML Fundamentals — Semantic HTML, Forms, Accessibility

Source: [HTML Fundamentals — Semantic HTML, Forms, Accessibility](10.7.01-html-fundamentals.md)

**Q:** Why is a clickable div not equivalent to a button?

**A:** A button supplies semantics, keyboard behavior, focus and disabled/form behavior. Reimplementing those correctly is more work than using the appropriate native element.

## CSS Fundamentals — Grid, Flexbox, Responsive Design, Variables

Source: [CSS Fundamentals — Grid, Flexbox, Responsive Design, Variables](10.7.02-css-fundamentals.md)

**Q:** Why can a layered rule lose even with a more specific selector?

**A:** Cascade origin, importance and layer precedence are resolved before specificity. Normal unlayered author rules outrank normal layered rules; important layer ordering reverses.

**Q:** Why should DOM order remain meaningful when a flex or grid layout visually reorders items?

**A:** Visual placement does not rewrite source order. `reading-flow` can adjust sequential reading/navigation in supporting browsers, but it has limited availability; keep the source order sensible as the fallback and verify the actual browser and assistive technology.

## Browser Rendering — Critical Rendering Path, Reflow, Paint

Source: [Browser Rendering — Critical Rendering Path, Reflow, Paint](10.7.03-browser-rendering.md)

**Q:** What causes layout thrashing in a read/write loop?

**A:** A layout-dependent read after a style write may force synchronous layout repeatedly. Batch reads before writes and confirm the cost in a performance trace.

## SEO — Meta Tags, Structured Data, Core Web Vitals

Source: [SEO — Meta Tags, Structured Data, Core Web Vitals](10.7.04-seo.md)

**Q:** Why does valid structured data not guarantee a rich search result?

**A:** Eligibility, content policies and search-engine decisions still apply. Validate the markup and rendered content without promising a particular display or ranking.

## Progressive Web Apps (PWA) — Service Workers, Manifest, Offline

Source: [Progressive Web Apps (PWA) — Service Workers, Manifest, Offline](10.7.05-pwa.md)

**Q:** Why may skipWaiting create a compatibility problem for open tabs?

**A:** The new worker can control pages loaded with old assets or data assumptions. Design update activation and cache lifetime for mixed versions.

**Q:** When is it safe to delete an offline write from IndexedDB?

**A:** After the server acknowledges the result for that stable operation ID. The server must atomically enforce idempotency so a retry after a lost response returns the committed outcome; authentication, conflict and validation failures need foreground recovery.

## CSS Architecture & Styling Approaches

Source: [CSS Architecture & Styling Approaches](10.7.06-css-architecture-styling-approaches.md)

**Q:** Why do cascade layers help governance without replacing naming or tokens?

**A:** They make precedence explicit across style sources. They do not define component boundaries, semantic values or safe migration by themselves.

## Theming & Design Tokens

Source: [Theming & Design Tokens](10.7.07-theming-design-tokens.md)

**Q:** Why should dark mode switch semantic tokens rather than individual component colors?

**A:** Components retain their intent while the palette changes centrally. Each theme still needs contrast, native-control and persisted-preference verification.

## Browser Storage

Source: [Browser Storage](10.7.08-browser-storage.md)

**Q:** What protection does an HttpOnly cookie provide, and what remains?

**A:** JavaScript cannot directly read that cookie. XSS may still act as the user, and cookie-based requests still require an appropriate CSRF and authorization design.

## Tailwind CSS — Utility-First Styling with Design Tokens

Source: [Tailwind CSS — Utility-First Styling with Design Tokens](10.7.09-tailwind-css.md)

**Q:** Why does changing one brand color require only the config file, not every component?

**A:** Components reference semantic roles (`bg-surface`, `text-error`) defined in `tailwind.config.ts`; updating a token rebuilds every element that uses it.

**Q:** Why can a class written at runtime (`bg-${color}-500`) produce missing styles?

**A:** The JIT compiler scans static class strings in the configured `content` paths; concatenated classes are invisible unless safelisted.

**Q:** Why prefer extracting repeated utility lists into components instead of `@apply`?

**A:** `@apply` hides the token chain and the compiled output; components keep tokens visible in markup while removing repetition.

## Trace reload, metadata and layout conditions

Source: [HTML](10.7.01-html-fundamentals.md), [CSS](10.7.02-css-fundamentals.md), [SEO](10.7.04-seo.md), [PWA](10.7.05-pwa.md), [Themes](10.7.07-theming-design-tokens.md), [Storage](10.7.08-browser-storage.md)

**Q:** A labeled input lacks name. What happens on ordinary form submission?
**A:** The label still names it for interaction/accessibility, but it supplies no named entry in FormData. Label association and submitted key have different jobs.

**Q:** Why can a flex child overflow despite flex:1?
**A:** Its automatic minimum can preserve a long content width. Inspect min-width and wrapping/overflow; min-width:0 permits shrinking but does not itself wrap content.

**Q:** Does a canonical link redirect the visitor to the preferred URL?
**A:** No. It is a search processing signal. An HTTP redirect performs navigation, and consistency with internal links/sitemaps supports canonical identity.

**Q:** How do you handle app updates in a PWA?
**A:** Installation and activation are separate. An installed update may wait while old clients remain; default waiting or an explicit accepted activation protocol must preserve asset/data compatibility. skipWaiting does not itself reload pages or guarantee safety.

**Q:** When would you use cache-first vs network-first?
**A:** Use a cache-first rule for suitable immutable/public assets, and network-first only for deliberately cacheable data with defined stale fallback. Private healthcare responses require identity, retention and device-security policy; no strategy name grants permission to store them.

**Q:** Why can precached HTML still fail on offline reload?
**A:** Its referenced scripts/styles must also be stored and served by matching fetch rules. A manifest or cached document alone does not provide the whole shell.

**Q:** Why does choosing system differ from storing dark?
**A:** System is a policy that follows later OS changes. Dark is an explicit choice; store the policy separately from the effective root appearance.

**Q:** A request write succeeded but its IndexedDB transaction aborted. Is the draft saved?
**A:** No. Report success only after transaction completion; request success is not the final commit acknowledgment.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
