# NestJS — Index

> **15 files** — NestJS framework from modules and controllers to guards, pipes, interceptors, CQRS, microservices, testing, configuration, custom decorators, and interview questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-success)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why NestJS:** The most common Node.js framework for production TypeScript backends. Used by mid-stage startups (n8n, SumUp, etc.), enterprises, and increasingly at FAANG adjacent companies. Senior interviews test NestJS architecture (modules, DI), request lifecycle (middleware → guards → pipes → interceptors → controller), and patterns (CQRS, microservices, custom decorators).

---

## Topic Categories

The 15 files are organized into 5 categories.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Core Architecture](#core-architecture) | 4 | Modules, Controllers, Providers, DI — the foundation |
| [Request Lifecycle](#request-lifecycle) | 5 | Middleware, Guards, Pipes, Interceptors, Exception Filters — what runs in what order |
| [Patterns & Architecture](#patterns--architecture) | 2 | CQRS, Microservices — the patterns NestJS supports out of the box |
| [Quality & Configuration](#quality--configuration) | 3 | Testing, Validation, Config — production hygiene |
| [Advanced & Interview](#advanced--interview) | 2 | Custom decorators, 50+ interview Qs |

---

## Core Architecture

How NestJS apps are structured. Read these first.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Modules](20.2.01-modules.md) | Feature modules, shared modules, global modules, dynamic modules, module re-exports | 25 min |
| 02 | [Controllers](20.2.02-controllers.md) | Route handlers, request/response objects, decorators, version controllers | 20 min |
| 03 | [Providers](20.2.03-providers.md) | Service providers, custom providers, provider scopes (default, request, transient) | 20 min |
| 04 | [Dependency Injection](20.2.04-dependency-injection.md) | DI container, custom providers, circular dependencies, `forwardRef` | 30 min |

---

## Request Lifecycle

The order of execution for every request — **every NestJS interview tests this**. Read in order.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 08 | [Middleware](20.2.08-middleware.md) | Functional middleware, class middleware, consumer configuration, `NestModule` | 15 min |
| 05 | [Guards](20.2.05-guards.md) | Auth guards, role-based access, custom guards, `CanActivate`, execution context | 25 min |
| 06 | [Pipes](20.2.06-pipes.md) | Validation pipes, transformation pipes, built-in pipes, custom pipes | 25 min |
| 07 | [Interceptors](20.2.07-interceptors.md) | Request/response transformation, logging, caching, mapping, async interceptors | 25 min |
| 09 | [Exception Filters](20.2.09-exception-filters.md) | Built-in exceptions, custom exception filters, catch-all filters, `@Catch()` | 20 min |

**Lifecycle order:** Middleware → Guards → Pipes → Controller → Interceptors (rxjs pipeline) → Exception Filters.

---

## Patterns & Architecture

The patterns NestJS supports out of the box.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 10 | [CQRS](20.2.10-cqrs.md) | Commands, queries, events, sagas, command/query buses, `@nestjs/cqrs` | 30 min |
| 11 | [Microservices](20.2.11-microservices.md) | TCP, Redis, RabbitMQ, Kafka, gRPC transports, hybrid apps, message patterns | 30 min |

---

## Quality & Configuration

Production hygiene.

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 13 | [Testing](20.2.12-testing.md) | Jest, TestingModule, supertest, Testcontainers, e2e/integration/unit | 30 min |
| 14 | [Configuration & Validation](20.2.13-configuration-validation.md) | ConfigModule, ValidationPipe, class-validator, Joi, DTOs, env validation | 25 min |

---

## Advanced & Interview

| # | File | Topics | Read time |
|--:|------|--------|----------:|
| 16 | [Custom Decorators](20.2.15-custom-decorators.md) | Parameter decorators (@CurrentUser, @ClinicId, @Pagination), method decorators (@RateLimit, @Cache, @Audit), decorator composition | 25 min |
| 15 | [Interview Questions](20.2.14-interview-questions.md) | 50+ curated questions with answers | 3 hrs |

---

## Suggested Study Order

1. **Core Architecture** (4 files, ~2 hrs) — must know
2. **Request Lifecycle** (5 files, ~2 hrs) — must know, the most-asked cluster
3. **Patterns** (CQRS + Microservices) — for senior/DDD roles
4. **Quality & Configuration** — production hygiene
5. **Custom Decorators** — senior-level
6. **Interview Questions** — final review

---

## Cross-References

- [Node.js](../20.1-node.js/INDEX.md) — the runtime NestJS sits on
- [REST APIs](../20.3-rest-apis/INDEX.md) — NestJS controllers map to REST routes
- [Microservices (gRPC, Service Mesh)](../20.6-microservices/INDEX.md) — microservices patterns NestJS implements
- [Design Patterns (CQRS)](../../30-architecture/30.1-design-patterns/30.1.4-architectural/30.1.42-cqrs-di.md) — CQRS deep-dive
- [Testing](../../50-quality/50.1-testing/INDEX.md) — testing patterns

---

## Navigation

[← Previous: Node.js](../20.1-node.js/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: REST APIs →](../20.3-rest-apis/INDEX.md)
