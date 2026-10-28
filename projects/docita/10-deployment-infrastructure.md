# 10 — Deployment: Keep Versions, Schema and Background Work Compatible

[![Role priority](https://img.shields.io/badge/role--priority-Important-blue)](../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Specialized-lightgrey)](../../docs/topic-importance.md)



Consider a release that adds an invoice field and changes a PDF job payload. A successful build is only the start: old API instances, new workers, existing jobs and the database can overlap during rollout. The release must preserve their contracts and provide evidence that the new version works.

## Definition

Deployment changes running application versions and their configuration. In Docita, the API and worker run as separate Fly applications. The React single-page application (SPA) loads its interface in the browser, while an API proxy forwards browser API requests to the backend. Cloudflare Workers serve that proxy and the static application assets.

> **Textbook Definition:** Deployment replaces or introduces running software and configuration while managing compatibility among application versions, persistent schemas and queued work. A release is complete only within its defined verification boundary.

This case began with source inspected on **2 October 2026**. A **28 October 2026** refresh inspected canonical Docita revision `f3fddffc0`, read Fly machine inventory and checked scheduled-workflow state. The API and worker each had one stopped machine in Singapore. The current database provider was confirmed as temporarily Neon; its account tier, compute envelope and storage were not independently inspected. AWS RDS remains the future production reference. Configuration, an inventory snapshot and a completed workload experiment establish different facts.

## First Principles

Applications and databases do not switch versions as one atomic unit. Requests and jobs can outlive a process, a healthy process can still perform incorrect work, and routing infrastructure can acknowledge traffic before all application dependencies are ready.

A useful release protocol therefore separates build validation, schema compatibility, process readiness, business probes, rollout and recovery. Each stage must state what it actually establishes.

## Why Separate API, Worker and Browser Deployment?

| Component | Responsibility | Source evidence |
| ----------------------------- | -------------------------------------- | ------------------------------------------------ |
| Fly API application | HTTP requests and application services | Root `fly.toml`, API Dockerfile |
| Fly worker application | Background processors and schedulers | `apps/worker/fly.toml`, worker entry point |
| Cloudflare application Worker | API proxy and asset integration | `apps/app/api/index.ts`, shared proxy factory |
| Static SPA assets | Browser interface and client routing | App Wrangler assets configuration |
| PostgreSQL and object storage | Durable state and files | Persistence/storage configuration and migrations |

Separating lifecycles permits different capacity and rollout decisions. It also introduces compatibility requirements. A new worker may consume a job produced by an old API; a cached browser bundle may call a newer server.

## How the Current Fly Configuration Handles Idle Traffic

The checked-in API configuration uses:

```toml
[http_service]
internal_port = 3001
force_https = true
auto_stop_machines = 'suspend'
auto_start_machines = true
min_machines_running = 0
```

It declares Singapore (`sin`) as the primary region and a 512 MB shared-CPU VM. This source does **not** support the earlier claim that one API machine is always kept warm. The worker has its own configuration, declares a 256 MB VM and enables schedulers; it has no HTTP service block in that file.

Fly autostop/autostart manages existing machines. It does not automatically create additional machines, and the minimum-running setting applies to the primary region. Worker lifecycle and capacity must be managed separately when there is no proxy-routed HTTP service. [Fly autostop/autostart documentation](https://docs.fly.io/launch/autostop-autostart).

A warm minimum may reduce idle-start delays, but it cannot guarantee no cold starts or no errors during replacement, failure or regional disruption. Measure startup, readiness and first-request latency under the actual memory limits before selecting the trade-off. The old three-minute bootstrap incident, proxy-timeout and monthly-cost figures were not verified in this review.

## Trace the Deployment Before Choosing a Machine

A request and a document job use different execution paths. Starting the API can restore interactive requests while leaving the background worker stopped. The worker has no incoming HTTP service in its checked-in configuration, so the API's Fly Proxy wake-up settings do not wake that worker.

```text
Browser
  | HTTPS: application assets, authenticated API calls
  v
Cloudflare: SPA assets + same-origin API proxy
  | HTTPS: identity/session and request forwarded to backend
  v
Fly API, Singapore                         Provider callbacks
  | HTTP business rules <---------------- HMAC-verified ingress
  | tenant-scoped transaction
  +----------------------+------------------------+
  |                      |                        |
  v                      v                        v
PostgreSQL            Cloudflare R2          Process-local events
  | business rows       | document objects     | local socket clients
  | QueueJob/Outbox     |                      | no replica-wide bus implied
  ^                     ^
  | claim/acknowledge    | upload completed artifact
  +---------------------+
  |
Fly worker, Singapore
  | PDFKit, scheduled work, retries and outbox dispatch
  v
External providers: messages, email and payment-related effects

Database placement:
  current temporary host: Neon; account resources not yet verified
  future reference: AWS RDS; same-region placement is a design choice
```

The diagram shows responsibilities, not proof that every route emits a durable outbox event. Read [background work](03-async-processing.md) for the exact transaction and acknowledgment boundaries. Database traffic and file payload traffic require separate network, access and backup policies.

## Read CPU, RAM, Heap and Swap as Different Limits

The following source settings were inspected on 28 October. The read-only Fly inventory agreed with the guest CPU/RAM sizes, but a stopped machine provides no current CPU-utilization or memory-pressure measurement.

| Resource | API | Worker | Interpretation |
| ------------------------------ | ------------- | --------------- | --------------------------------------------------------------- |
| Guest CPU | 1 shared vCPU | 1 shared vCPU | A schedulable virtual CPU, with shared-CPU quota/burst behavior |
| Guest RAM | 512 MiB | 256 MiB | Total guest memory envelope, not just JavaScript objects |
| V8 old-space ceiling | 384 MiB | 192 MiB | Requested Node heap setting, not a total RSS limit |
| Configured swap | 512 MiB | 512 MiB | Disk-backed memory; not additional low-latency RAM |
| Observed machine count/state | 1, stopped | 1, stopped | Dated inventory; requests and jobs were not load-tested here |
| Proxy request soft/hard limits | 60 / 100 | No HTTP service | Routing thresholds, not measured throughput or database slots |

[Fly's CPU documentation](https://fly.io/docs/machines/cpu-performance/) distinguishes shared and performance CPU scheduling. Inspect quota balance and throttling during a sustained run. A short burst can look healthy while a longer run exhausts accumulated CPU allowance. A Node event loop can also be saturated even when adding more virtual CPUs would not parallelize that JavaScript work automatically.

```text
Guest RAM budget
+----------------------------------------------------------+
| V8 old space: application objects and caches               |
| V8 other spaces + runtime/native allocations               |
| Driver/Prisma runtime + TLS/socket buffers                  |
| PDFKit pages, fonts/images, document and upload Buffers     |
| Operating-system and process overhead                      |
+----------------------------------------------------------+
        | allocation pressure / reclaim
        v
Swap: separate disk-backed allowance, with latency consequences

RSS measures resident process memory across relevant allocations.
A heap ceiling below guest RAM does not prove adequate RSS headroom.
```

PDF generation here uses PDFKit with buffered pages, not a Chromium subprocess. Two registered PDF job names can still run at the same time and retain two document buffers. Measure maximum document size, simultaneous handlers, RSS, heap, garbage-collection pauses and swap activity. If heap stays stable while RSS grows, investigate buffers/native memory before raising the V8 ceiling. If both settle after a burst, the peak may be a bounded working set rather than a leak.

## Separate Existing Capacity From Machine Lifecycle

[Fly autostop/autostart](https://fly.io/docs/reference/fly-proxy-autostop-autostart/) starts or suspends machines that already exist. A different controller or an explicit scale operation is needed to create more capacity. With one existing API machine, the configured request limits cannot create a second machine.

```text
Configured machine pool: [ API A ] [ API B, only if provisioned ]
                              ^               ^
                              | start/suspend |
                        Fly Proxy lifecycle control
                              ^
                         incoming requests

Separate capacity decision:
  observed sustained pressure -> reviewed scale policy -> create/remove machine

Worker queue depth does not become HTTP traffic automatically.
A stopped worker needs an explicit lifecycle policy.
```

At this inspection, the scheduled scale-hours, synthetic-monitoring and daily-worker workflows reported `disabled_manually`. The standards gate also flagged the daily-worker schedule as stale, with its last run nine days old. That is a dated account observation. Their historical Mumbai comments are not a reason to move the current Singapore configuration. Re-enabling a schedule, starting a stopped worker and providing resilient capacity are separate operational decisions.

The current cache, several rate counters and socket/event delivery are process-local. Adding API replicas can multiply effective per-replica limits and split notifications between processes. Before horizontal growth, decide which limits must be atomic across replicas, how invalidation propagates, and how clients recover missed updates. A Redis-looking environment value alone does not establish a shared adapter.

## Keep the Cheap Deployment and Future Balanced Reference Distinct

The current implementation should retain the existing paid-resource limits. The future column is a **starting configuration to benchmark**, not a measured requirement or an applied upgrade.

| Component | Current low-cost operation | Future balanced reference, pending budget and measurements |
| ------------ | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| API | Existing 1 shared vCPU / 512 MiB guest; allow idle suspension | Evaluate 2 API machines, 1 shared vCPU / 1 GiB each, with one warm and the second available for traffic |
| Worker | Existing 1 shared vCPU / 256 MiB guest; currently stopped | Evaluate 1 worker, 1 shared vCPU / 512 MiB, running while scheduled jobs are promised |
| Database | Temporary Neon; retain its existing tier/settings | Evaluate AWS RDS PostgreSQL `db.t4g.medium`: 2 vCPU / 4 GiB, with 50 GiB gp3 as a reviewed initial allocation |
| File storage | R2 document objects; usage not measured in this inspection | Retain object storage; measure bytes, access, lifecycle and recovery separately |
| Availability | Cold starts and stopped background processing remain visible | Warm API plus spare capacity; database failover and a redundant worker require their own design and cost review |

AWS publishes the [RDS instance specifications](https://aws.amazon.com/rds/instance-types/). The T4g reference is burstable; CPU-credit use and possible surplus charges belong in its cost assessment. Fifty GiB is an illustrative allocation with maintenance headroom, not a calculation from 25 clinics. Check measured data/index growth, write I/O, WAL, temporary files and restore needs before accepting it. Multi-AZ changes availability, cost and failover behavior; it is not implied by the instance class.

For Neon, distinguish the configured minimum/maximum compute from the compute active at an instant. Record actual account settings and storage from the console/API rather than guessing a tier from the hostname. [Neon's pooling documentation](https://neon.com/docs/connect/connection-pooling) describes transaction pooling: many client connections can share fewer database sessions. That does not give those clients independent CPU, memory or transaction capacity. Keep tenant context transaction-local and test it through the chosen pooler. Use the provider's direct endpoint for operations that require a session or migration semantics unsupported by the pooled path.

## Establish Database Size Without Confusing Four Quantities

Provider inventory establishes allocated CPU/RAM/storage. PostgreSQL establishes its settings and logical data sizes. Runtime monitoring establishes pressure. A workload experiment connects that pressure to a specific request mix.

```sql
-- Authorized read-only inspection; save only permitted aggregates.
SELECT pg_size_pretty(pg_database_size(current_database())) AS used_database_bytes;
SHOW max_connections;
SHOW shared_buffers;
SHOW work_mem;

SELECT relname,
       pg_total_relation_size(relid) AS total_relation_bytes,
       pg_indexes_size(relid) AS index_bytes
FROM pg_catalog.pg_statio_user_tables
ORDER BY total_relation_bytes DESC
LIMIT 10;
```

The formatted `pg_database_size` result is used database space, not purchased disk capacity. `shared_buffers` is a PostgreSQL cache setting, not machine RAM. `pg_total_relation_size` already includes related indexes and TOAST storage; do not add those same bytes again. Total server storage also needs WAL, temporary/maintenance work, logs and provider-specific reserved space. Object-store PDFs and backup copies need their own accounting.

For the future RDS reference, inspect instance class, allocated/max storage, storage type, Multi-AZ and backup retention. Then inspect [RDS runtime metrics](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-metrics.html): CPU, freeable memory, connections, free storage, I/O latency/queueing and applicable burst balances. A database can be connection-bound or I/O-bound before CPU reaches its limit. A high cache-hit ratio does not excuse a slow query or a long transaction.

## Set Up and Release Through Explicit Gates

Use this order for a new environment or the later Neon-to-AWS move. These are reviewed setup steps, not actions performed during this inspection.

1. Inventory machines, database tier/region, connection endpoints, storage and backup policy. Choose a low-cost or balanced profile explicitly. Record current stopped/running states before changing them.
2. Validate an isolated local environment first: install the locked pnpm dependencies, generate Prisma, apply the schema only to a positively identified disposable database, and run [the workload protocol](23-hypothetical-clinic-metrics.md#turn-the-model-into-a-reproducible-benchmark). Provider effects must use mocks or approved sandboxes.
3. Establish a reviewed database network path, TLS verification and least-privilege runtime role. Fly and an AWS private VPC do not share networking automatically. Do not solve reachability by opening the database to every public address.
4. Load secrets through the platform secret store. Validate database URL, JWT secret, encryption key, storage credentials and the credentials for enabled provider features. Keep migration/admin access separate from the tenant-scoped application role. Do not paste secret values into documentation or shell history.
5. Set the API and worker responsibilities deliberately: HTTP API on its configured port, schedulers disabled there, queue backend PostgreSQL, storage R2, and schedulers enabled in the worker. Verify the chosen RLS path against real pooled connections before traffic.
6. Apply backward-compatible schema changes using the canonical migration procedure, verify schema synchronization and take a recoverable backup. Build immutable API/worker/frontend artifacts from one recorded revision. Preserve compatibility with old browsers and queued payloads.
7. Populate a local/staging synthetic workload and collect actual per-route latency, errors, memory, database pressure and queue completion. The required API latency-baseline gate must fail until a real complete capture exists. A dry-run or a local stub cannot replace it.
8. Start/deploy approved capacity, verify readiness and one authorized business operation, then monitor the rollout. Check worker heartbeat and a real fixture job separately from API liveness. Preserve a bounded rollback decision point.
9. For a database-provider move, rehearse export/restore privately, reconcile schema and row/business invariants, fence writes during final cutover and validate the new writer. Repoint application secrets only after the cutover criteria pass. Preserve the old recovery path until reconciliation finishes.
10. Perform and time a restore rehearsal. Record actual recovery-point and recovery-time results, including application compatibility and integrity checks. A backup policy alone cannot establish them.

```text
Expand schema -> old/new versions overlap -> verify real business probes
                        |                          |
                        | compatible jobs/rows     v
                        +----------------------> traffic cutover
                                                   |
                                      observe -> accept or image rollback

Separate data recovery:
  backup + recovery log -> restore isolated database -> integrity checks
                       -> compatible application -> controlled writer cutover
```

### Reproduce the Local Checks Before a Release

Run these commands in an isolated Docita checkout with Node 24 and the repository's pinned pnpm. The database URL must identify a disposable loopback `docita_capacity_*` database. Generate/apply a full application fixture separately when testing the API; the SQL suite creates only its own projected tables and does not reset the database.

```bash
pnpm install --frozen-lockfile
pnpm --filter @workspace/db run db:generate
pnpm --filter @workspace/types run build
pnpm --filter @workspace/utils run build
pnpm --filter @workspace/auth run build
pnpm --filter @workspace/authorization run build
pnpm --filter @workspace/db run build

# Read-only model; no HTTP request or credential read.
pnpm capacity:plan
pnpm test:capacity

# Use only the positively checked disposable target.
DOCITA_METRICS_TEST_DATABASE_URL="$DATABASE_URL" \
  pnpm --filter @docita/api exec jest \
  --config test/metrics/jest.config.mjs --runInBand

pnpm --filter @docita/api run check-types
pnpm --filter @docita/internal run check-types
pnpm lint
pnpm verify:standard
```

Do not replace a blocked gate with target values or silently skip it. On the 28 October implementation pass, lint/typechecks, focused tests and the internal frontend build passed; the full standards chain stopped at the stale disabled daily-worker workflow. Later standards commands were checked separately, while required API-baseline mode remained blocked by its absent measurement. A local code validation does not authorize or establish a production deployment.

The operational flow for a future approved release remains: reviewed infrastructure/network and secrets, compatible migrations, immutable artifacts, API and worker checks, actual workload measurements, traffic cutover and a tested recovery path. Use the repository's deploy workflow and runbooks for commands that can create cost or change production; a documentation example should not start stopped machines as a side effect of an audit.

## How the SPA and Proxy Form One Browser Origin

The app entry point calls a shared `createCloudflareApiProxy` factory. The configuration supplies an `ASSETS` binding and a single-page-application fallback. The factory handles API and Socket.IO routes and delegates other paths to the assets binding.

A same-origin browser API path simplifies browser routing and cookie handling. It does not remove authentication, CSRF protection, backend authorization or every cross-origin concern. Direct API clients and separately configured socket URLs still need their own protocol review.

### Follow One API Request Across the Proxy

```text
browser: /api/v1/invoices?page=2
  → Worker route extracts API path segments
  → helper builds an upstream URL and preserves query parameters
  → upstream fetch returns status, headers and a response stream
  → proxy rewrites applicable cookie-domain attributes for the app origin
```

The old example concatenated a backend origin with the complete incoming URL; that produces an invalid target. The inspected source instead uses URL parsing and dedicated helpers.

There are important boundaries in the current helper:

- The `/api/v1/*` path buffers non-GET/HEAD request bodies with `arrayBuffer()`. Large concurrent uploads can consume memory; do not describe that request path as streaming.
- It returns the upstream response body as a stream and uses manual redirect handling.
- It filters headers and handles multiple Set-Cookie values. Cookies still require appropriate security attributes and a reviewed host/domain policy.
- Generic API/socket branches use a different forwarding path. Do not assume identical behavior across all routes.
- Path normalization and encoded segments require tests, including existing percent escapes, reserved characters and queries.

For large uploads, evaluate bounded bodies or direct, authorized object-storage uploads. Review forwarded-header trust at the backend rather than trusting arbitrary client-provided identity headers. The [Workers best-practices guidance](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/) favors bounded memory use and streaming unknown-size data.

## Why the Current Bundle-Limit Argument Must Change

The authenticated SPA's rendering needs can justify a Vite client application without an SSR runtime. Compare browser behavior, routing, performance, SEO requirements and operational complexity for the actual product; neither Vite nor Next.js has a universal bundle size.

The old claim that a 3.5 MB gzip Next.js bundle exceeds the current 3 MB Workers Free limit is stale. On the **2 October 2026** check, Cloudflare's limits page specifies **64 MiB uncompressed** Worker size for both Free and Paid, with **no compressed-size limit**. Worker executable code, static assets and browser JavaScript are different artifacts with different constraints. [Current Workers limits](https://developers.cloudflare.com/workers/platform/limits/).

A historical rejection needs its original date and deployment output before it can support a migration story. A modern decision needs current artifact measurements and startup/resource evidence. Static serving also does not establish zero cost for the entire application.

## How Migrations Fit Into the Release

The configured workflow applies safe migrations and then runs `scripts/deploy/verify-db-schema-sync.sh`. The script checks Prisma migration status and compares the configured database to the Prisma schema, failing when verification reports pending migrations or drift.

This is a **deployment verification step**, not evidence that every application startup refuses to run with pending migrations. No production database was queried during the 28 October refresh; database hardware and used bytes remain unverified.

A compatible sequence is:

1. Add schema support that existing code can tolerate.
2. Deploy code able to handle the transition and existing data.
3. Backfill or transform data with observable progress and recovery.
4. Remove obsolete fields or behavior only after old consumers are retired.

Applying a migration before new code is insufficient if it breaks old instances. Likewise, rolling back an image does not undo data changes or external effects. Document destructive steps and recovery separately from process rollback.

## What the Deployment Workflow Currently Enables

The inspected source retains paused production deployment/migration triggers. On 28 October the scale-hours and synthetic-monitoring schedules also reported `disabled_manually`; that limited account check does not establish the status or success of every deployment workflow. Treat the following jobs as configured release behavior, and verify the actual enabled pipeline before a deployment.

Within the configured jobs, change detection maps source paths to affected deploy targets, including shared packages and root build/configuration files. API and worker deployment depend on successful migration verification. The API also has a short startup check and uses **blue-green** deployment: start the new version separately, then switch traffic from the old version to it.

The worker script first deploys the new version to a selected machine as a canary—a limited trial before wider rollout. It checks that the machine remains `started` for a settling window—**90 seconds** in the workflow—then updates the remaining machines in stages through a rolling deployment. Machine state shows that the process remains running; it does not prove that jobs, tenant isolation or external effects are correct. The script itself distinguishes this from live worker health and scheduler heartbeat evidence.

Selective deployment reduces unnecessary changes only when the dependency map includes all affected consumers. Test that map against shared-contract changes; do not reduce it to “only deploy the folder that changed.”

## Real-World Decisions

| Release concern | Useful evidence | What it does not prove |
| --------------------------------------- | --------------------------------------------- | ------------------------------------------------- |
| Container starts within resource limits | Startup smoke and measured memory/startup | Correct business operations |
| HTTP process responds | Health/readiness endpoint results | Worker progress or database invariant correctness |
| Worker stays started | Canary state and heartbeat continuity | Correct delivery or duplicate-safe side effects |
| Database matches schema | Migration status and drift check | Compatibility with every old application version |
| New application can serve traffic | Targeted business probes and observed rollout | Safe reversal of already-applied data changes |
| Shared package changes reach consumers | Dependency-map tests | Atomic simultaneous deployment |

## Mistakes

- Describing paused workflow definitions as an active CI/CD pipeline.
- Assuming a warm setting, blue-green rollout or CDN propagation guarantees zero downtime.
- Confusing compressed Worker code, uncompressed limits, static assets and browser bundles.
- Treating same-origin proxying as complete authentication or security.
- Claiming a deployment schema check runs during every application startup.
- Equating machine liveness with successful background processing.

## Best Practices

Keep configuration claims dated and distinguish source, live settings and measured outcomes. Test startup and shutdown under declared limits, exercise representative requests and jobs during version overlap, and verify database compatibility before switching traffic. Observe error rates, latency, queue age and worker heartbeats during rollout. Define what recovery restores and what irreversible effects need reconciliation.

## Current Assessment and Recommended Design

| Assessment | What it means here |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Current strengths | Separate API/worker configurations, proxy helpers and selective build logic make responsibilities explicit. |
| Current limitations | Disabled workflow triggers and startup-state canaries do not demonstrate active automated deployment or business readiness. |
| Recommended design | Build once, identify immutable artifacts, run migration compatibility checks, deploy through protected credentials, verify business readiness, and retain a tested rollback path that respects schema compatibility. |
| Evidence needed | The deployed digest matches the verified artifact; interrupted rollout preserves service; rollback works against the current schema; API and worker probes exercise distinct responsibilities. |

The recommended design is a proposal, not an implemented or production-verified claim. Apply it incrementally, beginning with a reproduced failure or explicit invariant; preserve working behavior and verify each migration boundary.

## Summary

Docita's source separates API, worker and SPA lifecycles and defines migration checks, blue-green API rollout and a worker canary protocol. The workflows are currently paused in code. Reliable releases require compatible contracts, meaningful health evidence and recovery beyond reverting an application image.

## See Also

- [Category revision](REVISION.md) — release and recovery questions after the cases.
- [Architecture decisions](01-architecture-decisions.md) — monorepo compatibility.
- [Async processing](03-async-processing.md) — worker ownership and recovery.
- [Documents and uploads](19-documents-and-uploads.md) — file-transfer boundaries.
- [Case-study index](INDEX.md) — reading stages.

## References

- [Fly autostop/autostart](https://docs.fly.io/launch/autostop-autostart).
- [Cloudflare Workers limits](https://developers.cloudflare.com/workers/platform/limits/).
- [Cloudflare Workers best practices](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/).

Docita source inspected on 2 October 2026:

- `fly.toml`, `apps/worker/fly.toml` and `apps/api/Dockerfile`
- `apps/app/api/index.ts` and `apps/app/wrangler.toml`
- `packages/utils/src/http/cloudflare-api-proxy.ts` and `upstream-api-proxy.ts`
- `.github/workflows/deploy.yml` and `.github/workflows/db-migrations.yml`
- `scripts/deploy/verify-db-schema-sync.sh` and `worker-canary-deploy.sh`
- `scripts/workflow/detect-workflow-deploy.mjs` and `detect-workflow-api-base.mjs`
