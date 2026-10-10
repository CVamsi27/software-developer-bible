# Security — Index

> **Study time:** ≈ 3 h 38 m of reading (24 files, ~9 min average).
> **The senior security learning track.** Study in three passes: **I. Auth** (the [01-auth](01-auth/INDEX.md) deep-dive: fundamentals → Basic/API keys → sessions → tokens → OAuth → SSO/SAML → MFA/passkeys → authorization) → **II. Attacks & Defense** (XSS, CSRF, SQLi, API Top 10) → **III. Hardening & Operations** (headers/CSP, threat modeling, secrets). Finish with the interview banks.
>
> 24 files — from HTTP Basic auth to passkeys, and from XSS to STRIDE, secrets management, vulnerability management, and authored interview questions.

[![Files](https://img.shields.io/badge/files-24-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)
[![Read time](https://img.shields.io/badge/read%20time-12%2B%20hrs-blueviolet)](#)

**Why security:** Every senior interview (especially at healthcare/fintech) tests security knowledge. Auth (JWT vs sessions vs OAuth), attacks (XSS, CSRF, SQLi), and the security framework (OWASP, STRIDE, secrets management) are table stakes. These controls also help reason about real failures at trust boundaries.

---

## Topic Categories

The 21 files are organized into 4 categories, each with its own INDEX. Read in order within each.

| Category | Files | Why it matters |
| -------------------------------------------------------------- | ----: | -------------------------------------------------------------------------------------------------------------------------------------------- |
| [Auth (the deep-dive)](01-auth/INDEX.md) | 11 | The complete 11-stage auth track: fundamentals → Basic/API keys → sessions → JWT → OAuth/OIDC → SSO/SAML → MFA/passkeys → RBAC/ABAC + drills |
| [Attacks & Defense](02-attacks-and-defense/INDEX.md) | 4 | XSS, CSRF, SQLi, API Top 10 — what can go wrong |
| [Hardening & Operations](03-hardening-and-operations/INDEX.md) | 5 | Encryption/TLS primer, headers/CSP, STRIDE threat modeling, secrets, vulnerability management |
| [Interview Drills](04-interview-drills/INDEX.md) | 1 | Full security bank; pairs with the auth-track question set |

---

## The Track — Read In This Order

```text
Pass I — AUTH (start here)      Pass II — ATTACKS            Pass III — HARDENING & OPS
01-auth/INDEX.md                XSS                          Web Security (headers, CSP)
 └─ fundamentals                CSRF                         Threat Modeling (STRIDE)
    → basic/digest + api keys   SQL Injection                Secrets Management
      → sessions & cookies      API Security (Top 10)        Vulnerability Management
        → JWT                                                (CVE triage, SBOM, patch SLAs)
          → OAuth2 / OIDC           ↓
            → SSO / SAML          INTERVIEW DRILLS
              → MFA / passkeys    20.5.1.10 (auth bank)
                → RBAC / ABAC     20.5.4.01 (security bank)
                  ↓ Encryption & Hashing
                    (prerequisite primer)
```

**Total time: ~12 hours** if you read all files. Skip the encryption primer if you already know TLS + hashing.

---

## Authentication (the deep-dive)

A complete 10-stage track in [01-auth](01-auth/INDEX.md). Read these in order — each builds on the previous.

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | --------: |
| 0 | [Auth Fundamentals](01-auth/20.5.1.01-auth-fundamentals.md) | Identity vs permissions, hashing vs encryption vs signing, Argon2id, CSPRNG, TLS | Essential | 7 min | 7 min |
| 1 | [HTTP Basic & Digest Auth](01-auth/20.5.1.02-http-basic-digest-auth.md) | Authorization header, Base64-over-TLS, 401 handshake, Digest challenge-response legacy, nginx patterns | Important | 14 min | 15 min |
| 2 | [API Keys](01-auth/20.5.1.03-api-keys.md) | CSPRNG generation, hashing keys at rest, `sk_live_` prefixes, rotation windows, scopes, leak runbook | Essential | 13 min | 14 min |
| 3 | [Sessions & Cookies](01-auth/20.5.1.04-sessions-cookies.md) | Cookie flags, session stores, fixation/hijacking, timeouts | Essential | 16 min | 10 min |
| 4 | [JWT](01-auth/20.5.1.05-jwt.md) | Token structure, signing algorithms, storage trade-offs, refresh rotation, revocation | Essential | 12 min | 11 min |
| 5 | [OAuth2 / OIDC](01-auth/20.5.1.06-oauth2-oidc.md) | Grants, PKCE, scopes, social login, the OIDC identity layer | Essential | 19 min | 13 min |
| 6 | [SSO / SAML / Federation](01-auth/20.5.1.07-sso-saml-federation.md) | One IdP many SPs, SAML flows, assertions & certs, SAML vs OIDC, SCIM/JIT provisioning | Important | 14 min | 14 min |
| 7 | [MFA / Passkeys / WebAuthn](01-auth/20.5.1.08-mfa-passkeys-webauthn.md) | TOTP mechanics, SMS weaknesses, WebAuthn ceremonies, passkey sync, AAL levels, recovery | Important | 18 min | 14 min |
| 8 | [RBAC / ABAC](01-auth/20.5.1.09-rbac-abac.md) | Role-based vs attribute-based vs relationship-based, policy engines, deny-by-default | Essential | 20 min | 12 min |

Stages 10 = the auth question bank below ([drills](01-auth/20.5.1.11-interview-questions.md)); full flow table in the [auth INDEX](01-auth/INDEX.md).

---

## Attacks & Defense

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 9 | [XSS](02-attacks-and-defense/20.5.2.01-xss.md) | Stored/reflected/DOM XSS, CSP, encoding, sanitization | Essential | 11 min | 8 min |
| 10 | [CSRF](02-attacks-and-defense/20.5.2.02-csrf.md) | SameSite, CSRF tokens, double-submit cookies, origin checking | Essential | 14 min | 8 min |
| 11 | [SQL Injection](02-attacks-and-defense/20.5.2.03-sql-injection.md) | Parameterized queries, ORM protection, input validation, WAF | Essential | 12 min | 7 min |
| 12 | [API Security Best Practices](02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) | OWASP API Top 10, BOLA/BFLA, mass assignment, SSRF, helmet | Essential | 11 min | 10 min |

---

## Hardening & Operations

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | --------: |
| — | [Encryption, Hashing & TLS](03-hardening-and-operations/20.5.3.01-encryption.md) | Symmetric/asymmetric, salting, AES/RSA, TLS handshake *(prerequisite for Pass I)* | Essential | Foundational | 45 min |
| 13 | [Web Security](03-hardening-and-operations/20.5.3.02-web-security.md) | HTTPS, HSTS, CORS, CSP, security headers, OWASP Top 10 | Essential | 19 min | 8 min |
| 14 | [Threat Modeling — STRIDE](03-hardening-and-operations/20.5.3.03-threat-modeling-stride.md) | STRIDE, data-flow diagrams, trust boundaries, attack trees | Important | 9 min | 5 min |
| 15 | [Secrets Management](03-hardening-and-operations/20.5.3.04-secrets-management.md) | Vault, AWS/GCP secret managers, rotation, KMS, dynamic credentials | Essential | 11 min | 7 min |
| 16 | [Vulnerability Management & Patch Governance](03-hardening-and-operations/20.5.3.05-vulnerability-management-patch-governance.md) | CVE/CVSS + EPSS/KEV triage, SBOM (CycloneDX/SPDX), scanner roles, patch SLAs, emergency process, base-image refresh, risk acceptance, MTTR | Important | 11 min | 12 min |

---

Before drills, revisit [auth revision](01-auth/REVISION.md), [attack revision](02-attacks-and-defense/REVISION.md) and [hardening revision](03-hardening-and-operations/REVISION.md).

## Interview Drills

| File | Contents | Role priority | General importance |
| -------------------------------------------------------------------------- | --------------------------------------------- | ------------- | ------------------ |
| [Auth questions](01-auth/20.5.1.11-interview-questions.md) | 40 auth-specific Q&A with follow-up traps | Essential | Foundational |
| [Full security bank](04-interview-drills/20.5.4.01-interview-questions.md) | Security scenarios with source-linked answers | Essential | Foundational |

---

## Suggested Study Order

### Path A — Mid-stage startup (1-2 days)
1. **Auth Fundamentals + Sessions + JWT** (2.5 hrs) — must know
2. **XSS + CSRF + SQLi** (1.5 hrs) — the most-asked attacks
3. **Web Security + Secrets** (1 hr) — production basics
4. **Auth interview questions** (1.5 hrs)

### Path B — Healthcare / Fintech (3-4 days)
1. **All Auth files** (7 hrs)
2. **Encryption** (45 min)
3. **All Attacks** (2 hrs)
4. **Threat Modeling + STRIDE** (1 hr)
5. **API Security** (1 hr)
6. **Both interview banks** (3 hrs)

### Path C — Interview tomorrow
- Review each chapter’s definition, example and summary; focus on the topics listed above
- Re-read JWT + Sessions (the most-tested)
- Re-read the 20 hardest Auth + Security interview Qs

---

## Common interview topics

- "Sessions vs JWT — when to use which?"
- "Where do you store JWTs? Why not localStorage?"
- "How do you prevent CSRF?"
- "Walk me through an OAuth login flow."
- "Walk me through a SAML SSO flow. Why is IdP-initiated login riskier?"
- "Why are passkeys phishing-resistant but TOTP codes aren't?"
- "What's the difference between RBAC and ABAC?"
- "How do you manage secrets in production?"
- "Walk me through a STRIDE threat model for X."

---

## Cross-References

- **Authentication in REST context:** [REST — Authentication](../20.3-rest-apis/04-edge-and-scale/20.3.4.04-authentication.md)
- **Enforcement in NestJS:** [Guards](../20.2-nestjs/02-request-lifecycle/20.2.2.02-guards.md) · [Interceptors](../20.2-nestjs/02-request-lifecycle/20.2.2.04-interceptors.md)
- **System-level isolation:** [Microservices (mTLS, mesh)](../20.6-microservices/INDEX.md) · [System Design](../../30-architecture/30.2-system-design/INDEX.md)
- **AI safety & PII:** [AI Engineering — Safety & Cost](../20.12-ai-engineering/20.12.06-safety-cost-governance.md)

---

## Navigation

[← Previous: Database](../20.4-database/INDEX.md) · [ Back to Index](../../INDEX.md) · [Next: Microservices →](../20.6-microservices/INDEX.md)

---

## Docita Anchor

These [Docita](https://github.com/CVamsi27/docita) source paths are inspection starting points; source presence does not establish deployed coverage:

| Topic | Docita evidence |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| JWT auth | `apps/api/src/shared/modules/auth/auth/jwt.strategy.ts` + `jwt-auth.guard.ts` + `staff-jwt-audience.guard.ts` - passport strategy with audience checks |
| Sessions, API keys & resets | `apps/api/src/shared/modules/auth/auth/auth-session.service.ts`, `api-key.service.ts`, `auth-password.controller.ts`, `auth-email-verification.service.ts`, `auth-mfa-orchestrator.service.ts` |
| RBAC / ABAC | `apps/api/src/shared/modules/authorization/` - `authorization.service.ts` + `abac-policy.registry.ts` + `role-bridge.ts`; enforced via `roles.guard.ts` / `policy.guard.ts` / `require-policy.decorator.ts` |
| Tenant isolation | `apps/api/src/shared/common/middleware/tenant.middleware.ts` + `apps/api/src/shared/modules/auth/guards/tenant.guard.ts` + `shared/modules/rls/` — tenant mechanisms to trace; verify enabled RLS, scoped client usage and cross-tenant denial at each operation |
| CSRF & security headers | `apps/api/src/shared/common/interceptors/csrf.interceptor.ts`; `helmet` configured in `apps/api/src/main.ts` |
| Rate limiting | `apps/api/src/shared/modules/auth/guards/ip-rate-limit.guard.ts`, `user-rate-limit.guard.ts` + `shared/modules/tenant-rate-limit/` - per-IP/user/clinic quotas |
| Audit logging | `apps/api/src/shared/modules/audit/audit-logger.service.ts` + `shared/common/interceptors/patient-audit.interceptor.ts` - access events for PHI surfaces |
| Field-level encryption | `apps/api/src/shared/common/encryption.service.ts` + `encryption-patient-fields.boundary.ts` - sensitive patient fields encrypted before write |
| Emergency access | `apps/api/src/shared/common/interceptors/emergency-access.interceptor.ts` + `apps/api/src/shared/modules/auth/decorators/emergency-access.decorator.ts` - break-glass with audit trail |
