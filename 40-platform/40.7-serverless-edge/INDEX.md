# Serverless & Edge — Index

> **Study time:** ≈ 1 h 26 m of reading (11 files, ~8 min average).
> **11 files** — Serverless and edge computing fundamentals, from overview and edge functions to AWS Lambda, Vercel, serverless patterns, IaC frameworks, durable execution, Fly.io deployment, Vite SPA on Cloudflare, and curated interview questions.

[![Files](https://img.shields.io/badge/files-11-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-DevOps-informational)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

**Why serverless:** Managed functions, containers and edge services make different promises about lifetime, placement and recovery. Senior interviews test when to use serverless vs containers vs VMs — and the cold start / cost / state trade-offs.

---

## Topic Categories

| Category | Files | Why it matters |
| --------------------------------- | ----: | -------------------------------------------------------------------- |
| [Concepts](#concepts) | 2 | Overview, edge functions — the mental model |
| [Providers](#providers) | 2 | AWS Lambda, Vercel — the main platforms |
| [Patterns & IaC](#patterns--iac) | 3 | Serverless patterns, IaC frameworks (SAM/CDK/SST), durable execution |
| [Deployment](#deployment) | 2 | Fly.io containers, Vite SPA on Cloudflare |
| [Interview Prep](#interview-prep) | 1 | 32 source-linked prompts |

---

## Concepts

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [Serverless Overview](40.7.01-serverless-overview.md) | Request and event model, execution lifetime, retries, durable state, downstream capacity, cost, and runtime choice | Important | Specialized | 8 min |
| 02 | [Edge Functions](40.7.04-edge-functions.md) | Provider contracts, runtime limits, cache and KV consistency, Durable Object coordination, identity, and recovery | Important | Specialized | 8 min |

**Decision tree:**

```text
Deploy choice?
├── Bursty / event-driven / pay-per-use? ──→ Serverless (Lambda, Cloud Functions)
├── Can useful work finish near ingress? ──→ Evaluate edge placement and data authority
├── Long-running / stateful? ──→ Containers (ECS, K8s)
└── Predictable high load? ──→ Compare measured total provisioned/function costs
```

---

## Providers

| # | File | Topics | When to use | Role priority | General importance | Read time |
| --: | ------ | -------- | ------------- | --- | --- | ----------: |
| 03 | [AWS Lambda](40.7.02-aws-lambda.md) | Default environments, Managed Instances, Durable Functions, event-source retries, concurrency, SnapStart, aliases | AWS-heavy stacks | Important | Specialized | 10 min |
| 04 | [Vercel Deployments](40.7.03-vercel-deployments.md) | Deployment identity, preview isolation, runtime placement, caching, cron recovery, promotion and rollback | Next.js apps | Important | Specialized | 8 min |

---

## Patterns & IaC

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 05 | [Serverless Patterns](40.7.05-serverless-patterns.md) | Transactional outbox, business idempotency, SQS partial batches, publication acknowledgments, workflow guarantees, CQRS, and fan-in | Important | Specialized | 9 min |
| 06 | [Serverless Frameworks](40.7.06-serverless-frameworks.md) | SAM transforms, CDK synthesis/bootstrap, SST resource links, Serverless Framework v4, artifact and permission review | Important | Specialized | 8 min |
| 07 | [Durable Execution: Temporal & Inngest](40.7.07-durable-execution-temporal-inngest.md) | Replay and step history, signals and durable waits, activity retries, idempotency, code-version safety, Step Functions guarantees, and recovery tests | Important | Specialized | 9 min |

---

## Deployment

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 09 | [Fly.io Deployment](40.7.09-flyio-deployment.md) | Container deployment, auto-stop/start, health checks, multi-region, Docker multi-stage builds | Important | Specialized | 6 min |
| 10 | [Vite SPA on Cloudflare Workers](40.7.10-vite-spa-cloudflare-workers.md) | Static Assets, Hono proxy, SPA fallback, bundle size limits, same-domain API proxying | Important | Specialized | 9 min |

---

## Interview Prep

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 11 | [Interview Questions](40.7.08-interview-questions.md) | 32 preserved source-linked prompts | Important | Specialized | 5 min |

---

## Suggested Study Order

1. **Serverless Overview** — must know the trade-offs
2. **Edge Functions** — for modern web apps
3. **AWS Lambda** or **Vercel Deployments** — for the JD's stack
4. **Serverless Patterns** — for senior roles
5. **Serverless Frameworks** — for IaC-heavy roles
6. **Durable Execution** — for orchestration/stateful-flow questions
7. **Fly.io / Vite SPA on Cloudflare** — deployment for your stack
8. **[Section revision](REVISION.md)** — explain the mechanisms without copying
9. **Interview Questions** — choose a policy and trace one failure

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
- [Next.js deployment contracts](../../10-frontend/10.4-next.js/INDEX.md) — framework/runtime compatibility
- [Observability](../40.4-observability/INDEX.md) — distributed tracing for serverless
- [Microservices](../../20-backend/20.6-microservices/INDEX.md) — Saga, CQRS in serverless

---

## Navigation

[← Previous: Git Advanced](../40.6-git-advanced/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Monorepo →](../40.8-monorepo/INDEX.md)

---

## Docita Anchor

Source walkthrough for [Docita](../../projects/docita/INDEX.md), checked on 10 October 2026. Inspect the current source and actual release evidence separately; configuration/ADR intent does not prove a deployed path.

| Topic | Source to inspect | Boundary |
| ------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Landing output | Astro/Cloudflare adapter, build scripts and Wrangler config | Verify current emitted entry/assets and deployed routing |
| API/worker process | Fly config and suspend/resume ADR | Existing Machine lifecycle differs from invocation-based functions |
| Origin protection | Cloudflare-origin ADR and ingress checks | Verify the deployed trust path; an ADR alone is not enforcement |
| Deployment workflow | CI workflow triggers and deployment steps | Current source has commented deployment triggers; do not infer automatic live promotion |
| Durable Objects | No direct implementation claimed | Teaching examples are independent fixtures |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
