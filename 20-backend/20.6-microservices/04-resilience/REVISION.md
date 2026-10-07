<!-- section: Microservices | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# Microservices — Resilience Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Circuit Breaker

Source: [Circuit Breaker](20.6.4.01-circuit-breaker.md)

**Q:** How can retries amplify an overloaded dependency's failure?

**A:** Additional calls consume already constrained connections or CPU and can delay recovery. Bound retries, use backoff and reject calls through a breaker when the failure policy calls for it.

**Q:** How do closed, open and half-open states govern circuit-breaker calls?

**A:** Closed admits calls and tracks outcomes; open rejects protected calls; half-open admits limited recovery probes. Define how success and failure move the breaker between these states.

**Q:** Why should breaker thresholds and probe limits reflect dependency capacity?

**A:** Thresholds trade false rejection against continued overload. Bound probe concurrency and account for call volume and timeout behavior; a breaker alone does not cap resources consumed by in-flight calls.

## Bulkhead Pattern

Source: [Bulkhead Pattern](20.6.4.02-bulkhead-pattern.md)

**Q:** How does a shared resource pool couple otherwise separate workloads?

**A:** A slow workload can consume the pool used by unrelated requests. Separate limits prevent it from exhausting the partitioned resource, though shared downstream infrastructure can still fail.

**Q:** What capacity trade-off does dividing a pool introduce?

**A:** Reserved capacity isolates workloads but can leave one pool idle while another rejects work. Choose budgets from criticality, measured demand and the cost of unused capacity.

**Q:** How do bulkheads and circuit breakers address different failure paths?

**A:** A bulkhead limits resource sharing; a breaker suppresses calls to a failing dependency. Both need deadlines and bounded queues, and neither makes fallback or retry automatically safe.

## Summary

Use these prompts after the reading pass to recall the resilience mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
