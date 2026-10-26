<!-- section: Next.js | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Rendering Fundamentals — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## SSR, CSR, SSG, and ISR in Next.js

Source: [SSR, CSR, SSG, and ISR in Next.js](10.4.1.01-ssr-csr-ssg-isr.md)

**Q:** How do rendering time and freshness differ across static rendering, SSR, CSR and ISR?

**A:** Static output is produced before a request; SSR produces request-dependent output; CSR produces or updates UI in the browser; ISR revalidates cached static output. ISR is a freshness policy, and a Client Component can still appear in the initial server-rendered HTML.

**Q:** Why can a page stay stale after its revalidation interval has passed?

**A:** Expiry only makes it eligible for refresh. A later visit triggers regeneration, and failed or unfinished regeneration leaves the previous successful output in place.

**Q:** Does adding use client make the initial page purely browser-rendered?

**A:** No. Next normally prerenders the initial Client Component UI, then hydrates it; effect-based data loading occurs afterward.

**Q:** Which part of a static data function becomes public?

**A:** Returned props become part of the generated page payload. A secret used only for server authentication can stay private, but returning it or putting it in a logged URL exposes it.

**Q:** Why must a slow await sit below the intended Suspense boundary?

**A:** A parent that waits before returning its JSX cannot render that boundary yet. Moving the read into the wrapped child lets the parent reveal its shell.

**Q:** Can rendering mode alone predict a route's JavaScript bundle size?

**A:** No. Component boundaries and imported dependencies determine the browser code; Server Components can reduce it under several rendering modes.

## App Router in Next.js

Source: [App Router in Next.js](10.4.1.02-app-router.md)

**Q:** How does a folder become a publicly rendered URL?

**A:** Folders describe segments, but page.tsx exposes the UI at that location. A route group organizes files without adding a URL segment.

**Q:** Why does a shared layout preserve state while a template can reset it?

**A:** Navigation reuses the shared layout instance. A template remounts when its relevant segment key changes, so descendant client state and effects restart; deeper navigation can retain a higher template and search-parameter changes alone do not remount it.

**Q:** How should a server page read a dynamic segment in Next.js 15 and 16?

**A:** Receive params as a Promise and await it before reading the field. The temporary synchronous compatibility in 15 does not extend to 16.

**Q:** What does a parallel-route `default.tsx` do on a hard load, and what happens if an unmatched slot has none?

**A:** It provides fallback UI when Next cannot recover the slot's previous active state. Without a default, an unmatched slot returns a 404; the implicit `children` slot may need a default too. Return `null` for an intentionally empty slot or call `notFound()` when the route should be absent.

**Q:** If a layout checks a role and returns only the `admin` or `user` slot, has it prevented the other slot's server work?

**A:** No. Next renders every slot at that segment even when the layout does not return its output. Authorize inside each slot's data-access path, and do not mix prerendered and dynamically rendered slots at one segment.

**Q:** Why does the current segment's error.tsx fail to catch an error in its layout?

**A:** The error boundary is nested beneath that layout and catches the page and descendants. Use an ancestor boundary for layout or template errors; `global-error.tsx` can cover root-layout failure and must define its own `<html>` and `<body>`.

**Q:** Can a page and a Route Handler claim the same segment?

**A:** No. Both own the same URL, so place the handler in a different segment.

## Server Components in Next.js

Source: [Server Components in Next.js](10.4.1.03-server-components.md)

**Q:** What does RSC add beyond an ordinary server-rendered HTML response?

**A:** It serializes the server-rendered component tree for reconciliation without shipping those components' implementations. Initial HTML prerendering complements that payload.

**Q:** Why does a visual child of a Client Component not necessarily become client code?

**A:** The import graph defines the boundary. A Server Component can supply an already-rendered child through props without the client wrapper importing its module.

**Q:** What check is missing if a session lookup merely finds a database row?

**A:** Expiry and current authorization still need validation. Finding an ID does not establish that the session remains usable or can access the resource.

**Q:** Which callback can cross from server code to client UI?

**A:** A Server Function reference can cross through React's protocol. An ordinary closure created while rendering cannot be passed as a client event handler.

**Q:** How can server-only code still leak a secret?

**A:** Its rendered output and returned client props are delivered to the browser. Server execution protects the implementation, not every value it emits.

**Q:** Why is zero client component-code bytes different from zero delivery cost?

**A:** HTML and the RSC payload still carry rendered output, and the app needs client routing/runtime support. Large serialized results can remain expensive even without server component code.

## Client Components in Next.js

Source: [Client Components in Next.js](10.4.1.04-client-components.md)

**Q:** When does a Client Component execute before it becomes interactive?

**A:** Next normally executes it during server prerendering and again during browser hydration. Its effects wait until the browser commit.

**Q:** What expands the client bundle after a use client boundary?

**A:** Modules imported below that boundary join the client graph. Keeping a boundary close to the interactive control avoids pulling unrelated dependencies into it.

**Q:** Where must a dynamic import with ssr:false be declared?

**A:** Inside a Client Component wrapper. A server page can import that wrapper, but cannot directly disable SSR through that option.

**Q:** Why is a false mounted flag changed in an effect hydration-safe?

**A:** Both initial renders use the same false value. The effect changes content only after hydration has reconciled the matching initial HTML.

**Q:** Can a native Date and a Moment instance cross the same RSC boundary?

**A:** React supports native Date serialization. A Moment instance is an arbitrary class object and needs conversion to supported values.

**Q:** Why do local product-filter controls not change a server-rendered grid by themselves?

**A:** Their state belongs only to the client control. Connect it to URL parameters/server navigation or a client data layer to affect the product results.

## Trace and Boundary Checks

Source: [Rendering comparison](10.4.1.01-ssr-csr-ssg-isr.md), [App Router](10.4.1.02-app-router.md), [Server Components](10.4.1.03-server-components.md), [Client Components](10.4.1.04-client-components.md).

**Q:** Why can a request-rendered account page still display old data?

**A:** Request rendering and upstream caching are separate. An upstream data cache or lagging source can return an older value even when Next bypasses its own persistent fetch cache.

**Q:** Does a middleware header naming ISR prove regeneration happened?

**A:** No. It labels a request match. Verify production output and cache/timestamp behavior with controlled requests.

**Q:** Which interception marker reaches /photos from feed/@modal, and why?

**A:** `(..)photos` moves one route segment above feed. The @modal slot does not count as a URL segment; `(.)photos` would target a photo segment at the feed level instead.

**Q:** What does retry add beyond resetting a failed boundary in current Next.js?

**A:** Stable `retry` in 16.3+ re-fetches and re-renders the failed region. `reset` clears the boundary state without re-fetching server content; 16.2 names the newer API `unstable_retry`. Match the installed version and resource owner.

**Q:** Why attach the product ID to the stock result instead of only aborting on cleanup?

**A:** A render with a new product ID happens before the old Effect cleanup. Comparing the result identity during render prevents the previous product's stock from appearing in that gap; cleanup separately invalidates obsolete completions.

**Q:** What changes on reload after a photo was opened in an intercepted slot?

**A:** Direct navigation selects the normal photo page; an unmatched slot uses its default because the prior client navigation state is unavailable.

**Q:** Why can one review query per product card be slow even with zero card implementation bytes in the browser?

**A:** Those server reads can create an N+1 query pattern. Code placement reduces bundle cost but does not batch database work.

**Q:** Why capture a socket in an effect cleanup instead of merely closing whatever its ref currently contains?

**A:** Each setup owns its own connection. Cleanup must disable and close that instance so obsolete work cannot publish into a later setup.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
