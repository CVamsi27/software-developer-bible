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

## Summary

Use these prompts after the reading pass to recall the edge and scale mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
