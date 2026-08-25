# Auth — Authentication & Authorization Learning Track

> **The complete auth flow for senior interviews.** Study the 6 stages below **in order** — each stage builds on the previous one and ends with the trade-offs interviewers probe. Stage files: fundamentals → sessions → tokens → federation → authorization → interview drills.
>
> Part of [Security](../INDEX.md) · Prerequisites: [Encryption & Hashing](../03-hardening-and-operations/20.5.3.01-encryption.md)

[![Files](https://img.shields.io/badge/files-6-blue)](#files-in-this-track)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Status](https://img.shields.io/badge/status-complete-brightgreen)](#)

---

## The Flow — Read Top to Bottom

```text
Stage 0 Stage 1 Stage 2 Stage 3 Stage 4 Stage 5
FOUNDATIONS → SESSIONS → TOKENS → FEDERATED → AUTHORIZATION → INTERVIEW
Who are you? Server remembers Stateless proof Identity from Who may do what? Drills & war stories
(hashing, TLS) you (cookies) (JWT, refresh) others (OAuth/OIDC) (RBAC/ABAC/ReBAC) rehearsal
│ │ │ │ │ │
├─ hashing/salting ├─ cookie flags ├─ JWT anatomy ├─ OAuth 2.0 grants ├─ RBAC ├─ 40+ Q&A
├─ bcrypt/argon2 ├─ session stores ├─ signing: HS256 ├─ OIDC layers ID │ vs ABAC vs ReBAC ├─ trade-off traps
├─ symmetric/asym ├─ fixation/hijacking │ vs RS256 │ token on top ├─ scopes vs roles └─ system-design
└─ TLS/mTLS └─ timeouts/rotation ├─ storage: cookie ├─ PKCE, SAML, SSO vs policies variants
                                                 vs localStorage └─ passkeys future └─ policy engines
                                               └─ rotation + family
                                                  revocation
```

| # | Stage | File | Time | You can defend… |
|---|-------|------|------|-----------------|
| 0 | Foundations | [auth-fundamentals.md](../01-auth/20.5.1.01-auth-fundamentals.md) | 45 min | Hashing vs encryption, password storage, why TLS before anything else |
| 1 | Sessions | [sessions-cookies.md](../01-auth/20.5.1.04-sessions-cookies.md) | 45 min | Cookie flags, server-side state, fixation/hijacking, timeouts |
| 2 | Tokens | [jwt.md](../01-auth/20.5.1.05-jwt.md) | 60 min | JWT anatomy, HS256 vs RS256, storage trade-offs, revocation |
| 3 | Federation | [oauth2-oidc.md](../01-auth/20.5.1.06-oauth2-oidc.md) | 60 min | All OAuth grants, PKCE, OIDC vs OAuth, social login, SSO/SAML |
| 4 | Authorization | [rbac-abac.md](../01-auth/20.5.1.09-rbac-abac.md) | 45 min | RBAC vs ABAC vs ReBAC, scopes vs roles, policy engines, deny-by-default |
| 5 | Drills | [interview-questions.md](../01-auth/20.5.1.10-interview-questions.md) | 45 min | Every classic trap question + follow-ups |

---

## The Master Trade-off Table (memorize this)

Every senior auth interview is a variation of one question: **"which model, and why?"**

### Sessions vs JWT vs Hybrid

| Dimension | Server Sessions | Stateless JWT | Hybrid (access JWT + refresh) |
|-----------|----------------|---------------|-------------------------------|
| State | Server-side store (Redis/DB) | None | Refresh tokens stored; access stateless |
| Revocation | Instant (delete session) | Hard (wait for expiry / denylist) | Fast-ish (rotate + family revoke) |
| Latency | Store lookup per request | Zero lookup | Zero lookup on access path |
| Horizontal scale | Needs shared store or sticky | Free | Free on access path |
| CSRF exposure | Yes (cookie-based) | No if header-borne | Depends on transport (see below) |
| Logout everywhere | Trivial | Painful | Token-family revocation |
| Best for | Traditional web apps, banking | Machine-to-machine, short-lived APIs | SPAs + mobile + APIs (the default answer) |

**One-liner:** *"Stateless JWTs trade revocation for scale. I get both by pairing a 15-minute access JWT with a rotating refresh token — reuse of an old refresh token revokes the whole family."*

### Where do you put the token?

| Storage | XSS-safe | CSRF-safe | Notes |
|---------|-----------|-----------|-------|
| `localStorage` | any XSS steals it | not auto-sent | Never for refresh tokens |
| JS-readable cookie | | | Worst of both |
| `HttpOnly; Secure; SameSite` cookie | | needs SameSite/token | Default for browser apps |
| Memory only (SPA) | (lost on refresh) | | Pair with silent refresh |

### Authorization models

| Model | Question it answers | Example | Cost |
|-------|--------------------|---------|-----| 
| **RBAC** | "What is your role?" | Nurse can edit charts | Coarse; role explosion at scale |
| **ABAC** | "What is true about you, the resource, and the environment?" | Doctor may read patient X *if assigned*, during shift | Fine-grained; needs policy engine + tests |
| **ReBAC** | "What is your relationship to the resource?" | Alice is editor of doc 42 (Google Zanzibar style) | Powerful; heavy infra (SpiceDB/OpenFGA) |

**Decision rule:** start RBAC; add ABAC when ownership/context rules appear ("assigned doctor", "same clinic"); reach for ReBAC when sharing graphs explode (docs, drives). Most healthcare/fintech systems end at RBAC+ABAC layered.

---

## Decision Tree — "Design auth for my app"

```text
Browser-only app?
├── Yes → Session cookie (HttpOnly, Secure, SameSite=Lax) or hybrid w/ refresh rotation
│ └── Regulated data (health/fintech)? → add MFA, audit log, absolute session timeout
└── SPA / mobile / API consumers?
    ├── First-party only → access JWT (15 min) + rotating refresh (httpOnly cookie), family revocation
    ├── "Login with Google/GitHub"? → OAuth 2.0 + PKCE via OIDC provider; never roll your own
    └── Third-party devs calling your API → API keys (server-side) or OAuth client-credentials;
        user-scoped third-party access → full OAuth 2.0 authorization-code flow
Multi-service backend?
└── Gateway validates JWT once (RS256/JWKS); services trust claims; mTLS between services
```

---

## Implementation Recipes (NestJS-shaped)

The concepts above map to concrete guards/pipes. In interviews, name the enforcement point:

| Concept | Enforcement point | File to study |
|---------|-------------------|---------------|
| Credential check + hash verify | AuthService.login (bcrypt.compare) | [fundamentals](../01-auth/20.5.1.01-auth-fundamentals.md) |
| Session issue/rotate | Session middleware + store TTL | [sessions](../01-auth/20.5.1.04-sessions-cookies.md) |
| Token sign/verify | JwtStrategy (Passport), RS256 via JWKS | [JWT](../01-auth/20.5.1.05-jwt.md) |
| Refresh rotation + reuse detection | Refresh endpoint; `replacedBy = sha256(new)`; family revoke on replay | [JWT](../01-auth/20.5.1.05-jwt.md) |
| Social login | Passport Google strategy, auth-code + PKCE | [OAuth2/OIDC](../01-auth/20.5.1.06-oauth2-oidc.md) |
| Role gate | `@Roles('admin')` + RolesGuard | [RBAC/ABAC](../01-auth/20.5.1.09-rbac-abac.md) |
| Policy gate | `@RequirePolicy(resource, action)` + PolicyGuard (deny-by-default) | [RBAC/ABAC](../01-auth/20.5.1.09-rbac-abac.md) |
| Tenant isolation | Tenant interceptor sets context every request; DB-level RLS as backstop | [API security](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) |

> **Senior signal:** say where each control lives *in the request pipeline* (middleware → guard → interceptor → service → query layer) and which layer catches what a previous layer missed (defense in depth).

---

## Attack Surface Checklist (what each stage defends)

| Attack | Defended in stage | Key controls |
|--------|-------------------|--------------|
| Password cracking / credential stuffing | 0 Fundamentals | Argon2id/bcrypt, rate limiting, breach-password checks |
| Session hijacking / fixation | 1 Sessions | Rotate ID on login, Secure/HttpOnly, timeouts |
| Token theft via XSS | 2 Tokens | HttpOnly cookies, CSP, short access TTL |
| Token theft via CSRF | 1–2 | SameSite=Strict/Lax, double-submit token |
| Replay of old refresh token | 2 Tokens | Rotation + token-family revocation |
| Malicious redirect / code interception | 3 OAuth | Allow-list redirect URIs, PKCE |
| Privilege escalation / IDOR | 4 Authorization | Deny-by-default policies, object-level checks, tenant scoping |
| Confused deputy (third-party abuse) | 3–4 | Scopes, consent, audience restriction |

Cross-reference attack details: [XSS](../02-attacks-and-defense/20.5.2.01-xss.md) · [CSRF](../02-attacks-and-defense/20.5.2.02-csrf.md) · [SQL Injection](../02-attacks-and-defense/20.5.2.03-sql-injection.md) · [API Security Top 10](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md)

---

## Files in This Track

| File | Lines of study | Type |
|------|----------------|------|
| [auth-fundamentals.md](../01-auth/20.5.1.01-auth-fundamentals.md) | Identity, credentials, crypto primitives for auth | Core concept |
| [sessions-cookies.md](../01-auth/20.5.1.04-sessions-cookies.md) | Server-side state model | Core concept |
| [jwt.md](../01-auth/20.5.1.05-jwt.md) | Stateless tokens done right | Core concept |
| [oauth2-oidc.md](../01-auth/20.5.1.06-oauth2-oidc.md) | Delegated identity & access | Core concept |
| [rbac-abac.md](../01-auth/20.5.1.09-rbac-abac.md) | Authorization models | Core concept |
| [interview-questions.md](../01-auth/20.5.1.10-interview-questions.md) | 40+ questions with follow-up traps | Drill |
| [../20.5.13-interview-questions.md](../04-interview-drills/20.5.4.01-interview-questions.md) | Full security bank (50+) | Drill |

---

## References & Learn More

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [RFC 6749 — OAuth 2.0 Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [Auth0 — Why refresh tokens rotate](https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation)
- [WebAuthn / Passkeys guide — web.dev](https://web.dev/articles/passkey-registration)
- [Google Zanzibar paper (ReBAC)](https://research.google/pubs/pub48190/)
- [The NIST RBAC standard](https://csrc.nist.gov/projects/role-based-access-control)

---

## Navigation

[← Back to Security Index](../INDEX.md) · [Next: Attacks — XSS →](../02-attacks-and-defense/20.5.2.01-xss.md)
