<!-- section: REST APIs | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
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

**Q:** How do safety and idempotence affect caching and retries?

**A:** Safety means no intended state change; idempotence means repeating an identical request has the same intended effect. These properties inform retries, while cacheability additionally depends on response status and headers.

**Q:** How can a POST operation support duplicate-safe retry?

**A:** Define an idempotency-key contract and atomically record the key with the protected outcome. Reject mismatched reuse and retain state for the permitted retry window; POST itself does not promise idempotence.

**Q:** Why does choosing an HTTP method require more than mapping it to a CRUD label?

**A:** The method describes interaction semantics, such as replacement versus partial modification. It does not dictate whether the server executes a SQL INSERT or UPDATE.

## HTTP Status Codes

Source: [HTTP Status Codes](20.3.2.02-status-codes.md)

**Q:** How do status codes guide browsers, proxies and clients?

**A:** The first digit gives a broad outcome class. The specific status, method, headers and application contract determine caching, redirection and retry behavior.

**Q:** Why is the 4xx or 5xx class insufficient by itself to decide whether to retry?

**A:** Some 4xx responses are retryable after a condition changes, and some 5xx failures persist. Check operation idempotence, Retry-After, attempt limits and the documented failure meaning.

**Q:** When should an API use a specific status code rather than a generic error?

**A:** Use the code whose semantics match the outcome so clients can branch predictably. For example, 401 requires authentication handling, while 403 describes refusal; the response body supplies application detail.

## CORS (Cross-Origin Resource Sharing)

Source: [CORS (Cross-Origin Resource Sharing)](20.3.2.03-cors.md)

**Q:** Why does a browser restrict scripts from reading another origin's responses?

**A:** A script running under one origin must not automatically read private responses from another origin. Browsers apply the same-origin policy even when the user can navigate to both sites.

**Q:** How does a server permit selected cross-origin access?

**A:** Return the applicable CORS headers for allowed origins, methods and headers. Certain requests need preflight; authentication and authorization still apply to the actual request.

**Q:** Why can a request succeed in curl but be unreadable to browser JavaScript?

**A:** curl does not enforce browser origin policy. A browser can send a request yet withhold its response from JavaScript; credentialed CORS also cannot use a wildcard allowed origin.

## HTTP Caching Strategies

Source: [HTTP Caching Strategies](20.3.2.04-http-caching.md)

**Q:** How does freshness let a cache reuse a response without contacting the origin?

**A:** A fresh reusable response can be served from the relevant cache without revalidation. Lookup, transfer and rendering still have costs; this reduces origin traffic rather than creating literally zero latency.

**Q:** How do validators reduce transfer when a cached response becomes stale?

**A:** A conditional request can receive 304 when the stored representation remains valid, avoiding retransmission of its body. The response still carries headers, and validators are useful only when the response policy permits reuse.

**Q:** Which invalidation paths must a caching design account for?

**A:** Consider writes, permission changes, representation variants and deployment changes. Choose a key and freshness, validation or purge policy that match the tolerated stale-data window.

## HTTP retry and concurrency boundaries

Source: [Learning chapter](20.3.2.01-http-methods.md)

**Q:** Can an idempotent DELETE return 204 and then 404?

**A:** Yes. Its intended effect remains removal; response equality is not the idempotency contract.

**Q:** Why does an idempotent PUT still need If-Match?

**A:** Repeating one replacement is safe under the method contract, but two clients can overwrite each other. An atomic version precondition rejects an outdated write with 412.

## Response access and cache boundaries

Sources: [Status codes](20.3.2.02-status-codes.md), [CORS](20.3.2.03-cors.md), [HTTP caching](20.3.2.04-http-caching.md)

**Q:** Why can a report accepted with 202 later fail?

**A:** Acceptance records work for later processing; it is not its final outcome. Inspect the authorized status resource.

**Q:** What accompanies a 401 response for an authentication scheme?

**A:** An applicable WWW-Authenticate challenge; safe detail can explain the application's credential requirement.

**Q:** Can a cookie-bearing safelisted POST execute before CORS blocks reading its response?

**A:** Yes. Cookies do not by themselves require preflight. CORS cannot undo the effect or replace CSRF protection.

**Q:** Why does a JSON POST usually cause OPTIONS before the actual request?

**A:** Its Content-Type is not CORS-safelisted. The browser checks permitted method/header names, then checks the actual response too.

**Q:** Does no-cache prohibit storage?

**A:** No. It requires validation before reuse. No-store directs caches not to store the response.

**Q:** Why can a weak ETag validate GET but fail an If-Match write condition?

**A:** GET validation uses weak comparison; If-Match requires strong comparison.

**Q:** Does checking a version then awaiting an unrelated UPDATE prevent lost writes?

**A:** No. Another writer can change it in the gap. Check the expected version atomically with the update.

## Summary

Use these prompts after the reading pass to recall the http mechanics mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for caching, conditional requests and protocol behavior

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
