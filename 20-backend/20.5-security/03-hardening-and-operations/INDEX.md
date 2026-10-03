# Hardening & Operations - Security

> **Study time:** ≈ 1 h 7 m of reading (6 files, ~11 min average).
> **6 files.** Production hygiene: the encryption/hashing/TLS primer (prerequisite for the auth track), security headers and CSP, STRIDE threat modeling, secrets management, and vulnerability management & patch governance.

[![Files](https://img.shields.io/badge/files-6-blue)](../INDEX.md)
[![Category](https://img.shields.io/badge/category-Hardening%20%26%20Operations-blue)](../INDEX.md)

---

## Files

| Order | File | Topics | Role priority | General importance | Read time |
| --   : | ------ | -------- | --- | --- | ----------: |
| 01 | [Encryption, Hashing & TLS](20.5.3.01-encryption.md) | Symmetric/asymmetric, salting, AES/RSA, TLS handshake *(prerequisite for the auth track)* | Essential | Foundational | 14 min |
| 02 | [Web Security](20.5.3.02-web-security.md) | HTTPS, HSTS, CORS, CSP, security headers, OWASP Top 10 | Essential | Foundational | 19 min |
| 03 | [Threat Modeling — STRIDE](20.5.3.03-threat-modeling-stride.md) | STRIDE, data-flow diagrams, trust boundaries, attack trees | Important | Specialized | 9 min |
| 04 | [Secrets Management](20.5.3.04-secrets-management.md) | Vault, AWS/GCP secret managers, rotation, KMS, dynamic credentials | Essential | Foundational | 11 min |
| 05 | [Vulnerability Management & Patch Governance](20.5.3.05-vulnerability-management-patch-governance.md) | CVE/CVSS triage + EPSS/KEV, SBOM (CycloneDX/SPDX), npm audit/pip-audit/Snyk/Trivy roles, patch SLAs by severity, emergency patch process, base-image refresh, risk acceptance register, MTTR metrics | Important | Specialized | 11 min |

---

[← Back to Security](../INDEX.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the chapters, then see it shipped:

| Topic | Docita evidence |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Encryption at rest | `apps/api/src/shared/common/encryption.service.ts` - AES-256-GCM with versioned keys, fail-fast if ENCRYPTION_KEY missing |
| Field-level boundaries | `apps/api/src/shared/common/encryption-patient-fields.boundary.ts` - explicit allow-list of encrypted patient fields |
| Secrets validation | `apps/api/src/shared/modules/config/env-schema.ts` - Zod schema rejects boot without required secrets |
| Log / telemetry scrubbing | `apps/api/src/shared/modules/observability/phi-redactor.ts` - PHI redaction for pino lines + Sentry beforeSend |
| Vulnerability management tooling | `osv-scanner.toml` - dependency scanning config beside CI guardrail scripts (`scripts/checks/*.mjs`) |

A formal STRIDE/threat-model document does not exist in-repo; the tenant-isolation defense chain (middleware → extension → RLS) is the closest living artifact.
---

[← Previous: Attacks & Defense](../02-attacks-and-defense/INDEX.md) · [Next: Interview Drills →](../04-interview-drills/INDEX.md)

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
