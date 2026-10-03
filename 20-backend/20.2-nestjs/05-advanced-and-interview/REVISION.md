<!-- section: NestJS | category: Reference | tags: revision| general-importance: important| general-importance: important | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-NestJS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# NestJS — Advanced And Interview Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## NestJS Custom Decorators

Source: [NestJS Custom Decorators](20.2.5.01-custom-decorators.md)

**Q:** What core constraint explains why cross-cutting concerns (auth, logging, rate-limiting) applied imperatively must be called at the top of every handler governs nestjs custom decorators?

**A:** → any handler that forgets the call silently skips enforcement. The only structure that centralises enforcement while keeping declaration at the call site is metadata: the decorator stamps the handler at class-definition time, and the guard or interceptor reads that stamp at execution time via `Reflect`. The framework guarantees the guard runs — the developer only declares what role is required.

**Q:** What core constraint explains why the alternative to parameter decorators is manual extraction from `executioncontext`/`req` inside every handler governs nestjs custom decorators?

**A:** → every handler then knows about the HTTP layer, making it untestable outside an HTTP context and repeating the same extraction logic. `createParamDecorator` moves that extraction to one place and gives the handler a typed value, keeping business logic ignorant of the transport. The handler does not know *how* the value arrives; it only knows *what* it receives.

**Q:** What core constraint explains why the discipline is that decorators describe; they do not execute business logic governs nestjs custom decorators?

**A:** → a decorator runs once at class-definition time, not per request, so it cannot read per-request state or make I/O calls safely. Logic placed in decorators is invisible to readers, ordering-fragile (decorators evaluate bottom-up), and untestable in isolation. The correct split: declare intent in the decorator, implement enforcement in a guard or interceptor, implement business logic in a service — each layer independently testable and replaceable.

## NestJS Custom Decorators Edge Cases

Source: [NestJS Custom Decorators](20.2.5.01-custom-decorators.md)

**Q:** How should operational verification and health checks observe NestJS Custom Decorators under load condition 1?

**A:** Verification must inspect invariant stability, connection bounds, and error telemetry rather than relying solely on process liveness.

**Q:** How should operational verification and health checks observe NestJS Custom Decorators under load condition 2?

**A:** Verification must inspect invariant stability, connection bounds, and error telemetry rather than relying solely on process liveness.

## Summary

Use these prompts after the reading pass to recall the advanced and interview mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
