# CSS Animations

## Definition
CSS animations provide a way to create smooth, performant animations using only CSS, without JavaScript. They include transitions for simple state changes and keyframe animations for complex sequences.

## Why Do We Need It?
- **Performance**: Hardware-accelerated, runs on GPU
- **Simplicity**: No JavaScript required for basic animations
- **Declarative**: Define animations in CSS
- **Maintainability**: Separate animation concerns from logic
- **Accessibility**: Can be disabled with `prefers-reduced-motion`

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
│  │  • Triggered by pseudo-classes or class changes             │   │
│  │  • Properties: transition-property, transition-duration     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Keyframe Animations                       │   │
│  │  • Complex animation sequences                              │   │
│  │  • Multiple states                                          │   │
│  │  • Can loop, delay, and have complex timing                 │   │
│  │  • Defined with @keyframes rule                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Transform Properties                        │   │
│  │  • translate (position)                                      │   │
│  │  • scale (size)                                              │   │
│  │  • rotate (rotation)                                         │   │
│  │  • skew (distortion)                                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. CSS Transitions

```css
/* Basic transition */
.button {
  background-color: blue;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.button:hover {
  background-color: darkblue;
  transform: translateY(-2px);
}

.button:active {
  transform: translateY(0);
}

/* Multiple properties */
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition:
    box-shadow 0.3s ease,
    transform 0.3s ease,
    border-color 0.3s ease;
}

.card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-4px);
  border-color: #007bff;
}

/* Transition timing functions */
.ease {
  transition-timing-function: ease;
}

.ease-in {
  transition-timing-function: ease-in;
}

.ease-out {
  transition-timing-function: ease-out;
}

.ease-in-out {
  transition-timing-function: ease-in-out;
}

.cubic-bezier {
  transition-timing-function: cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### 2. CSS Keyframe Animations

```css
/* Basic keyframe animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

/* Multiple steps */
@keyframes slideIn {
  0% {
    transform: translateX(-100%);
    opacity: 0;
  }
  50% {
    transform: translateX(10%);
    opacity: 1;
  }
  100% {
    transform: translateX(0);
  }
}

.slide-in {
  animation: slideIn 0.8s ease-out forwards;
}

/* Infinite animation */
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.spinner {
  animation: spin 1s linear infinite;
}

/* Complex animation */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

.pulse {
  animation: pulse 2s ease-in-out infinite;
}

/* Bounce animation */
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    animation-timing-function: cubic-bezier(0.215, 0.61, 0.355, 1);
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06);
    transform: translate3d(0, -30px, 0);
  }
  70% {
    animation-timing-function: cubic-bezier(0.755, 0.05, 0.855, 0.06);
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
}

.bounce {
  animation: bounce 1s ease-in-out;
}
```

### 3. Transform Properties

```css
/* Translate */
.translate {
  transform: translateX(50px);
  transition: transform 0.3s ease;
}

.translate:hover {
  transform: translateX(100px);
}

/* Scale */
.scale {
  transform: scale(1);
  transition: transform 0.3s ease;
}

.scale:hover {
  transform: scale(1.2);
}

/* Rotate */
.rotate {
  transform: rotate(0deg);
  transition: transform 0.3s ease;
}

.rotate:hover {
  transform: rotate(45deg);
}

/* Skew */
.skew {
  transform: skew(0deg);
  transition: transform 0.3s ease;
}

.skew:hover {
  transform: skew(10deg);
}

/* Combined transforms */
.combined {
  transform: translate(0, 0) scale(1) rotate(0deg);
  transition: transform 0.3s ease;
}

.combined:hover {
  transform: translate(20px, -20px) scale(1.1) rotate(5deg);
}

/* Transform origin */
.origin-center {
  transform-origin: center;
}

.origin-top-left {
  transform-origin: top left;
}

.origin-custom {
  transform-origin: 30% 70%;
}
```

### 4. Animation Properties

```css
/* Animation shorthand */
.animated {
  animation: slideIn 0.5s ease-out 0.2s forwards;
}

/* Individual properties */
.animated {
  animation-name: slideIn;
  animation-duration: 0.5s;
  animation-timing-function: ease-out;
  animation-delay: 0.2s;
  animation-iteration-count: 1;
  animation-direction: normal;
  animation-fill-mode: forwards;
  animation-play-state: running;
}

/* Animation direction */
.alternate {
  animation-direction: alternate;
}

.reverse {
  animation-direction: reverse;
}

.alternate-reverse {
  animation-direction: alternate-reverse;
}

/* Animation fill mode */
.forwards {
  animation-fill-mode: forwards;
}

.backwards {
  animation-fill-mode: backwards;
}

.both {
  animation-fill-mode: both;
}

/* Animation play state */
.paused {
  animation-play-state: paused;
}

.running {
  animation-play-state: running;
}
```

### 5. Performance Optimization

```css
/* GPU acceleration */
.gpu-accelerated {
  transform: translateZ(0);
  will-change: transform;
}

/* Will-change (use sparingly) */
.will-change-transform {
  will-change: transform;
}

.will-change-opacity {
  will-change: opacity;
}

/* Hardware acceleration */
.hardware-accelerated {
  backface-visibility: hidden;
  perspective: 1000px;
}

/* Avoid animating these properties */
/* width, height, top, left, right, bottom, margin, padding */

/* Use transform instead */
.transform-position {
  transform: translateX(100px); /* Good */
}

.bad-position {
  left: 100px; /* Bad for performance */
}
```

### 6. Responsive Animations

```css
/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Mobile animations */
@media (max-width: 768px) {
  .mobile-animation {
    animation-duration: 0.3s;
  }
}

/* Desktop animations */
@media (min-width: 769px) {
  .desktop-animation {
    animation-duration: 0.5s;
  }
}
```

### 7. CSS Variables in Animations

```css
:root {
  --animation-duration: 0.3s;
  --animation-timing: ease-out;
  --primary-color: #007bff;
}

.animated {
  animation: fadeIn var(--animation-duration) var(--animation-timing);
  background-color: var(--primary-color);
}

/* Dynamic animations */
.dynamic {
  --scale: 1;
  transform: scale(var(--scale));
  transition: transform 0.3s ease;
}

.dynamic:hover {
  --scale: 1.2;
}
```

## Real-World Use Cases

### Button Hover Effects
```css
.button {
  background: linear-gradient(45deg, #007bff, #0056b3);
  border: none;
  padding: 12px 24px;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: left 0.5s ease;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4);
}

.button:hover::before {
  left: 100%;
}
```

### Loading Skeleton
```css
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}
```

### Page Transition
```css
.page {
  opacity: 0;
  transform: translateY(20px);
  animation: pageIn 0.5s ease-out forwards;
}

@keyframes pageIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.page-exit {
  animation: pageOut 0.3s ease-in forwards;
}

@keyframes pageOut {
  to {
    opacity: 0;
    transform: translateY(-20px);
  }
}
```

## Common Mistakes

1. **Animating non-transform properties**: width, height, margin cause reflows
2. **Missing will-change**: Can cause performance issues
3. **Overusing will-change**: Can consume GPU memory
4. **Ignoring reduced motion**: Accessibility concern
5. **Not using transform**: Missing hardware acceleration

## Best Practices

1. **Use transform properties**: translate, scale, rotate, opacity
2. **Add will-change**: For complex animations
3. **Respect reduced motion**: Check prefers-reduced-motion
4. **Keep animations subtle**: Enhance, don't distract
5. **Use CSS variables**: For dynamic values

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
│  • box-shadow                                                   │
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

## Interview Questions

### Beginner (5)
1. **What is the difference between transitions and keyframe animations?**
   - Answer: Transitions animate between two states; keyframe animations can have multiple states and more control.

2. **What is the transform property?**
   - Answer: A CSS property for 2D/3D transformations (translate, scale, rotate, skew).

3. **What is hardware acceleration?**
   - Answer: Using GPU for animations, achieved with transform and opacity properties.

4. **What is will-change?**
   - Answer: A CSS property that hints to the browser about upcoming animations for optimization.

5. **What is prefers-reduced-motion?**
   - Answer: A media query that detects if user prefers reduced motion for accessibility.

### Intermediate (5)
6. **How do you create a CSS transition?**
   - Answer: Use `transition` property: `transition: transform 0.3s ease;`

7. **What is the animation-fill-mode?**
   - Answer: Defines how styles apply before and after animation (forwards, backwards, both).

8. **How do you pause a CSS animation?**
   - Answer: Use `animation-play-state: paused;`

9. **What is the transform-origin property?**
   - Answer: Defines the point around which transformations occur.

10. **How do you create infinite animations?**
    - Answer: Use `animation-iteration-count: infinite;`

### Senior (10)
11. **How do you optimize CSS animations for performance?**
    - Answer: Use transform/opacity, add will-change, avoid animating layout properties, respect reduced motion.

12. **What causes animation jank?**
    - Answer: Animating layout properties, excessive DOM manipulation, heavy JavaScript, main thread blocking.

13. **How do you create complex animation sequences?**
    - Answer: Use animation-delay, multiple keyframes, or JavaScript animation libraries.

14. **How do you handle animations in responsive design?**
    - Answer: Use media queries, CSS variables, and respect prefers-reduced-motion.

15. **What is the difference between animation and transition?**
    - Answer: Animation has more control (keyframes, iteration, direction), transition is simpler for state changes.

16. **How do you create 3D transforms?**
    - Answer: Use transform-style: preserve-3d and perspective property.

17. **How do you handle animations with React?**
    - Answer: Use CSS classes, styled-components, or animation libraries like Framer Motion.

18. **What is the performance impact of box-shadow animations?**
    - Answer: Box-shadow is not GPU-accelerated, can cause repaints. Use filter: drop-shadow() instead.

19. **How do you test CSS animations?**
    - Answer: Visual regression testing, manual testing, automation with tools like Playwright.

20. **How do you handle animations in SSR?**
    - Answer: CSS animations work in SSR, but JavaScript animations need client-side hydration.

### FAANG-style (5)
21. **Design an animation system for a design system**
- **Answer**:
  - Animation tokens (duration, easing)
  - Transition utilities
  - Keyframe library
  - Performance budgets
  - Accessibility compliance

22. **How would you optimize animations for low-end devices?**
- **Answer**:
  - Simplify animations
  - Reduce DOM changes
  - Use will-change sparingly
  - Provide fallbacks

23. **Explain animation performance monitoring**
- **Answer**:
  - Frame rate measurement
  - Layout thrashing detection
  - GPU usage monitoring
  - User experience metrics

24. **How do you handle animations in micro-frontends?**
- **Answer**:
  - Consistent animation tokens
  - Performance budgets
  - Shared animation library

25. **Design a page transition system**
- **Answer**:
  - Route-based transitions
  - Loading states
  - Error states
  - Accessibility

### Follow-ups (5)
26. **How do you handle animations in React Server Components?**
- **Answer**: CSS animations work in RSC, but JavaScript animations need client components.

27. **How do you handle animations with third-party libraries?**
- **Answer**: Use CSS-in-JS libraries that support animations, or use animation libraries.

28. **How do you handle animation performance at scale?**
- **Answer**: Automated testing, performance budgets, monitoring, and optimization.

29. **How do you handle animations in different browsers?**
- **Answer**: Use vendor prefixes, feature detection, and fallbacks.

30. **How do you handle animations with content changes?**
- **Answer**: Use layout animations, FLIP technique, or animation libraries.

## Summary

CSS animations provide a performant, declarative way to create smooth animations. Master transitions, keyframes, transforms, and performance optimization for excellent user experiences.

## References & Learn More

- [MDN CSS Animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Animations)
- [MDN CSS Transitions](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Transitions)
- [CSS Triggers](https://csstriggers.com/)
- [Will-change MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/will-change)
- [Reduced Motion](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)
