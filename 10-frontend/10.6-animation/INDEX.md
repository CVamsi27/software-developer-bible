# Animation — Index

> **Study time:** ≈ 1 h 2 m of reading (9 files, ~7 min average).
> **9 files** — CSS and browser animation APIs, Motion for React (formerly Framer Motion), GSAP, React Spring, Canvas/SVG rendering, and interview practice.

[![Files](https://img.shields.io/badge/files-9-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Frontend-00b4d8)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Animation should explain a change: a panel opened, a list reordered, a task is progressing. Start with the browser cost of that change, then choose the control and lifecycle you need.

This stack is **Optional for the current full-stack preparation**. Skip library-specific depth while prioritizing core implementation and system design; keep reduced-motion and accessibility requirements when working with existing motion. See [topic priorities](../../docs/topic-importance.md).

## Pass 1 — connect visual changes to browser work

Read [CSS Animations](10.6.01-css-animations.md) for transitions, keyframes and reduced-motion alternatives. Follow with [Web Animations API](10.6.05-web-animations-api.md) to control playback and cancellation from JavaScript. CSS effects need an explicit reduced-motion policy; the browser does not supply one automatically.

Explain why an eligible transform animation can avoid repeated layout/paint, and why choosing transform still does not guarantee a frame rate.

## Pass 2 — choose how the interaction is controlled

| Interaction | Chapter | Mechanism to understand | Role priority | General importance |
| ----------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------- | ------------- | ------------------ |
| React entry, exit, gestures or reordered layout | [Motion for React](10.6.02-framer-motion.md) | Target interpolation, presence retention and layout projection | Optional | Specialized |
| Deliberate sequences with overlapping tracks | [GSAP](10.6.03-gsap.md) | Timeline ownership and cleanup | Optional | Specialized |
| Interruptible spring values | [React Spring](10.6.04-react-spring.md) | A changing target and a continuing physical state | Optional | Specialized |

These tools overlap. Build one small interaction and explain why its needed control justifies the tool; a simple hover can remain a CSS transition.

## Pass 3 — follow navigation, scroll and drawing lifecycles

[View Transitions & Scroll-Driven Animations](10.6.06-view-transitions-and-scroll-driven-animations.md) connects transitions to navigation or scroll progress. Distinguish same-document router changes from actual document navigation before choosing an integration.

[Canvas & SVG Animation](10.6.07-canvas-svg-animation.md) compares retained graphics with pixels your application redraws. Choose using interaction, accessibility and measured rendering cost; no fixed element-count threshold decides for every scene. SVG animation/SMIL remains supported.

## Finish with revision, then interview practice

Choose one effect and trace its input, state change, DOM/drawing updates, cancellation and cleanup. Show its reduced-motion alternative and usable API fallback. Use [section revision](REVISION.md) to recall these mechanisms, then [interview questions](10.6.08-interview-questions.md) to defend the design under changed requirements.

## Cross-References

- [Accessibility](../../50-quality/50.2-accessibility/INDEX.md) — focus, motion and keyboard behavior
- [Browser Rendering](../10.7-html-css/10.7.03-browser-rendering.md) — layout, painting and compositing
- [Performance Monitoring](../../50-quality/50.3-performance-monitoring/INDEX.md) — performance evidence
- [React](../10.3-react/INDEX.md) — component identity and lifecycle

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS API + React/Astro apps, TypeScript monorepo). Study the chapter, then find it in the repo:

| Topic in this category | Docita evidence |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| CSS animations (`@keyframes`) | `packages/ui/src/styles/globals.css` - pulse/shimmer/shake/fade-up keyframes with `prefers-reduced-motion` media blocks |
| `prefers-reduced-motion` in JS | `packages/hooks/src/use-prefers-reduced-motion.ts` - matchMedia hook plus a reduced-motion scroll-behavior helper |

_Motion for React, GSAP, React Spring, WAAPI, View Transitions, and Canvas/SVG animation: no direct Docita implementation yet._

---

## Navigation

[← Previous: Form Handling](../10.5-form-handling/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: HTML/CSS & PWA →](../10.7-html-css/INDEX.md)
