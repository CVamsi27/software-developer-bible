<!-- section: REST APIs | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-REST%20APIs-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# REST APIs — Design And Contract Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## API Design Patterns — REST, GraphQL, gRPC, Webhooks

Source: [API Design Patterns — REST, GraphQL, gRPC, Webhooks](20.3.1.01-api-design-patterns.md)

**Q:** Which trust and failure boundaries does a remote API call cross?

**A:** A network call can be delayed, rejected or completed without its response arriving. Validate the remote party and payload, bound waiting and make uncertain retries safe at the operation boundary.

**Q:** Why should an API contract avoid exposing internal implementation details?

**A:** Consumers depend on the public representation and behavior. Exposing storage details couples their releases to internal changes; publish the fields and operations they actually need.

**Q:** How does consistent API behavior help independently developed clients?

**A:** Consistent naming, error fields and pagination reduce client-specific branches. Document exceptions when an operation needs a different contract.

## REST Principles

Source: [REST Principles](20.3.1.02-rest-principles.md)

**Q:** What makes an interface uniform in REST?

**A:** The uniform interface combines resource identification, manipulation through representations, self-descriptive messages and hypermedia controls. HTTP methods and media types help express those constraints; naming endpoints consistently is not enough.

**Q:** Why does REST model resources rather than a list of remote actions?

**A:** A resource identifier gives representations and state transitions a stable target. Remote actions can be valid HTTP APIs, but an action catalog alone does not satisfy REST's uniform-interface constraints.

**Q:** What state may a REST server retain without making requests stateful?

**A:** Resource state can remain on the server. Each request must supply the context required to understand it, rather than depending on stored conversational client state from earlier requests.

## API Versioning

Source: [API Versioning](20.3.1.03-versioning.md)

**Q:** Why must API evolution account for clients that upgrade slowly?

**A:** Clients may upgrade long after the server. Preserve compatibility where practical and provide an explicit migration path when behavior cannot remain compatible.

**Q:** How can a provider introduce an incompatible contract without immediately breaking existing clients?

**A:** Offer an opt-in replacement with documented behavior, a deprecation period and usage evidence before retirement. An optional additive change often needs no new version, but strict consumers still need compatibility checks.

**Q:** What does a version identifier tell a client about its contract?

**A:** It identifies the externally visible contract being selected. A URL, header or media type can carry it; compatible additions may evolve within that contract.

## REST Maturity Model

Source: [REST Maturity Model](20.3.1.04-rest-maturity-model.md)

**Q:** What distinguishes a level 0 HTTP API in the Richardson model?

**A:** HTTP acts mainly as a transport for remote calls, commonly through one URI and POST. Generic HTTP infrastructure still operates, but it cannot infer application-operation semantics from the interface.

**Q:** What changes when an API introduces resource identifiers at level 1?

**A:** Distinct resource URIs identify separate targets. Method semantics and cache directives still determine whether their responses are safe to cache or retry.

**Q:** Which HTTP capabilities distinguish level 2 from level 1?

**A:** Methods communicate safety and idempotence; status codes and headers express outcomes and caching rules. These capabilities describe the interface, not its internal data model or overall quality.

## OpenAPI / Swagger Documentation

Source: [OpenAPI / Swagger Documentation](20.3.1.05-openapi-swagger.md)

**Q:** How can a machine-readable API description reduce documentation drift?

**A:** Docs and SDKs can be regenerated from one description, reducing separate edits. The description can still drift from the implementation, so validate real responses and compare contract changes.

**Q:** How does an API contract let frontend and backend teams work independently?

**A:** Teams can build clients and mocks against an agreed specification before the server is complete. Schema quality and representative contract tests determine how useful that independence is.

**Q:** Why can generated client code still fail against a running server?

**A:** Generated types reproduce omissions or errors in the specification. They also cannot establish that the deployed server returns compliant data or enforces the described permissions.

## Trace and Boundary Checks

Source: [API styles](20.3.1.01-api-design-patterns.md)

**Q:** Which API could a shop use for order reads, collaborative messages and payment callbacks?

**A:** A resource/GraphQL read contract, a WebSocket channel for two-way messages, and a webhook ingress can coexist. Choose interaction and recovery rules independently; one product need not select only one style.

**Q:** Does one GraphQL request or a protobuf body prove lower end-to-end latency?

**A:** No. Resolve/fan-out work, network calls, authorization, serialization, compression and client behavior affect cost. Measure representative operations rather than ranking transports universally.

Source: [REST](20.3.1.02-rest-principles.md)

**Q:** The client follows a cancellation control, but an order shipped since its read. What remains authoritative?

**A:** The server's current authorization and domain/version check. A displayed control can become stale; following it does not bypass validation or guarantee a transition.

**Q:** Does storing orders and idempotency records violate REST statelessness?

**A:** No. Resource state can remain server-side. Statelessness concerns the interaction context required to understand the request, not the absence of persistent domain data or a requirement to use JWT.

Source: [Versioning](20.3.1.03-versioning.md)

**Q:** Version 2 renames name to displayName. What should a supported version 1 reader still receive?

**A:** Its original documented name field from the version 1 adapter. A shared domain model can serve both, but a new shared serializer must not silently replace the old representation.

**Q:** Can Deprecation:true and Sunset:2027-04-01 serve as the standardized date syntax?

**A:** No. RFC 9745 uses a structured-field date such as @1790812800; Sunset uses an HTTP-date. These lifecycle hints do not themselves migrate clients or change the deprecated operation.

Source: [Maturity model](20.3.1.04-rest-maturity-model.md)

**Q:** Why is POST /appointments/42 with an action field a useful level 1 example?

**A:** It introduces a resource target while the method still hides whether the operation reads or changes it. Using GET correctly would already demonstrate part of level 2.

**Q:** Does adding an unexplained _links object prove level 3 or production readiness?

**A:** No. Clients need understood control/media semantics. The ladder also says nothing by itself about authorization, durability or the other REST constraints.

Source: [OpenAPI](20.3.1.05-openapi-swagger.md)

**Q:** A 200 Book response omits required title. Can generated docs prove that response valid?

**A:** No. Validate the actual representation against the declared schema. Generated docs can accurately display a description that the implementation violates.

**Q:** In OpenAPI, how does security:[{a:[],b:[]}] differ from security:[{a:[]},{b:[]}]?

**A:** The first requires both schemes; the second allows alternatives. The declaration still requires matching runtime verification and authorization.

**Q:** What should a team check before adopting an OpenAPI 3.2 feature such as `QUERY` or streaming `itemSchema`?

**A:** Confirm that validators, gateways, generators and deployed consumers support the feature end to end. A valid document cannot make an older tool interpret a new operation or streaming contract correctly.

## Summary

Use these prompts after the reading pass to recall the design and contract mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for resource identity and HTTP contracts

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
