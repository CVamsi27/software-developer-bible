<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-7_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Functional Patterns — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Modules

Source: [Modules](10.1.5.01-modules.md)

**Definition**

1. **Q:** What three properties separate a module from "a script in a wrapper"?
   **A:** A separately scoped unit, an explicit public surface and dependencies resolved by a host/toolchain. Unexported names are not directly addressable from imports. State is normally shared for one resolved identity within a loader; different URLs/realms/bundled copies can create separate instances.

**First Principles**

2. **Q:** Why does ESM insist that dependencies be static, and what does that buy?
   **A:** Static imports let tools discover dependency edges before evaluating bodies, while the host still resolves specifiers. Dynamic import supports computed/conditional loading. Removing unused code requires side-effect and usage analysis plus build configuration; static syntax alone is insufficient.

3. **Q:** Why is module top-level state a singleton, and when is that a hazard?
   **A:** The module map caches one instance per URL, so every importer shares the same bindings — ideal for config or a shared client, a trap the moment you wanted a fresh copy per importer.

**How It Works**

4. **Q:** Put the ESM loading pipeline in order.
   **A:** Parse the entry graph → resolve specifiers to URLs → fetch → parse each module → link imports to exports → evaluate in dependency order; evaluation happens once per module no matter how many importers it has.

5. **Q:** What can CommonJS `require()` do that a static `import` cannot, and what is ESM's escape hatch?
   **A:** `require()` builds its argument at runtime, so it can run conditionally or on a computed path; ESM imports are hoisted and resolved before any code runs — for conditional loading you `await import()`, which yields a promise for the module namespace.

**Common Mistakes**

6. **Q:** When a circular dependency bites, do you get `undefined` or an error?
   **A:** It depends on the system: CommonJS hands back a partially-filled `exports` object (`undefined` for anything not assigned yet, plus Node's circular-dependency warning), while reading an uninitialized ESM live binding throws a ReferenceError (TDZ).

7. **Q:** Why can `import { foo } from './utils'` fail in Node ESM yet work in a bundler?
   **A:** Node's ESM resolver requires the full path with an extension and does no directory/index guessing; bundlers apply their own `resolve.extensions` config — so dual-target code needs a deliberate strategy (`exports` map, or always ship explicit paths).

**Performance Considerations**

8. **Q:** What must a module provide before a bundler can tree-shake its exports away?
   **A:** The build must prove removal preserves behavior. Static named usage often helps; a statically accessed namespace can also be analyzed, and default-object property elimination varies. Package sideEffects metadata controls module-level removal in tools such as webpack; incorrect metadata can delete required initialization.

## Memoization

Source: [Memoization](10.1.5.02-memoization.md)

**First Principles**

1. **Q:** Why does an unbounded cache count as a leak rather than a slow-down?
   **A:** High-cardinality inputs can retain results long after they are useful. Capacity eviction bounds entries; TTL bounds reuse freshness only if expired entries are actually removed. The chapter lazy TTL wrapper still needs capacity, sweeping or a lifetime boundary.

2. **Q:** What breaks when a function reads module-level state you forgot to declare impure?
   **A:** The first call's answer is cached as if it were a function of its arguments alone, so every later hit returns a value computed under the old state — memoization cannot detect the hidden input; it just freezes whatever the first call observed.

**How It Works**

3. **Q:** Walk the second-call path of `memoize(fn)` when the arguments repeat.
   **A:** The wrapper stringifies the arguments into a key, finds it in the cache Map, and returns the stored value without ever invoking `fn` — the body does not run, which is the whole point and also why side effects would be silently skipped.

**Code Examples**

4. **Q:** What actually differs between `fibonacci` and `fibonacciMemo`?
   **A:** The naive version repeats the same subproblems along every branch — O(2^n) calls for fib(n) — while the memoized one computes each n once, O(n) states at O(1) lookup each; the manual version threads the cache as a parameter, the `memoize(fib)` version keeps it in closure state.

**Common Mistakes**

5. **Q:** Object-identity keying vs structural keying — when is each the right choice?
   **A:** Identity keying fits a stable immutable instance; mutating it can make a cached result stale. Structural keying requires a defined equivalence rule, such as the complete tenant/query/page tuple in the chapter. JSON serialization is not universal: it can reorder distinctions, discard values or throw.

6. **Q:** What goes wrong if an async function's rejected promise gets cached?
   **A:** The rejection is stored like any value, so every caller inside the TTL is served the same failure without a retry — production wrappers evict on `.catch` so the next call re-hits the network.

**Real-World Use Cases**

7. **Q:** In the `ProductList` example, why is the `useMemo` dependency list a correctness concern and not just an optimization knob?
   **A:** The memoized filter only recomputes when a listed dep changes — drop `category` from the deps and the component renders last category's products while looking perfectly healthy; a stale render reads as a data bug, not a cache bug.

**Performance Considerations**

8. **Q:** How do you tell whether a memoization actually paid off?
   **A:** Time both paths on real inputs and watch the hit-rate stats: a low ratio means you are paying Map lookups and permanent memory for mostly-missing keys, so either raise input reuse or remove the memoization.

## Generators

Source: [Generators](10.1.5.03-generators.md)

**First Principles**

1. **Q:** Why can a generator remember local variables between values while an ordinary function cannot?
   **A:** `yield` pauses the generator without finishing it. The generator object keeps the state needed for the next `next()` call to continue. An ordinary synchronous function returns or throws instead of pausing at an intermediate value. This is a behavioral rule, not a required physical frame layout.

**How It Works**

2. **Q:** What does calling `myGen()` actually execute, and what comes back?
   **A:** Nothing in the body runs — the call only builds a generator object that implements the iterator protocol. Statements execute up to the next `yield` on each `next()` call, one segment per request.

3. **Q:** How do `return(v)` and `throw(e)` differ in their effect on a suspended generator?
   **A:** return(v) injects completion through finally, which can itself yield before done becomes true. throw(e) raises e at the suspended yield, where catch can handle it and yield again. Calling return before the body starts does not execute its finally cleanup.

**Code Examples**

4. **Q:** In `inputProcessor`, what does `gen.next("Alice")` deliver, and where does the string end up?
   **A:** The argument becomes the completion value of the `yield` expression the generator is parked on, so it is assigned to `name` — data sent in arrives on the far side of the pause, not as a return value.

5. **Q:** Why does the paged-fetch example need `async function*` plus `for await`?
   **A:** `await` inside a plain `function*` is a SyntaxError, and every `next()` of an async generator returns a promise — `for await` pulls one chunk at a time and awaits each step for you.

**Common Mistakes**

6. **Q:** Why is the `yield 3` after `return 2` unreachable, and what does that say about the generator's completion?
   **A:** For the example yielding 1 then returning 2, the second next reports value:2/done:true; a later next reports undefined/done:true. The following yield 3 is unreachable. A yielding finally block would be a distinct completion path.

**Best Practices**

7. **Q:** Why prefer `for...of` over a manual `while (!done)` loop when both can print the same values?
   **A:** `for...of` closes the iterator when the loop exits early — it calls the generator's `return()`, so `finally` blocks inside run. A manual loop that simply stops calling `next()` leaves the generator suspended with its cleanup never executed.

**Performance Considerations**

8. **Q:** What does lazy evaluation change about space, and what does it leave alone?
   **A:** Producing values on demand can avoid storing a whole output array. Space still depends on the generator's retained local state and the consumer's buffers, so not every generator uses O(1) memory. The work needed to calculate each requested value remains.

## Currying & Function Composition

Source: [Currying & Function Composition](10.1.5.04-currying-composition.md)

**Definition**

1. **Q:** What separates currying from partial application?
   **A:** Currying always returns a chain of unary functions — one argument per call until the result falls out — while partial application fixes however many arguments you have now and hands back a function of the rest, which may take them all at once.

2. **Q:** Where does `Function.prototype.bind` sit relative to `curry()`?
   **A:** `bind` is the built-in partial application: it fixes `this` plus the leading arguments in one shot and lets the result take any remaining grouping. It neither splits the remainder into one-argument steps nor looks at the original arity — that chain-building is what a `curry()` helper adds.

**How It Works**

3. **Q:** What does each level of `curriedAdd(1)(2)(3)` hold onto?
   **A:** Each nested function closes over the arguments collected so far — the first over `1`, the second over `1` and `2` — so the chain works by ordinary closure state, with no shared mutable variables anywhere.

4. **Q:** In what order does `compose(f, g, h)(x)` run its functions, and which helper reads the other way?
   **A:** Right to left: `f(g(h(x)))`, because it reduces from the end with `reduceRight`. `pipe` uses `reduce` and runs left to right, matching the direction the data actually flows.

**Code Examples**

5. **Q:** Why does the generic `curry()` check `args.length >= fn.length` instead of demanding one argument per call?
   **A:** Grouped arguments are accepted as a convenience beyond unary currying. The helper now compares against an explicit arity whose default is fn.length. Defaults and rest parameters make that default incomplete; pass the intended arity when needed.

**Real-World Case Studies**

6. **Q:** What is each level of a Redux middleware `(store) => (next) => (action) => …` responsible for fixing?
   **A:** A different lifecycle moment: `store` once when the chain is built, `next` once per middleware wiring, `action` on every dispatch — currying used as staged dependency injection rather than as style.

**Common Mistakes**

7. **Q:** Why does `pipe(validate(userSchema), authorize('admin'), handler)` break as an Express chain?
   **A:** `pipe` passes each function's return value in as the next function's argument, so the first handler gets `req` alone, `next` arrives as `undefined`, and the call dies with `TypeError: next is not a function` — Express hands every middleware the same `(req, res, next)` and chains them through `next()` instead.

8. **Q:** When does point-free or curried style start hurting instead of helping?
   **A:** When there is nothing to reuse. Currying a one-off call only adds a closure layer per argument; the payoff appears when the intermediate function is genuinely reused — pre-bound loggers, per-role guards, configured clients.

## Recursion & Tail Call Optimization

Source: [Recursion & Tail Call Optimization](10.1.5.05-recursion-tail-call.md)

**Definition**

1. **Q:** What two parts does every recursive solution have to contain, and what does each one do?
   **A:** A base case — the smallest input answered without recursing — and a recursive case that calls the function on a smaller input. The base case must be reachable from every valid input, or the calls never stop and the stack grows until `RangeError`.

**How It Works**

2. **Q:** Why does `return n * factorial(n - 1)` keep the current frame alive while `return factorial(n - 1, n * acc)` can drop it?
   **A:** In the first form the multiplication still has to run *after* the inner call returns, so the frame's locals must survive; in the second nothing is left to do, so the engine is free to reuse the frame instead of allocating a new one.

3. **Q:** What is the trampoline loop actually executing in `safeFactorial`, and what does it buy you?
   **A:** Each step returns a function for the next step instead of making a nested recursive call. The loop `while (typeof r === 'function') r = r()` runs those steps iteratively. This avoids growing the call stack, but time and memory remain limited. Numeric range is separate: `100000!` still overflows Number to `Infinity`.

**Code Examples**

4. **Q:** Why is naive `fibonacci(100)` hopeless while the memoized one returns instantly?
   **A:** Repeated overlapping subproblems cause exponential growth in the naive version; memoization computes each bounded integer state once. There is no universal cutoff where execution never finishes. Number precision and recursion depth remain separate limits even when repeated work is removed.

**Real-World Case Studies**

5. **Q:** Why does the recursive tree-view component fit recursion so well, and where does it bite back?
   **A:** Child component elements mirror the tree shape, but creating JSX does not directly invoke the child component recursively in the current parent frame. Deep/large trees still impose rendering work and memory costs; cyclic graph data must be rejected or handled with a traversal policy.

**Common Mistakes**

6. **Q:** What breaks when you forget `return` in front of the recursive call?
   **A:** The function still recurses, but its own result is discarded and it evaluates to `undefined`, so callers downstream get `undefined` where they expected a number or structure — silent until something consumes it.

**Best Practices**

7. **Q:** At what point should you stop trusting recursion and convert to iteration?
   **A:** When valid input can exceed the depth you have tested and bounded for the deployed runtime. The safe depth depends on the engine and call shape; there is no universal ten-thousand-call budget. Use a loop or explicit stack when input depth is unbounded.

**Performance & TCO Support**

8. **Q:** ECMAScript mandates proper tail calls, so why can't production code rely on them?
   **A:** Qualifying strict-mode tail positions have specified behavior, and WebKit documents its implementation. Support is not portable across deployed engines/configurations; tail-recursive syntax alone cannot establish a safe depth budget. Use a loop, explicit stack or trampoline when the application must handle unbounded depth.

## Changed conditions

Sources: [Modules](10.1.5.01-modules.md), [Memoization](10.1.5.02-memoization.md), [Generators](10.1.5.03-generators.md), [Currying](10.1.5.04-currying-composition.md), [Recursion](10.1.5.05-recursion-tail-call.md).

**Q:** Why can a two-module cycle work until one module reads an imported const during initialization?
**A:** Linking connects the bindings before evaluation, but the exporting const still needs initialization. The early read can hit its uninitialized state; the cycle alone is not the failure.

**Q:** What happens if undefined is a legitimate computed result and a memoizer treats undefined as a miss?
**A:** It recomputes on every call. Check key membership separately from the value, as in the bounded wrapper.

**Q:** A yielded promise rejects, then the generator catch yields a fallback promise. What must its driver do?
**A:** Resume with throw(error), inspect that step's IteratorResult, await the newly yielded promise and resume again. Calling throw without processing its result can leave the outer promise pending.

**Q:** How does adding a default parameter change a curry helper that relies on fn.length?
**A:** Function.length stops counting at the first default, so the helper may execute before all intended arguments arrive. An explicit completion arity states the intended grouping.

**Q:** Why can a trampoline avoid stack overflow yet freeze a page or return Infinity?
**A:** It executes steps in one synchronous loop, so it does not yield to input. It also changes call depth rather than Number range or total arithmetic work.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
