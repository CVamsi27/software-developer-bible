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

**Q:** Where do `?.` and `??` draw their lines, and why does that split matter?

**A:** Optional chaining short-circuits a continuous optional chain when its guarded base is nullish; add it at each link that may be absent. Nullish coalescing falls back only on null or undefined, so values such as zero, an empty string, and false survive it but not logical OR.

**Q:** Which completion paths must a `Promise.withResolvers` owner preserve?

**A:** Return the promise and retain the functions needed to report the owned operation's outcomes. Resolve can fulfill with a value or adopt another promise's result, while reject reports a rejection reason. The owner must ensure completion/error paths settle appropriately; the API neither starts nor cancels work.

**Q:** What does `/^[\w--\d]+$/v` reject that the same pattern without `v` accepts, and what does that tell you about `v`?

**A:** With `v` the `--` is set subtraction, so the class means "word characters minus digits" and `'a1'` fails; in a non-Unicode legacy character class the repeated hyphens are accepted literally, `\d` still applies, and `'a1'` matches. The `v` (unicodeSets) flag is ES2024, and it changes what the same characters mean, not just which characters match.

**Q:** Why choose `toSorted()` when a sorted view must not change the source array?

**A:** `sort()` mutates the source array, so every owner of that array sees the new order. `toSorted()` returns a new outer array while retaining the original row objects; it protects the source order, not nested object identity.

**Q:** When does `Object.groupBy` silently merge groups that `Map.groupBy` would keep apart?

**A:** When distinct results convert to the same property key, such as numeric `1` and string `'1'`, or ordinary objects with matching string conversion. `Object.groupBy` preserves symbol keys, so not every non-string key collides. `Map.groupBy` retains object identity and key type.

**Q:** What should decide between `structuredClone()` and a JSON round trip?

**A:** Their data contracts differ. `structuredClone()` supports cycles and a broader set of built-in values; JSON serialization only handles JSON data and throws on cycles. Choose the required representation first, then benchmark only if both preserve the needed meaning.

**Q:** Why does the edition year alone fail to establish that a new API is safe to deploy?

**A:** Browsers, server runtimes, parsers, and type declarations adopt features on different schedules. Check syntax support in the build and method support in every deployed runtime; a declaration does not install the implementation.

**Q:** Is `structuredClone` uniformly faster than the JSON round-trip, and if not why does it still win?

**A:** No; measure the actual data and runtime. JSON serialization and structured cloning have different contracts. Structured cloning supports cycles and types such as Date, Map, Set and typed arrays that a JSON round-trip loses or changes. Choose the required behavior first, then compare timings for data supported by both.

**Q:** When does `Array.fromAsync` unwrap values from an async iterable, and what does a mapper change?

**A:** Without a mapper, a custom async iterator's promise-valued result can remain an element; Array.fromAsync does not re-await async-iterator values. An async generator adopts a promise at its own yield boundary. Mapper results and sync-iterator values are awaited during collection. `Array.fromAsync` is asynchronous collection, not an async-stream pipeline.

**Q:** How does `Iterator.concat` avoid the eager work of array concatenation?

**A:** It returns a synchronous iterator that asks each source for values in order as the consumer advances. It does not build an array, and later sources are not consumed before iteration reaches them.

**Q:** Why can `map.getOrInsert(key, expensiveDefault())` do work that `getOrInsertComputed` avoids?

**A:** JavaScript evaluates function arguments before the call, so `expensiveDefault()` runs even when the key already exists. The computed form calls its callback only for a missing key; a stored `undefined` still counts as present.

**Q:** What part of a JSON numeric token can an ES2026 reviver use to recover an exact integer?

**A:** For primitive values the reviver's third argument provides `context.source`, the original JSON spelling. Check the field's accepted syntax, then convert the text to `BigInt` before relying on the rounded Number. This does not make JSON numbers generally arbitrary-precision.

**Q:** Why is `Math.sumPrecise` still the wrong representation for an exact decimal currency total?

**A:** Its improved summation reduces intermediate floating-point error but returns a Number. Use integer minor units or a decimal type when the domain requires exact decimal arithmetic.

**Q:** What boundary does `Error.isError` handle that `instanceof Error` may miss?

**A:** It recognizes built-in Error objects across realms where the prototype chain differs. It does not prove an error is trusted or safe to render.

**Q:** Why decode base64 directly to `Uint8Array` instead of treating it as text?

**A:** Base64 represents bytes, not characters. The typed-array methods avoid an intermediate Latin-1 string and expose choices such as standard versus URL-safe alphabet and how strictly to accept the final chunk.

## Web Workers

Source: [Web Workers](10.1.6.02-web-workers.md)

**Q:** Why do workers get their own heap instead of sharing the page's objects?

**A:** Separate JavaScript object graphs avoid automatic shared mutation across the page and worker. Ordinary messages clone supported data or transfer supported resources. `SharedArrayBuffer` is a separate opt-in way to share bytes; it needs synchronization and the required browser isolation settings. Workers do not share arbitrary objects or DOM nodes.

**Q:** Why is a 200 ms computation a *correctness-of-experience* problem rather than merely slowness?

**A:** A long main-thread computation delays input handlers and rendering opportunities. A roughly 16.7 ms refresh interval applies at 60 Hz, not every device. A worker can perform the calculation separately while the page handles UI; sending and publishing results still cost main-thread work.

**Q:** What does `worker.postMessage({ buffer }, [buffer])` do to the sender's copy of the buffer?

**A:** It transfers ownership and detaches the sender's ArrayBuffer. Its `byteLength` becomes 0 and existing views can no longer use that backing data normally. The worker receives the transferred data. This does not guarantee that the engine physically moves bytes without copying.

**Q:** Why must a SharedWorker protocol choose between replying to the requesting tab and broadcasting to all tabs?

**A:** Each client connects through its own MessagePort. The worker must retain eligible ports and post to each for fan-out, or reply only through the requesting port; `BroadcastChannel` is a separate option when messages should be delivered to peers. With `addEventListener`, call `port.start()`; assigning `onmessage` starts delivery implicitly. Closing one tab's port does not close another's.

**Q:** What are the two OffscreenCanvas ownership paths, and who presents the result?

**A:** A page can transfer control of its visible canvas so the worker draws into the canvas the browser presents. Or the worker can draw to an independent OffscreenCanvas and send ImageBitmap frames back for the page to present. Bound frames in flight and close each bitmap after use.

**Q:** Why does moving an asynchronous network wait to a worker rarely improve page responsiveness?

**A:** Waiting for `fetch()` does not occupy the page with a long synchronous calculation. A worker adds startup and message costs without moving the network wait off the UI path; use one when measured CPU work around the request blocks the page.

**Q:** What happens if you post a DOM node or a function through `postMessage`?

**A:** Structured clone rejects it with a `DataCloneError` — those objects have no serializable representation. Pass plain data and rebuild the DOM on the main thread from whatever the worker returns.

**Q:** Why pool a worker instead of spawning one per task?

**A:** Startup and script evaluation add overhead, so reuse can help a sequence of tasks. Measure the actual workload; `hardwareConcurrency` is a hint, not an instruction to occupy every logical processor. Bound queued work, define per-task replies/errors, and stop idle workers when their owner ends.

## DOM Events & Delegation

Source: [DOM Events & Delegation](10.1.6.03-dom-events-delegation.md)

**Q:** Why is event delegation something the platform hands you rather than an optimization you bolt on?

**A:** A bubbling event already travels along its dispatch path, so one stable parent listener can route clicks from children added later. Non-bubbling events, shadow retargeting and stopped propagation change that visibility. Routing still requires validated target/closest/containment checks.

**Q:** Put the three propagation phases in order, and say where a `{ capture: true }` listener fires.

**A:** Capture runs top-down from `window` to the target's parent, the target phase runs listeners on the element itself, then bubbling climbs back to `window`. Ancestor capture listeners run on the first pass. On the target, capture listeners run before non-capture listeners, both in the target phase.

**Q:** Between `event.target` and `event.currentTarget`, which stays constant as the event climbs, and which changes?

**A:** `currentTarget` identifies the node whose listener is executing. `target` identifies the dispatch target as exposed to that listener; shadow DOM can retarget it across a boundary. Do not assume it is always the same deepest element for every listener.

**Q:** Why can't you delegate `focus` with a plain container-level listener, and what is the workaround?

**A:** `focus` does not bubble, so an ordinary ancestor bubble listener misses it. An ancestor capture listener can observe it, or you can use the bubbling `focusin` event. React's `onFocus` uses `focusin`.

**Q:** What can an ancestor capture listener observe, and what can still prevent it from running?

**A:** It runs on the event path before target and bubbling listeners, so later handlers cannot retroactively hide the event. A capture listener earlier in the path can stop propagation; capture does not guarantee observation of every event.

**Q:** What does `preventDefault()` on a link click leave running, and what would you call to stop that?

**A:** Propagation continues if the event bubbles. `stopPropagation` prevents later propagation steps, without undoing earlier capture handlers or necessarily stopping other listeners in the current invocation. `stopImmediatePropagation` also stops remaining current listeners. Default cancellation requires a cancelable event and a non-passive listener.

**Q:** What does `{ passive: true }` promise the browser, and what does that promise buy on the main thread?

**A:** That the handler will never call `preventDefault()`. The browser can avoid waiting for that handler to decide whether to cancel scrolling. This reduces a blocking decision; it does not guarantee immediate presentation or make an expensive handler free.

**Q:** Why pair `closest(selector)` with `root.contains(...)` inside a delegated handler?

**A:** `closest` walks up from whatever was actually hit, so a click on an icon inside a button still matches the button; `contains` rejects a `closest` match above/outside the delegated root. A neighbouring subtree does not normally bubble through this root; the guard limits the match search, rather than changing propagation.

## Cross-Tab Communication

Source: [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md)

**Q:** Why can't two same-origin tabs simply share an object instead of messaging?

**A:** Tabs independently initialize globals; a shared origin does not unify their models. Eligible same-origin windows with direct references can access objects, and explicit shared byte buffers have their own rules. Message transports copy supported data, constrain recipients and require a recovery policy for missing messages.

**Q:** You need one WebSocket serving five tabs. Which transport fits, and why doesn't `BroadcastChannel`?

**A:** A `SharedWorker` can own the single socket and accept a `MessagePort` from each tab; the worker's application code defines request ordering, queuing, backpressure and reconnect behavior. `BroadcastChannel` only fans messages out to eligible peers; it does not elect a socket owner, so each tab would otherwise manage its own connection.

**Q:** What are the two `storage`-event gotchas that break naive cross-tab code?

**A:** It never fires in the tab that wrote (apply the change locally yourself), and it never fires when the new value equals the old one — so re-writing an identical string notifies nobody.

**Q:** In the theme-sync example, why does the writer apply the theme after saving and posting a message?

**A:** The writing tab receives no `storage` event of its own, so it applies the change locally. The other tabs may receive a storage event, a BroadcastChannel message, or both, so applying the same validated value must be harmless.

**Q:** What should an authentication-change message contain, and why must the server remain authoritative?

**A:** Send a public session-generation value and event ID, not a credential. Tabs can deduplicate the event and reject a marker from an older session; they must revalidate with the server because a browser message cannot revoke or prove the validity of a credential.

**Q:** Why is `if (acquireLock("checkout")) chargeCard()` a double-charge waiting to happen?

**A:** A localStorage check followed by a write is not atomic: both tabs can read "free" before either writes. Web Locks can serialize cooperating local contexts, but cannot prove that a payment request reached the server only once. Use a server-side idempotency contract for the charge and local coordination for the UI.

**Q:** Why shouldn't the megabyte report itself travel over the channel?

**A:** Large fan-out adds serialization/copy and repeated processing costs. Commit the report in IndexedDB, then signal its ID; receivers validate the notification and read the stored result. Storage still has read/clone costs and quota/eviction limits, and the signal is not durable.

**Q:** Why version a changed message schema across deployments?

**A:** Because an old tab and a new tab are routinely open at the same time — a stale listener receiving a shape it doesn't recognize will throw or silently ignore it, so a `v` field lets each side decide whether to parse, upgrade, or drop the message.

## Changed-condition checks

Source: [Cross-Tab Communication](10.1.6.04-cross-tab-communication.md)

**Q:** A and B see the same logout through channel and storage, then C logs in later. What prevents duplicate work or a stale logout?

**A:** A unique event ID deduplicates recent deliveries; idempotent server revalidation tolerates repeats. The public session generation rejects a saved event from an earlier session. C must explicitly read the marker or current server state; a storage event is not history replay.

Source: [DOM Events](10.1.6.03-dom-events-delegation.md)

**Q:** With outer/inner capture and non-capture click listeners, what runs first, and what changes when the inner listener cancels default?

**A:** Outer capture, inner capture, inner non-capture, then outer bubble. Cancelling a cancelable non-passive click suppresses its default action without changing that propagation order. Stopping propagation is a separate operation.

Source: [Modern Features](10.1.6.01-es2024-features.md)

**Q:** A consumer needs only the first ten values from a sequence. How do `Iterator.concat()` and `Array.fromAsync()` differ?

**A:** `Iterator.concat()` composes synchronous iterables lazily, so stopping after ten values leaves later values and sources unconsumed. `Array.fromAsync()` consumes its source and stores the complete result before the array is available.

## Regular Expressions and Text Matching

Source: [Regular Expressions and Text Matching](10.1.6.06-regexp-and-text.md)

**Q:** What does the `g` flag on a regex do, and what state does it preserve between calls?

**A:** The `g` flag makes the regex persist its `lastIndex` position across `test` and `exec` calls so subsequent calls resume after the previous match. On a fresh regex `lastIndex` starts at 0; on a reused regex it remembers the last match end and may skip earlier material in later strings, which is the shared-`test` statefulness bug demonstrated in the chapter's runtime example.

**Q:** How does a backtracking matcher handle nested quantifiers such as `/(a+)+$/`, and what runtime consequence does it have?

**A:** The engine tries every partition of the `a` run; on a non-matching input it explores all partitions, which takes time exponential in the input length. Measured on Node 24.22.1 with inputs of 16 / 20 / 22 / 24 characters the elapsed time grows from 0.6 ms to 215 ms before giving up. The defense is to avoid nested quantifiers over overlapping alternatives, bound the input length, and prefer a character class to an alternation of prefixes.

**Q:** Why does `'👍'.match(/./g)` return two matches while `'👍'.match(/./gu)` returns one?

**A:** The default JavaScript matching model counts UTF-16 code units, so a plane-2 emoji occupies two units; with the `u` flag the engine interprets the pattern in Unicode code-point mode and reports a single match. Omitting `u` around astral or supplementary-plane characters is a correctness bug before it is a performance one.

**Q:** What is the difference between the `i`, `m` and `s` flags in terms of what they change about matching?

**A:** `i` makes the match case-insensitive, so `A` and `a` are equivalent; `m` changes `^` and `$` to match at line boundaries instead of only at the start and end of the entire string; `s` makes `.` also match a newline character, so multi-line input no longer stops the dot at the line break.

**Q:** Why does `RegExp.escape('a.b*c')` output `\x61\.b\*c` and what does it prevent?

**A:** Without escaping, `new RegExp('a.b*c')` interprets `.` as "any character" and `*` as "zero or more of the preceding", so a literal `a.b*c` string would not be matched. `RegExp.escape` renders each character literally, so the resulting regex matches the exact literal string `a.b*c`. It fixes the metacharacter problem but does not reduce the backtracking cost of a still-longer pattern with nested quantifiers.

**Q:** What does `String.prototype.matchAll` require, and how does it differ from `regex.test` with a shared `/g` object?

**A:** `String.prototype.matchAll` throws `TypeError: String.prototype.matchAll called with a non-global RegExp argument` if the regex is not global (`g`). The shared `/g` `test` statefulness bug — `lastIndex` not being reset — causes a second string's first match to be skipped even though `test` succeeds on the second message, because the regex is still parked past the first match's end. Resetting `re.lastIndex = 0` or creating a fresh regex fixes both.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
