# Security — Index

> **Study time:** ≈ 3 h 34 m of reading (24 files, ~9 min average).
> **The senior security learning track.** Study in three passes: **I. Auth** (the [01-auth](01-auth/INDEX.md) deep-dive: fundamentals → Basic/Digest → API keys → sessions → JWT → OAuth/OIDC → SSO/SAML → MFA/passkeys → RBAC → ABAC) → **II. Attacks & Defense** (XSS, CSRF, SQL injection, API security) → **III. Hardening & Operations** (encryption/TLS, browser policy, threat modeling, secrets and vulnerability response). Finish with the interview banks.
>
> The 21 learning and interview files, plus three revision companions, cover HTTP authentication through passkeys, common application attacks, and production security operations.

[![Files](https://img.shields.io/badge/files-24-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

Security decisions determine which identities can reach which data and how a service contains failures. This track moves from authentication and authorization through application attacks to production controls. Healthcare and fintech examples make regulatory boundaries concrete; actual obligations depend on the system, data and jurisdiction.

---

## Topic Categories

The 21 learning and interview files are organized into 4 categories. Three category revision companions bring the total to 24 files. Follow each category INDEX for its chapter order.

| Category | Files | Why it matters |
| -------------------------------------------------------------- | ----: | -------------------------------------------------------------------------------------------------------------------------------------------- |
| [Auth (the deep-dive)](01-auth/INDEX.md) | 11 | Ten concept chapters from credential handling through policy enforcement, followed by an auth interview bank |
| [Attacks & Defense](02-attacks-and-defense/INDEX.md) | 4 | XSS, CSRF, SQL injection and API abuse patterns |
| [Hardening & Operations](03-hardening-and-operations/INDEX.md) | 5 | Encryption/TLS primer, headers/CSP, STRIDE threat modeling, secrets, vulnerability management |
| [Interview Drills](04-interview-drills/INDEX.md) | 1 | Full security bank; pairs with the auth-track question set |

---

## The Track — Read In This Order

```text
Prerequisite — Encryption & TLS reference, if needed
Pass I — Auth: identity → credentials → sessions/tokens → federation → MFA → authorization
Pass II — Attacks: XSS → CSRF → SQL injection → API abuse
Pass III — Operations: browser policy → threat model → secrets → vulnerability response
Finish — Auth interview bank + full security scenario bank
```

The files take about 4 h 1 m to read. Reserve roughly 12 hours for a complete pass with revision and practice. The encryption chapter is a reference primer; skim it if TLS and cryptographic primitives are already familiar.

---

## Authentication (the deep-dive)

Ten auth and authorization chapters build from credentials to policy enforcement. Finish the learning sequence before attempting either interview bank.

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | --------: |
| 1 | [Auth Fundamentals](01-auth/20.5.1.01-auth-fundamentals.md) | Identity vs permissions, hashing vs encryption vs signing, Argon2id, CSPRNG, TLS | Essential | Foundational | 7 min |
| 2 | [HTTP Basic & Digest Auth](01-auth/20.5.1.02-http-basic-digest-auth.md) | Authorization header, Base64-over-TLS, 401 handshake, Digest challenge-response legacy, nginx patterns | Important | Specialized | 12 min |
| 3 | [API Keys](01-auth/20.5.1.03-api-keys.md) | CSPRNG generation, hashing keys at rest, `sk_live_` prefixes, rotation windows, scopes, leak runbook | Essential | Foundational | 13 min |
| 4 | [Sessions & Cookies](01-auth/20.5.1.04-sessions-cookies.md) | Cookie flags, session stores, fixation/hijacking, timeouts | Essential | Foundational | 8 min |
| 5 | [JWT](01-auth/20.5.1.05-jwt.md) | Token structure, signing algorithms, storage trade-offs, refresh rotation, revocation | Essential | Foundational | 9 min |
| 6 | [OAuth2 / OIDC](01-auth/20.5.1.06-oauth2-oidc.md) | Grants, PKCE, scopes, social login, the OIDC identity layer | Essential | Foundational | 13 min |
| 7 | [SSO / SAML / Federation](01-auth/20.5.1.07-sso-saml-federation.md) | One IdP many SPs, SAML flows, assertions & certs, SAML vs OIDC, SCIM/JIT provisioning | Important | Specialized | 12 min |
| 8 | [MFA / Passkeys / WebAuthn](01-auth/20.5.1.08-mfa-passkeys-webauthn.md) | TOTP mechanics, SMS weaknesses, WebAuthn ceremonies, passkey sync, AAL levels, recovery | Important | Specialized | 14 min |
| 9 | [RBAC / ABAC](01-auth/20.5.1.09-rbac-abac.md) | Role assignment and activation, policy models, and the boundary between a role and object access | Essential | Foundational | 10 min |
| 10 | [ABAC Access Control](01-auth/20.5.1.10-abac-access-control.md) | Trusted attribute sources, policy evaluation, enforcement points and failure handling | Essential | Foundational | 9 min |

Stage 10 is the auth question bank ([drills](01-auth/20.5.1.11-interview-questions.md)); the complete learning flow is in the [auth INDEX](01-auth/INDEX.md).

---

## Attacks & Defense

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------- | ------------------ | --------: |
| 11 | [XSS](02-attacks-and-defense/20.5.2.01-xss.md) | Stored/reflected/DOM XSS, CSP, encoding, sanitization | Essential | Foundational | 6 min |
| 12 | [CSRF](02-attacks-and-defense/20.5.2.02-csrf.md) | SameSite, CSRF tokens, double-submit cookies, origin checking | Essential | Foundational | 7 min |
| 13 | [SQL Injection](02-attacks-and-defense/20.5.2.03-sql-injection.md) | Parameterized queries, ORM protection, input validation, WAF | Essential | Foundational | 6 min |
| 14 | [API Security Best Practices](02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) | Object/property authorization, resource limits, SSRF and input/output boundaries | Essential | Foundational | 10 min |

---

## Hardening & Operations

| Order | File | Topics | Role priority | General importance | Read time |
| ----: | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ------------- | ------------------ | --------: |
| — | [Encryption, Hashing & TLS](03-hardening-and-operations/20.5.3.01-encryption.md) | Symmetric/asymmetric, salting, AES/RSA, TLS handshake *(prerequisite for Pass I)* | Essential | Foundational | 45 min |
| 15 | [Web Security](03-hardening-and-operations/20.5.3.02-web-security.md) | HTTPS, HSTS, CORS, CSP, security headers, OWASP Top 10 | Essential | Foundational | 8 min |
| 16 | [Threat Modeling — STRIDE](03-hardening-and-operations/20.5.3.03-threat-modeling-stride.md) | STRIDE, data-flow diagrams, trust boundaries, attack trees | Important | Specialized | 7 min |
| 17 | [Secrets Management](03-hardening-and-operations/20.5.3.04-secrets-management.md) | Vault, AWS/GCP secret managers, rotation, KMS, dynamic credentials | Essential | Foundational | 8 min |
| 18 | [Vulnerability Management & Patch Governance](03-hardening-and-operations/20.5.3.05-vulnerability-management-patch-governance.md) | CVE/CVSS + EPSS/KEV triage, SBOM (CycloneDX/SPDX), scanner roles, patch SLAs, emergency process, base-image refresh, risk acceptance, MTTR | Important | Specialized | 12 min |

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
1. **Auth Fundamentals + Sessions + JWT** (2.5 hrs) — establish identity, session and token boundaries
2. **XSS + CSRF + SQLi** (1.5 hrs) — trace the distinct browser, request and query boundaries
3. **Web Security + Secrets** (1 hr) — production basics
4. **Auth interview questions** (1.5 hrs)

### Path B — Healthcare / Fintech (3-4 days)
1. **All Auth files** (7 hrs)
2. **Encryption** (45 min)
3. **All Attacks** (2 hrs)
4. **Threat Modeling + STRIDE** (1 hr)
5. **Triage and response practice** (1 hr)
6. **Both interview banks** (3 hrs)

### Path C — Interview tomorrow
- Spend 60–90 minutes on session/JWT expiry and revocation, OAuth transaction binding, object/tenant authorization, XSS/CSRF boundaries and incident response.
- Rehearse five questions across the auth and security banks. State the threat, enforcement point, failure behavior and evidence you would test.
- Revisit only the summaries for weak areas; do not try to reread all 24 files.

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
