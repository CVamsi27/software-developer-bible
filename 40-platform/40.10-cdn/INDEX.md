# CDN & Edge Computing — Index

> **Content delivery networks, edge functions, cache invalidation, healthcare PHI considerations.**
>
> One deep chapter, but the *concepts inside it* classify like a pattern catalog. Learn the four concept groups below and you can answer any edge question.

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Concept Categories (within the chapter)

| Category | What it covers | The one-line exam answer |
|----------|----------------|--------------------------|
| **Edge Caching** | PoPs, origin shielding, cache keys, TTL/SWR, stale-while-revalidate | Static + cacheable API responses live at the edge; everything needs a cache key |
| **Invalidation & Versioning** | Tag/purge APIs, content-hashed URLs, deploy-time invalidation | You can't delete what the CDN already cached — version URLs instead |
| **Edge Compute** | Cloudflare Workers, Vercel Edge, compute-light request handling | Auth-adjacent routing, A/B, rewrites at the edge — never heavy stateful work |
| **Compliance & PHI** | Regulated data at the edge, scrubbing, residency | Per-request personalized/regulated processing stays at origin unless you have a caching-key + scrubbing story |

---

## The File

| File | Topics | Read time |
|------|--------|----------:|
| [40.10.01-cdn-architecture.md](40.10.01-cdn-architecture.md) | CDN caching strategies, cache invalidation, edge computing (Cloudflare Workers, Vercel Edge), healthcare PHI considerations, provider comparison | 45 min |

## The Interview Answer in One Table

| Question | Answer spine |
|----------|--------------|
| What belongs at the edge? | Static assets, cached API responses, auth-adjacent routing — anything compute-light and latency-sensitive |
| What never goes there? | Per-request personalized/regulated data processing without a clear caching key and scrubbing story |
| How do you invalidate? | Tag/purge APIs, versioned URLs (`app.[hash].js`), short TTL + SWR for semi-dynamic |
| Real example to cite | SPA assets on Cloudflare Workers + ~50KB same-origin proxy worker (Docita topology) |

---

## When to read

- **Before any system-design interview with a "global users" angle** — pairs with [HTTP caching](../../20-backend/20.3-rest-apis/20.3.13-http-caching.md)
- 45 min read; skim the provider comparison if pressed for time

## Common interview questions

- "How does a CDN know what to cache for an API response?"
- "A deploy just shipped — how do users get the new JS bundle without stale chunks?"
- "Where does edge computing fit vs a traditional origin server?"
- "How would you serve EU-only data under GDPR?" (residency + purge story)

---

## Cross-references

[Serverless & Edge](../40.7-serverless-edge/INDEX.md) · [HTTP caching](../../20-backend/20.3-rest-apis/20.3.13-http-caching.md) · [Caching stack](../../20-backend/20.8-caching/INDEX.md) · [CDN architecture (system-design view)](../../30-architecture/30.3-infra-patterns/30.3.07-cdn-architecture.md)

---

## Navigation

[← Previous: Twelve-Factor](../40.9-twelve-factor/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Quality →](../../50-quality/INDEX.md)
