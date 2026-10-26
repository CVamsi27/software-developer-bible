# Java — Index

> **Study time:** ≈ 1 h 32 m of reading (7 files, ~13 min average).
> **7 files** — language, object design, concurrency, testing, Spring Boot, and interview practice form the shared Java backend path for Java-heavy roles.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Java here:** the shared stacks cover the web-engineering topics (JS/TS frontend, Node/Nest backend, databases, infra). Java is a first-class backend language in the EU market and the interview language of the SDE/FAANG lane — its language and ecosystem knowledge is generic, so it lives in the stack, not in any single lane.

---

## Topic Categories

| Category | File | Why it matters | Role priority | General importance |
| ----------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------- | ------------------ |
| Language & JVM boundary | [Java Language Fundamentals](20.13.01-java-language-fundamentals.md) | Values, types, collections, streams, generics, and a source-to-execution JVM trace | Deferred | Important |
| OOP & Design | [OOP Principles, Interfaces & SOLID](20.13.02-java-oop-solid.md) | Encapsulation, inheritance, polymorphism, composition, SOLID | Deferred | Important |
| Concurrency | [Concurrency & Multithreading](20.13.03-java-concurrency-multithreading.md) | Threads, synchronization, CompletableFuture, parallel streams, starvation | Deferred | Important |
| Testing | [Testing with JUnit & Mockito](20.13.04-java-testing-junit-mockito.md) | JUnit 6, Mockito, Spring test slices, Testcontainers 2 | Deferred | Important |
| Framework | [Spring Boot Essentials](20.13.05-spring-boot.md) | Boot 4, dependency wiring, MVC, transactions, security, Actuator | Deferred | Important |
| Interview | [Java Interview Questions](20.13.06-interview-questions.md) | Thirty prompts across language, design, concurrency, testing and Spring | Deferred | Important |

---

## Read order

1. **Build valid values and contracts.** Read language fundamentals and follow one class through loading, initialization, execution, and HotSpot optimization; then read OOP. Keep VM implementation behavior separate from Java language guarantees.
2. **Share and schedule work safely.** Read concurrency. Follow the bounded-buffer cycle, then distinguish shared-state safety from task and downstream-resource limits.
3. **Choose evidence for each boundary.** Read testing before Spring. Compare unit, MVC-slice, and real-database tests, then follow one request through authorization, transaction, repository, and commit.
4. **Recall separately.** Use [Revision](REVISION.md), then the interview bank for spoken answers and boundary changes.

## See Also

- [Backend Index](../INDEX.md) — Node.js and NestJS backend stacks that provide architectural equivalents to JVM services
- [Design Patterns](../../30-architecture/30.1-design-patterns/INDEX.md) — Gang of Four design patterns whose canonical textbook implementations are in Java
- [Testing — Quality](../../50-quality/50.1-testing/INDEX.md) — unit, integration, and mocking strategies comparing JUnit/Mockito with Jest/Vitest
- [Coding Patterns — Interview Toolkit](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — algorithmic patterns for the data structures coding portion of enterprise Java loops

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) TypeScript/NestJS pointers offer conceptual comparisons. Inspect current implementation and deployment evidence before claiming behavior or the absence of Java code:

| Java chapter | Closest docita concept |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DI / Spring container | NestJS modules + providers - `apps/api/src/app.module.ts`, `apps/api/src/domains/clinical/clinical.module.ts` |
| MVC controllers / filter chain | NestJS controllers, guards, pipes - `apps/api/src/domains/clinical/presentation/controllers/`, `shared/modules/auth/guards/` |
| Concurrency & multithreading | Node's single-thread event loop + process separation - `apps/worker/src/main.ts`, `shared/modules/queue/postgres-queue.service.ts` (background job separation is the architectural goal; inspect actual CPU/I/O behavior) |
| JUnit & Mockito testing | Colocated Vitest specs (`*.spec.ts`) - e.g. `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.spec.ts` |
| Actuator / ops | `apps/api/src/shared/modules/monitoring/` + `apps/api/src/instrument.ts` (Sentry) - health, metrics, and tracing analogues |

---

[← Previous: AI Engineering](../20.12-ai-engineering/INDEX.md) · [Next: NestJS →](../20.2-nestjs/INDEX.md)
