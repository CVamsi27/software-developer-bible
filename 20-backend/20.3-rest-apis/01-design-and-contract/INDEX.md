# Design & Contract - REST APIs

> **Study time:** ≈ 33 min of reading (6 files, ~6 min average).
> **6 files.** How the API is shaped and specified: protocol/design-pattern selection, REST principles, versioning strategy, the maturity model, and the OpenAPI contract.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Design%20%26%20Contract-blue)](../INDEX.md)

---

## Reading Flow

Choose the interaction and client constraints first. Derive resource/HTTP semantics from REST, then study compatibility and the maturity diagnostic. Finish by describing the selected contract in OpenAPI, use revision, and proceed to HTTP mechanisms.

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [API Design Patterns](20.3.1.01-api-design-patterns.md) | REST vs GraphQL vs gRPC selection, resource naming, consistency, evolution | Essential | Foundational | 7 min |
| 02 | [REST Principles](20.3.1.02-rest-principles.md) | Stateless, uniform interface, constraints | Essential | Foundational | 6 min |
| 03 | [Versioning](20.3.1.03-versioning.md) | URL vs header vs query versioning, deprecation policy | Essential | Foundational | 6 min |
| 04 | [REST Maturity Model](20.3.1.04-rest-maturity-model.md) | Richardson L0-L3, HATEOAS | Important | Important | 4 min |
| 05 | [OpenAPI / Swagger](20.3.1.05-openapi-swagger.md) | Spec-first design, codegen | Essential | Foundational | 7 min |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) healthcare-application pointers are investigation starting points. Inspect the current checkout and generated contract before treating them as current behavior or deployment evidence:

Investigate its URI-versioning configuration, resource-scoped controllers and generated OpenAPI artifact together; dependency absence and supported contracts require current inspection.

| Topic | Docita evidence |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| Versioning | `apps/api/src/main.ts` - `enableVersioning({ type: VersioningType.URI })` |
| Resource-oriented controllers | `apps/api/src/domains/appointments/presentation/controllers/appointments-schedule.controller.ts` - noun-scoped routes split by concern |
| OpenAPI contract | `apps/api/src/main.ts` - SwaggerModule spec generated from Zod-typed DTOs |

Classify an observed interface by its resource, method and control behavior; endpoint naming alone does not prove a maturity level or full REST constraints.
---

[Next: HTTP Mechanics →](../02-http-mechanics/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
