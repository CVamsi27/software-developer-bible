<!-- section: NestJS | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-NestJS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# NestJS — Request Lifecycle Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## NestJS Middleware

Source: [NestJS Middleware](20.2.2.01-middleware.md)

**Q:** Which shared request tasks are suited to middleware?

**A:** Middleware suits early transport tasks such as correlation, session parsing and completion observation on its matched routes. It can respond or pass control; parser, guard and service boundaries still own their respective contracts.

**Q:** How does the context available to middleware differ from handler-level components?

**A:** Class middleware supports module DI and sees adapter request/response/next. A guard/interceptor ExecutionContext additionally identifies the selected controller and handler, enabling route-metadata policy.

**Q:** Why must middleware registration order follow dependencies between tasks?

**A:** Create correlation before logging, and establish verified identity before policies that consume it. Global/module registration and adapter behavior affect ordering; test the intended matches and exclusions.

## NestJS Guards

Source: [NestJS Guards](20.2.2.02-guards.md)

**Q:** Why perform access checks in a guard before the handler?

**A:** A denied guard prevents protected downstream work. The decision still needs verified identity, the intended action/resource, and a consistency boundary for changing authorization state.

**Q:** How do a roles decorator and a guard divide policy declaration from enforcement?

**A:** The decorator records metadata. A registered guard selects it, for example handler-first getAllAndOverride, and evaluates the verified principal. A decorator alone grants or denies nothing.

**Q:** Which responsibilities belong outside a guard's allow-or-deny decision?

**A:** A guard can enforce admission, permissions, flags or quotas; services own the detailed operation and data consistency. Response field projection and durable effects need their own explicit boundaries.

## NestJS Pipes

Source: [NestJS Pipes](20.2.2.03-pipes.md)

**Q:** How can a pipe convert, validate, or default an argument?

**A:** A pipe receives an extracted argument, returns its validated/transformed/defaulted value or throws. Default missing input deliberately; reject malformed nonmissing representations rather than accepting a numeric prefix.

**Q:** What must be configured to validate a DTO at runtime?

**A:** Register ValidationPipe, use runtime DTO classes with suitable decorators/nested metadata, and select transform/whitelist/null/coercion policies. TypeScript annotations alone perform no runtime validation or authorization.

**Q:** Why does the order of guards and pipes matter, and which argument is piped first in `update(@Body() body, @Param('id', ParseUUIDPipe) id)`?

**A:** Guards execute before argument pipes, so they cannot assume a later ParseUUIDPipe has already validated raw input. Parameter pipes resolve from the last handler parameter to the first, so the ID is piped before the body. Avoid cross-parameter side effects that depend on this ordering.

## NestJS Interceptors

Source: [NestJS Interceptors](20.2.2.04-interceptors.md)

**Q:** What does an interceptor observe that an argument pipe or guard does not?

**A:** An interceptor wraps remaining execution and can observe/map/replace its emitted values/errors. A guard decides admission and an argument pipe validates input; none alone proves client delivery.

**Q:** How do RxJS operators add behavior around next.handle()?

**A:** map changes values, tap observes notifications, finalize handles subscription termination, and catchError replaces/rethrows errors. timeout stops waiting and retry resubscribes; neither implies cancellation, rollback or idempotency.

**Q:** In what order do nested interceptors run before and after the handler?

**A:** Before-work nests from global to controller to route; result transformations unwind in reverse. Short-circuiting next.handle can deliberately skip downstream pipes/handler, so cache eligibility and access policy must remain safe.

## NestJS Exception Filters

Source: [NestJS Exception Filters](20.2.2.05-exception-filters.md)

**Q:** Why should known application failures map to specific HTTP status codes?

**A:** A known missing resource can map to 404 and a known domain conflict to 409. Unexpected failures receive a generic safe 500; status/message choices must match the business/protocol meaning.

**Q:** What should a shared error response contain or omit?

**A:** A stable bounded envelope and server-owned correlation ID can identify the failure. Omit stacks, arbitrary exception messages, rejected secrets and raw database details; diagnostics need redaction and access controls too.

**Q:** Where do exception filters fit when request processing throws?

**A:** An uncaught supported request failure selects an applicable route, controller or global filter. A handled exception is not automatically forwarded through every outer filter, and detached work remains outside that request ownership.

**Q:** Which filters can handle an exception thrown by Nest middleware?

**A:** Only global exception filters apply because middleware runs before a route or controller is selected. A caught exception never enters the filter layer.

## Request Context & AsyncLocalStorage

Source: [Request Context & AsyncLocalStorage](20.2.2.06-request-context-and-async-local-storage.md)

**Q:** Why might several layers need the same request identifier?

**A:** Layers can attribute operations with a narrow ambient identifier, or use an explicit context parameter. Neither choice is mandatory for every repository; document the chosen dependency and keep business data explicit.

**Q:** Why is a global current-request variable unsafe when requests overlap?

**A:** A mutable process current-request variable can be overwritten while another request awaits. ALS associates stores with supported async resources; explicit parameters or appropriately scoped DI are also valid mechanisms.

**Q:** What dependency tradeoff comes with reading request context implicitly?

**A:** Ambient context hides inputs from signatures. Keep the store small and documented, require verified identity where used for enforcement, and give transaction/resource handles a real lifetime contract.

## Traces and changed conditions

### Middleware

Source: [Middleware fixture](20.2.2.01-middleware.md).

**Q:** Trace the generated request ID through the middleware fixture and completion log.

**A:** Correlation assigns a server UUID, the handler returns it and finish records the same ID. The client-supplied ID does not select it. Stages are identified, handler, finished.

**Q:** What changes when the response closes before finish?

**A:** Record closed once and remove both terminal listeners. Finish means transport handoff, not client receipt; neither event makes request IDs appropriate metric labels.

### Guards

Source: [Guard fixture](20.2.2.02-guards.md).

**Q:** Explain health 200, missing credential 401, reader 403 and admin 200 in order.

**A:** Public health bypasses authentication. Reports without a credential stop at authentication; a verified reader fails the inherited admin policy; an admin passes both guards.

**Q:** Why does a reader succeed on `/reports/read`, and what if its metadata is removed?

**A:** Handler-first override chooses the reader role. Removing that declaration exposes the controller admin requirement again. Merge would be a different declared policy.

### Pipes

Source: [Bounded page-size pipe](20.2.2.03-pipes.md).

**Q:** What do undefined, `'25'`, `'10junk'` and a repeated-value array produce?

**A:** Default 10, accepted 25, then two 400 rejections. Absence differs from malformed input; accepted values are safe positive integers at most 100.

**Q:** What changes if a database uniqueness lookup moves into a pipe?

**A:** It can give early feedback, but two requests can both pass before either insert. The database constraint and domain-aware conflict mapping still enforce the concurrent invariant.

### Interceptors

Source: [Wrapper and timeout fixtures](20.2.2.04-interceptors.md).

**Q:** Trace handler 1 through inner and outer mapping.

**A:** Outer before precedes inner before; handler emits 1, inner maps 2, outer maps 3. Finalizers observe subscription termination, not delivery of the response.

**Q:** Why does the timeout fixture print stopped waiting and later 1?

**A:** The 5 ms first-emission deadline unsubscribes, but the 40 ms promise continues and increments its effect. A mutation can complete after timeout; cancellation needs a cooperative API and uncertain outcomes need reconciliation.

### Filters

Source: [Safe HTTP filter](20.2.2.05-exception-filters.md).

**Q:** What reaches clients for private 404, private 400 and an unexpected database-secret error?

**A:** Fixed Not found/Invalid request/Internal server error messages with 404/400/500. The arbitrary exception text remains outside the public envelope.

**Q:** What changes if response headers were already sent or a local filter handles the error?

**A:** A new complete JSON/status cannot replace sent bytes; the adapter/stream must handle the existing response. A local applicable filter handles its scope rather than automatically forwarding through every global filter.

### Async context

Source: [ALS interleaving fixture](20.2.2.06-request-context-and-async-local-storage.md).

**Q:** Why do overlapping operations return clinic-a/clinic-b and the later A timer still returns clinic-a?

**A:** Their supported descendant resources retain distinct stores. The timer was created inside A even though it outlives the main callback. Outside both roots getStore is undefined and required tenant access throws.

**Q:** What changes if a timer retains a transaction client after its callback committed?

**A:** Context association may remain, but the client lifetime is over. Await transaction work before leaving, and open a fresh owned transaction at a job boundary; ALS does not automatically bind root-client queries or make missing tenant context safe.

## Summary

Use these prompts after the reading pass to recall the request lifecycle mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for request ownership and scoped context

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
