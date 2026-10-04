<!-- section: NestJS | category: Reference | tags: revisi | role-priority: essential | general-importance: important -->
[![Section](https://img.shields.io/badge/section-NestJS-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../../docs/topic-importance.md)

# NestJS — Core Architecture Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## NestJS Modules

Source: [NestJS Modules](20.2.1.01-modules.md)

**Q:** What do providers, controllers, imports, and exports tell the Nest container?

**A:** Providers, controllers, imports, exports — the module is the *declaration of a wiring context*; without it the DI graph is unbounded guesswork. Modules make the graph explicit, reviewable, and refactorable.

**Q:** How do module exports control which providers another module may use?

**A:** A provider not exported is unreachable outside — visibility is declared, not conventional. This is the same "make structure explicit, not remembered" principle as RLS  applied to code organization.

**Q:** Why organize a growing application into feature modules?

**A:** As the app grows, modules are what you review, test, and extract into a library or service — the architecture's real units of change.

## NestJS Controllers

Source: [NestJS Controllers](20.2.1.02-controllers.md)

**Q:** Which responsibilities belong in an HTTP controller rather than a business service?

**A:** Status codes, headers, body shapes, and routing change for protocol reasons; business rules change for product reasons. The controller is the seam: parse/validate/delegate/respond — nothing else.

**Q:** Why should HTTP handlers and queue consumers share business rules through services?

**A:** The moment a controller holds a business rule, two transports (HTTP + queue consumer, → 20.6.2.05) need it duplicated. The rule: controllers translate, services decide.

**Q:** How does Nest use route decorators when the application starts?

**A:** `@Get()`, `@Param()` register route info the DI container reads at bootstrap — the same reflection trick that powers DI itself ; it's one mechanism, not magic.

## NestJS Providers

Source: [NestJS Providers](20.2.1.03-providers.md)

**Q:** Why receive a dependency through a constructor instead of creating it inside a provider?

**A:** A provider that `new`s its own dependencies owns them forever (untestable, unconfigurable); a provider that *receives* them has substitutable parts. Constructor injection is that principle made mechanical.

**Q:** How does provider scope affect state ownership and construction cost?

**A:** Singleton by default, request-scoped on demand — scope is a *correctness decision* (per-request state) with a cost (instantiation per request, → 20.2.2 chain), not a preference.

**Q:** Why does Nest support value, factory, and class provider bindings?

**A:** Custom providers (useValue, useFactory, useClass) exist because interfaces, configs, and third-party clients need injection too — the token system is what makes the container universal.

## NestJS Dependency Injection

Source: [NestJS Dependency Injection](20.2.1.04-dependency-injection.md)

**Q:** How does separating construction from use make a repository replaceable?

**A:** A service that news its repository hard-codes the implementation, the config, and the test double. Inverting construction to a container makes implementations swappable and tests trivial (provide a mock token).

**Q:** Which dependency-wiring mistakes can the container detect while starting the application?

**A:** Circular dependencies, missing providers, and scope mismatches are graph errors — caught at bootstrap *because* Nest builds the graph up-front. That fail-fast is the container's real value: wiring errors become startup errors.

**Q:** How can a token allow different environments to supply different implementations?

**A:** Program against a token, bind implementations per environment — the same seam as OpenAPI for APIs: a contract layer between consumer and implementation.

## Summary

Use these prompts after the reading pass to recall the core architecture mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.

## Module ownership and visibility

Source: [Learning chapter](20.2.1.01-modules.md)

**Q:** Why does importing UsersModule only in AppModule not satisfy AppointmentsService?

**A:** Sibling modules do not automatically inherit each other’s exports. AppointmentsModule must import the owner that exports UsersService.

**Q:** Why can re-registering a shared service hide a wiring bug?

**A:** It creates another provider registration rather than consuming the owner’s exported instance. Default scope does not make every registration globally identical.

**Q:** What cannot be assumed about a lazily loaded Nest module?

**A:** LazyModuleLoader loads provider modules on demand; normal lifecycle hooks are not invoked, and it is not a mechanism for adding controllers/routes after startup.
