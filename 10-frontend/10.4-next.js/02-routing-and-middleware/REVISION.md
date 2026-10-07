<!-- section: Next.js | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Routing & Middleware — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Middleware in Next.js

Source: [Middleware in Next.js](10.4.2.01-middleware.md)

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

## Route Handlers in Next.js

Source: [Route Handlers in Next.js](10.4.2.02-route-handlers.md)

**Definition**

1. **Q:** Must a Route Handler live below an api folder?
   **A:** No. Any app segment can expose a route.ts handler, provided it does not also contain a page claiming that URL.


**How It Works**

2. **Q:** Are Next.js 15 GET handlers persistently cached automatically?
   **A:** No. Opt a request-independent public GET into caching explicitly, and distinguish framework caches from HTTP browser/CDN caching.


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

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
