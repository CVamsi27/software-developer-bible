<!-- section: Microservices | category: Reference | tags: revisi | role-priority: important | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Microservices — Service Topology Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Service Discovery

Source: [Service Discovery](20.6.1.01-service-discovery.md)

**Q:** What core constraint explains why in a scaled, auto-healing deployment, "where is service x?" changes hourly. governs service discovery?

**A:** IPs die on reschedule; DNS alone is too slow and too static. Discovery is the answer: a registry that instances *register to on start* and *deregister from on death*, with health checks evicting the lying.

**Q:** What core constraint explains why client-side vs server-side discovery trades coupling for hops. governs service discovery?

**A:** Client-side (lookup in-process: less latency, registry library coupled to every language) vs server-side (LB/gateway does it: one place, extra hop). Kubernetes collapsed this debate: Services + kube-proxy are server-side discovery as platform.

**Q:** What core constraint explains why health is part of the answer, not an add-on. governs service discovery?

**A:** A registry entry without health checks routes traffic to corpses — the readiness probe  is discovery's truth source.

## API Gateway

Source: [API Gateway](20.6.1.02-api-gateway.md)

**Q:** What core constraint explains why n services × m clients = the mapping problem. governs api gateway?

**A:** Without a gateway, every client knows every service's address, auth, and versioning — a full mesh of coupling. The gateway restores one front door: clients speak the facade, the topology refactors freely.

**Q:** What core constraint explains why cross-cutting policy must exist once. governs api gateway?

**A:** AuthN, rate limiting, TLS, request shaping — enforced at the edge, services trust internal identity only (the gateway's tokens), which is the zero-trust boundary made practical.

**Q:** What core constraint explains why the gateway is on the critical path, so it must be boring. governs api gateway?

**A:** Horizontally scalable, config-as-code, and never the place for business logic — the moment a gateway holds domain rules, deploy independence (the point of microservices) dies at the front door.

## Service Mesh

Source: [Service Mesh](20.6.1.03-service-mesh.md)

**Q:** What core constraint explains why service-to-service calls need tls, retries, timeouts, mtls identity, and telemetry — in every service, in every language. governs service mesh?

**A:** Implementing them in each codebase guarantees drift; the mesh moves them into a per-pod sidecar proxy. Your code speaks plain HTTP; the mesh upgrades it to encrypted, retried, observed traffic — a platform decision, not a library.

**Q:** What core constraint explains why the sidecar is the price and the point governs service mesh?

**A:** uniform policy enforcement without touching app code (policy-as-code in the mesh config), at the cost of a hop and operational complexity. That trade is worth it at ~50+ services and questionable below.

**Q:** What core constraint explains why traffic management is the hidden product governs service mesh?

**A:** canary splits, circuit breaking, and fault injection become config — release engineering  without redeployment.

## Strangler Fig Pattern

Source: [Strangler Fig Pattern](20.6.1.04-strangler-fig.md)

**Q:** What core constraint explains why a rewrite freezes the system it replaces. governs strangler fig pattern?

**A:** Six months of "new system" means six months of unshipped product features stacking onto the old one — the rewrite finishes bigger and later than the monolith it killed. Incremental replacement is the only path that keeps shipping.

**Q:** What core constraint explains why the facade is the mechanism governs strangler fig pattern?

**A:** route at the edge , extract one capability at a time into the new architecture, migrate its traffic, repeat. At every moment the system ships — the old and new coexist by design.

**Q:** What core constraint explains why the discipline is the kill switch governs strangler fig pattern?

**A:** each extracted piece must have a route that can flip back, because the old system is the safety net until the last module strangles. Migration without rollback is gambling.

## Summary

Use these prompts after the reading pass to recall the service topology mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
