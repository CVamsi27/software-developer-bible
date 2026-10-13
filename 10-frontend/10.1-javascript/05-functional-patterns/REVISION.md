<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-6_min-informational)](#)
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
   **A:** Within a loader, one resolved identity normally shares an instance. Different realms/URLs/bundled copies can differ. Shared config/client state may fit; per-request mutable session state needs a separate owner.

**How It Works**

4. **Q:** Put the ESM loading pipeline in order.
   **A:** Discover dependencies while parsing/loading, resolve identities, obtain their source, link bindings, then evaluate the graph with cycle/await rules. Fetching can overlap, and evaluation sharing is per resolved identity/loader rather than universally once.

5. **Q:** What can CommonJS `require()` do that a static `import` cannot, and what is ESM's escape hatch?
   **A:** `require()` builds its argument at runtime, so it can run conditionally or on a computed path; ESM imports are hoisted and resolved before any code runs — for conditional loading you `await import()`, which yields a promise for the module namespace.

**Common Mistakes**

6. **Q:** When a circular dependency bites, do you get `undefined` or an error?
   **A:** It depends on the system: CommonJS hands back a partially initialized exported value (some missing properties can produce undefined or a warning), while reading an uninitialized ESM live binding throws a ReferenceError (TDZ).

7. **Q:** Why can `import { foo } from './utils'` fail in Node ESM yet work in a bundler?
   **A:** Node's ESM resolver requires the full path with an extension and does no directory/index guessing; bundlers apply their own `resolve.extensions` config — so dual-target code needs a deliberate strategy (`exports` map, or always ship explicit paths).

**Performance Considerations**

8. **Q:** What must a module provide before a bundler can tree-shake its exports away?
   **A:** The build must prove removal preserves behavior. Static named usage often helps; a statically accessed namespace can also be analyzed, and default-object property elimination varies. Package sideEffects metadata controls module-level removal in tools such as webpack; incorrect metadata can delete required initialization.

## Memoization

Source: [Memoization](10.1.5.02-memoization.md)

**First Principles**

1. **Q:** Why can a TTL cache still retain unbounded memory?
   **A:** A TTL controls how long an entry may be reused, but a cold expired entry remains stored if expiry is checked only on reads. Add a capacity, a cleanup pass, or a shorter-lived owner to bound retention.

2. **Q:** What breaks when a function reads module-level state you forgot to declare impure?
   **A:** The first call's answer is cached as if it were a function of its arguments alone, so every later hit returns a value computed under the old state — memoization cannot detect the hidden input; it just freezes whatever the first call observed.

**How It Works**

3. **Q:** What must happen on a cache hit, and what must the key preserve?
   **A:** The wrapper derives the same domain key, finds it in the cache, and returns the stored value without invoking the function. That is correct only when equivalent keys represent calls with interchangeable results and hidden dependencies are handled.

**Code Examples**

4. **Q:** What repeated work does the Fibonacci cache eliminate?
   **A:** It stores each computed input once, so later overlapping branches reuse that result instead of recursively recalculating it. For one input the example computes O(n) states and retains O(n) results; a larger result may still exceed Number precision or stack depth.

**Common Mistakes**

5. **Q:** Object-identity keying vs structural keying — when is each the right choice?
   **A:** Identity keying fits a stable immutable instance; mutating it can make a cached result stale. Structural keying requires a defined equivalence rule, such as the complete tenant/query/page tuple in the chapter. JSON serialization is not universal: it can reorder distinctions, discard values or throw.

6. **Q:** What goes wrong if an async function's rejected promise gets cached?
   **A:** The rejection is stored like any value, so every caller inside the TTL is served the same failure without a retry — a retryable-failure policy removes only the matching cached promise while preserving rejection for callers. A negative-cache policy may instead deliberately retain a classified failure for a bounded time.

**Real-World Use Cases**

7. **Q:** Why can omitting a reactive value from `useMemo` dependencies return a stale result?
   **A:** React reuses the prior value when listed dependencies compare equal. If the calculation also reads an omitted value, that value can change without invalidating the cache; include every reactive value used by the calculation.

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

4. **Q:** In `askName`, what does `iterator.next("Sam")` deliver, and where does the string end up?
   **A:** The argument becomes the completion value of the `yield` expression the generator is parked on, so it is assigned to `name` — data sent in arrives on the far side of the pause, not as a return value.

5. **Q:** Why does the paged-fetch example need `async function*` plus `for await`?
   **A:** `await` inside a plain `function*` is a SyntaxError, and every `next()` of an async generator returns a promise — `for await` pulls one chunk at a time and awaits each step for you.

**Common Mistakes**

6. **Q:** What does the iterator return after a generator has completed?
   **A:** Later `next()` calls keep reporting `done: true`; the generator does not restart. A `finally` block that yields is a special completion path because its yielded value must be pulled before the return completes.

**Best Practices**

7. **Q:** Why prefer `for...of` over a manual `while (!done)` loop when both can print the same values?
   **A:** A body break/return/throw invokes an available iterator return. Producer next failures differ, and a yielding finally may require more pulls, so mandatory cleanup must not depend on that pattern. A manual loop needs its own owned close on early exit.

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

5. **Q:** Why is `Function.length` an unreliable default arity for a generic curry helper?
   **A:** `Function.length` excludes parameters after the first default and excludes rest parameters. A helper can therefore run before the intended arguments arrive; use explicit arity or a documented helper contract.

**Real-World Case Studies**

6. **Q:** In `requireRole('admin')`, what is fixed at setup and what does Express supply later?
   **A:** The factory captures the required role once. Express later calls the returned handler with `(req, res, next)` for each request; this is a multi-argument middleware protocol, not a unary composition pipeline.

**Common Mistakes**

7. **Q:** Why does `pipe(validate(userSchema), authorize('admin'), handler)` break as an Express chain?
   **A:** `pipe` passes each function's return value in as the next function's argument, so the first handler gets `req` alone, `next` arrives as `undefined`, and the call dies with `TypeError: next is not a function` — Express hands every middleware the same `(req, res, next)` and chains them through `next()` instead.

8. **Q:** When does point-free or curried style start hurting instead of helping?
   **A:** When there is nothing to reuse. Currying a one-off call only adds a closure layer per argument; the payoff appears when the intermediate function is genuinely reused — pre-bound loggers, per-role guards, configured clients.

## Recursion and Tail Calls

Source: [Recursion and Tail Calls](10.1.5.05-recursion-tail-call.md)

**Definition**

1. **Q:** What two parts does every recursive solution have to contain, and what does each one do?
   **A:** A base case — the smallest input answered without recursing — and a recursive case that calls the function on a smaller input. The base case must be reachable from every valid input, or the calls never stop and the stack grows until `RangeError`.

**How It Works**

2. **Q:** Why does `return n * factorial(n - 1)` keep the current frame alive while `return factorial(n - 1, n * acc)` can drop it?
   **A:** In the first form the multiplication still has to run *after* the inner call returns, so the frame's locals must survive; in the second nothing is left to do, so the engine is free to reuse the frame instead of allocating a new one.

3. **Q:** What does an explicit work stack change for an unbounded tree walk, and what does it not remove?
   **A:** It stores pending nodes in application-managed memory instead of nested JavaScript call frames, allowing a depth or size limit and avoiding call-stack overflow. It still retains queued nodes and must define cycle handling; moving work off the call stack does not make it free.

**Code Examples**

4. **Q:** What does memoization improve for recursive Fibonacci, and which limit remains?
   **A:** It reuses overlapping subproblems so one call computes each smaller state once instead of recomputing branches. It reduces repeated work, not recursion depth or Number precision limits; use iteration when depth is unbounded.

**Real-World Case Studies**

5. **Q:** Why does a graph traversal need more than the tree's recursive base case?
   **A:** A graph can contain cycles or shared nodes, so traversal needs an identity policy such as a visited set. For input-controlled depth, an explicit stack also avoids relying on the engine's call-stack limit.

**Common Mistakes**

6. **Q:** What breaks when you forget `return` in front of the recursive call?
   **A:** When a function should return the child’s result but simply calls it and falls through, the caller receives undefined. Side-effect-only traversals can correctly omit return; the intended result contract decides.

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

**Q:** A consumer breaks from an async-generator page loop while a fetch is in progress. What stops, and what may continue?
**A:** Iterator closure prevents future page steps and awaits the generator's close path. It does not cancel an already pending fetch unless the owner also aborts the request through its signal.

**Q:** How does adding a default parameter change a curry helper that relies on fn.length?
**A:** Function.length stops counting at the first default, so the helper may execute before all intended arguments arrive. An explicit completion arity states the intended grouping.

**Q:** Why can replacing recursion with a work stack avoid stack overflow without reducing total work?
**A:** It moves pending calls into an explicit data structure and still visits each required node. Memory and CPU costs remain proportional to the traversal; cycle handling and a maximum-work policy are still needed.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
