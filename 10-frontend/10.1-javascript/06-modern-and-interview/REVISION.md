<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Modern JS & Interview Prep — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## ES2024+ Modern JavaScript Features (through ES2025)

Source: [ES2024+ Modern JavaScript Features (through ES2025)](10.1.6.01-es2024-features.md)

**How It Works**

1. **Q:** Where do `?.` and `??` draw their lines, and why does that split matter?
   **A:** `?.` short-circuits the rest of the chain on the first `null`/`undefined`; `??` falls back only on those two values. A port of `0` or an empty-string name therefore survives `??` but is silently replaced by `||` — choosing between them means saying out loud whether `0`/`''`/`false` are real values to you.

2. **Q:** Why does the `withTimeout` example destructure all three of `promise`, `resolve`, and `reject`?
   **A:** It has to both settle the wrapper (resolve on success, reject on timeout) and return it. Dropping `resolve` still compiles — the reference is only a free variable — but throws `ReferenceError: resolve is not defined` the instant the inner promise fulfills, which is exactly the boilerplate `withResolvers` was added to remove.

3. **Q:** What does `/^[\w--\d]+$/v` reject that the same pattern without `v` accepts, and what does that tell you about `v`?
   **A:** With `v` the `--` is set subtraction, so the class means "word characters minus digits" and `'a1'` fails; without `v`, `--` is just two literal hyphens, `\d` still applies, and `'a1'` matches. The `v` (unicodeSets) flag is ES2024, and it changes what the same characters *mean*, not just which characters match.

**Code Examples**

4. **Q:** Why is `setItems(prev => prev.toSorted(cmp))` the shape you want in React, where does the old version go wrong?
   **A:** `sort()` mutates the array in place, so React sees the same reference, may skip the re-render, and any shared reference sees reordered data underneath it. `toSorted` returns a fresh array, which is what both React's identity check and a reducer's purity expect.

**Real-World Use Cases**

5. **Q:** When does `Object.groupBy` silently merge groups that `Map.groupBy` would keep apart?
   **A:** When your callback returns non-string keys. `Object.groupBy` turns them into property keys, so two different objects both become `"[object Object]"` and land in one bucket; `Map.groupBy` uses them as keys by identity and preserves insertion order.

**Common Mistakes**

6. **Q:** Which contents does `JSON.parse(JSON.stringify(x))` destroy that `structuredClone(x)` keeps, and what does it do on cycles?
   **A:** Dates become strings, Maps and Sets become empty objects, RegExps become `{}`, and anything non-JSON-valued is lost — while a circular structure makes `JSON.stringify` throw outright. `structuredClone` preserves Date/Map/Set/RegExp/typed arrays and follows cycles back to the same object.

**Best Practices**

7. **Q:** The chapter recommends feature-detecting before adopting these APIs — what is the concrete support floor for the ES2024 trio called out here?
   **A:** `Object.groupBy`, `Promise.withResolvers`, and `ArrayBuffer.transfer` need roughly Node 21+, Chrome 117+, and Safari 17.4+, so `typeof Object.groupBy === "function"` (or a small polyfill) is the guard before shipping them to older runtimes.

**Performance Considerations**

8. **Q:** Is `structuredClone` uniformly faster than the JSON round-trip, and if not why does it still win?
   **A:** No — on plain JSON-shaped objects the JSON round-trip is the faster one (about 2× in a Node 23 check). `structuredClone` wins where it has to: it survives cycles and non-JSON types JSON cannot represent, and it copies a typed array in memory rather than serializing a million-element number array through a string.

## Web Workers

Source: [Web Workers](10.1.6.02-web-workers.md)

**First Principles**

1. **Q:** Why do workers get their own heap instead of sharing the page's objects?
   **A:** Shared objects would mean shared mutable state, which forces locks and reintroduces every concurrency bug workers exist to avoid. With separate heaps the only crossing is `postMessage`, so the isolation itself *is* the concurrency model: copy (structured clone) or hand off (transferable), nothing else.

**Why It Matters**

2. **Q:** Why is a 200 ms computation a *correctness-of-experience* problem rather than merely slowness?
   **A:** Frames are budgeted at about 16 ms; anything longer steals paint time, so the UI freezes and frames drop. The worker answers it by moving the budget-buster to a thread the paints don't depend on — the main thread keeps rendering while the 200 ms runs elsewhere.

**Dedicated Worker**

3. **Q:** What does `worker.postMessage({ buffer }, [buffer])` do to the sender's copy of the buffer?
   **A:** Ownership moves instead of bytes being copied: the worker receives the same 100 MB untouched, and on the main thread `buffer.byteLength` drops to 0 — the sender can never read it again, which is exactly the point of transferring rather than cloning.

**Shared Worker**

4. **Q:** How does the shared worker fan a message out to every connected tab?
   **A:** It keeps a `Set` of `MessagePort`s handed to it by each `onconnect` event and re-posts incoming messages to all of them; on the page side each tab calls `worker.port.start()` before posting or listening, since the port is delivered, not constructed.

**OffscreenCanvas**

5. **Q:** Where does the rendering in the OffscreenCanvas example actually happen, and how does a frame reach the screen?
   **A:** Inside the worker — an `OffscreenCanvas` has its own 2D context there, so `clearRect`/`fillRect` run off-thread. `transferToImageBitmap()` snapshots the frame, the bitmap goes back as a transferable, and the main thread only `drawImage`s it while `requestAnimationFrame` keeps asking for more.

**When to Use Workers**

6. **Q:** Why does `fetch` sit in the "No" column when it can easily take seconds?
   **A:** It is network-bound, not CPU-bound — already asynchronous and off the UI path. A worker would add worker startup plus two message hops around work the event loop was going to await anyway.

**Common Mistakes**

7. **Q:** What happens if you post a DOM node or a function through `postMessage`?
   **A:** Structured clone rejects it with a `DataCloneError` — those objects have no serializable representation. Pass plain data and rebuild the DOM on the main thread from whatever the worker returns.

**Best Practices**

8. **Q:** Why pool a worker instead of spawning one per task?
   **A:** Creation costs roughly 1–40 ms plus script evaluation on every spawn; for many small tasks that overhead dominates the work itself. One reused worker (or `navigator.hardwareConcurrency` of them) amortizes the startup across the whole queue.

## DOM Events & Delegation

Source: [DOM Events & Delegation](10.1.6.03-dom-events-delegation.md)

**First Principles**

1. **Q:** Why is event delegation something the platform hands you rather than an optimization you bolt on?
   **A:** Because the event already walks past every ancestor on its way back up — a listener on a stable parent sees all current and future children without any extra propagation. The only cost delegation adds is routing: asking `event.target` which child was responsible.

**Definition**

2. **Q:** Put the three propagation phases in order, and say where a `{ capture: true }` listener fires.
   **A:** Capture runs top-down from `window` to the target's parent, the target phase runs listeners on the element itself, then bubbling climbs back to `window`. A capture listener sits in the first pass — before any default bubble-phase handler on the way down.

**How It Works**

3. **Q:** Between `event.target` and `event.currentTarget`, which stays constant as the event climbs, and which changes?
   **A:** `target` stays the deepest element that initiated the event at every hop; `currentTarget` is whichever node's listener is executing right now, so it differs at each level of the tree.

4. **Q:** Why can't you delegate `focus` with a plain container-level listener, and what is the workaround?
   **A:** `focus` does not bubble, so the event never reaches an ancestor listener at all — you either attach directly or switch to `focusin`, which does bubble. That is exactly why React maps `onFocus` onto `focusin`.

**Real-World Use Cases**

5. **Q:** Why does the chapter's analytics listener register with `{ capture: true }`?
   **A:** Capture runs before bubbling, so it observes the click before any application handler can call `stopPropagation` and cut the climb short — an observer that must see *every* click cannot sit downstream of code that can mute it.

**Common Mistakes**

6. **Q:** What does `preventDefault()` on a link click leave running, and what would you call to stop that?
   **A:** Propagation — the event keeps bubbling, so document-level analytics still records the click. `stopPropagation()` stops the travel (ancestors never see it) and `stopImmediatePropagation()` additionally silences sibling listeners on the same node; neither of them cancels navigation.

**Performance Considerations**

7. **Q:** What does `{ passive: true }` promise the browser, and what does that promise buy on the main thread?
   **A:** That the handler will never call `preventDefault()`. Because the browser does not have to wait for your JavaScript to finish before deciding, scrolling starts immediately on the compositor instead of after a main-thread round trip on every wheel tick.

**Best Practices**

8. **Q:** Why pair `closest(selector)` with `root.contains(...)` inside a delegated handler?
   **A:** `closest` walks up from whatever was actually hit, so a click on an icon inside a button still matches the button; `contains` then rejects matches that arrived from outside the container, so an event bubbling in from a neighbouring subtree can't trigger the wrong listener.

## Cross-Tab Communication

Source: [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md)

**First Principles**

1. **Q:** Why can't two same-origin tabs simply share an object instead of messaging?
   **A:** Each tab is its own event loop, heap, and realm — the browser shares origin and storage, never memory. So every exchange must ride a channel the browser mediates, and picking a channel is really picking who is allowed to hear you.

**How It Works**

2. **Q:** You need one WebSocket serving five tabs. Which transport fits, and why doesn't `BroadcastChannel`?
   **A:** A `SharedWorker` hub: it lives outside every tab, so it owns the single socket and a single serialized queue in a star topology. `BroadcastChannel` only fans messages out to peers — each tab would still open its own socket and its own copy of the state.

3. **Q:** What are the two `storage`-event gotchas that break naive cross-tab code?
   **A:** It never fires in the tab that wrote (apply the change locally yourself), and it never fires when the new value equals the old one — so re-writing an identical string notifies nobody.

**Code Examples**

4. **Q:** In `ThemeSync.set`, why call `this.apply(theme)` after already writing to storage and posting a message?
   **A:** The writing tab receives no `storage` event of its own, so the local apply is what updates this tab; `localStorage.setItem` persists and notifies the others, and the BroadcastChannel post gives them the change without waiting for storage to round-trip.

**Real-World Use Cases**

5. **Q:** Why does the sync-logout recipe do all three of broadcast, storage write, and server invalidation?
   **A:** The broadcast reaches live tabs immediately, the persisted `auth-event` marker catches tabs that load later, and the server-side invalidation is what actually kills the session — without it a token already copied out still works.

**Common Mistakes**

6. **Q:** Why is `if (acquireLock("checkout")) chargeCard()` a double-charge waiting to happen?
   **A:** Read-then-write over `localStorage` has a race window: both tabs can read "free" before either writes, so both proceed. Treat that lock as UX only — correctness needs idempotency keys (or Web Locks, which the browser serializes atomically).

**Performance Considerations**

7. **Q:** Why shouldn't the megabyte report itself travel over the channel?
   **A:** `storage` events stringify everything and every channel pays clone cost per listener, so big payloads turn each tab into a JSON tax. Signal with a tiny message and let the receiver read the bytes from IndexedDB, which is shared on disk and written once.

**Best Practices**

8. **Q:** Why version your message schema after every deploy?
   **A:** Because an old tab and a new tab are routinely open at the same time — a stale listener receiving a shape it doesn't recognize will throw or silently ignore it, so a `v` field lets each side decide whether to parse, upgrade, or drop the message.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
