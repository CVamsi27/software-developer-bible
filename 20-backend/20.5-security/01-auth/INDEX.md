# Auth - Security

> **Study time:** ≈ 2 h 12 m of reading (12 files, ~11 min average).
> **The complete authentication & authorization learning track — ten concept stages plus separate practice.** Read them **in order**, each builds on the previous; finish with the interview drills.
>
> Part of [Security](../INDEX.md) · Prerequisite: [Encryption & Hashing](../03-hardening-and-operations/20.5.3.01-encryption.md)

[![Files](https://img.shields.io/badge/files-12-blue)](#files-in-this-track)
[![Category](https://img.shields.io/badge/category-Auth-blue)](../INDEX.md)

---

## The Flow — Read Top to Bottom

```text
0 Foundations -> 1 Basic/Digest -> 2 API keys -> 3 Sessions -> 4 JWT
5 OAuth/OIDC -> 6 SAML/SCIM -> 7 MFA/passkeys -> 8 RBAC -> 9 ABAC
Then: REVISION -> 10 Interview drills
```

---

## Read the Mechanisms, Then Practice

Stage numbers are study order (`0`-`10`, including practice), not file IDs — read top to bottom.

| # | Stage | File | Time | You can defend… | Role priority | General importance |
| --: | ------- | ------ | ------ | ------------------ | --- | --- |
| 0 | Foundations | [20.5.1.01-auth-fundamentals.md](20.5.1.01-auth-fundamentals.md) | 45 min | Hashing vs encryption, password storage (Argon2id), CSPRNG, why TLS before anything else | Essential | Foundational |
| 1 | HTTP Basic & Digest Auth | [20.5.1.02-http-basic-digest-auth.md](20.5.1.02-http-basic-digest-auth.md) | 30 min | Authorization header mechanics, Base64-over-TLS only, Digest challenge-response and its verifier/TLS trade-off, when Basic is still OK | Important | Specialized |
| 2 | API Keys | [20.5.1.03-api-keys.md](20.5.1.03-api-keys.md) | 30 min | Key generation with CSPRNG, hashing keys at rest, prefix schemes (`sk_live_`), rotation grace windows, per-key scopes | Essential | Foundational |
| 3 | Sessions & Cookies | [20.5.1.04-sessions-cookies.md](20.5.1.04-sessions-cookies.md) | 45 min | Cookie flags, server-side state, fixation/hijacking, timeouts | Essential | Foundational |
| 4 | Tokens (JWT) | [20.5.1.05-jwt.md](20.5.1.05-jwt.md) | 60 min | JWT anatomy, HS256 vs RS256, storage trade-offs, refresh rotation + family revocation | Essential | Foundational |
| 5 | Federation (OAuth2 / OIDC) | [20.5.1.06-oauth2-oidc.md](20.5.1.06-oauth2-oidc.md) | 60 min | All OAuth grants, PKCE, OIDC vs OAuth, scopes, social login | Essential | Foundational |
| 6 | SSO / SAML / Federation | [20.5.1.07-sso-saml-federation.md](20.5.1.07-sso-saml-federation.md) | 45 min | One IdP session many SPs, SAML 2.0 flows (SP-/IdP-initiated), assertions & signing certs, SAML vs OIDC, SCIM + JIT provisioning | Important | Specialized |
| 7 | MFA / Passkeys / WebAuthn | [20.5.1.08-mfa-passkeys-webauthn.md](20.5.1.08-mfa-passkeys-webauthn.md) | 45 min | TOTP mechanics (RFC 6238), SMS/SIM-swap weakness, WebAuthn ceremonies, passkey sync, AAL levels, recovery as weakest link | Important | Specialized |
| 8 | Authorization (RBAC / ABAC) | [20.5.1.09-rbac-abac.md](20.5.1.09-rbac-abac.md) | 45 min | RBAC vs ABAC vs ReBAC, scopes vs roles, policy engines, deny-by-default | Essential | Foundational |
| 9 | ABAC Deep Dive | [20.5.1.10-abac-access-control.md](20.5.1.10-abac-access-control.md) | 35 min | Attribute-based policies, deny-overrides, policy engines, testing ABAC | Essential | Foundational |
| — | Revision | [REVISION.md](REVISION.md) | Recall pass | Trace each mechanism and change one trust/lifetime condition | Essential | Foundational |
| 10 | Interview Drills | [20.5.1.11-interview-questions.md](20.5.1.11-interview-questions.md) | Timed practice | Trace the boundary, then change authority or lifetime | Essential | Foundational |

---

## Compare the Required Contracts

Every senior auth interview is a variation of one question: **"which model, and why?"**

### Sessions vs JWT vs Hybrid

| Dimension | Server Sessions | Stateless JWT | Hybrid (access JWT + refresh) |
| ----------------- | ---------------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------- |
| State | Server-side store (Redis/DB) | Key/claim trust configuration; revocation may add state | Refresh state; access policy may add current checks |
| Revocation | Store deletion plus cache/in-flight rejection window | Hard (wait for expiry / denylist) | Refresh family revocation; access tokens remain valid until policy rejects |
| Latency | Store lookup per request | Offline signature check possible | Offline signature check possible; policy decides current lookups |
| Horizontal scale | Needs shared store or sticky | Independent verifiers need key/policy distribution | Independent verifiers plus shared refresh authority |
| CSRF exposure | Yes (cookie-based) | No if header-borne | Depends on transport (see below) |
| Logout everywhere | Revoke all active sessions under store policy | Expiry/current state/denylist boundary | Revoke refresh grants and define access rejection |
| Best for | Traditional web apps, banking | Machine-to-machine, short-lived APIs | Where its state and offline exposure contract fits |

**Decision condition:** Refresh rotation secures the renewal chain; it does not revoke every existing access token. Choose access expiry and online rejection checks from the allowed exposure window.

### Where do you put the token?

| Storage | Script exposure | Automatic request delivery | Required controls |
| ------------------ | ------------------------------------------------ | --------------------------- | -------------------------------------------------------------------- |
| `localStorage` | XSS can read and persistently steal tokens | No | Minimize lifetime and address XSS; unsuitable for long-lived secrets |
| JS-readable cookie | XSS can read it | Yes within cookie rules | Both XSS and CSRF defenses |
| HttpOnly cookie | Direct script reads blocked; XSS can still act | Yes within cookie rules | Secure transport, cookie scope, CSRF/origin policy |
| Memory only | Active XSS can access/use it; reload discards it | Application supplies header | Secure renewal/session design and XSS defenses |

### Authorization models

| Model | Question it answers | Example | Cost |
| --------- | ------------------------------------------------------------ | ----------------------------------------------------- | ----------------------------------------- |
| **RBAC** | "What is your role?" | Nurse can edit charts | Coarse; role explosion at scale |
| **ABAC** | "What is true about you, the resource, and the environment?" | Doctor may read patient X *if assigned*, during shift | Fine-grained; needs policy engine + tests |
| **ReBAC** | "What is your relationship to the resource?" | Alice is editor of doc 42 (Google Zanzibar style) | Powerful; heavy infra (SpiceDB/OpenFGA) |

**Decision condition:** RBAC fits stable role permissions, ABAC evaluates trusted object/environment attributes, and ReBAC models sharing relationships. Choose the checks required by the actual resource policy; role membership alone cannot establish access to every object.

---

## Decision Tree — "Design auth for my app"

```text
Browser-only app?
├── Yes → Session cookie (HttpOnly, Secure, SameSite=Lax) or hybrid w/ refresh rotation
│         └── Regulated data (health/fintech)? → add MFA, audit log, absolute session timeout
└── SPA / mobile / API consumers?
    ├── First-party only → access JWT (15 min) + rotating refresh (httpOnly cookie), family revocation
    ├── "Login with provider"? → OIDC where supported; GitHub OAuth login has a provider-specific user API contract
    └── Third-party devs calling your API → API keys (server-side) or OAuth client-credentials;
        user-scoped third-party access → full OAuth 2.0 authorization-code flow
Multi-service backend?
└── Gateway validates evidence; services authenticate the propagation boundary and enforce object/tenant policy
```

---

## Implementation Recipes (NestJS-shaped)

The concepts above map to concrete guards/pipes. In interviews, name the enforcement point:

| Concept | Enforcement point | File to study | Role priority | General importance |
| ---------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------- | ------------------ |
| Credential check + hash verify | Credential verifier using maintained password hashing | [fundamentals](20.5.1.01-auth-fundamentals.md) | Essential | Foundational |
| Static credential gate (Basic) | BasicAuthGuard validates encoding + provisioned Argon2 verifier | [Basic/Digest](20.5.1.02-http-basic-digest-auth.md) | Important | Specialized |
| Machine-to-machine identity | ApiKeyGuard: prefix lookup -> SHA-256 compare -> scopes | [API Keys](20.5.1.03-api-keys.md) | Essential | Foundational |
| Session issue/rotate | Session middleware + store TTL | [sessions](20.5.1.04-sessions-cookies.md) | Essential | Foundational |
| Token sign/verify | JwtStrategy (Passport), RS256 via JWKS | [JWT](20.5.1.05-jwt.md) | Essential | Foundational |
| Refresh rotation + reuse detection | Atomic consume + successor persist; grant replay/lost-response policy | [JWT](20.5.1.05-jwt.md) | Essential | Foundational |
| Social login | Passport Google strategy, auth-code + PKCE | [OAuth2/OIDC](20.5.1.06-oauth2-oidc.md) | Essential | Foundational |
| Enterprise SSO login | Tenant-pinned SAML validator -> stable subject mapping -> regenerated local session | [SSO/SAML](20.5.1.07-sso-saml-federation.md) | Important | Specialized |
| Second factor ceremony | OTP replay-aware verifier or account/browser-bound WebAuthn ceremony | [MFA/Passkeys](20.5.1.08-mfa-passkeys-webauthn.md) | Important | Specialized |
| Role gate | `@Roles('admin')` + RolesGuard | [RBAC/ABAC](20.5.1.09-rbac-abac.md) | Essential | Foundational |
| Policy gate | `@RequirePolicy(resource, action)` + PEP/PDP with trusted stored attributes | [ABAC](20.5.1.10-abac-access-control.md) | Essential | Foundational |
| Tenant isolation | Tenant interceptor sets context every request; DB-level RLS as backstop | [API security](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) | Essential | Foundational |

> **Senior signal:** say where each control lives *in the request pipeline* (middleware → guard → interceptor → service → query layer) and which layer catches what a previous layer missed (defense in depth).

---

## Attack Surface Checklist (what each stage defends)

| Attack | Defended in stage | Key controls |
| ----------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------- |
| Password cracking / credential stuffing | 0 Fundamentals | Argon2id/bcrypt, rate limiting, breach-password checks |
| Credential interception on plaintext HTTP | 1 Basic/Digest | TLS everywhere, HSTS, proxy basic-auth only over TLS |
| API key leakage / abuse | 2 API Keys | Hashed at rest, scopes, IP binding, dual-key rotation, leak runbook |
| Session hijacking / fixation | 3 Sessions | Rotate ID on login, Secure/HttpOnly, timeouts |
| Token theft via XSS | 4 Tokens | Prevent unsafe rendering; HttpOnly limits direct reads but not authenticated injected actions |
| Cookie-authenticated unwanted actions | 3–4 | SameSite policy plus synchronizer token or signed session-bound double-submit contract |
| Replay of old refresh token | 4 Tokens | Rotation + token-family revocation |
| Malicious redirect / code interception | 5 OAuth | Allow-list redirect URIs, PKCE |
| Assertion replay / login CSRF | 6 SAML | InResponseTo check, replay cache, pinned IdP certs |
| Phishing / AiTM account takeover | 7 MFA | Origin-bound passkeys over SMS/TOTP, guarded recovery |
| Privilege escalation / IDOR | 8 Authorization | Deny-by-default policies, object-level checks, tenant scoping |
| Confused deputy (third-party abuse) | 5, 8 | Scopes, consent, audience restriction |

Cross-reference attack details: [XSS](../02-attacks-and-defense/20.5.2.01-xss.md) · [CSRF](../02-attacks-and-defense/20.5.2.02-csrf.md) · [SQL Injection](../02-attacks-and-defense/20.5.2.03-sql-injection.md) · [API Security Top 10](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md)

---

## Files in This Track

| File | Lines of study | Type | Role priority | General importance |
| -------------------------------------------------------------------------- | ------------------------------------------------- | ------------ | ------------- | ------------------ |
| [20.5.1.01-auth-fundamentals.md](20.5.1.01-auth-fundamentals.md) | Identity, credentials, crypto primitives for auth | Core concept | Essential | Foundational |
| [20.5.1.02-http-basic-digest-auth.md](20.5.1.02-http-basic-digest-auth.md) | Legacy HTTP credential schemes and their limits | Core concept | Important | Specialized |
| [20.5.1.03-api-keys.md](20.5.1.03-api-keys.md) | Machine-to-machine credentials done right | Core concept | Essential | Foundational |
| [20.5.1.04-sessions-cookies.md](20.5.1.04-sessions-cookies.md) | Server-side state model | Core concept | Essential | Foundational |
| [20.5.1.05-jwt.md](20.5.1.05-jwt.md) | Stateless tokens done right | Core concept | Essential | Foundational |
| [20.5.1.06-oauth2-oidc.md](20.5.1.06-oauth2-oidc.md) | Delegated identity & access | Core concept | Essential | Foundational |
| [20.5.1.07-sso-saml-federation.md](20.5.1.07-sso-saml-federation.md) | Enterprise federation & provisioning | Core concept | Important | Specialized |
| [20.5.1.08-mfa-passkeys-webauthn.md](20.5.1.08-mfa-passkeys-webauthn.md) | Strong authn: TOTP to phishing-resistant passkeys | Core concept | Important | Specialized |
| [20.5.1.09-rbac-abac.md](20.5.1.09-rbac-abac.md) | Authorization models | Core concept | Essential | Foundational |
| [20.5.1.10-abac-access-control.md](20.5.1.10-abac-access-control.md) | Trusted attributes, applicability and enforcement | Core concept | Essential | Foundational |
| [REVISION.md](REVISION.md) | Mechanism recall before timed practice | Revision | Essential | Foundational |
| [20.5.1.11-interview-questions.md](20.5.1.11-interview-questions.md) | 40+ questions with follow-up traps | Drill | Essential | Foundational |

---

## References & Learn More

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [RFC 6749 — OAuth 2.0 Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [RFC 7519 — JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [OAuth 2.0 Security Best Current Practice — RFC9700](https://datatracker.ietf.org/doc/html/rfc9700)
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

The Docita study material points to these NestJS/Prisma authentication modules. Confirm the current checkout, wiring and deployed configuration before describing a path as production evidence:

| Stage | Docita evidence |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 4 · Tokens (JWT) | `apps/api/src/shared/modules/auth/auth/jwt.strategy.ts` - passport-jwt validation with audience separation (staff vs portal vs WS) |
| 3 · Sessions & Cookies | `apps/api/src/shared/modules/auth/auth/auth-session.service.ts` - server-side sessions with SHA-256-hashed tokens |
| 2 · API Keys | `apps/api/src/shared/modules/auth/auth/api-key.service.ts` - CSPRNG keys hashed at rest, scoped access |
| 7 · MFA | `apps/api/src/shared/modules/auth/auth/mfa.service.ts` - otplib TOTP enrollment, QR codes, bcrypt-hashed backup codes |
| 8 · Authorization (RBAC) | `apps/api/src/shared/modules/auth/auth/roles.guard.ts` - @Roles gate driven by JWT role claims |
| 8 · Authorization (ABAC) | `apps/api/src/shared/modules/authorization/abac-policy.registry.ts` - per-resource policies resolved by PolicyGuard + resource resolvers |

Stages 5-6 (OAuth2/OIDC social login, SAML/SCIM) and WebAuthn passkeys: _not established by this study table; verify the current repository before claiming presence or absence._

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
