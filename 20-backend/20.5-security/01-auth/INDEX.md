# Auth - Security

> **Study time:** ≈ 2 h 9 m of reading (12 files, ~11 min average).
> The table gives the intended study order; revision and timed practice are separate activities.
> **Prerequisite:** [Encryption & Hashing](../03-hardening-and-operations/20.5.3.01-encryption.md).
>
> Authentication establishes who or what is calling. Authorization decides what that principal may do. Read the chapters in order, use the separate revision pass, then defend a design in the interview drill.

[![Files](https://img.shields.io/badge/files-12-blue)](#read-order)
[![Category](https://img.shields.io/badge/category-Auth-blue)](../INDEX.md)

## Read order

| Stage | Topic | Read | Be ready to explain | Priority |
| ----: | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | --------- |
| 0 | Foundations | [Auth fundamentals](20.5.1.01-auth-fundamentals.md) · 7 min | Identity evidence, password verifiers, random credentials, cryptographic boundaries and bounded login work | Essential |
| 1 | HTTP Basic and Digest | [Basic/Digest](20.5.1.02-http-basic-digest-auth.md) · 15 min | Header and challenge mechanics, TLS requirements, Digest verifier cost and where either scheme still fits | Important |
| 2 | API keys | [API keys](20.5.1.03-api-keys.md) · 16 min | High-entropy issuance, verifier storage, scopes, key ownership and revocation delay | Essential |
| 3 | Sessions and cookies | [Sessions/cookies](20.5.1.04-sessions-cookies.md) · 8 min | Session rotation, cookie delivery, CSRF, server expiry and store failure | Essential |
| 4 | JWT | [JWT](20.5.1.05-jwt.md) · 9 min | Token profile validation, issuer/audience, signing authority, refresh rotation and revocation limits | Essential |
| 5 | OAuth 2.0 and OIDC | [OAuth/OIDC](20.5.1.06-oauth2-oidc.md) · 13 min | Authorization Code with PKCE, delegated scopes, OIDC identity validation and browser architecture trade-offs | Essential |
| 6 | SSO, SAML and federation | [SSO/SAML](20.5.1.07-sso-saml-federation.md) · 12 min | Metadata trust, signed assertion validation, request/replay binding, local sessions and deprovisioning | Important |
| 7 | MFA, passkeys and WebAuthn | [MFA/passkeys](20.5.1.08-mfa-passkeys-webauthn.md) · 14 min | TOTP replay, phishing resistance, origin/RP validation, assurance and recovery | Important |
| 8 | RBAC | [RBAC](20.5.1.09-rbac-abac.md) · 10 min | User-role assignments, active roles, optional hierarchy/constraints and object-level checks | Essential |
| 9 | ABAC | [ABAC](20.5.1.10-abac-access-control.md) · 9 min | Attribute authority/freshness, policy decision and enforcement, composition and failure behavior | Essential |
| — | Revision | [Auth revision](REVISION.md) | Recall every mechanism and explain which boundary fails under changed conditions | Essential |
| 10 | Interview practice | [40 interview questions](20.5.1.11-interview-questions.md) | Trace complete login, token, recovery and authorization flows; defend trade-offs and failure handling | Essential |

## Carry these decisions through the track

For every design, answer four questions:

1. **Who is the principal?** A human, a workload, or a client acting for a user? Pick a credential that proves that identity and authority.
2. **Where does current state live?** State which parts can be checked offline, how account or permission changes take effect, and the maximum revocation delay.
3. **What resource is protected?** A role or scope may grant a capability; the data operation must still enforce current ownership, tenant and workflow rules.
4. **How does the client carry proof?** Browser cookies are sent automatically and need CSRF controls. JavaScript-held bearer tokens face XSS exposure. Native and service clients have different storage and rotation boundaries.

### Session, JWT or hybrid?

| Design | Request-time check | Revocation boundary | Fits when |
| ------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| Server-side session | Shared session state, often through an opaque cookie | Delete or invalidate server state; caches and in-flight requests determine propagation | The app needs central session control and immediate current-state decisions |
| Self-contained JWT | Trusted key plus a required issuer-specific token profile | Offline validators accept it until expiry unless they perform an online/current-state check | Independent verification is useful and its validity window is acceptable |
| Hybrid access and refresh | Short-lived access-token policy plus stateful refresh grant | Revoke the refresh grant; existing access tokens remain valid until rejected by expiry or current-state policy | Renewal needs central state while normal API checks can use a bounded access credential |

Refresh rotation protects the renewal chain; it does not automatically revoke already-issued access tokens. Cookie use and bearer-token format are independent choices: choose transport from the client threat model.

## Connect the concepts to a production codebase

These Docita paths and the study project provide examples of implementation patterns. Verify the current checkout before claiming that a feature is deployed: code presence alone does not prove configuration, tests, rollout or operational behavior.

| Concern | Example path |
| ---------------------------- | ------------------------------------------------------------------- |
| JWT audiences and strategies | `apps/api/src/shared/modules/auth/auth/jwt.strategy.ts` |
| Server-side sessions | `apps/api/src/shared/modules/auth/auth/auth-session.service.ts` |
| API-key verification | `apps/api/src/shared/modules/auth/auth/api-key.service.ts` |
| MFA and recovery | `apps/api/src/shared/modules/auth/auth/mfa.service.ts` |
| Role enforcement | `apps/api/src/shared/modules/auth/auth/roles.guard.ts` |
| Attribute policy | `apps/api/src/shared/modules/authorization/abac-policy.registry.ts` |

The study example does not establish OAuth/OIDC, SAML/SCIM or passkey implementation. Check the repository before making claims about those features.

## Finish the track

Use [REVISION.md](REVISION.md) after reading to retrieve the main mechanisms without reopening the examples. Then answer the [interview questions](20.5.1.11-interview-questions.md) aloud: explain the trust boundary first, then state how the design handles revocation, outages and unauthorized resource access.

[← Back to Security](../INDEX.md) · [Next: Attacks and Defense — XSS →](../02-attacks-and-defense/20.5.2.01-xss.md)
