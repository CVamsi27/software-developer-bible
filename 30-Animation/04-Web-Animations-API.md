# Web Animations API

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

terface for creating smooth, performant animations in the browser. It combines CSS animation power with JavaScript control, enabling timeline-based animations that run on the compositor thread for 60fps performance.

## Why Do We Need It?

1. **Performance**: Runs on compositor thread — doesn't block main thread
2. **Control**: Start, pause, reverse, seek to any point programmatically
3. **No dependencies**: Built into modern browsers — no library needed
4. **CSS integration**: Can read/write CSS animation properties

## Code Examples

```javascript
const element = document.querySelector('.box');

// Basic animation
const animation = element.animate([
  { transform: 'translateX(0px)', opacity: 1 },
  { transform: 'translateX(300px)', opacity: 0.5 },
], {
  duration: 1000,
  easing: 'ease-in-out',
  iterations: Infinity,
  direction: 'alternate',
});

// Control
animation.pause();
animation.play();
animation.reverse();
animation.finish();
animation.cancel();

// Seek to 50%
animation.currentTime = 500;

// Promise-based completion
await animation.finished;
```

## Summary

- Web Animations API (WAAPI) provides native browser animations with JavaScript control and CSS performance
- Keyframe animations support compositing, easing, iteration, and direction properties like CSS
- Animation timeline control enables play, pause, reverse, seek, and playback rate manipulation
- Performance benefits from running on the compositor thread rather than the main thread
- Element.getAnimations() and document.getAnimations() provide global animation inspection and control

---

## Cheat Sheet
```text
WEB ANIMATIONS API CHEAT SHEET
============================================================

INTERVIEW TIPS:
  - Understand the core concepts and trade-offs
  - Be ready to explain with real-world examples
  - Discuss performance implications and best practices
  - Show awareness of common pitfalls

```
## See Also
- [CSS Animations](02-CSS-Animations.md)
- [Performance Monitoring](../26-Performance-Monitoring/)

## References & Learn More

- [MDN: Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API)
- [WAAPI Concepts](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Web_Animations_API_Concepts)
