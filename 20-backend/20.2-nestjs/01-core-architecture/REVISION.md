<!-- section: NestJS | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-NestJS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# NestJS — Core Architecture Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## NestJS Modules

Source: [NestJS Modules](20.2.1.01-modules.md)

**Q:** What do providers, controllers, imports, and exports tell the Nest container?

**A:** Providers register dependencies, controllers register handlers, imports expose another module’s exported tokens, and exports expose this module’s public tokens. Together they tell Nest which dependencies it may resolve for a consumer.

**Q:** How do module exports control which providers another module may use?

**A:** A consuming module needs an import of the owner that exports the token, unless a deliberate global registration supplies it. This controls container visibility, not a runtime data authorization boundary.

**Q:** Why organize a growing application into feature modules?

**A:** A feature module makes ownership and public dependencies explicit. Its imports and exports can be reviewed and tested as a graph. Moving it into another deployment still requires separate transport, data and operational decisions.

## NestJS Controllers

Source: [NestJS Controllers](20.2.1.02-controllers.md)

**Q:** Which responsibilities belong in an HTTP controller rather than a business service?

**A:** The controller maps routes, parses and validates transport input, invokes an application operation and projects its result into status, headers and body. Reusable product rules belong in the service; authentication and resource authorization remain required around that operation.

**Q:** Why should HTTP handlers and queue consumers share business rules through services?

**A:** Both transports can call the same operation while translating their own inputs and outcomes. A queue acknowledgment and an HTTP response have different retry contracts even when the product rule is shared.

**Q:** How does Nest use route decorators when the application starts?

**A:** Nest reads @Controller and method decorators such as @Get at startup to register route handlers through the HTTP adapter. Parameter decorators such as @Param describe which request value a handler receives; attached pipes run before invocation. Dependency resolution is a separate use of metadata.

## NestJS Providers

Source: [NestJS Providers](20.2.1.03-providers.md)

**Q:** Why receive a dependency through a constructor instead of creating it inside a provider?

**A:** A consumer that constructs a collaborator chooses its implementation/configuration there. Receiving it lets application wiring or a test supply another implementation. Manual construction can still be appropriate for an owned value or inside a factory.

**Q:** How does provider scope affect state ownership and construction cost?

**A:** Default scope shares an instance in its registration context. Request scope creates a graph for a request/context and bubbles to dependent consumers. Transient scope supplies a dedicated instance per consumer. Choose state ownership first, then measure allocation cost; no scope makes an untrusted tenant ID authorized.

**Q:** Why does Nest support value, factory, and class provider bindings?

**A:** useValue supplies an existing value, useClass constructs an implementation, and useFactory computes or asynchronously initializes a dependency. A runtime token identifies the registration; a TypeScript interface alone cannot identify it. useExisting shares an already registered dependency.

## NestJS Dependency Injection

Source: [NestJS Dependency Injection](20.2.1.04-dependency-injection.md)

**Q:** How does separating construction from use make a repository replaceable?

**A:** The consumer uses repository operations while application wiring selects its implementation. A mock binding can isolate the consumer; actual module wiring, async readiness and persistence require separate checks.

**Q:** Which dependency-wiring mistakes can the container detect while starting the application?

**A:** Missing visible registrations and unsupported construction cycles can fail during compile/startup. Scoped graphs may resolve later per request/context. Request scope can bubble to consumers rather than being a universal scope-mismatch error; business contracts are not proved by startup.

**Q:** How can a token allow different environments to supply different implementations?

**A:** A consumer requests a canonical runtime token and uses a declared operation contract. Application wiring binds a production repository or test fake to that token. Nest resolves the object; tests still need to check the implementation’s actual success and failure behavior.

## Module ownership and visibility

Source: [Learning chapter](20.2.1.01-modules.md)

**Q:** Why does importing UsersModule only in AppModule not satisfy AppointmentsService?

**A:** Sibling modules do not automatically inherit each other’s exports. AppointmentsModule must import the owner that exports UsersService.

**Q:** Why can re-registering a shared service hide a wiring bug?

**A:** It creates another provider registration rather than consuming the owner’s exported instance. Default scope does not make every registration globally identical.

**Q:** What cannot be assumed about a lazily loaded Nest module?

**A:** LazyModuleLoader loads provider modules on demand; normal lifecycle hooks are not invoked, and it is not a mechanism for adding controllers/routes after startup.


## Fixture traces and changed conditions

Sources: [controller fixture](20.2.1.02-controllers.md), [provider identity](20.2.1.03-providers.md), [DI contexts](20.2.1.04-dependency-injection.md).

**Q:** Trace valid creation, an invalid ID and a missing valid ID through the controller fixture.

**A:** Creation validates then stores one row and returns a projected 201 result. The invalid ID fails ParseIntPipe with 400 before the service. A valid absent ID reaches the service then becomes 404.

**Q:** What changes if the POST includes `role: 'admin'` or the global validation pipe is removed?

**A:** With forbidNonWhitelisted, the undeclared field gets 400 before creation. DTO decorators alone do not validate when the pipe is absent. Neither setting establishes resource authorization.

**Q:** Why do the two USER_STORE aliases compare equal, and what changes with useClass?

**A:** useExisting refers to the already registered provider. Two useClass registrations construct separate instances even if both classes have the same name; the comparison becomes false.

**Q:** What does `true false clinic-a clinic-b` mean in the scoped-resolution fixture?

**A:** The same context ID reuses its request-scoped graph; a different ID gets another graph with its registered request. ReportService inherits request scope through its dependency.

**Q:** What changes if the worker creates a new context ID but never supplies REQUEST?

**A:** The ID chooses a DI subtree, not caller identity. A REQUEST-dependent provider needs an associated request/context object. Register verified context or pass the operation's trusted identity explicitly.

**Q:** Why does an injectable event emitter not make user creation and delivery atomic?

**A:** Injection only supplies the emitter object. A database commit and later in-process emission still have a crash gap; a required event needs durable intent in the same transaction, then owned publication/retry.

## Summary

Use these prompts after the reading pass to recall the core architecture mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — rebuild the ownership graph before debugging transport or context failures

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
