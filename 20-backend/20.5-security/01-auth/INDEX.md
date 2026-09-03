# Auth - Security

> **The complete authentication & authorization learning track — all 10 stages.** Read them **in order**, each builds on the previous; finish with the interview drills.
>
> Part of [Security](../INDEX.md) · Prerequisite: [Encryption & Hashing](../03-hardening-and-operations/20.5.3.01-encryption.md)

[![Files](https://img.shields.io/badge/files-11-blue)](#files-in-this-track)
[![Category](https://img.shields.io/badge/category-Auth-blue)](../INDEX.md)

---

## The Flow — Read Top to Bottom

```text
Stage 0          Stage 1            Stage 2           Stage 3           Stage 4
FOUNDATIONS  →   BASIC & DIGEST →   API KEYS      →   SESSIONS      →   TOKENS (JWT)
Who are you?     Legacy HTTP        Machine id for    Server remembers  Stateless proof
(hashing, TLS)   credentials        services          you (cookies)     (+ refresh rotation)

Stage 5          Stage 6            Stage 7           Stage 8           Stage 9
FEDERATED    →   ENTERPRISE SSO →   STRONG AUTH   →   AUTHORIZATION →   INTERVIEW
IDENTITY         SAML + SCIM        MFA / PASSKEYS    Who may do what?  Drills & war
(OAuth / OIDC)   workforce trust    WebAuthn          RBAC/ABAC/ReBAC   stories rehearsal
```

---

## The 10-Stage Auth Track

Stage numbers are study order (`0`-`9`), not file IDs — read top to bottom.

| #   | Stage                       | File                                                                       | Time   | You can defend…                                                                                                                 |
| --: | -------                     | ------                                                                     | ------ | ------------------                                                                                                              |
| 0   | Foundations                 | [20.5.1.01-auth-fundamentals.md](20.5.1.01-auth-fundamentals.md)           | 45 min | Hashing vs encryption, password storage (Argon2id), CSPRNG, why TLS before anything else                                        |
| 1   | HTTP Basic & Digest Auth    | [20.5.1.02-http-basic-digest-auth.md](20.5.1.02-http-basic-digest-auth.md) | 30 min | Authorization header mechanics, Base64-over-TLS only, Digest challenge-response and why it died, when Basic is still OK         |
| 2   | API Keys                    | [20.5.1.03-api-keys.md](20.5.1.03-api-keys.md)                             | 30 min | Key generation with CSPRNG, hashing keys at rest, prefix schemes (`sk_live_`), rotation grace windows, per-key scopes           |
| 3   | Sessions & Cookies          | [20.5.1.04-sessions-cookies.md](20.5.1.04-sessions-cookies.md)             | 45 min | Cookie flags, server-side state, fixation/hijacking, timeouts                                                                   |
| 4   | Tokens (JWT)                | [20.5.1.05-jwt.md](20.5.1.05-jwt.md)                                       | 60 min | JWT anatomy, HS256 vs RS256, storage trade-offs, refresh rotation + family revocation                                           |
| 5   | Federation (OAuth2 / OIDC)  | [20.5.1.06-oauth2-oidc.md](20.5.1.06-oauth2-oidc.md)                       | 60 min | All OAuth grants, PKCE, OIDC vs OAuth, scopes, social login                                                                     |
| 6   | SSO / SAML / Federation     | [20.5.1.07-sso-saml-federation.md](20.5.1.07-sso-saml-federation.md)       | 45 min | One IdP session many SPs, SAML 2.0 flows (SP-/IdP-initiated), assertions & signing certs, SAML vs OIDC, SCIM + JIT provisioning |
| 7   | MFA / Passkeys / WebAuthn   | [20.5.1.08-mfa-passkeys-webauthn.md](20.5.1.08-mfa-passkeys-webauthn.md)   | 45 min | TOTP mechanics (RFC 6238), SMS/SIM-swap weakness, WebAuthn ceremonies, passkey sync, AAL levels, recovery as weakest link       |
| 8   | Authorization (RBAC / ABAC) | [20.5.1.09-rbac-abac.md](20.5.1.09-rbac-abac.md)                           | 45 min | RBAC vs ABAC vs ReBAC, scopes vs roles, policy engines, deny-by-default                                                         |
| 9   | Interview Drills            | [20.5.1.10-interview-questions.md](20.5.1.10-interview-questions.md)       | 45 min | Every classic trap question + follow-ups                                                                                        |
| 10  | ABAC Deep Dive              | [20.5.1.11-abac-access-control.md](20.5.1.11-abac-access-control.md)     | 35 min | Attribute-based policies, deny-overrides, policy engines, testing ABAC                                                            |

---

## The Master Trade-off Table (memorize this)

Every senior auth interview is a variation of one question: **"which model, and why?"**

### Sessions vs JWT vs Hybrid

| Dimension         | Server Sessions               | Stateless JWT                        | Hybrid (access JWT + refresh)             |
| ----------------- | ----------------------------- | ------------------------------------ | ----------------------------------------- |
| State             | Server-side store (Redis/DB)  | None                                 | Refresh tokens stored; access stateless   |
| Revocation        | Instant (delete session)      | Hard (wait for expiry / denylist)    | Fast-ish (rotate + family revoke)         |
| Latency           | Store lookup per request      | Zero lookup                          | Zero lookup on access path                |
| Horizontal scale  | Needs shared store or sticky  | Free                                 | Free on access path                       |
| CSRF exposure     | Yes (cookie-based)            | No if header-borne                   | Depends on transport (see below)          |
| Logout everywhere | Trivial                       | Painful                              | Token-family revocation                   |
| Best for          | Traditional web apps, banking | Machine-to-machine, short-lived APIs | SPAs + mobile + APIs (the default answer) |

**One-liner:** *"Stateless JWTs trade revocation for scale. I get both by pairing a 15-minute access JWT with a rotating refresh token — reuse of an old refresh token revokes the whole family."*

### Where do you put the token?

| Storage                             | XSS-safe          | CSRF-safe            | Notes                    |
| ----------------------------------- | ----------------- | -------------------- | ------------------------ |
| `localStorage`                      | any XSS steals it | not auto-sent        | Never for refresh tokens |
| JS-readable cookie                  |                   |                      | Worst of both            |
| `HttpOnly; Secure; SameSite` cookie |                   | needs SameSite/token | Default for browser apps |
| Memory only (SPA)                   | (lost on refresh) |                      | Pair with silent refresh |

### Authorization models

| Model     | Question it answers                                          | Example                                               | Cost                                      |
| --------- | ------------------------------------------------------------ | ----------------------------------------------------- | ----------------------------------------- |
| **RBAC**  | "What is your role?"                                         | Nurse can edit charts                                 | Coarse; role explosion at scale           |
| **ABAC**  | "What is true about you, the resource, and the environment?" | Doctor may read patient X *if assigned*, during shift | Fine-grained; needs policy engine + tests |
| **ReBAC** | "What is your relationship to the resource?"                 | Alice is editor of doc 42 (Google Zanzibar style)     | Powerful; heavy infra (SpiceDB/OpenFGA)   |

**Decision rule:** start RBAC; add ABAC when ownership/context rules appear ("assigned doctor", "same clinic"); reach for ReBAC when sharing graphs explode (docs, drives). Most healthcare/fintech systems end at RBAC+ABAC layered.

---

## Decision Tree — "Design auth for my app"

```text
Browser-only app?
├── Yes → Session cookie (HttpOnly, Secure, SameSite=Lax) or hybrid w/ refresh rotation
│         └── Regulated data (health/fintech)? → add MFA, audit log, absolute session timeout
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

| Concept                            | Enforcement point                                                       | File to study                                                                      |
| ---------------------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Credential check + hash verify     | AuthService.login (bcrypt.compare)                                      | [fundamentals](20.5.1.01-auth-fundamentals.md)                                     |
| Static credential gate (Basic)     | BasicAuthGuard decodes header + timing-safe compare                     | [Basic/Digest](20.5.1.02-http-basic-digest-auth.md)                                |
| Machine-to-machine identity        | ApiKeyGuard: prefix lookup -> SHA-256 compare -> scopes                 | [API Keys](20.5.1.03-api-keys.md)                                                  |
| Session issue/rotate               | Session middleware + store TTL                                          | [sessions](20.5.1.04-sessions-cookies.md)                                          |
| Token sign/verify                  | JwtStrategy (Passport), RS256 via JWKS                                  | [JWT](20.5.1.05-jwt.md)                                                            |
| Refresh rotation + reuse detection | Refresh endpoint; `replacedBy = sha256(new)`; family revoke on replay   | [JWT](20.5.1.05-jwt.md)                                                            |
| Social login                       | Passport Google strategy, auth-code + PKCE                              | [OAuth2/OIDC](20.5.1.06-oauth2-oidc.md)                                            |
| Enterprise SSO login               | SamlStrategy.validate -> JIT provision -> SP session                    | [SSO/SAML](20.5.1.07-sso-saml-federation.md)                                       |
| Second factor ceremony             | TotpService.verify or @simplewebauthn loginFinish                       | [MFA/Passkeys](20.5.1.08-mfa-passkeys-webauthn.md)                                 |
| Role gate                          | `@Roles('admin')` + RolesGuard                                          | [RBAC/ABAC](20.5.1.09-rbac-abac.md)                                                |
| Policy gate                        | `@RequirePolicy(resource, action)` + PolicyGuard (deny-by-default)      | [RBAC/ABAC](20.5.1.09-rbac-abac.md)                                                |
| Tenant isolation                   | Tenant interceptor sets context every request; DB-level RLS as backstop | [API security](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) |

> **Senior signal:** say where each control lives *in the request pipeline* (middleware → guard → interceptor → service → query layer) and which layer catches what a previous layer missed (defense in depth).

---

## Attack Surface Checklist (what each stage defends)

| Attack                                    | Defended in stage | Key controls                                                        |
| ----------------------------------------- | ----------------- | ------------------------------------------------------------------- |
| Password cracking / credential stuffing   | 0 Fundamentals    | Argon2id/bcrypt, rate limiting, breach-password checks              |
| Credential interception on plaintext HTTP | 1 Basic/Digest    | TLS everywhere, HSTS, proxy basic-auth only over TLS                |
| API key leakage / abuse                   | 2 API Keys        | Hashed at rest, scopes, IP binding, dual-key rotation, leak runbook |
| Session hijacking / fixation              | 3 Sessions        | Rotate ID on login, Secure/HttpOnly, timeouts                       |
| Token theft via XSS                       | 4 Tokens          | HttpOnly cookies, CSP, short access TTL                             |
| Token theft via CSRF                      | 3–4               | SameSite=Strict/Lax, double-submit token                            |
| Replay of old refresh token               | 4 Tokens          | Rotation + token-family revocation                                  |
| Malicious redirect / code interception    | 5 OAuth           | Allow-list redirect URIs, PKCE                                      |
| Assertion replay / login CSRF             | 6 SAML            | InResponseTo check, replay cache, pinned IdP certs                  |
| Phishing / AiTM account takeover          | 7 MFA             | Origin-bound passkeys over SMS/TOTP, guarded recovery               |
| Privilege escalation / IDOR               | 8 Authorization   | Deny-by-default policies, object-level checks, tenant scoping       |
| Confused deputy (third-party abuse)       | 5, 8              | Scopes, consent, audience restriction                               |

Cross-reference attack details: [XSS](../02-attacks-and-defense/20.5.2.01-xss.md) · [CSRF](../02-attacks-and-defense/20.5.2.02-csrf.md) · [SQL Injection](../02-attacks-and-defense/20.5.2.03-sql-injection.md) · [API Security Top 10](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md)

---

## Files in This Track

| File                                                                       | Lines of study                                    | Type         |
| -------------------------------------------------------------------------- | ------------------------------------------------- | ------------ |
| [20.5.1.01-auth-fundamentals.md](20.5.1.01-auth-fundamentals.md)           | Identity, credentials, crypto primitives for auth | Core concept |
| [20.5.1.02-http-basic-digest-auth.md](20.5.1.02-http-basic-digest-auth.md) | Legacy HTTP credential schemes and their limits   | Core concept |
| [20.5.1.03-api-keys.md](20.5.1.03-api-keys.md)                             | Machine-to-machine credentials done right         | Core concept |
| [20.5.1.04-sessions-cookies.md](20.5.1.04-sessions-cookies.md)             | Server-side state model                           | Core concept |
| [20.5.1.05-jwt.md](20.5.1.05-jwt.md)                                       | Stateless tokens done right                       | Core concept |
| [20.5.1.06-oauth2-oidc.md](20.5.1.06-oauth2-oidc.md)                       | Delegated identity & access                       | Core concept |
| [20.5.1.07-sso-saml-federation.md](20.5.1.07-sso-saml-federation.md)       | Enterprise federation & provisioning              | Core concept |
| [20.5.1.08-mfa-passkeys-webauthn.md](20.5.1.08-mfa-passkeys-webauthn.md)   | Strong authn: TOTP to phishing-resistant passkeys | Core concept |
| [20.5.1.09-rbac-abac.md](20.5.1.09-rbac-abac.md)                           | Authorization models                              | Core concept |
| [20.5.1.10-interview-questions.md](20.5.1.10-interview-questions.md)       | 40+ questions with follow-up traps                | Drill        |

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
- [Hayk Simonyan — Full Auth Course video: Basic, Digest, API Keys, Sessions, JWT, OAuth2, OIDC, SSO, SAML, Authorization](https://www.youtube.com/watch?v=iX8g4LqF8p8)
- [The NIST RBAC standard](https://csrc.nist.gov/projects/role-based-access-control)

---

## Navigation

[← Back to Security](../INDEX.md) · [Next: Attacks — XSS →](../02-attacks-and-defense/20.5.2.01-xss.md)

---

## Docita Anchor

Real code from [docita](https://github.com/CVamsi27/docita) - production healthcare platform (NestJS + Prisma + Postgres). Study the stages, then see them shipped:

| Stage                    | Docita evidence                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 4 · Tokens (JWT)         | `apps/api/src/shared/modules/auth/auth/jwt.strategy.ts` - passport-jwt validation with audience separation (staff vs portal vs WS)       |
| 3 · Sessions & Cookies   | `apps/api/src/shared/modules/auth/auth/auth-session.service.ts` - server-side sessions with SHA-256-hashed tokens                        |
| 2 · API Keys             | `apps/api/src/shared/modules/auth/auth/api-key.service.ts` - CSPRNG keys hashed at rest, scoped access                                   |
| 7 · MFA                  | `apps/api/src/shared/modules/auth/auth/mfa.service.ts` - otplib TOTP enrollment, QR codes, bcrypt-hashed backup codes                    |
| 8 · Authorization (RBAC) | `apps/api/src/shared/modules/auth/auth/roles.guard.ts` - @Roles gate driven by JWT role claims                                           |
| 8 · Authorization (ABAC) | `apps/api/src/shared/modules/authorization/abac-policy.registry.ts` - per-resource policies resolved by PolicyGuard + resource resolvers |

Stages 5-6 (OAuth2/OIDC social login, SAML/SCIM) and WebAuthn passkeys: _no direct docita implementation yet._
