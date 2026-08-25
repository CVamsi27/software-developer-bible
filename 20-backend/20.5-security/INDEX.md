# Security — Index

> **The senior security learning track.** Study in three passes: **I. Auth** (the [auth/](01-auth/INDEX.md) deep-dive: fundamentals → sessions → tokens → OAuth → authorization) → **II. Attacks & Defense** (XSS, CSRF, SQLi, API Top 10) → **III. Hardening & Operations** (headers/CSP, threat modeling, secrets). Finish with the interview banks.
>
> 15 files — from JWT/OAuth to STRIDE, secrets management, and 50+ curated questions.

[![Files](https://img.shields.io/badge/files-15-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)
[![Read time](https://img.shields.io/badge/read%20time-10%2B%20hrs-blueviolet)](#)

**Why security:** Every senior interview (especially at healthcare/fintech) tests security knowledge. Auth (JWT vs sessions vs OAuth), attacks (XSS, CSRF, SQLi), and the security framework (OWASP, STRIDE, secrets management) are table stakes. Plus, real production bugs are usually security bugs.

---

## Topic Categories

The 15 files are organized into 5 conceptual categories. Read in order within each.

| Category | Files | Why it matters |
|----------|------:|----------------|
| [Authentication (the deep-dive)](#authentication-the-deep-dive) | 5 + 1 interview | JWT, OAuth, sessions, RBAC — the core of every app |
| [Cryptography Primer](#cryptography-primer) | 1 | Encryption, hashing, TLS — the foundation for auth |
| [Attacks & Defense](#attacks--defense) | 4 | XSS, CSRF, SQLi, API Top 10 — what can go wrong |
| [Hardening & Operations](#hardening--operations) | 3 | Headers, threat modeling, secrets — production hygiene |
| [Interview Drills](#interview-drills) | 2 | 90+ curated Q&A across auth + general security |

---

## The Track — Read In This Order

```text
Pass I — AUTH (start here) Pass II — ATTACKS Pass III — HARDENING & OPS
auth/INDEX.md XSS Web Security (headers, CSP)
 └─ fundamentals CSRF Threat Modeling (STRIDE)
    → sessions & cookies SQL Injection Secrets Management
      → JWT API Security (Top 10) ↓
        → OAuth2 / OIDC ↓ INTERVIEW DRILLS
          → RBAC / ABAC Encryption & Hashing auth/interview-questions.md
                                    (prerequisite primer) 20.5.13-interview-questions.md
```

**Total time: ~10-12 hours** if you read all files. Skip the encryption primer if you already know TLS + hashing.

---

## Authentication (the deep-dive)

A standalone track in [auth/](01-auth/INDEX.md). Read these in order — each builds on the previous.

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 0 | [Auth Fundamentals](01-auth/20.5.1.01-auth-fundamentals.md) | Identity vs permissions, hashing vs encryption vs signing, Argon2id, CSPRNG, TLS | 45 min |
| 1 | [Sessions & Cookies](01-auth/20.5.1.04-sessions-cookies.md) | Cookie flags, session stores, fixation/hijacking, timeouts | 45 min |
| 2 | [JWT](01-auth/20.5.1.05-jwt.md) | Token structure, signing algorithms, storage trade-offs, refresh rotation, revocation | 60 min |
| 3 | [OAuth2 / OIDC](01-auth/20.5.1.06-oauth2-oidc.md) | Grants, PKCE, scopes, social login, SSO/SAML, passkeys | 60 min |
| 4 | [RBAC / ABAC](01-auth/20.5.1.09-rbac-abac.md) | Role-based vs attribute-based vs relationship-based, policy engines, deny-by-default | 45 min |

---

## Cryptography Primer

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 5 | [Encryption, Hashing & TLS](03-hardening-and-operations/20.5.3.01-encryption.md) | Symmetric/asymmetric, salting, AES/RSA, TLS handshake *(prerequisite for Pass I)* | 45 min |

---

## Attacks & Defense

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 6 | [XSS](02-attacks-and-defense/20.5.2.01-xss.md) | Stored/reflected/DOM XSS, CSP, encoding, sanitization | 30 min |
| 7 | [CSRF](02-attacks-and-defense/20.5.2.02-csrf.md) | SameSite, CSRF tokens, double-submit cookies, origin checking | 25 min |
| 8 | [SQL Injection](02-attacks-and-defense/20.5.2.03-sql-injection.md) | Parameterized queries, ORM protection, input validation, WAF | 30 min |
| 9 | [API Security Best Practices](02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) | OWASP API Top 10, BOLA/BFLA, mass assignment, SSRF, helmet | 30 min |

---

## Hardening & Operations

| Order | File | Topics | Read time |
|------:|------|--------|----------:|
| 10 | [Web Security](03-hardening-and-operations/20.5.3.02-web-security.md) | HTTPS, HSTS, CORS, CSP, security headers, OWASP Top 10 | 30 min |
| 11 | [Threat Modeling — STRIDE](03-hardening-and-operations/20.5.3.03-threat-modeling-stride.md) | STRIDE, data-flow diagrams, trust boundaries, attack trees | 30 min |
| 12 | [Secrets Management](03-hardening-and-operations/20.5.3.04-secrets-management.md) | Vault, AWS/GCP secret managers, rotation, KMS, dynamic credentials | 25 min |

---

## Interview Drills

| File | Contents |
|------|----------|
| [Auth questions](01-auth/20.5.1.10-interview-questions.md) | 40 auth-specific Q&A with follow-up traps |
| [Full security bank](04-interview-drills/20.5.4.01-interview-questions.md) | 50+ curated security Q&A with answers |

---

## Suggested Study Order

### Path A — Mid-stage startup (1-2 days)
1. **Auth Fundamentals + Sessions + JWT** (2.5 hrs) — must know
2. **XSS + CSRF + SQLi** (1.5 hrs) — the most-asked attacks
3. **Web Security + Secrets** (1 hr) — production basics
4. **Auth interview questions** (1.5 hrs)

### Path B — Healthcare / Fintech (3-4 days)
1. **All Auth files** (5 hrs)
2. **Encryption** (45 min)
3. **All Attacks** (2 hrs)
4. **Threat Modeling + STRIDE** (1 hr)
5. **API Security** (1 hr)
6. **Both interview banks** (3 hrs)

### Path C — Interview tomorrow
- Skim all TL;DR boxes
- Re-read JWT + Sessions (the most-tested)
- Re-read the 20 hardest Auth + Security interview Qs

---

## Common interview topics

- "Sessions vs JWT — when to use which?"
- "Where do you store JWTs? Why not localStorage?"
- "How do you prevent CSRF?"
- "Walk me through an OAuth login flow."
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
