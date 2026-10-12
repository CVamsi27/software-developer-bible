# Auth - Security

> **Study time:** ≈ 2 h 13 m of reading (12 files, ~11 min average).
> **Planning:** The stage blocks below estimate study and practice time; chapter badges and the total above report reading time only. Revision and timed practice are separate stages.
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

| # | Stage | File | Planned block | You can defend… | Role priority | General importance |
| --: | ------- | ------ | ------ | ------------------ | --- | --- |
| 0 | Foundations | [20.5.1.01-auth-fundamentals.md](20.5.1.01-auth-fundamentals.md) | 45 min | Hashing vs encryption, password storage (Argon2id), CSPRNG, authenticated transport and bounded login work | Essential | Foundational |
| 1 | HTTP Basic & Digest Auth | [20.5.1.02-http-basic-digest-auth.md](20.5.1.02-http-basic-digest-auth.md) | 30 min | Authorization header mechanics, Base64-over-TLS only, Digest challenge-response and its verifier/TLS trade-off, when Basic is still OK | Important | Specialized |
| 2 | API Keys | [20.5.1.03-api-keys.md](20.5.1.03-api-keys.md) | 30 min | Key generation with CSPRNG, hashing keys at rest, prefix schemes (`sk_live_`), rotation grace windows, per-key scopes | Essential | Foundational |
| 3 | Sessions & Cookies | [20.5.1.04-sessions-cookies.md](20.5.1.04-sessions-cookies.md) | 45 min | Cookie flags, server-side state, fixation/hijacking, timeouts | Essential | Foundational |
| 4 | Tokens (JWT) | [20.5.1.05-jwt.md](20.5.1.05-jwt.md) | 60 min | JWT anatomy, HS256 vs RS256, storage trade-offs, refresh rotation + family revocation | Essential | Foundational |
| 5 | Federation (OAuth2 / OIDC) | [20.5.1.06-oauth2-oidc.md](20.5.1.06-oauth2-oidc.md) | 60 min | Authorization Code/PKCE, Client Credentials, Device Authorization, OIDC identity validation, refresh/revocation, and BFF vs token-mediating vs browser-client trade-offs | Essential | Foundational |
| 6 | SSO / SAML / Federation | [20.5.1.07-sso-saml-federation.md](20.5.1.07-sso-saml-federation.md) | 45 min | Authenticated metadata, signed response/assertion checks, SP/IdP-initiated risks, request and assertion replay, local sessions and SCIM lifecycle | Important | Specialized |
| 7 | MFA / Passkeys / WebAuthn | [20.5.1.08-mfa-passkeys-webauthn.md](20.5.1.08-mfa-passkeys-webauthn.md) | 45 min | TOTP replay limits, PSTN risks, WebAuthn challenge/origin/RP ID checks, sync boundaries, NIST AAL requirements and recovery | Important | Specialized |
| 8 | Authorization (RBAC / ABAC) | [20.5.1.09-rbac-abac.md](20.5.1.09-rbac-abac.md) | 45 min | Core role assignments and sessions, optional hierarchy/constraints, capability versus object/tenant checks | Essential | Foundational |
| 9 | ABAC Deep Dive | [20.5.1.10-abac-access-control.md](20.5.1.10-abac-access-control.md) | 35 min | Attribute provenance and freshness, PIP/PDP/PEP, policy composition, evaluation failures and tests | Essential | Foundational |
| — | Revision | [REVISION.md](REVISION.md) | Recall pass | Trace each mechanism and change one trust/lifetime condition | Essential | Foundational |
| 10 | Interview Drills | [20.5.1.11-interview-questions.md](20.5.1.11-interview-questions.md) | Timed practice | Trace the boundary, then change authority or lifetime | Essential | Foundational |

---

## Compare the Required Contracts

In senior design discussions, the recurring task is to justify the authentication or authorization contract against the system’s risks and constraints.

### Sessions vs self-contained JWTs vs hybrid credentials

| Dimension | Server Sessions | Self-contained JWT (offline validation) | Hybrid (access token + refresh credential) |
| ----------------- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| State | Server-side store (Redis/DB) | Key/claim trust configuration; revocation may add state | Refresh state; access policy may add current checks |
| Revocation | Store deletion plus cache/in-flight rejection window | Hard (wait for expiry / denylist) | Refresh family revocation; access tokens remain valid until policy rejects |
| Latency | Store lookup per request | Offline signature check possible | Offline signature check possible; policy decides current lookups |
| Horizontal scale | Needs shared store or sticky | Independent verifiers need key/policy distribution | Independent verifiers plus shared refresh authority |
| CSRF exposure | Yes (cookie-based) | No if header-borne | Depends on transport (see below) |
| Logout everywhere | Revoke all active sessions under store policy | Expiry/current state/denylist boundary | Revoke refresh grants and define access rejection |
| Fits when | The service needs central revocation or current server-side state | Independent verification is useful and the accepted offline-validity window is explicit | Renewal needs central state while request checks can tolerate the access-token policy |

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
| --------- | ------------------------------------------------------------- | ----------------------------------------------------- | -------------------------------------------------------------------- |
| **RBAC** | "Which permissions are active for this user in this session?" | `editor` may update articles | Role assignment, activation and permission review |
| **ABAC** | "Which trusted facts make this operation valid?" | Same tenant, sufficient clearance and assigned doctor | Attribute authority, freshness and policy tests |
| **ReBAC** | "What relationship connects this subject to the resource?" | Alice can edit a document shared with her team | Relationship storage, evaluation and consistency |

**Decision condition:** Select the model from the facts the decision must depend on. These models can be used alone or combined. A role capability does not by itself establish that a particular object or tenant is in scope.

---

## Decision Tree — "Design auth for my app"

```text
Who is authorizing the request?
├── A user
│   ├── Interactive browser/native client → Authorization Code with PKCE; use OIDC when the client needs a login identity assertion
│   ├── Input-constrained device → Device Authorization Grant with a user-reviewed client and scope
│   └── Browser app with its own backend → prefer a BFF for sensitive data when feasible; otherwise document token exposure from a token-mediating backend or browser client
└── The application or service itself → scoped API key or OAuth Client Credentials; choose by attribution, lifecycle and revocation needs

Does access need immediate current-state checks? → use server state or introspection where required; an offline token has an explicit expiry and revocation window.
Across services → each service authenticates direct callers or trusted identity propagation and enforces its own object/tenant policy; a gateway may add coarse checks.
```

---

## Implementation Recipes (NestJS-shaped)

These examples use NestJS-shaped names; guards such as `ApiKeyGuard` and decorators such as `@RequirePolicy` are application code, not built-in auth guarantees. Name the enforcement point and its contract:

| Concept | Enforcement point | File to study | Role priority | General importance |
| ---------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------- | ------------------ |
| Credential check + hash verify | Credential verifier using maintained password hashing | [fundamentals](20.5.1.01-auth-fundamentals.md) | Essential | Foundational |
| Static credential gate (Basic) | BasicAuthGuard validates encoding + provisioned Argon2 verifier | [Basic/Digest](20.5.1.02-http-basic-digest-auth.md) | Important | Specialized |
| Machine-to-machine identity | ApiKeyGuard: prefix lookup -> SHA-256 compare -> scopes | [API Keys](20.5.1.03-api-keys.md) | Essential | Foundational |
| Session issue/rotate | Session middleware + store TTL; regenerate the ID on login or privilege elevation | [sessions](20.5.1.04-sessions-cookies.md) | Essential | Foundational |
| Token sign/verify | Maintained validator with pinned algorithms, trusted issuer/audience and controlled key discovery | [JWT](20.5.1.05-jwt.md) | Essential | Foundational |
| Refresh rotation + reuse detection | Atomic consume + successor persist; grant replay/lost-response policy | [JWT](20.5.1.05-jwt.md) | Essential | Foundational |
| Social login | Maintained OIDC client, authorization code + PKCE and issuer/client validation | [OAuth2/OIDC](20.5.1.06-oauth2-oidc.md) | Essential | Foundational |
| Enterprise SSO login | Tenant-pinned SAML validator -> stable subject mapping -> regenerated local session | [SSO/SAML](20.5.1.07-sso-saml-federation.md) | Important | Specialized |
| Second factor ceremony | OTP replay-aware verifier or account/browser-bound WebAuthn ceremony | [MFA/Passkeys](20.5.1.08-mfa-passkeys-webauthn.md) | Important | Specialized |
| Role gate | `@Roles('admin')` + RolesGuard | [RBAC/ABAC](20.5.1.09-rbac-abac.md) | Essential | Foundational |
| Policy gate | `@RequirePolicy(resource, action)` + PEP/PDP with trusted stored attributes | [ABAC](20.5.1.10-abac-access-control.md) | Essential | Foundational |
| Tenant isolation | Resolve active membership, bind request context, scope data access; consider RLS as a backstop | [API security](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md) | Essential | Foundational |

> **Senior signal:** say where each control lives *in the request pipeline* (middleware → guard → interceptor → service → query layer) and which layer catches what a previous layer missed (defense in depth).

---

## Attack Surface Checklist (what each stage defends)

| Attack | Defended in stage | Key controls |
| ----------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------- |
| Password cracking / credential stuffing | 0 Fundamentals | Argon2id/bcrypt, rate limiting, breach-password checks |
| Credential interception on plaintext HTTP | 1 Basic/Digest | TLS everywhere, HSTS, proxy basic-auth only over TLS |
| API key leakage / abuse | 2 API Keys | Hashed at rest, narrow scopes, risk controls where suitable, dual-key rotation, revocation runbook |
| Session hijacking / fixation | 3 Sessions | Rotate ID on login or privilege elevation, Secure/HttpOnly, timeouts |
| Token theft via XSS | 4 Tokens | Prevent unsafe rendering; HttpOnly limits direct reads but not authenticated injected actions |
| Cookie-authenticated unwanted actions | 3–4 | SameSite policy plus synchronizer token or signed session-bound double-submit contract |
| Replay of old refresh token | 4 Tokens | Rotation + token-family revocation |
| Malicious redirect / code interception | 5 OAuth | Allow-list redirect URIs, PKCE |
| Assertion replay / login CSRF | 6 SAML | SP-initiated request correlation, atomic assertion replay checks, explicit unsolicited-login policy, trusted IdP keys |
| Phishing / AiTM account takeover | 7 MFA | Phishing-resistant WebAuthn, guarded recovery, tightly controlled phishable fallbacks |
| Privilege escalation / IDOR | 8 Authorization | Deny-by-default policies, object-level checks, tenant scoping |
| Confused deputy (third-party abuse) | 5, 8 | Scopes, consent, audience restriction |

Cross-reference attack details: [XSS](../02-attacks-and-defense/20.5.2.01-xss.md) · [CSRF](../02-attacks-and-defense/20.5.2.02-csrf.md) · [SQL Injection](../02-attacks-and-defense/20.5.2.03-sql-injection.md) · [API Security Top 10](../02-attacks-and-defense/20.5.2.04-api-security-best-practices.md)

---

## Files in This Track

| File | Lines of study | Type | Role priority | General importance |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------ | ------------- | ------------------ |
| [20.5.1.01-auth-fundamentals.md](20.5.1.01-auth-fundamentals.md) | Identity, credentials, crypto primitives for auth | Core concept | Essential | Foundational |
| [20.5.1.02-http-basic-digest-auth.md](20.5.1.02-http-basic-digest-auth.md) | Legacy HTTP credential schemes and their limits | Core concept | Important | Specialized |
| [20.5.1.03-api-keys.md](20.5.1.03-api-keys.md) | Machine-to-machine credentials done right | Core concept | Essential | Foundational |
| [20.5.1.04-sessions-cookies.md](20.5.1.04-sessions-cookies.md) | Server-side state model | Core concept | Essential | Foundational |
| [20.5.1.05-jwt.md](20.5.1.05-jwt.md) | Self-contained tokens and their validation limits | Core concept | Essential | Foundational |
| [20.5.1.06-oauth2-oidc.md](20.5.1.06-oauth2-oidc.md) | Delegated identity & access | Core concept | Essential | Foundational |
| [20.5.1.07-sso-saml-federation.md](20.5.1.07-sso-saml-federation.md) | Enterprise federation & provisioning | Core concept | Important | Specialized |
| [20.5.1.08-mfa-passkeys-webauthn.md](20.5.1.08-mfa-passkeys-webauthn.md) | TOTP, WebAuthn verification, sync boundaries, assurance and recovery | Core concept | Important | Specialized |
| [20.5.1.09-rbac-abac.md](20.5.1.09-rbac-abac.md) | Authorization models | Core concept | Essential | Foundational |
| [20.5.1.10-abac-access-control.md](20.5.1.10-abac-access-control.md) | Trusted attributes, applicability and enforcement | Core concept | Essential | Foundational |
| [REVISION.md](REVISION.md) | Mechanism recall before timed practice | Revision | Essential | Foundational |
| [20.5.1.11-interview-questions.md](20.5.1.11-interview-questions.md) | 40 questions with follow-up traps | Drill | Essential | Foundational |

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
| 9 · Authorization (ABAC) | `apps/api/src/shared/modules/authorization/abac-policy.registry.ts` - per-resource policies resolved by PolicyGuard + resource resolvers |

Stages 5-6 (OAuth2/OIDC social login, SAML/SCIM) and WebAuthn passkeys: _not established by this study table; verify the current repository before claiming presence or absence._

## Section Revision

After the learning chapters, use the [separate revision drill](REVISION.md) to check recall before interview practice.
