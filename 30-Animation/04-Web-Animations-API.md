---
section: Animation
category: Frontend
tags: [concept, reference]
---

# Web Animations API (WAAPI)

> The Web Animations API (WAAPI) provides a native JavaScript interface for creating smooth, performant animations. It combines the power of CSS animations with the control of JavaScript, enabling timeline-based animations that run on the compositor thread for 60fps.

## Definition

WAAPI is a browser-native JavaScript API for creating and controlling CSS-style animations programmatically. The main entry point is `element.animate(keyframes, options)`, which returns an `Animation` object with `.play()`, `.pause()`, `.reverse()`, `.finish()`, `.cancel()`, and `.currentTime` setters. It runs on the compositor thread — same performance as CSS, more control than JavaScript-driven rAF.

## Why It Matters (TL;DR)

- **Native performance** — runs on the compositor thread, 60fps without libraries
- **Programmatic control** — start, pause, reverse, seek, set playback rate
- **No dependencies** — no Framer Motion / GSAP needed for simple cases
- **CSS integration** — can read/write CSS animation properties
- **Element inspection** — `element.getAnimations()` and `document.getAnimations()` for global control

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                  WEB ANIMATIONS API LIFECYCLE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐     │
│  │  Fetch   │ ──▶│  Parse   │ ──▶│ Execute  │ ──▶│ Response │     │
│  │  Event   │    │  Request │    │  Handler │    │          │     │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘     │
│                                                                     │
│  Isolate Model:                                                     │
│  • Each Worker runs in isolated V8 isolate                        │
│  • No shared memory between Workers                               │
│  • Cold start < 5ms (V8 isolates)                                 │
│  • CPU time limit: 10ms (free), 30s (paid)                        │
│  • Memory limit: 128MB                                             │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Animation

```javascript
const el = document.querySelector('.box');

const animation = el.animate(
  [
    { transform: 'translateX(0px)', opacity: 1 },
    { transform: 'translateX(300px)', opacity: 0.5 },
  ],
  {
    duration: 1000,
    easing: 'ease-in-out',
    iterations: Infinity,
    direction: 'alternate',
  }
);
```

### 2. Animation Control

```javascript
// Playback control
animation.pause();
animation.play();
animation.reverse();
animation.finish();
animation.cancel();

// Seek to a specific time (ms)
animation.currentTime = 500;

// Set playback rate (negative = reverse, 0 = pause)
animation.playbackRate = 2; // 2x speed

// Promise-based completion
await animation.finished;
console.log('Animation done');
```

### 3. Animation Options Reference

```javascript
el.animate(keyframes, {
  duration: 1000,           // ms
  delay: 200,               // ms before start
  endDelay: 0,              // ms after end (before finished resolves)
  easing: 'ease-in-out',    // or 'cubic-bezier(0.4, 0, 0.2, 1)'
  iterations: 1,            // or Infinity
  iterationStart: 0,       // start position (0-1)
  direction: 'normal',      // 'normal' | 'reverse' | 'alternate' | 'alternate-reverse'
  fill: 'none',             // 'none' | 'forwards' | 'backwards' | 'both' | 'auto'
  composite: 'replace',     // 'replace' | 'add' | 'accumulate'
  iterationComposite: 'replace',
});
```

### 4. Complex Keyframes

```javascript
const anim = el.animate(
  [
    { transform: 'scale(1)',   opacity: 1, offset: 0 },
    { transform: 'scale(1.2)', opacity: 0.8, offset: 0.5 },
    { transform: 'scale(1)',   opacity: 1, offset: 1 },
  ],
  { duration: 1500, iterations: 3, direction: 'alternate' }
);
```

### 5. Reading CSS Animations

```javascript
const el = document.querySelector('.fade-in');
const running = el.getAnimations();
console.log(running[0].currentTime, running[0].playState);

// Pause all animations on the page
document.getAnimations().forEach((a) => a.pause());
```

### 6. Replacing CSS Animations Programmatically

```javascript
// Apply a CSS class, then take over with WAAPI
el.classList.add('fade-in');
const animations = el.getAnimations();
const fade = animations[0];

// Wait for the animation to start, then customize
fade.ready.then(() => {
  fade.currentTime = 0;
  fade.pause();
  // Custom logic
});
```

### 7. Effect: Spring-like with WAAPI (Not Native, But Possible)

```javascript
function springify(el, keyframes, duration = 1000) {
  // Use a custom cubic-bezier approximation of a spring
  return el.animate(keyframes, {
    duration,
    easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)', // slight overshoot
  });
}
```

### 8. Combining Multiple Animations

```javascript
const moveX = el.animate(
  [{ transform: 'translateX(0)' }, { transform: 'translateX(300px)' }],
  { duration: 500, fill: 'forwards' }
);

const fade = el.animate(
  [{ opacity: 0 }, { opacity: 1 }],
  { duration: 500, fill: 'forwards' }
);

// Both run in parallel on the same element
await Promise.all([moveX.finished, fade.finished]);
```

### 9. React Hook for WAAPI

```typescript
import { useEffect, useRef } from 'react';

function useAnimate(deps: unknown[] = []) {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    if (!ref.current) return;
    const anim = ref.current.animate(
      [{ opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: 300, easing: 'ease-out' }
    );
    return () => anim.cancel();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  return ref;
}

// Usage
function MyComponent() {
  const ref = useAnimate([/* trigger */]);
  return <div ref={ref}>Hello</div>;
}
```

## Real-World Use Cases

### 1. Skeleton → Content Reveal

```javascript
function revealContent(skeleton, content) {
  const fade = skeleton.animate(
    [{ opacity: 1 }, { opacity: 0 }],
    { duration: 200, fill: 'forwards' }
  );

  fade.finished.then(() => {
    skeleton.style.display = 'none';
    content.style.display = 'block';
    content.animate(
      [{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'translateY(0)' }],
      { duration: 300, easing: 'ease-out', fill: 'forwards' }
    );
  });
}
```

### 2. Drag and Drop with WAAPI

```javascript
element.addEventListener('pointerdown', (e) => {
  const anim = element.animate(
    [{ transform: 'scale(1)' }, { transform: 'scale(1.05)' }],
    { duration: 200, fill: 'forwards' }
  );
  // Start drag, then cancel the scale animation on pointerup
  // ...
  element.addEventListener('pointerup', () => anim.cancel(), { once: true });
});
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Animating layout properties via WAAPI | Use `transform` and `opacity` only |
| Not awaiting `animation.finished` | Use `.finished` Promise for sequential animations |
| Forgetting `fill: 'forwards'` | Element snaps back to the start state without it |
| Not cancelling animations on unmount | `return () => animation.cancel()` in `useEffect` |
| Re-creating animations on every render | Cache the animation in a `useRef` or hoist to module scope |

## Best Practices

1. **Animate `transform` / `opacity` only** — same rules as CSS animations
2. **Use `.finished` for sequenced animations** — chain via Promises
3. **Cancel on unmount** — prevent leaked animations in SPAs
4. **Use `fill: 'forwards'`** to persist the end state
5. **Compose multiple animations** on the same element for parallel effects
6. **Read animations with `getAnimations()`** for global control
7. **Test reduced-motion** — manually check `matchMedia('(prefers-reduced-motion: reduce)')`

## Performance Considerations

```text
WAAPI vs CSS vs rAF:
┌─────────────────────────────────────────────────────────────────┐
│  CSS animations:        Native, fastest, no JS                  │
│  WAAPI:                 Native, controllable, compositor        │
│  requestAnimationFrame: JS-driven, main thread                  │
│  setInterval / setTimeout: Avoid — drifts, doesn't pause       │
│                                                                 │
│  WAAPI best for:                                                 │
│  • Need to seek/pause/reverse                                  │
│  • Sequential animations                                       │
│  • Coordinated multi-element animation                         │
│  • Replacing CSS animations programmatically                  │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- WAAPI is the native browser API for programmatic animation — same performance as CSS
- Use `element.animate(keyframes, options)` to start; control via `.play()`, `.pause()`, `.reverse()`, `.currentTime`
- Animate `transform` and `opacity` only; respect `prefers-reduced-motion`
- Use `.finished` Promise for sequenced animations; cancel on unmount
- Reach for it when you need control beyond what CSS provides, without pulling in a library

---

## Cheat Sheet

```text
WAAPI CHEAT SHEET
═══════════════════════════════════════════════════════════════

BASIC:
  const anim = el.animate(keyframes, options);
  anim.play() / pause() / reverse() / cancel() / finish()
  anim.currentTime = ms
  anim.playbackRate = 2

OPTIONS:
  duration, delay, endDelay, easing, iterations, iterationStart,
  direction, fill, composite, iterationComposite

KEYFRAMES:
  [{ offset: 0, transform: '...', opacity: 1 }, { offset: 1, ... }]

READING:
  el.getAnimations()              → all animations on element
  document.getAnimations()        → all animations on page

INTERVIEW ANSWER:
  1. Native browser API, compositor-thread, no library
  2. Same keyframe syntax as CSS, but controllable
  3. Use for sequential / seekable / controllable animations
  4. Cancel on unmount, respect prefers-reduced-motion
```

---

## See Also

- [CSS Animations](02-CSS-Animations.md)
- [Framer Motion](01-Framer-Motion.md)
- [GSAP](05-GSAP.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React Spring](06-React-Spring.md)
- [View Transitions & Scroll-Driven Animations](07-View-Transitions-and-Scroll-Driven-Animations.md)


## References & Learn More

- [CSS Animations vs WAAPI](https://css-tricks.com/css-animations-vs-web-animations-api/)
- [MDN: Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [WAAPI Concepts](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Web_Animations_API_Concepts)
- [web.dev: Animations](https://web.dev/animations/)
