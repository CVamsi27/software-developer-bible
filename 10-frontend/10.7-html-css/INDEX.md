# HTML/CSS & PWA — Index

> **Study time:** ≈ 1 h 26 m of reading (8 files, ~11 min average).
> **7 files** — HTML fundamentals, CSS layout, CSS architecture, theming/design tokens, PWA, SEO, and browser rendering — the foundational web platform skills every senior frontend engineer needs.

[![Files](https://img.shields.io/badge/files-7-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why this matters:** Even with React/Next.js, you need HTML/CSS fluency. Semantic HTML, accessibility, responsive design, and browser rendering are foundational. PWAs and SEO are increasingly important for product companies. Senior interviews still test these — "draw a layout", "explain critical rendering path", "what's the difference between LCP and INP".

---

## Topic Categories

| Category | Files | Why it matters |
| -------------------------------------------------------- | ----: | ------------------------------------------------------------------------------------------ |
| [HTML](#html) | 1 | Semantic HTML, forms, accessibility, ARIA, HTML5 APIs |
| [CSS](#css) | 1 | Flexbox, Grid, responsive design, CSS variables, modern CSS |
| [CSS Architecture & Theming](#css-architecture--theming) | 2 | Cascade layers, BEM/CUBE/ITCSS, Modules vs CSS-in-JS vs Tailwind, design tokens, dark mode |
| [Browser Internals](#browser-internals) | 1 | Critical rendering path, reflow vs repaint, GPU acceleration |
| [PWA & SEO](#pwa--seo) | 2 | Service workers, offline support, Core Web Vitals, structured data |

---

## HTML

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [HTML Fundamentals](10.7.01-html-fundamentals.md) | Semantic HTML, forms, accessibility, ARIA, HTML5 APIs, microdata | 7 min |

---

## CSS

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 02 | [CSS Fundamentals](10.7.02-css-fundamentals.md) | Flexbox, Grid, responsive design, media queries, container queries, CSS variables, `:has()` | 9 min |

---

## CSS Architecture & Theming

Styling at scale: how you structure, name, and theme.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 06 | [CSS Architecture & Styling Approaches](10.7.06-css-architecture-styling-approaches.md) | Cascade layers (`@layer`), specificity management, BEM, CUBE CSS, ITCSS, CSS Modules vs CSS-in-JS vs Tailwind decision matrix, stylelint governance, migration strategies | 11 min |
| 07 | [Theming & Design Tokens](10.7.07-theming-design-tokens.md) | Primitive vs semantic tokens, custom-property theming, `prefers-color-scheme` + manual toggle, FOUC prevention, `data-theme` scoping, token distribution (Tailwind/CSS-in-JS), WCAG contrast recap | 13 min |
| 08 | [Interview Questions](10.7.08-interview-questions.md) | 6 senior Q&A: margin collapsing, stacking contexts, flex-vs-grid, rendering cost model, semantic a11y, CSS architecture at scale | 4 min |

---

## Browser Internals

How the browser turns HTML/CSS/JS into pixels.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 03 | [Browser Rendering](10.7.03-browser-rendering.md) | Critical rendering path, reflow vs repaint vs composite, layout thrashing, GPU acceleration, layers | 13 min |

---

## PWA & SEO

Production concerns.

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 05 | [PWA](10.7.05-pwa.md) | Service workers, caching strategies (cache-first, network-first), background sync, push notifications, install prompt, manifest | 18 min |
| 04 | [SEO](10.7.04-seo.md) | Core Web Vitals (LCP/INP/CLS), structured data (JSON-LD), meta tags, OG tags, sitemap, robots.txt, SSR vs CSR for SEO | 11 min |

---

## Suggested Study Order

1. **HTML Fundamentals** (30 min) — semantic HTML is the foundation
2. **CSS Fundamentals** (45 min) — Flexbox + Grid for layout
3. **CSS Architecture & Styling Approaches** (35 min) — scale without specificity wars
4. **Theming & Design Tokens** (30 min) — dark mode done right
5. **Browser Rendering** (30 min) — the mental model for performance
6. **SEO** (30 min) — Core Web Vitals
7. **PWA** (30 min) — if relevant to the JD

---

## Common interview topics

- "Draw a layout for X" (Flexbox/Grid)
- "What's the difference between LCP and INP?" (Core Web Vitals)
- "How does the browser render a page?" (critical rendering path)
- "How do you make a site accessible?" (semantic HTML, ARIA, keyboard)
- "How would you implement dark mode without a theme flash?" (tokens + pre-paint script)
- "CSS Modules vs Tailwind vs CSS-in-JS — how do you choose?" (runtime cost, SSR/RSC, tokens)
- "What's a service worker?" (PWA)
- "How do you optimize for SEO?" (SSR, structured data, meta tags)

---

## Cross-References

- [Accessibility](../../50-quality/50.2-accessibility/INDEX.md) — the deep-dive on WCAG, ARIA, screen readers
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — Core Web Vitals measurement
- [React](../10.3-react/INDEX.md) — JSX is just HTML
- [Next.js](../10.4-next.js/INDEX.md) — SSR/SSG for SEO
- [Animation](../10.6-animation/INDEX.md) — CSS animations

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

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
