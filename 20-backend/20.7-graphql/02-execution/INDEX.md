# Execution - GraphQL

> **Study time:** ≈ 1 h 8 m of reading (2 files, ~34 min average).
> **2 files.** How the server resolves queries: resolver chains with DataLoader for N+1 prevention, and Apollo Server's plugin model, federation, and subscriptions.

[![Files](https://img.shields.io/badge/files-2-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Execution-%23ff6b35)](../INDEX.md)

---

## Files

| Order | File | Topics | Read time |
| --   : | ------ | -------- | ----------: |
| 01 | [Resolvers](20.7.2.01-resolvers.md) | Resolver chain, `(parent, args, context, info)`, default resolvers, DataLoader batching/caching (N+1 fix), `GraphQLError` + `extensions.code` | 35 min |
| 02 | [Apollo Server](20.7.2.02-apollo-server.md) | Server setup (Express/Fastify/Lambda), plugins, landing page/Explorer, CSRF prevention, federation, subscriptions; Yoga/Mercurius alternatives | 33 min |

---

[← Back to GraphQL](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

_No direct docita implementation yet._ No resolvers, DataLoader, or Apollo server exist — `apps/api/package.json` has no GraphQL dependency (REST-first choice). The closest execution analog is use cases resolving through repository ports: `apps/api/src/domains/appointments/application/use-cases/create-appointment.use-case.ts`.
---

[← Previous: Fundamentals](../01-fundamentals/INDEX.md) · [Next: Clients & Production →](../03-clients-and-production/INDEX.md)
