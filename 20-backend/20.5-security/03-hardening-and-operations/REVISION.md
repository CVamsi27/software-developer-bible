<!-- section: Security | category: Reference | tags: revision | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-3_min-informational)](#)
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

**A:** CSP constrains supported execution and resource loads; HSTS influences transport; MIME and framing directives address other browser behaviors. Each has a specific scope and must be tested against the intended page behavior.

**Q:** Which security assumptions depend on authenticated HTTPS transport?

**A:** TLS protects confidentiality and authenticates the transport peer under the certificate contract. HSTS learned over HTTPS protects later connections; preloading can protect a first visit when supported and appropriate.

**Q:** Why must a security review examine framework and deployment defaults?

**A:** Defaults vary by component and version. Check the controls actually emitted and enforced, then permit required behavior deliberately rather than assuming a framework's default policy matches the threat model.

## Threat Modeling — STRIDE & Attack Surfaces

Source: [Threat Modeling — STRIDE & Attack Surfaces](20.5.3.03-threat-modeling-stride.md)

**Q:** Why must a threat model identify assets and trust boundaries before choosing defenses?

**A:** The model needs to know what must be protected, who can interact and where trust changes. Apply STRIDE categories to relevant system elements and flows rather than assuming one threat per boundary.

**Q:** How does a threat category help select a mitigation?

**A:** A category suggests controls such as authentication for spoofing or integrity checks for tampering. Select and verify defenses against the concrete attack path, assigning residual risk and ownership.

**Q:** Which design changes should trigger a threat-model review?

**A:** Changes to assets, data flows, authentication, dependencies or deployment boundaries can invalidate assumptions. Review the affected model during design changes and after incidents.

## Secrets Management

Source: [Secrets Management](20.5.3.04-secrets-management.md)

**Q:** Why must a secret exposed in source control be revoked or rotated?

**A:** Removing a file does not revoke copies in history, clones or logs. Treat the credential as exposed, revoke or rotate it, inspect its use and then remove retained copies where practical.

**Q:** How does a secrets manager control both storage and access?

**A:** A secrets manager uses identity-based retrieval policy, protected storage and audit logs. Supported lease and rotation features can shorten exposure, but a compromised authorized workload can still retrieve permitted secrets.

**Q:** How should least privilege apply to secret retrieval and use?

**A:** Give each workload access only to the secrets and operations it needs. Prefer short-lived credentials when supported and restrict both secret retrieval and the authority the credential grants.

## Vulnerability Management & Patch Governance

Source: [Vulnerability Management & Patch Governance](20.5.3.05-vulnerability-management-patch-governance.md)

**Q:** Why must vulnerability management include application dependencies?

**A:** Dependencies and transitive components expand the executing code and attack surface. Inventory and scan them, then assess whether a finding is present, reachable and relevant to the deployed service.

**Q:** How do ownership and patch deadlines improve remediation reliability?

**A:** Assign an owner, risk-based target date and verified closure criteria. Exceptions need approval and expiry; exploitation timing varies, so a deadline does not substitute for current threat evidence.

**Q:** Why should vulnerability prioritization consider exposure and exploitability?

**A:** Severity is one input alongside known exploitation, exposure, reachability and compensating controls. Document uncertainty and prioritize the concrete threat without dismissing a high-severity finding merely because exploitation has not been observed.

## Trace the rotation and verification boundary

Source: [Encryption](20.5.3.01-encryption.md), [Web security](20.5.3.02-web-security.md), [Threat modeling](20.5.3.03-threat-modeling-stride.md), [Secrets management](20.5.3.04-secrets-management.md), [Vulnerability management](20.5.3.05-vulnerability-management-patch-governance.md).

**Q:** Why does moving encrypted patient 42 data into patient 43's record fail when the context is authenticated?

**A:** The additional authenticated data changes, so tag verification fails even though the key and ciphertext remain the same. Do not release plaintext before authentication completes.

**Q:** Two cached HTML responses contain different nonces. What must remain paired at the edge?

**A:** Each response's CSP header and nonce-bearing script body. Mixing versions can block legitimate execution; a fixed predictable nonce is not a repair.

**Q:** Does a gateway's valid token establish permission to read an arbitrary order?

**A:** No. The service must join trusted caller context to the stored object's tenant and authorized relationship, then project permitted properties.

**Q:** Why can't a KMS signature be passed to `jwt.sign` as the private key?

**A:** It is already a signature over a precise message. A JWS integration must sign the encoded header/payload input with the matching algorithm and assemble the correctly represented signature.

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
