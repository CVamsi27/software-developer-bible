<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-6_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Async & Concurrency — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Event Loop

Source: [Event Loop](10.1.3.01-event-loop.md)

**Definition**

1. **Q:** In one sentence, what job does the event loop do?
   **A:** It selects host work and runs JavaScript with the relevant checkpoints. Browser loops process microtasks and coordinate rendering opportunities; Node has different host phases.

**How It Works**

2. **Q:** Why do promise continuations get a separate queue instead of waiting alongside timers?
   **A:** Queued reactions run at microtask checkpoints after settlement. The checkpoint drains newly added microtasks too, which can starve later tasks and rendering; an unresolved promise has no reaction ready to run.

3. **Q:** Where does Node's `process.nextTick` sit relative to those queues?
   **A:** At common CommonJS callback boundaries, Node drains next-tick work before promise microtasks. Module evaluation and already-running microtasks require their own ordering analysis; nextTick does not universally preempt them.

**Code Examples**

4. **Q:** A snippet logs synchronously, then schedules `setTimeout(fn, 0)` and a `.then`; what order do the three print in?
   **A:** The synchronous lines, then the microtask, then the timer — the stack empties, microtasks drain to exhaustion, and only then does the loop take one task off the timer queue.

5. **Q:** Why does code after `await Promise.resolve()` start running after the caller's remaining synchronous code?
   **A:** `await` hands a pending promise back to the caller and parks the rest of the function as a reaction, so the caller finishes on this stack and the continuation arrives in a later microtask drain.

**Common Mistakes**

6. **Q:** Why is `setTimeout(fn, 0)` never equivalent to calling `fn()` on the next line?
   **A:** It enqueues a task, and a task cannot start until the stack is empty *and* every microtask queued in the meantime has already run.

**Performance Considerations**

7. **Q:** What stops running while a synchronous loop occupies the stack for two seconds?
   **A:** That agent cannot run other callbacks while the synchronous work occupies it. Main-thread input handling and rendering work can be delayed; independent workers and eligible compositor work may still progress.

**Best Practices**

8. **Q:** Can a microtask guarantee that a DOM write appears in the next paint?
   **A:** No. Microtasks run before an eligible rendering update, but a rendering opportunity is not guaranteed after every task. Use `requestAnimationFrame` to coordinate visual changes with rendering; its callback still cannot force a paint or guarantee a deadline.

## Promises

Source: [Promises](10.1.3.02-promises.md)

**Definition**

1. **Q:** What is a promise, as a piece of state rather than as syntax?
   **A:** An object that starts `pending` and transitions exactly once to either a fulfilled value or a rejection reason, and then never changes — everything else is plumbing around that ratchet.

**How It Works**

2. **Q:** What happens when a `.then` callback returns a plain value instead of a promise?
   **A:** The link resolves immediately with that value, so the next `.then` receives it directly; return a promise and the chain adopts its eventual outcome instead.

3. **Q:** Why can a `.then` attached to an already-settled promise still fire?
   **A:** Settlement stores the outcome, and reactions attach to the stored result — late handlers take the same path as early ones, so "already done" needs no special case.

**Code Examples**

4. **Q:** What does `Promise.any` return when its first input rejects but a later one fulfils?
   **A:** It resolves with the first fulfillment, ignoring earlier rejections, and only rejects with an `AggregateError` once every input has rejected.

5. **Q:** How do `Promise.all` and `Promise.allSettled` differ in their reaction to one failure?
   **A:** `all` rejects when an input rejection is observed; other operations continue unless separately cancelled. `allSettled` waits for every input and returns one outcome record per input, in input order.

**Common Mistakes**

6. **Q:** Why does `new Promise(resolve => fetch(url).then(resolve))` usually make things worse?
   **A:** It re-implements adoption for no gain and adds a second place where errors can be dropped, so returning the inner promise directly is strictly simpler.

7. **Q:** What actually happens to a rejected promise nobody attached a handler to?
   **A:** The host reports an unhandled rejection. Browser `unhandledrejection` and Node behavior depend on host policy, installed handlers and Node's flags; do not rely on one universal warning or termination outcome.

**Performance Considerations**

8. **Q:** Three independent requests are awaited in sequence; what does that cost you, and what replaces it?
   **A:** If each request is called only after the previous await, their waits accumulate. Call independent operations first, then combine their promises with `Promise.all`; the calls start work, while the combinator observes outcomes. Already-started promises can overlap even when awaited in sequence.

## Async/Await

Source: [Async/Await](10.1.3.03-async-await.md)

**Definition**

1. **Q:** What does the `async` keyword do to a function's return value?
   **A:** It forces it into a promise — `return x` hands back a promise of `x`, and `throw` becomes a rejection — so callers can treat async and promise-returning functions identically.

**How It Works**

2. **Q:** What actually happens to the thread at an `await`?
   **A:** Nothing blocks: the function is split at that point, the caller gets control back immediately, and the remainder is scheduled as a microtask for when the awaited promise settles.

3. **Q:** Why does awaiting a non-promise still change timing?
   **A:** The value is adopted through the same machinery, so continuation is deferred by one microtask turn — code after the `await` never runs in the same synchronous pass as code before it.

**Code Examples**

4. **Q:** Why does `await Promise.all([fetchA(), fetchB()])` run the two fetches together when it reads as a single line?
   **A:** The array literal is evaluated first, so both calls start and both requests are already in flight by the time anything is awaited.

5. **Q:** What does `for await (… of gen())` take care of for you?
   **A:** It drives resumption of the async iterator, calls the generator's cleanup on `break` or `return`, and propagates rejections — all of which a hand-rolled `next()` loop would have to do itself.

**Common Mistakes**

6. **Q:** A loop awaits 100 independent requests; what does that cost, and what is the fix?
   **A:** Calling and awaiting one request at a time prevents overlap. Schedule independent work with an explicit concurrency budget so connection limits, upstream quotas and memory stay controlled. An unbounded `Promise.all` is appropriate only when that workload is safe to start together.

**Performance Considerations**

7. **Q:** When is a sequential chain of awaits the *right* choice?
   **A:** When each step consumes the previous step's output — the order is then the data dependency itself, and no amount of parallelism can remove it.

**Best Practices**

8. **Q:** What does an explicit `Promise<T>` return type check, and what does it fail to detect?
   **A:** It checks the eventual fulfilled value against `T`. Returning another `Promise<T>` is valid because async return adopts it, so this signature does not detect every missing await. Await inside a local try/catch when that catch must handle the eventual rejection.

## Error Handling

Source: [Error Handling](10.1.3.04-error-handling.md)

**Definition**

1. **Q:** What does JavaScript guarantee when something throws?
   **A:** Control transfers to the nearest enclosing `try`, every frame between the throw site and that handler is popped on the way, and any `finally` blocks still run during the unwind.

**How It Works**

2. **Q:** Why can't a `try` wrapped around `fetch(url)` catch the network failure that happens afterwards?
   **A:** The failure arrives in a later tick, after the calling frame has already returned — only the promise channel, through `await` or `.catch`, still spans that gap, which is the whole reason rejection travels as a value.

3. **Q:** What are `Promise.all` and `Promise.allSettled` each asserting about many results where some fail?
   **A:** `all` asserts that any failure is *the* answer and rejects at once; `allSettled` asserts that every outcome is data and resolves with one record per input.

**Code Examples**

4. **Q:** What type does `catch (error)` bind under strict TypeScript, and what follows from that?
   **A:** `unknown`, so properties may only be read after narrowing — `instanceof Error`, `'message' in error`, or a `typeof` check — which turns a careless `error.message` into a compile error.

5. **Q:** Why does `Error` have a `cause` option instead of requiring you to splice the original message into the new one?
   **A:** It preserves the original error object with its own stack, so logs keep both the wrapper's context and the true origin rather than a flattened string.

**Common Mistakes**

6. **Q:** What is the actual damage done by `catch (error) {}`?
   **A:** It turns a diagnosable failure into an invisible one: the caller proceeds as if nothing happened, the log stays empty, and any partial writes remain half-applied — log it with context or re-throw.

7. **Q:** Why is `throw 'not found'` a review-blocking habit?
   **A:** A thrown string carries no stack, no `.name`, and nowhere to attach a `code`, so both `instanceof` branching and error reporting break down — throw an `Error` subclass.

**Best Practices**

8. **Q:** Where should a `try/catch` sit, and where is it just noise?
   **A:** At a boundary where you can recover, translate, or return a `Result`; around internal lines it hides the failure without adding a decision, so let the error propagate instead.

## Aborting & Cancellation

Source: [Aborting & Cancellation](10.1.3.05-abort-and-cancellation.md)

**Definition**

1. **Q:** What are the two halves of the cancellation API, and what does each one do?
   **A:** `AbortController` is the broadcaster — it owns `signal` and `abort()` — and `AbortSignal` is what you hand out: an observable flag carrying `aborted`, `reason`, and an `abort` event.

**How It Works**

2. **Q:** What does "cancellation is cooperative" mean for a long `for` loop of your own?
   **A:** The loop must check the signal at safe points. A new abort triggered by another task cannot run while that same agent is blocked in the loop, so long work must also yield to tasks or move to a worker. Awaiting an already-fulfilled promise alone does not let timer or input tasks run.

3. **Q:** Can a controller that has fired ever fire again?
   **A:** No — it is one-shot: `aborted` stays `true` and the stored `reason` never changes, so a second attempt needs a fresh controller.

**Code Examples**

4. **Q:** What distinguishes an `AbortError` rejection from a `TimeoutError` rejection?
   **A:** A no-argument abort uses an `AbortError` DOMException; a timeout signal uses a `TimeoutError` DOMException. `abort(reason)` may carry any custom value, and `AbortSignal.any` adopts the first signal's reason. Read the signal and ownership policy rather than assuming every abort has a particular name.

5. **Q:** Who should own the controller for an operation?
   **A:** The owner that decides when work ends should retain cancellation control and pass a signal downward. A function can create a controller for its own timeout or return a cancel handle; it can also combine its local deadline with a caller signal.

**Common Mistakes**

6. **Q:** What goes wrong with `catch (err) { showError(err.message); }` on a request that carries a signal?
   **A:** It treats every reason as an Error with a message and ignores intent. Suppress obsolete or intentional cancellation according to the owning signal; a timeout may need a visible retry action. Check unknown error values and retain the current-request guard.

7. **Q:** Where should an `abort` listener be registered if the code registering it may itself be torn down?
   **A:** Register before starting work and handle an already-aborted signal. Use `{ once: true }` for the abort path, and explicitly remove the listener after normal completion or owner teardown; once does not clean up a listener when abort never happens.

**Performance Considerations**

8. **Q:** Does calling `controller.abort()` actually stop the server from finishing the request?
   **A:** No. An abort-aware client operation stops its own work according to its API, without guaranteeing a dedicated socket closes or a remote write rolls back. The server may commit; use idempotency, operation status and reconciliation for uncertain outcomes.

## Bounded Concurrency & Promise Pools

Source: [Bounded Concurrency & Promise Pools](10.1.3.06-bounded-concurrency.md)

**First Principles**

1. **Q:** Why does passing already-created fetch promises defeat a pool's scheduling budget?
   **A:** Their requests have already been initiated. Give the pool items and a mapper it calls only when a slot becomes available.

**How It Works**

2. **Q:** Why does the shared cursor not need a lock in these workers?
   **A:** Claiming an index happens synchronously within one JavaScript agent before awaiting. This reasoning does not apply to shared memory accessed by multiple worker threads.

**Code Examples**

3. **Q:** What happens when a mapper rejects in the canonical fail-fast pool?
   **A:** Its worker and the aggregate reject, while other workers continue their own loops. Stopping outstanding I/O or later starts requires a cancellation policy.

4. **Q:** Why catch failures inside the collect-all worker?
   **A:** Catching records that input's failure and lets the same worker claim another item; each input receives an indexed outcome.

5. **Q:** What should an already-aborted pool return for its queued inputs?
   **A:** This version starts none of them and records a rejected outcome with the abort reason for each index. It never returns sparse result holes.

**Common Mistakes**

6. **Q:** Why reject a concurrency limit of zero rather than create zero workers?
   **A:** Zero workers perform no work yet `Promise.all([])` resolves; an unfilled output array can look like success. Validate the budget at the API boundary.

**Best Practices**

7. **Q:** Can a concurrency budget of four guarantee fewer than ten requests each second?
   **A:** No; fast tasks can recycle those slots many times a second. Concurrency limits active work, while rate limiting controls starts over time.

**Performance Considerations**

8. **Q:** What additional buffer matters in an ordered streaming pool?
   **A:** Results that finish ahead of a slow earlier item may accumulate before delivery. Bound that buffer as well as active tasks to provide consumer backpressure.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
