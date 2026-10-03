<!-- section: REST APIs | category: Reference | tags: revision| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-REST%20APIs-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# REST APIs — Edge And Scale Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## API Rate Limiting

Source: [API Rate Limiting](20.3.4.01-rate-limiting.md)

**Q:** What core constraint explains why every resource has a max sustainable rate governs api rate limiting?

**A:** (DB connections, CPU, downstream API quota). Without a gate, one client's burst degrades *everyone* — the limiter converts "the system collapsed" into "you got a 429," which is a survivable, diagnosable outcome.

**Q:** What core constraint explains why it must be decided at the edge. governs api rate limiting?

**A:** By the time a request reaches your business logic, it has already cost you. Counters must therefore be shared state (Redis) across instances — per-process in-memory counts are lies in a horizontally scaled deployment.

**Q:** What core constraint explains why the algorithm is a shape-of-burst decision. governs api rate limiting?

**A:** Fixed window is cheap but allows 2× bursts at boundaries; sliding window/token bucket smooths that at slightly higher bookkeeping cost. And a limiter without client-visible headers (X-RateLimit-Remaining, Retry-After) just produces mysterious failures.

## API Gateway Pattern

Source: [API Gateway Pattern](20.3.4.02-api-gateway.md)

**Q:** What core constraint explains why every concern that must apply to every request needs one enforcement point. governs api gateway pattern?

**A:** Auth, rate limiting, TLS termination, request logging — implementing them in each service guarantees drift and gaps. The gateway is the single choke point by construction.

**Q:** What core constraint explains why it buys uniformity at the price of a hop and a single point of failure governs api gateway pattern?

**A:** — which is why gateways must be horizontally scalable, config-as-code, and why latency-sensitive internal paths sometimes bypass it (service mesh is the answer for east-west traffic).

**Q:** What core constraint explains why routing is its real product. governs api gateway pattern?

**A:** Clients speak one stable surface (your domain); the gateway maps it onto a refactorable service topology — which is what decouples "clients deployed on their schedule" from "backend refactored on ours.".

## BFF — Backend for Frontend

Source: [BFF — Backend for Frontend](20.3.4.03-bff.md)

**Q:** What core constraint explains why one api cannot be optimal for many clients. governs bff — backend for frontend?

**A:** A mobile screen needs 3 fields in one round trip; a web dashboard needs a different aggregation; both hit the same services. Forcing them through one generic API produces either over-fetching or N+1 round trips — the mismatch is structural, not fixable by parameter tweaking.

**Q:** What core constraint explains why so give each client family its own aggregation layer. governs bff — backend for frontend?

**A:** The BFF is owned by the client team, speaks the client's shape, and calls downstream services. It's the recognition that *composition logic* is a real layer worth owning, not duplication.

**Q:** What core constraint explains why the cost is more deployables and the risk of logic drifting into the wrong bff governs bff — backend for frontend?

**A:** — which is why the rule is: BFFs aggregate and reshape, they don't own business rules.

## API Authentication

Source: [API Authentication](20.3.4.04-authentication.md)

**Q:** What core constraint explains why the server must verify a claim it didn't witness. governs api authentication?

**A:** "This is Vamsi" arrives over the wire; the proof is either *something only Vamsi has* presented again (a session token the server can look up) or *a cryptographic signature* the server can verify offline (JWT). Every credential scheme is one of these two, or a hybrid.

**Q:** What core constraint explains why verification state is the scaling decision. governs api authentication?

**A:** Sessions centralize state (revocation is instant; every request pays the lookup); self-contained tokens distribute it (verification is free; revocation requires lists or short TTLs). Neither dominates — the choice is which failure you can afford.

**Q:** What core constraint explains why transport and storage are part of the design, not afterthoughts. governs api authentication?

**A:** Credentials over TLS only, never in URLs (they leak via logs and Referer), and browser storage choice (cookie vs localStorage) determines your CSRF/XSS exposure — which is why auth and security chapters interlock.

## Summary

Use these prompts after the reading pass to recall the edge and scale mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
