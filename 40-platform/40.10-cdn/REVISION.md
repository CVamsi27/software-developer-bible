<!-- section: CDN & Edge Computing | category: Reference | tags: revision, practice | role-priority: important | general-importance: specialized -->
[![Section](https://img.shields.io/badge/section-CDN%20%26%20Edge%20Computing-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-lightgrey)](#)
[![Tags](https://img.shields.io/badge/tags-revision%20%C2%B7%20practice-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)

# CDN & Edge Computing — Section Revision

Read the chapters in the [section learning flow](INDEX.md), then close them and work through these prompts. Explain the mechanism before checking an answer; return to the linked chapter when the reasoning is incomplete.

## CDN Architecture

Source: [CDN Architecture](40.10.01-cdn-architecture.md)

**Q:** Why can the cache key cause a data leak even when the origin authenticates?

**A:** A shared cached response can bypass the origin on later hits. Keying and caching policy must distinguish authorized variants or exclude personalized responses.

**Q:** What does an origin shield protect during a popular-object miss?

**A:** It aggregates/coalesces eligible misses before the origin. It does not repair uncacheable traffic or compensate for a wrong key/TTL policy.

**Q:** Does using POST with no-store prove a patient response avoids sensitive processing at the edge?

**A:** No. Intermediaries may process bodies, headers and telemetry even without caching. Verify actual bypass rules, data flow, logs and applicable service obligations.

**Q:** New hashed JS is published. Can the old asset and API behavior immediately disappear?

**A:** No. Old tabs/HTML/service workers may still reference them. Keep the chosen compatibility/retention window; versioned identity does not update every client.

**Q:** How do you handle cache invalidation for a SPA?

**A:** Publish immutable versioned assets before references, select the HTML freshness/revalidation policy and retain old clients' supported assets/API behavior. Purge corrections under a verified recovery path.

**Q:** How do you prevent PHI from being cached at the CDN edge?

**A:** Use an explicit no-store/bypass policy and test every protected response path. Method choice is insufficient; validate keys/custom code, processing and telemetry obligations separately.

## Multi-CDN Traffic Steering

Source: [Multi-CDN Traffic Steering](40.10.02-multi-cdn-traffic-steering.md)

**Q:** Why is a DNS TTL not a guaranteed failover deadline?

**A:** Resolver/client caches, connection reuse, propagation, and health detection also affect when traffic moves. Validate behavior from the users' paths.

**Q:** Why warm a secondary CDN before deliberately shifting major traffic?

**A:** A cold secondary can surge the origin and have worse latency during failover. Health, cache policy, certificates, and routing need parity before the switch.

**Q:** A purge submits on A and fails on B. Is the operation atomic or worse than no purge by definition?

**A:** Neither. Record both statuses and the affected content risk, retry/reconcile B and verify each provider's completion. Partial success can matter; no global rollback is implied.

**Q:** Does an 80:20 DNS weight mean exactly eighty percent of users receive A?

**A:** No. It affects eligible DNS answer selection. Resolver caching, user grouping, live connections and health policy change observed request/byte shares.

## Media Optimization at the Edge

Source: [Media Optimization at the Edge](40.10.03-media-optimization-at-the-edge.md)

**Q:** Why must format negotiation participate in cache identity?

**A:** Different Accept capabilities may select different representations at the same URL. A matching Vary/key rule keeps caches from serving the wrong variant.

**Q:** A valid signature is checked only on a cache miss. What happens on a hit after expiry?

**A:** The hit can bypass the expired grant unless authorization runs first for every request. Shared content identity and caller permission are separate.

**Q:** Width 420 normalizes to bucket 480. Which width must the renderer use?

**A:** 480. Key and renderer inputs must match; otherwise one key can represent different bytes. Source/transform version and selected format also participate.

**Q:** Does Accept: image/avif;q=0 permit choosing AVIF by substring?

**A:** No. q=0 excludes that representation. Use supported negotiation and preserve the resolved format in cache identity.

**Q:** Why reject malformed signature length before timingSafeEqual?

**A:** The API compares equal-length byte buffers and throws for unequal lengths. Validate encoded shape, decode to bytes and reject malformed grants before comparison.

## Summary

Use the answers to check your reasoning, then revisit the source mechanism and reproduce any relevant example without copying it. A remembered label is useful only when you can explain its limits.

## See Also

- [Section learning flow](INDEX.md)

## References & Learn More

The source chapter links above contain the implementation examples and primary references for each prompt.
