<!-- section: REST APIs | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-REST%20APIs-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# REST APIs — Http Mechanics Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## HTTP Methods

Source: [HTTP Methods](20.3.2.01-http-methods.md)

**Q:** What core constraint explains why safe and idempotent are load-bearing promises. governs http methods?

**A:** A retry layer cannot know your code — it only knows the method. GET/HEAD must be safe and PUT/DELETE idempotent *because the network retries and proxies pre-fetch*; violate the promise and retries corrupt data.

**Q:** What core constraint explains why post is the escape hatch, so it needs help. governs http methods?

**A:** POST is neither safe nor idempotent — which is exactly why client-generated idempotency keys exist: they give a non-idempotent method the retry-safety it otherwise lacks.

**Q:** What core constraint explains why method ≠ crud dogma. governs http methods?

**A:** The method encodes the *semantics of the interaction* (replace vs partial-modify: PUT vs PATCH), not a mapping onto database operations. Designing "PUT = SQL UPDATE" produces APIs that lie to intermediaries.

## HTTP Status Codes

Source: [HTTP Status Codes](20.3.2.02-status-codes.md)

**Q:** What core constraint explains why a cache, proxy, or browser sees only the status line. governs http status codes?

**A:** It must decide "retryable? cacheable? redirect?" from three digits — so the classes encode exactly those decisions: 1xx informational, 2xx success, 3xx redirect (cacheable by default!), 4xx client's fault, 5xx server's fault.

**Q:** What core constraint explains why 4xx vs 5xx is the retry contract. governs http status codes?

**A:** Retrying a 400 changes nothing; retrying a 503 might. Clients and load balancers build policies on this line, so returning 500 for validation errors breaks automation everywhere.

**Q:** What core constraint explains why precision below the class is for clients, not humans. governs http status codes?

**A:** 401 vs 403 ("who are you" vs "not allowed"), 404 vs 410 ("missing" vs "gone forever") exist so machines branch correctly — picking "close enough" codes destroys that.

## CORS (Cross-Origin Resource Sharing)

Source: [CORS (Cross-Origin Resource Sharing)](20.3.2.03-cors.md)

**Q:** What core constraint explains why scripts run with the user's authority. governs cors (cross-origin resource sharing)?

**A:** Code from evil.com executing in your browser sends requests *with the user's cookies* — the browser must distinguish "user navigated there" from "some other site's code asked." Same-origin policy is that wall.

**Q:** What core constraint explains why the wall needs a door, so the server holds the key. governs cors (cross-origin resource sharing)?

**A:** CORS is not a security feature the server configures *for* itself; it's the server *opting in* to letting other origins read responses the browser would block. The preflight is the browser asking "may I?" before a non-simple request.

**Q:** What core constraint explains why enforcement lives in the browser, so curl doesn't care. governs cors (cross-origin resource sharing)?

**A:** That's why CORS misconfigurations are invisible to Postman and why "it works in curl" proves nothing — and why `Access-Control-Allow-Origin: *` with credentials is impossible by construction.

## HTTP Caching Strategies

Source: [HTTP Caching Strategies](20.3.2.04-http-caching.md)

**Q:** What core constraint explains why freshness: don't ask at all. governs http caching strategies?

**A:** `Cache-Control` max-age lets the client answer from its own store without touching the network. This is the only strategy with zero latency and zero load; everything else is a refinement of it.

**Q:** What core constraint explains why validation: ask cheaply. governs http caching strategies?

**A:** When freshness expires, `ETag`/`If-None-Match` lets the server answer "unchanged — 304, zero bytes" instead of resending the body. Freshness + validation compose: every cached response should carry both.

**Q:** What core constraint explains why correctness demands invalidation paths. governs http caching strategies?

**A:** Any cached representation can be stale after a write; hence explicit no-store for sensitive data, versioned URLs for deploy assets, and revalidation for everything else. Cache design is deciding *what staleness is acceptable where* — a product decision, not a header afterthought.

## Summary

Use these prompts after the reading pass to recall the http mechanics mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
