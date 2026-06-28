# JavaScript Interview Questions

## 50 Most Asked JavaScript Interview Questions

### Beginner Level (10 Questions)

**Q1: What is JavaScript?**

A: JavaScript is a high-level, interpreted programming language primarily used for web development. It's single-threaded, event-driven, and supports both object-oriented and functional programming paradigms.

**Q2: What are the different data types in JavaScript?**

A: Primitive types: Number, String, Boolean, null, undefined, Symbol, BigInt. Reference types: Object, Array, Function, Date, RegExp, Map, Set.

**Q3: What is the difference between `let`, `const`, and `var`?**

A:
- `var`: Function-scoped, hoisted, reassignable
- `let`: Block-scoped, not hoisted (TDZ), reassignable
- `const`: Block-scoped, not hoisted (TDZ), not reassignable

**Q4: What is hoisting?**

A: Hoisting is JavaScript's behavior of moving declarations to the top of their scope during the creation phase. `var` declarations are hoisted and initialized to `undefined`, while `let`/`const` are hoisted but remain in the Temporal Dead Zone.

**Q5: What is the difference between `==` and `===`?**

A: `==` performs type coercion before comparison (loose equality). `===` compares both value and type without coercion (strict equality).

**Q6: What are closures?**

A: A closure is a function that retains access to its outer scope's variables even after the outer function has returned. Closures are created every time a function is created.

**Q7: What is `this` in JavaScript?**

A: `this` refers to the object that is currently executing the code. Its value depends on how a function is called: global context (window/undefined), method call (object), constructor (new instance), or explicit binding (call/apply/bind).

**Q8: What is the event loop?**

A: The event loop is the mechanism that allows JavaScript to perform non-blocking operations. It continuously checks the call stack and callback queues, executing tasks when the stack is empty.

**Q9: What is the difference between synchronous and asynchronous code?**

A: Synchronous code executes immediately and blocks further execution. Asynchronous code is scheduled to run later, allowing other code to execute while waiting.

**Q10: What are Promises?**

A: A Promise is an object representing the eventual completion or failure of an asynchronous operation. It has three states: pending, fulfilled, and rejected.

### Intermediate Level (10 Questions)

**Q11: Explain the difference between primitive and reference types.**

A: Primitives (number, string, boolean) are passed by value - copying the actual value. References (objects, arrays) are passed by value of the reference - both variables point to the same object.

**Q12: What is prototypal inheritance?**

A: JavaScript uses prototypal inheritance where objects inherit from other objects via the prototype chain. Each object has a `[[Prototype]]` property that references another object.

**Q13: What is the difference between `map`, `filter`, and `reduce`?**

A:
- `map`: Transforms each element, returns new array
- `filter`: Selects elements based on condition, returns new array
- `reduce`: Accumulates elements into a single value

**Q14: What is destructuring?**

A: Destructuring is a syntax that unpacks values from arrays or properties from objects into distinct variables: `const { name, age } = person;`

**Q15: What are template literals?**

A: Template literals use backticks and `${expression}` syntax for string interpolation: `` `Hello, ${name}!` ``

**Q16: What is the spread operator?**

A: The spread operator `...` expands an iterable into individual elements: `const newArray = [...oldArray];` or `const newObj = { ...oldObj };`

**Q17: What is async/await?**

A: Async/await is syntactic sugar over Promises. `async` functions return Promises, and `await` pauses execution until a Promise settles.

**Q18: What are the different ways to create objects?**

A: Object literals `{}`, constructor functions `new Func()`, `Object.create()`, class syntax `class Foo {}`, and factory functions.

**Q19: What is event delegation?**

A: Event delegation is a technique where a single event listener is attached to a parent element to handle events for all its children, using event bubbling.

**Q20: What is the difference between `null` and `undefined`?**

A: `undefined` means a variable has been declared but not assigned. `null` is an intentional assignment of "no value".

### Senior Level (15 Questions)

**Q21: Explain the execution context and scope chain.**

A: Execution context is the environment where code runs. It contains the lexical environment, variable environment, and `this` binding. The scope chain is the hierarchy of scopes used to resolve variables.

**Q22: What is the difference between call, apply, and bind?**

A:
- `call`: Invokes function with specific `this` and individual arguments
- `apply`: Invokes function with specific `this` and arguments array
- `bind`: Returns new function with `this` permanently bound

**Q23: How does garbage collection work in JavaScript?**

A: JavaScript uses mark-and-sweep algorithm. It marks all reachable objects from roots, then sweeps (collects) unmarked objects. Generational GC optimizes by separating young and old objects.

**Q24: What is the difference between debouncing and throttling?**

A: Debouncing delays execution until a pause in calls. Throttling limits execution to once per interval. Debounce for search, throttle for scroll.

**Q25: How do you prevent memory leaks?**

A: Clean up event listeners, clear timers, use WeakMap/WeakRef, limit cache sizes, and properly handle React useEffect cleanup.

**Q26: What is the difference between shallow and deep copy?**

A: Shallow copy copies top-level properties but nested objects are shared references. Deep copy creates independent copies of all nested objects.

**Q27: Explain the module system (CommonJS vs ES Modules).**

A: CommonJS uses `require()` and is synchronous (Node.js). ES Modules use `import/export`, are asynchronous, support tree shaking, and work in browsers.

**Q28: What are generators and their use cases?**

A: Generators are functions that can be paused and resumed using `yield`. Use cases: lazy evaluation, infinite sequences, async flows, state machines.

**Q29: How does `this` work in arrow functions vs regular functions?**

A: Arrow functions don't have their own `this` - they inherit from the enclosing lexical scope. Regular functions have `this` based on how they're called.

**Q30: What is memoization and when should you use it?**

A: Memoization caches function results for repeated inputs. Use for expensive computations, API calls, and recursive functions. Trade memory for time.

**Q31: Explain the event loop phases in Node.js.**

A: Node.js event loop has phases: timers, I/O callbacks, idle/prepare, poll, check, close callbacks. `process.nextTick` runs before microtasks.

**Q32: What is the difference between iteration and recursion?**

A: Iteration uses loops, recursion uses function calls. Iteration is generally more memory-efficient. Recursion is cleaner for tree/graph problems.

**Q33: How do you implement immutability in JavaScript?**

A: Use `Object.freeze()`, spread operator for copies, pure functions, and immutable data structures (Immutable.js).

**Q34: What is currying and when is it useful?**

A: Currying transforms a function with multiple arguments into a series of functions each taking one argument. Useful for partial application and function composition.

**Q35: Explain the difference between microtasks and macrotasks.**

A: Microtasks (Promises, queueMicrotask) run after current task, before next macrotask. Macrotasks (setTimeout, I/O) run one per event loop iteration.

### FAANG-style (10 Questions)

**Q36: Design a debounce function from scratch.**

A: Use setTimeout and clearTimeout. Each call clears previous timer and sets new one. Support leading/trailing options, cancel, and flush methods.

```typescript
function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  return function(this: any, ...args: Parameters<T>) {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func.apply(this, args), wait);
  };
}
```

**Q37: Implement a memoization function with LRU cache.**

A: Use Map for cache, track access order, evict least recently used when full.

```typescript
function memoize<T extends (...args: any[]) => any>(fn: T, maxSize = 100) {
  const cache = new Map<string, ReturnType<T>>();

  return function(...args: Parameters<T>) {
    const key = JSON.stringify(args);
    if (cache.has(key)) return cache.get(key)!;

    if (cache.size >= maxSize) {
      const firstKey = cache.keys().next().value;
      cache.delete(firstKey);
    }

    const result = fn(...args);
    cache.set(key, result);
    return result;
  };
}
```

**Q38: Design an event emitter class.**

A: Implement `on`, `off`, `emit` methods using a Map to store listeners by event name.

```typescript
class EventEmitter {
  private listeners = new Map<string, Set<Function>>();

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
    return () => this.off(event, callback);
  }

  off(event: string, callback: Function) {
    this.listeners.get(event)?.delete(callback);
  }

  emit(event: string, ...args: any[]) {
    this.listeners.get(event)?.forEach(cb => cb(...args));
  }
}
```

**Q39: Implement a deep clone function.**

A: Handle objects, arrays, Dates, RegExps, Maps, Sets, and circular references using WeakMap.

```typescript
function deepClone<T>(obj: T, seen = new WeakMap()): T {
  if (obj === null || typeof obj !== 'object') return obj;
  if (seen.has(obj as object)) return seen.get(obj as object);

  if (obj instanceof Date) return new Date(obj) as T;
  if (obj instanceof RegExp) return new RegExp(obj) as T;

  const clone = Array.isArray(obj) ? [] : Object.create(Object.getPrototypeOf(obj));
  seen.set(obj as object, clone);

  for (const key of Reflect.ownKeys(obj)) {
    clone[key] = deepClone((obj as any)[key], seen);
  }

  return clone;
}
```

**Q40: Design a promise-based task scheduler with concurrency control.**

A: Use a queue, track running tasks, process queue when slots available.

```typescript
class TaskScheduler {
  private queue: (() => Promise<any>)[] = [];
  private running = 0;

  constructor(private maxConcurrent: number = 5) {}

  async add<T>(task: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          this.running++;
          resolve(await task());
        } catch (e) {
          reject(e);
        } finally {
          this.running--;
          this.processQueue();
        }
      });
      this.processQueue();
    });
  }

  private processQueue() {
    while (this.running < this.maxConcurrent && this.queue.length) {
      this.queue.shift()!();
    }
  }
}
```

**Q41: Implement a reactive state management system.**

A: Use Proxy for reactivity, track dependencies, notify subscribers on changes.

**Q42: Design a custom React hook for data fetching.**

A: Use useState, useEffect, and AbortController. Handle loading, error, and data states.

**Q43: Implement a pub/sub system with wildcard support.**

A: Use Map for subscriptions, implement pattern matching for wildcards.

**Q44: Design a rate limiter.**

A: Use sliding window or token bucket algorithm. Track request timestamps per user.

**Q45: Implement a dependency injection container.**

A: Use Map for registrations, resolve dependencies recursively, handle circular dependencies.

### Follow-up Questions (5 Questions)

**Q46: How would you optimize a React application that's re-rendering too much?**

A:
1. Use React.memo for pure components
2. Memoize expensive computations with useMemo
3. Memoize callbacks with useCallback
4. Avoid inline objects/functions in JSX
5. Use React DevTools Profiler to identify issues
6. Implement code splitting with React.lazy
7. Use virtualization for long lists

**Q47: Explain how you would debug a memory leak in a production application.**

A:
1. Monitor memory usage over time
2. Take heap snapshots in Chrome DevTools
3. Compare snapshots to find growing objects
4. Check for detached DOM elements
5. Verify event listener cleanup
6. Review closure captures
7. Use performance.memory API
8. Implement memory monitoring alerts

**Q48: How would you implement optimistic UI updates?**

A: Update UI immediately, make API call, rollback on failure. Use local state for immediate feedback, sync with server state.

**Q49: Design a caching strategy for a web application.**

A:
1. Browser cache with appropriate headers
2. Service worker for offline support
3. Client-side cache with TTL
4. Server-side cache (Redis)
5. CDN for static assets
6. Cache invalidation strategy

**Q50: How would you handle authentication in a single-page application?**

A:
1. JWT tokens stored in httpOnly cookies
2. Refresh token rotation
3. Secure token storage
4. CSRF protection
5. Session management
6. Automatic logout on inactivity
7. Multi-factor authentication

## Summary

This comprehensive guide covers 50 essential JavaScript interview questions across all difficulty levels:

1. **Beginner**: Core concepts, data types, basic syntax
2. **Intermediate**: Advanced features, patterns, frameworks
3. **Senior**: Architecture, performance, internals
4. **FAANG-style**: System design, implementation, optimization
5. **Follow-ups**: Real-world scenarios, debugging, best practices

Understanding these topics thoroughly will help you ace any JavaScript interview.

## Quick Reference

```
JAVASCRIPT INTERVIEW QUICK REFERENCE
═══════════════════════════════════════════════════════════════

CORE CONCEPTS:
• Execution Context & Scope Chain
• Closures & Lexical Scoping
• Prototypal Inheritance
• Event Loop & Async/Await
• Promises & Generators

ADVANCED TOPICS:
• Memory Management & GC
• Module Systems
• Performance Optimization
• Design Patterns
• System Design

COMMON PATTERNS:
• Debounce/Throttle
• Memoization
• Currying
• Composition
• Factory Pattern

REACT SPECIFIC:
• Hooks (useState, useEffect, useMemo, useCallback)
• Performance Optimization
• State Management
• Component Patterns

DEBUGGING:
• Chrome DevTools
• Memory Profiling
• Performance Monitoring
• Error Tracking

BEST PRACTICES:
• TypeScript for type safety
• ESLint for code quality
• Testing (Jest, React Testing Library)
• Code Review
• Documentation
```

## References & Learn More

- [InterviewBit: JavaScript Interview Questions](https://www.interviewbit.com/javascript-interview-questions/)
- [JS The Right Way](https://www.jstherightway.org/)
- [33 JavaScript Concepts Every Developer Should Know](https://github.com/leonardomso/33-js-concepts)
- [Eloquent JavaScript](https://eloquentjavascript.net/)
- [You Don't Know JS (YDKJS)](https://github.com/getify/You-Dont-Know-JS)
