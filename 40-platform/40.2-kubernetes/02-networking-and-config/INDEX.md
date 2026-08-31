# Networking & Config

> **3 files.** How traffic gets in and how configuration gets in: Services and Ingress for traffic, ConfigMaps and Secrets for configuration, PodPresets for admission-time injection.

[![Files](https://img.shields.io/badge/files-3-blue)](#file-index)
[![Category](https://img.shields.io/badge/category-Networking%20%26%20Config-blue)](../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## Why this category exists

A pod without a Service is unreachable; a Deployment without ConfigMaps/Secrets has baked-in config and fails twelve-factor review. These three chapters cover the plumbing every real deployment needs: stable virtual IPs and load balancing, external entry with TLS, environment-specific configuration, and automatic injection of common config at admission time.

---

## File Index

| Order | File                                                    | Topics                                                                                                 | Read time |
| --   :  | ------                                                    | --------                                                                                                 | ----------: |
| 01    | [Services & Ingress](40.2.2.01-services-ingress.md)     | ClusterIP, NodePort, LoadBalancer, kube-proxy, Ingress controllers, TLS termination, host/path routing | 30 min    |
| 02    | [ConfigMaps & Secrets](40.2.2.02-configmaps-secrets.md) | ConfigMaps, Secrets, mounting vs env vars, encryption at rest, rolling config changes                  | 25 min    |
| 03    | [PodPresets](40.2.2.03-podpresets.md)                   | Admission-time injection of env vars, volumes, secrets; label selectors; Kyverno alternatives          | 15 min    |

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

| Topic                            | Docita evidence                                                                                          |
| -------                            | -----------------                                                                                          |
| Ingress & TLS termination        | Cloudflare edge (origin protection, ADR 0014) → Fly `http_service` with `force_https = true`             |
| ConfigMap-like env config        | `fly.toml [env]` block + turbo `globalEnv` allowlist, validated by `shared/modules/config/env-schema.ts` |
| Secrets handling                 | Never in-repo; runtime env only (`RAZORPAY_KEY_SECRET`, DB URLs appear solely as env references)         |
| PodPresets / admission injection | _No direct docita implementation yet._                                                                   |
