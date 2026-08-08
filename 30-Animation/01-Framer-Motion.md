---
section: Animation
category: Frontend
tags: [concept, reference]
---

# Framer Motion

> Framer Motion is a production-ready React animation library that provides a declarative API for smooth, performant animations. It handles complex animation logic — gestures, layout transitions, exit animations, scroll-linked motion — while staying hardware-accelerated.

## Definition

Framer Motion is a React animation library from the Framer team (now `motion/react`). It exposes `motion` components (`motion.div`, `motion.span`, etc.) that wrap native elements and accept `initial`, `animate`, `exit`, `whileHover`, `whileTap`, `whileInView`, and `layout` props. Built on the Web Animations API + style projections for 60fps on the compositor thread.

## Why It Matters (TL;DR)

- **Declarative API** — props describe the animation, not the steps
- **Gestures** — built-in drag, hover, tap, pan, focus recognition
- **Layout animations** — automatic FLIP-style transitions when elements move
- **AnimatePresence** — exit animations on unmount
- **Hardware-accelerated** — animates transform / opacity via the compositor

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    FRAMER MOTION ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Motion Components                         │   │
│  │  • motion.div, motion.span, etc. (1:1 with HTML elements) │   │
│  │  • AnimatePresence → handles exit animations on unmount    │   │
│  │  • LayoutGroup + layout prop → automatic FLIP transitions  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Animation Engine                          │   │
│  │  • Spring physics (mass, stiffness, damping)                │   │
│  │  • Tween animations (duration, ease)                        │   │
│  │  • Keyframe animations (multi-step)                        │   │
│  │  • Gesture handling (drag, hover, tap, pan)                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Performance Layer                           │   │
│  │  • GPU acceleration for transform / opacity                │   │
│  │  • Style projection — minimal React re-renders             │   │
│  │  • Will-change applied automatically                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Animations

```typescript
import { motion } from 'framer-motion';

function FadeIn() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: 'easeOut' }}
    >
      Hello, Framer Motion!
    </motion.div>
  );
}

function SpringIn() {
  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: 'spring', stiffness: 260, damping: 20 }}
    >
      Spring!
    </motion.div>
  );
}

function KeyframeLoop() {
  return (
    <motion.div
      animate={{ scale: [1, 1.2, 1], rotate: [0, 10, -10, 0] }}
      transition={{ duration: 0.6, repeat: Infinity, repeatDelay: 1 }}
    />
  );
}
```

### 2. Gesture Animations

```typescript
function Draggable() {
  return (
    <motion.div
      drag
      dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
      dragElastic={0.1}
      dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
      whileDrag={{ scale: 1.05, cursor: 'grabbing' }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      Drag me
    </motion.div>
  );
}
```

### 3. Variants (Reusable Animation States)

```typescript
import type { Variants } from 'framer-motion';

const container: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const item: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { type: 'spring' } },
};

function ListAnimation() {
  return (
    <motion.ul variants={container} initial="hidden" animate="visible">
      {['A', 'B', 'C'].map((label) => (
        <motion.li key={label} variants={item}>{label}</motion.li>
      ))}
    </motion.ul>
  );
}
```

### 4. AnimatePresence (Exit Animations)

```typescript
import { AnimatePresence } from 'framer-motion';

function Toggle() {
  const [isVisible, setVisible] = useState(true);
  return (
    <>
      <button onClick={() => setVisible((v) => !v)}>Toggle</button>
      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.3 }}
          >
            Content
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

function PageTransition({ pathname }: { pathname: string }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        exit={{ opacity: 0, x: 20 }}
        transition={{ duration: 0.25 }}
      >
        {/* page content */}
      </motion.div>
    </AnimatePresence>
  );
}
```

### 5. Layout Animations (FLIP)

```typescript
import { LayoutGroup } from 'framer-motion';

function ReorderableList() {
  const [items, setItems] = useState([1, 2, 3, 4]);
  return (
    <LayoutGroup>
      <button onClick={() => setItems([...items].reverse())}>Reverse</button>
      {items.map((id) => (
        <motion.div
          key={id}
          layout
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        >
          {id}
        </motion.div>
      ))}
    </LayoutGroup>
  );
}

// Shared layout between two trees (e.g., card → modal)
function SharedLayout() {
  const [selected, setSelected] = useState<string | null>(null);
  return (
    <>
      {items.map((item) =>
        selected === item.id ? (
          <motion.div layoutId={item.id} key={item.id} onClick={() => setSelected(null)}>
            {/* full content */}
          </motion.div>
        ) : (
          <motion.div layoutId={item.id} key={item.id} onClick={() => setSelected(item.id)}>
            {/* thumbnail */}
          </motion.div>
        )
      )}
    </>
  );
}
```

### 6. Scroll-Linked Animations

```typescript
function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useTransform(scrollYProgress, [0, 1], [0, 1]);
  return <motion.div style={{ scaleX, transformOrigin: '0% 50%' }} className="progress-bar" />;
}

function Parallax() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, 200]);
  return <motion.div style={{ y }}>Parallax content</motion.div>;
}

function RevealOnScroll() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.5 }}
    >
      Revealed when in view
    </motion.div>
  );
}
```

### 7. Imperative Controls (`useAnimation` + `useMotionValue`)

```typescript
function AnimatedButton() {
  const controls = useAnimation();

  const sequence = async () => {
    await controls.start({ scale: 1.2 });
    await controls.start({ rotate: 180 });
    await controls.start({ scale: 1, rotate: 0 });
  };

  return <motion.div animate={controls} onClick={sequence}>Click me</motion.div>;
}

function MotionValue() {
  const x = useMotionValue(0);
  const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0]);

  return (
    <motion.div drag="x" dragConstraints={{ left: -200, right: 200 }} style={{ x, opacity }}>
      Drag me
    </motion.div>
  );
}
```

## Real-World Use Cases

```text
COMMON USE CASES:
  • Modal open/close with backdrop fade
  • Page transitions (route change)
  • List reordering (drag-and-drop, sortable tables)
  • Reveal-on-scroll for marketing pages
  • Loading spinners and skeletons
  • Notification toasts (slide in / out)
  • Accordion / collapsible content
  • Image gallery with shared layout (thumbnail → lightbox)
  • Hover / tap micro-interactions
  • Hero animations (text reveal, illustrations)
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Animating layout properties (`width`, `height`, `top`) | Animate `transform` (`scale`, `y`, `x`) and `opacity` only |
| Missing `<AnimatePresence>` for exit animations | Wrap conditional rendering in `<AnimatePresence>` to animate on unmount |
| Animating too many elements at once | Use `LayoutGroup` for shared layout, or virtualize long lists |
| Forgetting `prefers-reduced-motion` | Check the media query; provide instant or no animation when set |
| Not keying the layout element | `<motion.div layoutId="x">` requires consistent IDs across trees |

## Best Practices

1. **Animate transform / opacity only** — they're GPU-accelerated
2. **Use `AnimatePresence` for exit animations** — without it, unmount is instant
3. **Respect `prefers-reduced-motion`** — accessibility requirement
4. **Use variants for complex sequences** — declarative, composable
5. **Use `layout` for FLIP transitions** — automatic, no math
6. **Avoid running on the main thread** — let motion handle the projection
7. **Test on low-end devices** — animations that look great on M3 may jank on a $200 Android

## Performance Considerations

```text
GPU-Accelerated (Good — animate these):
  • transform: translate, scale, rotate
  • opacity
  • filter (some)

CPU-Heavy (Avoid — triggers layout):
  • width, height, top, left, right, bottom
  • margin, padding
  • box-shadow with blur
  • font-size, line-height

Framer Motion Optimizations:
  • Style projection — minimal React re-renders
  • Automatic will-change for active animations
  • Hardware acceleration
  • Batch updates in RAF loop

Bundle:
  • ~30 KB gzipped (core)
  • Tree-shakeable
  • Lazy-load for routes that don't use it
```

## Summary

- Framer Motion is the de-facto React animation library — declarative, gesture-aware, hardware-accelerated
- Animate `transform` and `opacity` only; everything else triggers layout
- `<AnimatePresence>` enables exit animations; `layout` enables FLIP-style transitions
- Respect `prefers-reduced-motion` for accessibility
- Use `useMotionValue` for high-frequency updates that bypass React state

---

## Cheat Sheet

```text
FRAMER MOTION CHEAT SHEET
═══════════════════════════════════════════════════════════════

CORE PROPS:
  initial     → starting state
  animate     → target state
  exit        → state on unmount (requires AnimatePresence)
  transition  → { duration, ease, type: 'spring' | 'tween' }
  whileHover  / whileTap / whileDrag / whileFocus
  whileInView → animate when scrolled into view
  layout      → animate layout changes (FLIP)
  layoutId    → shared layout across trees

COMPONENTS:
  motion.div, motion.span, etc. (1:1 HTML)
  AnimatePresence → exit animations
  LayoutGroup     → coordinate layouts

HOOKS:
  useAnimation()         → imperative controls
  useMotionValue()       → high-freq values, no re-render
  useTransform()         → derive from a motion value
  useScroll()            → { scrollY, scrollYProgress }
  useDragControls()      → programmatic drag

INTERVIEW ANSWER:
  1. Animate transform / opacity only (GPU)
  2. AnimatePresence for exit; layout for FLIP
  3. Respect prefers-reduced-motion
  4. useMotionValue bypasses React for hot paths
```

---

## See Also

- [CSS Animations](02-CSS-Animations.md)
- [GSAP](05-GSAP.md)
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)
- [React Spring](06-React-Spring.md)
- [View Transitions & Scroll-Driven Animations](07-View-Transitions-and-Scroll-Driven-Animations.md)
- [Web Animations API](04-Web-Animations-API.md)


## References & Learn More

- [Animation Performance (web.dev)](https://web.dev/animations/)
- [Framer Motion Documentation](https://motion.dev/)
- [Gestures](https://motion.dev/docs/react-gestures)
- [Layout Animations](https://motion.dev/docs/react-layout-animations)
- [Motion (Framer Motion GitHub)](https://github.com/framer/motion)
- [useScroll](https://motion.dev/docs/react-use-scroll)
