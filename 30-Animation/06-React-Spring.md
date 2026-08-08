---
section: Animation
category: Frontend
tags: [concept, reference]
---

# React Spring

> React Spring is a spring-physics-based animation library for React. Unlike CSS transitions or GSAP timelines, it uses natural spring physics (mass, tension, friction) to create fluid, natural-feeling motion that adapts to user input and interrupts.

## Definition

React Spring is a React animation library that uses spring physics instead of time-based easing. The library exposes hooks (`useSpring`, `useSprings`, `useTrail`, `useTransition`, `useChain`) that return animated values, which you apply to JSX via the `animated` component. It works on the web and React Native.

## Why It Matters (TL;DR)

- **Physics-based** — natural motion with mass / tension / friction
- **React + React Native** — same API across platforms
- **Hooks-first** — composable, no JSX wrappers
- **Interruptible** — springs adapt smoothly to new targets mid-animation
- **TypeScript-friendly** — typed animated components

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    REACT SPRING ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Spring Engine (no fixed duration)              │   │
│  │  • Config: mass, tension, friction, damping, precision      │   │
│  │  • Always tries to reach the target value                   │   │
│  │  • Adapts when the target changes mid-animation            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Hooks                                           │   │
│  │  • useSpring     — single animated value                   │   │
│  │  • useSprings    — multiple springs in parallel            │   │
│  │  • useTrail      — staggered single-value sequence         │   │
│  │  • useTransition — mount / unmount transitions             │   │
│  │  • useChain      — orchestrate multiple animations         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              animated.* Components                          │   │
│  │  • animated.div, animated.span, etc.                       │   │
│  │  • Accept spring values via style prop                     │   │
│  │  • Update outside React's render cycle (no re-renders)    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Spring

```tsx
import { useSpring, animated } from '@react-spring/web';

function FadeIn() {
  const styles = useSpring({
    from: { opacity: 0, y: 20 },
    to: { opacity: 1, y: 0 },
  });
  return <animated.div style={styles}>Hello</animated.div>;
}
```

### 2. Spring Config (Mass, Tension, Friction)

```tsx
function Bounce() {
  const styles = useSpring({
    from: { scale: 0 },
    to: { scale: 1 },
    config: {
      mass: 1,        // higher = heavier
      tension: 280,   // higher = faster
      friction: 20,   // higher = less bounce
    },
  });
  return <animated.div style={{ ...styles, transform: styles.scale.to((s) => `scale(${s})`) }} />;
}
```

### 3. useTrail — Staggered Sequence

```tsx
import { useTrail, animated } from '@react-spring/web';

function ListAnimation({ items }: { items: string[] }) {
  const trail = useTrail(items.length, {
    from: { opacity: 0, x: -20 },
    to: { opacity: 1, x: 0 },
    config: { tension: 200, friction: 20 },
  });

  return (
    <>
      {trail.map((style, i) => (
        <animated.div key={i} style={style}>
          {items[i]}
        </animated.div>
      ))}
    </>
  );
}
```

### 4. useTransition — Mount / Unmount

```tsx
import { useTransition, animated } from '@react-spring/web';

function ToggleList({ items }: { items: { id: number; text: string }[] }) {
  const transitions = useTransition(items, {
    from: { opacity: 0, height: 0 },
    enter: { opacity: 1, height: 80 },
    leave: { opacity: 0, height: 0 },
    config: { tension: 220, friction: 20 },
  });

  return transitions((style, item) => (
    <animated.div style={style}>{item.text}</animated.div>
  ));
}
```

### 5. useChain — Orchestrate Sequences

```tsx
import { useChain, useSpringRef, useSpring, useTrail, animated } from '@react-spring/web';

function ChainedAnimation() {
  const ref = useSpringRef();
  const titleSpring = useSpring({ ref, from: { opacity: 0 }, to: { opacity: 1 } });

  const trailRef = useSpringRef();
  const trail = useTrail(3, { ref: trailRef, from: { y: 30 }, to: { y: 0 } });

  useChain([ref, trailRef], [0, 0.5]); // trailRef starts when ref is 50% done

  return (
    <>
      <animated.h1 style={titleSpring}>Title</animated.h1>
      {trail.map((s, i) => (
        <animated.div key={i} style={s}>Item {i}</animated.div>
      ))}
    </>
  );
}
```

### 6. Interpolation (Stringify Animated Values)

```tsx
function RotateNumber() {
  const { x } = useSpring({ from: { x: 0 }, to: { x: 360 } });
  return <animated.div>{x.to((n) => `${Math.round(n)}°`)}</animated.div>;
}
```

### 7. useSprings — Parallel Independent Springs

```tsx
import { useSprings, animated } from '@react-spring/web';

function DraggableCards({ count = 5 }: { count?: number }) {
  const [springs, api] = useSprings(count, (i) => ({
    from: { y: -100 * i },
    to: { y: 0 },
    config: { tension: 200, friction: 18 },
  }));

  return (
    <>
      {springs.map((s, i) => (
        <animated.div key={i} style={{ ...s, position: 'absolute' }}>
          Card {i}
        </animated.div>
      ))}
    </>
  );
}
```

### 8. Spring with Reduced Motion

```tsx
import { useReducedMotion } from '@react-spring/web';

function Accessible() {
  const reduced = useReducedMotion();
  const styles = useSpring({
    from: { opacity: 0, y: reduced ? 0 : 20 },
    to:   { opacity: 1, y: 0 },
  });
  return <animated.div style={styles}>Content</animated.div>;
}
```

### 9. Spring with Imperative API

```tsx
import { useSpring, animated } from '@react-spring/web';

function Toggle() {
  const [open, setOpen] = useState(false);
  const styles = useSpring({
    height: open ? 200 : 0,
    config: { tension: 220, friction: 20 },
  });
  return (
    <animated.div style={{ overflow: 'hidden', ...styles }}>
      <button onClick={() => setOpen((o) => !o)}>Toggle</button>
    </animated.div>
  );
}
```

## React Spring vs Framer Motion

| Dimension | React Spring | Framer Motion |
|-----------|--------------|---------------|
| Motion model | Spring physics | Tween + spring + keyframe |
| Configuration | mass / tension / friction | stiffness / damping / mass |
| Hooks API | `useSpring`, `useTrail`, `useTransition`, `useChain` | `<motion>` + props |
| Interruptible | Naturally (springs always catch up) | Naturally (tweens get cancelled) |
| Best for | Natural, organic motion | Declarative React animations |
| Layout animations | Not built-in (use react-spring-layout) | Built-in `layout` prop |
| Gestures | `@react-spring/gesture` | Built-in (`whileHover`, `drag`) |
| Bundle | ~12 KB | ~30 KB |
| Learning curve | Spring physics + 5 hooks | Many props / variants |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using `style` directly with animated values | Use `animated.div` so the values update without re-rendering |
| Forgetting to interpolate | Use `.to(fn)` for string or computed values (e.g., `transform`) |
| Over-tuning config | Start with `{ tension: 200, friction: 20 }` and adjust |
| Animating non-transform properties | Stick to `transform`, `opacity` for GPU |
| Not using `useReducedMotion` | Detect the preference and skip motion |

## Best Practices

1. **Use `animated.*` components** — never apply spring values to plain HTML elements
2. **Configure with mass / tension / friction** — match the visual weight of the element
3. **Use `useTrail` for lists** — built-in stagger
4. **Use `useTransition` for mount / unmount** — animates items in / out
5. **Use `useChain` for orchestration** — sequence multiple animations
6. **Interpolate to strings** — `.to((n) => `${n}°``) for transform strings
7. **Use `useReducedMotion`** for accessibility

## Performance Considerations

```text
Why React Spring is performant:
┌─────────────────────────────────────────────────────────────────┐
│  • animated.* updates bypass React's render cycle              │
│  • Direct DOM mutations via ref                                │
│  • Single RAF loop for all springs                             │
│  • Spring values are objects, not state                        │
│                                                                 │
│  Bundle:                                                        │
│  • @react-spring/web: ~12 KB gzipped                           │
│  • @react-spring/three: ~6 KB (for R3F)                        │
│  • @react-spring/native: for React Native                     │
│  • @react-spring/gesture: ~5 KB                                │
│                                                                 │
│  Pitfalls:                                                       │
│  • Don't put spring values in React state                     │
│  • Don't re-create springs on every render                     │
│  • Stick to transform / opacity for 60fps                      │
└─────────────────────────────────────────────────────────────────┘
```

## Summary

- React Spring is the physics-based animation library for React — natural, interruptible motion
- Configure with `mass`, `tension`, `friction` instead of duration
- Five hooks: `useSpring`, `useSprings`, `useTrail`, `useTransition`, `useChain`
- Use `animated.div` to apply spring values without React re-renders
- `useReducedMotion` for accessibility

---

## Cheat Sheet

```text
REACT SPRING CHEAT SHEET
═══════════════════════════════════════════════════════════════

HOOKS:
  useSpring({ from, to, config })     → single value
  useSprings(count, factory)         → parallel
  useTrail(count, config)             → staggered
  useTransition(items, { from, enter, leave })
  useChain([refs], [positions])       → orchestration

SPRING CONFIG:
  mass: 1, tension: 200, friction: 20     // default-ish
  mass: 1, tension: 280, friction: 18     // snappier
  mass: 1, tension: 170, friction: 26     // softer
  precision: 0.0001                        // stop threshold

INTERPOLATION:
  const { x } = useSpring({ x: 0 });
  <animated.div>{x.to((n) => `${n}°`)}</animated.div>

INTERVIEW ANSWER:
  1. Spring physics (mass / tension / friction) vs tween duration
  2. Hooks: useSpring, useTrail, useTransition, useChain
  3. animated.* bypasses React's render cycle
  4. useReducedMotion for accessibility
```

---

## See Also

- [CSS Animations](02-CSS-Animations.md)
- [Framer Motion](01-Framer-Motion.md)
- [GSAP](05-GSAP.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [View Transitions & Scroll-Driven Animations](07-View-Transitions-and-Scroll-Driven-Animations.md)
- [Web Animations API](04-Web-Animations-API.md)


## References & Learn More

- [Common Spring Configurations](https://www.react-spring.dev/docs/advanced/config)
- [React Spring Documentation](https://www.react-spring.dev/)
- [React Spring Hooks API](https://www.react-spring.dev/docs/props/hooks)
- [react-use-gesture](https://github.com/pmndrs/use-gesture)
- [Spring Physics (Daniel Callander)](https://danielcwilson.com/blog/2018/02/spring-physics-with-javascript/)
