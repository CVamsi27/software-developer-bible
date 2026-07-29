# GSAP (GreenSock Animation Platform)

[![Category: Frontend](https://img.shields.io/badge/category-Frontend-00b4d8)](.)

## Definition

**GSAP** is a professional-grade JavaScript animation library for creating high-performance, complex animations. It supports timelines, easing functions, scroll triggers, morphing, and works across all major browsers including legacy IE. GSAP is used by 50%+ of the top 10,000 websites for animation.

## Why Do We Need It?

1. **Performance**: Optimized for 60fps, works with transforms/opacity (GPU-accelerated)
2. **Timeline control**: Sequence, overlap, and stagger complex animations easily
3. **ScrollTrigger**: Animate elements based on scroll position (parallax, pinning)
4. **Cross-browser**: Normalizes inconsistencies across all major browsers
5. **Plugins**: MorphSVG, MotionPath, Flip (layout animations), Draggable

## Code Examples

```javascript
// Basic tween
gsap.to('.box', {
  x: 300,
  rotation: 360,
  duration: 1,
  ease: 'power2.out',
});

// Timeline
const tl = gsap.timeline({ defaults: { duration: 0.5 } });
tl.from('.title', { y: -50, opacity: 0 })
  .from('.subtitle', { y: -30, opacity: 0 }, '-=0.2')
  .from('.button', { scale: 0 }, '-=0.1');

// ScrollTrigger
gsap.from('.reveal', {
  scrollTrigger: '.reveal',
  y: 100,
  opacity: 0,
  duration: 1,
});
```

## Summary

- GSAP (GreenSock Animation Platform) is a professional-grade JavaScript animation library
- Tween-based API (gsap.to, gsap.from, gsap.fromTo) provides precise animation control with easing presets
- TimelineMax/gsap.timeline enables sequencing and synchronization of complex multi-element animations
- ScrollTrigger plugin ties animations to scroll position for parallax, reveal, and progress-based effects
- Performance is optimized with GPU-accelerated transforms and minimal garbage collection overhead

---

## Cheat Sheet
```text
GSAP (GREENSOCK ANIMATION PLATFORM) CHEAT SHEET
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

- [GSAP Documentation](https://gsap.com/docs/)
- [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/)
