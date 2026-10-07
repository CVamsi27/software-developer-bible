<!-- section: Next.js | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Rendering Fundamentals — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## SSR, CSR, SSG, and ISR in Next.js

Source: [SSR, CSR, SSG, and ISR in Next.js](10.4.1.01-ssr-csr-ssg-isr.md)

**Definition**

1. **Q:** What distinguishes the four strategies before JavaScript runs?
   **A:** CSR waits for browser work to create its data-driven UI; SSR renders per request, SSG creates a build snapshot, and ISR reuses a snapshot until regeneration.


**How It Works**

2. **Q:** Why can a page stay stale after its revalidation interval has passed?
   **A:** Expiry only makes it eligible for refresh. A later visit triggers regeneration, and failed or unfinished regeneration leaves the previous successful output in place.


**Code Examples**

3. **Q:** Does adding use client make the initial page purely browser-rendered?
   **A:** No. Next normally prerenders the initial Client Component UI, then hydrates it; effect-based data loading occurs afterward.

4. **Q:** Which part of a static data function becomes public?
   **A:** Returned props become part of the generated page payload. A secret used only for server authentication can stay private, but returning it or putting it in a logged URL exposes it.


**Common Mistakes**

5. **Q:** Why must a slow await sit below the intended Suspense boundary?
   **A:** A parent that waits before returning its JSX cannot render that boundary yet. Moving the read into the wrapped child lets the parent reveal its shell.


**Performance Considerations**

6. **Q:** Can rendering mode alone predict a route's JavaScript bundle size?
   **A:** No. Component boundaries and imported dependencies determine the browser code; Server Components can reduce it under several rendering modes.

## App Router in Next.js

Source: [App Router in Next.js](10.4.1.02-app-router.md)

**Definition**

1. **Q:** How does a folder become a publicly rendered URL?
   **A:** Folders describe segments, but page.tsx exposes the UI at that location. A route group organizes files without adding a URL segment.


**How It Works**

2. **Q:** Why does a shared layout preserve state while a template can reset it?
   **A:** Navigation reuses the shared layout instance. A template receives a new instance/key, so its state and effects restart.


**Code Examples**

3. **Q:** How should a server page read a dynamic segment in Next.js 15 and 16?
   **A:** Receive params as a Promise and await it before reading the field. The temporary synchronous compatibility in 15 does not extend to 16.

4. **Q:** What happens to an unmatched parallel slot after a hard navigation?
   **A:** The router needs a default.tsx fallback because it cannot recover that slot's prior active state. Provide one for each potentially unmatched slot.


**Common Mistakes**

5. **Q:** Why does the current segment's error.tsx fail to catch an error in its layout?
   **A:** The error boundary is nested beneath that layout. A parent boundary, or global-error.tsx for root-layout failure, must cover the failing ancestor.


**Code Examples**

6. **Q:** Can a page and a Route Handler claim the same segment?
   **A:** No. Both own the same URL, so place the handler in a different segment.

## Server Components in Next.js

Source: [Server Components in Next.js](10.4.1.03-server-components.md)

**Definition**

1. **Q:** What does RSC add beyond an ordinary server-rendered HTML response?
   **A:** It serializes the server-rendered component tree for reconciliation without shipping those components' implementations. Initial HTML prerendering complements that payload.


**How It Works**

2. **Q:** Why does a visual child of a Client Component not necessarily become client code?
   **A:** The import graph defines the boundary. A Server Component can supply an already-rendered child through props without the client wrapper importing its module.


**Code Examples**

3. **Q:** What check is missing if a session lookup merely finds a database row?
   **A:** Expiry and current authorization still need validation. Finding an ID does not establish that the session remains usable or can access the resource.


**Common Mistakes**

4. **Q:** Which callback can cross from server code to client UI?
   **A:** A Server Function reference can cross through React's protocol. An ordinary closure created while rendering cannot be passed as a client event handler.

5. **Q:** How can server-only code still leak a secret?
   **A:** Its rendered output and returned client props are delivered to the browser. Server execution protects the implementation, not every value it emits.


**Performance Considerations**

6. **Q:** Why is zero client component-code bytes different from zero delivery cost?
   **A:** HTML and the RSC payload still carry rendered output, and the app needs client routing/runtime support. Large serialized results can remain expensive even without server component code.

## Client Components in Next.js

Source: [Client Components in Next.js](10.4.1.04-client-components.md)

**Definition**

1. **Q:** When does a Client Component execute before it becomes interactive?
   **A:** Next normally executes it during server prerendering and again during browser hydration. Its effects wait until the browser commit.


**How It Works**

2. **Q:** What expands the client bundle after a use client boundary?
   **A:** Modules imported below that boundary join the client graph. Keeping a boundary close to the interactive control avoids pulling unrelated dependencies into it.


**Code Examples**

3. **Q:** Where must a dynamic import with ssr:false be declared?
   **A:** Inside a Client Component wrapper. A server page can import that wrapper, but cannot directly disable SSR through that option.


**Common Mistakes**

4. **Q:** Why is a false mounted flag changed in an effect hydration-safe?
   **A:** Both initial renders use the same false value. The effect changes content only after hydration has reconciled the matching initial HTML.

5. **Q:** Can a native Date and a Moment instance cross the same RSC boundary?
   **A:** React supports native Date serialization. A Moment instance is an arbitrary class object and needs conversion to supported values.


**Code Examples**

6. **Q:** Why do local product-filter controls not change a server-rendered grid by themselves?
   **A:** Their state belongs only to the client control. Connect it to URL parameters/server navigation or a client data layer to affect the product results.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
