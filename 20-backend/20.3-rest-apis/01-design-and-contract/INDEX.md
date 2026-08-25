# Design & Contract - REST APIs

> **5 files.** How the API is shaped and specified: protocol/design-pattern selection, REST principles, versioning strategy, the maturity model, and the OpenAPI contract.

[![Files](https://img.shields.io/badge/files-5-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Design%20%26%20Contract-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [API Design Patterns](20.3.1.01-api-design-patterns.md) | REST vs GraphQL vs gRPC selection, resource naming, consistency, evolution | 25 min |
| 02 | [REST Principles](20.3.1.02-rest-principles.md) | Stateless, uniform interface, constraints | 20 min |
| 03 | [Versioning](20.3.1.03-versioning.md) | URL vs header vs query versioning, deprecation policy | 20 min |
| 04 | [REST Maturity Model](20.3.1.04-rest-maturity-model.md) | Richardson L0-L3, HATEOAS | 10 min |
| 05 | [OpenAPI / Swagger](20.3.1.05-openapi-swagger.md) | Spec-first design, codegen | 15 min |

---

[← Back to REST APIs](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

Docita is deliberately REST-first: no GraphQL or gRPC dependency exists — URI-versioned REST documented with OpenAPI.

| Topic | Docita evidence |
|-------|-----------------|
| Versioning | `apps/api/src/main.ts` - `enableVersioning({ type: VersioningType.URI })` |
| Resource-oriented controllers | `apps/api/src/domains/appointments/presentation/controllers/appointments-schedule.controller.ts` - noun-scoped routes split by concern |
| OpenAPI contract | `apps/api/src/main.ts` - SwaggerModule spec generated from Zod-typed DTOs |

The maturity model sits at Richardson L2 — resources + verbs + status codes, no HATEOAS.
