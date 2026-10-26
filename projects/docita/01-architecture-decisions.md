# 01 — Architecture: Keep Business Rules, Contracts and Execution Boundaries Clear

[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Important-blue)](../../docs/topic-importance.md)



Consider creating an appointment. An HTTP request needs validation and authorization, scheduling rules, persistence, and possibly later notifications. Putting these responsibilities in one service makes every change harder to test and reason about. Separating them helps only when the boundaries remain visible in the actual imports and execution path.

## Definition

Architecture assigns responsibilities and controls dependencies. In Docita, domain modules organize business capabilities; shared schemas define application contracts; separate API and worker entry points divide interactive requests from background work.

> **Textbook Definition:** Software architecture defines a system's elements, their responsibilities and relationships, and the constraints governing their evolution. An architectural boundary is effective only where dependencies and execution honor it.

This case study describes source inspected on **2 October 2026**. Source structure is evidence of implementation, not proof that every production path or verification gate currently passes. Earlier incident stories, test totals and build-speed claims lacked supporting evidence and are not treated as measured outcomes here.

## First Principles

Three constraints drive the design:

1. Business rules outlive individual HTTP handlers and database adapters.
2. TypeScript types disappear at runtime, while requests and stored data still cross trust boundaries.
3. Background work can outlive a request and compete for CPU, connections and deployment resources.

The design therefore needs explicit dependency contracts, executable input validation and separate lifecycles. Adding folders alone satisfies none of these constraints.

## Why Separate Responsibilities Before Adding More Modules?

A scheduling rule should be testable without starting an HTTP server. A controller should not need to know how a database query is constructed. A background processor should not assume the request's tenant context or transaction is still available.

These are different boundaries. Domain-driven design organizes code around business capabilities and rules. Ports are interfaces that state what the application needs; adapters connect those interfaces to a database, transport or other tool. They keep dependencies pointed toward application contracts. These approaches can be used together.

## How an Appointment Crosses the Domain Layers

```text
HTTP presentation
  → application use case: coordinate one business operation
    → core rules/entities/ports: express the decision and contracts
      → infrastructure adapter: perform persistence or external I/O
```

| Layer | Responsibility | Appointment source example |
| -------------- | ------------------------------------------------------------------- | --------------------------------------------------------------- |
| Presentation | Translate HTTP input and apply transport concerns | Domain controllers |
| Application | Coordinate validation, rules and repository calls | `create-appointment.use-case.ts` |
| Core | Express scheduling rules, entity behavior and persistence contracts | `appointment-scheduling-rules.service.ts`, repository interface |
| Infrastructure | Implement persistence through Prisma | `prisma-appointment-read.repository.ts` |

The inspected create use case rejects a start time at or after the end time, asks scheduling rules to validate overlap, constructs an appointment entity, then saves through a repository. This gives a focused test seam: supply controlled dependencies and inspect the decision and save request.

**A pre-save overlap query is not a concurrency guarantee.** Two requests can both observe an available slot before either saves. The final persistence operation needs a suitable constraint, lock or transaction protocol to enforce the scheduling invariant; see the [concurrency case](05-clinic-workflows.md).

### The Core Is Not Completely Framework-Free

The current scheduling rules service imports NestJS injection and exception APIs and an appointment status from the database package. Some repository contracts also use Prisma types. The accurate claim is that important persistence behavior is accessed through interfaces—not that every core file is independent of frameworks.

Removing framework dependencies can make a rule easier to reuse and test, but it costs adapter and mapping work. Decide whether that isolation earns its complexity for the rule being maintained.

The current `check:prisma-boundary` command invokes `scripts/checks/check-prisma-boundary.js --enforce-prisma-service`. Its rules target particular imports and locations and include legacy exceptions. A configured check is useful enforcement; it does not establish zero coupling or prove that the current checkout passes it. Feature-boundary checks complement it because a domain can become coupled without directly constructing a Prisma client.

## How Shared Zod Schemas Connect Runtime Input and TypeScript

A schema is executable validation. An inferred type describes the schema's output to TypeScript. Sharing that schema can reduce duplicated API/form definitions, provided each boundary actually parses its input.

The inspected patient contract lives at `packages/types/src/patient/patients.ts`. Its create schema extends the patient schema and makes date of birth required. The following is a **standalone illustration of that relationship**, not a copy of the full patient contract:

```typescript
import { z } from "zod";

const patientSchema = z.object({
  firstName: z.string().min(1).max(100),
  dateOfBirth: z.string().optional(),
});
const createPatientSchema = patientSchema.extend({
  dateOfBirth: z.string().min(1),
});
type CreatePatientInput = z.infer<typeof createPatientSchema>;

const input: CreatePatientInput = createPatientSchema.parse({
  firstName: "Ada",
  dateOfBirth: "1990-01-01",
});
```

The real contract additionally checks that the date parses and lies in the past and contains other fields and transformations. Validation must run before trusted application logic; importing the inferred type alone does not validate a request. If a schema transforms values, distinguish its input type from its output type.

### Validation Is Not Database Alignment or Authorization

An ordinary Zod object strips unknown keys by default rather than necessarily rejecting them. Select the unknown-key policy deliberately and use the installed version's strict-object API when rejection is required.

A valid request can still violate a database uniqueness constraint, reference another tenant, or request an unauthorized operation. Prisma models and Zod contracts remain separate definitions unless a verified generation process connects them. Migrations, contract tests and authorization checks address different risks. Do not present shared inference as eliminating every kind of drift.

## Why the Worker Has Its Own Process and Module

`apps/worker/src/main.ts` creates a Nest application context using `apps/api/src/worker.module.ts`. That module imports worker-specific domain modules, Prisma worker configuration, schedulers and outbox support. The entry point registers shutdown handling and closes the application context, with a bounded forced-exit fallback.

A separate process provides a separate event loop and lifecycle. CPU-heavy JavaScript in the API process blocks its event loop; awaiting asynchronous I/O does not inherently block it for the entire elapsed duration. Moving work to a worker helps isolate request latency and permits separate scaling, but both processes can still compete for the same database or host resources.

```text
API: validate and authorize → commit durable work intent → return
Worker: claim work → perform side effect → record result/retry state
```

This is the intended responsibility split. The [jobs and outbox case](03-async-processing.md) explains the actual delivery protocol and its failure boundaries. Separate processes alone do not make delivery reliable or effects occur exactly once. Workers need explicit tenant scope, retry rules, idempotency and graceful draining; starting another process supplies none of them automatically.

## How the Monorepo Supports Coordinated Changes

pnpm workspaces organize applications and shared packages. The current root build uses **Turborepo** (`turbo build --concurrency=1`); the earlier claim that build caching had not been introduced was outdated.

| Shared package | Role | Boundary to retain |
| --------------- | -------------------------------------------- | ----------------------------------------------------------- |
| `types` | Application contracts and validation schemas | Parse at runtime; keep persistence and permissions separate |
| `db` | Prisma models and migrations | Review data changes and compatible rollout order |
| `ui` | Reusable React components | Avoid assuming every consumer upgrades at once |
| `data-access` | Client fetching and server-state integration | Keep cache identity and tenant scope explicit |
| `authorization` | Policy evaluation | Supply trustworthy identity and resource attributes |

One commit can contain compatible API, UI and schema changes. **Deployment is still not atomic:** old and new processes can coexist during rollout. Additive contracts and expand–migrate–contract database changes help accommodate that interval. A shared workspace also does not guarantee one dependency version or that a build checks runtime behavior.

## Real-World Decisions

| Situation | Useful choice | Cost or limitation |
| ----------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------- |
| Small straightforward CRUD feature | Keep a cohesive module with clear responsibilities | Four layers for every trivial action can add ceremony |
| Business invariant with multiple callers | Put the rule behind explicit dependencies and test it directly | Persistence still has to enforce concurrent correctness |
| API and forms share a contract | Share a runtime schema and infer types | Database and authorization rules remain separate |
| Work outlives the request or consumes substantial CPU | Durable background processing with its own lifecycle | Retry, duplicate handling and capacity become explicit work |
| Related applications change together | Monorepo with dependency-aware tasks | Coordinated source changes still require compatible deployment |

## Mistakes

- Treating folder names as proof of dependency isolation.
- Claiming framework-free core logic while the actual imports contradict it.
- Assuming a successful schema parse proves authorization or database consistency.
- Describing every slow asynchronous operation as event-loop blocking.
- Equating a shared commit, build or worker process with atomic deployment or reliable delivery.

## Best Practices

Trace one real operation through its layers before describing the architecture. State which dependency check is enforced, what it permits and whether its current result was measured. Test business decisions separately from persistence concurrency and contract validation. For a rollout, explain what happens when old and new application versions coexist.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Ports, application services and separate worker entry make business capabilities and process responsibilities visible. |
| Current limitations | Core still imports framework/database types, and allowlisted boundary checks permit known coupling. |
| Recommended design | Keep business rules independent of adapter types; expose narrow capability ports, enforce dependency direction, and replace allowlists incrementally with tested seams. |
| Evidence needed | A core package compiles without Nest or Prisma; architecture checks reject a planted forbidden dependency; an adapter contract test exercises both success and failure. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

The useful boundaries are business rules behind contracts, runtime validation at trust boundaries, durable work across process lifecycles and compatible changes across deployments. Docita implements parts of these boundaries; its source does not support absolute claims of zero coupling, zero drift or automatic reliability.

## See Also

- [Category revision](REVISION.md) — recall and decision practice after reading the cases.
- [Tenant isolation](02-multi-tenancy-rls.md) — identity, transaction routing and database policy.
- [Jobs and outbox](03-async-processing.md) — durable intent and delivery failures.
- [Concurrency and slot reservation](05-clinic-workflows.md) — protecting scheduling invariants.
- [Case-study index](INDEX.md) — learning order.

## References

Source paths below refer to the Docita repository inspected on 2 October 2026:

- `apps/api/src/domains/appointments/application/use-cases/create-appointment.use-case.ts`
- `apps/api/src/domains/appointments/core/domain-services/appointment-scheduling-rules.service.ts`
- `apps/api/src/domains/appointments/core/repositories/appointment.repository.interface.ts`
- `apps/api/src/domains/appointments/infrastructure/persistence/prisma-appointment-read.repository.ts`
- `packages/types/src/patient/patients.ts`
- `apps/worker/src/main.ts` and `apps/api/src/worker.module.ts`
- `package.json`, `turbo.json` and `scripts/checks/check-prisma-boundary.js`
