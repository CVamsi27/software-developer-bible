<!-- section: Next.js | category: Reference | tags: revision, retrieval-practi | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Data & Caching — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Data Fetching Patterns in Next.js (App Router)

Source: [Data Fetching Patterns in Next.js (App Router)](10.4.3.01-data-fetching-patterns.md)

**Definition**

1. **Q:** What separates a server read from an interactive client query?
   **A:** A server read can supply data before browser execution when its inputs are already known. Browser-driven search, polling, and optimistic interactions benefit from a client query cache.


**How It Works**

2. **Q:** Why does adding a fetch tag not necessarily persist its response?
   **A:** Tags label entries for invalidation. Next.js 15 still needs an explicit persistent-cache choice such as force-cache or positive revalidate.

3. **Q:** How do React cache and unstable_cache differ?
   **A:** React cache deduplicates within a server render request. unstable_cache stores supported non-fetch results across requests with configurable revalidation.


**Code Examples**

4. **Q:** Why can parallelizing queries silently change the requested result?
   **A:** A dependent query needs its original input, such as the first post's ID. Substituting a user ID may remove a dependency but fetch a different dataset.


**Common Mistakes**

5. **Q:** Will useDeferredValue guarantee fewer search requests?
   **A:** No. It prioritizes rendering rather than enforcing a time-based debounce; use debouncing/cancellation when controlling query traffic.


**Best Practices**

6. **Q:** Where should cache invalidation occur relative to a mutation?
   **A:** After the authorized, validated write succeeds and before redirecting to dependent output. Target the routes/tags affected rather than invalidating unrelated data.

## Server Actions in Next.js

Source: [Server Actions in Next.js](10.4.3.02-server-actions.md)

**Definition**

1. **Q:** Why is a server-only action still an externally reachable security boundary?
   **A:** Next creates a client-callable POST interface for it. Keep identity, ownership, and runtime input validation inside the action.


**How It Works**

2. **Q:** Which hook now owns returned form state in the React 19 stack?
   **A:** useActionState from react pairs the previous state with the next submission. The older react-dom useFormState API is deprecated.


**Code Examples**

3. **Q:** Why must a useFormStatus submit button be below the form it observes?
   **A:** The hook reads the nearest parent form context. Calling it in the component that creates the form cannot observe that future child form.

4. **Q:** What infrastructure setting must match a form that accepts a five-MiB upload?
   **A:** The Server Action request-body limit must be raised from its default one MiB to a bounded suitable value, or the file should upload directly to storage.


**Common Mistakes**

5. **Q:** Why should redirect be outside a broad action catch block?
   **A:** Redirect throws a framework control-flow signal. A catch can intercept it and incorrectly report a successful redirect as a failed mutation.

6. **Q:** Which returned values prove that React serialization is broader than JSON?
   **A:** Native Date, Map, and Set can be supported values. Ordinary functions and arbitrary class instances still cannot be returned across the boundary.

## Caching in Next.js

Source: [Caching in Next.js](10.4.3.03-caching.md)

**Definition**

1. **Q:** Which cache survives longer than one render but stores data rather than HTML?
   **A:** The Data Cache persists reusable reads across requests. Request memoization is shorter-lived, and the Full Route Cache holds rendered route output.


**How It Works**

2. **Q:** Why can router.refresh still display the same old server data?
   **A:** It refreshes the browser's route view without invalidating persistent server data. The new render may read the same cached entry.


**Code Examples**

3. **Q:** Which requests does automatic request memoization combine?
   **A:** Identical GET URL/options calls within a React server render. Different endpoints and Route Handler execution are outside that deduplication rule.


**Common Mistakes**

4. **Q:** Why does an invalidation tag not isolate two users' cached records?
   **A:** A tag groups entries for refresh, rather than assigning a distinct user key or granting access. Identity-aware keys and authorization are separate requirements.


**Modern Paradigm: `use cache` and Partial Prerendering**

5. **Q:** How does enabling Cache Components change the route design in Next.js 16?
   **A:** Cache reusable functions/components explicitly and place uncached request-time work under Suspense. This uses the 16 cacheComponents configuration rather than stable 15.5 segment behavior.

6. **Q:** Which Next.js 16 invalidation choice gives a Server Action read-your-writes behavior?
   **A:** updateTag immediately expires tagged data for that action workflow. revalidateTag with max instead permits stale output while background refresh runs.

## Streaming in Next.js

Source: [Streaming in Next.js](10.4.3.04-streaming.md)

**Definition**

1. **Q:** What can the browser show before every streamed section finishes?
   **A:** The completed shell and the fallbacks of pending subtrees. Each subtree can replace its placeholder when its server work finishes.


**How It Works**

2. **Q:** Does adding three Suspense boundaries remove a sequential data dependency?
   **A:** No. Boundaries control reveal timing; a later read that needs an earlier result still waits for that result.


**Code Examples**

3. **Q:** What does loading.tsx wrap that an arbitrary local fallback may not?
   **A:** It supplies a segment-level Suspense boundary around the page and its descendants beneath the layout. Local boundaries provide more granular reveal inside that route.


**Common Mistakes**

4. **Q:** Must every Suspense boundary have its own error.tsx?
   **A:** No. Suspense handles pending work, while route/custom error boundaries handle failures. A route boundary may cover several Suspense regions.


**Best Practices**

5. **Q:** Why can a late not-found result still have HTTP status 200?
   **A:** The shell may already have sent its headers. Perform decisions needing a real status or redirect before streaming begins.


**Performance Considerations**

6. **Q:** Why can a quick shell improve first paint without fixing LCP?
   **A:** The largest visible element may still depend on a slow section. Measure its actual arrival and reserve matching placeholder geometry to reduce layout shift.

## Incremental Static Regeneration (ISR)

Source: [Incremental Static Regeneration (ISR)](10.4.3.05-incremental-static-regeneration.md)

**Definition**

1. **Q:** Who triggers regeneration after a time interval elapses?
   **A:** The next qualifying request, not a timer job. Warm stale output is served while background regeneration proceeds.


**How It Works**

2. **Q:** When does a newly visited ID incur render latency?
   **A:** When no page has been generated for it yet. Build-time generation of popular IDs avoids that first-visit cost.


**Code Examples**

3. **Q:** Does a CMS webhook calling revalidatePath eagerly rebuild the route?
   **A:** No. A Route Handler marks the path for regeneration on its next visit; completed regeneration produces the replacement cache entry.

4. **Q:** How do multiple fetch intervals affect a statically cached route?
   **A:** The smallest interval governs that route's regeneration. Each data entry can still keep its own cache policy.


**Common Mistakes**

5. **Q:** Why is catching an upstream error and returning a placeholder risky during ISR?
   **A:** That placeholder may count as a successful regeneration and replace useful cached content. Let unexpected failures throw so Next retains the last successful page.


**Best Practices**

6. **Q:** Why can pure static hosting not support ISR?
   **A:** There is no runtime available to regenerate and replace cached route output after deployment. A new build is required instead.

## Static Exports in Next.js

Source: [Static Exports in Next.js](10.4.3.06-static-exports.md)

**Definition**

1. **Q:** Which command produces the export folder on modern Next.js?
   **A:** next build with output set to export emits the static output. The old next export command was removed in version 14.


**How It Works**

2. **Q:** Do Server Components disappear from an exported app?
   **A:** Their runtime execution moves to build time. The browser receives generated HTML and static navigation payloads, without a request-time Next server.


**Code Examples**

3. **Q:** How do App and Pages routers prohibit unknown exported dynamic IDs?
   **A:** App Router enumerates generateStaticParams and disables dynamicParams. Pages Router uses getStaticPaths with fallback:false.


**Common Mistakes**

4. **Q:** Can a request-independent GET Route Handler be exported?
   **A:** Yes, with appropriate static configuration it emits a build-time file. Request-dependent handlers and mutation methods still require a runtime.


**Best Practices**

5. **Q:** How can next/image work when no optimizer server exists?
   **A:** Serve the source unoptimized or use a custom loader pointing to an external optimizer/CDN. Preserve layout dimensions either way.


**How It Works**

6. **Q:** Where is authorization enforced when an exported shell shows private API data?
   **A:** The external API must verify the request and enforce permissions. Hiding client UI is not an access-control boundary.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

## Configured cache model and freshness

Source: [Learning chapter](10.4.3.03-caching.md)

**Q:** Why must you inspect cacheComponents before copying a caching example?

**A:** Next.js 16 Cache Components and the traditional model use different configuration controls. Segment dynamic/revalidate/fetchCache options are not interchangeable with use-cache boundaries.

**Q:** Why can router.refresh still show old server data?

**A:** It requests fresh client route rendering without necessarily invalidating the persistent server Data Cache. Invalidate the relevant server entry/path according to the write contract.

**Q:** How do updateTag and revalidateTag with max differ?

**A:** updateTag is Server Actions-only immediate expiry for read-your-writes. revalidateTag(tag, max) marks entries stale for stale-while-revalidate, so readers can briefly see prior data.


---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
