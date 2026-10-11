<!-- section: Next.js | category: Reference | tags: revision, retrieval-practice | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Next.js-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20retrieval--practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Production — Next.js — Revision

Complete the learning chapters first, then answer these questions without reopening them. Use each source link to check an uncertain answer.

## Authentication in Next.js

Source: [Authentication in Next.js](10.4.4.01-authentication.md)

**Definition**

1. **Q:** What proves identity beyond the presence of a session cookie?
   **A:** A verified, unexpired token or valid stored session plus current account checks. Protected resources also need authorization for that verified identity.


**How It Works**

2. **Q:** Why does httpOnly not make an application immune to XSS?
   **A:** It prevents JavaScript from reading the token directly. Injected code may still issue authenticated requests or read exposed page data.


**Code Examples**

3. **Q:** Which route should be considered first when /admin and /admin/users have different roles?
   **A:** Evaluate the most specific matching segment path first. Otherwise the broad admin rule can shadow the stricter users rule.

4. **Q:** Why is a reusable JWT labeled csrf an inadequate CSRF protocol?
   **A:** It is not tied to the visitor's session and can be replayed. Use a trusted origin check or the library's session-bound token protocol.


**Common Mistakes**

5. **Q:** Does clearing a signed-token cookie revoke a stolen copy?
   **A:** No. Another holder can use it until expiry unless the server implements revocation or related session checks.


**Best Practices**

6. **Q:** What differs between the shown NextAuth.js v4 integration and Auth.js v5?
   **A:** The shown v4 configuration returns an HTTP handler and uses its compatible adapter. v5 exposes handlers/auth helpers differently, so examples and adapter packages must match the pinned version.

## Image Optimization in Next.js

Source: [Image Optimization in Next.js](10.4.4.02-image-optimization.md)

**Definition**

1. **Q:** Does the default image optimizer transform every image during the build?
   **A:** No. Requested variants are transformed on demand and then cached. External custom loaders can use a different optimization service.


**How It Works**

2. **Q:** Why must sizes describe the image's real displayed width?
   **A:** The browser uses that hint to choose a srcset candidate. An inaccurate hint can download a much larger image than the layout needs.


**Code Examples**

3. **Q:** When can dimensions and blur data come from a static import?
   **A:** Supported static JPEG/PNG/WebP/AVIF imports can provide dimensions and blur metadata automatically; animated sources do not get that blur treatment.

4. **Q:** Which parent requirements make fill mode reserve stable space?
   **A:** A positioned container needs a defined size or aspect ratio. The image can fill it without determining the container's height itself.


**Common Mistakes**

5. **Q:** How does image preload guidance differ between Next.js 15 and 16?
   **A:** Next.js 15 examples may use `priority`; Next.js 16 deprecates it. Prefer `loading="eager"` or `fetchPriority="high"` in most cases, and use `preload` only when the LCP image is unambiguous. Do not combine the hints.

6. **Q:** Why must a Next.js 16 image configuration allowlist quality values?
   **A:** The optimizer accepts only configured `qualities`; restricting the choices bounds which output variants callers can request and prevents arbitrary quality values from expanding optimization work.


**Best Practices**

7. **Q:** How can changed images become visible before a long optimizer TTL ends?
   **A:** Version or change the source URL so it selects a new variant key. Route tag revalidation does not purge the image optimizer cache.

## Deploying Next.js

Source: [Deploying Next.js](10.4.4.03-deploying-nextjs.md)

**Definition**

1. **Q:** Which responsibilities remain when leaving managed hosting for Node containers?
   **A:** Own deployment, shared caching, runtime dependencies, network access, and observability. Standalone output reduces packaging work but does not provide those operations.


**How It Works**

2. **Q:** Why copy public and .next/static after copying standalone output?
   **A:** Output tracing does not include those static asset directories by default. Missing them leaves HTML without its expected files.

3. **Q:** Which tag sources and values must a previous-model cache handler preserve?
   **A:** Page/route entries carry tags in `data.headers` (`x-next-cache-tags`); cached `fetch` entries use `ctx.tags`. Preserve the full cache value and timestamp, serialize values such as `Buffer` and `Map`, and synchronize invalidations across replicas.

4. **Q:** What must match across replicas when they serve the same build?
   **A:** Run the same build and Server Action encryption key on every instance. Use a deployment ID during rolling releases to detect version skew, and retain the corresponding immutable assets.


**Code Examples**

5. **Q:** Why can changing a container variable leave a NEXT_PUBLIC URL unchanged?
   **A:** Its browser value was inlined during build. Rebuild the client bundle or read configurable values through request-time server code.


**Common Mistakes**

6. **Q:** Why is a rewrite back to the same local path insufficient for a zone split?
   **A:** It never forwards to the independent deployment. Route the path and asset namespace to that zone's actual origin.


**Best Practices**

7. **Q:** What proves that a self-hosted shutdown drains real work?
   **A:** Send `SIGTERM` or `SIGINT` to the process that owns the Next.js server, allow the configured drain interval, and test with requests in flight. A Kubernetes `preStop` delay alone does not prove ingress has stopped sending traffic.

## Trace a production boundary

Source: [Authentication](10.4.4.01-authentication.md), [Image optimization](10.4.4.02-image-optimization.md), [Deployment](10.4.4.03-deploying-nextjs.md)

**Q:** A signed session says admin but the account was demoted. What should authorize a protected write?
**A:** A verified identity resolved against current account/permission policy. An early routing check based on token claims cannot establish current resource access by itself.

**Q:** Can a response generation counter stop an older login response from setting a cookie?
**A:** No. It can ignore stale client state updates, but the browser processes response cookies independently. Serialize account-changing operations or enforce an appropriate server/session protocol.

**Q:** A 400-CSS-pixel card appears on a density-2 display. Why might the browser choose an approximately 800-pixel image?
**A:** The display needs about two source pixels per CSS pixel. Accurate sizes and available srcset candidates let it choose suitable bytes; optimizer configuration and browser choice determine the actual candidate.

**Q:** Why should source replacement create a new loading-state owner?
**A:** An old image can complete or fail after the replacement. A source-keyed component resets state and isolates those late events from the new image's feedback.

**Q:** The new server is healthy but older browser tabs cannot fetch chunks. What did the rollout omit?
**A:** Asset/version compatibility and retention during overlapping deployments. A health probe proves current serving behavior, not that clients with an older build still have the files and action references they need.

**Q:** Does a shared ISR store automatically provide cross-replica coherence?
**A:** No. Storage also needs compatible serialization, versioned keys and coordinated tag invalidation, including a way for instances to learn about invalidations made elsewhere. Test failure, concurrent regeneration and rollback on the actual deployment topology.

## Summary

Revisit the linked chapter when an answer misses the mechanism, a boundary or a failure case.

---

## See Also

- [Section reading order](INDEX.md)

## References & Learn More

The source chapters above contain the technical references for these answers.
