<!-- section: Next.js | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Data & Caching — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Data Fetching Patterns in Next.js (App Router)

Source: [Data Fetching Patterns in Next.js (App Router)](10.4.3.01-data-fetching-patterns.md)

**Definition**

1. **Q:** What separates a server read from an interactive client query?
   **A:** A server read can supply data before browser execution when its inputs are already known. Browser-driven search, polling, and optimistic interactions benefit from a client query cache.


**Reuse and Dependencies**

2. **Q:** Why does adding a fetch tag not necessarily persist its response?
   **A:** Tags label entries for invalidation. In the traditional cache model, choose `force-cache` or a positive `revalidate` to opt into persistent fetch reuse.

3. **Q:** In the traditional cache model, how do React `cache` and `unstable_cache` differ?
   **A:** React `cache` deduplicates helper work within a server render. `unstable_cache` stores supported non-fetch results across requests with a revalidation policy.


**Parallel Work**

4. **Q:** Why can parallelizing queries silently change the requested result?
   **A:** A dependent query needs its original input, such as a product ID. Removing that dependency by changing the query can fetch a different dataset.


**Interactive Reads**

5. **Q:** What does it mean when a Server Component passes a promise to a Client Component using React `use()`?
   **A:** The server starts the read and passes its serializable result across the component boundary. The Client Component reads it under Suspense; this does not make browser-owned live queries server-cached.

6. **Q:** Will `useDeferredValue` guarantee fewer search requests?
   **A:** No. It prioritizes rendering rather than enforcing a time-based debounce; use debouncing/cancellation when controlling query traffic.


7. **Q:** Where should cache invalidation occur relative to a mutation?
   **A:** After the authorized, validated write succeeds and before redirecting to dependent output. Target the routes/tags affected rather than invalidating unrelated data.

## Server Actions in Next.js

Source: [Server Actions in Next.js](10.4.3.02-server-actions.md)

**Definition**

1. **Q:** Why is a server-only action still an externally reachable security boundary?
   **A:** Next creates a client-callable POST interface for it. Keep identity, ownership, and runtime input validation inside the action.


**Form State and Dispatch**

2. **Q:** Which hook now owns returned form state in the React 19 stack?
   **A:** useActionState from react pairs the previous state with the next submission. The older react-dom useFormState API is deprecated.


**Upload and Form Context**

3. **Q:** Why must a useFormStatus submit button be below the form it observes?
   **A:** The hook reads the nearest parent form context. Calling it in the component that creates the form cannot observe that future child form.

4. **Q:** What infrastructure setting must match a form that accepts a five-MiB upload?
   **A:** The Server Action request-body limit must be raised from its default one MiB to a bounded suitable value, or the file should upload directly to storage.


**Failure and Serialization Boundaries**

5. **Q:** Why should redirect be outside a broad action catch block?
   **A:** Redirect throws a framework control-flow signal. A catch can intercept it and incorrectly report a successful redirect as a failed mutation.

6. **Q:** Which returned values prove that React serialization is broader than JSON?
   **A:** Native Date, Map, and Set can be supported values. Ordinary functions and arbitrary class instances still cannot be returned across the boundary.

7. **Q:** Why should independent reads not be dispatched as separate client actions?
   **A:** The Next.js client currently dispatches and awaits Server Functions one at a time. Keep reads in Server Components, or run independent server work together inside one action or Route Handler.

## Caching in Next.js

Source: [Caching in Next.js](10.4.3.03-caching.md)

**Definition**

1. **Q:** Which cache survives longer than one render but stores data rather than HTML?
   **A:** The Data Cache persists reusable reads across requests. Request memoization is shorter-lived, and the Full Route Cache holds rendered route output.


**Refreshing the View**

2. **Q:** Why can router.refresh still display the same old server data?
   **A:** It refreshes the browser's route view without invalidating persistent server data. The new render may read the same cached entry.


**Request Deduplication**

3. **Q:** Which requests does automatic request memoization combine?
   **A:** Identical GET URL/options calls within a React server render. Different endpoints and Route Handler execution are outside that deduplication rule.


**Cache Identity**

4. **Q:** Why does an invalidation tag not isolate two users' cached records?
   **A:** A tag groups entries for refresh, rather than assigning a distinct user key or granting access. Identity-aware keys and authorization are separate requirements.


**Cache Components and Partial Prefetching**

5. **Q:** What must an existing Next.js 16 app configure to use the current Cache Components and Partial Prefetching model?
   **A:** Set both `cacheComponents: true` and `partialPrefetching: true`. Cache reusable functions or components explicitly and place uncached request-time work under Suspense; traditional dynamic/revalidate/fetchCache segment settings are not equivalent controls.

6. **Q:** Which Next.js 16 invalidation choice gives a Server Action read-your-writes behavior?
   **A:** updateTag immediately expires tagged data for that action workflow. revalidateTag with max instead permits stale output while background refresh runs.

## Streaming in Next.js

Source: [Streaming in Next.js](10.4.3.04-streaming.md)

**Definition**

1. **Q:** What can the browser show before every streamed section finishes?
   **A:** The completed shell and the fallbacks of pending subtrees. Each subtree can replace its placeholder when its server work finishes.


**Data Dependencies**

2. **Q:** Does adding three Suspense boundaries remove a sequential data dependency?
   **A:** No. Boundaries control reveal timing; a later read that needs an earlier result still waits for that result.


**Loading Boundaries**

3. **Q:** What does loading.tsx wrap that an arbitrary local fallback may not?
   **A:** It supplies a segment-level Suspense boundary around the page and its descendants beneath the layout. Local boundaries provide more granular reveal inside that route.


**Pending and Failure**

4. **Q:** Must every Suspense boundary have its own error.tsx?
   **A:** No. Suspense handles pending work, while route/custom error boundaries handle failures. A route boundary may cover several Suspense regions.


**Crawler and Layout Boundaries**

5. **Q:** Why can a late not-found result still have HTTP status 200?
   **A:** The shell may already have sent its headers. Perform decisions needing a real status or redirect before streaming begins.

6. **Q:** Why can `loading.tsx` fail to cover a slow request in a layout?
   **A:** It wraps the page and descendants beneath the layout, not the parent layout itself. Put request-time work below the fallback or add a nearer Suspense boundary.


**Performance**

7. **Q:** Why can a quick shell improve first paint without fixing LCP?
   **A:** The largest visible element may still depend on a slow section. Measure its actual arrival and reserve matching placeholder geometry to reduce layout shift.

8. **Q:** What streaming behavior should an HTML-limited crawler expect around metadata?
   **A:** Next.js waits for `generateMetadata` so the crawler receives metadata in the initial head. Page content can still stream after that metadata resolves; DOM-capable crawlers can receive streamed metadata.

## Incremental Static Regeneration (ISR)

Source: [Incremental Static Regeneration (ISR)](10.4.3.05-incremental-static-regeneration.md)

**Definition**

1. **Q:** Who triggers regeneration after a time interval elapses?
   **A:** The next qualifying request, not a timer job. Warm stale output is served while background regeneration proceeds.


**Build and Runtime Boundaries**

2. **Q:** When does a newly visited ID incur render latency?
   **A:** When no page has been generated for it yet. Build-time generation of popular IDs avoids that first-visit cost.


**Invalidation and Cache Lifetimes**

3. **Q:** Does a CMS webhook calling revalidatePath eagerly rebuild the route?
   **A:** No. A Route Handler marks the path for regeneration on its next visit; completed regeneration produces the replacement cache entry.

4. **Q:** How do multiple fetch intervals affect a statically cached route?
   **A:** The smallest interval governs that route's regeneration. Each data entry can still keep its own cache policy.


**Failed Regeneration**

5. **Q:** Why is catching an upstream error and returning a placeholder risky during ISR?
   **A:** That placeholder may count as a successful regeneration and replace useful cached content. Let unexpected failures throw so Next retains the last successful page.


**Runtime and Host Limits**

6. **Q:** Why can pure static hosting not support ISR?
   **A:** There is no runtime available to regenerate and replace cached route output after deployment. A new build is required instead.

7. **Q:** What must a webhook account for when Proxy rewrites a URL to an ISR route?
   **A:** On-demand ISR requests do not run Proxy, so invalidate the actual route path after rewriting. Multi-instance self-hosting also needs shared cache coordination.

## Static Exports in Next.js

Source: [Static Exports in Next.js](10.4.3.06-static-exports.md)

**Definition**

1. **Q:** Which command produces the export folder on modern Next.js?
   **A:** next build with output set to export emits the static output. The old next export command was removed in version 14.


**Build-Time Rendering**

2. **Q:** Do Server Components disappear from an exported app?
   **A:** Their runtime execution moves to build time. The browser receives generated HTML and static navigation payloads, without a request-time Next server.


**Route Enumeration**

3. **Q:** How do App and Pages routers prohibit unknown exported dynamic IDs?
   **A:** App Router enumerates generateStaticParams and disables dynamicParams. Pages Router uses getStaticPaths with fallback:false.


**Static Files and Runtime Endpoints**

4. **Q:** Can a request-independent GET Route Handler be exported?
   **A:** Yes, with appropriate static configuration it emits a build-time file. Request-dependent handlers and mutation methods still require a runtime.


**Image Delivery**

5. **Q:** How can next/image work when no optimizer server exists?
   **A:** Serve the source unoptimized or use a custom loader pointing to an external optimizer/CDN. Preserve layout dimensions either way.


**Authorization Boundary**

6. **Q:** Where is authorization enforced when an exported shell shows private API data?
   **A:** The external API must verify the request and enforce permissions. Hiding client UI is not an access-control boundary.

## Configured cache model and freshness

Source: [Learning chapter](10.4.3.03-caching.md)

**Q:** Why must you inspect cacheComponents before copying a caching example?

**A:** Next.js 16 Cache Components and the traditional model use different configuration controls. Segment dynamic/revalidate/fetchCache options are not interchangeable with use-cache boundaries.

**Q:** Why can router.refresh still show old server data?

**A:** It requests fresh client route rendering without necessarily invalidating the persistent server Data Cache. Invalidate the relevant server entry/path according to the write contract.

**Q:** How do updateTag and revalidateTag with max differ?

**A:** updateTag is Server Actions-only immediate expiry for read-your-writes. revalidateTag(tag, max) marks entries stale for stale-while-revalidate, so readers can briefly see prior data.


## Write and Delivery Traces

Source: [Fetching](10.4.3.01-data-fetching-patterns.md), [Actions](10.4.3.02-server-actions.md), [Caching](10.4.3.03-caching.md), [Streaming](10.4.3.04-streaming.md), [ISR](10.4.3.05-incremental-static-regeneration.md), [Export](10.4.3.06-static-exports.md).

**Q:** Why label retained search results while the new key loads?
**A:** Placeholder data can belong to the previous query. It is useful continuity only when users can tell that the current input has not finished resolving.

**Q:** Why does setting a desired like state behave more predictably on retry than toggling it?
**A:** Retrying the same desired state is idempotent under the unique record constraint; a second toggle reverses the first result. Competing opposite states still need an ordering policy.

**Q:** What makes a temporary optimistic todo disappear after successful submission?
**A:** The action overlay ends. If the authorized server list has not become the new base, React returns to the old list; revalidation/base reconciliation is part of success.

**Q:** Can a fast streamed title guarantee a fast largest-content paint?
**A:** No. The largest visible region may still wait for data, assets or proxy buffering. Measure its arrival separately from shell delivery.

**Q:** Why invalidate a bestseller list when a rating falls below its threshold?
**A:** The product was present in the old selection and must be removed. Checking only the new qualifying state misses that change; use before/after data or conservative list invalidation.

**Q:** Does fetching generated JSON after mount make an exported dashboard live?
**A:** No. The JSON remains the deployed build snapshot. Live or private data requires a separate runtime and the appropriate freshness/access policy.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
