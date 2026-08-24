<!-- section: Security/Auth | category: Backend | tags: concept -->
[![Section](https://img.shields.io/badge/section-Auth-blue)](INDEX.md)
[![Category](https://img.shields.io/badge/category-Backend-blue)](../../INDEX.md)
[![Tags](https://img.shields.io/badge/tags-fundamentals-lightgrey)](#)

# Auth Fundamentals — Identity, Credentials & Crypto Primitives

> **TL;DR:** Authentication answers "who are you?"; authorization answers "what may you do?". Everything in auth reduces to three primitives — **hashing** (one-way verification), **encryption** (two-way confidentiality), and **signing** (integrity + non-repudiation). Passwords must be stored with a *slow, salted* hash (Argon2id/bcrypt); tokens and data at rest use encryption/signatures; transport uses TLS. Senior interviews test whether you know *which primitive for which job* and *why the naive choice fails*.
>
> **Track position:** Stage 0 of the [auth track](INDEX.md) — read this before sessions/JWT/OAuth.

---

## Definition

| Term | Meaning | Interview one-liner |
|------|---------|---------------------|
| **Authentication (AuthN)** | Verifying *identity* of a user/service | "Proving you are who you claim to be" |
| **Authorization (AuthZ)** | Verifying *permissions* of that identity | "Deciding what you're allowed to do" |
| **Identification** | Claiming an identity (username, client ID) | Comes before AuthN |
| **Credential** | Proof used for AuthN (password, OTP, biometric, key) | Something you know / have / are |
| **Hashing** | One-way function: `hash(x)` irreversible | For *verification*, never retrieval |
| **Encryption** | Two-way with a key: reversible | For *confidentiality* |
| **Signing** | Hash + private key; verified with public key | For *integrity + authenticity* |
| **MFA** | Two or more independent factors | Knows / has / is |

---

## Why Do We Need It?

- HTTP is stateless and untrusted: every request claims an identity, so every request needs proof.
- Password databases leak — the storage format determines whether leaked data is usable by attackers.
- Tokens/cookies travel over networks — primitives decide whether interception matters.
- Regulators (GDPR/DPDP/HIPAA-style regimes) require demonstrable access control + auditability.

**The failure modes you'll be asked about all come from mixing up primitives:**

| Mistake | Consequence |
|---------|-------------|
| Storing passwords with MD5/SHA-256 (fast hash) | GPU-cracked in hours after any leak |
| Encrypting passwords instead of hashing | Decryptable with the app's own key |
| Using `Math.random()` for tokens | Predictable session/token IDs |
| Rolling your own crypto ("XOR with key") | Broken immediately |
| Skipping TLS on internal hops | MITM inside the perimeter |

---

## How It Works

### 1. The three primitives

```text
HASHING (one-way) ENCRYPTION (two-way) SIGNING (integrity)
password ──► argon2 ──► digest plaintext ──AES-GCM──► ciphertext payload ──hash──► h
login attempt ──► argon2 ──► compare │key h ──sign(priv)──► sig
                          match? └──decryption──► plaintext pub verifies(sig,h)
Use: passwords, integrity checks Use: data at rest, PHI, secrets Use: JWTs, webhooks, TLS
```

### 2. Password storage done right

```text
password ──► Argon2id(password, salt, memory=64MB, iterations=3) ──► store(digest + params)
login ──► recompute with SAME params ──► timing-safe compare
```

Why slow hashes: a fast hash (SHA-256) does billions of guesses/sec on commodity GPUs; Argon2id/bcrypt are deliberately memory/time-hard, dropping that to thousands/sec.

```typescript
// Node.js — what production code looks like
import { randomBytes, timingSafeEqual } from 'node:crypto';
import argon2 from 'argon2';

// register
const hash = await argon2.hash(password, {
  type: argon2.argon2id,
  memoryCost: 65536, // 64 MB
  timeCost: 3,
  parallelism: 1,
});
// login — constant-time compare inside the lib
const ok = await argon2.verify(hash, candidatePassword);
```

```text
Stored format (self-describing): $argon2id$v=19$m=65536,t=3,p=1$<salt>$<digest>
→ lets you raise cost params later without invalidating old hashes (rehash-on-login).
```

### 3. Randomness for tokens

```typescript
import { randomBytes } from 'node:crypto';

const sessionId = randomBytes(32).toString('base64url'); // 256 bits of CSPRNG entropy
// NEVER Math.random() — not cryptographically secure.
```

### 4. Symmetric vs asymmetric (the mental model for JWT/webhooks/TLS)

| | Symmetric (AES, HMAC) | Asymmetric (RSA, ECDSA) |
|---|----------------------|--------------------------|
| Keys | One shared secret | Private (sign) + public (verify) |
| Speed | Fast | ~100–1000× slower |
| Key distribution | Hard — both sides need secret | Easy — public key is public |
| Use when | Same trust domain (sessions, webhook HMAC) | Different trust domains (JWT verified by many services, TLS, JWKS rotation) |

### 5. TLS — the non-negotiable base

Everything above is moot without TLS in transit: it gives confidentiality, integrity, and *server authentication*. Know the handshake at interview depth: certificate chain validation → key exchange (ECDHE = forward secrecy) → symmetric session keys. Internal service-to-service traffic uses mTLS (both sides present certificates).

---

## Code Examples

### Timing-safe comparison (why it exists)

```typescript
// Leaks information via early exit (timing side channel)
if (userInputHash === storedHash) { ... }

// Constant-time
import { timingSafeEqual } from 'node:crypto';
const a = Buffer.from(userInputHash);
const b = Buffer.from(storedHash);
if (a.length === b.length && timingSafeEqual(a, b)) { ... }
```

### Credential-stuffing defense stack

```text
1. Argon2id verify (slow by design → natural throttle)
2. Per-account lockout/backoff (exponential)
3. Per-IP + per-device rate limiting
4. Check password against breached-corpus (haveibeenpwned k-anonymity API)
5. MFA prompt on new device/IP
```

---

## Real-World Use Cases

| Scenario | Primitive choice | Why |
|----------|------------------|-----|
| Clinic SaaS storing clinician passwords | Argon2id, params versioned | Leak-resistant; upgradeable via rehash-on-login |
| Payment webhook from provider | HMAC-SHA256 signature over raw body | Shared secret known only to both parties; raw body avoids canonicalization bugs |
| Microservices verifying user JWTs | RS256/ES256 + JWKS | Services verify with public key; issuer keeps private key; rotate without redeploying everyone |
| PHI columns at rest | AES-256-GCM envelope encryption | Confidentiality + tamper detection (GCM auth tag) |
| Session IDs | 256-bit CSPRNG | Unpredictability is the whole defense |

> Healthcare-grade pattern worth citing in interviews: per-row DEK encrypts each record; a KEK wraps the DEKs — rotating the KEK means re-wrapping small DEKs, not re-encrypting the whole dataset (envelope encryption).

---

## Common Mistakes

| Mistake | Why it fails | Instead |
|-----------|--------------|-----------|
| SHA-256 for passwords | Too fast → brute-forceable | Argon2id / bcrypt / scrypt |
| Salt = username or constant | Rainbow tables per-app | Unique random salt per password |
| Base64 "encryption" | Encoding ≠ encryption | AES-GCM with real KMS-managed keys |
| Secrets in env files committed to git | Permanent leak | Secret manager + rotation |
| Comparing hashes with `===` | Timing attack | `timingSafeEqual` |
| Unlimited login attempts | Credential stuffing | Rate limit + backoff + lockout |
| "We have HTTPS internally" as design | Insider/LMITM risk remains | mTLS or zero-trust service mesh |

---

## Best Practices

- **Deny by default**: an unauthenticated request has no privileges anywhere in the pipeline.
- **Layer defenses**: TLS → credential check → rate limits → session/token issuance → authorization → row-level scoping. Each layer assumes the previous can fail.
- **Version your crypto parameters** so algorithms/costs can evolve (stored alongside each hash/token header).
- **Log security events** (login success/failure, token refresh, permission denial) to an append-only audit trail — but never log passwords or full tokens.
- **Rehearse rotation**: keys, certificates, and signing credentials must be rotatable without downtime.

---

## Performance Considerations

- Argon2id at 64MB memory × N cores: budget concurrent logins accordingly (this is why login endpoints get dedicated rate limits and queues at scale).
- Verify-cost asymmetry is intentional: make *verification* expensive once per login, keep *per-request* checks cheap (JWT signature check ≈ sub-ms; DB session lookup ≈ 0.5–2ms with Redis).
- Offload password hashing from the request path if needed (worker queue) — but never weaken parameters to hit latency targets.

---

## Summary

- AuthN ≠ AuthZ; interviews probe whether you keep them separate in design and in code enforcement points.
- Hashing verifies, encryption conceals, signatures authenticate — pick by job, never invent.
- Slow salted hashes (Argon2id) for passwords; CSPRNG for anything that must be unpredictable; timing-safe compares everywhere.
- TLS/mTLS is the floor, not the ceiling.

---

## Cheat Sheet

```text
PASSWORDS → Argon2id (m=64MB,t=3) · unique salt · rehash-on-login upgrade
TOKENS → randomBytes(32) · CSPRNG only
INTEGRITY → HMAC (shared trust) · ES256/RS256 (distributed trust)
CONFIDENT. → AES-256-GCM · envelope encryption for regulated fields
TRANSPORT → TLS everywhere · mTLS service-to-service
COMPARE → timingSafeEqual
LOGIN → rate limit + backoff + breach check + MFA step-up
NEVER → Math.random() for tokens · fast-hash passwords · homegrown crypto
```

---

## See Also

Next in track: [Sessions & Cookies](sessions-cookies.md) → [JWT](jwt.md) → [OAuth2/OIDC](oauth2-oidc.md) → [RBAC/ABAC](rbac-abac.md)
Deep dive: [Encryption, Hashing & TLS](../20.5.06-encryption.md) · [Secrets Management](../20.5.11-secrets-management.md) · [Web Security](../20.5.09-web-security.md)

---

## References & Learn More

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [RFC 9106 — Argon2 Memory-Hard Function](https://datatracker.ietf.org/doc/html/rfc9106)
- [Cloudflare — What is TLS?](https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/)
- [MDN — Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API)
- [Google — Identity Best Practices](https://cloud.google.com/architecture/identity/checklist-reviews-enterprise-authentication)
