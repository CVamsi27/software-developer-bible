<!-- section: React | category: Reference | tags: revision, retrieval-practice | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-React-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-8_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Advanced Hooks & Patterns — React — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Suspense

Source: [Suspense](10.3.3.01-suspense.md)

**Q:** What does React do when a supported read cannot finish during render?

**A:** The nearest `<Suspense>` boundary can show its fallback for that region and retry when the resource settles. Already revealed content may remain visible during a transition, and render attempts can repeat; boundary placement controls reveal scope, not an exact invocation count.

**Q:** Does a Suspense boundary make the whole app wait, or only part of it?

**A:** Only the subtree inside it. Sibling boundaries and content above it render immediately, which is why the granularity of boundaries — not Suspense itself — decides which regions block which.

**Q:** Which work can activate Suspense besides a `React.lazy` component?

**A:** A Promise read with `use` or by a Suspense-enabled data source can suspend; streaming server rendering and selective hydration also integrate with boundaries. A library must own a stable Promise/cache, because Suspense does not cache arbitrary requests.

**Q:** What happens when a lazy child suspends but has no nearby boundary?

**A:** The nearest ancestor boundary owns the fallback, so it may replace a much larger region than intended. Add a closer boundary when that feature should load independently.

**Q:** What does reading a stable Promise with `use` change compared with fetching in an Effect?

**A:** The read can suspend during render, so the nearest Suspense boundary handles pending work and an Error Boundary handles rejection. The component's resolved rendering still needs to validate and display its data.

**Q:** Why is a single full-page Suspense wrapper a bad default?

**A:** Every async region then waits on the slowest one — the header spins behind the same fallback as the content. Per-section boundaries let each region show its own fallback and load independently.

**Q:** When is lazy-loading a component not worth the added chunk?

**A:** When the component is small and needed immediately, the separate request and first-use wait may outweigh the initial bundle savings. Measure the build and load path; route-level editors or charts are stronger candidates than tiny shared controls.

**Q:** What does declaring `lazy` at module scope guarantee, and what does it not guarantee?

**A:** It preserves one component type so rerenders do not reset its state. It does not preload the chunk or remove first-use latency; choose a fallback and measure whether preloading is needed.

## Error Boundary

Source: [Error Boundary](10.3.3.02-error-boundary.md)

**Q:** Why can't a plain function component serve as an error boundary?

**A:** The React boundary primitive uses class lifecycle methods: `getDerivedStateFromError` selects fallback state and `componentDidCatch` reports after commit. React has no built-in function Hook equivalent; a third-party library can wrap a class boundary with a Hook-friendly API.

**Q:** Which errors does a boundary catch, and which slip through?

**A:** It handles errors thrown while React renders descendants. Ordinary event handlers, detached async callbacks and server-rendering failures need their own handling. A rejected promise read with `use` and an error from a React 19 `useTransition` Action can reach a boundary; a pending promise belongs to Suspense.

**Q:** What's the difference between `getDerivedStateFromError` and `componentDidCatch`?

**A:** The first is static, runs in the render phase, must be pure, and only returns the state patch that flips the boundary to its fallback; the second is an instance method that runs after commit with `(error, errorInfo)` and is where side effects like reporting belong.

**Q:** What does `errorInfo.componentStack` add to a JavaScript error stack?

**A:** It identifies the React component-tree locations involved in the failed render; it is not the JavaScript call stack. Send it with sanitized error details from `componentDidCatch` so reports identify the failing UI region.

**Q:** What does clearing the boundary's failure state do, and what does it leave untouched?

**A:** It retries rendering the region and remounts its children, losing their local state. It does not invalidate a rejected Promise held in an external cache; the resource owner must provide a fresh value before that retry can succeed.

**Q:** Why does wrapping a throwing `onClick` handler in an ErrorBoundary do nothing?

**A:** Event handlers run outside React's render pass, so the throw never travels up the fiber tree to the boundary — it must be caught with `try/catch` inside the handler.

**Q:** What's wrong with a boundary that only renders "Error occurred"?

**A:** The user is stuck: the failure state remains set with no path back to working UI. A boundary's real value is recovery — clear the error state to retry, or offer navigation — not merely displaying the failure.

**Q:** Where should boundaries sit in a real application?

**A:** Put a boundary around each independently recoverable route, feature or widget, with a higher-level fallback for failures the local boundaries cannot contain. Keep expected form validation in form state so a bad field does not discard the whole draft.

**Q:** Why can a retry button immediately return to the fallback when Suspense data failed?

**A:** Clearing the boundary does not replace a cached rejected resource. Reset or invalidate that resource through its owner before retrying; a persistent render bug needs a different recovery path.

**Q:** Why does the example store a boolean failure flag rather than treating the caught value as an Error?

**A:** JavaScript can throw a string or even null. A truthiness check on the thrown value can miss the failure; an explicit flag selects the fallback while the unknown value goes to a safe reporting adapter.

## Custom Hooks

Source: [Custom Hooks](10.3.3.03-custom-hooks.md)

**Q:** What does a custom Hook reuse, and what does each call own?

**A:** It reuses the Hook logic. State remains associated with the component instance making the call, so two components calling `useDebouncedValue` have separate values and timers. Shared state needs a shared owner such as a parent, Context provider, or external store.

**Q:** Why must a custom Hook call its Hooks at the top level?

**A:** React associates Hook state with the order of calls during a component render. A conditional or loop can change that order between renders, pairing state with the wrong call or producing a Hook-order error. The Rules of Hooks linter checks this constraint.

**Q:** When is a normal function clearer than a custom Hook?

**A:** A pure calculation such as `value * 2` has no component state, effect, or subscription to organize, so a normal function is enough. Extract a Hook when its name and return value make a repeated stateful behavior easier to understand or reuse.

**Q:** Why does `useDebouncedValue` clear its timer in Effect cleanup?

**A:** When the input or delay changes, cleanup cancels the earlier timer before scheduling the next one. Without that cleanup, an older timer could publish an obsolete value after a newer input.

**Q:** What does passing TanStack Query's `signal` to `fetch` establish?

**A:** It lets TanStack Query abort an obsolete request when the query becomes out of date or inactive. The debounced value reduces how often a query key changes; the signal handles cancellation; neither replaces server-side validation, authorization, or rate limiting.

**Q:** What does the fake-timer test for `useDebouncedValue` prove, and what does it leave unproven?

**A:** It proves the published value stays old until the delay expires and that the latest scheduled value wins. It does not prove HTTP cancellation, caching, response validation, or server behavior; those belong to separate query and API tests.

**Q:** When is React 19.2's `useEffectEvent` appropriate for a subscription?

**A:** Use it when logic called from an Effect needs the latest committed values but those values should not restart the subscription. Keep values that should trigger resynchronization in the Effect dependencies; an Effect Event cannot be passed to a child or used as a general event handler.

**Q:** Why should an Effect dependency remain when changing it requires a new subscription or request?

**A:** That value is part of the external system's synchronization contract. Removing it can leave the Effect connected to stale inputs. `useEffectEvent` is for non-reactive logic called by an Effect, not a way to suppress a dependency that should restart the work.

## useSyncExternalStore

Source: [useSyncExternalStore](10.3.3.04-usesyncexternalstore.md)

**Q:** What is "tearing", and why does interruptible rendering make it possible?

**A:** One committed frame showing *different values of the same external state* in different components. React can pause a render mid-tree for higher-priority input; if the store changes during that pause, components rendered before it keep the old value while resumed components read the new one — two truths in a single frame.

**Q:** Why not just bridge a store with `useState` + `useEffect`?

**A:** A naive bridge can miss a change between reading the source and attaching its listener, and can commit inconsistent values during concurrent rendering. React rechecks external snapshots around subscription and concurrent commit; attachment before paint is not the guarantee.

**Q:** What is the `getSnapshot` contract, and what happens when it's broken?

**A:** It must be pure and return a *cached* reference — same data ⇒ same object. A fresh object per call makes React's `Object.is` check report "changed" on every render, which triggers another render, which produces another fresh object: an infinite loop, plus the warning *"The result of getSnapshot should be cached to avoid an infinite loop."*

**Q:** What is `getServerSnapshot` for, and when does React stop using it?

**A:** It's what the server render *and* the hydration render read so the markup matches; after hydration, with the subscription attached, React reads `getSnapshot`. Returning a client-only value (e.g. from `localStorage`) as the server snapshot causes a hydration mismatch.

**Q:** How should a browser-only snapshot behave during server rendering and hydration?

**A:** Use an explicit neutral value from `getServerSnapshot` on both the server and the initial client render, then let the subscription reconcile the browser value. Reading browser globals as server data can produce a hydration mismatch.

**Q:** Why must the counter update its stored value before notifying listeners?

**A:** Listeners re-read the snapshot synchronously when notified. If notification happens first, they read the old value; identical snapshots should return early without waking subscribers.

**Q:** Why does returning `() => ({ id: user.id })` directly as `getSnapshot` loop, and how should a binding handle that selection?

**A:** It builds a new object on every read, so `Object.is` never sees equality. Cache the snapshot at the source, return an existing immutable record, or use the selector and equality API supported by the store binding; a selector-aware adapter can reuse a derived object when its selected fields are unchanged.

**Q:** When is this hook a better fit than an Effect bridge?

**A:** Use it when React must read a synchronous external snapshot consistently, such as a store or browser value with a change event. An Effect can remain simpler when it synchronizes one resource or moves asynchronous results into React-owned state. The Hook does not promise pre-paint subscription attachment.

## React Performance Optimization

Source: [React Performance Optimization](10.3.3.05-performance.md)

**Q:** Which evidence separates expensive React rendering from browser layout and paint work?

**A:** The React Profiler shows which components rendered and how much React work they did. A browser Performance trace exposes long tasks, DOM updates, layout and paint. Use the tool that measures the stage users are waiting on.

**Q:** Why is "reduce the work, don't memoize it" the right first instinct?

**A:** Memoization only caches work you still perform, and it adds comparison and bookkeeping overhead to every render. Deleting the work — fewer rows in the DOM via virtualization, fewer bytes via code splitting, fewer components re-rendering via colocation — removes cost outright instead of relocating it.

**Q:** Why can a fresh products array prevent the result subtree from skipping an urgent render?

**A:** `memo` compares each prop with `Object.is` by default. A new array reference counts as changed even if its entries look the same; state or Context consumed by the child can also render it.

**Q:** What does the Updating results status in ProductSearch communicate?

**A:** `useDeferredValue(query)` can lag behind the input while the result subtree renders, so `query !== deferredQuery` means the visible list still matches an older query. The status paragraph makes that delay explicit instead of presenting retained results as the final response to the newest input.

**Q:** What do stable keys preserve in a virtualized list, and what problem remains?

**A:** A domain key preserves record identity when rows move or return, but virtualization can still unmount the focused row. The interface needs an explicit focus and keyboard-navigation policy.

**Q:** Can `useMemo` interrupt one expensive calculation when its inputs change?

**A:** No. It may reuse a result when dependencies are unchanged, but the first calculation and a new-input calculation still run synchronously. Reduce the data, move suitable work to a worker, or query an indexed service.

**Q:** When does wrapping a tiny handler in `useCallback` actually hurt?

**A:** When no identity-sensitive consumer uses its stable reference, the cache adds bookkeeping without skipping useful work. Effects, providers and custom Hook APIs can also supply legitimate consumers besides memoized children.

**Q:** What evidence should you collect before adding a memo layer?

**A:** Profile the real interaction, separate React work from browser work, and choose the lever that addresses the measured cost. Compare the same workload after the change; unmeasured memoization may only move the bottleneck.

## State Management

Source: [State Management](10.3.3.06-state-management.md)

**Q:** Why does remote data need more than a global client-state container?

**A:** The remote owner can change data without a local event, so cached copies need freshness, requests, invalidation and retry policies. A plain client store can hold that data but does not provide those policies automatically. TanStack Query manages the request/cache lifecycle; application-specific optimistic rollback still needs an explicit policy.

**Q:** What is the selector model, and why is it "the performance contract"?

**A:** A binding reads a selected slice and compares it with the previous selected value. An unchanged slice can suppress a store-triggered render; the component can still render from its parent, local state or context. Immutable normalized data and focused selectors help unchanged slices retain identity.

**Q:** When can one broad context value cause costly updates?

**A:** When the provider's value changes by `Object.is`, every component reading that context receives the new value, even if it uses only one field. Context does not provide field selectors. Split independently changing values or use selector-based subscriptions when profiling shows this update boundary is costly. A reducer plus context can still handle complex state; frequency alone is not a prohibition.

**Q:** What actually distinguishes server state from client state?

**A:** Ownership and timing. Server state arrives asynchronously with loading/error and can be invalidated externally, so it needs cache/revalidate/retry semantics; client state is owned by the application; React schedules its local updates, and persistence is optional.

**Q:** Why does the mutation example show pending text as an independent UI overlay instead of patching the query cache?

**A:** The confirmed cache remains untouched while the request is pending, so a rollback cannot restore an old snapshot over a newer mutation. Mutation variables drive the temporary row label; the server's accepted response updates the cache, and conflicts require a deliberate rebase.

**Q:** How can a selector reduce store-driven renders without preventing every render?

**A:** It compares only the selected slice and can ignore an unrelated store update. The component may still render because of its parent, local state or Context.

**Q:** What shape keeps a large client-owned relational collection normalized?

**A:** Keep one record per ID in a lookup table and a separate ordered ID list. This avoids duplicate entities and supports direct lookup; remote records should remain with their query-cache owner.

**Q:** State appears and the team asks "where does it go?" — give the decision rule.

**A:** Component-only → `useState`/`useReducer`; shared by siblings → lift to the common ancestor; shared provider values → Context; independently selected external state or action tooling → a suitable store; remote copies needing freshness/invalidation → a server-state cache; shareable filters → validated URL state. Frequency and complexity are considerations rather than rigid library boundaries.

## TanStack Query — Server State Ownership

Source: [TanStack Query: Server State Ownership](10.3.3.07-tanstack-query.md)

**Q:** Why can concurrent observers of the same key share a request, while a list and detail disagree?

**A:** The same QueryClient coordinates an in-flight fetch for that key. List and detail keys own independent result objects; TanStack Query does not automatically normalize their shared entities. Update or invalidate every affected result explicitly.

**Q:** What happens if an optimistic update succeeds in the UI but the server rejects the mutation?

**A:** The application must implement its `onError` reconciliation. A saved snapshot can restore an isolated edit, but blindly restoring it can erase a later concurrent optimistic edit. Keep one write owner or use pending variables/version-aware patches.

**Q:** Does passing a stale-time deadline start a background request?

**A:** It changes freshness. Mount, focus, reconnect, explicit invalidation/refetch or a separately configured polling interval supplies the trigger. Test an idle query to avoid confusing staleness with polling.

**Q:** Why must `staleTime` agree between server (`dehydrate`) and client hydration?

**A:** Exact agreement is not required. Choose freshness to avoid an unwanted immediate refetch, and use matching query keys and request-scoped clients. A stale-time difference alone does not prove a React markup mismatch; the rendered content must be checked separately.

**Q:** Which API restores dehydrated state, and what protects an HTML script boundary?

**A:** React uses HydrationBoundary; core clients can use hydrate. Dehydration returns state, not an automatic HTML-safe serialization. Use the framework's safe transport and do not interpolate untrusted raw JSON into a script.

**Q:** Why can invalidating a query leave the network idle?

**A:** Invalidation marks matching results stale. By default it refetches active queries; inactive results can wait for a later observer. Disabled queries and stricter policies also require their documented handling.

**Q:** A clinician switches clinics while a detail request is pending. What does a tenant key solve?

**A:** Including tenant identity separates cached results and query work. It does not authorize access: the API must verify the caller's tenant/resource rights, and sign-out/account changes need an explicit cache-clearing policy.

## Ownership under changed conditions

Source: [Custom Hooks](10.3.3.03-custom-hooks.md), [Suspense](10.3.3.01-suspense.md), [External stores](10.3.3.04-usesyncexternalstore.md), [State management](10.3.3.06-state-management.md)

**Q:** A parent renders again with the same pending promise. Is that another network request?

**A:** Not from the read itself. The stable promise owner controls creation; the read remains pending until that resource settles.

**Q:** Why does returning a new lazy component type on every render reset more than loading UI?

**A:** React sees a different component identity, so retained local state can be lost and work restarted. Declare lazy types outside rendering.

**Q:** What remains independent when two components call useCounter?

**A:** Each caller owns distinct Hook records and counts. Reusing the implementation shares logic, not storage.

**Q:** Why must every debounced-value call own and clear its own timer?

**A:** Each caller has a separate value and lifecycle. A shared timer could cancel another caller's work, while missing cleanup lets an obsolete value publish after the input changes or the caller unmounts. Every entry point must preserve that ownership contract.

**Q:** Does navigator.onLine establish that an authenticated API request will succeed?

**A:** No. It is a browser connectivity hint; DNS, service health, authorization or a particular route can still fail.

**Q:** Does an optimistic rollback always restore the correct displayed state?

**A:** Only with a valid operation-ownership policy. Restoring an old snapshot after a newer patch can erase that patch; independent overlays or versioned patches avoid that blind restoration.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
