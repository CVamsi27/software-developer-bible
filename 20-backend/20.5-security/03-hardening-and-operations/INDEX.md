# Hardening & Operations - Security

> **Study time:** ≈ 46 min of reading (6 files, ~8 min average).
> **6 files.** Production hygiene: the encryption/hashing/TLS primer (prerequisite for the auth track), security headers and CSP, STRIDE threat modeling, secrets management, and vulnerability management & patch governance.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Hardening%20%26%20Operations-blue)](../INDEX.md)

---

## Learning flow

Start with confidentiality, integrity and key roles. Then trace one browser response policy, model the trust boundaries those controls protect, and follow credential rotation through consumers. Finish with finding triage and verified remediation; use [revision](REVISION.md) before the [interview bank](../04-interview-drills/20.5.4.01-interview-questions.md).

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Encryption, Hashing & TLS](20.5.3.01-encryption.md) | Symmetric/asymmetric, salting, AES/RSA, TLS handshake *(prerequisite for the auth track)* | Essential | Foundational | 7 min |
| 02 | [Web Security](20.5.3.02-web-security.md) | HTTPS/HSTS, CSP nonce policy, CORS, framing, redirects, SSRF and XXE boundaries | Essential | Foundational | 8 min |
| 03 | [Threat Modeling — STRIDE](20.5.3.03-threat-modeling-stride.md) | STRIDE, data-flow diagrams, trust boundaries, attack trees | Important | Specialized | 7 min |
| 04 | [Secrets Management](20.5.3.04-secrets-management.md) | Vault, AWS/GCP secret managers, rotation, KMS, dynamic credentials | Essential | Foundational | 8 min |
| 05 | [Vulnerability Management & Patch Governance](20.5.3.05-vulnerability-management-patch-governance.md) | CVE/CVSS triage + EPSS/KEV, SBOM (CycloneDX/SPDX), npm audit/pip-audit/Snyk/Trivy roles, patch SLAs by severity, emergency patch process, base-image refresh, risk acceptance register, MTTR metrics | Important | Specialized | 12 min |

---

[← Back to Security](../INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) source paths are inspection starting points. They do not by themselves establish deployment coverage or operating effectiveness:

| Topic | Docita evidence |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Encryption at rest | `apps/api/src/shared/common/encryption.service.ts` - AES-256-GCM with versioned keys, fail-fast if ENCRYPTION_KEY missing |
| Field-level boundaries | `apps/api/src/shared/common/encryption-patient-fields.boundary.ts` - explicit allow-list of encrypted patient fields |
| Secrets validation | `apps/api/src/shared/modules/config/env-schema.ts` - Zod schema rejects boot without required secrets |
| Log / telemetry scrubbing | `apps/api/src/shared/modules/observability/phi-redactor.ts` - PHI redaction for pino lines + Sentry beforeSend |
| Vulnerability management tooling | `osv-scanner.toml` - dependency scanning config beside CI guardrail scripts (`scripts/checks/*.mjs`) |
| Threat modeling | `docs/operations/SECURITY_HARDENING_CHECKLIST.md` §3 (2026-08-05 point-in-time threat table), `docs/compliance/ACCESS_AUDIT.md` and `docs/compliance/RLS_ROLLOUT.md` (authorization and tenant boundaries) |

The checklist is a point-in-time threat table, not a dedicated STRIDE or data-flow diagram (DFD) model; no dedicated STRIDE/DFD artifact was found in the reviewed Docita checkout. Its access and row-level security (RLS) documents describe tenant enforcement across role-based access control (RBAC), tier and tenant guards, context-aware attribute-based access control (ABAC), a Prisma tenant extension and PostgreSQL RLS. Use those documents to inspect control order and limits. Source paths and documents are inspection leads; they do not prove that a control is deployed or operating effectively.
---

[← Previous: Attacks & Defense](../02-attacks-and-defense/INDEX.md) · [Next: Interview Drills →](../04-interview-drills/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
