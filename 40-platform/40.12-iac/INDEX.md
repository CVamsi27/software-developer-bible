# IaC & Terraform — Index

> **Study time:** ≈ 16 min of reading (3 files, ~5 min average).
> **1 teaching chapter** — Follow a resource from configuration through state, planning, apply, and verification. Then use the revision companion and interview bank to test identity, failure recovery, and access boundaries.

[![Files](https://img.shields.io/badge/files-3-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Platform-blue)](#)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this sub-stack exists

Every other sub-stack in Platform assumes infrastructure *exists*. This one answers: **how does that infrastructure get created, versioned, and changed safely?** Even full-stack roles now expect you to read and reason about a `terraform plan` diff — IaC is how modern teams deploy everything from this bible's own CI patterns to the [Docita](../40.7-serverless-edge/40.7.05-serverless-patterns.md) Fly.io + Cloudflare setup.

## Learning flow (passes)

**Pass 1 — Trace a change (15 min):** Read [the chapter](40.12.01-iac-fundamentals-terraform.md) and follow one resource from address to remote identifier, through planning, and into verification. Explain what configuration, state, and provider observation each tell you.

**Pass 2 — Safe local experiment (15 min):** Run the isolated `terraform_data` example in a temporary directory. Change its input, inspect the plan, apply the saved plan, and confirm the next plan is empty. Then rename its address and explain why a `moved` block changes the identity interpretation.

**Pass 3 — Retrieve and practice:** Close the chapter and complete [section revision](REVISION.md), then use [the interview bank](40.12.02-interview-questions.md). Focus on partial apply, stale plans, brownfield adoption, and how state boundaries relate to access control.

---

## The Files

| # | File | Topics | Role priority | General importance | Read time |
| --: | ------ | -------- | --- | --- | ----------: |
| 01 | [40.12.01-iac-fundamentals-terraform.md](40.12.01-iac-fundamentals-terraform.md) | Configuration, addresses and state, dependency graph, plan/apply, saved artifacts, partial failure, locking, environment boundaries, secrets, modules and tool lifecycle | Optional | Specialized | 9 min |
| — | [Revision questions](REVISION.md) | Recall checks for identity, stale plans, locking, secrets, imports, and post-apply verification | Optional | Specialized | 2 min |
| 02 | [40.12.02-interview-questions.md](40.12.02-interview-questions.md) | Applied scenarios for drift, adoption, CI safety, module contracts, workspaces, state migration, and recovery | Optional | Specialized | 5 min |

---

## Quick Reference

| Concept | One-liner |
| ---------- | -------------------------------------------------------------------------------------------------------- |
| IaC | Versioned definitions for creating and changing infrastructure |
| State | Address-to-remote-object mapping; it can lag behind reality |
| Drift | Provider-readable difference between configuration, state, and remote attributes |
| Plan | Proposed actions based on configuration, state, and provider reads |
| Apply | Executes a new approved plan or the exact supplied saved plan |
| Backend | State storage; locking and access controls depend on backend configuration |
| Module | Reusable resources with declared inputs and outputs |
| Brownfield | Import a remote ID, match configuration, review the changes |

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

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
