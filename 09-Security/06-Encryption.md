---
section: Security
category: Architecture
tags: [concept]
---

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

---

## See Also
- [REST APIs](../07-REST-API/)
- [System Design](../11-System-Design/)

## References & Learn More

- [OWASP Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/)
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
- [AES Encryption - Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
- [RSA Algorithm - Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem)))
- [TLS 1.3 Specification - RFC 8446](https://datatracker.ietf.org/doc/html/rfc8446)
- [OWASP Transport Layer Protection Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html)
