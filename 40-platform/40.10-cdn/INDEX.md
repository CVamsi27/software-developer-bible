# CDN & Edge Computing — Index

> **Content delivery networks, edge functions, cache invalidation, multi-CDN steering, media optimization, healthcare PHI considerations.**
>
> Three deep chapters, but the *concepts inside them* classify like a pattern catalog. Learn the concept groups below and you can answer any edge question.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Concept Categories (across the chapters)

| Category | What it covers | The one-line exam answer |
|----------|----------------|--------------------------|
| **Edge Caching** | PoPs, origin shielding, cache keys, TTL/SWR, stale-while-revalidate | Static + cacheable API responses live at the edge; everything needs a cache key |
| **Invalidation & Versioning** | Tag/purge APIs, content-hashed URLs, deploy-time invalidation | You can't delete what the CDN already cached — version URLs instead |
| **Edge Compute** | Cloudflare Workers, Vercel Edge, compute-light request handling | Auth-adjacent routing, A/B, rewrites at the edge — never heavy stateful work |
| **Multi-CDN Steering** | DNS/GSLB, RUM-based weights, failover health checks, cost arbitration | Steer by measured per-region performance; failover needs warm caches + short TTLs |
| **Media at the Edge** | Image CDNs, AVIF/WebP negotiation, HLS/DASH ladders, signed URLs | Transform on the fly; format must be part of the cache key |
| **Compliance & PHI** | Regulated data at the edge, scrubbing, residency | Per-request personalized/regulated processing stays at origin unless you have a caching-key + scrubbing story |

---

## The Files

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [40.10.01-cdn-architecture.md](40.10.01-cdn-architecture.md) | CDN caching strategies, cache invalidation, edge computing (Cloudflare Workers, Vercel Edge), healthcare PHI considerations, provider comparison | 45 min |
| 02 | [40.10.02-multi-cdn-traffic-steering.md](40.10.02-multi-cdn-traffic-steering.md) | Why multi-CDN, DNS/GSLB vs RUM vs edge-orchestrator steering, failover hazards, cross-CDN invalidation, cost arbitration, measurement infrastructure | 30 min |
| 03 | [40.10.03-media-optimization-at-the-edge.md](40.10.03-media-optimization-at-the-edge.md) | Image CDNs (on-the-fly transforms), AVIF/WebP negotiation, HLS/DASH ABR ladders, origin shields, signed URLs/hotlink protection, transformation cache keys, cost levers | 30 min |

---

## The Interview Answer in One Table

| Question | Answer spine |
|----------|--------------|
| What belongs at the edge? | Static assets, cached API responses, auth-adjacent routing — anything compute-light and latency-sensitive |
| What never goes there? | Per-request personalized/regulated data processing without a clear caching key and scrubbing story |
| How do you invalidate? | Tag/purge APIs, versioned URLs (`app.[hash].js`), short TTL + SWR for semi-dynamic |
| Why multi-CDN? | Resilience to provider outages, per-region performance wins, egress cost arbitrage — proven with RUM data |
| How do you serve media fast? | Edge image transforms + format negotiation; video as CMAF/HLS-DASH ladders behind origin shields |
| Real example to cite | SPA assets on Cloudflare Workers + ~50KB same-origin proxy worker (Docita topology) |

---

## When to read

- **Before any system-design interview with a "global users" angle** — pairs with [HTTP caching](../../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md)
- Chapter 01 first (45 min); chapters 02/03 for scale-, cost-, or media-heavy roles
- Skim the provider comparison if pressed for time

## Common interview questions

- "How does a CDN know what to cache for an API response?"
- "A deploy just shipped — how do users get the new JS bundle without stale chunks?"
- "Where does edge computing fit vs a traditional origin server?"
- "How would you serve EU-only data under GDPR?" (residency + purge story)
- "Why run two CDNs? How do you decide who serves which user?" (steering + RUM)
- "How do you stop one visitor's optimized image being served to everyone?" (`Vary: Accept` / cache-key rules)

---

## Cross-references

[Serverless & Edge](../40.7-serverless-edge/INDEX.md) · [HTTP caching](../../20-backend/20.3-rest-apis/02-http-mechanics/20.3.2.04-http-caching.md) · [Caching stack](../../20-backend/20.8-caching/INDEX.md) · [CDN architecture (system-design view)](../../30-architecture/30.3-infra-patterns/04-data-at-scale/30.3.4.03-cdn-architecture.md)

---

## Navigation

[← Previous: Twelve-Factor](../40.9-twelve-factor/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Quality →](../../50-quality/INDEX.md)
