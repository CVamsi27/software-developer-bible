<!-- section: NestJS | category: Reference | tags: revisi | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-NestJS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# NestJS — Request Lifecycle Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## NestJS Middleware

Source: [NestJS Middleware](20.2.2.01-middleware.md)

**Q:** What core constraint explains why cross-cutting concerns need a before-everything hook. governs nestjs middleware?

**A:** Logging, correlation IDs, session parsing — things that must happen for *every* request regardless of route. Express-compatible middleware is exactly that: the rawest interception point .

**Q:** What core constraint explains why it runs before the container knows your route context. governs nestjs middleware?

**A:** Middleware can't inject route-scoped dependencies (it's registered outside the DI route graph) — that limitation *is* the design: it separates transport-level from handler-level concerns.

**Q:** What core constraint explains why order is semantics. governs nestjs middleware?

**A:** Middleware executes in registration order — CORS before auth, correlation ID before logging. The chain's ordering is configuration with runtime consequences, which is why it lives in explicit module setup, never implicit discovery.

## NestJS Guards

Source: [NestJS Guards](20.2.2.02-guards.md)

**Q:** What core constraint explains why "may this request proceed?" is a gate, not a check. governs nestjs guards?

**A:** If it lives inside the handler, forgetting it is one `if` away — a structural fix (execution-order guarantee) beats remembered discipline . Guards run after middleware, before interceptors and handlers: nothing downstream executes on denial.

**Q:** What core constraint explains why the metadata/reflection pairing makes policy declarative. governs nestjs guards?

**A:** `@Roles('admin')` + `RolesGuard` reading `Reflector` = policy stated at the route, enforced centrally. The same "declare + enforce" split as ABAC policies .

**Q:** What core constraint explains why guards return boolean, so nuance lives elsewhere. governs nestjs guards?

**A:** Per-field filtering, quota logic — anything richer than allow/deny belongs in interceptors or services; forcing it into a guard produces 400-line guards that re-implement services.

## NestJS Pipes

Source: [NestJS Pipes](20.2.2.03-pipes.md)

**Q:** What core constraint explains why validation is transformation with a verdict. governs nestjs pipes?

**A:** A pipe transforms argument data and may reject it — which unifies coercion (string→number), validation (DTO schema), and defaulting into one boundary concept, applied at the argument level.

**Q:** What core constraint explains why the schema is the contract, enforced structurally. governs nestjs pipes?

**A:** `ValidationPipe` + class-validator DTOs mean a handler's signature *is* its input contract — malformed data is rejected before business code runs, the same fail-fast-at-boundary as zod env parsing .

**Q:** What core constraint explains why order in the lifecycle is load-bearing governs nestjs pipes?

**A:** pipes run after guards — you validate identity first, then input. Every lifecycle component's position encodes a dependency between concerns.

## NestJS Interceptors

Source: [NestJS Interceptors](20.2.2.04-interceptors.md)

**Q:** What core constraint explains why before-and-after visibility is the unique capability. governs nestjs interceptors?

**A:** Timing, response mapping, caching, logging *around* the call — none of these fit guards (boolean) or pipes (argument-level). Interceptors are Nest's AOP: cross-cutting behavior composed via RxJS streams over the response.

**Q:** What core constraint explains why the stream abstraction is the composition mechanism. governs nestjs interceptors?

**A:** `next.handle()` returns an Observable; `tap` for side-effects, `map` for transforms, `timeout`/`retry` for resilience — response concerns compose without touching handlers.

**Q:** What core constraint explains why with great wrap-power comes ordering subtlety governs nestjs interceptors?

**A:** interceptors execute in registration order for "before," reverse for "after" — nesting semantics. Like middleware order , it's configuration with runtime consequences.

## NestJS Exception Filters

Source: [NestJS Exception Filters](20.2.2.05-exception-filters.md)

**Q:** What core constraint explains why unhandled exceptions default to 500 — which is a lie for known failures. governs nestjs exception filters?

**A:** A `NotFoundException` is a 404, not a server error; the filter layer maps thrown domain errors to HTTP semantics *once*, centrally.

**Q:** What core constraint explains why the catch-everything filter is the error contract's implementation. governs nestjs exception filters?

**A:** Uniform error envelope, correlation ID, no stack traces — every rule from API error design lands here as code. Without it, every handler invents its own error shape.

**Q:** What core constraint explains why filters complete the lifecycle as the safety net governs nestjs exception filters?

**A:** guards → interceptors → pipes → handler → filter on throw. Each ring's position is a dependency of concerns — authorization before validation before execution, errors last.

## Request Context & AsyncLocalStorage

Source: [Request Context & AsyncLocalStorage](20.2.2.06-request-context-and-async-local-storage.md)

**Q:** What core constraint explains why the work for one request is scattered across layers that must not know about each other. governs request context & asynclocalstorage?

**A:** The repository must not take a `traceId` argument (it has nothing to do with data access), yet its queries should be attributed to the request. Without an ambient mechanism, either the signature grows or the attribution is lost.

**Q:** What core constraint explains why node is single-threaded, so "current request" is not a thread-local — it is a callback-graph-local. governs request context & asynclocalstorage?

**A:** State cannot live in a variable; it must follow the *asynchronous continuation* of each request. That is precisely what `async_hooks`-based stores do and precisely why they are the only correct mechanism.

**Q:** What core constraint explains why implicit state is a trade, not a free win. governs request context & asynclocalstorage?

**A:** Ambient context removes plumbing at the cost of hidden inputs: a function's dependencies are no longer visible in its signature. The mitigation is a *narrow, documented* store — ids and immutable facts, never business data or mutable state.

## Summary

Use these prompts after the reading pass to recall the request lifecycle mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
