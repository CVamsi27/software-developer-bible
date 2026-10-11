# CDN & Edge Computing — Index

> **Study time:** ≈ 34 min of reading (5 files, ~7 min average).
> **Content delivery networks, edge functions, cache invalidation, multi-CDN steering, media optimization, healthcare PHI considerations.**
>
> Three deep chapters, but the *concepts inside them* classify like a pattern catalog. Follow each mechanism, then test a changed condition in the separate revision.

[![Files](https://img.shields.io/badge/files-5-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Concept Categories (across the chapters)

| Category | What it covers | The one-line exam answer |
| ----------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Edge Caching** | PoPs, origin shielding, cache keys, TTL/SWR, stale-while-revalidate | Static + cacheable API responses live at the edge; everything needs a cache key |
| **Invalidation & Versioning** | Tag/purge APIs, content-hashed URLs, deploy-time invalidation | Purge under verified provider semantics; versioned assets avoid overwriting an identity |
| **Edge Compute** | Cloudflare Workers and provider-specific edge runtimes | Routing or bounded request logic under a measured runtime and data-authority contract |
| **Multi-CDN Steering** | DNS/GSLB, RUM-based weights, failover health checks, cost arbitration | Steer by measured per-region performance; failover needs warm caches + short TTLs |
| **Media at the Edge** | Image CDNs, AVIF/WebP negotiation, HLS/DASH ladders, signed URLs | Transform on the fly; format must be part of the cache key |
| **Compliance & PHI** | Regulated data at the edge, scrubbing, residency | Per-request personalized/regulated processing stays at origin unless you have a caching-key + scrubbing story |

---

## The Files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [40.10.01-cdn-architecture.md](40.10.01-cdn-architecture.md) | CDN caching strategies, cache invalidation, edge computing (Cloudflare Workers, Vercel Edge), healthcare PHI considerations, provider evaluation criteria | Important | Specialized | 7 min |
| 02 | [40.10.02-multi-cdn-traffic-steering.md](40.10.02-multi-cdn-traffic-steering.md) | Why multi-CDN, DNS/GSLB vs RUM vs edge-orchestrator steering, failover hazards, cross-CDN invalidation, cost arbitration, measurement infrastructure | Important | Specialized | 11 min |
| 03 | [40.10.03-media-optimization-at-the-edge.md](40.10.03-media-optimization-at-the-edge.md) | Image CDNs (on-the-fly transforms), AVIF/WebP negotiation, HLS/DASH ABR ladders, origin shields, signed URLs/hotlink protection, transformation cache keys, cost levers | Important | Specialized | 8 min |
| 04 | [Interview Questions](40.10.04-interview-questions.md) | Applied Q&A: cache-key design, purge strategy, origin shields, dynamic edge caching, media delivery, multi-CDN steering | Important | Specialized | 6 min |

---

## The Interview Answer in One Table

| Question | Answer spine |
| ------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| What belongs at the edge? | Static assets, cached API responses, auth-adjacent routing — anything compute-light and latency-sensitive |
| How should private or regulated data be handled? | Keep personalized responses out of shared caching unless authorization, processing, logging, and residency policies permit it; edge computation still needs those controls |
| How do you invalidate? | Tag/purge APIs, versioned URLs (`app.[hash].js`), short TTL + SWR for semi-dynamic |
| Why multi-CDN? | Resilience to provider outages, per-region performance wins, egress cost arbitrage — proven with RUM data |
| How do you serve media fast? | Edge image transforms + format negotiation; video as CMAF/HLS-DASH ladders behind origin shields |
| Real example to cite | A Vite SPA's static assets and explicitly routed API proxy; verify the deployed trust boundary and measured bundle size |

---

## Reading Passes

- **Before any system-design interview with a "global users" angle** — pairs with [HTTP caching](../../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md)
- Chapter 01 first (7 min); chapters 02/03 for scale-, cost-, or media-heavy roles
- Skim the provider evaluation criteria if pressed for time

## Common interview questions

- "How does a CDN know what to cache for an API response?"
- "A deploy just shipped — how do users get the new JS bundle without stale chunks?"
- "Where does edge computing fit vs a traditional origin server?"
- "How would you serve EU-only data under a stated processing-location requirement?" (actual service/data-flow contract)
- "Why run two CDNs? How do you decide who serves which user?" (steering + RUM)
- "How do you stop one visitor's optimized image being served to everyone?" (`Vary: Accept` / cache-key rules)

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
