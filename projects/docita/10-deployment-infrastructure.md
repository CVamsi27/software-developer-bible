# 10 — Deployment & Infrastructure

> Production reliability at small-team scale — Fly.io, Cloudflare, migrations, and cold starts.

---

## Context

Docita runs on:

| Component | Technology | Why |
| ------------------ | ------------------------------------------------- | ------------------------------- |
| **API + Worker** | Fly.io (sin region) | Simple deployment, auto-scaling |
| **Frontend** | Cloudflare Workers (Static Assets) | Global CDN, zero server cost |
| **Proxy** | Cloudflare Hono Worker | SPA routing + API proxy |
| **Database** | AWS RDS PostgreSQL (ap-south-1) | Managed, HA, Indian region |
| **Object Storage** | Cloudflare R2 | S3-compatible, no egress fees |
| **External** | Razorpay, WhatsApp API, ZeptoMail, Sentry, OpenAI |  |

---

## Decision 1: Fly.io for API + Worker

### What We Chose

```text
fly.toml (API)                    fly.toml (Worker)
├── http_service                   ├── process = "worker"
├── min_machines_running = 1      ├── min_machines_running = 1
├── auto_stop_machines = true     ├── auto_stop_machines = false
└── auto_start_machines = true    └── memory = "2GB"
```

### Why Fly.io

| Factor | Fly.io | AWS ECS | Railway | Render |
| -------------------- | --------------- | ------------------- | --------- | -------- |
| **Setup complexity** | Low | High | Low | Low |
| **Cost (2GB RAM)** | ~$15/mo | ~$30/mo | ~$20/mo | ~$20/mo |
| **Indian region** | sin (Singapore) | ap-south-1 (Mumbai) | No | No |
| **Auto-scaling** | Yes | Yes | Yes | Yes |
| **Docker support** | Native | Native | Native | Native |

**Why not AWS ECS:** Higher operational complexity for a solo engineer. Fly.io's `fly deploy` is simpler than ECS task definitions, service discovery, and ALB configuration.

**Why not Railway/Render:** No Indian-region deployment. Latency matters for real-time clinic operations.

### The Cold Start Problem

**What happened:** Fly.io auto-stop shut down the VM after idle. Next request triggered a 3-minute NestJS bootstrap. Fly's HTTP proxy only waits ~10-15s → 502 Bad Gateway.

**Root cause:** Trusted platform defaults without measuring actual bootstrap time.

**Fix:** `min_machines_running = 1` — keep one machine always warm.

**Cost:** ~$7/mo extra for the always-on machine. Worth it for zero cold starts.

---

## Decision 2: Vite SPA + Cloudflare Workers

### What We Chose

```text
apps/app/ (Vite SPA)
├── React 19 + React Router v7
├── TanStack Query for data fetching
├── Tailwind CSS 4
└── Deployed to Cloudflare Workers (Static Assets)

apps/app/api/index.ts (Hono proxy)
├── /api/* → proxied to Fly.io API
└── SPA fallback for client-side routing
```

### Why Vite (Not Next.js)

| Factor | Vite SPA | Next.js SSR |
| ------------------------- | -------------------------- | -------------------------- |
| **Bundle size** | ~800KB gzip | ~3.5MB gzip |
| **Cloudflare Free limit** | ✅ Under 3MB | ❌ Over 3MB |
| **SEO** | Not needed (auth-gated) | Not needed (auth-gated) |
| **Dev experience** | Sub-second HMR | Fast, but slower than Vite |
| **Deployment** | Static assets, zero server | Requires server (OpenNext) |

**The tipping point:** Next.js 16 + OpenNext bundle was ~3.5 MB gzip, over Cloudflare's 3 MB Free limit. Every feature port increased bundle size with framework overhead rather than app code.

### Why Hono Proxy (Not Direct API Access)

**The problem:** SPA is on `docita.work`, API is on `api.fly.io`. Different domains = CORS + separate auth.

**The solution:** Hono proxy Worker on Cloudflare routes `/api/*` to Fly.io. Same domain, no CORS, same cookie scope.

```typescript
// apps/app/api/index.ts
const app = new Hono();
app.all('/api/*', async (c) => {
  return fetch(`https://api.fly.io${c.req.url}`, {
    method: c.req.method,
    headers: c.req.raw.headers,
    body: c.req.raw.body,
  });
});
```

---

## Decision 3: Database Migrations

### What We Chose

Prisma Migrate with a verification script:

```text
1. Developer runs `prisma migrate dev` locally
2. Migration file committed to git
3. Deploy: `prisma migrate deploy` runs before API starts
4. Verification script confirms no pending migrations
```

### Why Verification Script

**The problem:** A developer merges a migration but forgets to run `prisma migrate deploy` on the staging server. The API starts, tries to query a new column, and crashes.

**The solution:** The verification script checks that the latest migration has been applied. If not, the API refuses to start.

---

## Decision 4: Selective Deploys

### What We Chose

GitHub Actions triggers deploys only for changed apps:

```text
If apps/api/* changed → deploy API
If apps/app/* changed → deploy frontend
If packages/types/* changed → deploy all (shared types)
```

**Why selective:** Deploying the frontend when only the API changed (and vice versa) wastes time and introduces unnecessary risk.

---

## What Worked

- **Zero-downtime deployments** — Fly.io rolling deploys + Cloudflare instant propagation
- **Cold start fix** — `min_machines_running = 1` eliminated 502 errors
- **Selective deploys** — average deploy time reduced from 5 minutes to 2 minutes

## What Failed

- **Cloudflare 3MB limit** — discovered after building the Next.js app. Required emergency migration to Vite.

- **Fly.io region latency** — sin (Singapore) has ~50ms latency to Indian users. Not terrible, but not optimal. AWS ap-south-1 (Mumbai) would be better but Fly.io doesn't have a Mumbai region.

- **Migration drift** — a developer applied a migration locally but the production database was behind. The verification script caught it, but the deploy was blocked until manual intervention.

## What Could Be Better

- **Blue-green deployments** — currently rolling deploys. Blue-green would allow instant rollback.

- **Canary deployments** — deploy to 10% of traffic first, monitor for errors, then full rollout.

- **Infrastructure as Code** — Fly.io config is in `fly.toml`. Terraform would provide better reproducibility and drift detection.

- **APM integration** — currently using Sentry for errors. Adding APM (e.g., Fly.io metrics, Datadog) would improve performance visibility.

---

## Code Evidence

| Claim | File |
| ------------------- | -------------------------------- |
| Fly.io config | `fly.toml` |
| Dockerfile | `apps/api/Dockerfile` |
| Hono proxy | `apps/app/api/index.ts` |
| GitHub Actions | `.github/workflows/` |
| Prisma migrations | `packages/db/prisma/migrations/` |
| Verification script | `scripts/verify-migrations.mjs` |

---

## Interview Script (60 seconds)

> "Docita deploys on Fly.io for the API/worker and Cloudflare Workers for the frontend. The API uses Docker with a multi-stage build. Frontend is a Vite SPA deployed as Cloudflare Static Assets — we migrated from Next.js because the 3.5MB bundle exceeded Cloudflare's 3MB Free limit. A Hono proxy Worker routes `/api/*` to Fly.io, avoiding CORS. We hit a cold-start outage because Fly's proxy only waits ~10-15s but NestJS bootstrap takes ~3 minutes. Fix: `min_machines_running = 1`. Database migrations use Prisma Migrate with a verification script that blocks deploys if migrations are pending. Selective deploys via GitHub Actions — only changed apps are deployed."
---

[← Previous: Subscription System](09-subscription-system.md) · [ Back to Index](INDEX.md) · [Next: Insurance Claims →](11-insurance-claims.md)
