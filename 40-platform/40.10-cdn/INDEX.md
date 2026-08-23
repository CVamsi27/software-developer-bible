# CDN & Edge Computing

> **Content delivery networks, edge functions, cache invalidation, healthcare PHI considerations.**

[![Files](https://img.shields.io/badge/files-1-blue)](../../INDEX.md)

## Contents

| File | Topics |
|------|--------|
| [40.10.01-cdn-architecture.md](40.10.01-cdn-architecture.md) | CDN caching strategies, cache invalidation, edge computing (Cloudflare Workers, Vercel Edge), healthcare PHI considerations, provider comparison |

## The Interview Answer in One Table

| Question | Answer spine |
|----------|--------------|
| What belongs at the edge? | Static assets, cached API responses, auth-adjacent routing — anything compute-light and latency-sensitive |
| What never goes there? | Per-request personalized/regulated data processing without a clear caching key and scrubbing story |
| How do you invalidate? | Tag/purge APIs, versioned URLs (`app.[hash].js`), short TTL + SWR for semi-dynamic |
| Real example to cite | SPA assets on Cloudflare Workers + ~50KB same-origin proxy worker (Docita topology) |

## Cross-references

[Serverless & Edge](../40.7-serverless-edge/INDEX.md) · [HTTP caching](../../20-backend/20.3-rest-apis/20.3.13-http-caching.md) · [Caching stack](../../20-backend/20.8-caching/INDEX.md)

---

## Navigation

[← Previous: Twelve-Factor](../40.9-twelve-factor/INDEX.md) · [🏠 Back to Index](../../INDEX.md)
