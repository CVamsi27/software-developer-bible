<!-- section: NestJS | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
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

**Q:** Which shared request tasks are suited to middleware?

**A:** Logging, correlation IDs, session parsing — things that must happen for *every* request regardless of route. Express-compatible middleware is exactly that: the rawest interception point .

**Q:** How does the context available to middleware differ from handler-level components?

**A:** Middleware can't inject route-scoped dependencies (it's registered outside the DI route graph) — that limitation *is* the design: it separates transport-level from handler-level concerns.

**Q:** Why must middleware registration order follow dependencies between tasks?

**A:** Middleware executes in registration order — CORS before auth, correlation ID before logging. The chain's ordering is configuration with runtime consequences, which is why it lives in explicit module setup, never implicit discovery.

## NestJS Guards

Source: [NestJS Guards](20.2.2.02-guards.md)

**Q:** Why perform access checks in a guard before the handler?

**A:** If it lives inside the handler, forgetting it is one `if` away — a structural fix (execution-order guarantee) beats remembered discipline . Guards run after middleware, before interceptors and handlers: nothing downstream executes on denial.

**Q:** How do a roles decorator and a guard divide policy declaration from enforcement?

**A:** `@Roles('admin')` + `RolesGuard` reading `Reflector` = policy stated at the route, enforced centrally. The same "declare + enforce" split as ABAC policies .

**Q:** Which responsibilities belong outside a guard's allow-or-deny decision?

**A:** Per-field filtering, quota logic — anything richer than allow/deny belongs in interceptors or services; forcing it into a guard produces 400-line guards that re-implement services.

## NestJS Pipes

Source: [NestJS Pipes](20.2.2.03-pipes.md)

**Q:** How can a pipe convert, validate, or default an argument?

**A:** A pipe transforms argument data and may reject it — which unifies coercion (string→number), validation (DTO schema), and defaulting into one boundary concept, applied at the argument level.

**Q:** What must be configured to validate a DTO at runtime?

**A:** `ValidationPipe` + class-validator DTOs mean a handler's signature *is* its input contract — malformed data is rejected before business code runs, the same fail-fast-at-boundary as zod env parsing .

**Q:** Why does the order of guards and pipes matter?

**A:** pipes run after guards — you validate identity first, then input. Every lifecycle component's position encodes a dependency between concerns.

## NestJS Interceptors

Source: [NestJS Interceptors](20.2.2.04-interceptors.md)

**Q:** What does an interceptor observe that an argument pipe or guard does not?

**A:** Timing, response mapping, caching, logging *around* the call — none of these fit guards (boolean) or pipes (argument-level). Interceptors are Nest's AOP: cross-cutting behavior composed via RxJS streams over the response.

**Q:** How do RxJS operators add behavior around next.handle()?

**A:** `next.handle()` returns an Observable; `tap` for side-effects, `map` for transforms, `timeout`/`retry` for resilience — response concerns compose without touching handlers.

**Q:** In what order do nested interceptors run before and after the handler?

**A:** interceptors execute in registration order for "before," reverse for "after" — nesting semantics. Like middleware order , it's configuration with runtime consequences.

## NestJS Exception Filters

Source: [NestJS Exception Filters](20.2.2.05-exception-filters.md)

**Q:** Why should known application failures map to specific HTTP status codes?

**A:** A `NotFoundException` is a 404, not a server error; the filter layer maps thrown domain errors to HTTP semantics *once*, centrally.

**Q:** What should a shared error response contain or omit?

**A:** Uniform error envelope, correlation ID, no stack traces — every rule from API error design lands here as code. Without it, every handler invents its own error shape.

**Q:** Where do exception filters fit when request processing throws?

**A:** guards → interceptors → pipes → handler → filter on throw. Each ring's position is a dependency of concerns — authorization before validation before execution, errors last.

## Request Context & AsyncLocalStorage

Source: [Request Context & AsyncLocalStorage](20.2.2.06-request-context-and-async-local-storage.md)

**Q:** Why might several layers need the same request identifier?

**A:** The repository must not take a `traceId` argument (it has nothing to do with data access), yet its queries should be attributed to the request. Without an ambient mechanism, either the signature grows or the attribution is lost.

**Q:** Why is a global current-request variable unsafe when requests overlap?

**A:** State cannot live in a variable; it must follow the *asynchronous continuation* of each request. That is precisely what `async_hooks`-based stores do and precisely why they are the only correct mechanism.

**Q:** What dependency tradeoff comes with reading request context implicitly?

**A:** Ambient context removes plumbing at the cost of hidden inputs: a function's dependencies are no longer visible in its signature. The mitigation is a *narrow, documented* store — ids and immutable facts, never business data or mutable state.

## Summary

Use these prompts after the reading pass to recall the request lifecycle mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
