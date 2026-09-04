# 01 — Architecture Decisions

> DDD, Zod-first types, NestJS modules, monorepo structure — the foundation choices that shaped everything.

---

## Context

Docita started as a single NestJS app with everything in one folder. As we added domains (patients, appointments, billing, prescriptions, WhatsApp...), services started importing from each other. A change in billing broke prescriptions. A refactor in appointments required touching 5 other domains. We needed structure.

**The problems we faced:**

1. **Coupling** — Services importing from each other created a dependency web
2. **Type drift** — TypeScript interfaces, Prisma models, and NestJS DTOs diverged
3. **Testability** — Business logic was coupled to Prisma, making unit tests impossible
4. **Onboarding** — New developers couldn't understand the codebase structure

---

## Decision 1: Domain-Driven Design (DDD)

### What We Chose

Each business domain gets its own module with 4 layers:

```text
domains/appointments/
├── core/                    → entities, value objects, repository interfaces
│   ├── entities/
│   │   └── appointment.entity.ts
│   ├── value-objects/
│   │   └── appointment-status.value-object.ts
│   ├── domain-services/
│   │   └── appointment-scheduling-rules.service.ts
│   └── repositories/
│       └── appointment.repository.interface.ts
├── application/             → use-cases, DTOs, service orchestration
│   ├── use-cases/
│   │   ├── create-appointment.use-case.ts
│   │   └── start-consultation.use-case.ts
│   ├── services/
│   │   ├── appointment-command.service.ts
│   │   └── appointment-query.service.ts
│   └── dto/
├── infrastructure/          → Prisma repositories, external API adapters
│   ├── persistence/
│   │   ├── prisma-appointment-read.repository.ts
│   │   └── prisma-appointment-write.repository.ts
│   └── mappers/
└── presentation/            → NestJS controllers, guards, interceptors
    └── controllers/
        ├── appointments.controller.access.ts
        └── appointments-schedule.controller.ts
```

### Alternatives Considered

| Option | Pros | Cons |
| -------------------------------- | ------------------------------- | -------------------------------------- |
| **Flat folder structure** | Simple, fast to start | Becomes unmaintainable at 29 domains |
| **Feature-based (by UI route)** | Co-locates related code | Business logic mixed with presentation |
| **DDD (chosen)** | Clear boundaries, testable core | More boilerplate per domain |
| **Hexagonal (ports & adapters)** | Maximum testability | Overkill for our team size |

### Why DDD Was Chosen

**The tipping point:** A developer added a `findAllByClinicId` method to the patient repository. It worked. But it queried across the prescription table too — without going through the prescription domain. When we refactored prescriptions, the patient module broke.

**The key insight:** Repository interfaces live in `core/`. Only infrastructure implements them. Business logic in `core/` has zero framework imports — no Prisma, no NestJS, no `@Inject`. This means:

- `Appointment` entity can be tested without a database
- `AppointmentSchedulingRulesService` can be unit-tested with plain objects
- Repository interfaces are contracts — swap Prisma for anything

**Rule enforced by CI:** `check:prisma-boundary` fails the build if any file outside `infrastructure/` imports `PrismaClient`.

### Trade-offs

| What We Gained | What We Gave Up |
| ------------------------------------------ | --------------------------------------------- |
| Clear module boundaries | More boilerplate (4 files per domain minimum) |
| Testable business logic | Slightly longer initial development |
| Safe refactoring within domains | Need discipline to maintain boundaries |
| Easy onboarding (structure is predictable) | NestJS module wiring is verbose |

### What Worked

- **29 domains without coupling** — each domain can be modified independently
- **Test coverage** — ~5,077 non-e2e test cases repo-wide (measured 2026-09-03), API domain suites the largest share
- **CI enforcement** — boundary violations caught at build time, not code review

### What Failed

- **NestJS module wiring** — every domain needs a `Module` class that imports all providers. With 29 domains, this is ~500 lines of pure wiring code. We solved it with a `DOMAIN_MODULES` array in `app.module.ts`.

- **Cross-domain queries** — sometimes you genuinely need data from another domain (e.g., invoice generation needs patient data). We use port interfaces (`PatientPersistencePort`) instead of direct imports. But it's still tempting to shortcut.

### What Could Be Better

- **Shared kernel** — a `shared/` domain for cross-cutting concerns (audit, notifications) could reduce duplication
- **Module generation CLI** — a `nest g domain patients` command would eliminate boilerplate
- **Event-driven cross-domain communication** — instead of ports, emit events and let other domains subscribe

### Code Evidence

| Claim | File |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| Appointment entity | `apps/api/src/domains/appointments/core/entities/appointment.entity.ts` |
| Scheduling rules | `apps/api/src/domains/appointments/core/domain-services/appointment-scheduling-rules.service.ts` |
| Repository interface | `apps/api/src/domains/appointments/core/repositories/appointment.repository.interface.ts` |
| Use case | `apps/api/src/domains/appointments/application/use-cases/create-appointment.use-case.ts` |
| Prisma repository | `apps/api/src/domains/appointments/infrastructure/persistence/prisma-appointment-read.repository.ts` |
| CI boundary check | `scripts/checks/check-prisma-boundary.mjs` |

### Interview Script (60 seconds)

> "I structured Docita using DDD with 4 layers per domain: core (entities, repository interfaces), application (use-cases, DTOs), infrastructure (Prisma adapters), and presentation (controllers). The key rule: only infrastructure imports PrismaClient. This means business logic is testable without a database — we have ~5,077 non-e2e test cases repo-wide (measured 2026-09-03). The trade-off is more boilerplate, but at 29 domains, the boundary enforcement pays for itself. A CI check catches any boundary violations at build time."

---

## Decision 2: Zod-First Types

### What We Chose

Zod schemas in `packages/types` are the single source of truth. All other types are inferred:

```typescript
// packages/types/src/patients/create-patient.schema.ts
export const createPatientSchema = z.object({
  firstName: z.string().min(1),
  lastName: z.string().min(1),
  phoneNumber: z.string().regex(/^\+?[1-9]\d{1,14}$/),
  dateOfBirth: z.string().datetime(),
  gender: z.enum(['MALE', 'FEMALE', 'OTHER']),
  // ...
});

export type CreatePatientInput = z.infer<typeof createPatientSchema>;
```

**Flow:** `Zod Schema → infer TS types → API contracts → UI forms → DB-safe DTOs`

### Alternatives Considered

| Option | Pros | Cons |
| ------------------------- | -------------------------------------------- | ----------------------------------------------- |
| **TypeScript interfaces** | Native, no dependency | No runtime validation, can't infer Prisma types |
| **io-ts** | Functional, composable | Steeper learning curve, less ecosystem |
| **Zod (chosen)** | Great DX, Prisma integration, error messages | Slightly verbose definitions |
| **class-validator** | Decorator-based, NestJS native | Tied to class instances, harder to compose |
| **JSON Schema** | Language-agnostic | Verbose, less TypeScript integration |

### Why Zod Was Chosen

**The tipping point:** A field was added to the Prisma schema (`Patient.secondaryPhone`) but not to the TypeScript interface. The API accepted the field silently (Prisma ignored it). The frontend didn't send it. Nobody noticed for 2 weeks.

**The key insight:** Zod schemas are *validated at runtime*. If the API receives unexpected data, it fails fast with a clear error message. And `z.infer` generates TypeScript types automatically — no drift possible.

### Trade-offs

| What We Gained | What We Gave Up |
| ----------------------------------------------- | --------------------------------------------------- |
| Zero type drift between Prisma, API, and UI | Slightly verbose schema definitions |
| Runtime validation with clear error messages | Can't use complex class-based patterns |
| Single source of truth | Learning curve for team members unfamiliar with Zod |
| Auto-generated API documentation (from schemas) | Schema files are longer than plain interfaces |

### What Could Be Better

- **Schema composition** — some schemas repeat the same 5 fields (clinicId, patientId, etc.). A `commonFields` base schema would reduce duplication.
- **Auto-generate Prisma types from Zod** — currently we manually align Zod schemas with Prisma models. A code generator could enforce this.
- **Frontend form integration** — we manually map Zod schemas to React Hook Form validation. A generator could produce form configs from schemas.

### Code Evidence

| Claim | File |
| -------------- | ---------------------------------- |
| Zod schemas | `packages/types/src/` |
| Prisma models | `packages/db/prisma/schema.prisma` |
| Type inference | `packages/types/src/patients/` |

### Interview Script (60 seconds)

> "I used Zod schemas as the single source of truth for all types. A Zod schema defines the shape, `z.infer` generates the TypeScript type, and the same schema validates API requests at runtime. This eliminated type drift between Prisma models, API contracts, and UI forms. The trade-off is slightly more verbose definitions, but we caught zero type-related bugs after adopting this pattern. It also gave us runtime validation — if an API receives unexpected data, it fails fast with a clear error message instead of silently ignoring the field."

---

## Decision 3: NestJS with Separate API + Worker Processes

### What We Chose

Two NestJS processes sharing the same codebase:

```text
apps/api/     → HTTP controllers, WebSocket gateways, authentication
apps/worker/  → Queue job processing, cron schedulers, PDF generation
```

Both import from `apps/api/src/domains/`. The worker has its own `worker.module.ts` that only imports the modules it needs.

### Alternatives Considered

| Option | Pros | Cons |
| ---------------------------------- | ------------------------------ | ------------------------------------- |
| **Single process** | Simple deployment | Queue processing blocks HTTP requests |
| **Separate repos** | Independent deployment | Code duplication, sync issues |
| **Monorepo, shared code (chosen)** | Zero duplication, shared types | Must coordinate deployments |
| **Serverless functions** | Auto-scaling | Cold starts, stateful operations hard |

### Why Separate Processes Were Chained

**The problem:** PDF generation takes 2-3 seconds. If it runs in the HTTP process, it blocks the event loop. A clinic generating a prescription PDF would slow down all other API requests.

**The solution:** The API emits a `prescription.created` event → outbox → worker picks up the job → generates PDF → stores in R2 → notifies via WebSocket.

### What Could Be Better

- **Shared health checks** — the API and worker have separate health endpoints. A unified dashboard would be better.
- **Graceful shutdown coordination** — if the worker is processing a job when the API deploys, the job might fail. We need coordinated drain.

---

## Decision 4: Monorepo with pnpm Workspaces

### What We Chose

```text
docita/
├── apps/
│   ├── api/          → NestJS API
│   ├── app/          → Vite SPA (main clinic dashboard)
│   ├── internal/     → Vite SPA (admin portal)
│   └── landing/      → Astro (marketing site)
├── packages/
│   ├── db/           → Prisma schema + migrations
│   ├── types/        → Zod schemas
│   ├── ui/           → Shared React components
│   ├── data-access/  → React Query hooks + Axios
│   └── authorization/ → ABAC policy engine
└── fly.toml
```

### Why Monorepo

- **Shared types** — `packages/types` is used by both API and frontend
- **Atomic commits** — a schema change and its API/frontend updates ship together
- **Single CI pipeline** — one `pnpm build` catches all issues
- **Dependency deduplication** — React, NestJS, Prisma shared across apps

### What Could Be Better

- **Build caching** — we don't use Turborepo or Nx. Build times are ~3 minutes. Turborepo could cut this to ~30 seconds.
- **Dependency isolation** — a breaking change in `packages/ui` can break all apps. We need stricter versioning.
---

[ Back to Index](INDEX.md) · [Next: Multi Tenancy Rls →](02-multi-tenancy-rls.md)
