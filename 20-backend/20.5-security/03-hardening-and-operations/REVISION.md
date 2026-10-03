<!-- section: Security | category: Reference | tags: revisi | role-priority: essential | general-importance: foundational -->
[![Section](https://img.shields.io/badge/section-Security-blue)](#)
[![Category](https://img.shields.io/badge/category-Reference-success)](#)
[![Tags](https://img.shields.io/badge/tags-revision-lightgrey)](#)
[![Read time](https://img.shields.io/badge/read--time-2_min-informational)](#)
[![Role priority](https://img.shields.io/badge/role--priority-Essential-brightgreen)](../../../docs/topic-importance.md)
[![General importance](https://img.shields.io/badge/general--importance-Foundational-blueviolet)](../../../docs/topic-importance.md)

# Security — Hardening And Operations Revision

Explain each mechanism before checking the answer. Revisit its source for the example and boundary conditions.

## Encryption, Hashing & TLS

Source: [Encryption, Hashing & TLS](20.5.3.01-encryption.md)

**Q:** What core constraint explains why symmetric crypto is fast but needs a shared secret governs encryption, hashing & tls?

**A:** — key distribution *is* the problem, solved by asymmetric crypto (public encrypt, private decrypt) at 1000× the cost. Real systems compose: asymmetric to agree on a symmetric key (TLS), symmetric for the data. Composition is the design pattern.

**Q:** What core constraint explains why authenticated encryption is the default, not an upgrade. governs encryption, hashing & tls?

**A:** AES-GCM/ChaCha20-Poly1305 encrypt *and* authenticate — unauthenticated modes (AES-CBC alone) are malleable, meaning tampering goes undetected. "Encrypt with the right mode" is where most home-rolled designs fail.

**Q:** What core constraint explains why key management dominates crypto math in practice. governs encryption, hashing & tls?

**A:** Key rotation, storage (KMS, HSM), separation of duties — the algorithm is the easy part; keeping keys out of repos, logs, and memory dumps is where systems actually break .

## Web Security Headers & HTTPS

Source: [Web Security Headers & HTTPS](20.5.3.02-web-security.md)

**Q:** What core constraint explains why you cannot patch the client; you can only instruct it. governs web security headers & https?

**A:** CSP, HSTS, X-Content-Type-Options, frame-ancestors are *directives to the browser* — the server's only lever over execution on someone else's machine. Each header maps to one attack class the browser could otherwise be talked into.

**Q:** What core constraint explains why https is the substrate everything else assumes. governs web security headers & https?

**A:** Without TLS, no header, cookie, or token is trustworthy in transit; HSTS exists because the *first* HTTP request is the vulnerability (SSL-strip), so the policy must be preloaded.

**Q:** What core constraint explains why defaults are the attack surface. governs web security headers & https?

**A:** Browsers permit inline scripts, framing, MIME-sniffing by default because pages need them; headers exist to *turn off* what you don't need — the security posture is "deny by default, allow explicitly.".

## Threat Modeling — STRIDE & Attack Surfaces

Source: [Threat Modeling — STRIDE & Attack Surfaces](20.5.3.03-threat-modeling-stride.md)

**Q:** What core constraint explains why you cannot defend what you haven't enumerated. governs threat modeling — stride & attack surfaces?

**A:** STRIDE is a checklist over *system facts* — Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege — one threat class per trust-boundary crossing. The diagram is the method: draw data flows, label trust boundaries, ask STRIDE at each.

**Q:** What core constraint explains why every threat pairs with a standard mitigation class governs threat modeling — stride & attack surfaces?

**A:** (authentication, integrity, logging, confidentiality, redundancy, authorization) — which is why the exercise produces actionable backlog, not fear. The output is ranked mitigations, not a document.

**Q:** What core constraint explains why it must run when the design changes governs threat modeling — stride & attack surfaces?

**A:** , because the model is of *this* system: a threat model of last year's architecture is fiction. Lighter than pen-testing; catches design flaws code review never can.

## Secrets Management

Source: [Secrets Management](20.5.3.04-secrets-management.md)

**Q:** What core constraint explains why anything in source control is compromised forever governs secrets management?

**A:** — git history is eternal, rotation is the only cure, and rotation is expensive enough that prevention (never commit) is cheaper. Env vars move the leak to logs, crash dumps, and child processes — better, not good.

**Q:** What core constraint explains why a secrets manager centralizes both storage and *access* governs secrets management?

**A:** short-lived leases, automatic rotation, audit logs of who-read-what-when. The audit trail is half the product — secret access IS security telemetry.

**Q:** What core constraint explains why least privilege applies to secrets too governs secrets management?

**A:** per-service identities, per-path permissions, TTLs. The endgame design is zero long-lived secrets in app land: workload identity minting short-lived credentials on demand.

## Vulnerability Management & Patch Governance

Source: [Vulnerability Management & Patch Governance](20.5.3.05-vulnerability-management-patch-governance.md)

**Q:** What core constraint explains why your dependencies are attack surface you didn't audit. governs vulnerability management & patch governance?

**A:** Transitively, a web app pulls thousands of packages; one vulnerable transitive dep is your breach. Scanning (SCA) exists to make the invisible inventory visible.

**Q:** What core constraint explains why patch speed is the whole game — and it's an sla, not a hero effort. governs vulnerability management & patch governance?

**A:** Exploitation follows disclosure within days; time-to-patch beats scanning frequency. Governance (severity SLAs, ownership, exceptions with expiry) is what makes patching a process instead of an all-hands.

**Q:** What core constraint explains why prioritization must be risk-based because the backlog is unbounded. governs vulnerability management & patch governance?

**A:** KEV (known-exploited) + reachability + exposure beats raw CVSS: a 9.8 with no exploit path in your runtime is *less urgent* than a 7.5 in the auth path.

## Summary

Use these prompts after the reading pass to recall the hardening and operations mechanisms and boundary constraints.

## See Also

- [Category reading flow](INDEX.md)

## References & Learn More

The linked source chapters provide detailed architectural rationale, implementation contracts, and further reading.
