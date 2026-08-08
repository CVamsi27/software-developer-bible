---
section: Animation
category: Frontend
tags: [interview-questions, practice]
---

# Animation Interview Questions

> 30+ curated questions on animation in web development — from CSS basics to React animation patterns, performance, and accessibility.

## Definition

This guide covers the questions a senior full-stack engineer should be able to answer about web animation — CSS transitions/keyframes, Web Animations API, React animation libraries, performance, and accessibility. Grouped by difficulty.

## Why It Matters (TL;DR)

- **UX skill** — animation is a key differentiator in product quality
- **Performance** — animations impact perceived and actual performance
- **Accessibility** — must be inclusive (vestibular disorders, screen readers)
- **Library fluency** — interviewers expect knowledge of Framer Motion, GSAP, etc.

## Answer Framework

```text
ANSWER STRUCTURE:
  1. Definition        (CSS / WAAPI / library)
  2. How it works      (compositor, transform/opacity)
  3. Implementation    (code example)
  4. Performance       (GPU vs CPU, jank, will-change)
  5. Accessibility     (prefers-reduced-motion, focus)
```

## Beginner

**Q1: What is the difference between CSS transitions and `@keyframes` animations?**

A: A **transition** animates between two states (start → end) when something changes (e.g., `:hover`, class change, JS). A **`@keyframes`** animation is multi-step, can loop, delay, and play without any state change. Transitions are for two-state reactions; `@keyframes` are for declarative sequences.

**Q2: What is the `transform` property and which values are GPU-accelerated?**

A: `transform` applies 2D/3D transformations to an element: `translate`, `scale`, `rotate`, `skew`, `matrix`. All `transform` values are GPU-accelerated — animated on the compositor thread, no layout, no paint. This is the foundation of performant web animation.

**Q3: How do you create a hover effect?**

A: Use `transition` to interpolate a property and change it on `:hover`:

```css
.button {
  background: blue;
  transition: transform 0.3s ease, background 0.3s ease;
}
.button:hover {
  background: darkblue;
  transform: translateY(-2px);
}
```

**Q4: What is hardware acceleration?**

A: Using the GPU instead of the CPU for rendering. Achieved by animating `transform` and `opacity` (composited on the GPU) instead of layout-triggering properties (`width`, `top`, `margin`). The result: smoother animations, less main-thread work.

**Q5: What is `will-change`?**

A: A CSS hint that tells the browser which properties will animate, so it can pre-optimize (create a compositor layer, allocate GPU memory). Use sparingly — overuse consumes GPU memory and slows down the page. Remove after the animation completes.

**Q6: What are CSS animation properties?**

A: `animation-name`, `animation-duration`, `animation-timing-function`, `animation-delay`, `animation-iteration-count`, `animation-direction`, `animation-fill-mode`, `animation-play-state`. Combined into the shorthand: `animation: name duration timing delay iter dir fill state`.

## Intermediate

**Q7: How do you create a CSS keyframe animation?**

A: Define keyframes with `@keyframes`, then apply via `animation` property:

```css
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
.fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}
```

**Q8: What is `animation-fill-mode`?**

A: Defines how styles apply before and after the animation:
- `none` — element reverts to its base state when not animating
- `forwards` — element retains the final state after the animation
- `backwards` — element gets the first keyframe styles during delay
- `both` — applies both forwards and backwards

**Q9: How do you optimize CSS animations for performance?**

A: (1) Animate `transform` and `opacity` only (GPU). (2) Use `will-change` sparingly. (3) Avoid animating layout-triggering properties (`width`, `height`, `top`, `left`, `margin`, `padding`, `box-shadow`). (4) Use `contain: layout` or `contain: paint` to scope the reflow. (5) Respect `prefers-reduced-motion`.

**Q10: What is the FLIP technique?**

A: First, Last, Invert, Play — a technique for animating between two layout states smoothly: (1) capture initial position (`First`), (2) apply the new layout, capture final position (`Last`), (3) compute the delta, apply `transform: translate(dx, dy)` to revert to the initial position (`Invert`), (4) remove the transform with a transition to animate to the natural position (`Play`). Framer Motion's `layout` prop does this automatically.

**Q11: How do you handle animations in responsive design?**

A: (1) Use `clamp()` for fluid sizing in keyframes. (2) Use media queries to reduce animation distance/duration on small screens. (3) Always respect `prefers-reduced-motion`. (4) Test on touch devices — gestures change animation needs.

**Q12: What is the Web Animations API (WAAPI)?**

A: A browser-native JavaScript API for controlling animations: `element.animate(keyframes, options)` returns an `Animation` object with `.play()`, `.pause()`, `.reverse()`, `.cancel()`, `.finish()`, `.currentTime`. Combines the power of CSS animations with JS control, runs on the compositor thread for 60fps.

## Senior

**Q13: What is Framer Motion and when do you reach for it?**

A: A React animation library with declarative API (`<motion.div>`), built-in gestures (`whileHover`, `whileTap`, `drag`), `<AnimatePresence>` for exit animations, `layout` prop for FLIP transitions, `useScroll` for scroll-linked animations. Reach for it when: React app, complex state-driven animations, gesture support needed, layout transitions, or scroll-linked motion.

**Q14: How does Framer Motion achieve good performance?**

A: (1) Animates `transform` and `opacity` by default — GPU-accelerated. (2) Style projection — only the changed style updates, no React re-render. (3) `useMotionValue` lets you read values without re-rendering. (4) Hardware acceleration with `will-change` applied automatically. (5) RAF batching for smooth updates.

**Q15: Framer Motion vs React Spring?**

A:
- **Framer Motion** — simpler API, layout animations, gestures, declarative. Good default for React.
- **React Spring** — physics-based springs, more natural motion, supports React Native. Better for organic motion; harder to learn.

**Q16: How do you implement page transitions in React?**

A: Use `<AnimatePresence mode="wait">` with a `key` on the route element:

```typescript
<AnimatePresence mode="wait">
  <motion.div
    key={pathname}
    initial={{ opacity: 0, x: -20 }}
    animate={{ opacity: 1, x: 0 }}
    exit={{ opacity: 0, x: 20 }}
    transition={{ duration: 0.25 }}
  >
    {children}
  </motion.div>
</AnimatePresence>
```

In Next.js App Router, wrap in a client component and place in the root layout. With view transitions (modern browsers), you can also use the View Transitions API.

**Q17: How do you make animations accessible?**

A: (1) Respect `prefers-reduced-motion: reduce` — disable or shorten animations. (2) Don't animate essential UI (focus rings, form validation feedback). (3) Avoid flashing > 3 times per second (photosensitive epilepsy). (4) Provide a way to pause long animations. (5) Keep transitions short (< 400ms for UI). (6) Ensure animations don't trap focus or block keyboard nav.

**Q18: What causes animation jank and how do you fix it?**

A: **Causes**: (1) Animating layout-triggering properties. (2) Long-running JS competing for main thread. (3) Excessive DOM manipulation. (4) Large images / videos. **Fixes**: (1) Animate transform/opacity only. (2) Use `requestAnimationFrame` or offload to Web Workers. (3) Virtualize long lists. (4) Use `content-visibility: auto` for off-screen content. (5) Reduce animation count.

**Q19: How do you create scroll-triggered animations?**

A: Three options: (1) **Intersection Observer** — observe an element, animate when it enters the viewport. (2) **Scroll event + `requestAnimationFrame`** — manual, throttled. (3) **CSS Scroll-Driven Animations** — `@keyframes` tied to `scroll()` / `view()` progress. (4) **Framer Motion** `useScroll` + `useTransform` — declarative scroll-linked values. (5) **GSAP ScrollTrigger** — full-featured, pin / scrub / batch.

**Q20: How do you test animations?**

A: (1) Visual regression — Playwright screenshots before/after. (2) Frame rate measurement — `requestAnimationFrame` counter, `Performance API`. (3) Manual testing on real devices (especially low-end Android). (4) E2E test: assert on final state. (5) Storybook for visual review. (6) Performance budget in CI (Lighthouse).

**Q21: How do you handle animations in SSR (Next.js, Remix)?**

A: (1) CSS animations work in SSR — they're just styles. (2) JS animation libraries (Framer Motion) need client-side hydration — use `'use client'` directive. (3) Use `dynamic()` to lazy-load heavy animation code. (4) The View Transitions API is browser-native — works in SSR-rendered pages. (5) Disable initial animations for users with `prefers-reduced-motion`.

**Q22: How do you animate complex sequences?**

A: Three options: (1) **`@keyframes` with `animation-delay`** — declarative, no JS. (2) **Framer Motion variants + `staggerChildren`** — declarative for React. (3) **GSAP timeline** — imperative, very flexible, scrub / pause / reverse / pin. (4) **Web Animations API** — `animation.commitStyles()` for sequenced triggers.

## FAANG-style

**Q23: Design an animation system for a design system.**

A:
- **Tokens** — durations (instant, fast, normal, slow), easings (ease-out, ease-in-out), distances (small, medium, large) as CSS variables
- **Primitives** — `<Transition>` component, `<Fade>`, `<Slide>`, `<Scale>` wrappers
- **Variants** — defined states (idle, hover, focus, active, disabled) per component
- **Utilities** — `useReducedMotion()` hook, `useAnimate()` for imperative
- **Performance budgets** — max 200ms for UI, 400ms for page transitions
- **Accessibility** — `prefers-reduced-motion` always respected
- **Documentation** — Storybook for each state
- **Testing** — visual regression + performance monitoring

**Q24: How would you optimize animations for low-end devices?**

A: (1) Detect via `navigator.hardwareConcurrency` (≤ 2 cores = low-end) or `navigator.deviceMemory` (≤ 2GB). (2) Reduce animation count and duration. (3) Replace `box-shadow` with `border` or `outline`. (4) Skip `filter` effects. (5) Use `content-visibility: auto` for off-screen. (6) Disable parallax and complex transforms. (7) Test on a $200 Android with throttled CPU.

**Q25: Explain animation performance monitoring.**

A:
- **Frame rate** — measure with `requestAnimationFrame` loop; target 60fps (16.6ms per frame). Tools: Chrome DevTools Performance panel, `PerformanceObserver` API.
- **Long Tasks** — `PerformanceObserver({ entryTypes: ['longtask'] })` catches tasks > 50ms.
- **Core Web Vitals** — INP (Interaction to Next Paint) measures responsiveness, including animation delays.
- **Frame budget** — 16.6ms total per frame for 60fps. Animation work + JS work must fit.
- **Lighthouse** — measures animation-heavy pages, flags jank.

**Q26: How do you handle animations in micro-frontends?**

A: (1) **Consistent animation tokens** — share CSS variables across micro-frontends. (2) **Shared animation library** — single dependency to avoid bundle bloat and version conflicts. (3) **Module Federation** — load the animation library once, share. (4) **Style isolation** — scoped CSS or shadow DOM to prevent animation leakage. (5) **Performance budget** — per micro-frontend; total page must stay under budget.

**Q27: Design a page transition system for a multi-page app.**

A:
- **Trigger** — `usePathname()` or router event
- **Library** — Framer Motion `<AnimatePresence>` (React), View Transitions API (vanilla)
- **Modes** — `wait` (one at a time), `popLayout`, `sync`
- **Variants** — `initial`, `animate`, `exit` per page
- **Loading state** — animate a skeleton between route changes
- **Error boundary** — cancel transition, show error inline
- **Reduced motion** — instant transition, no animation
- **A11y** — `aria-live="polite"` on the transition region so screen readers announce the change

## Follow-ups

**Q28: How do you handle animations in React Server Components?**

A: (1) CSS animations work in RSC — they're just CSS. (2) JS animation libraries (Framer Motion) need client components (`'use client'`). (3) Wrap motion components in a client component and import into the server tree. (4) Initial state can be passed from server; runtime animations are client-side.

**Q29: How do you handle animations with third-party libraries?**

A: (1) Check if they expose `data-` attributes or CSS classes for animation hooks. (2) Wrap them in a client component with Framer Motion. (3) Use `useReducedMotion` to disable for accessibility. (4) Test that the library's internal animations also respect the motion preference (not all do).

**Q30: How do you handle animation performance at scale?**

A: (1) **Performance budgets** in CI (Lighthouse CI) — fail the build if budgets exceeded. (2) **Real User Monitoring** (RUM) — track INP, frame rate, jank in production. (3) **Animation inventory** — document all animations with rationale and performance impact. (4) **Code review checklist** — every animation PR must show: GPU-only properties, will-change usage, reduced-motion fallback, performance test.

**Q31: How do you handle animations in different browsers?**

A: (1) Vendor prefixes (rarely needed in 2026 — Autoprefixer handles it). (2) Feature detect with `@supports`. (3) Fallback to `transition` for browsers without `@keyframes`. (4) Test in Safari, Firefox, Chrome, Edge. (5) Use `autoprefixer` PostCSS plugin in your build.

**Q32: How do you handle animations with content changes?**

A: (1) Use `layout` (Framer Motion) for FLIP-style layout transitions. (2) Use `useTransition` (React 19) to keep the old UI while the new renders. (3) Animate list reorders with `LayoutGroup`. (4) Use `key` changes to trigger AnimatePresence exit/enter. (5) View Transitions API for cross-document transitions.

## Key Concepts to Master

| Concept | Key Points |
|---------|------------|
| CSS Transitions | Two-state, triggered by class / pseudo / JS |
| `@keyframes` | Multi-step, loops, delays |
| Transform / Opacity | GPU-accelerated; always prefer |
| `will-change` | Hint, not a free pass; use sparingly |
| `prefers-reduced-motion` | Accessibility — always handle |
| Framer Motion | React declarative; `AnimatePresence`, `layout`, `useScroll` |
| GSAP | Imperative timelines, ScrollTrigger, robust |
| React Spring | Physics-based, natural motion |
| Web Animations API | Native JS API, compositor-thread |
| View Transitions API | Cross-document transitions (modern) |
| Scroll-Driven Animations | CSS-only, `animation-timeline: scroll()` |

## Common Follow-up Questions

- "How would you implement this in production?"
- "What are the performance implications?"
- "How do you handle accessibility?"
- "What are the alternatives?"
- "How do you test this?"
- "How do you handle reduced motion?"

## Summary

- Animation is a senior-level UX skill — know CSS, JS APIs, and React libraries
- Always animate `transform` and `opacity` for 60fps
- Respect `prefers-reduced-motion` for accessibility
- Modern stack: Framer Motion for React, GSAP for complex sequences, View Transitions for native cross-page
- Test on low-end devices, monitor INP in production

---

## Cheat Sheet

```text
ANIMATION INTERVIEW CHEAT SHEET
═══════════════════════════════════════════════════════════════

ANSWER FRAMEWORK:
  1. CSS / WAAPI / library
  2. Compositor / transform / opacity
  3. Implementation (CSS or code)
  4. Performance (GPU, will-change, jank)
  5. Accessibility (prefers-reduced-motion)

CHOOSE BY USE CASE:
  Hover / focus / simple state    → CSS transition
  Multi-step sequence             → @keyframes
  Gestures (drag, swipe)          → Framer Motion / GSAP
  Layout changes                  → Framer Motion layout (FLIP)
  Page transitions                → AnimatePresence / View Transitions
  Scroll-linked                   → useScroll / ScrollTrigger / @scroll-timeline
  Physics-based                   → React Spring

PERFORMANCE RULES:
  • Animate transform / opacity only
  • will-change sparingly, remove after
  • Respect prefers-reduced-motion
  • Avoid animating during heavy JS

INTERVIEW WINNERS:
  - Mention FLIP technique (Framer Motion's `layout` prop)
  - Bring up View Transitions API for cross-document
  - Discuss prefers-reduced-motion handling
  - Reference CSS scroll-driven animations (animation-timeline)
  - Talk about GPU vs CPU properties
```

---

## See Also

- [Accessibility](../25-Accessibility/)
- [CSS Animations](02-CSS-Animations.md)
- [Framer Motion](01-Framer-Motion.md)
- [GSAP](05-GSAP.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [React Spring](06-React-Spring.md)
- [View Transitions & Scroll-Driven Animations](07-View-Transitions-and-Scroll-Driven-Animations.md)
- [Web Animations API](04-Web-Animations-API.md)


## References & Learn More

- [CSS Triggers](https://csstriggers.com/)
- [Framer Motion](https://motion.dev/)
- [GSAP](https://gsap.com/)
- [MDN CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [MDN CSS Transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions)
- [MDN Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [View Transitions API (Chrome)](https://developer.chrome.com/docs/web-platform/view-transitions/)
- [web.dev Animations Guide](https://web.dev/animations/)
