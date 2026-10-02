# Serverless & Edge — Index

> **Study time:** ≈ 1 h 45 m of reading (11 files, ~10 min average).
> **11 files** — Serverless and edge computing fundamentals, from overview and edge functions to AWS Lambda, Vercel, serverless patterns, IaC frameworks, durable execution, Fly.io deployment, Vite SPA on Cloudflare, and curated interview questions.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-informational)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why serverless:** Many mid-stage startups and most AWS deployments use Lambda, Step Functions, or event-driven architectures. Edge functions (Cloudflare Workers, Vercel Edge) are increasingly common for low-latency APIs. Senior interviews test when to use serverless vs containers vs VMs — and the cold start / cost / state trade-offs.

---

## Topic Categories

| Category | Files | Why it matters |
| --------------------------------- | ----: | -------------------------------------------------------------------- |
| [Concepts](#concepts) | 2 | Overview, edge functions — the mental model |
| [Providers](#providers) | 2 | AWS Lambda, Vercel — the main platforms |
| [Patterns & IaC](#patterns--iac) | 3 | Serverless patterns, IaC frameworks (SAM/CDK/SST), durable execution |
| [Deployment](#deployment) | 2 | Fly.io containers, Vite SPA on Cloudflare |
| [Interview Prep](#interview-prep) | 1 | 30+ Qs |

---

## Concepts

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [Serverless Overview](40.7.01-serverless-overview.md) | FaaS model, cold starts, FaaS vs containers vs VMs, providers (AWS Lambda, Azure Functions, GCP Cloud Functions) | 10 min |
| 02 | [Edge Functions](40.7.04-edge-functions.md) | Edge runtimes (Cloudflare Workers, Vercel Edge, Lambda@Edge), V8 isolates, state storage | 12 min |

**Decision tree:**

```text
Deploy choice?
├── Bursty / event-driven / pay-per-use? ──→ Serverless (Lambda, Cloud Functions)
├── Low-latency global API? ──→ Edge functions (Cloudflare Workers)
├── Long-running / stateful? ──→ Containers (ECS, K8s)
└── Predictable high load? ──→ VMs or containers (cheaper at scale)
```

---

## Providers

| # | File | Topics | When to use | Read time |
| --: | ------ | -------- | ------------- | ----------: |
| 03 | [AWS Lambda](40.7.02-aws-lambda.md) | Event sources, cold starts, SnapStart, Provisioned Concurrency, Lambda@Edge | AWS-heavy stacks | 9 min |
| 04 | [Vercel Deployments](40.7.03-vercel-deployments.md) | Edge runtime, Edge Middleware, ISR, preview deploys, Fluid Compute | Next.js apps | 10 min |

---

## Patterns & IaC

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 05 | [Serverless Patterns](40.7.05-serverless-patterns.md) | API patterns, event-driven, orchestration (Step Functions), Saga, CQRS | 13 min |
| 06 | [Serverless Frameworks](40.7.06-serverless-frameworks.md) | SAM, CDK, Serverless Framework, SST — IaC for serverless | 11 min |
| 07 | [Durable Execution: Temporal & Inngest](40.7.07-durable-execution-temporal-inngest.md) | Event-sourced replay, workflow/activity split, determinism rules, signals/queries, Inngest steps, retries/timeouts, Step Functions vs code-first trade-offs | 13 min |

---

## Deployment

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 09 | [Fly.io Deployment](40.7.09-flyio-deployment.md) | Container deployment, auto-stop/start, health checks, multi-region, Docker multi-stage builds | 9 min |
| 10 | [Vite SPA on Cloudflare Workers](40.7.10-vite-spa-cloudflare-workers.md) | Static Assets, Hono proxy, SPA fallback, bundle size limits, same-domain API proxying | 9 min |

---

## Interview Prep

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 11 | [Interview Questions](40.7.08-interview-questions.md) | 30+ curated questions from beginner to FAANG-style | 7 min |

---

## Suggested Study Order

1. **Serverless Overview** — must know the trade-offs
2. **Edge Functions** — for modern web apps
3. **AWS Lambda** or **Vercel Deployments** — for the JD's stack
4. **Serverless Patterns** — for senior roles
5. **Serverless Frameworks** — for IaC-heavy roles
6. **Durable Execution** — for orchestration/stateful-flow questions
7. **Fly.io / Vite SPA on Cloudflare** — deployment for your stack
8. **Interview Questions** — final review

---

## Common interview topics

- "When to use Lambda vs ECS vs K8s?"
- "What is a cold start? How do you mitigate it?"
- "Edge functions vs Lambda — when to use which?"
- "How do you handle state in serverless?"
- "What is the Saga pattern? How does it relate to Step Functions?"
- "How would you run a multi-day approval workflow on serverless?" (durable execution)

---

## Cross-References

- [CI/CD](../40.3-ci-cd/INDEX.md) — deploying serverless
- [Docker](../40.1-docker/INDEX.md) — containers vs serverless trade-offs
- [Next.js (Edge Middleware)](../../10-frontend/10.4-next.js/INDEX.md) — Vercel Edge
- [Observability](../40.4-observability/INDEX.md) — distributed tracing for serverless
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — Saga, CQRS in serverless

---

## Navigation

[← Previous: Git Advanced](../40.6-git-advanced/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Monorepo →](../40.8-monorepo/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets serverless — the honest answer is **split**:

| Topic | Docita evidence |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Serverless: YES (landing/edge) | `apps/landing` is Astro deployed to Cloudflare Workers — `deploy:cloudflare` runs `wrangler deploy` with a `_worker.js` entry; `@astrojs/cloudflare` adapter |
| Serverless: NO (core API, deliberately) | The NestJS API and worker are long-running Fly.io machines; ADR 0011 chose suspend/resume (`auto_stop_machines='suspend'`) over scale-to-zero functions for cold-start control |
| Edge caching | Cloudflare in front of the API with origin protection (ADR 0014); `DOCITA_CLOUDFLARE` build flag switches landing to CF mode |
| Durable Objects / edge compute in the hot path | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
