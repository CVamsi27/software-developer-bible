# Java — Index

> **Study time:** ≈ 1 h 37 m of reading (7 files, ~14 min average).
> **7 files** — Java language fundamentals, OOP & SOLID, concurrency & multithreading, and JUnit/Mockito testing — the shared Java backend corpus, used by the SDE/FAANG lane and any Java-heavy EU full-stack target.

[![Files](https://img.shields.io/badge/files-7-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why Java here:** the shared stacks cover the web-engineering topics (JS/TS frontend, Node/Nest backend, databases, infra). Java is a first-class backend language in the EU market and the interview language of the SDE/FAANG lane — its language and ecosystem knowledge is generic, so it lives in the stack, not in any single lane.

---

## Topic Categories

| Category | File | Why it matters |
| ---------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Language | [Java Language Fundamentals](20.13.01-java-language-fundamentals.md) | Types, control flow, strings, arrays, collections, streams, generics — the core tour |
| OOP & Design | [OOP Principles, Interfaces & SOLID](20.13.02-java-oop-solid.md) | Encapsulation, inheritance, polymorphism, composition, SOLID |
| Concurrency | [Concurrency & Multithreading](20.13.03-java-concurrency-multithreading.md) | Threads, synchronization, CompletableFuture, parallel streams, starvation |
| Testing | [Testing with JUnit & Mockito](20.13.04-java-testing-junit-mockito.md) | JUnit 5, Mockito, test data builders, API/integration testing |
| Framework | [Spring Boot Essentials](20.13.05-spring-boot.md) | DI, starters, MVC, Spring Data JPA, security filter chain, actuator |
| Interview | [Java Interview Questions](20.13.06-interview-questions.md) | Thirty prompts across language, design, concurrency, testing and Spring |

---

## Read order

1. **Build one correct object.** Read language fundamentals, then OOP. Trace identity, collection ordering, and account invariants before adding a framework.
2. **Share and schedule work.** Read concurrency. Follow a full bounded-buffer put/take cycle, cancellation, and executor cleanup.
3. **Wire a request boundary.** Read Spring Boot, then testing. Map HTTP → authorization → service transaction → repository and choose the smallest test that exercises each boundary.
4. **Recall separately.** Use [Revision](REVISION.md), then the interview bank for spoken answers and follow-up tradeoffs.

## See Also

- [Backend Index](../INDEX.md) — Node.js and NestJS backend stacks that provide architectural equivalents to JVM services
- [Design Patterns](../../30-architecture/30.1-design-patterns/INDEX.md) — Gang of Four design patterns whose canonical textbook implementations are in Java
- [Testing — Quality](../../50-quality/50.1-testing/INDEX.md) — unit, integration, and mocking strategies comparing JUnit/Mockito with Jest/Vitest
- [Coding Patterns — Interview Toolkit](../../70-interview-toolkit/70.2-coding-patterns/INDEX.md) — algorithmic patterns for the data structures coding portion of enterprise Java loops

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Docita is a **TypeScript/NestJS monorepo — there is no Java code to map to**. The Java chapters teach JVM concepts the stack itself doesn't use; the closest conceptual counterparts (not code mappings):

| Java chapter | Closest docita concept |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DI / Spring container | NestJS modules + providers - `apps/api/src/app.module.ts`, `apps/api/src/domains/clinical/clinical.module.ts` |
| MVC controllers / filter chain | NestJS controllers, guards, pipes - `apps/api/src/domains/clinical/presentation/controllers/`, `shared/modules/auth/guards/` |
| Concurrency & multithreading | Node's single-thread event loop + process separation - `apps/worker/src/main.ts`, `shared/modules/queue/postgres-queue.service.ts` (background job separation is the architectural goal; inspect actual CPU/I/O behavior) |
| JUnit & Mockito testing | Colocated Vitest specs (`*.spec.ts`) - e.g. `apps/api/src/shared/modules/outbox/outbox-relay.scheduler.spec.ts` |
| Actuator / ops | `apps/api/src/shared/modules/monitoring/` + `apps/api/src/instrument.ts` (Sentry) - health, metrics, and tracing analogues |
---

[← Previous: AI Engineering](../20.12-ai-engineering/INDEX.md) · [Next: NestJS →](../20.2-nestjs/INDEX.md)
