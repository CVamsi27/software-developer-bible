---
section: Animation
category: Frontend
tags: [concept, reference]
---

# View Transitions API & CSS Scroll-Driven Animations

> Two modern browser APIs that are reshaping web animation: the **View Transitions API** for native cross-page / state-change transitions, and **CSS scroll-driven animations** for declarative scroll-linked effects without JavaScript. Both are the 2026 frontier for high-quality motion.

## Definition

The **View Transitions API** is a browser-native API that animates between DOM states. Triggered by `document.startViewTransition()`, it captures the old state, applies the new state, and cross-fades with optional per-element transforms. **CSS scroll-driven animations** let you bind `@keyframes` to scroll progress using `animation-timeline: scroll()` (axis) or `view()` (visibility) — no JavaScript required.

## Why It Matters (TL;DR)

- **View Transitions** — SPA-like page transitions with one API call, no library
- **Scroll-driven animations** — CSS-only scroll effects, no scroll listener
- **Performance** — compositor-thread, GPU-accelerated
- **No library** — modern browser APIs, zero bundle cost
- **Senior interview topic** — these are the cutting-edge primitives for 2026

## View Transitions API

### How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                VIEW TRANSITIONS API FLOW                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Old State              document.startViewTransition(() => {        │
│  ┌──────┐               ┌──────┐                                    │
│  │      │  snapshot  →  │ old  │                                    │
│  │      │               └──────┘                                    │
│  └──────┘                    │                                      │
│                              ▼                                      │
│                        DOM update                                    │
│                              │                                      │
│                              ▼                                      │
│  New State              ┌──────┐                                    │
│  ┌──────┐    animate →  │ new  │   → composite + cross-fade         │
│  │      │               └──────┘                                    │
│  └──────┘                                                            │
│                                                                     │
│  view-transition-name lets you animate per-element transforms       │
│  (e.g., shared element transitions).                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Code Examples

#### 1. Basic Cross-Page Transition (Multi-Page App)

```javascript
// Trigger on a link click
document.addEventListener('click', (e) => {
  const link = (e.target as HTMLElement).closest('a');
  if (!link || link.target === '_blank') return;
  if (e.metaKey || e.ctrlKey) return;

  e.preventDefault();
  const url = link.href;

  document.startViewTransition(async () => {
    // Fetch and swap content
    const res = await fetch(url);
    const html = await res.text();
    const doc = new DOMParser().parseFromString(html, 'text/html');
    document.body.innerHTML = doc.body.innerHTML;
    history.pushState(null, '', url);
  });
});
```

#### 2. SPA Route Change (React)

```tsx
import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function useViewTransition() {
  const location = useLocation();

  useEffect(() => {
    if (!document.startViewTransition) return;
    document.startViewTransition(() => {
      // Trigger re-render
      window.scrollTo(0, 0);
    });
  }, [location.pathname]);
}
```

#### 3. Shared Element Transition

```css
/* CSS — give the same view-transition-name to source and target */
.card-grid .card {
  view-transition-name: card-1;
}

.detail-page .card-image {
  view-transition-name: card-1;
}

/* Customize the animation per state */
::view-transition-old(card-1),
::view-transition-new(card-1) {
  animation-duration: 0.4s;
  animation-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
```

```javascript
// JavaScript — just trigger
document.startViewTransition(() => updateDOM());
```

#### 4. Customize the Default Cross-Fade

```css
/* Slow cross-fade */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.5s;
  animation-timing-function: ease;
}

/* Slide-in for new content */
::view-transition-new(root) {
  animation: slide-in-from-right 0.4s ease forwards;
}

@keyframes slide-in-from-right {
  from { transform: translateX(100%); }
  to   { transform: translateX(0); }
}
```

#### 5. View Transition Types (Single Document)

```javascript
// In an SPA: animate state changes without route change
function toggleTheme() {
  const transition = document.startViewTransition(() => {
    document.body.classList.toggle('dark');
  });

  // Optional: wait for transition to complete
  transition.ready.then(() => {
    // Customize animations if needed
    document.documentElement.animate(
      [{ clipPath: 'circle(0% at 50% 50%)' }, { clipPath: 'circle(100% at 50% 50%)' }],
      { duration: 500, easing: 'ease-in-out', pseudoElement: '::view-transition-new(root)' }
    );
  });
}
```

#### 6. View Transition Lifecycle

```javascript
const transition = document.startViewTransition(callback);

// Phases: capturing → DOM updated → snapshot taken → animating
// Skip the default animation:
transition.skipTransition();

// Wait for ready (snapshot done, animation about to start)
await transition.ready;

// Wait for finished (animation complete)
await transition.finished;
```

### Browser Support (2026)

| Browser | View Transitions | Notes |
|---------|-----------------|-------|
| Chrome / Edge | ✅ (since v111) | Full support |
| Safari | ✅ (since 18) | Full support |
| Firefox | ⚠️ (in progress) | Behind flag, partial support |
| Mobile Safari | ✅ | Full support |
| Mobile Chrome | ✅ | Full support |

For unsupported browsers, the transition simply happens instantly — graceful degradation.

### When to Use View Transitions

| Use case | View Transitions wins? |
|----------|------------------------|
| Theme toggle with smooth animation | ✅ (one API call) |
| Multi-page app page change | ✅ (no library needed) |
| SPA route change | ✅ (no router coupling) |
| Shared element (list → detail) | ✅ (CSS view-transition-name) |
| Complex sequenced animations | ❌ (use Framer Motion / GSAP) |
| Browser not yet supported | ❌ (graceful degradation, but no animation) |

## CSS Scroll-Driven Animations

### How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│              CSS SCROLL-DRIVEN ANIMATIONS                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  animation-timeline: scroll()  → axis-driven (scroll position)    │
│  animation-timeline: view()    → element visibility                │
│                                                                     │
│  scroll(root)  → whole document scroll                            │
│  scroll(nearest) → nearest scroll container                       │
│  scroll(self)   → element's own scroll (overflow: scroll)         │
│                                                                     │
│  view()        → when element enters / exits the viewport         │
│  view(block)   → block-axis visibility (default)                  │
│  view(inline)  → inline-axis                                      │
│  view(x) / view(y)  → single-axis                                 │
│                                                                     │
│  Combined with animation-range: which 0-100% of the timeline      │
│  fires which 0-100% of the @keyframes.                            │
└─────────────────────────────────────────────────────────────────────┘
```

### Code Examples

#### 1. Reading Progress Bar (Scroll-Driven)

```css
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 4px;
  background: #ff6b6b;
  transform-origin: 0 50%;
  animation: reading-progress linear;
  animation-timeline: scroll(root);  /* tie to document scroll */
}

@keyframes reading-progress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}
```

No JavaScript. No scroll listeners. The animation is tied to the page's scroll position.

#### 2. Reveal on Scroll (View-Driven)

```css
.reveal {
  opacity: 0;
  transform: translateY(50px);
  animation: reveal linear forwards;
  animation-timeline: view();
  animation-range: entry 0% entry 100%;  /* from fully off-screen to fully in */
}

@keyframes reveal {
  to { opacity: 1; transform: translateY(0); }
}
```

The `view()` timeline progresses as the element enters the viewport. `entry 0%` is when the element starts entering; `entry 100%` is when it's fully visible.

#### 3. Parallax Effect

```css
.parallax-bg {
  animation: parallax linear;
  animation-timeline: scroll(root);
  animation-range: cover 0% cover 100%;
}

@keyframes parallax {
  from { transform: translateY(0); }
  to   { transform: translateY(-30%); }
}
```

#### 4. Sticky Section Indicator

```css
.section-progress {
  --dot-count: 5;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-progress::before {
  content: '';
  width: 4px;
  height: 100%;
  background: #ddd;
  position: absolute;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ddd;
}

.dot.active {
  background: #ff6b6b;
  animation: active-dot linear;
  animation-timeline: view();
  animation-range: contain 0% contain 100%;
}

@keyframes active-dot {
  from { transform: scale(0.8); }
  to   { transform: scale(1.2); }
}
```

#### 5. Combined Scroll + View Timelines

```css
/* Pin a section that animates as you scroll within it */
.pinned-section {
  animation: pin-content linear;
  animation-timeline: scroll(nearest);
  animation-range: contain 0% contain 100%;
  position: sticky;
  top: 0;
  height: 100vh;
}

@keyframes pin-content {
  from { transform: translateY(0); }
  to   { transform: translateY(-200px); }
}
```

### Browser Support (2026)

| Browser | scroll() | view() |
|---------|----------|--------|
| Chrome / Edge | ✅ (v115+) | ✅ |
| Safari | ✅ (since 17.4) | ✅ |
| Firefox | ⚠️ (in progress) | ⚠️ |
| Mobile | ✅ | ✅ |

Fallback: feature-detect with `@supports`:

```css
@supports (animation-timeline: scroll()) {
  .reading-progress {
    animation-timeline: scroll(root);
  }
}
@supports not (animation-timeline: scroll()) {
  .reading-progress {
    /* JS fallback: use scroll listener + rAF */
  }
}
```

### When to Use Scroll-Driven Animations

| Use case | Scroll-driven wins? |
|----------|---------------------|
| Reading progress bar | ✅ (perfect — no JS) |
| Reveal on scroll | ✅ (declarative) |
| Parallax | ✅ (single CSS rule) |
| Complex timeline with branches | ❌ (use GSAP ScrollTrigger) |
| Browser not yet supported | ⚠️ (use @supports fallback) |

## View Transitions + Scroll-Driven: The Pair

Both APIs complement each other. A common pattern:

```css
/* Smooth route change on scroll progress */
.page {
  animation: fade-in linear;
  animation-timeline: view();
  animation-range: entry 0% entry 50%;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
```

```javascript
// Trigger view transition on navigation
function navigate(url) {
  if (document.startViewTransition) {
    document.startViewTransition(async () => {
      // Update DOM
      const html = await (await fetch(url)).text();
      document.body.innerHTML = new DOMParser().parseFromString(html, 'text/html').body.innerHTML;
    });
  } else {
    location.href = url;
  }
}
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Animating `width` / `height` in scroll-driven | Stick to `transform` and `opacity` |
| Forgetting `view-transition-name` for shared elements | Both source and target need the same name |
| Using View Transitions in unsupported browsers without fallback | Test with feature detection; default is instant transition |
| Not using `animation-range` | Without it, animation triggers across the full scroll range — usually wrong |
| Heavy use of `::view-transition-*` pseudo-elements | They're rendered as snapshots; minimize their count for perf |

## Best Practices

1. **Use `view-transition-name` for shared elements** — define source and target with the same name
2. **Stick to `transform` and `opacity`** — same rule as everywhere
3. **Feature-detect for unsupported browsers** — use `@supports` for scroll-driven
4. **Use `animation-range` precisely** — `entry`, `cover`, `contain` give fine-grained control
5. **Avoid animating `width` / `height` in scroll-driven** — GPU compositing is critical
6. **Test with reduced motion** — `prefers-reduced-motion: reduce` should disable both
7. **Combine with `@media (prefers-reduced-motion)`** for accessibility

## Summary

- View Transitions API and CSS Scroll-Driven Animations are the 2026 frontier for web animation
- View Transitions: native cross-page / state-change transitions, no library
- Scroll-Driven Animations: CSS-only scroll effects, no `addEventListener('scroll', …)`
- Both are GPU-accelerated and respect `prefers-reduced-motion`
- Browser support is good in Chrome/Edge/Safari, partial in Firefox — always feature-detect
- Pair with Framer Motion / GSAP for complex sequences

---

## Cheat Sheet

```text
VIEW TRANSITIONS & SCROLL-DRIVEN CHEAT SHEET
═══════════════════════════════════════════════════════════════

VIEW TRANSITIONS:
  document.startViewTransition(() => updateDOM())
  transition.ready      → snapshot done
  transition.finished   → animation done
  transition.skipTransition()  → instant
  view-transition-name: card-1  → shared element

SCROLL-DRIVEN:
  animation-timeline: scroll()   → axis
  animation-timeline: view()     → visibility
  animation-timeline: scroll(root)  → document
  animation-timeline: scroll(nearest)  → nearest
  animation-range: entry 0% entry 100%

CUSTOMIZE:
  ::view-transition-old(root)  /  ::view-transition-new(root)

FALLBACK:
  @supports (animation-timeline: scroll()) { … }
  if (!document.startViewTransition) { /* fallback */ }

INTERVIEW ANSWER:
  1. View Transitions: native, no library, one API call
  2. Scroll-driven: CSS-only, no scroll listener
  3. Both GPU-accelerated, both feature-detectable
  4. Fallback to JS / library for unsupported browsers
```

---

## See Also

- [Accessibility](../25-Accessibility/)
- [CSS Animations](02-CSS-Animations.md)
- [Framer Motion](01-Framer-Motion.md)
- [GSAP](05-GSAP.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React Spring](06-React-Spring.md)
- [Web Animations API](04-Web-Animations-API.md)


## References & Learn More

- [Astro View Transitions](https://docs.astro.build/en/guides/view-transitions/)
- [CSS Scroll-Driven Animations (MDN)](https://developer.mozilla.org/en-US/docs/Web/CSS/animation-timeline)
- [Scroll-driven Animations (Chrome for Developers)](https://developer.chrome.com/docs/css-ui/scroll-driven-animations)
- [Scroll-Linked Animations (Bram.us)](https://www.bram.us/2023/05/23/scroll-driven-animations-with-css/)
- [View Transitions API (Chrome for Developers)](https://developer.chrome.com/docs/web-platform/view-transitions/)
- [View Transitions API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
- [View Transitions in Next.js (canary)](https://nextjs.org/docs/app/api-reference/functions/use-router)
