# 10 — Deployment: Keep Versions, Schema and Background Work Compatible

## Definition

Deployment changes running application versions and their configuration. In Docita, the API and worker run as separate Fly applications, while the React SPA and API proxy use Cloudflare Workers with static assets.

Consider a release that adds an invoice field and changes a PDF job payload. A successful build is only the start: old API instances, new workers, existing jobs and the database can overlap during rollout. The release must preserve their contracts and provide evidence that the new version works.

This case describes checked-in source inspected on **2 October 2026**. Configuration and workflow code do not establish current deployed settings or successful production releases.

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

This is a **deployment verification step**, not evidence that every application startup refuses to run with pending migrations. No production database was contacted during this documentation review.

A compatible sequence is:

1. Add schema support that existing code can tolerate.
2. Deploy code able to handle the transition and existing data.
3. Backfill or transform data with observable progress and recovery.
4. Remove obsolete fields or behavior only after old consumers are retired.

Applying a migration before new code is insufficient if it breaks old instances. Likewise, rolling back an image does not undo data changes or external effects. Document destructive steps and recovery separately from process rollback.

## What the Deployment Workflow Currently Enables

The checked-in production deploy and database-migration workflows have their `on:` triggers commented out. They therefore describe a **paused configuration**, not an active automatic deployment pipeline. Comments also mention GitHub-level disabling, but that external setting was not checked here.

Within the configured jobs, change detection maps source paths to affected deploy targets, including shared packages and root build/configuration files. API and worker deployment depend on successful migration verification. The API additionally has a startup smoke gate and is configured for **blue-green** deployment.

The worker script performs a canary deployment, checks that the selected machine remains `started` for a settling window—**90 seconds** in the workflow—then promotes through a rolling deployment. Machine state is a process-liveness signal; it does not prove that jobs, tenant isolation or external effects are correct. The script itself distinguishes this from live worker health and scheduler heartbeat evidence.

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
