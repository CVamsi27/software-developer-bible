# Releases & Metrics

> **1 file.** Shipping safely: blue-green and canary deployments for zero-downtime releases with instant rollback.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Releases-green)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-in--progress-yellow)](#)

---

## Why this category exists

Rolling updates are the default but not always enough: big-bang rollouts carry all-or-nothing risk, and "deploy = release" couples shipping code to exposing it to users. Blue-green gives instant rollback; canary gives graduated risk reduction backed by metrics. Senior interviews treat these as the minimum bar for "how do you deploy?" answers.

---

## File Index

| Order | File | Topics | Read time |
|--:|------|--------|----------:|
| 01 | [Blue-Green & Canary](40.3.3.01-blue-green-canary.md) | Blue-green swaps, canary traffic shifting, automated rollback on metrics, feature flags as decoupling | 25 min |

*Slot reserved: `40.3.3.02` DORA metrics & delivery performance (upcoming chapter — no link yet).*

---

## Cross-References

- [Build & Deploy](../02-build-and-deploy/INDEX.md) — pipelines that execute these releases
- [Observability Stack](../../../40-platform/40.4-observability/INDEX.md) — the metrics canary decisions depend on

---

## Navigation

[← Build & Deploy](../02-build-and-deploy/INDEX.md) · [↑ CI/CD Home](../INDEX.md) · [Next: Interview Prep →](../04-interview-prep/INDEX.md)
