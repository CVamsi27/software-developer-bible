# HTML/CSS & PWA — Index

> **Study time:** ≈ 1 h 2 m of reading (10 files, ~6 min average).
> **10 files** — HTML fundamentals, CSS layout, CSS architecture, theming/design tokens, browser storage, PWA, SEO, and browser rendering — the foundational web platform skills every senior frontend engineer needs.

[![Files](https://img.shields.io/badge/files-10-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

A web page starts as meaningful content, receives a layout, turns into pixels, and may retain data across reloads. Read these chapters in that causal order so each API has a job inside the whole page.

For the current full-stack path, complete the HTML/CSS fundamentals first. Browser rendering/storage and working style architecture follow; PWA, SEO and deep theming are optional specialization. See [topic priorities](../../docs/topic-importance.md).

## Pass 1 — give content meaning and position

[HTML Fundamentals](10.7.01-html-fundamentals.md) explains semantic elements, forms and accessible relationships. Then [CSS Fundamentals](10.7.02-css-fundamentals.md) shows how the cascade selects styles and Flexbox/Grid position content.

Build a form that still has labels, submission behavior and understandable errors before adding a framework. Explain which layout axis each rule controls.

## Pass 2 — follow styles into pixels and shared decisions

[Browser Rendering](10.7.03-browser-rendering.md) traces style calculation, layout, paint and composition. Use that model when evaluating a slow interaction.

[CSS Architecture & Styling Approaches](10.7.06-css-architecture-styling-approaches.md) assigns ownership and precedence to growing stylesheets. [Theming & Design Tokens](10.7.07-theming-design-tokens.md) connects visual roles to values and distinguishes a user's chosen theme from the effective system theme.

## Pass 3 — decide what survives navigation and reload

[Browser Storage](10.7.08-browser-storage.md) compares stores by data model, access, lifetime and failure behavior. An HttpOnly cookie protects against direct script reads, but the complete session design must also address requests, CSRF and script injection.

[PWA](10.7.05-pwa.md) adds a service-worker lifecycle, app-managed Cache API rules and offline behavior alongside the separate HTTP cache. Trace which responses are safe to store and how queued work becomes acknowledged server state.

## Pass 4 — make public pages discoverable

[SEO](10.7.04-seo.md) follows crawling, rendering and indexing. Evaluate public URLs, status codes, genuine navigation links and useful content before metadata or optional rich-result features. SSR and structured data do not guarantee indexing or ranking.

## Finish with revision, then interview practice

Trace a page from accessible markup through layout, paint, storage and reload. Explain its behavior when optional APIs or persistence fail. Use [section revision](REVISION.md) to recall the mechanisms, then [interview questions](10.7.09-interview-questions.md) to compare alternatives.

## Cross-References

- [Accessibility](../../50-quality/50.2-accessibility/INDEX.md) — WCAG, ARIA and practical verification
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — loading and interaction evidence
- [React](../10.3-react/INDEX.md) — component rendering and DOM behavior
- [Next.js](../10.4-next.js/INDEX.md) — server rendering, caching and routing
- [Animation](../10.6-animation/INDEX.md) — visual updates and lifecycle
- [Security](../../20-backend/20.5-security/INDEX.md) — server-side session and authorization mechanisms

---

## Docita Anchor

Examples in [Docita](https://github.com/CVamsi27/docita), a healthcare-platform repository with a NestJS API and React/Astro apps in a TypeScript monorepo. Study the chapter, then locate the implementation:

| Topic in this category | Docita evidence |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Theming & design tokens | `packages/ui/src/styles/globals.css` - oklch semantic token system with dark-variant overrides |
| Tailwind architecture | `packages/ui/tailwind.config.ts` - CSS-variable color bridge and `darkMode: class + data-theme` |
| Accessibility auditing | `scripts/perf/accessibility-audit.ts` - Playwright + axe violation reports per app/page |
| PWA service worker | `apps/app/src/components/pwa/pwa-register.tsx` - prod-only SW registration; precached shell + offline fallback in `apps/app/public/sw.js` |
| SEO meta tags | `apps/landing/src/layouts/main-layout.astro` - title/description/canonical/OG metadata in the marketing layout |

---

## Navigation

[← Previous: Animation](../10.6-animation/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Mobile →](../10.8-mobile/INDEX.md)
