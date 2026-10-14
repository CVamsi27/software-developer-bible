<!-- section: CDN & Edge Computing | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-CDN%20%26%20Edge%20Computing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# CDN & Edge Computing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## CDN Architecture

Source: [CDN Architecture](40.10.01-cdn-architecture.md)

**Q:** Why can the cache key cause a data leak even when the origin authenticates?

**A:** A cache hit can bypass origin authentication. A per-user key prevents cross-user representation mixing but does not recheck an expired token, revoked grant or changed entitlement. Authorize each protected request before serving the hit, or bypass shared caching if the edge cannot check current permission.

**Q:** How does an origin shield differ from request collapsing during a popular-object miss?

**A:** An origin shield is an additional cache tier that can reuse objects across edge regions and reduce origin fetches. Request collapsing combines simultaneous misses for the same cache key at a cache node. Provider scope and eligibility differ; neither helps distinct keys or guarantees protection for uncacheable traffic. See [CloudFront Origin Shield](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/origin-shield.html) and [request collapsing](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/RequestAndResponseBehaviorCustomOrigin.html#simultaneous-requests-for-the-same-object-request-collapsing).

**Q:** Does using POST with no-store prove a patient response avoids sensitive processing at the edge?

**A:** No. Intermediaries may process bodies, headers and telemetry even without caching. Verify actual bypass rules, data flow, logs and applicable service obligations.

**Q:** New hashed JavaScript is published. Can the old asset and application programming interface (API) behavior immediately disappear?

**A:** No. Old tabs, HTML and service workers may still reference them. Keep the chosen compatibility/retention window; versioned identity does not update every client.

**Q:** How do you handle cache invalidation for a single-page application (SPA)?

**A:** Publish immutable versioned assets before references, select the HTML freshness/revalidation policy and retain old clients' supported assets/API behavior. Purge corrections under a verified recovery path.

**Q:** How do you prevent protected health information (PHI) from being cached at the CDN edge?

**A:** Use an explicit no-store/bypass policy and test every protected response path. Method choice is insufficient; validate keys/custom code, processing and telemetry obligations separately.

**Q:** Does HIPAA itself require all electronic PHI to stay in the United States?

**A:** HHS guidance states that HIPAA has no specific U.S.-location requirement for ePHI processed or stored by a cloud provider. Location still affects required risk analysis; other laws, contracts or organizational policy may impose stricter boundaries. Verify the actual processing, storage and support paths. See [HHS HIPAA and Cloud Computing guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/health-information-technology/cloud-computing/index.html).

## Multi-CDN Traffic Steering

Source: [Multi-CDN Traffic Steering](40.10.02-multi-cdn-traffic-steering.md)

**Q:** Why is a Domain Name System (DNS) time-to-live (TTL) not a guaranteed failover deadline?

**A:** The DNS answer is cached by recursive resolvers, while clients can reuse live connections. Some resolvers may serve stale data after expiry if they cannot refresh the authoritative answer. A shorter TTL can help a planned change but does not bound total user-visible convergence. See [RFC 8767](https://www.rfc-editor.org/rfc/rfc8767.html).

**Q:** Why warm a secondary CDN before deliberately shifting major traffic?

**A:** A cold secondary can surge a shared origin and have worse latency during failover. Verify cache policy, authorization, certificates, routing and origin capacity on the alternate path; warming helps where supported but does not guarantee every cache stays warm.

**Q:** A purge submits on A and fails on B. Is the operation atomic or worse than no purge by definition?

**A:** Neither. Record both statuses and the affected content risk, retry/reconcile B and verify each provider's completion. Partial success can matter; no global rollback is implied.

**Q:** Does an 80:20 DNS weight mean exactly eighty percent of users receive A?

**A:** No. A weight such as 80:20 is a relative share of eligible DNS answers under that provider's policy, not a guarantee about people, requests or bytes. Resolver caching, connection reuse, geography and retries change observed traffic. See [Route 53 weighted routing](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy-weighted.html) for one provider's contract.

**Q:** A successful-page real-user monitoring (RUM) dashboard says B is faster, but probes report more failures. Is that enough evidence to move traffic?

**A:** No. Page beacons can miss users whose requests fail before the page can report, making successful samples look faster. Compare the same audience/content cohorts, include success and error rates, test the unselected path synthetically, and verify shared-origin load before a controlled shift. See the [Server Timing specification](https://www.w3.org/TR/server-timing/) for the browser metric interface and its privacy boundary.

## Media Optimization at the Edge

Source: [Media Optimization at the Edge](40.10.03-media-optimization-at-the-edge.md)

**Q:** Why must format negotiation participate in cache identity?

**A:** Different `Accept` preferences can select different bytes at one URL. Return the matching `Vary: Accept` signal and configure the CDN key to include the selected format; verify both because downstream `Vary` does not configure every provider key. See [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-accept) and [Cloudflare's image format options](https://developers.cloudflare.com/images/optimization/features/).

**Q:** What do `srcset` and `sizes` tell a browser that one `src` cannot?

**A:** `srcset` offers image candidates with intrinsic widths; `sizes` describes the layout slot so the browser can choose a candidate for the viewport and display density. Keep intrinsic dimensions on the image to reserve layout space. See [MDN's responsive image guide](https://developer.mozilla.org/en-US/docs/Web/HTML/Guides/Responsive_images).

**Q:** A signature is verified only on a cache miss. What can happen when a cached hit is requested after token expiry?

**A:** The hit can bypass the expired grant unless authorization runs first for every request. Shared content identity and caller permission are separate. Set browser cache lifetime to fit the access policy; an edge check cannot stop reuse of an already cached local copy.

**Q:** Width 420 normalizes to bucket 480. Which width must the renderer use?

**A:** 480. Key and renderer inputs must match; otherwise one key can represent different bytes. Include source revision, transform-policy version and selected format in identity. See [Cloudflare's transform parameters](https://developers.cloudflare.com/images/optimization/features/) for one provider's option contract.

**Q:** Does Accept: image/avif;q=0 permit choosing AVIF by substring?

**A:** No. A quality value of zero means the representation is unacceptable. Parse `Accept` according to [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-accept) and preserve the resolved format in cache identity.

**Q:** Why reject malformed signature length before timingSafeEqual?

**A:** The API compares equal-length byte buffers and throws for unequal lengths. Validate encoded shape, decode to bytes and reject malformed grants before comparison. See [Node.js `timingSafeEqual`](https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b).

**Q:** Why give a live HLS manifest and its media segments different cache policies?

**A:** The live manifest changes as new segments become available, while versioned segments can remain immutable. Give each resource a freshness rule that matches its update behavior and access policy. Check the current [HLS authoring specification](https://developer.apple.com/documentation/http-live-streaming/hls-authoring-specification-for-apple-devices/) for playlist and device constraints.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
