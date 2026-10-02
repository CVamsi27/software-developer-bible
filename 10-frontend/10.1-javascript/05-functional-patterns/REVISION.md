<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-6_min-informational)](#)

# Functional Patterns — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Modules

Source: [Modules](10.1.5.01-modules.md)

**Definition**

1. **Q:** What three properties separate a module from "a script in a wrapper"?
   **A:** A top-level scope nothing outside can reach, an explicit export list as the only way through that wall, and one cached instance per URL — so importing the same module twice still runs it once.

**First Principles**

2. **Q:** Why does ESM insist that dependencies be static, and what does that buy?
   **A:** `import` specifiers are fixed at parse time, so tools can build the full graph, detect cycles, and drop unused exports without executing anything — analyzability is the feature, not the syntax.

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
   **A:** Static, side-effect-free named exports the bundler can prove are unused (ideally with `sideEffects: false` in `package.json`) — a namespace import or a default-exported object keeps every member reachable.

## Memoization

Source: [Memoization](10.1.5.02-memoization.md)

**First Principles**

1. **Q:** Why does an unbounded cache count as a leak rather than a slow-down?
   **A:** The map only grows — every new argument tuple is retained forever, so a hot path over high-cardinality inputs (user ids, raw query strings) pins memory for entries that are rarely read again; the fix is a bound (LRU) or an expiry (TTL).

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
   **A:** A Map keyed by the object itself is right when the contract is "same instance → same answer" (per-request contexts, repeated parses of one literal); structural keying is right when equal-by-value arguments must share an entry — and then the stringification has to be key-order-insensitive or `{a,b}` and `{b,a}` miss each other.

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
   **A:** A normal function's frame is destroyed when it returns, but a generator's frame is suspended at the `yield` instead of popped — the engine keeps it allocated, so the next `next()` resumes with the same locals still in place.

**How It Works**

2. **Q:** What does calling `myGen()` actually execute, and what comes back?
   **A:** Nothing in the body runs — the call only builds a generator object that implements the iterator protocol. Statements execute up to the next `yield` on each `next()` call, one segment per request.

3. **Q:** How do `return(v)` and `throw(e)` differ in their effect on a suspended generator?
   **A:** `return(v)` completes it, producing `{ value: v, done: true }`; `throw(e)` re-raises `e` *at the suspended yield expression*, where the generator's own `try/catch` can handle it and resume.

**Code Examples**

4. **Q:** In `inputProcessor`, what does `gen.next("Alice")` deliver, and where does the string end up?
   **A:** The argument becomes the completion value of the `yield` expression the generator is parked on, so it is assigned to `name` — data sent in arrives on the far side of the pause, not as a return value.

5. **Q:** Why does the paged-fetch example need `async function*` plus `for await`?
   **A:** `await` inside a plain `function*` is a SyntaxError, and every `next()` of an async generator returns a promise — `for await` pulls one chunk at a time and awaits each step for you.

**Common Mistakes**

6. **Q:** Why is the `yield 3` after `return 2` unreachable, and what does that say about the generator's completion?
   **A:** `return` finishes the generator immediately; only `yield` suspends it, so anything after `return` is dead code and the third `next()` call simply reports `{ value: 2, done: true }`.

**Best Practices**

7. **Q:** Why prefer `for...of` over a manual `while (!done)` loop when both can print the same values?
   **A:** `for...of` closes the iterator when the loop exits early — it calls the generator's `return()`, so `finally` blocks inside run. A manual loop that simply stops calling `next()` leaves the generator suspended with its cleanup never executed.

**Performance Considerations**

8. **Q:** What does lazy evaluation change about space, and what does it leave alone?
   **A:** A generator holds only its one live frame instead of materializing the whole sequence — O(1) space where an array of the same values costs O(n) — but the time to produce each value is exactly what it always was.

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
   **A:** So callers can group arguments freely — `curried(1)(2, 3)`, `curried(1, 2)(3)`, and `curried(1, 2, 3)` all hit the same path — and the original function fires as soon as enough arguments have accumulated to satisfy its declared arity.

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
   **A:** The thunk form never calls itself — it returns `() => factorialThunk(...)`, so `while (typeof r === 'function') r = r()` converts 100,000 nested calls into 100,000 iterations inside a single frame. You get unlimited depth; magnitude is a separate problem, since `100000!` still comes back as `Infinity`.

**Code Examples**

4. **Q:** Why is naive `fibonacci(100)` hopeless while the memoized one returns instantly?
   **A:** The naive version recomputes overlapping subtrees — O(2^n) calls, and past ~n=40 it never finishes — while `memoize` turns each distinct `n` into a single cached call, collapsing the work to a chain of n entries.

**Real-World Case Studies**

5. **Q:** Why does the recursive tree-view component fit recursion so well, and where does it bite back?
   **A:** Nested `TreeNode`s mirror the data's own definition — the code *is* the shape — but depth equals data depth, so an unexpectedly deep or cycle-containing structure overflows the stack the same way any other unguarded recursion would.

**Common Mistakes**

6. **Q:** What breaks when you forget `return` in front of the recursive call?
   **A:** The function still recurses, but its own result is discarded and it evaluates to `undefined`, so callers downstream get `undefined` where they expected a number or structure — silent until something consumes it.

**Best Practices**

7. **Q:** At what point should you stop trusting recursion and convert to iteration?
   **A:** Once input depth can reach the order of ten thousand frames — engines only admit that many simple frames, and the exact ceiling moves with frame size and engine version — so any structure that big deserves an explicit stack or a plain loop.

**Performance & TCO Support**

8. **Q:** ECMAScript mandates proper tail calls, so why can't production code rely on them?
   **A:** Only JavaScriptCore (Safari) implements them; V8 removed its version in 2017 and SpiderMonkey dropped theirs, so on Chrome, Node, and Firefox a "tail-recursive" function still allocates a frame per call and dies with `RangeError` at ordinary recursion depths.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
