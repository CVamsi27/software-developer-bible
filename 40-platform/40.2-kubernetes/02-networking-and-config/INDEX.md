# Networking & Config

> **Study time:** ≈ 25 min of reading (4 files, ~6 min average).
> **4 files.** How traffic gets in and how configuration gets in: Services and Ingress for traffic, ConfigMaps and Secrets for configuration, the historical PodPreset API and supported injection ownership.

[![Files](https://img.shields.io/badge/files-4-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Networking%20%26%20Config-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

A Pod can be reached directly when routing allows, but its address is not a durable application entry point. Services stabilize discovery; ingress or Gateway implementations publish HTTP routes; ConfigMaps and Secrets supply runtime inputs. PodPresets are historical: that API was removed in Kubernetes 1.20.

## Reading Passes

1. **Trace traffic:** follow DNS, controller routing, Service ports and ready endpoints in [Services & Ingress](40.2.2.01-services-ingress.md). Separate the Ingress API from the retired ingress-nginx controller.
2. **Trace configuration:** compare mounted data and environment injection in [ConfigMaps & Secrets](40.2.2.02-configmaps-secrets.md), including reload and access boundaries.
3. **Replace historical injection:** read [PodPresets](40.2.2.03-podpresets.md) for the removed API's role, then choose supported templates or deliberate admission policies. Complete [revision](REVISION.md) afterward.

---

## File Index

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Services & Ingress](40.2.2.01-services-ingress.md) | ClusterIP, NodePort, LoadBalancer, kube-proxy, Ingress controllers, TLS termination, host/path routing | Optional | Specialized | 8 min |
| 02 | [ConfigMaps & Secrets](40.2.2.02-configmaps-secrets.md) | ConfigMaps, Secrets, mounting vs env vars, encryption at rest, rolling config changes | Optional | Specialized | 10 min |
| 03 | [PodPresets](40.2.2.03-podpresets.md) | Removed API history; supported templates, Helm/Kustomize and admission alternatives | Optional | Specialized | 5 min |

---

## Cross-References

- [Core Workloads](../01-core-workloads/INDEX.md) — the workloads this config attaches to
- [Production Hardening](../04-production-hardening/INDEX.md) — NetworkPolicies and RBAC restrict what networking allows

---

## Navigation

[← Core Workloads](../01-core-workloads/INDEX.md) · [↑ Kubernetes Home](../INDEX.md) · [Next: Scaling →](../03-scaling/INDEX.md)

---

## Docita Anchor

Where [docita](https://github.com/CVamsi27/docita) meets this topic.

_No direct docita implementation yet_ — no Services/Ingress/ConfigMaps; a Fly router + Cloudflare play those roles:

| Topic | Docita evidence |
| -------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Ingress & TLS termination | Cloudflare edge (origin protection, ADR 0014) → Fly `http_service` with `force_https = true` |
| ConfigMap-like env config | `fly.toml [env]` block + turbo `globalEnv` allowlist, validated by `shared/modules/config/env-schema.ts` |
| Secrets handling | Never in-repo; runtime env only (`RAZORPAY_KEY_SECRET`, DB URLs appear solely as env references) |
| PodPresets / admission injection | _No direct docita implementation yet._ |

## Finish This Section

After the reading pass, complete the [section revision questions](REVISION.md) in a separate session. Revisit only the source chapters whose mechanisms you cannot yet explain or reproduce.
