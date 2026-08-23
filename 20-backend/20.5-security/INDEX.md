# Security — Index

> **The senior security learning track.** Study in three passes: **I. Auth** (the [auth/](auth/INDEX.md) deep-dive: fundamentals → sessions → tokens → OAuth → authorization) → **II. Attacks & Defense** (XSS, CSRF, SQLi, API Top 10) → **III. Hardening & Operations** (headers/CSP, threat modeling, secrets). Finish with the interview banks.
>
> 16 files — from JWT/OAuth to STRIDE, secrets management, and 50+ curated questions.

[![Files](https://img.shields.io/badge/files-16-blue)](../../INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The Track — Read In This Order

```text
Pass I — AUTH (start here)          Pass II — ATTACKS          Pass III — HARDENING & OPS
auth/INDEX.md                       XSS                        Web Security (headers, CSP)
 └─ fundamentals                    CSRF                       Threat Modeling (STRIDE)
    → sessions & cookies            SQL Injection              Secrets Management
      → JWT                         API Security (Top 10)           ↓
        → OAuth2 / OIDC                  ↓                  INTERVIEW DRILLS
          → RBAC / ABAC             Encryption & Hashing     auth/interview-questions.md
                                    (prerequisite primer)         20.5.13-interview-questions.md
```

### Pass I — Auth ([dedicated index →](auth/INDEX.md))

| Order | File | Topics |
|---|------|--------|
| 0 | [Auth Fundamentals](auth/auth-fundamentals.md) | Identity vs permissions, hashing vs encryption vs signing, Argon2id, CSPRNG, TLS |
| 1 | [Sessions & Cookies](auth/sessions-cookies.md) | Cookie flags, session stores, fixation/hijacking, timeouts |
| 2 | [JWT](auth/jwt.md) | Token structure, signing algorithms, storage trade-offs, refresh rotation, revocation |
| 3 | [OAuth2 / OIDC](auth/oauth2-oidc.md) | Grants, PKCE, scopes, social login, SSO/SAML, passkeys |
| 4 | [RBAC / ABAC](auth/rbac-abac.md) | Role-based vs attribute-based vs relationship-based, policy engines, deny-by-default |

### Pass II — Attacks & Defense

| Order | File | Topics |
|---|------|--------|
| 5 | [Encryption, Hashing & TLS](20.5.06-encryption.md) | Symmetric/asymmetric, salting, AES/RSA, TLS handshake *(primer for Pass I)* |
| 6 | [XSS](20.5.03-xss.md) | Stored/reflected/DOM XSS, CSP, encoding, sanitization |
| 7 | [CSRF](20.5.04-csrf.md) | SameSite, CSRF tokens, double-submit cookies, origin checking |
| 8 | [SQL Injection](20.5.05-sql-injection.md) | Parameterized queries, ORM protection, input validation, WAF |
| 9 | [API Security Best Practices](20.5.12-api-security-best-practices.md) | OWASP API Top 10, BOLA/BFLA, mass assignment, SSRF, helmet |

### Pass III — Hardening & Operations

| Order | File | Topics |
|---|------|--------|
| 10 | [Web Security](20.5.09-web-security.md) | HTTPS, HSTS, CORS, CSP, security headers, OWASP Top 10 |
| 11 | [Threat Modeling — STRIDE](20.5.10-threat-modeling-stride.md) | STRIDE, data-flow diagrams, trust boundaries, attack trees |
| 12 | [Secrets Management](20.5.11-secrets-management.md) | Vault, AWS/GCP secret managers, rotation, KMS, dynamic credentials |

### Interview Drills

| File | Contents |
|------|----------|
| [Auth questions](auth/interview-questions.md) | 40 auth-specific Q&A with follow-up traps |
| [Full security bank](20.5.13-interview-questions.md) | 50+ curated security Q&A with answers |

---

## Cross-References

- Authentication in REST context: [REST — Authentication](../20.3-rest-apis/20.3.07-authentication.md)
- Enforcement in NestJS: [Guards](../20.2-nestjs/20.2.05-guards.md) · [Interceptors](../20.2-nestjs/20.2.07-interceptors.md)
- System-level isolation: [Microservices (mTLS, mesh)](../20.6-microservices/INDEX.md) · [System Design](../../30-architecture/30.2-system-design/INDEX.md)

---

## Navigation

[← Previous: Database](../20.4-database/INDEX.md) · [🏠 Back to Index](../../INDEX.md) · [Next: Microservices →](../20.6-microservices/INDEX.md)
