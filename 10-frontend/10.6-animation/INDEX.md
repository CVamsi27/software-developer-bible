# Animation — Index

> **8 files** — Web animation techniques from Framer Motion and CSS animations to Web Animations API, GSAP, React Spring, View Transitions API, Canvas/SVG rendering, and curated interview questions.

[![Files](https://img.shields.io/badge/files-8-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why animation:** Senior frontend interviews increasingly include animation questions (micro-interactions, transitions, performance). Modern apps use animation to communicate state, guide attention, and provide feedback. Pick the right tool: CSS for simple, Framer Motion for React, GSAP for complex sequences, Web Animations API for imperative control.

---

## Topic Categories

| Category | Files | When to use | Read time |
|----------|------:|-------------|----------:|
| [CSS-Native](#css-native) | 1 | Simple transitions, @keyframes, hover effects | 25 min |
| [JS Libraries](#js-libraries) | 4 | Complex animations, spring physics, timeline sequences | 2 hrs |
| [Platform APIs](#platform-apis) | 3 | Native browser animation control, view transitions, Canvas/SVG | 1.5 hr |
| [Interview Prep](#interview-prep) | 1 | 30+ Qs | 2 hrs |

---

## CSS-Native

The fastest, cheapest animation. Use this first.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [CSS Animations](10.6.01-css-animations.md) | Transitions, @keyframes, transform, will-change, prefers-reduced-motion | 25 min |

**When to use:** Hover effects, simple state transitions, loading spinners. No JS needed; GPU-accelerated; respects `prefers-reduced-motion` for free.

---

## JS Libraries

For complex animations.

| # | File | Topics | When to use | Read time |
|--:|------|--------|-------------|----------:|
| 02 | [Framer Motion](10.6.02-framer-motion.md) | motion components, AnimatePresence, layout (FLIP), useScroll, gestures | React 18+, default for component animations | 45 min |
| 03 | [GSAP](10.6.03-gsap.md) | Timelines, ScrollTrigger, easings, plugins (Flip, SplitText, MorphSVG) | Complex sequences, scroll-driven, marketing sites | 30 min |
| 04 | [React Spring](10.6.04-react-spring.md) | Spring physics, useSpring/useTrail/useTransition/useChain, animated.* | Physics-based animations (when spring > easing) | 25 min |
| 05 | [Web Animations API](10.6.05-web-animations-api.md) | element.animate, keyframes, play/pause/reverse, finish, getAnimations | Imperative control, fine-grained timeline control | 30 min |

**Decision tree:**

```text
Need animation?
├── Simple hover/state change? ──→ CSS transitions
├── Loop / auto-play? ──→ CSS @keyframes (or WAAPI)
├── React component entering/leaving/animating layout? ──→ Framer Motion
├── Spring physics (natural-feeling bounce)? ──→ React Spring
├── Marketing site with complex timelines? ──→ GSAP
├── Need imperative control, not React? ──→ WAAPI
├── Multi-page transition (Next.js)? ──→ View Transitions API
└── Hundreds+ of elements / pixel work? ──→ Canvas (or SVG below ~500)
```

---

## Platform APIs

Newer browser-native capabilities.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 06 | [View Transitions & Scroll-Driven](10.6.06-view-transitions-and-scroll-driven-animations.md) | `startViewTransition`, `view-transition-name`, `animation-timeline: scroll()/view()` | 30 min |
| 07 | [Canvas & SVG Animation](10.6.07-canvas-svg-animation.md) | rAF loop with delta time, canvas 2D + devicePixelRatio, `stroke-dashoffset` draw-on, SMIL deprecation, performance envelope (DOM vs SVG vs Canvas), OffscreenCanvas workers, React rAF cleanup | 35 min |

---

## Interview Prep

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 08 | [Interview Questions](10.6.08-interview-questions.md) | 30+ questions covering CSS, WAAPI, libraries, perf, a11y | 2 hrs |

---

## Suggested Study Order

1. **CSS Animations** (25 min) — the foundation
2. **Framer Motion** (45 min) — the React default
3. **Web Animations API** (30 min) — for the interview "what's under the hood"
4. **View Transitions** (30 min) — modern Next.js
5. **Canvas & SVG** (35 min) — when element counts leave the DOM
6. **GSAP + React Spring** — as needed
7. **Interview Questions** (2 hrs)

---

## Performance & Accessibility

Animation has two non-negotiable constraints:

1. **Performance** — animate `transform` and `opacity` only (GPU-accelerated). Avoid animating `top`, `left`, `width`, `height` (triggers layout).
2. **Accessibility** — always respect `prefers-reduced-motion: reduce`. Disable or reduce non-essential animations.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

```typescript
// Framer Motion
const prefersReducedMotion = useReducedMotion();
const animateProps = prefersReducedMotion ? {} : { scale: 1.1 };
```

---

## Cross-References

- [Accessibility](../../50-quality/50.2-accessibility/INDEX.md) — `prefers-reduced-motion`
- [Next.js](../10.4-next.js/INDEX.md) — View Transitions API
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — animation perf
- [React](../10.3-react/INDEX.md) — Framer Motion is React-native

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
|------------------------|-----------------|
| CSS animations (`@keyframes`) | `packages/ui/src/styles/globals.css` - pulse/shimmer/shake/fade-up keyframes with `prefers-reduced-motion` media blocks |
| `prefers-reduced-motion` in JS | `packages/hooks/src/use-prefers-reduced-motion.ts` - matchMedia hook plus a reduced-motion scroll-behavior helper |

_Framer Motion, GSAP, React Spring, WAAPI, View Transitions, and Canvas/SVG animation: no direct docita implementation yet._

---

## Navigation

[← Previous: Form Handling](../10.5-form-handling/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Node.js →](../../20-backend/20.1-node.js/INDEX.md)
