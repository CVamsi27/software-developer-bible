<!-- section: Animation | category: Reference | tags: revision, retrieval-practice | role-priority: optional | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-Animation-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Optional-lightgrey)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# Animation — Revision

Read the section's learning chapters first. Close them, explain each answer with a concrete failure or tradeoff, then use the source link to check what you missed.

## CSS Animations

Source: [CSS Animations](10.6.01-css-animations.md)

**Q:** Why are transform and opacity preferred rather than guaranteed to be free?

**A:** They are often eligible for compositing without layout or paint, but layer size, rasterization and browser decisions still matter. Verify the actual animation.

**Q:** Why is replacing an animated width with scale sometimes incorrect?

**A:** Width changes layout geometry and can move neighboring content. Scale changes the visual result without changing normal-flow sizing. Choose the required behavior before optimizing its rendering work.

## Motion for React

Source: [Motion for React](10.6.02-framer-motion.md)

**Q:** Why does an exit animation need AnimatePresence to retain a leaving element?

**A:** React normally removes an unmounted element immediately. Presence management keeps it available for its exit phase before completing removal.

**Q:** What does Motion for React’s reduced-motion hook report, and which effects does MotionConfig change?

**A:** The hook reports and tracks the device preference. MotionConfig can disable transform and layout animation while leaving effects such as opacity in place; CSS, video, and Canvas motion need their own policy.

## GSAP (GreenSock Animation Platform)

Source: [GSAP (GreenSock Animation Platform)](10.6.03-gsap.md)

**Q:** Why must GSAP work created by a React effect have scoped cleanup?

**A:** Remounts and dependency changes can leave duplicate timelines or triggers. Revert or dispose the effect's context so it restores styles and removes owned animation work.

**Q:** Does `lazy: true` defer a ScrollTrigger animation until it enters the viewport?

**A:** No. Tween lazy rendering batches initial writes within a ticker update. ScrollTrigger controls playback through its trigger/start configuration; it has no equivalent `lazy` offscreen-loading setting.

**Q:** Why does an animation started by a later click need `contextSafe`?

**A:** The callback runs after the original `useGSAP` setup, so its new animation is not automatically recorded by that setup's context. `contextSafe` records it for scoped cleanup; manually installed event listeners still need removal.

## React Spring

Source: [React Spring](10.6.04-react-spring.md)

**Q:** How does a spring's target differ from a fixed-duration tween?

**A:** A spring evolves from its physical/configured state toward the target; tension, friction and mass shape settling behavior rather than one predetermined duration.

**Q:** Why should React Spring's reduced-motion utility usually live near the app root?

**A:** The utility sets the library's global `skipAnimation` flag. Calling it in an isolated leaf can change animation behavior for other Spring components; read the preference once at the shared owner and pass a local value only when one effect needs a tailored alternative.

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

## Trace changed timing and cancellation

Source: [CSS animation](10.6.01-css-animations.md), [GSAP](10.6.03-gsap.md), [WAAPI](10.6.05-web-animations-api.md), [View/scroll transitions](10.6.06-view-transitions-and-scroll-driven-animations.md), [Canvas](10.6.07-canvas-svg-animation.md)

**Q:** At half the duration, why need a transition not be halfway in distance?
**A:** A timing function maps elapsed progress into effect progress. A nonlinear ease changes that mapping.

**Q:** Why does GSAP subtitle start at 0.3 seconds after a 0.5-second title with position −=0.2?
**A:** The position subtracts 0.2 seconds from the timeline's current end. It overlaps the title's last 0.2 seconds rather than delaying it.

**Q:** Why can canceling a fade prevent a reveal but still require promise handling?
**A:** Cancellation rejects a pending finished promise. The owner must catch that outcome and stop obsolete callbacks from changing the current interface.

**Q:** Why keep forwards fill until committing a completed WAAPI effect?
**A:** It retains the final effect for compatible browsers while commitStyles writes it to inline styles; cancel then releases the retained animation.

**Q:** Why does starting a view transition after a route effect lose the previous snapshot?
**A:** The route DOM already changed. The transition must wrap the actual update or use a router integration that does so.

**Q:** Why does the Canvas example clamp a long frame interval?
**A:** It deliberately discards excess simulation time to avoid teleporting after a pause. Real-time simulation would need a different catch-up policy.

## Summary

A useful answer names the guarantee, the mechanism that enforces it, and the failure boundary. Revisit the source when any of those is unclear.

## See Also

- [Section learning flow](INDEX.md) — return to the study sequence

## References

The source-linked chapters contain the supporting documentation and worked examples.

[Back to section index](INDEX.md)
