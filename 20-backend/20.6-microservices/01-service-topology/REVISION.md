<!-- section: Microservices | category: Reference | tags: revision | role-priority: important | general-importance: important -->
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

**Q:** Why must endpoint discovery adapt to changing service instances?

**A:** Scaling, restarts and failover change instance addresses. Resolve a logical service identity through current membership and routing state instead of assuming fixed locations.

**Q:** How do client-side and server-side discovery trade client coupling against an extra hop?

**A:** Client-side discovery gives the client endpoint-selection responsibility; server-side discovery puts that selection in a proxy or load balancer. Compare client complexity, observability and additional hops.

**Q:** Why should discovery account for endpoint health and readiness?

**A:** An address can exist while the instance cannot serve the workload. Define health/readiness signals and expiry behavior, recognizing that cached information and network failures make availability uncertain.

**Q:** When would you choose a Kubernetes Service, Consul or Eureka for discovery?

**A:** Prefer the platform Service when cluster DNS and forwarding meet the routing need. Consul adds a catalog with health-aware DNS/API lookup for environments that need its registry model; Eureka fits Spring Cloud clients that register and query a replicated registry. In every case, verify the health signal, cache age and who selects the endpoint. See the [Kubernetes Service DNS contract](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/), [Consul discovery model](https://developer.hashicorp.com/consul/docs/discover) and [Spring Cloud Eureka behavior](https://docs.spring.io/spring-cloud-netflix/docs/current/reference/html/).

## API Gateway

Source: [API Gateway](20.6.1.02-api-gateway.md)

**Q:** How does a gateway reduce the client-to-service routing problem?

**A:** Clients use one external routing contract instead of maintaining every service address. The gateway translates requests to services while preserving the documented public behavior.

**Q:** Which shared policies belong at the gateway, and which still belong in services?

**A:** TLS, coarse admission and common telemetry fit the edge. Tenant ownership, object-level permission and business invariants still require enforcement by authoritative services.

**Q:** Why does a gateway need bounded work and predictable failure behavior?

**A:** It is on the request path for many operations. Bound queues, timeouts and transformations so one expensive route cannot exhaust it, and provide observable configuration rollout and recovery.

## Service Mesh

Source: [Service Mesh](20.6.1.03-service-mesh.md)

**Q:** Which service-to-service concerns can a mesh apply consistently?

**A:** A mesh can standardize communication identity, TLS, routing and telemetry across services. It does not replace domain authorization or guarantee that application operations are safe to retry.

**Q:** What resource and lifecycle costs do sidecar proxies introduce?

**A:** Sidecars consume memory, CPU and connection capacity and need configuration and lifecycle management. Sidecars are one mesh model; evaluate the actual data-plane architecture.

**Q:** How can mesh routing support a controlled rollout?

**A:** Weighted routing and subsets can direct controlled traffic to a new version. Pair those mechanisms with compatible contracts, meaningful health evidence and rollback rules.

## Strangler Fig Pattern

Source: [Strangler Fig Pattern](20.6.1.04-strangler-fig.md)

**Q:** Why can a full rewrite make continued delivery difficult?

**A:** A long rewrite can create divergent behavior while the legacy product continues changing. Incremental replacement reduces the scope of each cutover but still needs compatibility and ownership planning.

**Q:** How does a routing facade enable incremental replacement?

**A:** The facade routes a selected capability to its new implementation while the rest remains legacy. Make routing, data ownership and fallback behavior explicit during coexistence.

**Q:** What rollback and retirement criteria does a strangler migration need?

**A:** Define the conditions that trigger fallback and whether data written by the new path remains compatible. Retire the old capability only after dependency, traffic and recovery evidence support removal.

## Changed conditions

Source: [Discovery](20.6.1.01-service-discovery.md), [Gateway](20.6.1.02-api-gateway.md), [Mesh](20.6.1.03-service-mesh.md), [Strangler](20.6.1.04-strangler-fig.md).

**Q:** An endpoint's lease expires at time 10. Can a snapshot selector use it at time 10?

**A:** Not under the chapter's strict greater-than-now contract. A live connection might still exist, but that is different evidence with separate draining rules.

**Q:** Why does `/api/orders-archive` not select the `/api/orders` route?

**A:** Prefix matching must respect a path-segment boundary; exact prefix or prefix plus slash does, raw startsWith does not.

**Q:** Is a URL-only cache safe for a caller-authorized order read?

**A:** No. Different callers can have different permitted data. Define cache eligibility and authorization/representation scope, or avoid caching the response.

**Q:** A mesh retries a write whose response was lost. What property must come from the application?

**A:** Idempotent acceptance/status resolution under a durable operation contract. Authenticated transport cannot prove the first attempt did not commit.

**Q:** Why can a strangler's legacy fallback duplicate an order after timeout?

**A:** Replacement may have committed before its response failed. Resolve the unknown outcome instead of blindly executing the command on legacy.

**Q:** Equal row counts appear after backfill. What is still unproven?

**A:** Entity identity, values, versions, deletion handling and replication position. Compare semantic state under a consistent observation boundary.

## Summary

Use these prompts after the reading pass to recall the service topology mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for routes, mesh identity and safe migration

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
