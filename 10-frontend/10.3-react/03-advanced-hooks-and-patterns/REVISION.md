<!-- section: React | category: Reference | tags: revision, retrieval-practice| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-7_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Advanced Hooks & Patterns — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Suspense

Source: [Suspense](10.3.3.01-suspense.md)

**How It Works**

1. **Q:** What physically happens when a component suspends?
   **A:** The component throws a promise during render; React catches it at the nearest `<Suspense>` boundary above, renders that boundary's fallback instead of the subtree, and re-renders the real UI once the promise resolves — everything outside the boundary keeps rendering untouched.

2. **Q:** Does a Suspense boundary make the whole app wait, or only part of it?
   **A:** Only the subtree inside it. Sibling boundaries and content above it render immediately, which is why the granularity of boundaries — not Suspense itself — decides which regions block which.

3. **Q:** Which React features does Suspense sit underneath besides `React.lazy`?
   **A:** Data fetching (React Query/Relay suspense modes, `use(promise)` in React 19), streaming server-rendered HTML, and selective hydration of urgent components — all reuse the same throw-a-promise-and-show-a-fallback mechanism.

**Code Examples**

4. **Q:** What is lost when a lazy component has no Suspense wrapper?
   **A:** A lazy component can suspend while its chunk loads. Without an explicit boundary a concurrent root can wait without intentional loading UI; a boundary defines what the user sees during that wait.

5. **Q:** What does reading a stable promise with `use` give you that the effect-based version does not?
   **A:** The loading/error branches move out of the component: `use` reads the promise in render and suspends, so the component only ever renders real UI while the Suspense (and Error) boundary above owns the spinner and failure states.

**Common Mistakes**

6. **Q:** Why is a single full-page Suspense wrapper a bad default?
   **A:** Every async region then waits on the slowest one — the header spins behind the same fallback as the content. Per-section boundaries let each region show its own fallback and load independently.

7. **Q:** When is lazy-loading a component *not* worth it?
   **A:** When it's small and needed immediately — a 1KB button or icon costs a chunk request and a fallback flash that outweigh the bytes saved. Split only large, on-demand pieces: routes, editors, charts, modals.

**Best Practices**

8. **Q:** What hides the extra network round-trip that code splitting introduces?
   **A:** Preloading — start the dynamic import before the user navigates (e.g., on hover) so the Suspense fallback shows for milliseconds instead of the full download; without it, first visits to a split route pay the 100-200ms chunk fetch.

## Error Boundary

Source: [Error Boundary](10.3.3.02-error-boundary.md)

**Definition**

1. **Q:** Why can't a plain function component serve as an error boundary?
   **A:** Catching a child's throw requires React to invoke lifecycle methods *on the boundary itself* — `getDerivedStateFromError` during render and `componentDidCatch` after commit — and function components have neither; React ships no hook equivalent (the `useErrorBoundary` hook people cite comes from the third-party `react-error-boundary` library).

2. **Q:** Which errors does a boundary catch, and which slip through?
   **A:** It catches anything thrown while React renders its children: render bodies, lifecycle methods, child constructors. Ordinary event handlers and detached async callbacks need local error handling. React 19 transition Action failures and rejected promises read with `use` can reach a boundary; server rendering and a boundary's own fallback errors have different handling.

**How It Works**

3. **Q:** What's the difference between `getDerivedStateFromError` and `componentDidCatch`?
   **A:** The first is static, runs in the render phase, must be pure, and only returns the state patch that flips the boundary to its fallback; the second is an instance method that runs after commit with `(error, errorInfo)` and is where side effects like reporting belong.

4. **Q:** What is `errorInfo.componentStack` and where do you use it?
   **A:** The chain of component instances that led to the throw — React's equivalent of a stack trace. You log it inside `componentDidCatch` so your error service can point at the failing component, not just the message.

**Code Examples**

5. **Q:** How does the "Try again" button in the retry examples actually recover?
   **A:** It calls `setState` to flip `hasError` back to `false`, so React re-renders the children from scratch — the subtree remounts and a transient failure (flaky fetch, bad intermediate state) can succeed; a persistent bug simply throws again and the fallback returns.

**Common Mistakes**

6. **Q:** Why does wrapping a throwing `onClick` handler in an ErrorBoundary do nothing?
   **A:** Event handlers run outside React's render pass, so the throw never travels up the fiber tree to the boundary — it must be caught with `try/catch` inside the handler.

7. **Q:** What's wrong with a boundary that only renders "Error occurred"?
   **A:** The user is stuck: `hasError` stays `true` with no path back to working UI. A boundary's real value is recovery — clear the error state to retry, or offer navigation — not merely displaying the failure.

**Best Practices**

8. **Q:** Where should boundaries sit in a real application?
   **A:** One per independent failure domain — route, widget, form, feature — nested inside a top-level catch-all, each with its own fallback, so a crash degrades one region instead of blanking the app; a single app-wide boundary is only a last resort.

## Custom Hooks

Source: [Custom Hooks](10.3.3.03-custom-hooks.md)

**First Principles**

1. **Q:** What connects extracted stateful logic to React's render lifecycle?
   **A:** JavaScript functions can maintain closure or module state. A custom hook specifically calls React Hooks during a component render, which ties its state and effects to that caller's Hook records and cleanup lifecycle. Each independent caller receives its own records.

2. **Q:** How do custom hooks escape "wrapper hell" where HOCs and render props don't?
   **A:** They share the logic without inserting nodes into the component tree: the caller receives return values instead of a wrapped component, so the hierarchy in JSX and DevTools stays exactly what you wrote — no nesting, no prop-injection collisions, no renamed `displayName`.

3. **Q:** Why does extraction also create a test boundary?
   **A:** `renderHook` mounts a small harness that calls the hook, allowing direct assertions on its returned behavior. It isolates reusable logic from markup; component tests still verify that UI interactions use the hook correctly, and provider-dependent hooks need an appropriate wrapper.

**How It Works**

4. **Q:** What does the `use` prefix actually buy you?
   **A:** The prefix followed by an uppercase letter or digit tells tooling and readers that callers must follow the Hook rules. Runtime access still depends on React's active dispatcher and stable Hook ordering; renaming a function cannot bypass those checks.

5. **Q:** Is state shared between two components that call the same `useCounter`?
   **A:** No. The hook function is ordinary module-scope code; each call site gets its own `useState` slot, so state is isolated per component instance — that isolation is what lets you drop the same hook anywhere without cross-talk.

**Code Examples**

6. **Q:** Why does `useDebounce` return `clearTimeout(timer)` from its effect?
   **A:** Every new `value` re-runs the effect; without the cleanup the previous timer would still fire and commit a stale value after a newer one. Clearing guarantees only the final change's timer survives, so rapid typing settles on the last query.

7. **Q:** Why keep fetch options as dependencies but an event handler in a committed ref?
   **A:** A URL or request-option change should cancel the old request and start a new one, so use stable options and list them as dependencies. A handler change can update what an existing event listener calls without reinstalling that listener; updating the handler ref after commit separates callback behavior from subscription lifetime.

**Common Mistakes**

8. **Q:** Why is a `useDouble` built on `useState` + `useEffect` a worse hook than `value * 2`?
   **A:** Storing a derived product in state renders once with the old derived value, then schedules another render from the effect. Compute the product during render. A custom hook is useful when it organizes reusable Hook behavior; a pure helper is sufficient for arithmetic alone.

## useSyncExternalStore

Source: [useSyncExternalStore](10.3.3.04-usesyncexternalstore.md)

**First Principles**

1. **Q:** What is "tearing", and why does interruptible rendering make it possible?
   **A:** One committed frame showing *different values of the same external state* in different components. React can pause a render mid-tree for higher-priority input; if the store changes during that pause, components rendered before it keep the old value while resumed components read the new one — two truths in a single frame.

2. **Q:** Why not just bridge a store with `useState` + `useEffect`?
   **A:** A naive bridge can miss a change between reading the source and attaching its listener, and can commit inconsistent values during concurrent rendering. React rechecks external snapshots around subscription and concurrent commit; attachment before paint is not the guarantee.

**How It Works**

3. **Q:** What is the `getSnapshot` contract, and what happens when it's broken?
   **A:** It must be pure and return a *cached* reference — same data ⇒ same object. A fresh object per call makes React's `Object.is` check report "changed" on every render, which triggers another render, which produces another fresh object: an infinite loop, plus the warning *"The result of getSnapshot should be cached to avoid an infinite loop."*

4. **Q:** What is `getServerSnapshot` for, and when does React stop using it?
   **A:** It's what the server render *and* the hydration render read so the markup matches; after hydration, with the subscription attached, React reads `getSnapshot`. Returning a client-only value (e.g. from `localStorage`) as the server snapshot causes a hydration mismatch.

**Code Examples**

5. **Q:** In the viewport hook, where does referential stability come from?
   **A:** The getter retains its cached object while dimensions match. The shared resize handler refreshes it and notifies every subscriber; React suppresses a resulting render when the selected snapshot is unchanged.

6. **Q:** Why does the hand-rolled store assign `state = next` *before* notifying listeners?
   **A:** Listeners synchronously re-read the snapshot when notified; notifying first would make them read the stale value and conclude nothing changed. The `Object.is` bail-out before the swap also keeps identical updates from waking subscribers at all.

**Common Mistakes**

7. **Q:** Why does an inline selector like `() => ({ id: user.id })` loop forever, and what's the fix?
   **A:** It builds a new object on every poll, so `Object.is` never sees equality. Fix it by caching at the source (rebuild only when the underlying data changes) or by using `useSyncExternalStoreWithSelector` with an equality function such as `shallowEqual` — the selector shim used by Zustand's traditional equality-enabled bindings.

**Best Practices**

8. **Q:** When should you reach for this hook instead of an effect?
   **A:** Whenever the source looks like "events + a current-value getter" — `matchMedia`, online status, sockets, `store.getState()`. React checks snapshot consistency around subscription and concurrent commit and supports a matching server snapshot. External-store mutations may force a transition to restart as blocking work; pre-paint subscription setup is not the contract.

## React Performance Optimization

Source: [React Performance Optimization](10.3.3.05-performance.md)

**First Principles**

1. **Q:** What two distinct diseases does a flamegraph let you tell apart, and why does it matter?
   **A:** *Too-wide* renders — many components re-rendering (cure: memoization, state colocation) vs. *too-expensive* commits — heavy DOM churn (cure: virtualization, fewer nodes). Treating DOM churn with `React.memo` does nothing, because the components doing the rendering were never the bottleneck.

2. **Q:** Why is "reduce the work, don't memoize it" the right first instinct?
   **A:** Memoization only caches work you still perform, and it adds comparison and bookkeeping overhead to every render. Deleting the work — fewer rows in the DOM via virtualization, fewer bytes via code splitting, fewer components re-rendering via colocation — removes cost outright instead of relocating it.

**Code Examples**

3. **Q:** In the `React.memo` example, why do `data` and `onClick` need `useState`/`useCallback` for the memo to bite?
   **A:** `memo` compares props shallowly with `Object.is`; an inline object or a re-created function is a fresh reference on every parent render, so the comparison always fails. Stabilizing both props is what lets the comparison succeed and skip the child's render.

4. **Q:** What is the dimmed list in `SearchBox` communicating to the user?
   **A:** `useDeferredValue(query)` lags behind the input while the heavy filter re-renders, so `query !== deferredQuery` means the visible list still matches an older query. Dropping its opacity tells the user "these results are behind your typing" instead of letting stale results look final or the UI look frozen.

**Common Mistakes**

5. **Q:** Why can deleting an index-keyed row transfer state to the wrong record?
   **A:** React reuses positions whose index keys match, potentially assigning an old row's state to a different record after deletion. Stable domain keys preserve the intended row identities.

6. **Q:** Why doesn't `useMemo` let 1,000 chart instances compute a value once?
   **A:** The cache lives in each instance's hook slots, so 1,000 instances mean 1,000 independent caches. Cross-instance sharing requires something outside the component — a module-level LRU or an external cache like TanStack Query.

**Best Practices**

7. **Q:** When does wrapping a tiny handler in `useCallback` actually hurt?
   **A:** When no identity-sensitive consumer uses its stable reference, the cache adds bookkeeping without skipping useful work. Effects, providers and custom Hook APIs can also supply legitimate consumers besides memoized children.

8. **Q:** What is the correct order of operations before adding a memo layer?
   **A:** Record a DevTools Profiler flamegraph of the real interaction, confirm whether render width or DOM work dominates, then apply the matching lever — memo for wide renders, virtualization for big trees, splitting for load. Unmeasured memoization only moves the bottleneck.

## State Management

Source: [State Management](10.3.3.06-state-management.md)

**First Principles**

1. **Q:** Why does remote data need more than a global client-state container?
   **A:** The remote owner can change data without a local event, so cached copies need freshness, requests, invalidation and retry policies. A plain client store can hold that data but does not provide those policies automatically. TanStack Query manages the request/cache lifecycle; application-specific optimistic rollback still needs an explicit policy.

2. **Q:** What is the selector model, and why is it "the performance contract"?
   **A:** A binding reads a selected slice and compares it with the previous selected value. An unchanged slice can suppress a store-triggered render; the component can still render from its parent, local state or context. Immutable normalized data and focused selectors help unchanged slices retain identity.

**How It Works**

3. **Q:** When can one broad context value cause costly updates?
   **A:** Context has no selectors — any change to the provider's value re-renders every consumer, even one that reads a different field — and it offers no middleware, devtools, or time-travel. Split independent context values or use selector-based subscriptions when broad consumer updates are costly. A reducer plus context can still handle complex state; frequency alone is not a prohibition.

4. **Q:** What actually distinguishes server state from client state?
   **A:** Ownership and timing. Server state arrives asynchronously with loading/error and can be invalidated externally, so it needs cache/revalidate/retry semantics; client state is owned by the application; React schedules its local updates, and persistence is optional.

**Code Examples**

5. **Q:** Why do all three steps in the optimistic-toggle mutation — cancel, snapshot, rollback — exist?
   **A:** `cancelQueries` stops an in-flight refetch from overwriting the patch; the `previous` snapshot returned from `onMutate` lets `onError` restore the exact prior list when the PATCH fails; `onSettled` revalidates either way so the cache converges on server truth.

6. **Q:** Why does the Zustand example subscribe to `state.todos` and `state.addTodo` separately?
   **A:** Each `useTodoStore(selector)` call compares its selected value to decide whether that store update requires a render. Selecting the whole store — or returning an inline-built object — would wake the component on every write, defeating the selector contract from First Principles.

**Common Mistakes**

7. **Q:** Why does normalization matter more as the app grows?
   **A:** Nested copies mean one entity update rebuilds every ancestor path, and duplicates drift out of sync; a flat `byId`/`allIds` map updates a single key, keeps one source of truth, and makes lookups O(1).

**Best Practices**

8. **Q:** State appears and the team asks "where does it go?" — give the decision rule.
   **A:** Component-only → `useState`/`useReducer`; shared by siblings → lift to the common ancestor; low-frequency app-wide reads → Context; complex high-frequency client logic → Zustand/Redux; anything fetched from an API → React Query; anything shareable via link → the URL.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
