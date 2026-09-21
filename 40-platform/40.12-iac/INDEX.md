# IaC & Terraform — Index

> **Study time:** ≈ 16 min of reading (2 files, ~8 min average).
> **Infrastructure as Code fundamentals, Terraform state/plan/apply, modules, drift, backends, CI/CD safety, OpenTofu/Pulumi comparisons.**

[![Files](https://img.shields.io/badge/files-2-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this sub-stack exists

Every other sub-stack in Platform assumes infrastructure *exists*. This one answers: **how does that infrastructure get created, versioned, and changed safely?** Even full-stack roles now expect you to read and reason about a `terraform plan` diff — IaC is how modern teams deploy everything from this bible's own CI patterns to the [Docita](../40.7-serverless-edge/40.7.05-serverless-patterns.md) Fly.io + Cloudflare setup.

## Learning flow (passes)

**Pass 1 — The model (30 min):** Read [40.12.01-iac-fundamentals-terraform.md](40.12.01-iac-fundamentals-terraform.md) TL;DR → How It Works. You must be able to explain *state, drift, plan/apply, declarative vs imperative* in one sentence each.

**Pass 2 — Hands-on mental reps (30 min):** Trace the command lifecycle (`init → validate → plan → apply`) and the CI/CD workflow. Explain to yourself what happens when two engineers run `apply` without locking.

**Pass 3 — Interviews (30 min):** Work [40.12.02-interview-questions.md](40.12.02-interview-questions.md). The three that recur: state & drift, brownfield adoption (`import`), and IaC in CI.

**Recap:** Re-read Mistakes + Cheat Sheet before any platform interview.

---

## The Files

| # | File | Topics | Read time |
| --: | ------ | -------- | ----------: |
| 01 | [40.12.01-iac-fundamentals-terraform.md](40.12.01-iac-fundamentals-terraform.md) | IaC model, HCL, state & drift, plan/apply, providers, backends, modules, workspaces, OpenTofu/Pulumi/CDKTF, mistakes, best practices | 8 min |
| 02 | [40.12.02-interview-questions.md](40.12.02-interview-questions.md) | 11 Q&A: state, drift, declarative vs imperative, brownfield import, environments, modules, GitOps, CI safety, tool comparison + behavioral story | 8 min |

---

## Quick Reference

| Concept | One-liner |
| ---------- | ------------------------------------------------------------ |
| IaC | Infrastructure declared as reviewable, versioned code |
| State | Terraform's record of what exists — needed to compute a diff |
| Drift | Config vs reality mismatch; `plan` reveals it |
| Plan | Read-only diff — the review artifact |
| Apply | The only mutating step |
| Backend | Where state lives (remote + lock = non-negotiable) |
| Module | Reusable, parameterized infra function |
| Brownfield | `import` existing resources — never recreate |

---

## Cross-References

- [Kubernetes](../40.2-kubernetes/INDEX.md) — declarative infra inside the cluster
- [CI/CD](../40.3-ci-cd/INDEX.md) — pipelines that run plan/apply; ArgoCD GitOps
- [Serverless & Edge](../40.7-serverless-edge/INDEX.md) — SAM/CDK (AWS IaC) and Cloudflare Workers
- [Git Advanced](../40.6-git-advanced/INDEX.md) — versioning discipline IaC relies on

---

## Docita Anchor

Docita runs on Fly.io + Cloudflare with GitHub Actions deploys — no Terraform in production today (see the [Docita Anchor note](../INDEX.md#docita-anchor) in the Platform INDEX). Interview framing: *\"the infra is small enough that Fly CLI + Cloudflare dashboard + Actions is honest; the IaC pattern (state, plan/apply, drift) is exactly what I'd adopt the day the environment count or team size grows — the knowledge is in this sub-stack, the discipline is documented in 40.3.\"* Marked `_No direct docita implementation yet._` rather than faked.
---

[← Previous: Reverse Proxy](../40.11-reverse-proxy/INDEX.md) · [Next: Kubernetes →](../40.2-kubernetes/INDEX.md)
