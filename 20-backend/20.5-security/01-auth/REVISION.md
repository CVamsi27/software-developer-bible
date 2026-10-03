<!-- section: Security | category: Reference | tags: revision| general-importance: foundational| general-importance: foundational | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Security — Auth Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Auth Fundamentals — Identity, Credentials & Crypto Primitives

Source: [Auth Fundamentals — Identity, Credentials & Crypto Primitives](20.5.1.01-auth-fundamentals.md)

**Q:** What core constraint explains why the server must verify a claim it didn't witness. governs auth fundamentals — identity, credentials & crypto primitives?

**A:** "This is Vamsi" is just bytes; proof requires either *something only the user has* (knowledge, device, biometric) presented to a verifier, or a *cryptographic token* previously issued by the verifier. Every auth scheme is one of these.

**Q:** What core constraint explains why credentials are attack surface by existing. governs auth fundamentals — identity, credentials & crypto primitives?

**A:** Anything presented can be stolen, phished, replayed, or guessed — so the entire discipline is reducing what a stolen credential is worth: hashing (server breach ≠ credential theft), expiry, rotation, MFA (possession factor), and rate limits.

**Q:** What core constraint explains why authentication and authorization are different questions. governs auth fundamentals — identity, credentials & crypto primitives?

**A:** "Who are you?" ≠ "what may you do?" — conflating them (roles baked into identity, scopes implied by login) couples systems that change at different rates. RBAC/ABAC  exist because authorization deserves its own model.

## HTTP Basic & Digest Authentication

Source: [HTTP Basic & Digest Authentication](20.5.1.02-http-basic-digest-auth.md)

**Q:** What core constraint explains why http has no login concept — credentials ride *with every request*. governs http basic & digest authentication?

**A:** Basic sends base64 (not encryption!) of user:password; protection comes entirely from TLS. That's the minimal viable credential transport: universal support, zero redirects, no session infrastructure.

**Q:** What core constraint explains why the password itself is the weakness. governs http basic & digest authentication?

**A:** Sending reusable secrets on every request means one TLS bypass or log leak = total compromise. Digest's hash challenge was the pre-TLS mitigation; it's obsolete because TLS made "never send the reusable secret" achievable properly (tokens, → 20.5.1.05).

**Q:** What core constraint explains why no logout, no expiry, no granularity. governs http basic & digest authentication?

**A:** Because credentials are replayed per-request and browsers cache them, the server controls nothing after the fact — the missing capabilities are exactly what session/token systems were invented to provide.

## API Keys

Source: [API Keys](20.5.1.03-api-keys.md)

**Q:** What core constraint explains why a key identifies an app, not a human. governs api keys?

**A:** No user context, no consent flow, no scopes-per-user — that's its honesty and its limit. Whenever you need "acting on behalf of user X," keys alone are the wrong tool (OAuth, → 20.5.1.06).

**Q:** What core constraint explains why a static secret is only as safe as its storage. governs api keys?

**A:** Keys leak via repos, logs, and frontend bundles — hence server-side-only, environment storage, rotation, and scoping (keys that can only read) as the entire defense. Detection (leak scanners) matters as much as prevention because leaks are statistical certainties.

**Q:** What core constraint explains why keys are infrastructure auth, not user auth. governs api keys?

**A:** Rate limiting, billing, and service identification are what they're for — using them as login credentials couples app identity to user identity and blocks per-user permission models.

## Sessions & Cookies

Source: [Sessions & Cookies](20.5.1.04-sessions-cookies.md)

**Q:** What core constraint explains why the server must remember the login — the only question is where. governs sessions & cookies?

**A:** Server-side session store (instant revocation, every request pays a lookup) vs client-side token (no lookup, revocation is hard). Sessions pick the server-side half of that trade.

**Q:** What core constraint explains why the cookie is the transport because browsers made it one. governs sessions & cookies?

**A:** Automatic sending is both the feature (no JS needed, HttpOnly hides it from XSS) and the liability (CSRF: other origins' requests carry it too — hence SameSite, CSRF tokens, → 20.5.2.02).

**Q:** What core constraint explains why session fixation and hijacking are the same fact governs sessions & cookies?

**A:** the session ID *is* the identity for its lifetime. Protect it like a password — rotate on login, secure transport, short TTL with sliding renewal.

## JWT (JSON Web Tokens)

Source: [JWT (JSON Web Tokens)](20.5.1.05-jwt.md)

**Q:** What core constraint explains why the token carries its own proof. governs jwt (json web tokens)?

**A:** Sign the payload (HMAC: shared secret; RSA/ECDSA: private sign, public verify) and any holder of the key can verify offline — no session DB, which is what makes stateless horizontal scaling trivial and is the entire point.

**Q:** What core constraint explains why the cost is the mirror: you cannot unissue a token. governs jwt (json web tokens)?

**A:** No central store means no instant revocation — mitigations (short TTL + refresh rotation, denylists, `jti`) each reintroduce some state. The senior position: *revocation requirements dictate statefulness*, not fashion.

**Q:** What core constraint explains why a jwt is signed, not encrypted. governs jwt (json web tokens)?

**A:** Anyone can read its claims (base64) — hence never put secrets in payloads, and understand `alg` confusion: the header is attacker-controlled input, so pin acceptable algorithms server-side.

## OAuth 2.0 & OpenID Connect

Source: [OAuth 2.0 & OpenID Connect](20.5.1.06-oauth2-oidc.md)

**Q:** What core constraint explains why apps need access without your password. governs oauth 2.0 & openid connect?

**A:** Sharing credentials gives away everything, forever, to everyone — so OAuth inverts it: the resource server trusts *tokens* issued by an authorization server that handled the user interaction. Password never leaves the identity provider.

**Q:** What core constraint explains why flows differ by client capability, by necessity. governs oauth 2.0 & openid connect?

**A:** Server can keep a secret → authorization code (+PKCE now, always). SPA/mobile cannot → PKCE proves possession without a secret. Backend service with no user → client credentials. Each flow exists because a trust assumption died; knowing which assumption each flow patches is the understanding.

**Q:** What core constraint explains why oidc is oauth + identity, not oauth rebranded. governs oauth 2.0 & openid connect?

**A:** OAuth answers "what may this client access?"; OIDC adds the ID token ("who is the user?") on the same rails — one protocol answering the two questions apps actually have.

## SSO, SAML & Federation

Source: [SSO, SAML & Federation](20.5.1.07-sso-saml-federation.md)

**Q:** What core constraint explains why every app holding its own user store multiplies risk and friction. governs sso, saml & federation?

**A:** One IdP centralizes the credential attack surface, MFA, and offboarding (deprovision once, everywhere) — SSO is the org-scale application of "one fact, one place" .

**Q:** What core constraint explains why federation needs a trust contract. governs sso, saml & federation?

**A:** SAML (XML, enterprise standard) and OIDC (modern, web-first) differ in syntax, not in structure: principal, IdP assertion, SP reliance on signatures. The metadata exchange *is* the trust root — everything else is protocol.

**Q:** What core constraint explains why the single point of failure is chosen, not eliminated. governs sso, saml & federation?

**A:** IdP down = nobody logs in (hopefully — cached sessions buy hours, not days). That concentration is the trade SSO makes deliberately.

## MFA, Passkeys & WebAuthn

Source: [MFA, Passkeys & WebAuthn](20.5.1.08-mfa-passkeys-webauthn.md)

**Q:** What core constraint explains why factors are independent because they fail independently. governs mfa, passkeys & webauthn?

**A:** Knowledge (password) and possession (phone, key) and inherence (biometric) are compromised by different attack classes — which is why combining them defeats credential stuffing wholesale. "Something you know + something you have" is the minimum honest pair.

**Q:** What core constraint explains why phishing is the dominant attack, so bind to origin. governs mfa, passkeys & webauthn?

**A:** OTPs are phishable (user relays the code); WebAuthn/passkeys sign *the origin* — a credential created for evil.com cannot be exercised on your-bank.com. Origin-binding is the structural fix, not user education.

**Q:** What core constraint explains why no shared secret means nothing to steal from the server. governs mfa, passkeys & webauthn?

**A:** Passkeys store public keys; a server breach yields nothing reusable — eliminating phishing and server-breach reuse in one design.

## RBAC (Role-Based Access Control)

Source: [RBAC (Role-Based Access Control)](20.5.1.09-rbac-abac.md)

**Q:** What core constraint explains why rbac: role membership. governs rbac (role-based access control)?

**A:** When the org chart is the truth ("managers approve expense reports"), roles map cleanly and audits are easy — the model's whole value is reviewability. Its ceiling: roles explode combinatorially when context matters ("manager *of that project*, *during business hours*").

**Q:** What core constraint explains why abac: attributes of user, resource, environment. governs rbac (role-based access control)?

**A:** When context is the truth, policies evaluate attributes — expressive but hard to audit ("why was this denied?"). Every ABAC policy is a boolean function; complexity lives in policy management, not evaluation.

**Q:** What core constraint explains why hybrid is the honest answer governs rbac (role-based access control)?

**A:** (role baseline + attribute conditions), because real orgs have both static structure and contextual exceptions. ReBAC (relationship-based, Google Zanzibar style) enters when *relationships between resources* (doc in folder in team) drive decisions.

## ABAC (Attribute-Based Access Control)

Source: [ABAC (Attribute-Based Access Control)](20.5.1.10-abac-access-control.md)

**Q:** What core constraint explains why decisions are functions of (subject, resource, action, environment). governs abac (attribute-based access control)?

**A:** That four-tuple is the model's entire ontology — every "can Alice edit this doc?" reduces to evaluating a policy over those four attribute sets at request time.

**Q:** What core constraint explains why expressiveness and auditability pull in opposite directions. governs abac (attribute-based access control)?

**A:** More attributes = finer control = harder "why denied?" answers — which is why mature deployments version policies, log every decision with inputs, and test policies like code. Policy-as-code with CI is the only way to keep the combinatorics sane.

**Q:** What core constraint explains why abac's real enemy is evaluation cost and error at scale governs abac (attribute-based access control)?

**A:** attributes must be fresh (stale group membership = wrong access), complete (missing attribute = deny-by-default or hole), and the PDP must be fast — hence caching decisions with careful invalidation .

## Summary

Use these prompts after the reading pass to recall the auth mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
