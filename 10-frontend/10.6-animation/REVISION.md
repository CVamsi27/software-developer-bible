<!-- section: Animation | category: Reference | tags: revision, retrieval-practice| general-importance: specialized| general-importance: specialized | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Animation-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Animation — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## CSS Animations

Source: [CSS Animations](10.6.01-css-animations.md)

**Q:** Why are transform and opacity preferred rather than guaranteed to be free?

**A:** They are often eligible for compositing without layout or paint, but layer size, rasterization and browser decisions still matter. Verify the actual animation.

## Framer Motion

Source: [Framer Motion](10.6.02-framer-motion.md)

**Q:** Why does an exit animation need AnimatePresence to retain a leaving element?

**A:** React normally removes an unmounted element immediately. Presence management keeps it available for its exit phase before completing removal.

## GSAP (GreenSock Animation Platform)

Source: [GSAP (GreenSock Animation Platform)](10.6.03-gsap.md)

**Q:** Why must GSAP work created by a React effect have scoped cleanup?

**A:** Remounts and dependency changes can leave duplicate timelines or triggers. Revert or dispose the effect's context so it restores styles and removes owned animation work.

## React Spring

Source: [React Spring](10.6.04-react-spring.md)

**Q:** How does a spring's target differ from a fixed-duration tween?

**A:** A spring evolves from its physical/configured state toward the target; tension, friction and mass shape settling behavior rather than one predetermined duration.

## Web Animations API (WAAPI)

Source: [Web Animations API (WAAPI)](10.6.05-web-animations-api.md)

**Q:** Why should code awaiting animation.finished handle cancellation?

**A:** Canceling can reject the promise with AbortError. A finished animation's retained styles and its lifecycle also need an explicit cleanup decision.

## View Transitions API & CSS Scroll-Driven Animations

Source: [View Transitions API & CSS Scroll-Driven Animations](10.6.06-view-transitions-and-scroll-driven-animations.md)

**Q:** Why can reusing one view-transition-name on every card break a transition?

**A:** Captured visible elements need unique names. Assign a shared transition identity only to the selected old/new pair and preserve a visible fallback when unsupported.

## Canvas & SVG Animation

Source: [Canvas & SVG Animation](10.6.07-canvas-svg-animation.md)

**Q:** Why should canvas resolution differ from CSS size on a high-DPI display?

**A:** The backing buffer needs enough device pixels for sharp output. Scale/reset the drawing transform deliberately and account for the memory and fill-rate cost.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
