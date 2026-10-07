<!-- section: HTML/CSS | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-HTML/CSS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../docs/topic-importance.md)

# Html Css — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## HTML Fundamentals — Semantic HTML, Forms, Accessibility

Source: [HTML Fundamentals — Semantic HTML, Forms, Accessibility](10.7.01-html-fundamentals.md)

**Q:** Why is a clickable div not equivalent to a button?

**A:** A button supplies semantics, keyboard behavior, focus and disabled/form behavior. Reimplementing those correctly is more work than using the appropriate native element.

## CSS Fundamentals — Grid, Flexbox, Responsive Design, Variables

Source: [CSS Fundamentals — Grid, Flexbox, Responsive Design, Variables](10.7.02-css-fundamentals.md)

**Q:** Why can a layered rule lose even with a more specific selector?

**A:** Cascade origin, importance and layer precedence are resolved before specificity. Normal unlayered author rules outrank normal layered rules; important layer ordering reverses.

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

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
