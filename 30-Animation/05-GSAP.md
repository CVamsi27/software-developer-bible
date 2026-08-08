---
section: Animation
category: Frontend
tags: [concept, reference]
---

# GSAP (GreenSock Animation Platform)

> GSAP is a professional-grade JavaScript animation library used on 50%+ of the top 10,000 websites. It supports timelines, scroll triggers, morphing, motion paths, and works across every major browser (including legacy IE11) — with a robust plugin ecosystem for advanced effects.

## Definition

GSAP is an imperative, chainable JavaScript animation library. You create tweens (`gsap.to()`, `gsap.from()`, `gsap.fromTo()`) and timelines (`gsap.timeline()`) that interpolate any property of any object. Plugins like ScrollTrigger add scroll-linked animations; SplitText adds text-reveal effects; MorphSVG and MotionPath add shape and path animations.

## Why It Matters (TL;DR)

- **Professional-grade** — used by Apple, Google, Nike, Slack, etc.
- **Performance** — 60fps, GPU-accelerated, smooth on any device
- **Cross-browser** — normalizes inconsistencies (including IE11)
- **ScrollTrigger plugin** — pin, scrub, batch, parallax for scroll-linked animations
- **Plugins** — MorphSVG, MotionPath, Flip (layout), SplitText, Draggable

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    GSAP ARCHITECTURE                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Tween Engine (gsap.to/from/fromTo)             │   │
│  │  • Tweens a single target over time                        │   │
│  │  • Easing presets (power1-4, expo, elastic, bounce, …)    │   │
│  │  • Set / get / kill / yoyo / repeat                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Timeline (gsap.timeline)                        │   │
│  │  • Sequences multiple tweens                                │   │
│  │  • Position parameters: '-=0.5', '+=0.2', '<', '>50%'    │   │
│  │  • Control: play, pause, reverse, seek, timeScale         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Plugins                                         │   │
│  │  • ScrollTrigger: scroll-linked animations                │   │
│  │  • Flip: layout animations (FLIP)                         │   │
│  │  • MorphSVG / MotionPath: shape & path animations         │   │
│  │  • SplitText: text reveal / per-character                  │   │
│  │  • Draggable: drag & drop                                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Tweens

```javascript
// Animate to a state
gsap.to('.box', { x: 300, rotation: 360, duration: 1, ease: 'power2.out' });

// Animate from a state (current → from)
gsap.from('.box', { opacity: 0, y: 50, duration: 1 });

// Animate from one state to another
gsap.fromTo('.box', { opacity: 0, scale: 0 }, { opacity: 1, scale: 1, duration: 0.8 });

// Set immediately (no animation)
gsap.set('.box', { x: 100 });

// Chain multiple properties
gsap.to('.box', { x: 300, y: 100, scale: 1.5, rotation: 180, backgroundColor: 'red', duration: 1 });
```

### 2. Timelines (Sequenced Animations)

```javascript
const tl = gsap.timeline({ defaults: { duration: 0.5, ease: 'power2.out' } });

tl.from('.title',    { y: -50, opacity: 0 })
  .from('.subtitle', { y: -30, opacity: 0 }, '-=0.2')     // start 0.2s before previous ends
  .from('.button',   { scale: 0 }, '-=0.1')
  .to('.button',     { scale: 1.1, repeat: 1, yoyo: true, duration: 0.3 }, '+=0.2');

// Position parameters:
// '-=0.5' → start 0.5s before previous ends
// '+=0.5' → start 0.5s after previous ends
// '<0.2'  → start 0.2s after previous starts
// '>0.5'  → start 0.5s after previous starts
// 'label' → start at the labeled point

// Control
tl.play();
tl.pause();
tl.reverse();
tl.seek(2);
tl.timeScale(2); // 2x speed
```

### 3. ScrollTrigger Plugin

```javascript
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

// Basic reveal
gsap.from('.reveal', {
  scrollTrigger: '.reveal',
  y: 100,
  opacity: 0,
  duration: 1,
});

// Scrub — animation tied to scroll position
gsap.to('.parallax', {
  y: () => -window.innerHeight * 0.5,
  ease: 'none',
  scrollTrigger: {
    trigger: '.parallax',
    start: 'top top',
    end: 'bottom top',
    scrub: true,           // tie to scroll, no smoothing
    // scrub: 0.5          // tie to scroll with 0.5s smoothing
  },
});

// Pin an element while animating
gsap.to('.pinned-section', {
  scale: 1.5,
  scrollTrigger: {
    trigger: '.pinned-section',
    start: 'top top',
    end: '+=500',           // pin for 500px of scroll
    pin: true,
    scrub: 1,
  },
});

// Batch — animate many elements as they enter
ScrollTrigger.batch('.card', {
  onEnter: (els) => gsap.to(els, { opacity: 1, y: 0, stagger: 0.1 }),
  start: 'top 80%',
});
```

### 4. Easing Functions

```javascript
// Built-in eases
gsap.to('.box', { x: 100, ease: 'power1.out' });
gsap.to('.box', { x: 100, ease: 'power2.out' });
gsap.to('.box', { x: 100, ease: 'power3.out' });
gsap.to('.box', { x: 100, ease: 'power4.out' });
gsap.to('.box', { x: 100, ease: 'back.out(1.7)' });
gsap.to('.box', { x: 100, ease: 'elastic.out(1, 0.3)' });
gsap.to('.box', { x: 100, ease: 'bounce.out' });

// Custom cubic-bezier
gsap.to('.box', { x: 100, ease: 'cubic-bezier(0.4, 0, 0.2, 1)' });
```

### 5. React Integration (via `@gsap/react`)

```tsx
import { useRef } from 'react';
import { useGSAP } from '@gsap/react';
import { gsap } from 'gsap';

function FadeIn() {
  const container = useRef(null);

  useGSAP(() => {
    gsap.from('.box', { opacity: 0, y: 30, duration: 0.6, stagger: 0.1 });
  }, { scope: container });

  return (
    <div ref={container}>
      <div className="box">1</div>
      <div className="box">2</div>
      <div className="box">3</div>
    </div>
  );
}
```

### 6. Timeline Markers and Labels

```javascript
const tl = gsap.timeline();

tl.addLabel('start')
  .from('.a', { x: -100, opacity: 0 })
  .addLabel('middle')
  .to('.a', { x: 0, opacity: 1 })
  .from('.b', { x: 100, opacity: 0 })
  .addLabel('end');

tl.play('start');          // play from the label
tl.seek('middle');         // jump to the label
```

### 7. Real-World: Hero Animation Sequence

```javascript
import { gsap } from 'gsap';
import { SplitText } from 'gsap/SplitText';

gsap.registerPlugin(SplitText);

function playHero() {
  const tl = gsap.timeline();

  // Split the title into characters
  const title = new SplitText('.hero-title', { type: 'chars' });
  const subtitle = new SplitText('.hero-subtitle', { type: 'lines' });

  tl.from(title.chars, {
    opacity: 0,
    y: 50,
    rotateX: -90,
    stagger: 0.03,
    duration: 0.8,
    ease: 'power4.out',
  })
  .from(subtitle.lines, {
    opacity: 0,
    y: 20,
    stagger: 0.1,
    duration: 0.6,
    ease: 'power2.out',
  }, '-=0.4')
  .from('.hero-cta', { scale: 0, ease: 'back.out(1.7)' }, '-=0.3')
  .from('.hero-image', { x: 100, opacity: 0, duration: 1 }, '-=0.8');
}
```

## Real-World Use Cases

```text
COMMON GSAP USE CASES:
  • Hero animations (text reveal, image slide-in)
  • Scroll-triggered reveal sequences
  • Parallax effects
  • Page transitions (with Barba.js)
  • Interactive product showcases
  • SVG morphing (logos, icons)
  • Animated charts and data viz
  • Loading sequences
  • Pinned scroll narratives (long-form storytelling)
  • Marquees and infinite-scroll effects
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Animating non-GPU properties | GSAP can animate anything, but stick to `x`, `y`, `scale`, `rotation`, `opacity` for perf |
| Not registering plugins | `gsap.registerPlugin(ScrollTrigger)` once at app start |
| Forgetting to clean up | Use `ScrollTrigger.kill()` and `tl.kill()` on unmount (React's `useGSAP` handles this) |
| Heavy main-thread work during animation | Use `lazy: true` for ScrollTrigger, or move heavy work to a Web Worker |
| Animating during `prefers-reduced-motion` | Detect and skip the animation, or use `gsap.matchMedia()` |

## Best Practices

1. **Animate `x`, `y`, `scale`, `rotation`, `opacity`** — GPU-friendly
2. **Use timelines for sequences** — easier to maintain than chained `.then()` calls
3. **Register plugins once at app start** — avoid duplicate registrations
4. **Use `useGSAP` in React** — handles cleanup automatically
5. **Use `ScrollTrigger.batch()` for many elements** — efficient
6. **Use `lazy: true` on ScrollTrigger** — don't compute until needed
7. **Respect `prefers-reduced-motion`** — `gsap.matchMedia()` for media-query-based animations
8. **Profile with DevTools** — GSAP has a GSAP panel for inspection

## Performance Considerations

```text
GSAP Performance:
┌─────────────────────────────────────────────────────────────────┐
│  Why it's fast:                                                 │
│  • Optimized RAF loop (single timer)                            │
│  • GPU-friendly properties (x, y, scale, rotation)             │
│  • Plugin system — only load what you use                       │
│  • Cross-browser normalization baked in                        │
│                                                                 │
│  Bundle:                                                        │
│  • Core: ~25 KB gzipped                                        │
│  • ScrollTrigger: ~10 KB                                        │
│  • SplitText: ~7 KB                                            │
│  • Most other plugins: 3-10 KB                                 │
│                                                                 │
│  Cost optimization:                                              │
│  • gsap.set() for instant changes (no tween)                   │
│  • overwrite: 'auto' to cancel conflicting tweens              │
│  • lazy: true on ScrollTrigger for off-screen                  │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- GSAP is the professional-grade animation library — 60fps, cross-browser, plugin-rich
- Use `gsap.to/from/fromTo` for tweens; `gsap.timeline()` for sequences
- ScrollTrigger plugin enables pin, scrub, batch, parallax for scroll-linked animations
- `useGSAP` hook for React handles cleanup automatically
- Animate `x`, `y`, `scale`, `rotation`, `opacity` for GPU performance

---

## Cheat Sheet

```text
GSAP CHEAT SHEET
═══════════════════════════════════════════════════════════════

CORE API:
  gsap.to(target, vars)       // animate to state
  gsap.from(target, vars)     // animate from state
  gsap.fromTo(target, from, to)
  gsap.set(target, vars)      // instant (no animation)

TIMELINE:
  const tl = gsap.timeline()
  tl.from('.a', { x: -100 })
    .from('.b', { y: 100 }, '-=0.2')   // position param
  tl.play() / pause() / reverse() / seek(time) / timeScale(rate)

SCROLLTRIGGER:
  gsap.to(el, {
    x: 100,
    scrollTrigger: { trigger: el, start: 'top 80%', end: 'bottom 20%', scrub: true, pin: true }
  });

EASING:
  'power1.out' / 'power2.out' / 'power3.out' / 'power4.out'
  'back.out(1.7)' / 'elastic.out(1, 0.3)' / 'bounce.out'

PLUGINS:
  ScrollTrigger, Flip, SplitText, MorphSVG, MotionPath, Draggable

INTERVIEW ANSWER:
  1. Why GSAP (cross-browser, robust, plugin ecosystem)
  2. Tweens vs timelines — when each
  3. ScrollTrigger — pin / scrub / batch
  4. Animate transform-only properties for 60fps
```

---

## See Also

- [CSS Animations](02-CSS-Animations.md)
- [Framer Motion](01-Framer-Motion.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React Spring](06-React-Spring.md)
- [View Transitions & Scroll-Driven Animations](07-View-Transitions-and-Scroll-Driven-Animations.md)
- [Web Animations API](04-Web-Animations-API.md)


## References & Learn More

- [@gsap/react](https://gsap.com/resources/React/)
- [GSAP Cheat Sheet](https://gsap.com/cheatsheet/)
- [GSAP Documentation](https://gsap.com/docs/)
- [GSAP Forum](https://gsap.com/community/forum/)
- [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)
- [GSAP Showcase](https://gsap.com/showcase/)
