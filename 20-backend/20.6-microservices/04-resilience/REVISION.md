<!-- section: Microservices | category: Reference | tags: revision -->
[![Section](https://img.shields.io/badge/section-Microservices-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)

# Microservices — Resilience Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Circuit Breaker

Source: [Circuit Breaker](20.6.4.01-circuit-breaker.md)

**Q:** What core constraint explains why retries against a dying service kill it faster. governs circuit breaker?

**A:** Every retry is load; a struggling dependency under retry-storm goes from slow to dead — the breaker's open state exists to *remove load* from something that needs to recover.

**Q:** What core constraint explains why three states are the whole model governs circuit breaker?

**A:** closed (normal, failures counted), open (fail fast — no network call at all), half-open (probe with limited traffic: recovered? close; not? stay open). The state machine is a control loop on the dependency's health, not on your request.

**Q:** What core constraint explains why the configuration is a capacity decision governs circuit breaker?

**A:** thresholds too sensitive = flapping (opening on normal variance); too lax = collapse before opening. Combined with fallbacks (serve cached/degraded), the breaker converts dependency failure from outage to degradation.

## Bulkhead Pattern

Source: [Bulkhead Pattern](20.6.4.02-bulkhead-pattern.md)

**Q:** What core constraint explains why one shared pool couples every workload. governs bulkhead pattern?

**A:** A report query exhausting the DB pool takes down login — unrelated features share fate through the resource. The bulkhead partitions the pool (per-dependency, per-priority): one compartment flooding doesn't sink the ship.

**Q:** What core constraint explains why the partition is a capacity allocation governs bulkhead pattern?

**A:** — and therefore a product decision: checkout gets more threads than analytics. Sizing is queueing math (Little's law), not vibes; undersized bulkheads fail fast (good) but loudly.

**Q:** What core constraint explains why it composes with breakers (→ 20.6.4.01) governs bulkhead pattern?

**A:** the breaker stops calling a failing dependency; the bulkhead bounds the damage while it still works. Both exist because the alternative — global shared resources — makes every failure everyone's failure.

## Summary

Use these prompts after the reading pass to recall the resilience mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
