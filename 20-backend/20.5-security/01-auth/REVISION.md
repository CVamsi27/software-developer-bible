<!-- section: Security | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-7_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Security — Auth Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Auth Fundamentals — Identity, Credentials & Crypto Primitives

Source: [Auth Fundamentals — Identity, Credentials & Crypto Primitives](20.5.1.01-auth-fundamentals.md)

**Q:** What evidence is needed to verify a caller's identity claim?

**A:** An identity claim needs accepted evidence, such as a verified credential or a trusted issuer's validated assertion. Identification alone is not authentication.

**Q:** Why store an encoded Argon2id verifier instead of a fast digest or encrypted password?

**A:** A unique salt and configurable memory/time cost make each offline password guess expensive; the encoded parameters also let the service raise its policy and rehash after successful login. Encryption is reversible, while a fast digest makes guesses cheap.

Source: [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) · [RFC 9106 — Argon2](https://datatracker.ietf.org/doc/html/rfc9106)

**Q:** How do expiration, rotation and storage controls limit credential exposure?

**A:** Controls limit where a credential can leak, how long it remains useful and what it can authorize. Hashing protects stored verifiers but does not make a stolen caller credential harmless.

**Q:** How should a service limit password-verification work without weakening its hash policy?

**A:** Bound input and attempts before expensive verification, use the library's asynchronous API with bounded concurrency, and combine account-oriented and network signals. Avoid permanent lockout that an attacker can trigger.

Source: [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

**Q:** Why must authentication and authorization be separate decisions?

**A:** Authentication establishes a principal; authorization decides whether that principal may perform this operation on this resource. A valid login does not establish tenant membership or ownership.

**Q:** Why does a public signature-verification key need trusted distribution even though it is not secret?

**A:** A verifier must know that the key belongs to its accepted issuer. An attacker-controlled replacement key can validate attacker-issued messages. Public verification material can be disclosed; its identity, allowed algorithms, audience and lifecycle still require validation.

**Q:** How does a webhook HMAC differ from a digital signature?

**A:** HMAC producers and verifiers share a secret, so every verifier can generate a valid MAC. A digital-signature verifier can use a public key without obtaining the private signing capability. Neither mechanism encrypts the body or supplies replay prevention by itself.

**Q:** How do API keys, JWTs and OAuth differ?

**A:** An API key is a credential, JWT is a token format, and OAuth is an authorization framework. A system can issue a JWT through OAuth, but the terms describe different parts of the design.

Source: [API keys](20.5.1.03-api-keys.md) · [OAuth 2.0](20.5.1.06-oauth2-oidc.md)

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

**Q:** What does storing a JWT in an HttpOnly cookie protect, and which risk remains?

**A:** HttpOnly prevents direct JavaScript reads, but the browser attaches the cookie automatically, so unsafe requests still need CSRF protection. Active XSS can also issue authenticated requests through the victim's browser.

Source: [JWT browser storage](20.5.1.05-jwt.md) · [CSRF](../02-attacks-and-defense/20.5.2.02-csrf.md)

## OAuth 2.0 & OpenID Connect

Source: [OAuth 2.0 & OpenID Connect](20.5.1.06-oauth2-oidc.md)

**Q:** How does OAuth let a client obtain access without collecting the user's password?

**A:** An authorization server issues limited access under a defined grant; the client uses the access token at the resource server. The client need not collect the user's password.

**Q:** How do a client's secrecy and user-interaction capabilities affect the OAuth flow?

**A:** A browser or native public client cannot keep a client secret, while a confidential server client can. Authorization Code with PKCE protects the code exchange; Client Credentials represents a service acting without a user grant. RFC 9700 says the Resource Owner Password Credentials grant MUST NOT be used and recommends against the Implicit grant because access tokens in authorization responses are exposed to leakage and replay.

**Q:** How do browser OAuth architectures trade token exposure against backend work?

**A:** A BFF holds access and refresh tokens and proxies every resource request; the browser gets a session cookie, so CSRF protection and proxy operations remain. A token-mediating backend keeps refresh credentials but returns access tokens to JavaScript, where active XSS can use or steal them. A browser-only client is public and handles the flow itself, so it cannot keep a secret and tokens remain exposed to browser code. RFC 10017 ranks these patterns by security and strongly recommends a BFF for business, sensitive and personal-data applications.

Source: [OAuth 2.0 for Browser-Based Applications, RFC 10017](https://datatracker.ietf.org/doc/html/rfc10017)

**Q:** When should a client use the Device Authorization Grant, and what must its polling loop handle?

**A:** Use it for an input-constrained client that cannot conveniently complete a browser redirect. Show the user code and verification URI, protect the `device_code`, wait at least the configured interval (five seconds by default), add five seconds after `slow_down`, reduce polling after a connection timeout, and stop on any token-endpoint error other than `authorization_pending` or `slow_down`. The user should review which client and permissions are being approved.

Source: [OAuth 2.0 Device Authorization Grant, RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)

**Q:** What do OAuth `state`, PKCE and OIDC `nonce` bind?

**A:** State correlates a browser-bound authorization response and may carry application state; PKCE binds code redemption to the client transaction; OIDC nonce binds the ID token to the authentication request and helps detect replay. A conforming server-enforced PKCE flow can also provide CSRF protection, but these values are not interchangeable.

Source: [OAuth 2.0 Security Best Current Practice, RFC 9700](https://datatracker.ietf.org/doc/html/rfc9700)

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

**Q:** Why does a signed metadata file still need a trust decision, and how should signing-key rollover work?

**A:** A metadata signature is useful only when verified against a key already trusted through an authenticated process. Validate the expected entity and endpoints, then introduce replacement keys through an explicit overlap and rollover policy; metadata received from an unknown source does not establish its own trust.

**Q:** Why can a duplicate SAML response pass during a race even when `InResponseTo` validation is enabled?

**A:** Node-SAML 5.1.0 checks and removes the request ID in separate cache calls, so concurrent requests can both observe it before removal. Serialize validation by request ID across instances or use a validator/cache contract with atomic consume, and independently enforce an atomic assertion-ID replay check.

**Q:** Does a matching `InResponseTo` prove that the response returned to the browser that started the login?

**A:** No. It proves that the response names an SP-generated request ID, but the application must separately bind the pending RelayState or transaction to the initiating browser and tenant before creating a local session.

**Q:** Which login and session failures remain when an identity provider is unavailable?

**A:** New authentication can fail while existing local sessions continue according to their policies. Define provider redundancy, session limits and emergency access rather than assuming every outage behaves identically.

## MFA, Passkeys & WebAuthn

Source: [MFA, Passkeys & WebAuthn](20.5.1.08-mfa-passkeys-webauthn.md)

**Q:** Why must MFA combine distinct factor categories?

**A:** Two proofs from one category are not two factors. Distinct factors can limit some independent compromise paths, but shared devices, phishing and account recovery can still correlate failures.

**Q:** How does WebAuthn's origin and relying-party binding resist phishing?

**A:** The RP ID scopes the credential, while the client origin identifies the calling website and includes its scheme, host and port. The server checks the fresh challenge, RP ID hash, client origin and signature; accepting an unexpected origin weakens the boundary.

**Q:** When does a passkey ceremony count as multi-factor authentication or meet AAL3?

**A:** The credential name alone does not establish either claim. Check whether user verification was performed and what factors the applicable policy requires. NIST AAL3 requires phishing-resistant public-key authentication with a non-exportable, hardware-protected key, so a syncable passkey cannot meet that level.

**Q:** What changes when a passkey can sync across devices?

**A:** The credential remains RP-scoped, but the sync provider, its account security and recovery become part of the trust model. NIST treats syncable keys as exportable, which rules them out for AAL3.

Sources: [W3C WebAuthn Level 3](https://www.w3.org/TR/webauthn-3/), [NIST SP 800-63B-4 AAL](https://pages.nist.gov/800-63-4/sp800-63b/aal/), [NIST syncable authenticators](https://pages.nist.gov/800-63-4/sp800-63b/syncable/)

**Q:** What credential material does a passkey server store, and what risks remain after a breach?

**A:** The server retains public-key verification material rather than a reusable password. A breach can still expose personal data, sessions or modified registration state; passkeys do not remove those risks.

## RBAC (Role-Based Access Control)

Source: [RBAC (Role-Based Access Control)](20.5.1.09-rbac-abac.md); [NIST RBAC FAQs](https://csrc.nist.gov/Projects/role-based-access-control/faqs); [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html).

**Q:** When does role membership provide a useful permission model?

**A:** RBAC is useful when permissions map to stable responsibilities. Core RBAC also models sessions and active roles; the service must still scope access to the particular object and tenant. A group that only collects users is not automatically an RBAC role.

**Q:** When do resource or environment attributes require more than a role check?

**A:** An operation may depend on resource ownership, project membership, time or device state. Encoding every combination as a new role can create role explosion.

**Q:** How can role permissions and contextual conditions work together?

**A:** Combine them when the access invariant needs both: the role grants a capability, while trusted tenant, ownership or workflow facts constrain its use. Define which check applies where and ensure neither path bypasses the other.

## ABAC (Attribute-Based Access Control)

Source: [ABAC (Attribute-Based Access Control)](20.5.1.10-abac-access-control.md); [NIST SP 800-162](https://csrc.nist.gov/publications/detail/sp/800-162/final); [OWASP Authorization Patterns](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Patterns_Cheat_Sheet.html).

**Q:** Which attribute sets determine an ABAC access decision?

**A:** NIST describes attributes of the subject, object, requested operation and, in some cases, the environment. A policy uses the categories it needs; it does not need all four for every decision. Resolve them from trusted sources, then have the PEP enforce the result on the same object and operation.

**Q:** Why do expressive policies need tests, versioning and decision diagnostics?

**A:** Policy meaning depends on its version and on which policies apply. Test predicates and their composition, record the decision and policy version, and redact sensitive inputs from diagnostics.

**Q:** How can missing, stale or expensive attributes undermine authorization?

**A:** A missing or stale required attribute must not grant access. Preserve an evaluation error as an operational failure so it can be surfaced or retried, and define how attribute or policy changes invalidate cached decisions.

## Failure Traces

Sources: [API keys](20.5.1.03-api-keys.md), [sessions](20.5.1.04-sessions-cookies.md), [JWT](20.5.1.05-jwt.md), [OAuth/OIDC](20.5.1.06-oauth2-oidc.md), [federation](20.5.1.07-sso-saml-federation.md), [MFA](20.5.1.08-mfa-passkeys-webauthn.md), [RBAC](20.5.1.09-rbac-abac.md) and [ABAC](20.5.1.10-abac-access-control.md).

**Q:** Why can a revoked API key still pass a cached guard, and what must the contract state?

**A:** A cached record may retain an earlier active state. Specify and enforce the rejection window; destructive operations may require a current check. Prefixes identify candidates and need uniqueness, while full verifiers and ownership still decide access.

**Q:** What must a server include with an HTTP 401 response?

**A:** At least one applicable `WWW-Authenticate` challenge, as required by HTTP semantics. A 403 has different meaning: the server understood the request but refuses it.

Source: [HTTP Semantics, RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110)

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

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading. Standards cited above: [HTTP Semantics, RFC 9110](https://datatracker.ietf.org/doc/html/rfc9110).
