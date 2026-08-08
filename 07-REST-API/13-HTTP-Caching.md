---
section: REST API
category: Backend
tags: [concept]
---

# HTTP Caching Strategies

> **TL;DR:** HTTP caching is the cheapest performance win in a REST API — get it right and you serve a million requests from CDN edge. The three knobs are `Cache-Control` (directive), `ETag` (validator), and `Last-Modified` (timestamp); the senior test is the difference between strong and weak ETags, public vs private caches, and stale-while-revalidate patterns.
>
> **Why it matters:** This is a Backend interview topic you will be asked about at the senior level (5+ YoE) — not for definition recall, but for tradeoffs, production failure modes, and the ability to compare it against alternatives.

## Definition

HTTP caching is the protocol-level mechanism that lets clients, proxies, and CDNs reuse prior responses without re-fetching from the origin. The cache directives live in the `Cache-Control` header (e.g., `public, max-age=60, stale-while-revalidate=30`), with `ETag` and `Last-Modified` as validators that drive conditional requests (`If-None-Match`, `If-Modified-Since`). The senior design choice is which responses are cacheable, for how long, by whom (public CDN vs private browser), and what to do when stale.

## Why Do We Need It?

1. **Latency** — A CDN-edge cache serves a 200 in 5ms; an origin roundtrip is 50–200ms.
2. **Origin cost** — A cache hit saves DB + app + serialization work; at scale this is the difference between 10 servers and 1000.
3. **Reliability** — When the origin is down, a stale cache is better than a 503.
4. **Bandwidth** — `304 Not Modified` responses can be empty — saves bytes on the wire.
5. **User experience** — Repeat requests are instant; users perceive the app as fast.
6. **Correctness contract** — Caching is part of the API contract; clients know what they can rely on.
7. **Stale-while-revalidate** — Serves stale data immediately, refreshes in the background — the right balance for most read APIs.

## How It Works

```text
Client                                   CDN / Proxy                                Origin
  │                                            │                                       │
  │  GET /products/42                           │                                       │
  │───────────────────────────────────────────>│                                       │
  │                                            │  Cache miss / stale                   │
  │                                            │──────────────────────────────────────>│
  │                                            │<──────────────────────────────────────│
  │                                            │  200 OK                               │
  │                                            │  Cache-Control: public, max-age=60     │
  │                                            │  ETag: "abc123"                       │
  │<───────────────────────────────────────────│                                       │
  │  200 OK                                    │                                       │
  │  ETag stored                               │                                       │
  │                                            │                                       │
  │  T+30s, GET /products/42                   │                                       │
  │  If-None-Match: "abc123"                   │                                       │
  │───────────────────────────────────────────>│                                       │
  │                                            │  Cache hit (still fresh)              │
  │<───────────────────────────────────────────│                                       │
  │  304 Not Modified                          │                                       │
  │  (no body, just headers)                   │                                       │
```

## Code Examples

### Strong ETag + Cache-Control in NestJS

```typescript
// products.controller.ts
import { Controller, Get, Param, Res, Header } from '@nestjs/common';
import { Response } from 'express';
import * as etag from 'etag';
import * as crypto from 'crypto';

@Controller('products')
export class ProductsController {
  @Get(':id')
  async getOne(@Param('id') id: string, @Res({ passthrough: true }) res: Response) {
    const product = await this.productsService.getById(id);
    const body = JSON.stringify(product);

    // Strong ETag from a hash of the body
    const tag = etag(body);
    res.setHeader('ETag', tag);
    res.setHeader('Cache-Control', 'public, max-age=60, stale-while-revalidate=30');

    // Conditional request: 304 if client already has this version
    if (res.req.headers['if-none-match'] === tag) {
      res.status(304);
      return;                       // empty body
    }
    return product;
  }
}
```

### Weak ETag from a Versioned Resource

```typescript
// When the body is large or recomputing the hash is expensive,
// use a weak ETag derived from a version / updated_at column.
@Get(':id')
async getOne(@Param('id') id: string) {
  const p = await this.productsService.getById(id);
  return {
    ...p,
    headers: {
      ETag: `W/"${p.version}"`,                            // weak
      'Cache-Control': 'public, max-age=300',
    },
  };
}
```

### Private vs Public Cache

```typescript
// Public — CDNs and proxies may store
res.setHeader('Cache-Control', 'public, max-age=300, s-maxage=3600');

// Private — only the end-user's browser may store (user-specific data)
res.setHeader('Cache-Control', 'private, max-age=60');

// No store — never cache (sensitive responses)
res.setHeader('Cache-Control', 'no-store');
```

### Stale-While-Revalidate

```typescript
// Serve stale up to N seconds while a background refresh happens.
// Best UX: instant response on repeat hits, eventual consistency.
res.setHeader(
  'Cache-Control',
  'public, max-age=60, stale-while-revalidate=600',
);
```

### `Vary` for Content Negotiation

```typescript
// Cache separate copies per Accept-Language or Authorization bucket.
@Get('feed')
async feed(@Headers('accept-language') lang: string, @Res({ passthrough: true }) res: Response) {
  res.setHeader('Vary', 'Accept-Language, Authorization');
  res.setHeader('Cache-Control', 'private, max-age=60');
  return this.feedService.forLang(lang);
}
```

### Cache Invalidation on Write

```typescript
// orders.service.ts
async placeOrder(dto: PlaceOrderDto) {
  const order = await this.ordersRepo.create(dto);
  // Bust the affected cache keys (CDN purge + local)
  await this.cache.bust(`user:${dto.userId}:orders`);
  await this.cdn.purge(`/users/${dto.userId}/orders*`);
  return order;
}
```

### Conditional PUT with If-Match

```typescript
@Put(':id')
async update(
  @Param('id') id: string,
  @Body() dto: UpdateDto,
  @Headers('if-match') ifMatch: string,
) {
  const current = await this.productsService.getById(id);
  if (ifMatch && ifMatch !== current.etag) {
    throw new PreconditionFailedException('Resource has changed');
  }
  return this.productsService.update(id, dto);
}
```

## Real-World Use Cases

1. **Public product catalog** — `Cache-Control: public, max-age=300, s-maxage=3600, stale-while-revalidate=86400`; CDN-edge serves 95% of reads.
2. **User-specific feeds** — `Cache-Control: private, max-age=60` so the browser caches, but no proxy does.
3. **Search results** — `Cache-Control: public, max-age=10, stale-while-revalidate=30`; quick to refresh, never very stale.
4. **Pricing/availability** — Strong ETag + short `max-age=0, must-revalidate`; always revalidate to avoid overselling.
5. **Static-like endpoints (categories, tags)** — Long `max-age` (1 day) with `immutable` if the response is truly immutable.
6. **Logout / auth changes** — `Cache-Control: no-store` and bust auth-related keys.
7. **Hot dashboards** — `stale-while-revalidate` keeps the dashboard fast; the data is allowed to be a few seconds stale.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Caching authenticated responses as `public` | Use `private` for user-specific responses; `public` only for anonymous-shared data |
| No `Vary` on language/authorization | Add `Vary: Accept-Language, Authorization` so caches don't return the wrong language/user |
| Cache busting by URL `?v=N` everywhere | Use proper ETag + `If-None-Match`; URL versioning hurts cacheability |
| Caching `Set-Cookie` responses as `public` | `Set-Cookie` implies `private`; respect it |
| Returning 200 + same body instead of 304 | Send 304 with no body on `If-None-Match` match — saves bytes and CPU |
| Forgetting `Vary: Origin` with CORS | Add `Vary: Origin` to prevent serving a CORS response to the wrong origin |
| Long `max-age` on personalized data | Personal data: `private, max-age=0, must-revalidate`; trust client, revalidate every time |
| Caching error responses | `Cache-Control: no-store` on 4xx/5xx; otherwise a transient failure becomes a long-lived cached failure |
| Using strong ETag for rapidly-changing resources | Use weak ETag (`W/"…"`) or just `Last-Modified` |
| `s-maxage=0` accidentally in front of CDN | Know the difference: `max-age` = browser, `s-maxage` = shared cache (CDN) |

## Best Practices

1. **Default to `no-store` for sensitive data** — Auth tokens, PII, account state.
2. **`public, max-age=N, s-maxage=M`** — For shared cacheable resources; `s-maxage` lets you tune CDN separately from browser.
3. **ETag for every GET that varies** — Strong when the body is small, weak when it is large/expensive.
4. **Send 304, not 200, on `If-None-Match` matches** — Empty body, just headers.
5. **`Vary` on every header that affects the body** — `Accept-Language`, `Authorization`, `Origin`, `Accept-Encoding`.
6. **Cache-bust on writes** — Either purge the affected keys or include a version number in the URL.
7. **Stale-while-revalidate for read-heavy endpoints** — `max-age=60, stale-while-revalidate=600` is a great default for product/listing endpoints.
8. **`must-revalidate` for safety** — Prevents a stale response from being served after a network partition.
9. **Document the cache contract in OpenAPI** — Response headers are part of the API contract; document them.
10. **Monitor cache hit ratio** — Origin `cache_status: HIT` / `MISS` headers from your CDN; alert when the ratio drops.

## Performance Considerations

- A cache hit is 1000× cheaper than an origin roundtrip — this is the highest-leverage perf knob in any API.
- `stale-while-revalidate` reduces p99 latency on repeat requests to near-zero.
- CDN-edge cache lives in POPs worldwide; cold-start latency from a far-flung user can still be 100ms.
- `Vary: Accept-Encoding` (gzip/brotli) and `Vary: Accept-Language` multiply cache storage linearly — keep variation small.
- `max-age=0, must-revalidate` still costs a request — use `ETag` + `If-None-Match` to make that request a 304.
- Don't cache responses larger than 1MB at edge — they break CDN memory budgets.

## Summary

- HTTP caching is the highest-leverage perf knob in any REST API; design it deliberately.
- The three headers to know: `Cache-Control` (policy), `ETag` (validator), `Vary` (content negotiation).
- `public, max-age=N, s-maxage=M, stale-while-revalidate=K` is the workhorse pattern for read endpoints.
- Send `304 Not Modified` on `If-None-Match` matches — empty body, just headers.
- Never cache `Set-Cookie` responses, personalized data, or error bodies.

## Cheat Sheet

| Concept | Description |
|---------|-------------|
| `Cache-Control: public` | Any cache (browser, CDN, proxy) may store |
| `Cache-Control: private` | Only the end-user's browser may store |
| `Cache-Control: no-store` | Never store |
| `Cache-Control: max-age=N` | Browser freshness window in seconds |
| `Cache-Control: s-maxage=N` | Shared cache (CDN) freshness window |
| `stale-while-revalidate=K` | Serve stale up to K seconds while revalidating in the background |
| `must-revalidate` | Don't serve stale once `max-age` has passed |
| `ETag: "abc"` | Strong validator; matches on byte-for-byte equality |
| `ETag: W/"abc"` | Weak validator; matches on semantic equivalence |
| `If-None-Match` | Client tells server which ETags it has; server returns 304 if match |
| `Last-Modified` + `If-Modified-Since` | Time-based validator pair |
| `Vary: Accept-Language` | Cache separate copies per language |
| `Vary: Authorization` | Don't serve user-A's response to user-B |
| `304 Not Modified` | Empty body; tells client to reuse its cache |
| Cache busting | Purge affected keys on write, or version the URL |

---

## See Also
- [Microservices](../12-Microservices/) (per-service cache invalidation)
- [NestJS](../06-NestJS/) (interceptors for caching responses)
- [Security](../09-Security/) (don't cache sensitive data)
- [System Design](../11-System-Design/) (caching in API design)

## References & Learn More

- [MDN — HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [RFC 9111 — HTTP Caching](https://datatracker.ietf.org/doc/html/rfc9111)
- [RFC 7232 — Conditional Requests (ETag, If-None-Match)](https://datatracker.ietf.org/doc/html/rfc7232)
- [Google — HTTP Cache](https://web.dev/articles/http-cache)
- [Fastly — Caching Best Practices](https://www.fastly.com/blog/5-tips-for-supercharging-your-caching-strategy)
- [httperf / WebPageTest — measuring cache hits](https://www.webpagetest.org/)
