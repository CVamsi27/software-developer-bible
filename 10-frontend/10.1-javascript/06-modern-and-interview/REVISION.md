<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-7_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Modern JS & Interview Prep — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Recent ECMAScript Features (ES2022–ES2026)

Source: [Recent ECMAScript Features](10.1.6.01-es2024-features.md)

**How It Works**

1. **Q:** Where do `?.` and `??` draw their lines, and why does that split matter?
   **A:** `?.` short-circuits the rest of the chain on the first `null`/`undefined`; `??` falls back only on those two values. A port of `0` or an empty-string name therefore survives `??` but is silently replaced by `||` — choosing between them means saying out loud whether `0`/`''`/`false` are real values to you.

2. **Q:** Why does the `withTimeout` example destructure all three of `promise`, `resolve`, and `reject`?
   **A:** It has to both settle the wrapper (resolve on success, reject on timeout) and return it. A missing `resolve` is an undeclared identifier that TypeScript normally reports; unchecked JavaScript throws `ReferenceError: resolve is not defined` the instant the inner promise fulfills, which is exactly the boilerplate `withResolvers` was added to remove.

3. **Q:** What does `/^[\w--\d]+$/v` reject that the same pattern without `v` accepts, and what does that tell you about `v`?
   **A:** With `v` the `--` is set subtraction, so the class means "word characters minus digits" and `'a1'` fails; in a non-Unicode legacy character class the repeated hyphens are accepted literally, `\d` still applies, and `'a1'` matches. The `v` (unicodeSets) flag is ES2024, and it changes what the same characters *mean*, not just which characters match.

**Code Examples**

4. **Q:** Why is `setItems(prev => prev.toSorted(cmp))` the shape you want in React, where does the old version go wrong?
   **A:** `sort()` mutates the array in place, so React sees the same reference, may skip the re-render, and any shared reference sees reordered data underneath it. `toSorted` returns a fresh array, which is what both React's identity check and a reducer's purity expect.

**Real-World Use Cases**

5. **Q:** When does `Object.groupBy` silently merge groups that `Map.groupBy` would keep apart?
   **A:** When distinct results convert to the same property key, such as numeric `1` and string `'1'`, or ordinary objects with matching string conversion. `Object.groupBy` preserves symbol keys, so not every non-string key collides. `Map.groupBy` retains object identity and key type.

**Common Mistakes**

6. **Q:** Which contents does `JSON.parse(JSON.stringify(x))` destroy that `structuredClone(x)` keeps, and what does it do on cycles?
   **A:** Dates become strings, Maps and Sets become empty objects, RegExps become `{}`, and anything non-JSON-valued is lost — while a circular structure makes `JSON.stringify` throw outright. `structuredClone` preserves Date/Map/Set/RegExp/typed arrays and follows cycles back to the same object.

**Best Practices**

7. **Q:** The chapter recommends feature-detecting before adopting these APIs — what is the concrete support floor for the ES2024 trio called out here?
   **A:** Check `Object.groupBy`, `Promise.withResolvers` and `ArrayBuffer.transfer` separately against the deployed browser and Node versions. Their support did not arrive together merely because they share a specification year. A method check such as `typeof Object.groupBy === "function"` can select a tested fallback. New syntax instead needs a compatible build or parser target.

**Performance Considerations**

8. **Q:** Is `structuredClone` uniformly faster than the JSON round-trip, and if not why does it still win?
   **A:** No; measure the actual data and runtime. JSON serialization and structured cloning have different contracts. Structured cloning supports cycles and types such as Date, Map, Set and typed arrays that a JSON round-trip loses or changes. Choose the required behavior first, then compare timings for data supported by both.

**ES2026 boundaries**

9. **Q:** When does `Array.fromAsync` unwrap values from an async iterable, and what does a mapper change?
   **A:** Without a mapper, a custom async iterator's promise-valued result can remain an element; Array.fromAsync does not re-await async-iterator values. An async generator adopts a promise at its own yield boundary. Mapper results and sync-iterator values are awaited during collection. `Array.fromAsync` is asynchronous collection, not an async-stream pipeline.

10. **Q:** How does `Iterator.concat` avoid the eager work of array concatenation?
    **A:** It returns a synchronous iterator that asks each source for values in order as the consumer advances. It does not build an array, and later sources are not consumed before iteration reaches them.

11. **Q:** Why can `map.getOrInsert(key, expensiveDefault())` do work that `getOrInsertComputed` avoids?
    **A:** JavaScript evaluates function arguments before the call, so `expensiveDefault()` runs even when the key already exists. The computed form calls its callback only for a missing key; a stored `undefined` still counts as present.

12. **Q:** What part of a JSON numeric token can an ES2026 reviver use to recover an exact integer?
    **A:** For primitive values the reviver's third argument provides `context.source`, the original JSON spelling. Check the field's accepted syntax, then convert the text to `BigInt` before relying on the rounded Number. This does not make JSON numbers generally arbitrary-precision.

13. **Q:** Why is `Math.sumPrecise` still the wrong representation for an exact decimal currency total?
    **A:** Its improved summation reduces intermediate floating-point error but returns a Number. Use integer minor units or a decimal type when the domain requires exact decimal arithmetic.

14. **Q:** What boundary does `Error.isError` handle that `instanceof Error` may miss?
    **A:** It recognizes built-in Error objects across realms where the prototype chain differs. It does not prove an error is trusted or safe to render.

15. **Q:** Why decode base64 directly to `Uint8Array` instead of treating it as text?
    **A:** Base64 represents bytes, not characters. The typed-array methods avoid an intermediate Latin-1 string and expose choices such as standard versus URL-safe alphabet and how strictly to accept the final chunk.

## Web Workers

Source: [Web Workers](10.1.6.02-web-workers.md)

**First Principles**

1. **Q:** Why do workers get their own heap instead of sharing the page's objects?
   **A:** Separate JavaScript object graphs avoid automatic shared mutation across the page and worker. Ordinary messages clone supported data or transfer supported resources. `SharedArrayBuffer` is a separate opt-in way to share bytes; it needs synchronization and the required browser isolation settings. Workers do not share arbitrary objects or DOM nodes.

**Why It Matters**

2. **Q:** Why is a 200 ms computation a *correctness-of-experience* problem rather than merely slowness?
   **A:** A long main-thread computation delays input handlers and rendering opportunities. A roughly 16.7 ms refresh interval applies at 60 Hz, not every device. A worker can perform the calculation separately while the page handles UI; sending and publishing results still cost main-thread work.

**Dedicated Worker**

3. **Q:** What does `worker.postMessage({ buffer }, [buffer])` do to the sender's copy of the buffer?
   **A:** It transfers ownership and detaches the sender's ArrayBuffer. Its `byteLength` becomes 0 and existing views can no longer use that backing data normally. The worker receives the transferred data. This does not guarantee that the engine physically moves bytes without copying.

**Shared Worker**

4. **Q:** How does the shared worker fan a message out to every connected tab?
   **A:** Fan-out is an explicit application policy: retain eligible connected ports and post to each. The chapter's cache protocol replies on the requesting port instead. `port.start()` enables queued delivery when using `addEventListener`; assigning `onmessage` implicitly starts that port. Closing one tab's port does not close another's.

**OffscreenCanvas**

5. **Q:** Where does the rendering in the OffscreenCanvas example actually happen, and how does a frame reach the screen?
   **A:** In the chapter's transferred-canvas path, the page calls `transferControlToOffscreen` and transfers that canvas to the worker, which draws into its own context. The browser presents it on the associated page canvas; no per-frame ImageBitmap reply is shown. Bitmap transfer is a separate presentation design.

**When to Use Workers**

6. **Q:** Why does `fetch` sit in the "No" column when it can easily take seconds?
   **A:** It is network-bound, not CPU-bound — already asynchronous and off the UI path. A worker would add worker startup plus two message hops around work the event loop was going to await anyway.

**Common Mistakes**

7. **Q:** What happens if you post a DOM node or a function through `postMessage`?
   **A:** Structured clone rejects it with a `DataCloneError` — those objects have no serializable representation. Pass plain data and rebuild the DOM on the main thread from whatever the worker returns.

**Best Practices**

8. **Q:** Why pool a worker instead of spawning one per task?
   **A:** Startup and script evaluation add overhead, so reuse can help a sequence of tasks. Measure the actual workload; `hardwareConcurrency` is a hint, not an instruction to occupy every logical processor. Bound queued work, define per-task replies/errors, and stop idle workers when their owner ends.

## DOM Events & Delegation

Source: [DOM Events & Delegation](10.1.6.03-dom-events-delegation.md)

**First Principles**

1. **Q:** Why is event delegation something the platform hands you rather than an optimization you bolt on?
   **A:** A bubbling event already travels along its dispatch path, so one stable parent listener can route clicks from children added later. Non-bubbling events, shadow retargeting and stopped propagation change that visibility. Routing still requires validated target/closest/containment checks.

**Definition**

2. **Q:** Put the three propagation phases in order, and say where a `{ capture: true }` listener fires.
   **A:** Capture runs top-down from `window` to the target's parent, the target phase runs listeners on the element itself, then bubbling climbs back to `window`. Ancestor capture listeners run on the first pass. On the target, capture listeners run before non-capture listeners, both in the target phase.

**How It Works**

3. **Q:** Between `event.target` and `event.currentTarget`, which stays constant as the event climbs, and which changes?
   **A:** `currentTarget` identifies the node whose listener is executing. `target` identifies the dispatch target as exposed to that listener; shadow DOM can retarget it across a boundary. Do not assume it is always the same deepest element for every listener.

4. **Q:** Why can't you delegate `focus` with a plain container-level listener, and what is the workaround?
   **A:** `focus` does not bubble, so an ordinary ancestor bubble listener misses it. An ancestor capture listener can observe it, or you can use the bubbling `focusin` event. React's `onFocus` uses `focusin`.

**Real-World Use Cases**

5. **Q:** Why does the chapter's analytics listener register with `{ capture: true }`?
   **A:** An ancestor capture listener runs before descendant target/bubble listeners, so those later handlers cannot retroactively hide that click. An earlier capture listener can still stop propagation or immediate propagation; no location promises to observe every possible event.

**Common Mistakes**

6. **Q:** What does `preventDefault()` on a link click leave running, and what would you call to stop that?
   **A:** Propagation continues if the event bubbles. `stopPropagation` prevents later propagation steps, without undoing earlier capture handlers or necessarily stopping other listeners in the current invocation. `stopImmediatePropagation` also stops remaining current listeners. Default cancellation requires a cancelable event and a non-passive listener.

**Performance Considerations**

7. **Q:** What does `{ passive: true }` promise the browser, and what does that promise buy on the main thread?
   **A:** That the handler will never call `preventDefault()`. The browser can avoid waiting for that handler to decide whether to cancel scrolling. This reduces a blocking decision; it does not guarantee immediate presentation or make an expensive handler free.

**Best Practices**

8. **Q:** Why pair `closest(selector)` with `root.contains(...)` inside a delegated handler?
   **A:** `closest` walks up from whatever was actually hit, so a click on an icon inside a button still matches the button; `contains` rejects a `closest` match above/outside the delegated root. A neighbouring subtree does not normally bubble through this root; the guard limits the match search, rather than changing propagation.

## Cross-Tab Communication

Source: [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md)

**First Principles**

1. **Q:** Why can't two same-origin tabs simply share an object instead of messaging?
   **A:** Tabs independently initialize globals; a shared origin does not unify their models. Eligible same-origin windows with direct references can access objects, and explicit shared byte buffers have their own rules. Message transports copy supported data, constrain recipients and require a recovery policy for missing messages.

**How It Works**

2. **Q:** You need one WebSocket serving five tabs. Which transport fits, and why doesn't `BroadcastChannel`?
   **A:** A `SharedWorker` can own the single socket and accept a `MessagePort` from each tab; the worker's application code defines request ordering, queuing, backpressure and reconnect behavior. `BroadcastChannel` only fans messages out to eligible peers; it does not elect a socket owner, so each tab would otherwise manage its own connection.

3. **Q:** What are the two `storage`-event gotchas that break naive cross-tab code?
   **A:** It never fires in the tab that wrote (apply the change locally yourself), and it never fires when the new value equals the old one — so re-writing an identical string notifies nobody.

**Code Examples**

4. **Q:** In `ThemeSync.set`, why call `this.apply(theme)` after already writing to storage and posting a message?
   **A:** The writing tab receives no `storage` event of its own, so the local apply is what updates this tab; `localStorage.setItem` persists and notifies the others, and the BroadcastChannel provides another transient notification path. Neither channel guarantees a faster delivery, and duplicate application must be harmless.

**Real-World Use Cases**

5. **Q:** Why does the sync-logout recipe do all three of broadcast, storage write, and server invalidation?
   **A:** BroadcastChannel notifies eligible live tabs asynchronously, but delivery is not durable. An explicit startup read of the session-generation-aware marker helps later tabs catch up, and server-side invalidation revokes the session according to the server's credential-validation contract; a client message alone cannot revoke a copied credential.

**Common Mistakes**

6. **Q:** Why is `if (acquireLock("checkout")) chargeCard()` a double-charge waiting to happen?
   **A:** A localStorage check followed by a write is not atomic: both tabs can read "free" before either writes. Web Locks can serialize cooperating local contexts, but cannot prove that a payment request reached the server only once. Use a server-side idempotency contract for the charge and local coordination for the UI.

**Performance Considerations**

7. **Q:** Why shouldn't the megabyte report itself travel over the channel?
   **A:** Large fan-out adds serialization/copy and repeated processing costs. Commit the report in IndexedDB, then signal its ID; receivers validate the notification and read the stored result. Storage still has read/clone costs and quota/eviction limits, and the signal is not durable.

**Best Practices**

8. **Q:** Why version a changed message schema across deployments?
   **A:** Because an old tab and a new tab are routinely open at the same time — a stale listener receiving a shape it doesn't recognize will throw or silently ignore it, so a `v` field lets each side decide whether to parse, upgrade, or drop the message.

## Changed-condition checks

Source: [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md)

**Q:** A and B see the same logout through channel and storage, then C logs in later. What prevents duplicate work or a stale logout?
**A:** A unique event ID deduplicates recent deliveries; idempotent server revalidation tolerates repeats. The public session generation rejects a saved event from an earlier session. C must explicitly read the marker or current server state; a storage event is not history replay.

Source: [DOM Events](10.1.6.03-dom-events-delegation.md)

**Q:** With outer/inner capture and non-capture click listeners, what runs first, and what changes when the inner listener cancels default?
**A:** Outer capture, inner capture, inner non-capture, then outer bubble. Cancelling a cancelable non-passive click suppresses its default action without changing that propagation order. Stopping propagation is a separate operation.

Source: [Modern Features](10.1.6.01-es2024-features.md)

**Q:** Does a timeout around a promise stop the original operation, and do copied sorting methods duplicate nested items?
**A:** No. Settlement and operation cancellation have separate ownership; use an abort contract if available. Copying array methods produce a new container while retaining nested identities.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
