<!-- section: Next.js | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Routing & Middleware — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Proxy (formerly Middleware) in Next.js

Source: [Proxy in Next.js](10.4.2.01-middleware.md)

**Definition**

1. **Q:** How does the runtime change when moving from Next.js 15 middleware to 16 Proxy?
   **A:** 15 defaults to Edge and supports configured Node middleware from 15.5. The renamed Proxy entry point in 16 uses Node.js without an Edge option.


**How It Works**

2. **Q:** How do rewrites and redirects differ for the visitor?
   **A:** A redirect asks the browser to navigate to another URL. A rewrite selects another destination while keeping the visible requested URL.


**Code Examples**

3. **Q:** Why can an experiment lose its sticky assignment even though cookies.set was called?
   **A:** The cookie was attached to a response that was discarded. Set it on the same rewrite/continue response that the entry point actually returns.

4. **Q:** How should verified identity reach a downstream server handler?
   **A:** Overwrite the cloned request headers and forward them through NextResponse.next's request option. Response headers instead expose values to the browser.


**Common Mistakes**

5. **Q:** Why is an in-memory IP limiter insufficient across replicas?
   **A:** Each process has independent counters and lifetimes. Shared atomic storage, expiry, and a trustworthy client-IP source are required for consistent enforcement.


**Best Practices**

6. **Q:** Why should a cookie-presence redirect never be the only authorization check?
   **A:** A cookie can be forged, expired, or insufficient for a particular resource. The data-access or mutation endpoint must independently verify identity and permissions.

7. **Q:** Why can excluding a page path in `config.matcher` leave its Server Function outside Proxy checks too?
   **A:** Server Function calls are POST requests to the page route, not separate routes. Their own function must authenticate and authorize every call; a Proxy matcher is not their security boundary.

## Route Handlers in Next.js

Source: [Route Handlers in Next.js](10.4.2.02-route-handlers.md)

**Definition**

1. **Q:** Must a Route Handler live below an api folder?
   **A:** No. Any app segment can expose a route.ts handler, provided it does not also contain a page claiming that URL.


**How It Works**

2. **Q:** How does GET caching differ with Cache Components off and on?
   **A:** With Cache Components off, Route Handlers are uncached by default and a safe public GET can opt in through route configuration. With it on, deterministic work can be prerendered and reusable data can be cached in a helper; request-specific reads remain dynamic.


**Code Examples**

3. **Q:** Why must signature verification precede JSON parsing for a webhook?
   **A:** The signature covers the exact raw bytes/text. Parsing and re-encoding may change those bytes, and the request body stream can only be consumed once.

4. **Q:** What must a schema failure return to become a useful HTTP validation response?
   **A:** Handle the failure and return an appropriate client-error status such as 400. An uncaught parse exception is not automatically that response.


**Common Mistakes**

5. **Q:** Should a read-only endpoint export every supported HTTP method?
   **A:** No. Only expose intended operations; the router supplies a method-not-allowed response for the rest and can generate OPTIONS.

6. **Q:** Why are response CORS headers alone insufficient for a preflighted request?
   **A:** The browser first asks OPTIONS whether the method and headers are allowed. That preflight also needs the intended CORS policy, while authentication remains a separate check.

7. **Q:** Why should a Route Handler prefer the generated `RouteContext` helper for dynamic params?
   **A:** Next.js generates the route-aware type during development, build, or type generation, keeping the handler's param shape aligned with the filesystem route.

8. **Q:** What should logout do beyond expiring the browser's session cookie?
   **A:** Revoke the server-side session as well. Cookie flags reduce exposure, but they do not validate the session or authorize a mutation; cookie-authenticated writes also need a CSRF policy.

## Metadata API in Next.js

Source: [Metadata API in Next.js](10.4.2.03-metadata.md)

**Definition**

1. **Q:** Does generateMetadata imply work on every incoming request?
   **A:** No. A prerenderable route can resolve generated metadata during build; request-dependent inputs may instead require runtime resolution or streaming.


**How It Works**

2. **Q:** What disappears when a page replaces its parent's openGraph object?
   **A:** Unrepeated nested fields can disappear because merging is shallow. Explicitly carry forward images or other needed parent fields.


**Code Examples**

3. **Q:** When should a page use title.absolute?
   **A:** Use it when that page must bypass an inherited title template. Ordinary page titles receive the ancestor's formatting.

4. **Q:** Does metadataBase create a canonical link?
   **A:** It provides a base for relative URL fields. Declare alternates.canonical to emit the canonical relationship.


**Common Mistakes**

5. **Q:** Why is JSON.stringify alone insufficient for untrusted JSON-LD inserted into a script?
   **A:** A literal less-than character can begin markup that terminates the script. Escape it before injection so CMS/user text remains script content.

6. **Q:** Do two Open Graph image sizes provide responsive on-page images?
   **A:** No. Sharing platforms choose preview images; a browser's responsive page image uses srcset/sizes through next/image.

7. **Q:** Where does JSON-LD belong if it is not a field in the Metadata object?
   **A:** Render structured data separately in a script element in the page or layout, with safe serialization. The Metadata API emits supported document metadata; it does not turn a custom JSON-LD field into structured data.

8. **Q:** What takes precedence when a route defines both `opengraph-image.png` and an `openGraph.images` value?
   **A:** The file-based metadata convention takes precedence for that field. Remove or align the competing declaration so the emitted preview is intentional.

9. **Q:** Which sitemap fields should be kept accurate for Google, and which do not affect its crawl decisions?
   **A:** `lastModified` should reflect a significant content change; Google ignores `priority` and `changefreq`. Split a sitemap above 50,000 URLs.

## Follow the Failure Boundary

Source: [Proxy](10.4.2.01-middleware.md), [Route Handlers](10.4.2.02-route-handlers.md), [Metadata](10.4.2.03-metadata.md).

**Q:** Why clone a rewrite URL before replacing its pathname?
**A:** The existing URL carries query parameters and other routing context. A path-only construction can silently lose pagination or search inputs.

**Q:** What makes an in-memory fixed-window limiter pass request 100 but reject 101?
**A:** The first request initializes count 1; accepted requests increment it until the maximum. Later requests in that window reject; a new window resets the record. Replicas still need a shared atomic policy.

**Q:** Why is putting JSON directly into an ORM update unsafe even after authentication?
**A:** Identity does not restrict supplied field names. Parse an allowlist and authorize the resource so protected fields such as roles cannot be mass-assigned.

**Q:** What work must stop when an SSE consumer disconnects?
**A:** The stream's producer and timers or upstream subscriptions must stop through cancellation; returning streaming headers alone does not clean them up.

**Q:** Why does a verified payment webhook still need event deduplication?
**A:** Verification establishes source/integrity. Delivery may retry or arrive out of order, so durable handling must avoid duplicate side effects and invalid state transitions.

**Q:** Why should a sitemap not stamp every page with the time the file was generated?
**A:** The field describes content modification, not the sitemap's execution time. Use actual page changes so the discovery signal remains accurate.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
