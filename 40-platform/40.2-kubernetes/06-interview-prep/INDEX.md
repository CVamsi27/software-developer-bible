# Interview Prep — Kubernetes

> **Study time:** ≈ 21 min of reading (1 file, ~21 min average).
> **1 file, A curated question bank with answers.** The drill that converts K8s knowledge into interview performance.

[![Files](https://img.shields.io/badge/files-1-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Interview%20Prep-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## How to use this bank

The 30 questions cover workloads, networking, configuration, scaling, reliability, security, packaging and delivery. Answer aloud before reading each explanation. State assumptions, trace the mechanism, then name a failure mode and a verification step. Use the linked chapter when an answer depends on a specific API or controller behavior.

---

## File Index

### [Kubernetes Interview Questions](40.2.6.01-interview-questions.md)

Thirty questions with explanations and source links. Attempt them after the five learning categories; the answers assume their vocabulary.

---

## Navigation

[← Packaging & Extensibility](../05-packaging-and-extensibility/INDEX.md) · [↑ Kubernetes Home](../INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet._ Docita runs on Fly.io, so K8s answers here can't cite production war stories from it. The honest interview move: use docita's Fly.io mechanics as working analogs — health-gated deploys ≈ readiness gating, suspend-to-zero + scheduled scaling ≈ HPA outcomes, RLS + ABAC as application data/access controls, separate from cluster admission and network policy — and say plainly that the cluster experience is theoretical.
