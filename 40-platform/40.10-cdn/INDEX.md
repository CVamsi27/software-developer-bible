# CDN & Edge Computing — Index

> **Study time:** ≈ 35 min of reading (5 files, ~7 min average).
> **Content delivery networks, edge functions, cache invalidation, multi-CDN steering, media optimization and protected health information (PHI) considerations.**
>
> Read the three chapters in order: establish cache identity and freshness, add multi-provider failover, then follow image and video delivery. Finish with the separate revision questions to test each boundary.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Concept Categories (across the chapters)

| Category | What it covers | The one-line exam answer |
| ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Edge Caching** | Edge locations, origin shields, cache keys, time-to-live (TTL), stale-while-revalidate | Share only representations with explicit identity and freshness; isolate caller-specific responses or authorize every hit |
| **Invalidation & Versioning** | Tag/URL purge APIs, content-hashed URLs, deploy-time invalidation | Purge by the provider's exact selector contract; versioned assets avoid replacing bytes under an existing identity |
| **Edge Compute** | Cloudflare Workers and provider-specific edge runtimes | Put bounded logic at the edge when runtime, dependency latency and data authority fit the request contract |
| **Multi-CDN Steering** | Domain Name System (DNS), global server load balancing (GSLB), real-user monitoring (RUM), failover health checks and cost arbitration | Steer from measured user paths; test health detection, resolver/client behavior and cold-cache origin load before relying on failover |
| **Media at the Edge** | Responsive images, bounded transforms, HTTP Live Streaming (HLS)/Dynamic Adaptive Streaming over HTTP (DASH), signed access and delivery cost | Version the source and transform policy in the cache key; negotiate the correct format and authorize every protected hit |
| **Compliance & PHI** | Protected health information (PHI), sensitive logging, residency and provider processing | Include edge processing and telemetry in the data-flow analysis; cache only when authorization and applicable obligations are enforced |

---

## The Files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [40.10.01-cdn-architecture.md](40.10.01-cdn-architecture.md) | Content delivery network (CDN) caching strategies, invalidation, edge computing (Cloudflare Workers, Vercel Edge), protected health information (PHI), provider evaluation | Important | Specialized | 8 min |
| 02 | [40.10.02-multi-cdn-traffic-steering.md](40.10.02-multi-cdn-traffic-steering.md) | When a second provider pays off, DNS/client/managed steering, RUM and synthetic evidence, failover readiness, per-provider purge state and cost | Important | Specialized | 8 min |
| 03 | [40.10.03-media-optimization-at-the-edge.md](40.10.03-media-optimization-at-the-edge.md) | Responsive image selection, bounded transforms and versioned cache keys, signed access, HLS/DASH streaming with adaptive bitrate (ABR), manifest and segment freshness | Important | Specialized | 10 min |
| 04 | [Interview Questions](40.10.04-interview-questions.md) | Applied Q&A: cache-key design, purge strategy, origin shields, dynamic edge caching, media delivery, multi-CDN steering | Important | Specialized | 6 min |

---

## The Interview Answer in One Table

| Question | Answer spine |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What belongs at the edge? | Public immutable assets, explicitly shareable responses and bounded request logic whose dependencies and trust contract fit the edge |
| How should private or regulated data be handled? | Keep caller-specific responses out of shared caching unless every hit enforces authorization and the provider's processing, logging, retention and location obligations are satisfied |
| How do you invalidate? | Use provider-specific selectors and completion checks; publish immutable hashed assets before referencing HTML, and use short freshness only where stale behavior is acceptable |
| Why multi-CDN? | Use measured path and availability evidence to justify resilience or regional performance; include steering lag, cache coldness and egress cost |
| How do you serve media fast? | Select responsive images, key bounded transforms by source and policy version, authorize protected hits, and give manifests and segments separate freshness policies |
| Real example to cite | Publish new hashed assets before HTML references them, retain old assets through client overlap, and verify rollback and origin load |

---

## Reading Passes

- **Before any system-design interview with a "global users" angle** — pairs with [HTTP caching](../../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md)
- Chapter 01 first (8 min); chapters 02/03 for scale-, cost-, or media-heavy roles
- Skim the provider evaluation criteria if pressed for time

## Common interview questions

- "How does a CDN know what to cache for an API response?"
- "A deploy just shipped — how do users get the new JavaScript bundle without stale chunks?"
- "Where does edge computing fit vs a traditional origin server?"
- "How would you serve European Union-only data under a stated processing-location requirement?" (actual service/data-flow contract)
- "Why run two CDNs? How do you decide who serves which user?" (steering + RUM)
- "How do you stop one visitor's optimized image being served to everyone?" (normalize transform inputs and ensure negotiated format and authorization are reflected in the cache policy)

---

## Cross-references

[Serverless & Edge](../40.7-serverless-edge/INDEX.md) · [HTTP caching](../../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md) · [Caching stack](../../20-backend/20.8-caching/INDEX.md) · [CDN architecture (system-design view)](../../30-architecture/30.3-infra-patterns/04-data-at-scale/30.3.4.03-cdn-architecture.md)

---

## Navigation

[← Previous: Twelve-Factor](../40.9-twelve-factor/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Quality →](../../50-quality/INDEX.md)

---

## Docita Anchor

Existing [Docita](https://github.com/CVamsi27/docita) pointers locate related Cloudflare configuration. Verify deployed routing/cache/trust behavior before using them as operational evidence.

| Topic | Docita evidence |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CDN in front of origin | Cloudflare sits before the Fly API: `shared/common/http/cloudflare-ips.ts` trusts CF for real client IPs |
| Origin protection | ADR 0014 locks the API to accept only Cloudflare-sourced traffic — inspect deployed source/authentication policy; the ADR alone does not prove all bypasses are blocked |
| Edge-hosted assets | `apps/landing` builds to Cloudflare Workers (`wrangler deploy`, `_worker.js`) behind the `DOCITA_CLOUDFLARE` build flag |
| Multi-CDN / media transforms | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
