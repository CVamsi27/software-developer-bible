# React Interview Questions

## 60 Most Asked React Interview Questions

### Category 1: Fundamentals (Questions 1-15)

**Q1: What is React?**
A: React is a JavaScript library for building user interfaces, maintained by Meta. It uses a declarative, component-based architecture with a Virtual DOM for efficient UI updates.

**Q2: What is JSX?**
A: JSX is a syntax extension for JavaScript that looks like HTML. It compiles to `React.createElement()` calls, which produce Virtual DOM nodes.

**Q3: What is the Virtual DOM?**
A: The Virtual DOM is a lightweight JavaScript representation of the real DOM. React creates a new Virtual DOM tree on state changes, diffs it with the previous one, and applies minimal updates to the real DOM.

**Q4: What is the difference between React and ReactDOM?**
A: `react` is the core library defining components, hooks, and the Virtual DOM. `react-dom` is the renderer that bridges React to the actual DOM (browser).

**Q5: What are components in React?**
A: Components are reusable pieces of UI. They can be function components (using hooks) or class components (using lifecycle methods).

**Q6: What is the difference between class and function components?**
A: Class components use `class` syntax with lifecycle methods and `this.state`. Function components use hooks (`useState`, `useEffect`) and are simpler and more flexible.

**Q7: What is the component lifecycle?**
A: The series of events from mounting (creation), through updates, to unmounting (destruction). Class components use lifecycle methods; function components use `useEffect`.

**Q8: What is reconciliation?**
A: Reconciliation is React's diffing algorithm that compares the new Virtual DOM with the previous one to determine the minimal set of DOM changes needed.

**Q9: What is the key prop used for?**
A: The `key` prop helps React identify which list items have changed, been added, or removed. It enables efficient list updates by matching elements across renders.

**Q10: What is prop drilling?**
A: Prop drilling is passing props through intermediate components that don't use them. It's solved by Context API or state management libraries.

**Q11: What are props?**
A: Props (properties) are read-only data passed from parent to child components. They configure child components and trigger re-renders when changed.

**Q12: What is state in React?**
A: State is internal data owned by a component. It's mutable and triggers re-renders when updated via `setState` or `useState`.

**Q13: What is the difference between state and props?**
A: State is internal and mutable. Props are external and read-only. State changes trigger re-renders; props changes trigger re-renders of the receiving component.

**Q14: What is the children prop?**
A: The `children` prop is a special prop that contains the content between a component's opening and closing tags.

**Q15: What are fragments?**
A: Fragments (`<React.Fragment>` or `<>...</>`) let you group multiple elements without adding extra DOM nodes.

---

### Category 2: Hooks (Questions 16-30)

**Q16: What are hooks?**
A: Hooks are functions that let you use state and lifecycle features in function components. They were introduced in React 16.8.

**Q17: What is useState?**
A: `useState` is a hook that adds state to function components. It returns a stateful value and a setter function.

**Q18: What is useEffect?**
A: `useEffect` is a hook that performs side effects after rendering. It runs after the browser paints and can return a cleanup function.

**Q19: What is the dependency array in useEffect?**
A: The dependency array tells React when to re-run the effect. Empty array `[]` = run once on mount. With deps = run when deps change. No array = run every render.

**Q20: What is the cleanup function in useEffect?**
A: The cleanup function runs before the effect re-runs (when deps change) and when the component unmounts. It's used for subscriptions, timers, and event listeners.

**Q21: What is useRef?**
A: `useRef` creates a mutable reference object with a `.current` property. It's used for DOM access and persistent values that don't trigger re-renders.

**Q22: What is useMemo?**
A: `useMemo` memoizes a computed value, only re-computing when dependencies change. Used for expensive computations.

**Q23: What is useCallback?**
A: `useCallback` memoizes a function reference, only re-creating when dependencies change. Used for functions passed to memoized children.

**Q24: What is useReducer?**
A: `useReducer` is a hook for complex state with multiple sub-values. It uses a reducer function similar to Redux.

**Q25: What is useContext?**
A: `useContext` is a hook that reads values from the nearest Context Provider without prop drilling.

**Q26: What is useLayoutEffect?**
A: `useLayoutEffect` runs synchronously after DOM mutations but before browser paint. Used for DOM measurements.

**Q27: What is useImperativeHandle?**
A: `useImperativeHandle` customizes the value exposed via `ref`, limiting what parent components can access.

**Q28: What are custom hooks?**
A: Custom hooks are functions that start with `use` and encapsulate reusable stateful logic. They can call other hooks.

**Q29: What are the rules of hooks?**
A: 1. Only call hooks at the top level (not in conditions, loops, or nested functions). 2. Only call hooks from React functions (components or custom hooks).

**Q30: What is useTransition?**
A: `useTransition` marks state updates as non-urgent, allowing React to defer them. It returns `isPending` and a `startTransition` function.

---

### Category 3: Advanced Concepts (Questions 31-45)

**Q31: What is React.memo?**
A: `React.memo` is a higher-order component that prevents re-rendering when props haven't changed (shallow comparison).

**Q32: What is the difference between React.memo and useMemo?**
A: `React.memo` prevents component re-renders. `useMemo` memoizes computed values. They serve different purposes.

**Q33: What is code splitting?**
A: Code splitting is splitting your bundle into smaller chunks loaded on demand using `React.lazy` and `Suspense`.

**Q34: What is Suspense?**
A: Suspense lets you "suspend" rendering until some condition is met (data loading). It shows a fallback UI while waiting.

**Q35: What is React.lazy?**
A: `React.lazy` is a function that lets you lazily load components, importing them dynamically.

**Q36: What are Error Boundaries?**
A: Error Boundaries are class components that catch JavaScript errors in their child component tree and display fallback UI.

**Q37: What is the Context API?**
A: Context API is React's solution for sharing data across the component tree without prop drilling.

**Q38: What is the difference between Context and Redux?**
A: Context is simple, built-in, good for themes/auth. Redux is complex, has devtools/middleware, good for complex state logic.

**Q39: What is React Fiber?**
A: React Fiber is React's reconciliation engine that enables incremental rendering, prioritization, and concurrent features.

**Q40: What is concurrent rendering?**
A: Concurrent rendering allows React to prepare multiple UI versions simultaneously, pausing and resuming work to keep the UI responsive.

**Q41: What is useDeferredValue?**
A: `useDeferredValue` returns a deferred version of a value that can lag behind its source, keeping the UI responsive.

**Q42: What is the difference between useTransition and useDeferredValue?**
A: `useTransition` marks updates as non-urgent. `useDeferredValue` creates a lagging derived value. They serve different purposes.

**Q43: What is flushSync?**
A: `flushSync` forces React to synchronously flush pending state updates. Used when you need immediate DOM updates.

**Q44: What is the difference between useEffect and useLayoutEffect?**
A: `useLayoutEffect` runs after DOM mutation, before paint (sync). `useEffect` runs after paint (async).

**Q45: What is the relationship between React and TypeScript?**
A: React has first-class TypeScript support. TypeScript provides type safety for props, state, hooks, and context.

---

### Category 4: Performance (Questions 46-55)

**Q46: How do you optimize React performance?**
A: Use React.memo, useMemo, useCallback, virtualization, code splitting, concurrent features, and state colocation.

**Q47: What is the impact of inline objects in JSX?**
A: Inline objects create new references on every render, causing memoized children to re-render unnecessarily.

**Q48: What is virtualization?**
A: Virtualization renders only visible items in a list, not all items, reducing DOM nodes and re-renders.

**Q49: What is the difference between useMemo and useCallback?**
A: `useMemo` memoizes values. `useCallback` memoizes functions. `useCallback(fn, deps)` is equivalent to `useMemo(() => fn, deps)`.

**Q50: What is the performance impact of Context?**
A: Context updates cause all consumers to re-render. Memoize value and split contexts to reduce impact.

**Q51: How do you profile React performance?**
A: Use React DevTools Profiler, Chrome DevTools Performance, and React.Profiler component.

**Q52: What is the impact of large component trees?**
A: Deep trees cause longer traversal times. Flatten hierarchy and use React.memo to prevent unnecessary re-renders.

**Q53: How do you optimize forms?**
A: Use controlled components, debounce inputs, validate lazily, and use form libraries like React Hook Form.

**Q54: What is the impact of re-renders?**
A: Re-renders cause Virtual DOM creation, diffing, and potential DOM updates. Minimize with memoization and state colocation.

**Q55: How do you handle performance in large apps?**
A: Profile first, memoize expensive components, virtualize lists, code split routes, and split contexts.

---

### Category 5: Architecture and Patterns (Questions 56-60)

**Q56: What are the common React design patterns?**
A: Container/Presentational, Higher-Order Components, Render Props, Compound Components, Custom Hooks.

**Q57: What is the difference between controlled and uncontrolled components?**
A: Controlled components have their value managed by React state. Uncontrolled components manage their own state via DOM refs.

**Q58: What is the Container/Presentational pattern?**
A: Container components handle logic and state. Presentational components handle UI. Separation of concerns.

**Q59: What are Higher-Order Components (HOCs)?**
A: HOCs are functions that take a component and return a new component with added functionality.

**Q60: What is the future of React?**
A: React is moving toward automatic memoization (React Compiler), Server Components, concurrent features, and better developer experience.

---

## Categorized by Difficulty

### Beginner (Questions 1-15)
Covers: What is React, JSX, Virtual DOM, components, props, state, lifecycle basics.

### Intermediate (Questions 16-35)
Covers: Hooks, useEffect, useRef, useMemo, useCallback, Context, Suspense, code splitting.

### Senior (Questions 36-55)
Covers: Error Boundaries, React Fiber, concurrent rendering, performance optimization, architecture patterns.

### FAANG-style (Questions 56-60)
Covers: Design patterns, architecture decisions, system design, future of React.

## Summary

This guide covers 60 essential React interview questions across all difficulty levels. Master these topics to demonstrate deep understanding of React's architecture, hooks, performance optimization, and best practices.

## References & Learn More

- [React Interview Questions](https://github.com/sudheerj/reactjs-interview-questions)
- [React Docs](https://react.dev/)
- [React Patterns](https://reactpatterns.com/)
- [Kent C. Dodds Blog](https://kentcdodds.com/blog)
