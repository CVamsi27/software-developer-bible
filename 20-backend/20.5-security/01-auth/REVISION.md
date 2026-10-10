<!-- section: Security | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-5_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Security — Auth Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Auth Fundamentals — Identity, Credentials & Crypto Primitives

Source: [Auth Fundamentals — Identity, Credentials & Crypto Primitives](20.5.1.01-auth-fundamentals.md)

**Q:** What evidence is needed to verify a caller's identity claim?

**A:** An identity claim needs accepted evidence, such as a verified credential or a trusted issuer's validated assertion. Identification alone is not authentication.

**Q:** How do expiration, rotation and storage controls limit credential exposure?

**A:** Controls limit where a credential can leak, how long it remains useful and what it can authorize. Hashing protects stored verifiers but does not make a stolen caller credential harmless.

**Q:** Why must authentication and authorization be separate decisions?

**A:** Authentication establishes a principal; authorization decides whether that principal may perform this operation on this resource. A valid login does not establish tenant membership or ownership.

**Q:** Why does a public signature-verification key need trusted distribution even though it is not secret?

**A:** A verifier must know that the key belongs to its accepted issuer. An attacker-controlled replacement key can validate attacker-issued messages. Public verification material can be disclosed; its identity, allowed algorithms, audience and lifecycle still require validation.

**Q:** How does a webhook HMAC differ from a digital signature?

**A:** HMAC producers and verifiers share a secret, so every verifier can generate a valid MAC. A digital-signature verifier can use a public key without obtaining the private signing capability. Neither mechanism encrypts the body or supplies replay prevention by itself.

## HTTP Basic & Digest Authentication

Source: [HTTP Basic & Digest Authentication](20.5.1.02-http-basic-digest-auth.md)

**Q:** How does HTTP Basic carry credentials on a request?

**A:** Basic sends a base64-encoded username and password in Authorization. Encoding is reversible; TLS and protection of every component that handles the header provide confidentiality.

**Q:** What risks arise from repeatedly transmitting a reusable password?

**A:** Headers can leak through logs, proxies or compromised clients. Digest avoids direct password transmission but still needs TLS, nonce validation and credential-equivalent verifier protection.

**Q:** Which logout, expiration and scope controls must an application add around Basic authentication?

**A:** The application can disable accounts, revoke credentials and restrict permission scope. Basic itself supplies no standardized browser logout or token-expiry mechanism, so browser caching and server policy must be handled separately.

## API Keys

Source: [API Keys](20.5.1.03-api-keys.md)

**Q:** What principal does an API key identify, and why does that matter?

**A:** A key commonly identifies an application or service but can be tied to a user's account. Its documented principal and scope determine what authorization it can support.

**Q:** Which storage and distribution choices expose a static API key?

**A:** Source control, logs, browser bundles and unprotected client storage can expose bearer keys. Store only a verifier server-side where possible, minimize distribution and support scoped rotation and revocation.

**Q:** Why is a service key alone insufficient for delegated user authorization?

**A:** A service key does not establish the user's delegated permission or consent. Add an explicit user/delegation contract when the operation acts on behalf of a person.

## Sessions & Cookies

Source: [Sessions & Cookies](20.5.1.04-sessions-cookies.md)

**Q:** Where can a system retain state that links requests to a login?

**A:** Server-side sessions retain state behind an identifier; signed client tokens carry claims. Current account status and immediate revocation can require server state in either design.

**Q:** Why is automatic cookie delivery both useful and relevant to CSRF?

**A:** The browser can attach a matching cookie without application JavaScript. HttpOnly prevents direct script reading, but XSS can still act as the user; automatic credential delivery also requires CSRF controls.

**Q:** How do fixation and hijacking compromise a session identifier?

**A:** Fixation makes a victim use an attacker-known identifier; hijacking steals an established one. Rotate identifiers after login or privilege changes and protect transport, expiry and storage.

## JWT (JSON Web Tokens)

Source: [JWT (JSON Web Tokens)](20.5.1.05-jwt.md)

**Q:** How can a recipient validate a signed JWT without contacting a session store?

**A:** Verify protection using a trusted key and allowed algorithm, then validate issuer, audience, time and application requirements. Offline signature verification does not establish current permission to access a resource.

**Q:** Why does immediate JWT revocation require an additional mechanism?

**A:** A previously issued signed token remains cryptographically valid until its expiry. Denylists, account-version checks, introspection or other state can enforce earlier revocation; refreshing a token is a separate lifecycle.

**Q:** How do signed and encrypted JWTs differ in claim confidentiality?

**A:** Signed JWS claims are readable and protected for integrity; JWE encrypts claims under a separate contract. Keep secrets out of signed payloads and validate algorithms and keys independently of untrusted headers.

## OAuth 2.0 & OpenID Connect

Source: [OAuth 2.0 & OpenID Connect](20.5.1.06-oauth2-oidc.md)

**Q:** How does OAuth let a client obtain access without collecting the user's password?

**A:** An authorization server issues limited access under a defined grant; the client uses the access token at the resource server. The client need not collect the user's password.

**Q:** How do a client's secrecy and user-interaction capabilities affect the OAuth flow?

**A:** A browser or native public client cannot keep a client secret, while a confidential server client can. Authorization code with PKCE protects the code exchange; client credentials represents a service acting without a user grant.

**Q:** What authentication contract does OpenID Connect add to OAuth?

**A:** OIDC adds authentication assertions, notably an ID token with recipient and issuer validation. An access token authorizes resource access; it should not be treated as an interchangeable identity token.

**Q:** A callback has a matching state and returns a valid access token. Has the application established an OIDC login?

**A:** No. It must validate the ID token under the trusted issuer/client/nonce contract, map the provider subject and then create the local session. The API independently validates the access token's intended recipient and permissions.

**Q:** Does storing a credential in an HttpOnly cookie remove the need for CSRF protection?

**A:** No. JavaScript cannot read that cookie, but the browser can still attach it automatically. A backend using it must protect its state-changing requests; direct bearer-header usage has a different credential-attachment boundary.

## SSO, SAML & Federation

Source: [SSO, SAML & Federation](20.5.1.07-sso-saml-federation.md)

**Q:** Which identity risks can a shared identity provider centralize?

**A:** A shared provider centralizes authentication policy, MFA and account lifecycle. Each service still owns local sessions and authorization, so offboarding must propagate to those boundaries.

**Q:** What trust and validation rules must federated services agree on?

**A:** Agree on trusted issuers and keys, audiences, recipients, assertion time limits and replay handling. A signature without those bindings can validate an assertion intended for a different service.

**Q:** Which login and session failures remain when an identity provider is unavailable?

**A:** New authentication can fail while existing local sessions continue according to their policies. Define provider redundancy, session limits and emergency access rather than assuming every outage behaves identically.

## MFA, Passkeys & WebAuthn

Source: [MFA, Passkeys & WebAuthn](20.5.1.08-mfa-passkeys-webauthn.md)

**Q:** Why must MFA combine distinct factor categories?

**A:** Two proofs from one category are not two factors. Distinct factors can limit some independent compromise paths, but shared devices, phishing and account recovery can still correlate failures.

**Q:** How does WebAuthn's origin and relying-party binding resist phishing?

**A:** A WebAuthn assertion is bound to the relying party and client origin, which the server validates with the challenge. A phishing origin cannot simply reuse a credential for the legitimate relying party.

**Q:** What credential material does a passkey server store, and what risks remain after a breach?

**A:** The server retains public-key verification material rather than a reusable password. A breach can still expose personal data, sessions or modified registration state; passkeys do not remove those risks.

## RBAC (Role-Based Access Control)

Source: [RBAC (Role-Based Access Control)](20.5.1.09-rbac-abac.md)

**Q:** When does role membership provide a useful permission model?

**A:** Roles provide a reviewable baseline when permissions follow stable responsibilities. Add tenant or ownership checks when a role alone does not identify the permitted resource.

**Q:** When do resource or environment attributes require more than a role check?

**A:** An operation may depend on resource ownership, project membership, time or device state. Encoding every combination as a new role can create role explosion.

**Q:** How can role permissions and contextual conditions work together?

**A:** Use role permissions as a baseline and evaluate relevant resource/context conditions. Define precedence, denial behavior and trusted inputs so combining the models does not accidentally broaden access.

## ABAC (Attribute-Based Access Control)

Source: [ABAC (Attribute-Based Access Control)](20.5.1.10-abac-access-control.md)

**Q:** Which attribute sets determine an ABAC access decision?

**A:** Evaluate trusted attributes of the subject, resource, action and environment under an explicit policy. The enforcement point must apply the resulting decision to the same operation and object.

**Q:** Why do expressive policies need tests, versioning and decision diagnostics?

**A:** More combinations create more opportunities for unintended allow or deny outcomes. Version policies, test representative cases and record safe decision diagnostics without logging sensitive attributes indiscriminately.

**Q:** How can missing, stale or expensive attributes undermine authorization?

**A:** A missing attribute needs a defined failure policy; stale membership can grant outdated access. Bound lookup and evaluation time and invalidate cached decisions when relevant facts change.

## Failure Traces

Sources: [API keys](20.5.1.03-api-keys.md), [sessions](20.5.1.04-sessions-cookies.md), [JWT](20.5.1.05-jwt.md), [OAuth/OIDC](20.5.1.06-oauth2-oidc.md), [federation](20.5.1.07-sso-saml-federation.md), [MFA](20.5.1.08-mfa-passkeys-webauthn.md), [RBAC](20.5.1.09-rbac-abac.md) and [ABAC](20.5.1.10-abac-access-control.md).

**Q:** Why can a revoked API key still pass a cached guard, and what must the contract state?

**A:** A cached record may retain an earlier active state. Specify and enforce the rejection window; destructive operations may require a current check. Prefixes identify candidates and need uniqueness, while full verifiers and ownership still decide access.

**Q:** A login sets `userId` on an existing session but never regenerates it. What survives?

**A:** The pre-login bearer identifier. If an attacker knew it, authentication grants that same identifier new privileges. Regenerate after accepted credentials, save new state before responding, then reject the old ID.

**Q:** Why does a correctly signed JWT with no `exp` need to fail a profile requiring short lifetimes?

**A:** A library can validate an expiration only when it exists. The application must require expiry and other profile fields, alongside algorithm/issuer/audience/purpose/runtime shape; a type cast does not validate them.

**Q:** An OAuth callback arrives twice with the same state. What blocks the second exchange?

**A:** An atomic browser-bound transaction consume before asynchronous redemption. State, PKCE verifier and OIDC nonce have separate roles; a missing stored value must never match a missing callback value.

**Q:** The directory disabled an employee, but an existing app cookie still works. Which boundary was missed?

**A:** IdP login rejection does not destroy the SP's local session. SCIM/account changes, app session revocation or current-state checks must propagate disablement within the allowed window.

**Q:** Why should registration not look up its challenge using the new credential ID?

**A:** That credential did not exist at start. Store an expiring attempt bound to the authenticated account and browser, consume it once, then validate origin/RP/challenge/user verification and unique credential ownership.

**Q:** A role inherits itself indirectly. Is recursive permission expansion safe?

**A:** No. Detect cycles and unknown parents, bound depth and reject invalid configuration. Role names do not imply inheritance, and expanded permissions do not replace tenant/object scope.

**Q:** A request says a patient belongs to clinic A and is public. Which attributes can authorize access?

**A:** Use verified current subject data and the actual stored patient's tenant/classification/assignment. Requested attributes cannot establish authority. Constrain the subsequent operation with the same state/version to prevent a stale decision race.

## Summary

Use these prompts after the reading pass to recall the auth mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for identity and current permissions

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
