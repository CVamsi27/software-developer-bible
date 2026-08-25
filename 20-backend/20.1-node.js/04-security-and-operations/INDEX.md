# Security & Operations - Node.js

> **4 files.** Node-specific security hygiene (input validation, headers, rate limiting, dependency scanning, prototype pollution), runtime diagnostics (debugging, profiling, leak hunts), framework internals (Express chain vs Fastify hooks), plus the full-stack interview self-test for the whole runtime.

[![Files](https://img.shields.io/badge/files-4-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Security%20%26%20Operations-success)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Node.js Security](20.1.4.01-node-security.md) | Input validation (Zod, Joi), injection prevention, password hashing (bcrypt/argon2), Helmet.js, rate limiting, prototype pollution, `npm audit`/Snyk | 25 min |
| 02 | [Debugging & Profiling](20.1.4.02-debugging-profiling-nodejs.md) | `node --inspect` + Chrome DevTools, `--prof` tick logs, heap snapshots + comparison for leaks, Clinic.js doctor/heapprofiler, event-loop lag monitoring, diagnostics reports without restarts | 30 min |
| 03 | [Express & Fastify Internals](20.1.4.03-express-fastify-internals.md) | Middleware chain model, arity-4 error handlers, mount paths, Fastify hook lifecycle, plugin encapsulation, schema-based serialization, benchmark caveats, migration notes | 25 min |
| 04 | [Interview Questions](20.1.4.04-interview-questions.md) | 50 curated questions covering event loop, streams, buffers, clustering, child processes, security; focus Senior tier for 5+ YoE | 3 hrs |

---

[← Back to Node.js](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
|-------|-----------------|
| Input validation at the boundary | `apps/api/src/shared/common/pipes/zod-validation.pipe.ts` - Zod schemas validate every controller payload |
| Security headers & edge hygiene | `apps/api/src/main.ts` - helmet() CSP headers, CORS allow-list, Sentry wired before first request |
| Express middleware chain | `apps/api/src/app.module.ts` - global APP_GUARD / APP_INTERCEPTOR registrations show the exact chain order |
| Runtime observability | `apps/api/src/shared/common/interceptors/request-logging.interceptor.ts` - structured request logs beside slow-query logging |
| Rate limiting | `apps/api/src/shared/common/interceptors/rate-limit.interceptor.ts` - cache-backed per-route limits next to IP/user guards |

_Debugging/profiling internals (`--inspect`, heap snapshots): no direct docita implementation yet._ Observability is pino + Sentry + Prometheus rather than V8 diagnostics tooling.
