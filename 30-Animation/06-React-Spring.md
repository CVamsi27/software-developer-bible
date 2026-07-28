---
section: Animation
category: Frontend
tags: [concept]
---

# React Spring

## Definition

**React Spring** is a spring-physics-based animation library for React. Unlike CSS transitions or GSAP timelines, it uses natural spring physics (mass, tension, friction) to create fluid, natural-feeling motion. It supports animated components, interpolations, gesture-based animations, and shared-element transitions.

## Why Do We Need It?

1. **Physics-based**: Natural motion with configurable mass/tension/friction
2. **React-native**: Works with both web and React Native
3. **Hooks API**: `useSpring`, `useSprings`, `useTrail`, `useTransition`, `useChain`
4. **Performance**: Runs on the React renderer — no direct DOM manipulation
5. **Gestures**: Integrates with `@react-spring/gesture` for drag/swipe animations

## Code Examples

```tsx
import { useSpring, animated, useTrail } from '@react-spring/web';

// Basic spring
function FadeIn() {
  const props = useSpring({ opacity: 1, from: { opacity: 0 } });
  return <animated.div style={props}>Hello</animated.div>;
}

// Spring with config
function Bounce() {
  const props = useSpring({
    scale: 1,
    from: { scale: 0 },
    config: { mass: 1, tension: 280, friction: 20 },
  });
  return <animated.div style={{ transform: props.scale.to(s => `scale(${s})`) }} />;
}

// Trail (staggered animation)
function Trail({ items }) {
  const trail = useTrail(items.length, {
    opacity: 1, x: 0, from: { opacity: 0, x: -20 },
  });
  return trail.map((style, i) => (
    <animated.div key={i} style={style}>{items[i]}</animated.div>
  ));
}
```

## Summary

- React Spring is a spring-physics based animation library for React with declarative hooks API
- Spring-based animations produce natural, fluid motion that automatically adapts to velocity and interrupts
- useSpring, useTrail, useChain, and useTransition hooks cover single, sequenced, and mount/unmount animations
- Native animation support delegates to browser compositor for jank-free 60fps rendering
- TypeScript support with typed animated components and gesture interaction via react-use-gesture

---

### See Also

- [CSS Animations](02-CSS-Animations.md)
- [Framer Motion](01-Framer-Motion.md)
- [GSAP](05-GSAP.md)
- [Interview Questions](03-Interview-Questions.md)
- [Web Animations API](04-Web-Animations-API.md)

## References & Learn More

- [React Spring Documentation](https://www.react-spring.dev/)
- [React Spring Hooks API](https://www.react-spring.dev/docs/props/hooks)
