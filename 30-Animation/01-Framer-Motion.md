---
section: Animation
category: Frontend
tags: [concept]
---

# Framer Motion

## Definition
Framer Motion is a production-ready React animation library that provides a simple, declarative API for creating smooth, performant animations. It handles complex animation logic while maintaining excellent performance through hardware acceleration.

## Why Do We Need It?

- **Simple API**: Declarative animations with minimal code
- **Performance**: Hardware-accelerated animations
- **Gestures**: Built-in gesture recognition (drag, hover, tap)
- **Layout Animations**: Automatic layout transitions
- **Variants**: Reusable animation states

## How It Works

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    FRAMER MOTION ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Motion Components                         │   │
│  │  • motion.div, motion.span, etc.                            │   │
│  │  • AnimatePresence for exit animations                      │   │
│  │  • layout for automatic layout transitions                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Animation Engine                          │   │
│  │  • Spring physics                                           │   │
│  │  • Tween animations                                         │   │
│  │  • Keyframe animations                                      │   │
│  │  • Gesture handling                                         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Performance Layer                           │   │
│  │  • GPU acceleration (transform, opacity)                    │   │
│  │  • Will-change optimization                                 │   │
│  │  • Batch updates                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

```

## Code Examples

### 1. Basic Animations

```typescript
import { motion } from 'framer-motion';

function BasicAnimation() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      Hello, Framer Motion!
    </motion.div>
  );
}

// With spring animation
function SpringAnimation() {
  return (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: 'spring', stiffness: 260, damping: 20 }}
    >
      Spring Animation
    </motion.div>
  );
}

// With keyframes
function KeyframeAnimation() {
  return (
    <motion.div
      animate={{
        scale: [1, 1.2, 1],
        rotate: [0, 10, -10, 0],
      }}
      transition={{
        duration: 0.5,
        repeat: Infinity,
        repeatDelay: 1,
      }}
    >
      Keyframe Animation
    </motion.div>
  );
}

```

### 2. Gesture Animations

```typescript
import { motion } from 'framer-motion';

function GestureAnimation() {
  return (
    <motion.div
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      whileDrag={{ scale: 1.05, rotate: 5 }}
      drag
      dragConstraints={{ left: -100, right: 100, top: -100, bottom: 100 }}
      dragElastic={0.1}
    >
      Drag, Hover, Tap
    </motion.div>
  );
}

// Drag with constraints
function ConstrainedDrag() {
  return (
    <motion.div
      drag
      dragConstraints={{
        top: -50,
        left: -50,
        right: 50,
        bottom: 50,
      }}
      dragTransition={{ bounceStiffness: 600, bounceDamping: 20 }}
      whileDrag={{ cursor: 'grabbing' }}
    >
      Constrained Drag
    </motion.div>
  );
}

```

### 3. Variants

```typescript
import { motion } from 'framer-motion';

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
  },
};

function ListAnimation() {
  return (
    <motion.ul
      variants={containerVariants}
      initial="hidden"
      animate="visible"
    >
      {['Item 1', 'Item 2', 'Item 3'].map((item, index) => (
        <motion.li key={index} variants={itemVariants}>
          {item}
        </motion.li>
      ))}
    </motion.ul>
  );
}

// Custom variants
const boxVariants = {
  idle: {
    scale: 1,
    rotate: 0,
  },
  hover: {
    scale: 1.1,
    rotate: 5,
    transition: {
      type: 'spring',
      stiffness: 300,
    },
  },
  tap: {
    scale: 0.95,
    rotate: -5,
  },
};

function CustomVariants() {
  return (
    <motion.div
      variants={boxVariants}
      initial="idle"
      whileHover="hover"
      whileTap="tap"
    >
      Custom Variants
    </motion.div>
  );
}

```

### 4. AnimatePresence

```typescript
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

function AnimatePresenceExample() {
  const [isVisible, setIsVisible] = useState(true);

  return (
    <div>
      <button onClick={() => setIsVisible(!isVisible)}>
        Toggle
      </button>

      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            transition={{ duration: 0.3 }}
          >
            Animated Content
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Page transitions
function PageTransition() {
  const [page, setPage] = useState(0);

  return (
    <div>
      <button onClick={() => setPage(1)}>Page 1</button>
      <button onClick={() => setPage(2)}>Page 2</button>

      <AnimatePresence mode="wait">
        <motion.div
          key={page}
          initial={{ opacity: 0, x: -100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 100 }}
          transition={{ duration: 0.3 }}
        >
          {page === 1 ? <Page1 /> : <Page2 />}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}

```

### 5. Layout Animations

```typescript
import { motion, LayoutGroup } from 'framer-motion';
import { useState } from 'react';

function LayoutAnimation() {
  const [items, setItems] = useState([
    { id: 1, color: 'red' },
    { id: 2, color: 'blue' },
    { id: 3, color: 'green' },
  ]);

  const reorder = () => {
    setItems([...items].reverse());
  };

  return (
    <LayoutGroup>
      <button onClick={reorder}>Reorder</button>

      {items.map((item) => (
        <motion.div
          key={item.id}
          layout
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            width: 100,
            height: 100,
            backgroundColor: item.color,
          }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        >
          {item.id}
        </motion.div>
      ))}
    </LayoutGroup>
  );
}

```

### 6. Scroll Animations

```typescript
import { motion, useScroll, useTransform } from 'framer-motion';

function ScrollAnimation() {
  const { scrollYProgress } = useScroll();
  const scale = useTransform(scrollYProgress, [0, 1], [1, 2]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <motion.div
      style={{ scale, opacity }}
    >
      Scroll to animate
    </motion.div>
  );
}

// Parallax effect
function ParallaxEffect() {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, 200]);

  return (
    <motion.div style={{ y }}>
      Parallax Content
    </motion.div>
  );
}

// Scroll-triggered animation
function ScrollTriggered() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-100px' }}
      transition={{ duration: 0.5 }}
    >
      Animate when in view
    </motion.div>
  );
}

```

### 7. Animation Controls

```typescript
import { motion, useAnimation, useMotionValue } from 'framer-motion';

function AnimationControls() {
  const controls = useAnimation();

  const sequence = async () => {
    await controls.start({ scale: 1.2 });
    await controls.start({ rotate: 180 });
    await controls.start({ scale: 1 });
    await controls.start({ rotate: 0 });
  };

  return (
    <motion.div
      animate={controls}
      onClick={sequence}
    >
      Click to animate
    </motion.div>
  );
}

// Motion values
function MotionValues() {
  const x = useMotionValue(0);
  const opacity = useTransform(x, [-200, 0, 200], [0, 1, 0]);

  return (
    <motion.div
      drag="x"
      dragConstraints={{ left: -200, right: 200 }}
      style={{ x, opacity }}
    >
      Drag me
    </motion.div>
  );
}

```

## Real-World Use Cases

### Modal Animation

```typescript
import { motion, AnimatePresence } from 'framer-motion';

function Modal({ isOpen, onClose, children }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal-backdrop"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="modal-content"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

```

### Loading Spinner

```typescript
import { motion } from 'framer-motion';

function LoadingSpinner() {
  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{
        duration: 1,
        repeat: Infinity,
        ease: 'linear',
      }}
      className="spinner"
    />
  );
}

```

## Common Mistakes

1. **Animating non-transform properties**: Use transform for better performance

2. **Missing AnimatePresence**: Exit animations won't work without it

3. **Overusing animations**: Too many animations hurt UX

4. **Ignoring prefers-reduced-motion**: Accessibility concern

5. **Not cleaning up**: Animations can cause memory leaks

## Best Practices

1. **Use transform properties**: opacity, scale, rotate, x, y

2. **Use AnimatePresence**: For exit animations

3. **Respect user preferences**: Check prefers-reduced-motion

4. **Keep animations subtle**: Enhance UX, don't distract

5. **Use variants**: For reusable animation states

## Performance Considerations

```text
Animation Performance:
┌─────────────────────────────────────────────────────────────────┐
│  GPU Accelerated (Good):                                         │
│  • transform: translate, scale, rotate                          │
│  • opacity                                                      │
│                                                                 │
│  CPU Heavy (Avoid):                                             │
│  • width, height                                                │
│  • top, left, right, bottom                                     │
│  • margin, padding                                              │
│                                                                 │
│  Framer Motion Optimizations:                                    │
│  • Automatic will-change                                         │
│  • Hardware acceleration                                        │
│  • Batch updates                                                │
│  • Optimized re-renders                                          │
└─────────────────────────────────────────────────────────────────┘

```

## Summary

Framer Motion provides a powerful, declarative API for creating performant animations in React. Master its components, gestures, and layout animations to build delightful user experiences.

---

## See Also
- [Performance Monitoring](../26-Performance-Monitoring/)
- [React](../03-React/)

## References & Learn More

- [Framer Motion Documentation](https://www.framer.com/motion/)
- [Framer Motion GitHub](https://github.com/framer/motion)
- [Animation Examples](https://www.framer.com/motion/)
- [Gesture Examples](https://www.framer.com/motion/gestures/)
- [Layout Animations](https://www.framer.com/motion/layout-animations/)
