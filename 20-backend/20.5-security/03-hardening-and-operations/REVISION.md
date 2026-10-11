<!-- section: Security | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-4_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Security — Hardening And Operations Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Encryption, Hashing & TLS

Source: [Encryption, Hashing & TLS](20.5.3.01-encryption.md)

**Q:** Why does symmetric encryption require a key-distribution plan?

**A:** Both endpoints need appropriate secret key material. Use an established key-agreement and authentication protocol or managed key distribution; do not invent an exchange or assume a fixed performance ratio.

**Q:** Why should encrypted application data also have integrity protection?

**A:** Authenticated encryption detects modified ciphertext in addition to hiding plaintext. Use a vetted construction such as AES-GCM with its nonce rules; encryption alone can leave tampering undetected.

**Q:** How can weak key management defeat a sound encryption algorithm?

**A:** An attacker who can retrieve or replace keys can bypass the intended confidentiality boundary. Restrict key access, separate responsibilities, rotate deliberately and inspect logs and backups for exposure.

## Web Security Headers & HTTPS

Source: [Web Security Headers & HTTPS](20.5.3.02-web-security.md)

**Q:** How can response headers constrain browser behavior?

**A:** Content Security Policy (CSP) constrains eligible scripts and resource loads; HTTP Strict Transport Security (HSTS) records an HTTPS-only policy; `X-Content-Type-Options: nosniff` and framing directives affect supported browser behavior. Each has a specific scope and cannot replace server authorization, redirect validation or parser hardening.

Source: [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html) · [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

**Q:** What must be true for a nonce-based CSP to authorize only the intended inline script?

**A:** Generate a hard-to-guess nonce per response, put the same value in the CSP header and trusted script tag, and do not attach it to untrusted markup. Caches must not mix the body and header or make a nonce reusable across responses.

Source: [Helmet CSP nonce example](https://helmet.js.org/faq/csp-nonce-example/) · [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)

**Q:** What is the difference between `frame-ancestors` and `frame-src`?

**A:** `frame-ancestors` restricts which sites may embed this response; `frame-src` restricts which frame sources this page may load. The directives govern opposite sides of the framing relationship.

Source: [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)

**Q:** Which security assumptions depend on authenticated HTTPS transport?

**A:** Transport Layer Security (TLS) encrypts the connection and, after successful certificate validation, lets the browser authenticate the server. A browser learns HSTS from a secure response for later visits; first-contact protection requires the domain to be included in a browser preload list. `includeSubDomains` also commits descendant hosts to HTTPS.

Source: [OWASP HSTS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Strict_Transport_Security_Cheat_Sheet.html)

**Q:** Why do CORS and CSRF require separate decisions for a cookie-authenticated API?

**A:** Cross-Origin Resource Sharing (CORS) controls whether browser script can read a response, while cross-site request forgery (CSRF) defenses establish whether an automatically credentialed state change came from an allowed request context. A simple cross-origin request may reach the server even when its response is hidden from script.

Source: [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) · [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)

**Q:** Why should a redirect choice map to a server-owned destination instead of passing a path-prefix check?

**A:** URL parsing normalizes ambiguous forms, so raw prefix tests can accept a destination that is not the intended local route. Prefer an opaque ID mapped server-side; if external targets are required, compare parsed scheme, canonical host and port against an allowlist.

Source: [OWASP Unvalidated Redirects Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html)

**Q:** What XML parser controls matter when processing untrusted documents?

**A:** Disable document type definitions (DTDs) and external-entity resolution where possible. Also restrict external access during validation or transformation, and bound parser work. A network-only setting may leave local-file access or other parser features enabled, so verify the specific library and version.

Source: [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)

**Q:** Why must a security review examine framework and deployment defaults?

**A:** Defaults and route syntax vary by framework version and deployment adapter. Inspect the headers actually emitted after proxy/CDN processing, then permit required behavior deliberately and test it on the routes that serve browser content.

Source: [Express 5 migration guide](https://expressjs.com/en/guide/migrating-5/) · [Helmet CSP nonce example](https://helmet.js.org/faq/csp-nonce-example/)

## Threat Modeling — STRIDE & Attack Surfaces

Source: [Threat Modeling — STRIDE & Attack Surfaces](20.5.3.03-threat-modeling-stride.md)

Sources: [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html) · [Microsoft Security Development Lifecycle](https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-security-development-lifecycle)

**Q:** Why must a threat model identify assets and trust boundaries before choosing defenses?

**A:** The model needs to know what must be protected, who can interact and where trust changes. Apply STRIDE categories to relevant system elements and flows rather than assuming one threat per boundary.

**Q:** How does a threat category help select a mitigation?

**A:** A category suggests controls such as authentication for spoofing or integrity checks for tampering. Select and verify defenses against the concrete attack path, assigning residual risk and ownership.

**Q:** Does a STRIDE category tell you how severe or likely a threat is?

**A:** No. STRIDE helps identify and classify a threat. Prioritize it using the affected asset, plausible impact, exposure, attacker capability, existing controls and uncertainty; record the owner and evidence for the response.

**Q:** How does an attack surface differ from a trust boundary?

**A:** The attack surface is the set of reachable entry points and exposed interfaces an attacker may use. A trust boundary marks where identity, authority or control assumptions change. A boundary helps locate paths that need analysis; it is not itself a control.

**Q:** Which design changes should trigger a threat-model review?

**A:** Changes to assets, data flows, authentication, dependencies or deployment boundaries can invalidate assumptions. Review the affected model during design changes and after incidents.

## Secrets Management

Source: [Secrets Management](20.5.3.04-secrets-management.md)

Sources: [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) · [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/) · [External Secrets v1](https://external-secrets.io/v1.0.0/api/externalsecret/) · [Vault dynamic credential leases](https://developer.hashicorp.com/vault/tutorials/db-credentials/manage-dynamic-leases) · [AWS KMS Sign API](https://docs.aws.amazon.com/kms/latest/APIReference/API_Sign.html)

**Q:** Why must a secret exposed in source control be revoked or rotated?

**A:** Removing a file does not revoke copies in history, clones or logs. Treat the credential as exposed, revoke or rotate it, inspect its use and then remove retained copies where practical.

**Q:** How does a secrets manager control both storage and access?

**A:** A secrets manager typically protects stored values, restricts retrieval by workload identity and emits or integrates access-audit events where supported. Lease and rotation features can shorten exposure, but a compromised authorized workload can still retrieve permitted secrets.

**Q:** How should least privilege apply to secret retrieval and use?

**A:** Give each workload access only to the secrets and operations it needs. Prefer short-lived credentials when supported and restrict both secret retrieval and the authority the credential grants.

**Q:** What must a database credential rotation do after the new value is published?

**A:** Consumers must fetch or receive it, establish and verify replacement connections, and drain old connections before the old credential is revoked. A projected volume updates eventually unless it uses `subPath`, and the application must reload the changed file; environment variables require a Pod restart. Neither delivery method replaces existing database sessions, so test the destination and pool behavior.

## Vulnerability Management & Patch Governance

Source: [Vulnerability Management & Patch Governance](20.5.3.05-vulnerability-management-patch-governance.md)

Sources: [FIRST CVSS v3.1](https://www.first.org/cvss/v3.1/specification-document) · [FIRST CVSS v4.0](https://www.first.org/cvss/v4.0/) · [FIRST EPSS](https://www.first.org/epss/) · [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) · [Syft SBOM generator](https://github.com/anchore/syft) · [Trivy SBOM and scanning](https://trivy.dev/docs/latest/guide/supply-chain/sbom/)

**Q:** Why must vulnerability management include application dependencies?

**A:** Dependencies and transitive components expand the executing code and attack surface. Inventory and scan them, then assess whether a finding is present, reachable and relevant to the deployed service.

**Q:** How do ownership and patch deadlines improve remediation reliability?

**A:** Assign an owner, risk-based target date and verified closure criteria. Exceptions need approval and expiry; exploitation timing varies, so a deadline does not substitute for current threat evidence.

**Q:** Why should vulnerability prioritization consider exposure and exploitability?

**A:** Severity is one input alongside known exploitation, exposure, reachability and compensating controls. Document uncertainty and prioritize the concrete threat without dismissing a high-severity finding merely because exploitation has not been observed.

**Q:** What does an SBOM prove about the deployed release?

**A:** It records components within the generator's declared scope. Bind it to the exact immutable artifact digest, and assess its coverage and creation inputs; an SBOM does not by itself prove completeness or deployment.

**Q:** How do you close a critical dependency finding after a patch?

**A:** Build and deploy a new immutable artifact, confirm the fixed component version in that artifact, rescan its digest, and verify the intended service is running it. Record the evidence and any remaining exposure; a clean source branch alone does not close the production finding.

## Trace the rotation and verification boundary

Source: [Encryption](20.5.3.01-encryption.md), [Web security](20.5.3.02-web-security.md), [Threat modeling](20.5.3.03-threat-modeling-stride.md), [Secrets management](20.5.3.04-secrets-management.md), [Vulnerability management](20.5.3.05-vulnerability-management-patch-governance.md).

**Q:** Why does moving encrypted patient 42 data into patient 43's record fail when the context is authenticated?

**A:** The additional authenticated data changes, so tag verification fails even though the key and ciphertext remain the same. Do not release plaintext before authentication completes.

**Q:** Two cached HTML responses contain different nonces. What must remain paired at the edge?

**A:** Each response's CSP header and nonce-bearing script body. Mixing versions can block legitimate execution; a fixed predictable nonce is not a repair.

**Q:** Does a gateway's valid token establish permission to read an arbitrary order?

**A:** No. The service must join trusted caller context to the stored object's tenant and authorized relationship, then project permitted properties.

**Q:** Why can't a KMS signature be passed to `jwt.sign` as the private key?

**A:** Amazon Web Services (AWS) Key Management Service (KMS) returns signature bytes over the caller-supplied input, not a private key. A JSON Web Signature (JWS) signer must sign the exact `base64url(protected-header).base64url(payload)` bytes with the selected algorithm and serialize the signature in JWS's required format; Elliptic Curve Digital Signature Algorithm (ECDSA) output, for example, must be converted to fixed-width `R || S`.

**Q:** Does changing a mounted manager-backed Secret immediately replace every database session?

**A:** No. Consumer reload and pool replacement/draining need explicit handling; environment values do not update in an existing process. Destination expiry and existing session termination are separate rules.

**Q:** An unfixed critical finding disappears under a scanner option. Has exposure ended?

**A:** No. Keep it visible and assess mitigation or an owned expiring exception. Closure requires deployed remediation evidence, not a filtered report.

## Summary

Use these prompts after the reading pass to recall the hardening and operations mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md) — return to prerequisites and learning stages for keys, policy and patch recovery

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
