<!-- section: NestJS | category: Reference | tags: revision | role-priority: essential | general-importance: important -->
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

**Q:** Why use role metadata instead of repeating an authorization check in each handler?

**A:** A role decorator records the requirement beside the handler. A registered guard reads it and checks each request. The metadata does not enforce access by itself.

**Q:** How does a custom parameter decorator reduce repeated request extraction?

**A:** Its callback extracts a value such as `req.user` and passes it as a handler argument. Handlers need less knowledge of the HTTP request shape and can be tested with ordinary values.

**Q:** Which decorator work runs once, and which work runs per request?

**A:** The decorator attaches metadata when the class is defined. Nest invokes a custom parameter decorator extraction callback for each request. Put business logic in services and access checks in registered guards or interceptors.

**Q:** Why might `ValidationPipe` accept an invalid value extracted by a custom parameter decorator?

**A:** It skips custom-decorator arguments by default. Enable `validateCustomDecorators` or attach an appropriate pipe; authentication and authorization still belong to their own request-lifecycle components.

## NestJS Custom Decorators Edge Cases

Source: [NestJS Custom Decorators](20.2.5.01-custom-decorators.md)

**Q:** Does `@CurrentUser()` verify the credential?

**A:** Usually it reads the user that an authentication guard or strategy has already verified and attached to the request. Extraction alone does not prove authentication.

**Q:** How can you check that a role decorator protects a route?

**A:** Test the metadata and the guard separately, then send allowed and disallowed requests through a route with the guard registered. A decorator test alone cannot prove enforcement.

## Extraction and enforcement boundaries

Source: [Custom decorators](20.2.5.01-custom-decorators.md)

**Q:** Does `@Controller` register a class that no module lists as a controller?

**A:** No. The decorator stores metadata; module registration makes it part of the application graph.

**Q:** Why is `emitDecoratorMetadata` different from a custom `SetMetadata` key?

**A:** The compiler emits design-type metadata for implicit injection. `SetMetadata` explicitly writes the application's chosen key/value.

**Q:** Why should a missing clinic identity fail before a repository call?

**A:** Passing undefined can weaken a query's tenant filter. Authenticate and authorize the tenant, then reject absent identity.

**Q:** Why reject `page=2abc` instead of accepting `parseInt`'s result?

**A:** It is malformed input, not the declared positive-integer contract. Explicit parsing avoids partial acceptance.

**Q:** What must accompany response-transform metadata to change an output?

**A:** A registered interceptor reads it and maps the downstream response. Metadata alone leaves execution unchanged.

**Q:** Why can a role decorator and a registered guard still disagree about an authenticated clinician?

**A:** They must share the exact metadata key and verified-principal location. Writing a string key while the guard reads a Symbol, or attaching `req.user` while it reads `req.principal`, leaves the consumer without its required policy or identity. Adapt both sides together and test the admitted and denied routes.

## Summary

Use these prompts after the reading pass to recall the advanced mechanisms and their boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for advanced dependency and request decisions

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
