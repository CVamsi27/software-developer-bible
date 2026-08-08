---
section: Animation
category: Frontend
tags: [concept, reference]
---

# CSS Animations

> CSS animations provide a way to create smooth, performant animations using only CSS — without JavaScript. They include transitions for simple state changes and `@keyframes` animations for complex sequences. Always hardware-accelerated when you stay on `transform` and `opacity`.

## Definition

CSS animations are declarative, browser-native animations. **Transitions** interpolate a property from a start to an end value when state changes (e.g., `:hover`). **`@keyframes`** define multi-step animations that can loop, delay, and play independently of any state change. Both run on the compositor thread for 60fps.

## Why It Matters (TL;DR)

- **Performance** — hardware-accelerated, runs on the GPU
- **No JavaScript** — pure CSS, smallest possible runtime cost
- **Declarative** — describe the end state, the browser handles the interpolation
- **Accessibility** — `prefers-reduced-motion` lets you disable for sensitive users
- **Maintainability** — animation logic separate from app logic

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    CSS ANIMATION TYPES                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Transitions                               │   │
│  │  • Smooth state changes                                      │   │
│  │  • Two states (from → to)                                   │   │
│  │  • Triggered by pseudo-classes, class changes, or JS        │   │
│  │  • Properties: transition-property, -duration, -timing, …   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Keyframe Animations                       │   │
│  │  • Complex multi-step sequences                              │   │
│  │  • Loop, delay, direction                                   │   │
│  │  • Triggered by class or auto-playing                       │   │
│  │  • Defined with @keyframes rule                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Transform Properties                        │   │
│  │  • translate (position)                                      │   │
│  │  • scale (size)                                              │   │
│  │  • rotate (rotation)                                         │   │
│  │  • skew (distortion)                                         │   │
│  │  • All GPU-accelerated                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. CSS Transitions

```css
.button {
  background-color: blue;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  /* transition: <property> <duration> <timing-function> <delay> */
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.button:hover {
  background-color: darkblue;
  transform: translateY(-2px);
}

.button:active {
  transform: translateY(0);
}
```

### 2. Timing Functions

```css
.ease          { transition-timing-function: ease; }
.ease-in       { transition-timing-function: ease-in; }
.ease-out      { transition-timing-function: ease-out; }
.ease-in-out   { transition-timing-function: ease-in-out; }
.linear        { transition-timing-function: linear; }
.bounce        { transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55); }

/* Material Design easing */
.material      { transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); }
```

### 3. `@keyframes` Animations

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

@keyframes pulse {
  0%, 100% { transform: scale(1);   opacity: 1; }
  50%      { transform: scale(1.1); opacity: 0.8; }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}

.skeleton {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

### 4. Animation Properties (Shorthand + Longhand)

```css
/* Shorthand: name duration timing-function delay iteration-count direction fill-mode play-state */
.animated {
  animation: slideIn 0.5s ease-out 0.2s 1 normal forwards;
}

/* Longhand */
.animated {
  animation-name: slideIn;
  animation-duration: 0.5s;
  animation-timing-function: ease-out;
  animation-delay: 0.2s;
  animation-iteration-count: 1;
  animation-direction: normal;        /* normal | reverse | alternate | alternate-reverse */
  animation-fill-mode: forwards;       /* none | forwards | backwards | both */
  animation-play-state: running;       /* running | paused */
}
```

### 5. Performance — `will-change` and GPU Acceleration

```css
/* Hint to the browser to promote the element to its own compositor layer */
.animated {
  will-change: transform, opacity;
}

/* Remove the hint after the animation completes */
.animated.done {
  will-change: auto;
}

/* Trigger hardware acceleration with a 3D transform */
.accelerated {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}
```

### 6. Accessibility — `prefers-reduced-motion`

```css
/* Disable animations for users who request reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Provide a non-animated fallback */
.no-motion {
  animation: none;
  transition: none;
}
```

### 7. CSS Variables in Animations

```css
:root {
  --duration: 0.3s;
  --easing: ease-out;
}

.animated {
  animation: fadeIn var(--duration) var(--easing);
  transition: transform var(--duration) var(--easing);
}

/* Per-instance override */
.card.featured {
  --duration: 0.6s;
}
```

### 8. Real-World Patterns

```css
/* Skeleton loader */
.skeleton {
  background: linear-gradient(90deg, #eee 0%, #f5f5f5 50%, #eee 100%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Hover lift effect */
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

/* Shimmering button */
.button {
  position: relative;
  overflow: hidden;
}

.button::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.button:hover::after {
  transform: translateX(100%);
}

/* Page transition (for SPAs that allow CSS-only routing) */
.page-enter   { animation: fadeIn 0.3s ease-out forwards; }
.page-exit    { animation: fadeOut 0.2s ease-in forwards; }
```

## GPU-Accelerated vs CPU-Heavy Properties

| GPU-Accelerated ✅ | CPU-Heavy ❌ |
|--------------------|--------------|
| `transform: translate/scale/rotate/skew` | `width`, `height` |
| `opacity` | `top`, `left`, `right`, `bottom` |
| `filter` (some) | `margin`, `padding` |
| `clip-path` | `border-width` |
| `background-position` (sometimes) | `box-shadow` with blur |
| | `font-size`, `line-height` |
| | `background-color` (acceptable but not free) |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Animating `width` / `height` | Use `transform: scale()` instead — GPU-accelerated |
| Animating `top` / `left` | Use `transform: translate()` instead |
| Adding `will-change` to everything | Use sparingly — it consumes GPU memory; remove after animation |
| Forgetting `prefers-reduced-motion` | Add the `@media` block to disable animations for sensitive users |
| No `forwards` fill mode | Element snaps back to the start state after animation ends |
| Using `transition: all` | List specific properties for predictability and perf |

## Best Practices

1. **Animate `transform` and `opacity` only** for best performance
2. **Use `prefers-reduced-motion`** to respect user preferences
3. **List specific properties in `transition`** — avoid `transition: all`
4. **Use `will-change` sparingly** — add before animation, remove after
5. **Use `forwards` fill mode** if the end state should persist
6. **Use `cubic-bezier()` for custom easing** — fine-grained control
7. **Avoid animating during heavy JS work** — animation competes for main thread

## Performance Considerations

```text
CSS Animation Performance:
┌─────────────────────────────────────────────────────────────────┐
│  GPU Accelerated (Good):                                         │
│  • transform: translate, scale, rotate                          │
│  • opacity                                                      │
│  • filter (some)                                                │
│                                                                 │
│  CPU Heavy (Avoid):                                             │
│  • width, height                                                │
│  • top, left, right, bottom                                     │
│  • margin, padding                                              │
│  • box-shadow with blur                                         │
│                                                                 │
│  will-change Usage:                                              │
│  • Add for complex animations                                   │
│  • Remove after animation completes                             │
│  • Don't overuse (memory consumption)                           │
│                                                                 │
│  Animation Timing:                                               │
│  • Use ease-out for entering                                    │
│  • Use ease-in for exiting                                      │
│  • Use ease-in-out for UI state changes                         │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- CSS animations and transitions are the most performant option — browser-native, GPU-accelerated
- Animate `transform` and `opacity` for 60fps; avoid `width`/`height`/`top`/`left`
- Use `@keyframes` for multi-step animations, `transition` for two-state changes
- Always respect `prefers-reduced-motion` for accessibility
- Use `will-change` sparingly; remove after the animation

---

## Cheat Sheet

```text
CSS ANIMATIONS CHEAT SHEET
═══════════════════════════════════════════════════════════════

WHEN TO USE:
  • Two-state changes           → transition
  • Multi-step sequences         → @keyframes
  • Hover / focus / active       → transition
  • Loading spinners / skeletons → @keyframes
  • Page enter / exit            → @keyframes

PERFORMANCE RULES:
  • Animate transform / opacity only
  • Use will-change sparingly
  • Avoid animating layout properties
  • Respect prefers-reduced-motion

SYNTAX:
  transition: <property> <duration> <timing> <delay>
  animation: <name> <duration> <timing> <delay> <iter> <dir> <fill> <state>

TIMING FUNCTIONS:
  ease, ease-in, ease-out, ease-in-out, linear
  cubic-bezier(0.4, 0, 0.2, 1)   /* Material */
  cubic-bezier(0.68, -0.55, 0.265, 1.55)  /* back */

INTERVIEW ANSWER:
  1. CSS animations are GPU-accelerated for transform/opacity
  2. transitions = 2 states; @keyframes = multi-step
  3. will-change is a hint, not a free pass
  4. Always handle prefers-reduced-motion
```

---

## See Also

- [Framer Motion](01-Framer-Motion.md)
- [GSAP](05-GSAP.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [React Spring](06-React-Spring.md)
- [View Transitions & Scroll-Driven Animations](07-View-Transitions-and-Scroll-Driven-Animations.md)
- [Web Animations API](04-Web-Animations-API.md)


## References & Learn More

- [CSS Triggers (what triggers layout/paint/composite)](https://csstriggers.com/)
- [MDN: CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [MDN: CSS Transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions)
- [MDN: will-change](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change)
- [prefers-reduced-motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
- [web.dev: Animations Guide](https://web.dev/animations/)
