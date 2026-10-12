<!-- section: JavaScript | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-JavaScript-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-10_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Memory & Data — JavaScript — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Pass by Value vs Pass by Reference

Source: [Pass by Value vs Pass by Reference](10.1.4.01-pass-by-value.md)

**Definition**

1. **Q:** What is the one rule JavaScript follows for every argument it passes?
   **A:** The parameter receives the argument's value in its own binding. If that value refers to an object, the caller and parameter refer to the same object. Passing it does not copy the object's contents or make the parameter another name for the caller's variable.

2. **Q:** Why do objects give the *illusion* of being passed by reference?
   **A:** A property write through the parameter changes the same object the caller uses. Reassigning the parameter changes only the parameter's binding, so it does not replace the caller's value. This describes observable behavior without requiring a particular pointer or memory layout.

**How It Works**

3. **Q:** Which act changes what the caller sees — mutation or reassignment?
   **A:** Mutation, because it writes into the object both sides point at. Reassignment replaces only the local binding, so the caller's variable keeps pointing at the original.

4. **Q:** Where does destructuring sit in this story?
   **A:** It is the copy rule in new syntax: the extracted values land in fresh bindings, so reassigning one of them leaves the source object's property untouched.

**Common Mistakes**

5. **Q:** What goes wrong with `function f(arr) { return arr.sort(cmp); }` when the caller wants its array untouched?
   **A:** `sort` reorders in place and returns the same array, so the caller's data changes; spread into a new array first if the input must survive.

6. **Q:** Why does `modifyObject(o)` fail when the body is `o = { value: 20 }`?
   **A:** The parameter is a copied reference. Replacing it allocates a new object and repoints the callee's copy — the caller never observes the new object.

**Best Practices**

7. **Q:** When is `Object.freeze` not enough to make data safe?
   **A:** It protects the object's own properties, not all nested objects. Copying can create independent supported data, but copying alone does not prevent later mutation. Use an explicit recursive protection strategy or an immutable-data library when the contract requires deeper protection.

## Map, Set, WeakMap, WeakSet

Source: [Map, Set, WeakMap, WeakSet](10.1.4.02-map-set-weakmap-weakset.md)

**Definition**

1. **Q:** What do `Map`, `Set`, `WeakMap` and `WeakSet` share, and where do they split?
   **A:** They provide keyed entries or unique membership, with different ownership and observation rules. `Map`/`Set` retain entries and expose size and iteration; weak collections do not retain eligible keys/members by themselves and cannot be enumerated. ECMAScript requires average sublinear access for Map/Set, rather than mandating a hash table or worst-case O(1).

2. **Q:** Why does using an object as a plain object's key break identity?
   **A:** Object property keys become strings or symbols. Ordinary objects with default string conversion commonly collapse to `"[object Object]"`, so they cannot reliably retain key identity. `Map` compares object keys by identity.

**How It Works**

3. **Q:** What actually decides when a `WeakMap` entry goes away?
   **A:** The collection does not keep an eligible key alive by itself. When no other strong path retains that key, its entry becomes eligible for collection; deletion timing is not observable or guaranteed.

4. **Q:** What does "insertion order" buy you in a `Map` that a plain object cannot promise?
   **A:** Iterators visit insertion order. Updating an existing key leaves its position unchanged; delete/reinsert moves it to the end. The LRU example moves a hit to the end, so the first key represents least recently used rather than merely earliest original insertion.

**Code Examples**

5. **Q:** What does `[...new Set(list)]` give you over a hand-written dedupe loop?
   **A:** Uniqueness is decided by SameValueZero and first-seen order is preserved in the resulting array. Engines commonly use hash-based membership, but ECMAScript requires average sublinear access rather than a universal constant-time operation.

**Common Mistakes**

6. **Q:** Why does `for (const x of someWeakMap)` throw a `TypeError`?
   **A:** Weak collections expose no enumerable key list: collection timing must not become an ordinary observable membership scan. Reach for a regular `Map` when you need to walk the contents.

**Best Practices**

7. **Q:** When is a plain object still the better choice than a `Map`?
   **A:** When the keys are a fixed set of known string names and JSON is the transport — object spreads and `JSON.stringify` work for free, while a `Map` stringifies to `{}`.

## Shallow Copy vs Deep Copy

Source: [Shallow Copy vs Deep Copy](10.1.4.03-shallow-vs-deep-copy.md)

**Definition**

1. **Q:** State the difference between a shallow copy and a deep copy in one sentence.
   **A:** A shallow copy separates the outer container and shares nested object values; a deep clone separates the supported graph while preserving its internal aliases/cycles. The API decides which object types and properties can be copied.

**How It Works**

2. **Q:** Why does a deep clone need an identity map (`WeakMap` of original → copy)?
   **A:** A graph copier records the copy before visiting children. Reusing that record preserves repeated references and lets a self-reference point back to the cloned root instead of recursing forever. Built-in structured cloning handles this bookkeeping for supported values.

**Code Examples**

3. **Q:** After `const shallow = { ...original }`, why does `shallow.hobbies.push('cooking')` change `original.hobbies`?
   **A:** Spread only duplicates the first level. The nested array is the same object in both places, so a mutation through either reference is visible through both.

4. **Q:** What does `JSON.parse(JSON.stringify(x))` silently rewrite, and what does it refuse outright?
   **A:** Dates normally become ISO strings, ordinary `Map`/`Set`/`RegExp` become `{}`, and `NaN`/infinities become `null`. Functions, `undefined`, and symbol-valued properties are omitted; array slots with those values become `null`. Cycles and unhandled `BigInt` values throw.

**Common Mistakes**

5. **Q:** What does `structuredClone` hand back when given a class instance?
   **A:** A supported ordinary class instance normally becomes a plain object with cloneable enumerable own properties, without the custom prototype/private fields. An uncloneable property such as a function can still throw, so success is not unconditional.

**Best Practices**

6. **Q:** Which copy routine should you use when a value is about to cross a worker boundary?
   **A:** Worker messaging uses structured cloning, so design a cloneable payload and let postMessage clone it; pre-cloning is usually unnecessary. Transfer lists, ownership and context restrictions still matter: local cloning success alone is not a universal transport guarantee.

**Performance Considerations**

7. **Q:** What should decide between a shallow and a deep copy on a hot path?
   **A:** Whether nested values are treated as immutable. If they are, sharing them keeps the copy proportional to the top-level key count, skips the walk over every reachable node, and avoids breaking identity that other code may rely on.

## Debounce

Source: [Debounce](10.1.4.04-debounce.md)

**Definition**

1. **Q:** What is a debounce function actually waiting for?
   **A:** For ordinary trailing debounce, a quiet gap of N milliseconds. Each call replaces the pending arguments and deadline. Leading execution and explicit flush are separate policies; sustained input can postpone trailing execution indefinitely.

**How It Works**

2. **Q:** Why does debounce fail on a scroll handler where throttle succeeds?
   **A:** Continuous scrolling can keep resetting a trailing debounce indefinitely; it runs when a sufficient pause occurs unless a maximum-wait policy intervenes. A throttle can produce feedback during the stream without waiting for quiet.

3. **Q:** What do the `leading` and `trailing` options choose between?
   **A:** Whether execution happens at the start of a burst or at its end. `leading` runs on the call that opens the quiet window; `trailing` (the default) runs the last call of the burst when the window closes.

**Code Examples**

4. **Q:** What does `.cancel()` actually destroy?
   **A:** It drops the pending invocation, including timer and saved arguments. It does not stop a callback/request that already started; in-flight cancellation and obsolete-result checks are separate policies.

**Real-World Use Cases**

5. **Q:** Why does the resize example pair `removeEventListener` with `handleResize.cancel()`?
   **A:** Removing the listener stops future events, but a timer already scheduled would still fire — calling `setState` after the component unmounted — unless `cancel()` clears it too.

**Common Mistakes**

6. **Q:** What's wrong with `debounce(fetchResults, 50)` and with `debounce(fetchResults, 2000)`?
   **A:** A short delay can expire between keystrokes and start more work; a long delay can feel unresponsive. The result depends on actual input cadence and task cost, so 300ms is an example to measure rather than a universal typing constant.

**Best Practices**

7. **Q:** How do you keep one debounced function alive across React re-renders?
   **A:** Keep the wrapper stable for its intended lifetime, update a callback ref after commit if it must call the latest function, and cancel the wrapper during cleanup. Create timers from events or effects, never during render.

**Summary**

8. **Q:** How do you test debouncing without making the suite slow and flaky?
   **A:** Install fake timers, advance the clock past the wait, and assert on call counts. Real sleeps introduce both the flakiness and the wall-clock cost that fake timers remove.

## Throttle

Source: [Throttle](10.1.4.05-throttle.md)

**First Principles**

1. **Q:** What single question tells you whether to debounce or throttle?
   **A:** Must feedback continue during input, or should work wait for a quiet period? Throttle supports periodic feedback; debounce waits for quiet. Both can preserve the final value with trailing execution, so final-value importance alone does not choose between them.

**Definition**

2. **Q:** What does a throttled function promise its caller?
   **A:** The chapter’s ordinary throttle spaces callback starts by at least the configured interval and can retain the latest suppressed arguments for trailing execution. Cancel resets timing and flush can override spacing; promises already started can overlap.

**How It Works**

3. **Q:** When does the trailing invocation fire, and whose arguments does it carry?
   **A:** If at least one call landed during the window, one final invocation runs as the window closes using the most recent call's arguments — everything older in that window is already gone.

4. **Q:** Why is `requestAnimationFrame` often a better throttle than a timer for scroll-driven work?
   **A:** It schedules work at a browser rendering opportunity. Keep one pending callback to combine incoming events before it runs. This coordinates visual work with rendering, but does not guarantee a displayed frame, a fixed rate or that none of the work is wasted.

**Code Examples**

5. **Q:** Why does the leading/trailing implementation stash `lastArgs` instead of invoking right away?
   **A:** A call arriving mid-window has to be remembered so exactly one trailing invocation can replay it — that is the difference between a throttle that preserves the last event and a naive gate that loses it.

**Common Mistakes**

6. **Q:** What goes wrong with `throttle(fetchResults, 300)` on a search box?
   **A:** Throttle can start queries during continuous typing; a trailing call can still carry the final query. Choose debounce when quiet is the desired trigger. Neither mechanism prevents older responses from overwriting newer results without a generation policy.

**Best Practices**

7. **Q:** What limits make sense for the usual event types?
   **A:** Those intervals are experiments, not guarantees. Coalesce visual work at rendering opportunities; measure mouse/scroll/resize latency. Prevent concurrent writes with an in-flight guard/idempotency, because a one-second window cannot guarantee request completion.

8. **Q:** What is the cleanup contract for a throttled event handler?
   **A:** Its owner removes the event listener and calls `.cancel()` to drop pending trailing work when that event source ends. Cancellation does not stop a callback or request that already started.

## Memory Leaks

Source: [Memory Leaks](10.1.4.06-memory-leaks.md)

**First Principles**

1. **Q:** Why can't a collector ever *prevent* a memory leak?
   **A:** It only reclaims unreachable objects, and a leak is by definition something still reachable from a long-lived holder. Knowing that the reference is unwanted is intent, which the engine has no way to observe.

**Definition**

2. **Q:** What is the practical test for "is this a leak?"
   **A:** Find the retaining path and ask whether it should still exist. Reachable obsolete data suggests a leak; unreachable data is eligible for collection, which may happen later. A wanted cache still needs a deliberate size/lifetime policy.

**How It Works**

3. **Q:** What are the chapter's five causes, and what is the single move that repairs each?
   **A:** Long-lived listener paths, closures retaining obsolete data, timers, globals and unbounded caches can keep data reachable. A detached node/listener cycle alone is collectible. Find the root path, then remove the unwanted owner or apply an explicit retention bound.

4. **Q:** How do you tell a growing heap apart from a leak while the app is running?
   **A:** Repeat a controlled lifecycle and compare snapshots/retaining paths after equivalent collection opportunities. Growth can also be wanted cache warm-up or delayed collection; distinguish retained obsolete objects from expected live state before calling it a leak.

**Code Examples**

5. **Q:** Why doesn't the detached-node example leak once its function returns?
   **A:** A node with only its own listener can become unreachable after its creating scope finishes. The revised window-listener example has a longer-lived path through window → callback → button; returning from the mounting function does not break it. Call and retire the disposer.

6. **Q:** Why does capturing `hugeData.length` instead of reading `hugeData` inside the closure change anything?
   **A:** Calculate the length first and let the callback use only that number. The callback then has no need to access the original array. The engine may reclaim the array once it is unreachable, but exact storage and collection timing remain implementation details.

**Real-World Use Cases**

7. **Q:** What does `AbortController` give a fetch effect that a boolean flag does not?
   **A:** It can ask a supported in-flight fetch or body read to stop. A flag can prevent an obsolete result from updating state, but does not cancel the underlying request. Use cleanup and a latest-result check together because cancellation can arrive after completion or be ignored by a custom loader.

**Common Mistakes**

8. **Q:** Why is a plain `Map` the wrong container for object-keyed side data?
   **A:** A reachable `Map` strongly retains its entries until they are removed or the map becomes unreachable. Use `WeakMap` when metadata should follow a key's external lifetime; use an ordinary bounded map when enumeration or explicit retention is required.

**Best Practices**

9. **Q:** What makes a cache safe to keep in module scope?
   **A:** A policy matching ownership: bounded entry/byte count, expiry that is actually enforced, and resource cleanup where needed. TTL checked only on reads leaves unread entries retained; weak keys leave values alive while keys remain externally reachable.

## Garbage Collection

Source: [Garbage Collection](10.1.4.07-garbage-collection.md)

**First Principles**

1. **Q:** Why is reachability the only criterion a collector can actually use?
   **A:** "Is it needed?" asks for intent, which the program never records, while "is it reachable from a root" is a graph walk with a decidable answer. The engine can always run it — including when the answer wrongly keeps a useless object alive.

2. **Q:** What does reference counting get wrong that mark-and-sweep gets right?
   **A:** Plain reference counting cannot reclaim an isolated cycle because its internal references keep counts positive. Tracing can identify the island as unreachable; reference-counting systems can also add cycle detection, and actual reclamation timing is policy-dependent.

**Definition**

3. **Q:** What does "generational" mean for a garbage collector?
   **A:** Objects are bucketed by age — a small young generation swept often and cheaply, a large old one swept rarely — based on the empirical observation that most allocations die almost immediately.

**How It Works**

4. **Q:** What happens in a scavenge, and what is promotion?
   **A:** In a copying young collector, reachable survivors move into available survivor/old storage; promotion makes an object old-generation data. This is one collector strategy, not a guarantee that every young collection copies every survivor or uses a fixed age threshold.

5. **Q:** How do incremental and concurrent marking reduce jank?
   **A:** Incremental marking interleaves portions of collection with application work; concurrent marking performs supported work alongside the application. Remaining pauses and synchronization depend on the collector/workload, so neither guarantees only short begin/end pauses.

**Common Mistakes**

6. **Q:** Why is `data = null` inside a short function pointless, and when does that same line matter?
   **A:** The local binding dies with the scope either way, so there is no pin to release. It only does something for a binding that outlives its usefulness — module scope, a cache closure, a long-lived object property.

**Best Practices**

7. **Q:** When do you reach for `WeakRef` instead of `WeakMap`?
   **A:** When you need a non-owning handle rather than metadata associated with a key. `deref()` may return `undefined` after collection; if it returns an object, that target remains retained through the current job. Do not use weak references for correctness-critical ownership.

**Performance Considerations**

8. **Q:** What does allocation rate actually control?
   **A:** Allocation contributes to heap pressure and collection work, alongside live size, object kinds and engine policy. Hot-loop allocation can cause pauses, but measured traces must establish whether it causes the observed frame drops.

## Hash Tables & HashMaps — Internals, Collision Resolution & V8

Source: [Hash Tables & HashMaps — Internals, Collision Resolution & V8](10.1.4.08-hash-tables-internals.md)

**First Principles**

1. **Q:** Why can a hash table never promise worst-case O(1) the way an array does?
   **A:** Direct indexing already has a bounded integer position. A hash table maps many possible keys to fewer candidate positions and must compare full keys to resolve collisions; growth can also move all entries. The examples provide expected/amortized, not per-operation worst-case constant bounds.

2. **Q:** What does "amortized" buy you that a worst-case claim wouldn't?
   **A:** Over a sequence of n inserts the rehashes cost 1 + 2 + 4 + … + n ≤ 2n, so the rare O(n) spike averages to a constant per insert — O(1) per op even though one op can still hitch.

**Definition**

3. **Q:** What is the load factor, and why do chaining and open addressing draw the line in different places?
   **A:** α = entries ÷ slots. Chaining can store multiple entries per bucket and exceed one; open addressing stores entries in the slots and needs insertion space. Its growth policy also accounts for probe distribution and tombstones; example thresholds are not universal.

**Follow a key from hash to stored entry**

4. **Q:** Two implementations both report "α = 0.5", but one still feels slow. Why?
   **A:** Load describes occupancy, not a bound on probes. Poor key distribution, clusters, tombstones or long string hashing can make a half-full table slow. Investigate the actual operation mix and collision paths.

**When keys collide, storage strategy matters**

5. **Q:** Why does linear probing collapse at high load while chaining only degrades gently?
   **A:** Occupied runs attract more displaced entries in linear probing, and a miss must traverse the run before finding an empty slot. Chaining searches the selected bucket without needing a vacancy in the main array. These are qualitative mechanisms, not measurements performed by this chapter.

**Separate JavaScript key rules from V8's implementation choices**

6. **Q:** How does V8's `Map`/`Set` actually resolve collisions, and how full does it let the table get?
   **A:** Current V8 source links bucket entries to ordered data entries and tracks deleted entries. Its table representation provides two data-entry slots per bucket; that is not a `Map` API load threshold, and growth/compaction remain version-specific.

7. **Q:** What hash does V8 use for a key, and why does that choice matter?
   **A:** ECMAScript specifies `Map` key equality with SameValueZero, not a hash algorithm. V8 uses internal hashes for ordered tables, but their algorithms and storage can change; do not rely on an assumed randomization scheme as a defense against hostile keys.

**Common Mistakes**

8. **Q:** Why is a plain object a poor stand-in for an insertion-ordered map?
   **A:** Integer-like keys are hoisted first and sorted ascending, then string keys follow in insertion order — so `{2:…, 1:…, b:…}` iterates as `1, 2, b`. Use `Map` when the order must be exact.

## Equality & Type Coercion

Source: [Equality & Type Coercion](10.1.4.09-equality-and-coercion.md)

**First Principles**

1. **Q:** If `===` exists, why does JavaScript still ship loose equality at all?
   **A:** Loose equality is an existing language contract retained for compatibility and deliberate type-dependent comparisons. It is not general input validation: boundary data still needs an explicit parsing/range policy before comparison.

2. **Q:** How can `[]` be truthy at the same time as `[] == false` being `true`?
   **A:** They answer different questions with different rule sets: a boolean context treats ordinary objects as truthy (the legacy browser `document.all` is exceptional), while `==` with a boolean operand runs ToNumber and lands both sides on `0`.

**Definition**

3. **Q:** What is type coercion, and which JavaScript constructs trigger it?
   **A:** Automatic conversion of a value into another primitive type, triggered by comparison operators, arithmetic operators, and boolean contexts — each carrying its own conversion rules rather than one shared set.

**How It Works**

4. **Q:** In what order does an object become a primitive?
   **A:** A supplied `Symbol.toPrimitive` handles the hint and must return a primitive. Otherwise ordinary number-hint conversion tries `valueOf` then `toString`; string-hint conversion reverses them. Dates customize default-hint behavior. Failed conversion throws.

5. **Q:** How does `+` decide between concatenation and addition?
   **A:** It converts operands to primitives and concatenates if either result is a string. Otherwise it applies numeric conversion: two Numbers add, two BigInts add, and mixing Number with BigInt throws. Thus `1 + '2'` is `"12"`, but `1n + 1` is an error.

**Code Examples**

6. **Q:** Why does `null == 0` evaluate to `false` while `null >= 0` evaluates to `true`?
   **A:** `==` carries an explicit carve-out that admits only `undefined` alongside `null`, whereas `>=` has no such exception and converts `null` to `0` — one value, two algorithms, opposite answers.

**Common Mistakes**

7. **Q:** Why does `v || 50` misbehave when `0` is a legitimate value?
   **A:** `||` treats every falsy value as a trigger — `0`, `''`, `false`, `NaN` — while `??` is limited to `null` and `undefined`, so any default that may legitimately be zero must use `??`.

**Best Practices**

8. **Q:** When is `==` the correct choice rather than a lapse?
   **A:** The nullish idioms deliberately collapse `null` and `undefined`. A different loose comparison is defensible only when its documented operand types and conversion behavior are the intended contract; strict comparison plus explicit parsing is usually clearer.

## Changed conditions

Sources: [Copying](10.1.4.03-shallow-vs-deep-copy.md), [Throttle](10.1.4.05-throttle.md), [GC](10.1.4.07-garbage-collection.md), [Hash tables](10.1.4.08-hash-tables-internals.md).

**Q:** If two original properties refer to one child and that child refers back to the root, what relationships must a supported deep clone retain?
**A:** Both copied properties refer to one cloned child, and its back-reference reaches the cloned root. The clone separates the original graph while preserving relationships inside the new graph.

**Q:** A throttle runs a trailing callback at 100ms, then receives an event at 101ms. What is the next ordinary execution time for a 100ms limit?
**A:** No earlier than about 200ms. The trailing execution resets actual execution spacing; flush can explicitly override the ordinary policy.

**Q:** Why can a young-generation collector not ignore references written by old objects?
**A:** An old object may be the only path to a young object that must survive. Write-barrier bookkeeping records those paths so a young-region collection can find them without rescanning every old object.

**Q:** Why must inserting into a deleted probe slot first check farther slots for the key?
**A:** The key may already exist later in the same probe path. Remember the tombstone, scan for an update, then reuse it only when the key is absent; otherwise insertion creates a duplicate.

## Ownership and conversion boundaries

Sources: [Copying](10.1.4.03-shallow-vs-deep-copy.md), [Debounce](10.1.4.04-debounce.md), [Coercion](10.1.4.09-equality-and-coercion.md).

**Q:** Does structured cloning a SharedArrayBuffer create isolated bytes?
**A:** No. The cloned wrapper accesses the same shared memory. Transfer of an ordinary ArrayBuffer is different: it moves ownership and detaches the original buffer.

**Q:** A search request is active when the input changes, but the replacement waits for debounce. When must the old result lose publication authority?
**A:** Immediately on the input change. Cancel/invalidate the old generation then, rather than waiting for the next request to start; otherwise an old response can publish during the quiet-time gap.

**Q:** Why must an undo history clone the new snapshot before removing redo entries?
**A:** Cloning can throw for unsupported data. Preparing the snapshot first preserves the existing history on failure instead of partly applying the update.

**Q:** What does Boolean('false') mean for a URL feature flag?
**A:** It means true because the string is nonempty. A textual flag needs an explicit accepted-spelling policy, with invalid values handled deliberately.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
