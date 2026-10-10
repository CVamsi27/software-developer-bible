<!-- section: REST APIs | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
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

**Q:** Why should admission limits reflect sustainable resource capacity?

**A:** Database slots, CPU and downstream quotas are finite. Admission protects those resources before a client's burst consumes capacity needed by others; choose limits from measured workload cost.

**Q:** Which limits belong at the edge and which need application-level enforcement?

**A:** The edge can reject coarse abuse early; application-level limits can enforce tenant, operation and downstream budgets. Global quotas need coordinated accounting, while local limits can deliberately protect each instance.

**Q:** How does a rate-limiting algorithm determine permitted bursts?

**A:** Fixed windows permit bursts near boundaries; sliding windows and token buckets have different burst and bookkeeping behavior. Publish useful retry information and define behavior when shared counters fail.

## API Gateway Pattern

Source: [API Gateway Pattern](20.3.4.02-api-gateway.md)

**Q:** Why can shared edge concerns benefit from centralized enforcement?

**A:** A shared gateway can apply TLS termination, coarse admission and logging consistently. Services still need resource-specific authorization and safe behavior when traffic reaches them by another trusted path.

**Q:** What latency and availability costs does a gateway introduce?

**A:** The gateway adds a hop and another component whose saturation or failure can affect requests. Replicate it, bound work and deploy routing policy with observable rollback.

**Q:** How does gateway routing decouple clients from service topology?

**A:** Clients use a stable external surface while the gateway selects upstream services. Routing changes can move implementations without changing every client, provided the public contract remains compatible.

## BFF — Backend for Frontend

Source: [BFF — Backend for Frontend](20.3.4.03-bff.md)

**Q:** When do differing client needs justify separate API composition?

**A:** Separate composition is useful when client payloads, latency budgets or release ownership differ materially. Small differences may be handled by one documented API without another deployable layer.

**Q:** What should a client-specific aggregation layer own?

**A:** It owns client-specific aggregation and representation, commonly with the client team. Authoritative business rules and access checks remain in domain services.

**Q:** What deployment and ownership costs does adding a BFF create?

**A:** Another BFF adds deployment, telemetry and failure paths, and composition may be duplicated. Keep ownership clear and share stable domain APIs when several clients need the same operation.

## API Authentication

Source: [API Authentication](20.3.4.04-authentication.md)

**Q:** What evidence lets an API verify a caller's identity claim?

**A:** Evidence can include a session identifier, opaque token, signed token, API key or client certificate. Validate it under the issuer and application contract before establishing a principal.

**Q:** How does verification state affect scaling and revocation?

**A:** Sessions and opaque tokens usually require current state; signed tokens can be checked locally but need trusted keys and may still require revocation state. Choose from actual lifecycle requirements.

**Q:** Why are credential transport and storage part of the authentication design?

**A:** A stolen bearer credential can be replayed regardless of its format. Protect transport and logs, and choose browser storage with explicit XSS and CSRF boundaries.

## Trace and Failure Checks

Source: [Rate limiting](20.3.4.01-rate-limiting.md)

**Q:** A depleted bucket is checked at0.4seconds and again at1.0second. Why preserve fractional refill?

**A:** The first check earns0.4tokens even if it cannot admit a cost1request. Discarding that time while advancing lastRefill can prevent a busy key from ever refilling; keep the fraction with the updated clock.

**Q:** Does a Redis pipeline or an always-fail-open policy enforce every shared quota correctly?

**A:** No. Combined read/refill/compare/consume needs an atomic decision, while pipelines only batch commands. Store-outage policy depends on the operation: hard quota, availability and degraded local protection have different risks.

Source: [Gateway forwarding](20.3.4.02-api-gateway.md)

**Q:** In the read-gateway fixture, what happens to /api/products/42?view=compact and a supplied X-User-Id?

**A:** The fixed target receives /products/42?view=compact. The fixture does not forward the asserted identity, and it generates its own request ID. A real protected gateway needs authenticated context and downstream resource authorization.

**Q:** An upstream starts a body then fails. Can the gateway write a new JSON502response?

**A:** No, response headers/body already started. Terminate the failed stream under the proxy contract. Before headers start, connection failure and deadline failure can map to documented502/504outcomes.

Source: [BFF composition](20.3.4.03-bff.md)

**Q:** Required profile data succeeds but optional activity fails. Why not return an empty activity list?

**A:** Empty means no activity, while unavailable means the dependency failed. Return an explicit partial state when permitted; fail the operation when required data or the total deadline contract fails.

**Q:** Does a partner requesting only displayName prove it may see that user?

**A:** No. Field selection shapes output; verified principal, tenant and resource policy authorize it. Enforce access at the data-owning boundary and scope private caches appropriately.

Source: [API authentication](20.3.4.04-authentication.md)

**Q:** A tenant-a principal has invoice:read:any. Can it read tenant-b's invoice in the example?

**A:** No. That permission is tenant-scoped; the tenant condition still rejects it. A global administrator needs a separate explicit policy.

**Q:** Two refresh calls read one unused token, then independently mark and replace it. What is missing?

**A:** Atomic consumption and successor creation under the session/family contract. Single-flight clients help legitimate concurrency but do not close server races or lost-response recovery; logout also needs an explicit access-token revocation window.

## Summary

Use these prompts after the reading pass to recall the edge and scale mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for proxy authority and demand budgets

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
