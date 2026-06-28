# Encryption

## Definition

Encryption is the process of converting plaintext into ciphertext using an algorithm and a key, making the data unreadable without the corresponding decryption key. It is a fundamental security mechanism that protects data confidentiality and integrity. Encryption can be symmetric (same key for encryption and decryption) or asymmetric (different keys for encryption and decryption).

In web development, encryption is used for protecting data in transit (HTTPS/TLS), data at rest (database encryption), password storage (hashing), and secure communication between services.

## Why Do We Need It?

- **Data Confidentiality**: Prevents unauthorized access to sensitive data
- **Data Integrity**: Ensures data hasn't been tampered with during transmission
- **Authentication**: Verifies the identity of communicating parties
- **Compliance**: Meets regulatory requirements (GDPR, HIPAA, PCI DSS)
- **Trust**: Builds user confidence in application security
- **Protection**: Safeguards against data breaches and interception

## How It Works

### Symmetric vs Asymmetric Encryption

```text
┌─────────────────────────────────────────────────────────────────┐
│              Symmetric vs Asymmetric Encryption                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SYMMETRIC (Same Key)                                           │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐              │
│  │ Plaintext│─────>│ Encrypt  │─────>│Ciphertext│              │
│  │          │      │ (Key K)  │      │          │              │
│  └──────────┘      └──────────┘      └────┬─────┘              │
│                                           │                     │
│  ┌──────────┐      ┌──────────┐      ┌────▼─────┐              │
│  │ Plaintext│<─────│ Decrypt  │<─────│Ciphertext│              │
│  │          │      │ (Key K)  │      │          │              │
│  └──────────┘      └──────────┘      └──────────┘              │
│                                                                 │
│  ASYMMETRIC (Key Pair)                                          │
│  ┌──────────┐      ┌──────────────┐      ┌──────────┐          │
│  │ Plaintext│─────>│ Encrypt      │─────>│Ciphertext│          │
│  │          │      │ (Public Key) │      │          │          │
│  └──────────┘      └──────────────┘      └────┬─────┘          │
│                                               │                 │
│  ┌──────────┐      ┌──────────────┐      ┌────▼─────┐          │
│  │ Plaintext│<─────│ Decrypt      │<─────│Ciphertext│          │
│  │          │      │ (Private Key)│      │          │          │
│  └──────────┘      └──────────────┘      └──────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

```

### TLS/HTTPS Handshake

```text
┌──────────┐                                    ┌──────────┐
│  Client  │                                    │  Server  │
└────┬─────┘                                    └────┬─────┘
     │                                               │
     │  1. ClientHello                               │
     │     (Supported ciphers, TLS version)          │
     │──────────────────────────────────────────────>│
     │                                               │
     │  2. ServerHello                               │
     │     (Selected cipher, certificate)            │
     │<──────────────────────────────────────────────│
     │                                               │
     │  3. Key Exchange                              │
     │     (Pre-master secret encrypted with         │
     │      server's public key)                     │
     │──────────────────────────────────────────────>│
     │                                               │
     │  4. Both derive session keys                  │
     │                                               │
     │  5. Encrypted communication                   │
     │<─────────────────────────────────────────────>│

```

### Hashing Process

```text
┌──────────┐      ┌──────────┐      ┌──────────┐
│ Password │─────>│  Hash    │─────>│  Hash    │
│          │      │ Function │      │ (Stored) │
└──────────┘      └──────────┘      └──────────┘
                        │
                   ┌────▼────┐
                   │  Salt   │
                   │ (Random)│
                   └─────────┘

```

## Code Examples

### Symmetric Encryption (AES)

```typescript
import crypto from "crypto";

// AES-256-GCM Encryption
class SymmetricEncryption {
  private algorithm = "aes-256-gcm";
  private key: Buffer;

  constructor(secret: string) {
    // Derive a 32-byte key from secret
    this.key = crypto.scryptSync(secret, "salt", 32);
  }

  encrypt(text: string): string {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv(this.algorithm, this.key, iv);

    let encrypted = cipher.update(text, "utf8", "hex");
    encrypted += cipher.final("hex");

    const authTag = cipher.getAuthTag();

    return `${iv.toString("hex")}:${authTag.toString("hex")}:${encrypted}`;
  }

  decrypt(encryptedData: string): string {
    const [ivHex, authTagHex, encrypted] = encryptedData.split(":");
    const iv = Buffer.from(ivHex, "hex");
    const authTag = Buffer.from(authTagHex, "hex");

    const decipher = crypto.createDecipheriv(this.algorithm, this.key, iv);
    decipher.setAuthTag(authTag);

    let decrypted = decipher.update(encrypted, "hex", "utf8");
    decrypted += decipher.final("utf8");

    return decrypted;
  }
}

// Usage
const encryptor = new SymmetricEncryption(process.env.ENCRYPTION_KEY!);
const encrypted = encryptor.encrypt("Sensitive data");
const decrypted = encryptor.decrypt(encrypted);

```

### Asymmetric Encryption (RSA)

```typescript
import crypto from "crypto";
import fs from "fs";

class AsymmetricEncryption {
  private privateKey: string;
  private publicKey: string;

  constructor() {
    const { publicKey, privateKey } = crypto.generateKeyPairSync("rsa", {
      modulusLength: 2048,
      publicKeyEncoding: { type: "spki", format: "pem" },
      privateKeyEncoding: { type: "pkcs8", format: "pem" },
    });

    this.publicKey = publicKey;
    this.privateKey = privateKey;
  }

  encrypt(text: string): string {
    const buffer = Buffer.from(text, "utf8");
    const encrypted = crypto.publicEncrypt(this.publicKey, buffer);
    return encrypted.toString("base64");
  }

  decrypt(encryptedData: string): string {
    const buffer = Buffer.from(encryptedData, "base64");
    const decrypted = crypto.privateDecrypt(this.privateKey, buffer);
    return decrypted.toString("utf8");
  }

  sign(data: string): string {
    const sign = crypto.createSign("SHA256");
    sign.update(data);
    sign.end();
    return sign.sign(this.privateKey, "hex");
  }

  verify(data: string, signature: string): boolean {
    const verify = crypto.createVerify("SHA256");
    verify.update(data);
    verify.end();
    return verify.verify(this.publicKey, signature, "hex");
  }
}

// Usage
const asymmetric = new AsymmetricEncryption();
const encrypted = asymmetric.encrypt("Secret message");
const decrypted = asymmetric.decrypt(encrypted);

```

### Password Hashing (bcrypt)

```typescript
import bcrypt from "bcrypt";

class PasswordHasher {
  private saltRounds: number;

  constructor(saltRounds: number = 12) {
    this.saltRounds = saltRounds;
  }

  async hash(password: string): Promise<string> {
    return bcrypt.hash(password, this.saltRounds);
  }

  async compare(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }
}

// Usage
const hasher = new PasswordHasher(12);

app.post("/register", async (req, res) => {
  const { password } = req.body;
  const hashedPassword = await hasher.hash(password);
  await db.createUser({ password: hashedPassword });
});

app.post("/login", async (req, res) => {
  const { password } = req.body;
  const user = await db.findUser(req.body.email);

  if (user && (await hasher.compare(password, user.password))) {
    // Login successful
  }
});

```

### Argon2 Password Hashing

```typescript
import argon2 from "argon2";

class Argon2Hasher {
  private options: argon2.Options = {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,
    parallelism: 4,
  };

  async hash(password: string): Promise<string> {
    return argon2.hash(password, this.options);
  }

  async verify(hash: string, password: string): Promise<boolean> {
    return argon2.verify(hash, password);
  }
}

// Usage
const argon2Hasher = new Argon2Hasher();
const hash = await argon2Hasher.hash("password123");
const isValid = await argon2Hasher.verify(hash, "password123");

```

### Encryption at Rest

```typescript
// Database field encryption
class FieldEncryption {
  private encryption: SymmetricEncryption;

  constructor(key: string) {
    this.encryption = new SymmetricEncryption(key);
  }

  encryptField(value: string): string {
    return this.encryption.encrypt(value);
  }

  decryptField(encryptedValue: string): string {
    return this.encryption.decrypt(encryptedValue);
  }
}

// Prisma middleware for transparent encryption
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();
const fieldEncryption = new FieldEncryption(process.env.FIELD_ENCRYPTION_KEY!);

prisma.$use(async (params, next) => {
  // Encrypt before write
  if (params.action === "create" || params.action === "update") {
    if (params.args.data.email) {
      params.args.data.email = fieldEncryption.encryptField(params.args.data.email);
    }
  }

  const result = await next(params);

  // Decrypt after read
  if (params.action === "findMany" || params.action === "findFirst") {
    if (Array.isArray(result)) {
      result.forEach((item) => {
        if (item.email) {
          item.email = fieldEncryption.decryptField(item.email);
        }
      });
    } else if (result?.email) {
      result.email = fieldEncryption.decryptField(result.email);
    }
  }

  return result;
});

```

## Real-World Use Cases

### 1. HTTPS/TLS

- Encrypts all data in transit between client and server
- Prevents man-in-the-middle attacks
- Required for secure web applications

### 2. Password Storage

- Never store plaintext passwords
- Use bcrypt, argon2, or scrypt with salt
- Verify passwords without decrypting

### 3. Database Encryption

- Encrypt sensitive fields (SSN, credit card numbers)
- Use transparent data encryption for full database
- Implement field-level encryption for specific data

### 4. API Communication

- Encrypt sensitive data in API requests/responses
- Use JWT with signed payloads
- Implement mutual TLS for service-to-service communication

### 5. File Storage

- Encrypt files before uploading to cloud storage
- Use envelope encryption for large files
- Implement key rotation for file encryption keys

## Common Mistakes

1. **Using MD5 or SHA1 for passwords**: These are fast hashes, not suitable for password storage

2. **Not using salt**: Enables rainbow table attacks

3. **Rolling your own crypto**: Use established libraries (crypto, bcrypt, argon2)

4. **Hardcoding encryption keys**: Never commit keys to source control

5. **Using weak encryption algorithms**: Use AES-256, not DES or 3DES

6. **Not rotating keys**: Implement key rotation for long-term security

7. **Storing keys with encrypted data**: Keep keys separate from encrypted data

8. **Not using HTTPS**: All web applications should use HTTPS

## Performance Considerations

| Aspect | Consideration |
|--------|---------------|
| AES-256-GCM | Fast, hardware-accelerated on modern CPUs |
| RSA-2048 | Slower than symmetric, use for key exchange |
| bcrypt | Intentionally slow (100ms+ per hash) |
| Argon2 | Memory-hard, slower but more secure |
| TLS Overhead | Minimal with modern hardware (< 1ms) |

## Interview Questions

### Beginner (5-10)

**Q1: What is the difference between encryption and hashing?**
A: Encryption is reversible (you can decrypt with the key). Hashing is one-way (you cannot reverse it). Encryption protects data confidentiality; hashing verifies data integrity and stores passwords.

**Q2: What is symmetric vs asymmetric encryption?**
A: Symmetric uses the same key for encryption and decryption (faster, used for bulk data). Asymmetric uses a key pair (public/private); slower, used for key exchange and digital signatures.

**Q3: Why should you never store plaintext passwords?**
A: If the database is compromised, all user passwords are exposed. Users often reuse passwords across sites, so a breach affects multiple accounts. Use bcrypt or argon2 instead.

**Q4: What is a salt in password hashing?**
A: A salt is a random value added to each password before hashing. It prevents rainbow table attacks by ensuring identical passwords have different hashes.

**Q5: What is HTTPS and why is it important?**
A: HTTPS is HTTP over TLS/SSL. It encrypts all data in transit, preventing eavesdropping and tampering. It's essential for protecting user data and building trust.

**Q6: What is the difference between AES and RSA?**
A: AES is symmetric (fast, same key). RSA is asymmetric (slower, key pair). AES is used for bulk encryption; RSA is used for key exchange and signatures.

**Q7: What is bcrypt?**
A: bcrypt is a password hashing function designed to be slow. It includes a salt and has a configurable cost factor. The slowness makes brute-force attacks impractical.

**Q8: What is a man-in-the-middle attack?**
A: An attacker intercepts communication between two parties, potentially reading or modifying data. HTTPS with valid certificates prevents MITM attacks.

**Q9: What is TLS?**
A: Transport Layer Security is a cryptographic protocol for secure communication. It provides encryption, authentication, and integrity. TLS 1.3 is the current standard.

**Q10: What is the purpose of digital signatures?**
A: Digital signatures verify the authenticity and integrity of messages. They use asymmetric cryptography: the sender signs with their private key, and the recipient verifies with the sender's public key.

### Intermediate (5-10)

**Q11: How would you implement encryption at rest for a database?**
A: Use transparent data encryption (TDE) for full database encryption. Implement field-level encryption for sensitive columns. Use envelope encryption for key management. Rotate encryption keys periodically.

**Q12: What is envelope encryption?**
A: Envelope encryption uses a data encryption key (DEK) to encrypt data, then encrypts the DEK with a key encryption key (KEK). The KEK is stored in a key management service (KMS).

**Q13: How do you securely manage encryption keys?**
A: Use a key management service (AWS KMS, HashiCorp Vault). Implement key rotation. Separate keys from encrypted data. Use hardware security modules (HSMs) for critical keys. Audit key usage.

**Q14: What is the difference between hashing algorithms for passwords?**
A: MD5/SHA1: Too fast, insecure. bcrypt: Good, widely used. Argon2: Memory-hard, more resistant to GPU attacks. scrypt: Memory-hard alternative. Always use salt.

**Q15: How does TLS 1.3 differ from TLS 1.2?**
A: TLS 1.3 is faster (1-RTT handshake), more secure (removed weak ciphers), and simpler. It requires forward secrecy and removes support for legacy algorithms.

**Q16: What is forward secrecy?**
A: Forward secrecy ensures that even if a private key is compromised, past session keys cannot be derived. It uses ephemeral key exchange (DHE or ECDHE) in TLS.

**Q17: How do you encrypt data in a microservices architecture?**
A: Use mTLS for service-to-service communication. Implement API gateway encryption. Use envelope encryption for data at rest. Implement centralized key management.

**Q18: What is tokenization?**
A: Tokenization replaces sensitive data with non-sensitive tokens. The tokens have no cryptographic relationship to the original data. Used for PCI DSS compliance (credit card numbers).

**Q19: How do you encrypt files for cloud storage?**
A: Encrypt files client-side before upload. Use envelope encryption with KMS. Implement client-side encryption libraries. Verify encryption after upload.

**Q20: What is the difference between encryption at rest and in transit?**
A: At rest: data stored on disk/database is encrypted. In transit: data moving between systems is encrypted (HTTPS/TLS). Both are essential for comprehensive security.

### Senior (10-15)

**Q21: Design a comprehensive encryption strategy for a healthcare application.**
A: Use TLS 1.3 for all communication. Implement AES-256-GCM for data at rest. Use argon2 for password hashing. Implement field-level encryption for PHI. Use HSMs for key management. Maintain audit logs.

**Q22: How would you implement key rotation without downtime?**
A: Use envelope encryption with multiple key versions. Implement key versioning in the encryption service. Rotate keys gradually. Support decryption with old keys. Remove old keys after migration.

**Q23: Design a system for end-to-end encryption in a messaging application.**
A: Use the Signal Protocol or similar. Implement key exchange (X3DH). Use Double Ratchet for message encryption. Store keys on device. Implement key backup and recovery.

**Q24: How would you handle encryption in a multi-tenant system?**
A: Use tenant-specific encryption keys. Implement key isolation per tenant. Use envelope encryption with tenant-scoped KEKs. Audit cross-tenant key access. Implement tenant key rotation.

**Q25: Explain the security implications of hardware security modules (HSMs).**
A: HSMs provide tamper-resistant key storage. Keys never leave the HSM. They perform cryptographic operations internally. FIPS 140-2 certified. Used for CA operations, payment processing, and critical key management.

**Q26: Design a zero-knowledge encryption system.**
A: Derive encryption keys from user passwords client-side. Never send passwords to server. Use SRP (Secure Remote Password) for authentication. Implement key escrow for recovery.

**Q27: How would you implement encryption for a real-time collaboration tool?**
A: Use per-document encryption keys. Implement key sharing for collaboration. Use E2E encryption for sensitive content. Implement key rotation for document updates. Balance security with performance.

**Q28: Explain the impact of quantum computing on encryption.**
A: Quantum computers can break RSA and ECC using Shor's algorithm. Symmetric encryption (AES) is less affected (Grover's algorithm reduces effective key length). Plan for post-quantum cryptography.

**Q29: Design an encryption system for IoT devices with limited resources.**
A: Use lightweight cryptographic algorithms. Implement hardware-based key storage. Use DTLS for communication. Implement secure boot. Use certificate-based authentication.

**Q30: How would you implement encryption for a financial trading platform?**
A: Use HSMs for transaction signing. Implement real-time encryption for market data. Use low-latency TLS. Implement audit logging. Meet regulatory requirements (MiFID II, SOX).

### FAANG-style (5-10)

**Q31: Design an encryption system for a global platform with billions of users.**
A: Use regional KMS deployments. Implement distributed key management. Use hardware acceleration for encryption. Implement key caching. Monitor key usage at scale.

**Q32: How would you implement encryption for a system requiring 99.999% availability?**
A: Use redundant KMS deployments. Implement key caching with failover. Use async encryption for non-critical paths. Implement circuit breakers. Deploy across multiple regions.

**Q33: Design a post-quantum encryption migration strategy.**
A: Inventory current cryptography. Implement hybrid encryption (classical + post-quantum). Use crypto-agile libraries. Plan for algorithm migration. Test performance impact.

**Q34: How would you handle encryption in a system with strict latency requirements (< 1ms)?**
A: Use hardware acceleration (AES-NI). Implement key caching. Use session resumption in TLS. Optimize cryptographic operations. Profile and benchmark.

**Q35: Design a key management system for a cloud-native application.**
A: Use cloud KMS (AWS KMS, GCP KMS). Implement envelope encryption. Use IAM for key access control. Implement key rotation. Monitor key usage. Implement disaster recovery.

### Follow-ups (5-10)

**Q36: How would your encryption strategy change if you needed to support legacy systems?**
A: Implement encryption gateways. Use protocol translation. Support multiple TLS versions. Implement backward compatibility. Plan for legacy system upgrades.

**Q37: If hardware acceleration was unavailable, how would you optimize encryption?**
A: Use software-optimized implementations. Implement caching. Use lighter algorithms where possible. Profile bottlenecks. Consider hardware upgrades.

**Q38: How would you implement encryption for a system with regulatory data retention requirements?**
A: Implement long-term key archival. Use escrow for recovery keys. Maintain encryption for archived data. Implement secure deletion. Audit compliance.

**Q39: How would your approach change for a system handling classified information?**
A: Use NSA-approved algorithms (Suite B). Implement Type 1 encryption for classified data. Use HSMs with FIPS 140-2 Level 4. Implement strict access controls. Maintain audit trails.

**Q40: If encryption was causing performance issues, what optimizations would you apply?**
A: Profile cryptographic operations. Use hardware acceleration. Implement key caching. Use session resumption. Optimize cipher suites. Consider asymmetric encryption for critical paths only.

## Summary

Encryption is fundamental to protecting data confidentiality, integrity, and authentication. Key takeaways:

- Use AES-256-GCM for symmetric encryption
- Use RSA-2048+ or ECC for asymmetric encryption
- Never store plaintext passwords; use argon2 or bcrypt
- Always use salt with password hashing
- Implement TLS 1.3 for all communication
- Use envelope encryption for key management
- Rotate encryption keys regularly
- Never roll your own crypto

## Cheat Sheet

| Use Case | Algorithm/Protocol |
|----------|-------------------|
| Password Storage | Argon2id or bcrypt |
| Data at Rest | AES-256-GCM |
| Data in Transit | TLS 1.3 |
| Key Exchange | RSA-2048 or ECDHE |
| Digital Signatures | RSA-2048 or ECDSA |
| File Encryption | AES-256-GCM |
| API Authentication | JWT with RS256 |
| Database Encryption | TDE or field-level AES |

## References & Learn More

- [OWASP Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
- [AES Encryption - Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [RSA Algorithm - Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [TLS 1.3 Specification - RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446)
- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
