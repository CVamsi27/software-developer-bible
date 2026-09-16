# Interview Prep — Kubernetes

> **Study time:** ≈ 15 min of reading (1 files, ~15 min average).
> **1 file, 50+ curated questions with answers.** The drill that converts K8s knowledge into interview performance.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview%20Prep-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## What's here

A question bank spanning everything in this stack: workload semantics, networking, config, scaling, hardening, and packaging.

- **Easy** — pod vs container, Service types, ConfigMap vs Secret
- **Medium** — rolling update mechanics, HPA metrics pipeline, probe tuning, PDB behavior during drains
- **Hard** — RBAC design for multi-tenancy, StatefulSet rollout ordering, quota enforcement edge cases

---

## File Index

### [Kubernetes Interview Questions](40.2.6.01-interview-questions.md)

50+ curated questions with answers, organized by difficulty. Work them only after reading the five content categories — the answers assume the vocabulary.

---

## Navigation

[← Packaging & Extensibility](../05-packaging-and-extensibility/INDEX.md) · [↑ Kubernetes Home](../INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet._ Docita runs on Fly.io, so K8s answers here can't cite production war stories from it. The honest interview move: use docita's Fly.io mechanics as working analogs — health-gated deploys ≈ readiness gating, suspend-to-zero + scheduled scaling ≈ HPA outcomes, RLS + ABAC ≈ namespace/quota isolation — and say plainly that the cluster experience is theoretical.
